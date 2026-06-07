import os
import json
import asyncio
from typing import Optional
from contextlib import asynccontextmanager

import httpx
import structlog
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)
log = structlog.get_logger()

GLPI_URL = os.getenv("GLPI_TARGET", "http://sovereign_glpi/apirest.php")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
NODE_ID = os.getenv("NODE_IDENTITY", "sov_node_santacruz_01")
GLPI_APP_TOKEN = os.getenv("GLPI_APP_TOKEN", "")
GLPI_USER_TOKEN = os.getenv("GLPI_USER_TOKEN", "")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")

INFERENCE_CONFIG = {
    "model": OLLAMA_MODEL,
    "stream": False,
    "options": {
        "temperature": 0.25,
        "top_p": 0.85,
        "repeat_penalty": 1.15,
        "num_ctx": 2048,
        "num_thread": 4,
        "num_gpu": 0,
    }
}

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "schemas")

def load_schema(name: str) -> dict:
    path = os.path.join(SCHEMA_DIR, f"{name}.json")
    with open(path) as f:
        return json.load(f)

class GLPISession:
    def __init__(self):
        self.session_token: Optional[str] = None
        self.client = httpx.AsyncClient(timeout=30.0)

    async def init_session(self) -> bool:
        try:
            headers = {
                "App-Token": GLPI_APP_TOKEN,
                "Authorization": f"user_token {GLPI_USER_TOKEN}",
                "Content-Type": "application/json"
            }
            response = await self.client.get(f"{GLPI_URL}/initSession", headers=headers)
            response.raise_for_status()
            self.session_token = response.json().get("session_token")
            log.info("glpi_session_init", status="ok", node=NODE_ID)
            return True
        except Exception as e:
            log.error("glpi_session_init_failed", error=str(e))
            return False

    async def kill_session(self):
        if self.session_token:
            try:
                await self.client.get(f"{GLPI_URL}/killSession", headers=self._headers())
                log.info("glpi_session_killed", node=NODE_ID)
            except Exception as e:
                log.warning("glpi_session_kill_failed", error=str(e))

    def _headers(self) -> dict:
        return {
            "App-Token": GLPI_APP_TOKEN,
            "Session-Token": self.session_token,
            "Content-Type": "application/json"
        }

    async def get_tickets(self, limit: int = 20) -> list:
        try:
            response = await self.client.get(
                f"{GLPI_URL}/Ticket",
                headers=self._headers(),
                params={"range": f"0-{limit-1}", "sort": "date_mod", "order": "DESC"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log.error("glpi_get_tickets_failed", error=str(e))
            return []

    async def create_ticket(self, ticket_data: dict) -> dict:
        try:
            response = await self.client.post(f"{GLPI_URL}/Ticket", headers=self._headers(), json={"input": ticket_data})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log.error("glpi_create_ticket_failed", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))

class OllamaEngine:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=120.0)

    async def is_ready(self) -> bool:
        try:
            response = await self.client.get(f"{OLLAMA_HOST}/api/tags")
            models = response.json().get("models", [])
            return any(OLLAMA_MODEL in m.get("name", "") for m in models)
        except Exception:
            return False

    async def triage_ticket(self, ticket_text: str, context_tickets: list) -> dict:
        context_block = self._build_context(context_tickets)
        try:
            ontology = load_schema("mesa_ontology")
            domain_terms = json.dumps(ontology.get("categories", {}))
        except Exception:
            domain_terms = "{}"

        prompt = f"""You are MESA, a sovereign municipal IT service management assistant.
Your job is to triage service tickets accurately and conservatively. Do not guess.

DOMAIN ONTOLOGY:
{domain_terms}

RECENT TICKET CONTEXT:
{context_block}

NEW TICKET:
{ticket_text[:500]}

Respond ONLY with valid JSON in this exact format:
{{
  "category": "string",
  "domain": "ITSM|ESM|ENERGY_UTILITIES",
  "priority": "low|medium|high|critical",
  "suggested_resolution": "string",
  "confidence": "low|medium|high",
  "reasoning": "string"
}}"""

        payload = {**INFERENCE_CONFIG, "prompt": prompt}
        try:
            response = await self.client.post(f"{OLLAMA_HOST}/api/generate", json=payload)
            response.raise_for_status()
            clean = response.json().get("response", "{}").strip()
            if clean.startswith("```"):
                lines = clean.split("\n")
                lines = [l for l in lines if not l.strip().startswith("```")]
                clean = "\n".join(lines).strip()
            return json.loads(clean)
        except Exception as e:
            log.error("ollama_inference_failed", error=str(e))
            return {"category": "uncategorized", "domain": "ITSM", "priority": "medium", "suggested_resolution": "Manual review required", "confidence": "low", "reasoning": "Inference breakdown"}

    def _build_context(self, tickets: list, max_tokens: int = 400) -> str:
        if not tickets or not isinstance(tickets, list): return "No prior context."
        lines = []
        for t in tickets[:10]:
            if isinstance(t, dict):
                lines.append(f"[{t.get('id', '?')}] {t.get('name', '')[:100]}")
        return "\n".join(lines)

class TicketRequest(BaseModel):
    title: str
    description: str
    requester: Optional[str] = "anonymous"

class TriageRequest(BaseModel):
    ticket_text: str

glpi = GLPISession()
ollama = OllamaEngine()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await glpi.init_session()
    yield
    await glpi.kill_session()
    await glpi.client.aclose()
    await ollama.client.aclose()

app = FastAPI(title="MESA Bridge", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health(): return {"status": "online", "node": NODE_ID}

@app.post("/triage")
async def triage_only(req: TriageRequest):
    recent = await glpi.get_tickets(limit=10)
    return await ollama.triage_ticket(req.ticket_text, recent)

@app.post("/tickets")
async def create_ticket(req: TicketRequest):
    recent = await glpi.get_tickets(limit=10)
    triage = await ollama.triage_ticket(f"{req.title}\n{req.description}", recent)
    ticket_data = {
        "name": req.title,
        "content": req.description,
        "urgency": 3,
        "impact": 3
    }
    result = await glpi.create_ticket(ticket_data)
    return {"ticket_id": result.get("id"), "triage": triage, "status": "created"}

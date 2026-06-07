# MESA: Municipal Enterprise Service Architecture
A sovereign, open-source ITSM/ESM platform for governments that own their future.
License: Apache 2.0
Built in Santa Cruz, CA by Paul Statchen
# MESA
## Municipal Enterprise Service Architecture

**A sovereign, open-source ITSM/ESM platform for governments that own their future.**

Built in Santa Cruz, CA. Free forever. Apache 2.0.

---

> *"The foundation of society is always built by people who love it and do it for free."*
> — Paul Statchen, Civic Scientist, Santa Cruz CA

---

## Why MESA Exists

On June 9, 2026, the Santa Cruz County Board of Supervisors considered agenda item 38: a $291,824.63 per year agreement with TeamDynamix, a cloud-based IT service management platform headquartered in Ohio.

County data would live on out-of-state servers. The county would own nothing. Prices could rise. Exit would be costly.

MESA is the alternative. Built in a few days on a Chromebook. Proven to run. Free forever.

---

## What MESA Is

MESA is a five-pillar sovereign service management platform designed specifically for municipal government:

### Pillar 1 - ITSM (IT Service Management)
- Incident management
- Service requests
- Change management
- Asset tracking and lifecycle
- Security incident response
- ITIL 4 compliant vocabulary

### Pillar 2 - ESM (Enterprise Service Management)
- Facilities management
- Human resources services
- Legal and compliance requests
- Finance and procurement workflows
- Communications and public affairs
- All departments through one unified interface

### Pillar 3 - Energy & Utilities
- Power grid monitoring and incident response
- Water and wastewater management
- Compute energy self-awareness (the system tracks its own power footprint)
- Renewable energy asset tracking
- Environmental monitoring and compliance
- Designed for municipal utilities operations

### Pillar 4 - Project Management
- Full project lifecycle tracking
- Cost ledger per project
- API handshake layer for external accounting systems (QuickBooks, municipal finance software)
- Built on GLPI's native project module
- Every project tied to financial audit trail

### Pillar 5 - Financial Audit Layer
- Transparent, tamper-evident public spending ledger
- Every ticket, project, and asset has cost attached
- Auditable by the public
- No data leaves county hardware
- Designed for the era of government transparency demands

---

## AI Architecture - Two Sovereign Tiers

### Tier 1 - Sovereign Local AI (Always On)
- Ollama running on county-owned hardware
- Zero telemetry - no data leaves the building
- Automatic ticket triage and categorization
- Priority assignment
- Resolution suggestions from knowledge base
- Works with no internet connection
- Models: Phi-3 Mini, Gemma 2B (runs on standard laptops)

### Tier 2 - Cloud AI Augmentation (Optional)
- Claude (Anthropic), Gemini (Google), GPT (OpenAI) available as optional connectors
- Explicitly opted into - never required
- Used for heavy lifting when needed
- Sovereign tier backs up cloud tier always
- If internet fails or vendor raises prices - MESA still works

The county controls the AI. The AI does not control the county.

---

## Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| ITSM/ESM Core | GLPI (GPL licensed) | System of record, ticketing, assets, projects |
| Database | MariaDB 10.11 | Sovereign relational storage |
| Local AI | Ollama + Phi-3 Mini | Zero-telemetry inference engine |
| Bridge Layer | Python FastAPI | Logic, triage, API translation |
| Network | Docker + custom bridge | Air-gapped sovereign data network |
| Mesh | DePIN architecture | Federated node network across county fleet |

---

## Network Architecture

```
┌─────────────────────────────────────────────────┐
│           BOINK INTERNAL NETWORK                │
│        (air-gapped, no internet routing)        │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ MariaDB  │◄─│   GLPI   │◄─│    Bridge    │  │
│  │(storage) │  │(ITSM/ESM)│  │ Controller  │  │
│  └──────────┘  └──────────┘  └──────┬───────┘  │
│                                     │           │
│                          ┌──────────┘           │
│                          │  ┌──────────┐        │
│                          └─►│  Ollama  │        │
│                             │(local AI)│        │
│                             └──────────┘        │
└─────────────────────────────────────────────────┘
                    │
          ┌─────────▼──────────┐
          │   DePIN Mesh Net   │
          │ (federated nodes)  │
          │                    │
          │  Every county      │
          │  computer = node   │
          └────────────────────┘
```

---

## Hardware Requirements

Designed to run on what governments already own:

| Component | Minimum |
|-----------|---------|
| RAM | 8GB |
| Storage | 20GB free |
| OS | Linux (including Chromebook Crostini) |
| GPU | Not required - CPU-only inference |
| Network | Local only - no cloud dependency |

---

## The Distributed County Vision

Every computer the county already owns - laptops, desktops, vehicles - can become a MESA node.

Combined idle compute across a county fleet creates significant processing power with zero additional hardware cost. When devices sleep at night they contribute to the mesh. The math is significant.

This is BOINC-style distributed computing applied to sovereign municipal infrastructure.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/paulstatchen10-ux/MESA.git
cd MESA

# 2. Configure
cp .env.template .env
nano .env  # Set your passwords

# 3. Create data directories
mkdir -p data/mysql_data data/glpi_files data/ollama_models

# 4. Launch
docker compose up -d

# 5. Pull AI model (first time only - ~2.3GB)
docker exec sovereign_ollama ollama pull phi3:mini

# 6. Access
# GLPI Dashboard: http://localhost:8080
# Bridge API:     http://localhost:8000
# API Docs:       http://localhost:8000/docs

# Default GLPI login: glpi / glpi
# CHANGE THIS IMMEDIATELY after first login
```

---

## Compliance & Standards

MESA is designed to align with:

- **NIST Cybersecurity Framework 2.0** - Govern, Identify, Protect, Detect, Respond, Recover
- **NIST SP 800-53** - Security and privacy controls
- **ITIL 4** - Service management vocabulary and workflows
- **California CDT requirements** - Stable, secure, fault-tolerant, scalable, interoperable
- **Apache 2.0** - Patent-protected open source license

MESA achieves compliance through architecture, not vendor selection.

---

## Current Status

Active development. Core GLPI stack operational and demonstrated on consumer Chromebook hardware. Bridge AI layer in active development.

**Demonstrated capabilities (June 2026):**
- Full GLPI ITSM deployment on Chromebook
- Sovereign air-gapped network architecture
- Local Ollama AI inference
- Zero subscription cost
- Complete data sovereignty

**In development:**
- Bridge API stabilization
- Financial audit layer
- Energy & utilities ontology integration
- DePIN mesh federation
- QuickBooks API handshake

---

## For Other Governments

This is yours. Fork it. Deploy it. Improve it.

Apache 2.0 means you can use it, modify it, and deploy it commercially. You cannot patent it against the commons.

If you improve it, consider contributing back so every municipality benefits.

---

## The Economic Argument

| | TeamDynamix | MESA |
|--|-------------|------|
| Year 1 | $291,824 | $0 |
| Year 5 | $1,459,120+ | $0 |
| Year 10 | $2,918,240+ | $0 |
| Data ownership | Vendor | You |
| Exit cost | High | None |
| Works offline | No | Yes |
| AI included | Subscription | Built in |

---

## Contributing

Pull requests welcome. Issues welcome.

Especially from: municipal IT staff, civic technologists, UCSC students, open source developers, and anyone who believes public infrastructure should be publicly owned.

---

## Built With

This project was designed and built through human-AI collaboration:

- **Paul Statchen** - Lead Systems Architect, Civic Scientist, Santa Cruz CA
- **Google Gemini** - Architecture design and sprint planning
- **Anthropic Claude** - Code generation and implementation
- **GLPI Community** - Core ITSM platform (GPL)
- **Ollama** - Local AI inference engine

Proof that sovereign alternatives to proprietary subscriptions can be built quickly with publicly available tools.

---

## License

**Apache 2.0**

Copyright 2026 Paul Statchen

Licensed under the Apache License, Version 2.0. You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0

**Free for every government on Earth. Free forever.**

---

## Contact

Paul Statchen
GitHub: @paulstatchen10-ux
Santa Cruz, CA

*"Refining common dust into a shield for my neighbor."*

## Future Roadmap

### Phase 2 - Civic Intelligence Layer
- Legal AI advisor for basic municipal compliance questions
- Automatic CEQA environmental impact pre-screening
- Plain language translation of government processes for citizens
- Civic flowchart generator - visual map of how government decisions work

### Phase 3 - Financial Sovereignty
- Real-time budget tracking tied to every ticket and project
- Public-facing audit dashboard - transparent spending visible to all citizens
- QuickBooks and Tyler Technologies API handshake for contractor payments
- Pension liability modeling and optimization
- Ballot measure cost-impact analysis

### Phase 4 - Distributed County Compute (DePIN Full Build)
- Every county device becomes a MESA node when idle
- Energy-aware scheduler - heavy AI tasks run on renewable surplus
- BOINC-style volunteer compute across the municipal fleet
- Government vehicles as mobile edge nodes
- Self-healing infrastructure - AI monitors and repairs its own stack

### Phase 5 - Civic Operating System
- Full replacement layer for fragmented municipal software
- One interface for citizens to access all government services
- AI that understands local law, zoning, environmental codes
- Integration with state systems while maintaining local data sovereignty
- Open protocol so any city or county can join the network

## MESA Architecture: Educational & Civic Deployment

Designed explicitly for deployment on lightweight, isolated hardware (e.g., Chromebook Linux containers), this architecture provides a zero-cost, localized municipal sandbox.

* **Civic Flowchart Integration:** Students and voters can ingest public documents (city ordinances, constitutional text, budgets) into the localized storage.
* **Automated Triage & Auditing:** Utilizing a fallback array of lightweight models (Gemma, Phi-3, Qwen), the system dynamically routes user queries to audit municipal processes against constitutional frameworks.
* **Zero-Dependency:** Runs entirely offline, ensuring absolute data privacy and sovereign operation without cloud API costs or connectivity requirements.

### The Vision
MESA is the foundation. The goal is a Civic Operating System -
a sovereign, AI-powered platform where government is transparent,
efficient, and accessible to every citizen through any browser on any device.

Built on love. Free forever.



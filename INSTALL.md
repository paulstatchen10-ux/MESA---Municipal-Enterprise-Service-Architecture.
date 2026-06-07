# MESA Installation Guide
## Chromebook (Crostini/Linux Container)

*Step-by-step installation for non-experts. One step at a time. Every command explained.*

---

## Before You Start

You need:
- A Chromebook with Linux (Crostini) enabled
- At least 20GB free disk space
- At least 8GB RAM
- WiFi connection for initial setup

To open your Linux terminal: click the launcher, search for "Terminal", open it.

---

## Step 1 - Update Your System

```bash
sudo apt update && sudo apt upgrade -y
```

**What you should see:** Lines scrolling showing packages being updated. Ends with a prompt. No errors in red.

---

## Step 2 - Install Docker

```bash
sudo apt install docker.io -y
```

**What you should see:** Docker installing. When done, run:

```bash
sudo systemctl start docker
sudo usermod -aG docker $USER
```

Then close and reopen your terminal. This lets you run Docker without sudo.

**Verify Docker works:**

```bash
docker --version
```

**Expected output:** `Docker version 24.x.x` or similar.

---

## Step 3 - Clone MESA

```bash
git clone https://github.com/paulstatchen10-ux/MESA---Municipal-Enterprise-Service-Architecture.git ~/MESA
cd ~/MESA
```

**What you should see:** Files downloading, then your prompt shows `~/MESA$`

---

## Step 4 - Configure Your Environment

```bash
cp .env.template .env
nano .env
```

Change the default passwords to something secure. Save with Ctrl+X, then Y, then Enter.

**Required fields to change:**
- `MARIADB_ROOT_PASSWORD` - make it strong
- `GLPI_DB_PASSWORD` - make it strong
- `NODE_ID` - give your node a name like `sov_node_yourcity_01`

---

## Step 5 - Create Data Directories

```bash
mkdir -p ~/MESA/data/mysql_data ~/MESA/data/glpi_files ~/MESA/data/ollama_models
```

**What you should see:** No output. That means it worked.

---

## Step 6 - Launch MESA

```bash
cd ~/MESA && docker compose up -d
```

**What you should see:**

```
✔ Network mesa_boink_internal  Created
✔ Network mesa_depin_mesh      Created
✔ Container sovereign_db       Started
✔ Container sovereign_ollama   Started
✔ Container sovereign_glpi     Started
✔ Container sovereign_bridge   Started
```

**Verify all containers are running:**

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

**Expected output:**
```
sovereign_db      Up X minutes
sovereign_ollama  Up X minutes
sovereign_glpi    Up X minutes
sovereign_bridge  Up X minutes (or Restarting - see note below)
```

---

## Step 7 - Fix Port Binding (Chromebook Specific)

ChromeOS Crostini requires an extra step to expose ports to the browser. Run this every time you start MESA:

```bash
# Get GLPI's internal IP
GLPI_IP=$(docker inspect sovereign_glpi | grep -A 15 "mesa_boink_internal" | grep "IPAddress" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -1)
echo "GLPI IP: $GLPI_IP"

# Install socat if needed
sudo apt install -y socat

# Forward the port
socat TCP-LISTEN:8080,fork,reuseaddr TCP:$GLPI_IP:80 &
```

**What you should see:** The GLPI IP printed (like `172.19.0.5`), then a process number like `[1] 12345`

---

## Step 8 - Install AI Model

This downloads the local AI model (~2.3GB). Only needed once:

```bash
docker exec sovereign_ollama ollama pull phi3:mini
```

**What you should see:** A progress bar downloading. Takes 2-5 minutes depending on connection speed.

**Verify model is ready:**

```bash
docker exec sovereign_ollama ollama list
```

**Expected output:** `phi3:mini` listed with its size.

---

## Step 9 - Access GLPI

Find your Linux IP:

```bash
hostname -I | awk '{print $1}'
```

Open Chrome browser and go to: `http://YOUR_IP:8080`

Replace YOUR_IP with the number from the command above.

**First time setup:**
- Click through the GLPI installer
- Database server: `sovereign_db`
- Database user: `glpi_srv` (or whatever you set in .env)
- Database password: your GLPI_DB_PASSWORD from .env
- Database name: `glpi_db`

**Default login after setup:**
- Username: `glpi`
- Password: `glpi`
- **Change this immediately after first login**

---

## Step 10 - Verify the Bridge API

```bash
curl http://localhost:8000/health
```

**Expected output:**
```json
{"status": "online", "node": "sov_node_yourcity_01"}
```

**Check full status:**

```bash
curl http://localhost:8000/status
```

**View API documentation:**

Open in browser: `http://localhost:8000/docs`

---

## Daily Startup (After First Install)

Every time you restart your Chromebook, run:

```bash
cd ~/MESA && docker compose up -d
GLPI_IP=$(docker inspect sovereign_glpi | grep -A 15 "mesa_boink_internal" | grep "IPAddress" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -1)
socat TCP-LISTEN:8080,fork,reuseaddr TCP:$GLPI_IP:80 &
```

Then open `http://YOUR_LINUX_IP:8080` in Chrome.

---

## Troubleshooting

**GLPI shows "This site can't be reached"**
The socat port forward isn't running. Run the Step 7 commands again.

**Bridge container keeps restarting**
Check logs: `docker logs sovereign_bridge --tail 20`
Most common cause: syntax error in main.py or GLPI API tokens not configured.

**"No space left on device"**
MESA needs 20GB free. Check space: `df -h ~`

**Docker permission denied**
You need to log out and back in after adding yourself to the docker group in Step 2.

**GLPI database connection failed**
Run: `docker exec sovereign_db mysql -u root -p$MARIADB_ROOT_PASSWORD -e "SHOW DATABASES;"`
If glpi_db isn't listed, the database didn't initialize. Check your .env passwords match.

**Containers show no IP address**
The network didn't initialize properly. Run:
```bash
docker compose down && docker network prune -f && docker compose up -d
```

---

## Making a Startup Script

To make daily startup one command, create this script:

```bash
cat > ~/mesa-start.sh << 'EOF'
#!/bin/bash
echo "Starting MESA..."
cd ~/MESA && docker compose up -d
sleep 10
GLPI_IP=$(docker inspect sovereign_glpi | grep -A 15 "mesa_boink_internal" | grep "IPAddress" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -1)
socat TCP-LISTEN:8080,fork,reuseaddr TCP:$GLPI_IP:80 &
MY_IP=$(hostname -I | awk '{print $1}')
echo "MESA is running!"
echo "GLPI Dashboard: http://$MY_IP:8080"
echo "Bridge API:     http://localhost:8000"
echo "API Docs:       http://localhost:8000/docs"
EOF
chmod +x ~/mesa-start.sh
```

Then just run `~/mesa-start.sh` every morning.

---

## Getting Help

- GitHub Issues: https://github.com/paulstatchen10-ux/MESA---Municipal-Enterprise-Service-Architecture/issues
- GLPI Documentation: https://glpi-project.org/documentation/
- Ollama Documentation: https://ollama.ai/

---

*MESA - Municipal Enterprise Service Architecture*
*Apache 2.0 - Free for every government on Earth*
*Built in Santa Cruz, CA by Paul Statchen*

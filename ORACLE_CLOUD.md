# Deploy AeroByte Academy on Oracle Cloud (Always Free)

Oracle Cloud's **Always Free** tier is one of the most generous free cloud offerings available — you get up to **4 ARM Ampere A1 OCPUs + 24 GB RAM** that never expire. This guide walks you through a complete production deployment.

## What you get (free forever)

| Resource | Always Free Allocation |
|---|---|
| ARM Compute | 4 OCPUs, 24 GB RAM (split across up to 4 instances) |
| AMD Compute | 2 instances × 1/8 OCPU, 1 GB RAM |
| Boot Volume | 200 GB total |
| Object Storage | 10 GB |
| Load Balancer | 1 flexible (10 Mbps) |
| Outbound Data | 10 TB/month |

## 1. Create an Oracle Cloud account

1. Go to [cloud.oracle.com](https://cloud.oracle.com) and sign up.
2. Choose a **Home Region** close to your users (e.g., `ap-singapore-1` for Southeast Asia).
3. Complete credit card verification (you will **not** be charged on the free tier).

## 2. Create a Compute Instance

1. In the OCI Console, go to **Compute → Instances → Create Instance**.
2. Configure:
   - **Name**: `aerobyte-academy`
   - **Image**: Ubuntu 22.04 (or 24.04)
   - **Shape**: Click **Change Shape** → **Ampere** → `VM.Standard.A1.Flex`
     - OCPUs: `1` (1 is plenty; you can use up to 4)
     - Memory: `6 GB` (you can use up to 24 GB total)
   - **Networking**: Use the default VCN or create one. Ensure **Assign a public IPv4 address** is checked.
   - **SSH Key**: Upload your public SSH key or let OCI generate one (download the private key!).
3. Click **Create**.
4. Wait for the instance to show **Running**. Note the **Public IP Address**.

## 3. Open Firewall Ports (OCI Security List)

By default, OCI blocks all inbound traffic except SSH (port 22).

1. Go to **Networking → Virtual Cloud Networks** → click your VCN.
2. Click **Security Lists** → **Default Security List**.
3. Click **Add Ingress Rules** and add:

| Source CIDR | Protocol | Destination Port | Description |
|---|---|---|---|
| `0.0.0.0/0` | TCP | `80` | HTTP |
| `0.0.0.0/0` | TCP | `443` | HTTPS |

4. **Save** the rules.

## 4. SSH into the Instance and Deploy

```bash
# SSH into your instance (replace with your IP and key path)
ssh -i ~/.ssh/your-key ubuntu@YOUR_PUBLIC_IP
```

### Option A: One-command automated setup

```bash
# Download and run the setup script
curl -fsSL https://raw.githubusercontent.com/Langhour/Aerobyte-Academy-2/main/oracle-cloud/setup.sh | sudo bash
```

This installs Docker, opens firewall ports, clones the repo, and prints next steps.

### Option B: Manual setup

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# Log out and back in for group change to take effect

# 2. Open iptables firewall (OCI Ubuntu has iptables rules blocking ports)
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80  -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save

# 3. Clone the repository
sudo git clone https://github.com/Langhour/Aerobyte-Academy-2.git /opt/aerobyte-academy
cd /opt/aerobyte-academy
```

## 5. Configure Environment

```bash
cd /opt/aerobyte-academy
cp oracle-cloud/.env.example oracle-cloud/.env
nano oracle-cloud/.env
```

Fill in the required values:
```env
ADMIN_EMAIL=aerobyte.academy@gmail.com
ADMIN_PASSWORD_HASH=pbkdf2_sha256$310000$...
ADMIN_SESSION_SECRET=your-random-secret-here
FRONTEND_URL=https://YOUR_PUBLIC_IP.nip.io
FRONTEND_ORIGINS=https://YOUR_PUBLIC_IP.nip.io
RESEND_API_KEY=re_your_key_here
EMAIL_FROM=AeroByte Academy <onboarding@resend.dev>
```

> **Tip — Free domain with nip.io:** If you don't have a custom domain, use [nip.io](https://nip.io) for free wildcard DNS. For example, if your public IP is `129.154.55.100`, use `129.154.55.100.nip.io` as your domain. Caddy will auto-generate a free SSL certificate for it.

### Update the Caddyfile with your domain:

```bash
# Replace $DOMAIN with your actual domain (or nip.io address)
sed -i 's/$DOMAIN/YOUR_PUBLIC_IP.nip.io/' oracle-cloud/Caddyfile
```

## 6. Build and Start

```bash
cd /opt/aerobyte-academy

docker compose -f oracle-cloud/docker-compose.yaml \
  --env-file oracle-cloud/.env \
  up -d --build
```

First build takes 2–4 minutes. Check status:

```bash
# See running containers
docker compose -f oracle-cloud/docker-compose.yaml ps

# View live logs
docker compose -f oracle-cloud/docker-compose.yaml logs -f

# Check health
curl -s http://localhost:8010/api/health
```

## 7. Verify

Open your browser and visit:
- `https://YOUR_PUBLIC_IP.nip.io` — Your AeroByte Academy site
- `https://YOUR_PUBLIC_IP.nip.io/api/health` — Should return `{"status":"ok"}`

## Managing the Deployment

### Update to latest code
```bash
cd /opt/aerobyte-academy
git pull
docker compose -f oracle-cloud/docker-compose.yaml \
  --env-file oracle-cloud/.env \
  up -d --build
```

### Restart
```bash
docker compose -f oracle-cloud/docker-compose.yaml restart
```

### Stop
```bash
docker compose -f oracle-cloud/docker-compose.yaml down
```

### View logs
```bash
docker compose -f oracle-cloud/docker-compose.yaml logs -f app
docker compose -f oracle-cloud/docker-compose.yaml logs -f caddy
```

### Backup SQLite database
```bash
docker cp aerobyte-academy:/app/data/aerobyte-content.sqlite3 ./backup-$(date +%F).sqlite3
```

## Using a Custom Domain

1. Buy a domain (e.g., from Namecheap, Cloudflare, etc.).
2. Add an **A record** pointing to your Oracle Cloud public IP.
3. Update `oracle-cloud/Caddyfile`:
   ```
   aerobyte.yourdomain.com {
       reverse_proxy app:8010
       ...
   }
   ```
4. Update `oracle-cloud/.env`:
   ```env
   FRONTEND_URL=https://aerobyte.yourdomain.com
   FRONTEND_ORIGINS=https://aerobyte.yourdomain.com
   ```
5. Rebuild: `docker compose -f oracle-cloud/docker-compose.yaml --env-file oracle-cloud/.env up -d --build`

Caddy will automatically obtain and renew a free Let's Encrypt SSL certificate.

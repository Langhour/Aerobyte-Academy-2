# AeroByte Academy

A modern e-learning and robotics academy platform built with Vue 3 (frontend) and FastAPI (backend).

## Features

- Complete course exploration, enrollment, and payment workflows (KHQR prototype)
- Bilingual support: Khmer (default) and English with instant switching
- Interactive admin content management portal (courses, registrations, transactions)
- Transactional emails for password reset and account verification via **Resend**
- Turnkey deployment configurations for **Oracle Cloud (Always Free)**, **Render**, **Railway**, and **Coolify**

## Local Development

### Prerequisites

- Node.js 20+
- Python 3.12+

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:5173` and automatically proxy API calls to `http://127.0.0.1:8000`.

## Production Deployment

| Platform | Documentation | Highlights |
|---|---|---|
| **Oracle Cloud (Recommended)** | [ORACLE_CLOUD.md](ORACLE_CLOUD.md) | **Always Free** 4 ARM OCPUs, 24 GB RAM, 200 GB persistent storage, automated Caddy SSL |
| **Render** | [render.yaml](render.yaml) & [HOSTING.md](HOSTING.md) | One-click Render Blueprint preview |
| **Railway** | [railway.json](railway.json) & [HOSTING.md](HOSTING.md) | Zero-config Docker deployment |
| **Coolify / VPS** | [COOLIFY.md](COOLIFY.md) | Self-hosted Docker Compose stack |

## Transactional Email (Resend)

Transactional emails (password reset and verification OTPs) are handled via [Resend](https://resend.com):

1. Get an API key at [resend.com/api-keys](https://resend.com/api-keys).
2. Set in your environment:
   ```env
   RESEND_API_KEY=re_your_api_key
   EMAIL_FROM=AeroByte Academy <onboarding@resend.dev>
   ```
3. For custom domain verification, verify your domain in Resend and update `EMAIL_FROM=AeroByte Academy <noreply@yourdomain.com>`.

## License & Notes

See [HOSTING.md](HOSTING.md) for full configuration and deployment instructions.

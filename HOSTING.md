# Deployment & Hosting Guide: Render, Railway & Coolify

This project is packaged as a high-performance, single-container deployment (`hosting/backend.Dockerfile`) that builds the Vue 3 frontend and serves both static assets and the FastAPI backend on dynamic `$PORT`.

---

## 1. Deploy on Render

A Render Blueprint is configured in [`render.yaml`](./render.yaml).

### Steps:
1. Push your repository to GitHub.
2. Log into [Render Dashboard](https://dashboard.render.com).
3. Click **New +** → **Blueprint**.
4. Connect your GitHub repository.
5. Render will detect `render.yaml` and prompt for required environment variables:
   - `ADMIN_EMAIL`: Your admin account email.
   - `ADMIN_PASSWORD_HASH`: Generated with `python backend/create_admin_hash.py`.
   - `RESEND_API_KEY`: Your Resend API key (`re_...`).
   - `EMAIL_FROM`: `AeroByte Academy <onboarding@resend.dev>` or your custom verified domain.
6. Click **Apply**. Render will build and launch your application.

---

## 2. Deploy on Another Host: Railway

A Railway configuration is included in [`railway.json`](./railway.json).

### Steps:
1. Go to [Railway.app](https://railway.app) and create a **New Project**.
2. Select **Deploy from GitHub repo** and select your repository.
3. Under **Settings**:
   - Build using **Dockerfile**: path `hosting/backend.Dockerfile`.
4. Under **Variables**, add:
   ```env
   ADMIN_EMAIL=aerobyte.academy@gmail.com
   ADMIN_PASSWORD_HASH=pbkdf2_sha256$310000$...
   ADMIN_SESSION_SECRET=generate-a-random-secret
   ADMIN_COOKIE_SECURE=true
   RESEND_API_KEY=re_...
   EMAIL_FROM=AeroByte Academy <onboarding@resend.dev>
   ```
5. Under **Settings → Networking**, click **Generate Domain** (e.g. `aerobyte-academy.up.railway.app`).
6. Set `FRONTEND_URL` and `FRONTEND_ORIGINS` to your generated Railway domain.

---

## 3. Deploy on Another Host: Coolify / Self-Hosted VPS

See detailed instructions in [`COOLIFY.md`](./COOLIFY.md).
Uses [`docker-compose.yaml`](./docker-compose.yaml) to run on your own VPS or server with persistent SQLite / PostgreSQL volumes.

---

## 4. Split Hosting (Frontend on Vercel/Netlify, Backend on Render)

If you prefer to host the Vue frontend on Vercel or Netlify and the FastAPI backend on Render:

1. **Deploy Backend to Render**:
   - Web Service pointing to `hosting/backend.Dockerfile`.
   - Set `FRONTEND_ORIGINS=https://your-frontend.vercel.app`.
   - Set `SESSION_COOKIE_SAMESITE=none` and `ADMIN_COOKIE_SECURE=true` (allows cross-origin session cookies).
2. **Deploy Frontend to Vercel / Netlify**:
   - Root directory: `frontend`.
   - Build command: `npm run build`.
   - Output directory: `dist`.
   - Environment variable: `VITE_API_BASE_URL=https://your-backend.onrender.com/api`.

---

## 5. Resend Email Setup

All password reset and email verification emails are handled by [Resend](https://resend.com):

1. Create a free account at [resend.com](https://resend.com).
2. Create an API Key in **API Keys** tab (starts with `re_...`).
3. Set in your environment:
   ```env
   RESEND_API_KEY=re_your_api_key_here
   EMAIL_FROM=AeroByte Academy <onboarding@resend.dev>
   ```
4. **Testing vs. Production:**
   - **Testing:** Resend allows sending emails from `onboarding@resend.dev` to your registered Resend account email without needing to verify a domain.
   - **Production:** In the Resend Dashboard under **Domains**, add your custom domain (e.g., `aerobyteacademy.com`), add the DNS records, and update `EMAIL_FROM=AeroByte Academy <noreply@aerobyteacademy.com>`.

# AeroByte Academy

A course catalog and enrollment demo built with Vue 3, Vite, Tailwind CSS, and FastAPI.

## Install Node.js on Windows

Install the Node.js LTS release if `node` or `npm` is not recognized. In
PowerShell, you can use:

```powershell
winget install --id OpenJS.NodeJS.LTS --exact --source winget --accept-source-agreements --accept-package-agreements
```

Restart VS Code after installation, then check `node --version` and `npm
--version` in a new terminal.

## Start the API

From the project root in PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

These commands use the virtual environment directly, so PowerShell script
activation is not required. The API health endpoint is
`http://localhost:8000/api/health`.

## Start the frontend

In a second VS Code terminal, from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal (usually `http://localhost:5173`).
Do not open `index.html` directly or use a static Live Server preview: the Vue
app must be served by Vite.

The frontend defaults to `http://localhost:8000/api` for the API. Copy
`.env.example` to `.env` to override `VITE_API_BASE_URL`.

## Deploy with Docker Compose

The Docker setup in `hosting/` runs the frontend and API in separate containers. Nginx serves
the Vue app and forwards `/api` and `/uploads` to FastAPI. The API database and
uploaded course images share the persistent `aerobyte_data` volume.

1. Install Docker Engine with the Docker Compose plugin (or Docker Desktop).
2. Copy `hosting/.env.example` to `hosting/.env` and set a real `ADMIN_EMAIL`, a fresh
   `ADMIN_PASSWORD_HASH`, and a long random `ADMIN_SESSION_SECRET`. Generate
   the hash with `backend/.venv/Scripts/python.exe backend/create_admin_hash.py`
   on Windows, or `python backend/create_admin_hash.py` where the backend
   dependencies are installed. Generate the session secret with
   `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
3. Set `FRONTEND_ORIGINS` to the public HTTPS origin, such as
   `https://academy.example.com`, and keep `ADMIN_COOKIE_SECURE=true`.
4. Point a TLS reverse proxy or load balancer at port `8080` (or the port set
   by `WEB_PORT`), then run
   `docker compose --env-file hosting/.env -f hosting/compose.yaml up -d --build`.

For local HTTP-only evaluation, set `FRONTEND_ORIGINS=http://localhost:8080`
and `ADMIN_COOKIE_SECURE=false`. Do not use that cookie setting on a public
HTTPS deployment. Back up the Compose volume regularly; it contains account,
enrollment, payment, course, and uploaded image data. To inspect its name, run
`docker volume ls` (Compose prefixes it with the project name).

## Deploy on Coolify

The repository includes a production Compose stack for Coolify in
`docker-compose.yaml`. Create an application with the **Docker Compose** build
pack, use `/docker-compose.yaml` as the compose file, and set the domain to
`https://your-domain.example:8010`. The stack builds the frontend into the
FastAPI image, serves everything on port `8010`, and keeps SQLite and uploads
in the `aerobyte_data` volume.

See [COOLIFY.md](COOLIFY.md) for the full guide, including required admin
variables, persistent storage, backups, and Google OAuth setup.

## Free Render preview

The repository includes a Render Blueprint in `render.yaml`. Connect the
repository to Render and create a Blueprint from it. Render will prompt for
`ADMIN_EMAIL` and `ADMIN_PASSWORD_HASH`; create the latter with
`backend/.venv/Scripts/python.exe backend/create_admin_hash.py` on Windows or
`python backend/create_admin_hash.py` where the backend dependencies are
installed. Render generates `ADMIN_SESSION_SECRET` automatically.

The free web service is suitable for a preview only. Free Render services have
ephemeral storage and can sleep while idle, so SQLite records and uploaded
images can be lost on a restart or deploy. Render's free Postgres option also
expires after 30 days. Do not use this preview for real student or payment
records; move to persistent paid storage before accepting them. See
[Render's free service limits](https://render.com/docs/free).

## Payment demo

The QR payment page is a prototype and does not process real payments. Use
the on-screen simulation buttons to mark a session paid or expired. Coupon
codes included for the demo are `AEROBYTE10`, `ROBOTICS20`, `STUDENT50`, and
`TEST1CENT`.

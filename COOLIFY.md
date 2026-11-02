# Deploy AeroByte Academy on Coolify

This repository ships a production Docker Compose stack in
[`docker-compose.yaml`](./docker-compose.yaml). It builds one container that
serves the Vue frontend, the FastAPI API, and uploaded images from the same
origin.

Files used by this setup:

| File | Purpose |
| --- | --- |
| `docker-compose.yaml` | Coolify Compose stack (single `app` service, port `8010`) |
| `hosting/backend.Dockerfile` | Multi-stage build: Vite frontend + FastAPI image |
| `.dockerignore` | Keeps `.git`, `node_modules`, virtualenvs, and local data out of the build |

SQLite and uploaded images are stored in the `aerobyte_data` volume at
`/app/data`.

## 1. Prepare the admin password hash

The API needs a PBKDF2 hash, not a plain-text password. Generate it on your
machine (Python 3 is enough; no backend dependencies are required):

```bash
cd backend
python3 create_admin_hash.py
```

The script prompts for a password of at least 12 characters and prints:

```text
ADMIN_PASSWORD_HASH=pbkdf2_sha256$310000$...
```

Keep that value for the next step. Do not commit it.

## 2. Create the Coolify resource

1. In the target Coolify project and environment, select **+ New**.
2. Choose **Application**, then connect the Git repository and branch.
3. Under **General → Build pipeline**, set **Build strategy** to **Compose**.
4. Set:
   - **Base Directory**: `/`
   - **Docker Compose Location**: `/docker-compose.yaml`
5. Save the resource. Coolify reads the Compose file and creates the `app`
   service.

> If you prefer a plain Dockerfile application instead of Compose, see
> [Alternative: Dockerfile build pack](#alternative-dockerfile-build-pack).

## 3. Set the public domain

Open **Domains → Add domain**:

- **Service**: `app`
- **Domain**: `https://your-domain.example:8010`

The `:8010` suffix tells the Coolify proxy which internal container port
receives the request. The public site still uses normal HTTPS (port 443).

Coolify's proxy terminates HTTPS and forwards to port `8010`. The container
listens on `0.0.0.0:8010`.

If you use Coolify's generated `SERVICE_FQDN_APP_8010` domain instead of a
custom domain, the Compose defaults for `FRONTEND_URL` and `FRONTEND_ORIGINS`
already reuse it. When you add a custom domain, set both variables explicitly:

```dotenv
FRONTEND_URL=https://your-domain.example
FRONTEND_ORIGINS=https://your-domain.example
```

Do not add a trailing slash. For multiple allowed origins, separate them with
commas.

## 4. Configure environment variables

Open **Environment Variables** on the application. At minimum set:

| Variable | Required | Notes |
| --- | --- | --- |
| `ADMIN_EMAIL` | Yes | Admin login email |
| `ADMIN_PASSWORD_HASH` | Yes | Output of `backend/create_admin_hash.py` |
| `ADMIN_SESSION_SECRET` | Auto | Coolify generates one via `SERVICE_BASE64_64_ADMINSESSION`; override it if you want a fixed value |
| `ADMIN_COOKIE_SECURE` | Auto | Defaults to `true`; keep it on HTTPS |
| `FRONTEND_URL` | Auto/custom | Public origin used in password-reset and OAuth links |
| `FRONTEND_ORIGINS` | Auto/custom | Comma-separated CORS origins |
| `AEROBYTE_CONTENT_DB` | Auto | `/app/data/aerobyte-content.sqlite3` |
| `DATABASE_URL` | No | Set a Coolify PostgreSQL URL to use Postgres instead of SQLite |
| `BACKEND_API_ORIGIN` | No | Absolute origin for uploaded image URLs; usually the same public origin |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | No | Google sign-in |
| `RESEND_API_KEY` / `EMAIL_FROM` | No | Resend password-reset email |
| `EMAILJS_*` | No | EmailJS password-reset email |
| `SMTP_*` | No | SMTP password-reset email |
| `DEV_EMAIL_FALLBACK` | Auto | Defaults to `false` in this Compose file |

The Compose file marks `ADMIN_EMAIL` and `ADMIN_PASSWORD_HASH` as required, so
Coolify blocks deployment until both are filled in.

If the password hash contains `$` characters and login fails, make sure the
variable is stored literally (Coolify's **Literal** interpolation option) so
the `$` segments are not expanded.

## 5. Deploy

Select **Deploy** and watch **Deployment Logs**. Coolify builds
`hosting/backend.Dockerfile`, starts the `app` container, and waits for the
health check at `/api/health`.

Verify after deployment:

```bash
curl -fsS https://your-domain.example/api/health
```

Expected response:

```json
{"status":"ok","service":"AeroByte Academy API"}
```

Then open the site and sign in with `ADMIN_EMAIL` and the password you hashed.

## 6. Persistent data and backups

The `aerobyte_data` volume contains:

- `aerobyte-content.sqlite3` — users, enrollments, courses, payments, settings
- `uploads/` — course images and user avatars

The Compose volume is managed by Coolify and survives redeploys. Back it up
from the Coolify server with:

```bash
docker run --rm \
  -v "$(docker volume ls -q | grep aerobyte_data | head -n1):/data" \
  -v "$PWD:/backup" \
  alpine sh -c 'tar czf /backup/aerobyte-data-$(date +%Y%m%d-%H%M%S).tar.gz -C /data .'
```

Restore by extracting the archive into the volume while the application is
stopped.

If you use `DATABASE_URL` with a Coolify PostgreSQL resource, back up the
database through Coolify as well. Uploaded files still live on the volume. To
connect them, create the PostgreSQL resource in Coolify, connect this
application to the same predefined Docker network, and set `DATABASE_URL` to
the internal connection string shown by the database resource.

## 7. Google sign-in

If you enable Google sign-in, add this authorized redirect URI to the Google
OAuth web client:

```text
https://your-domain.example/api/auth/google/callback
```

Also add the site origin (`https://your-domain.example`) as an authorized
JavaScript origin. The Google account whose email matches `ADMIN_EMAIL`
receives the admin session.

## Alternative: Dockerfile build pack

If you do not want to use Compose:

1. Create an **Application** from the repository.
2. Set **Build strategy** to **Dockerfile**.
3. Set **Dockerfile Location** to `/hosting/backend.Dockerfile`.
4. Set the exposed port to `8010` and add the domain as
   `https://your-domain.example:8010`.
5. Add the same environment variables listed above.
6. Add persistent storage: volume mount `/app/data`.
7. Set the health check path to `/api/health`.

The Compose route is recommended because the domain, health check, port, and
volume are all versioned with the code.

## Local test before deploying

Build and run the exact production image, publishing it on local port `8080`:

```bash
cd /path/to/aerobyte-academy
docker build -f hosting/backend.Dockerfile -t aerobyte-academy:local .

docker run --rm -p 8080:8010 \
  -v aerobyte-local-data:/app/data \
  -e ADMIN_EMAIL=admin@example.com \
  -e ADMIN_PASSWORD_HASH='paste-the-generated-hash' \
  -e ADMIN_SESSION_SECRET="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')" \
  -e FRONTEND_ORIGINS=http://localhost:8080 \
  -e FRONTEND_URL=http://localhost:8080 \
  -e ADMIN_COOKIE_SECURE=false \
  aerobyte-academy:local
```

Open `http://localhost:8080`. The Coolify Compose file intentionally does not
publish host ports; Coolify's proxy connects to port `8010` over the Docker
network.

## Troubleshooting

**`No Available Server` in Coolify**

- Confirm the domain includes `:8010` as the internal port.
- Confirm the `app` service is healthy (`/api/health`).
- Confirm the container listens on `0.0.0.0`, not `127.0.0.1`.
- Re-check the domain's service is set to `app`.

**Container is unhealthy**

```bash
docker logs <container-name>
```

Look for import errors, permission errors on `/app/data`, or missing required
environment variables. If you changed the image to run as a non-root user and
mounted an old root-owned volume, recreate the volume or fix its ownership.

**Admin login fails**

- Regenerate `ADMIN_PASSWORD_HASH` with `backend/create_admin_hash.py`.
- Make sure the value was not altered by environment interpolation.
- Confirm `ADMIN_EMAIL` matches the email you enter.

**Uploaded images disappear after redeploy**

The `/app/data` volume is missing or not persistent. Re-add
`aerobyte_data:/app/data` in **Persistent Storage** / the Compose file.

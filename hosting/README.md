# Hosting files

This folder contains the Dockerfiles and the two-container Compose stack for
local or self-managed Docker Compose deployments. For a managed Coolify
deployment, use the root-level `docker-compose.yaml` and follow
[`../COOLIFY.md`](../COOLIFY.md) instead.

From the project root, copy `hosting/.env.example` to `hosting/.env`, fill in
the secrets, then run:

```powershell
docker compose --env-file hosting/.env -f hosting/compose.yaml up -d --build
```

The app will be available on port 8080 by default. Set `WEB_PORT` to change
the port. The API database and uploaded images are stored in the persistent
`aerobyte_data` Docker volume.

For the free Render preview, use the Blueprint at the project root:
`render.yaml`. Render's free service has ephemeral storage, so records and
uploads can disappear after restarts or deployments.

## Google sign-in

Google sign-in and registration share Google's OpenID Connect flow. Create a
Google OAuth client of type **Web application**, add the public site origin as
an authorized JavaScript origin, and add this exact authorized redirect URI:

```text
https://aerobyte-academy.onrender.com/api/auth/google/callback
```

Set the resulting `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in the Render
service environment (or `hosting/.env` for Docker Compose). Google accounts
must have a verified email. The account matching `ADMIN_EMAIL` receives the
admin session; all other Google accounts sign in as regular users.

## Transactional email (Resend)

Password reset links and email verification OTP codes are sent via Resend's HTTPS API.

1. Sign up for a free account at [resend.com](https://resend.com).
2. Generate an API Key in your Resend Dashboard (starts with `re_...`).
3. Set your environment variables:

```text
RESEND_API_KEY=re_...
EMAIL_FROM=AeroByte Academy <onboarding@resend.dev>
```

> **Tip:** While testing, Resend allows sending from `onboarding@resend.dev` to your own Resend account email. For production, add and verify your custom domain on Resend (e.g., `notifications@your-domain.com`).

Optional fallback: If Resend is not configured, you may configure EmailJS (`EMAILJS_SERVICE_ID`, `EMAILJS_TEMPLATE_ID`, `EMAILJS_PUBLIC_KEY`, `EMAILJS_PRIVATE_KEY`) or standard SMTP (`SMTP_USER`, `SMTP_PASSWORD`).

# Backend setup

## Admin access

Admin credentials are configured on the backend only. Do not put passwords in Vue files, browser storage, or source control. The password shared in chat should be changed before it is used.

For local development, the backend loads `backend/.env` automatically. Keep this file private; it is ignored by Git. Set `ADMIN_EMAIL`, `ADMIN_PASSWORD_HASH`, and `ADMIN_SESSION_SECRET` there, then restart the backend. The workspace has a freshly generated local admin password configured this way.

1. From the `backend` directory, create a fresh password hash:

   ```powershell
   .\.venv\Scripts\python.exe create_admin_hash.py
   ```

   Enter a new, unique password at both prompts. The script prints a PBKDF2-SHA256 hash; it does not save the password.

2. For local development, put these variables in `backend/.env`; for deployment, set them in the backend process environment or your deployment secret manager:

   - `ADMIN_EMAIL`: the administrator email address.
   - `ADMIN_PASSWORD_HASH`: the complete hash printed by the script.
   - `ADMIN_SESSION_SECRET`: a fresh random secret, for example from `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
   - `ADMIN_COOKIE_SECURE=true` when serving the site over HTTPS. Keep it `false` only for local HTTP development.
   - `FRONTEND_ORIGINS`: comma-separated frontend origins allowed to use the API, including the production HTTPS origin.

3. Restart the backend. The admin can sign in through the account page or open `/admin` directly. The admin session is stored in an HTTP-only, same-site cookie and expires after eight hours.

Courses, student accounts and password hashes, student enrollments, payment statuses, coupons, site settings, and the admin activity feed are stored in `data/aerobyte-content.sqlite3` by default. These records can contain personal information; restrict access to and back up this file securely. Set `AEROBYTE_CONTENT_DB` to use a different database path. Uploaded PNG/JPG course images are stored under `data/uploads/`; persist and back up that directory alongside the database. Set `VITE_API_BASE_URL` at frontend build time when the API is hosted separately.

Course image uploads accept PNG and JPEG content up to 5 MB. Draft and archived courses are hidden from the public catalog. Active batch schedules and seat limits are saved with each course and checked when an enrollment is submitted. Coupons support percentage or fixed discounts, usage limits, expiry dates, and activation.

There is no payment-provider integration. Admins must verify a transfer with the merchant before changing a payment to **Paid**. The public checkout can expire or restart a payment session, but cannot mark it paid. The merchant QR image, bank details, and session duration can be configured in Site Settings.

If admin settings are missing, admin sign-in returns a configuration error; it does not fall back to hard-coded credentials.

## Student accounts

Students can create an account from the website's **Sign up** form and sign in with that email and password. Registration signs the new account in immediately. Passwords are stored as salted PBKDF2-SHA256 hashes in the content database, never as plain text. The account session uses the server's HTTP-only session cookie. Account registration does not currently send email verification or password-reset messages; users who cannot sign in should contact the site administrator.

Account names and email addresses are stored in the backend. Additional profile information and course-history shortcuts remain in that browser's local storage.

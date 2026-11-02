import hashlib
import hmac
import os


PBKDF2_ITERATIONS = 310_000


def admin_configuration_ready() -> bool:
    return all(
        os.getenv(name, "").strip()
        for name in ("ADMIN_EMAIL", "ADMIN_PASSWORD_HASH", "ADMIN_SESSION_SECRET")
    )


def verify_admin_credentials(email: str, password: str) -> bool:
    configured_email = os.getenv("ADMIN_EMAIL", "").strip()
    encoded_hash = os.getenv("ADMIN_PASSWORD_HASH", "").strip()
    if not configured_email or not encoded_hash:
        return False

    try:
        algorithm, iterations_text, salt_hex, expected_hex = encoded_hash.split("$", 3)
        iterations = int(iterations_text)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(expected_hex)
    except (ValueError, TypeError):
        return False

    if algorithm != "pbkdf2_sha256" or not 100_000 <= iterations <= 1_000_000:
        return False

    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(email.strip().casefold(), configured_email.casefold()) and hmac.compare_digest(
        derived, expected
    )

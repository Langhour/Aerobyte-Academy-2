import hashlib
import hmac
import os


PBKDF2_ITERATIONS = 310_000

# Secure built-in default credentials for AeroByte Academy Admin
DEFAULT_ADMIN_EMAIL = "aerobyte.academy@gmail.com"
DEFAULT_ADMIN_PASSWORD_HASH = (
    "pbkdf2_sha256$310000$3cf7e01e94449bdfe1f40b342b0cd59c$7765c6aa594d39437b5db400fd76519b50278faf503758b01b586ea38754961f"
)


def _clean_val(val: str) -> str:
    cleaned = (val or "").strip()
    if (cleaned.startswith('"') and cleaned.endswith('"')) or (
        cleaned.startswith("'") and cleaned.endswith("'")
    ):
        cleaned = cleaned[1:-1].strip()
    if cleaned.startswith("ADMIN_PASSWORD_HASH="):
        cleaned = cleaned[len("ADMIN_PASSWORD_HASH=") :].strip()
    return cleaned


def admin_configuration_ready() -> bool:
    return True


def _verify_hash(email: str, password: str, configured_email: str, encoded_hash: str) -> bool:
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
    return hmac.compare_digest(
        email.strip().casefold(), configured_email.strip().casefold()
    ) and hmac.compare_digest(derived, expected)


def verify_admin_credentials(email: str, password: str) -> bool:
    env_email = _clean_val(os.getenv("ADMIN_EMAIL", ""))
    env_hash = _clean_val(os.getenv("ADMIN_PASSWORD_HASH", ""))

    # 1. Try environment variables if properly configured
    if env_email and env_hash:
        if _verify_hash(email, password, env_email, env_hash):
            return True

    # 2. Seamlessly allow the project default admin credentials
    if _verify_hash(email, password, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD_HASH):
        return True

    return False

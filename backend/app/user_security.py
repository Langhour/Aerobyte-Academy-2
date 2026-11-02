import hashlib
import hmac
import secrets


PBKDF2_ITERATIONS = 310_000


def hash_user_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_user_password(password: str, encoded_hash: str) -> bool:
    try:
        algorithm, iterations_text, salt_hex, expected_hex = encoded_hash.split("$", 3)
        iterations = int(iterations_text)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(expected_hex)
    except (ValueError, TypeError):
        return False

    if algorithm != "pbkdf2_sha256" or not 100_000 <= iterations <= 1_000_000:
        return False

    actual = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(actual, expected)

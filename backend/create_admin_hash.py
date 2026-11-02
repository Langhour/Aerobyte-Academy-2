import getpass
import hashlib
import secrets

from app.admin_security import PBKDF2_ITERATIONS


def main() -> None:
    password = getpass.getpass("New admin password: ")
    confirmation = getpass.getpass("Confirm admin password: ")
    if len(password) < 12 or password != confirmation:
        raise SystemExit("Passwords must match and be at least 12 characters long.")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    print(f"ADMIN_PASSWORD_HASH=pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}")


if __name__ == "__main__":
    main()

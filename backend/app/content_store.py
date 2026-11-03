from datetime import datetime, timezone, timedelta

CAMBODIA_TZ = timezone(timedelta(hours=7))
import json
import os
import sqlite3
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Optional

from app.database import COURSES_DB
from app.models import Course, Coupon, EnrollmentRecord, SiteSettings


DATABASE_PATH = Path(
    os.getenv(
        "AEROBYTE_CONTENT_DB",
        str(Path(__file__).resolve().parents[1] / "data" / "aerobyte-content.sqlite3"),
    )
)
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()


class _PostgresConnection:
    """Small compatibility layer so existing store queries work on PostgreSQL."""

    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def _translate(statement: str) -> str:
        pragma_match = re.match(r"^\s*PRAGMA\s+TABLE_INFO\s*\(\s*([a-zA-Z0-9_]+)\s*\)", statement, re.I)
        if pragma_match:
            tbl = pragma_match.group(1).lower()
            return (
                f"SELECT column_name AS name FROM information_schema.columns "
                f"WHERE table_schema = current_schema() AND table_name = '{tbl}'"
            )
        statement = statement.replace("COLLATE NOCASE", "")
        statement = statement.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "BIGSERIAL PRIMARY KEY")
        statement = statement.replace("ORDER BY order_index ASC, rowid ASC", "ORDER BY order_index ASC, id ASC")
        statement = statement.replace("ORDER BY rowid DESC", "ORDER BY ctid DESC")
        statement = statement.replace("ORDER BY rowid", "ORDER BY id")
        statement = statement.replace("BLOB", "BYTEA")
        ignored_insert = statement.lstrip().upper().startswith("INSERT OR IGNORE")
        statement = re.sub(r"^\s*INSERT\s+OR\s+IGNORE\s+INTO", "INSERT INTO", statement, flags=re.I)
        statement = statement.replace("?", "%s")
        if ignored_insert and "ON CONFLICT" not in statement.upper():
            statement = statement.rstrip().rstrip(";") + " ON CONFLICT DO NOTHING"
        return statement

    def execute(self, statement, parameters=()):
        try:
            return self.connection.execute(self._translate(statement), parameters)
        except Exception as exc:
            import psycopg

            if isinstance(exc, psycopg.IntegrityError):
                raise sqlite3.IntegrityError(str(exc)) from exc
            raise

    def executemany(self, statement, parameters):
        try:
            translated = self._translate(statement)
            cursor = self.connection.cursor()
            for params in parameters:
                cursor.execute(translated, params)
            return cursor
        except Exception as exc:
            import psycopg

            if isinstance(exc, psycopg.IntegrityError):
                raise sqlite3.IntegrityError(str(exc)) from exc
            raise

    def executescript(self, script):
        for statement in script.split(";"):
            if statement.strip():
                self.execute(statement)


def _postgres_enabled() -> bool:
    return bool(DATABASE_URL)


@contextmanager
def _connect() -> Iterator[object]:
    if _postgres_enabled():
        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as raw_connection:
            yield _PostgresConnection(raw_connection)
        return
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATABASE_PATH.exists() or DATABASE_PATH.stat().st_size == 0:
        seed_db = Path(__file__).resolve().parents[2] / "seed_data" / "aerobyte-content.sqlite3"
        if not seed_db.exists():
            seed_db = Path(__file__).resolve().parents[1] / "data" / "aerobyte-content.sqlite3"
        if seed_db.exists() and seed_db.resolve() != DATABASE_PATH.resolve():
            import shutil
            try:
                shutil.copyfile(seed_db, DATABASE_PATH)
            except Exception:
                pass
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize_content_store() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                id TEXT PRIMARY KEY,
                slug TEXT NOT NULL UNIQUE,
                content_json TEXT NOT NULL,
                order_index INTEGER DEFAULT 0
            )
            """
        )
        course_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(courses)").fetchall()
        }
        if "order_index" not in course_columns:
            connection.execute("ALTER TABLE courses ADD COLUMN order_index INTEGER DEFAULT 0")
        zero_order_rows = connection.execute(
            "SELECT id FROM courses WHERE order_index IS NULL OR order_index = 0"
        ).fetchall()
        for idx, r in enumerate(zero_order_rows, start=1):
            connection.execute("UPDATE courses SET order_index = ? WHERE id = ?", (idx, r["id"]))
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS store_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                full_name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                google_sub TEXT
            );
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id TEXT PRIMARY KEY,
                transaction_id TEXT NOT NULL UNIQUE,
                content_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS coupons (
                code TEXT PRIMARY KEY,
                content_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS site_settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                content_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS admin_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                details TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS uploaded_files (
                filename TEXT PRIMARY KEY,
                content_type TEXT NOT NULL,
                data BLOB NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS login_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                user_email TEXT NOT NULL,
                user_name TEXT,
                role TEXT NOT NULL,
                login_method TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS visit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL,
                visitor_id TEXT,
                ip_address TEXT,
                user_agent TEXT,
                referrer TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                token_hash TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS email_verification_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                email TEXT NOT NULL COLLATE NOCASE,
                code_hash TEXT NOT NULL,
                token_hash TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL
            );
            """
        )
        user_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(users)").fetchall()
        }
        if "google_sub" not in user_columns:
            connection.execute("ALTER TABLE users ADD COLUMN google_sub TEXT")
        if "avatar_url" not in user_columns:
            connection.execute("ALTER TABLE users ADD COLUMN avatar_url TEXT")
        if "profile_json" not in user_columns:
            connection.execute("ALTER TABLE users ADD COLUMN profile_json TEXT DEFAULT '{}'")
        if "is_verified" not in user_columns:
            connection.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 1")
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS users_google_sub_unique "
            "ON users (google_sub) WHERE google_sub IS NOT NULL"
        )
        visit_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(visit_logs)").fetchall()
        }
        if "user_email" not in visit_columns:
            connection.execute("ALTER TABLE visit_logs ADD COLUMN user_email TEXT")
        if "user_name" not in visit_columns:
            connection.execute("ALTER TABLE visit_logs ADD COLUMN user_name TEXT")

        # Auto-link historical visits if path contained an email parameter
        try:
            email_visits = connection.execute(
                "SELECT DISTINCT visitor_id, path FROM visit_logs WHERE path LIKE '%email=%' AND (user_email IS NULL OR user_email = '')"
            ).fetchall()
            for row in email_visits:
                v_id = row["visitor_id"]
                p_text = row["path"]
                if v_id and "email=" in p_text:
                    from urllib.parse import urlparse, parse_qs
                    parsed = urlparse(p_text)
                    qs = parse_qs(parsed.query)
                    if "email" in qs and qs["email"]:
                        extracted_email = qs["email"][0].strip()
                        if extracted_email:
                            connection.execute(
                                "UPDATE visit_logs SET user_email = ? WHERE visitor_id = ? AND (user_email IS NULL OR user_email = '')",
                                (extracted_email, v_id),
                            )
        except Exception:
            pass

        upload_dir = Path(__file__).resolve().parents[1] / "data" / "uploads"
        if upload_dir.is_dir():
            for p in upload_dir.iterdir():
                if p.is_file() and p.stat().st_size > 0:
                    try:
                        existing = connection.execute(
                            "SELECT filename FROM uploaded_files WHERE filename = ?", (p.name,)
                        ).fetchone()
                        if not existing:
                            ext = p.suffix.lower()
                            media_type = "image/png" if ext == ".png" else ("image/jpeg" if ext in {".jpg", ".jpeg"} else "image/webp")
                            connection.execute(
                                "INSERT INTO uploaded_files (filename, content_type, data, created_at) VALUES (?, ?, ?, ?)",
                                (p.name, media_type, p.read_bytes(), datetime.now(timezone.utc).isoformat()),
                            )
                    except Exception:
                        pass
        # Ensure user profiles are strictly their own and not seeded from other users
        try:
            connection.execute(
                "UPDATE users SET profile_json = '{}' WHERE email = 'lghr2005@gmail.com' AND profile_json LIKE '%+855948010157%'"
            )
        except Exception:
            pass
        seeded = connection.execute(
            "SELECT 1 FROM store_metadata WHERE key = 'initial_courses_seeded'"
        ).fetchone()
        if seeded is None:
            connection.executemany(
                "INSERT INTO courses (id, slug, content_json) VALUES (?, ?, ?)",
                [
                    (course.id, course.slug, course.model_dump_json())
                    for course in COURSES_DB
                ],
            )
            connection.execute(
                "INSERT INTO store_metadata (key, value) VALUES ('initial_courses_seeded', 'true')"
            )
        for i, seed_course in enumerate(COURSES_DB):
            row = connection.execute(
                "SELECT content_json FROM courses WHERE id = ?",
                (seed_course.id,),
            ).fetchone()
            if row is None:
                connection.execute(
                    "INSERT INTO courses (id, slug, content_json, order_index) VALUES (?, ?, ?, ?)",
                    (seed_course.id, seed_course.slug, seed_course.model_dump_json(), i),
                )
                continue

            existing_course = Course.model_validate_json(row["content_json"])
            updates = {}
            if seed_course.slug == "microbit-robotics-courses":
                if existing_course.title == "MicroBit Robotics Courses":
                    updates["title"] = seed_course.title
                if existing_course.image_url.startswith(
                    "https://images.unsplash.com/photo-1485827404703-89b55fcc595e"
                ):
                    updates["image_url"] = seed_course.image_url
            if seed_course.title_kh:
                updates["title_kh"] = seed_course.title_kh
            if seed_course.short_description:
                updates["short_description"] = seed_course.short_description
            if seed_course.short_description_kh:
                updates["short_description_kh"] = seed_course.short_description_kh
            if seed_course.category_kh:
                updates["category_kh"] = seed_course.category_kh
            if seed_course.level:
                updates["level"] = seed_course.level
            if seed_course.level_kh:
                updates["level_kh"] = seed_course.level_kh
            if seed_course.duration:
                updates["duration"] = seed_course.duration
            if seed_course.duration_kh:
                updates["duration_kh"] = seed_course.duration_kh
            if seed_course.modules:
                updates["modules"] = seed_course.modules
            if seed_course.hardware_specs:
                updates["hardware_specs"] = seed_course.hardware_specs

            if updates:
                connection.execute(
                    "UPDATE courses SET content_json = ? WHERE id = ?",
                    (
                        existing_course.model_copy(update=updates).model_dump_json(),
                        seed_course.id,
                    ),
                )
        connection.execute(
            """
            INSERT OR IGNORE INTO site_settings (id, content_json)
            VALUES (1, ?)
            """,
            (SiteSettings().model_dump_json(),),
        )
        default_coupons = [
            Coupon(code="AEROBYTE10", value=10),
            Coupon(code="ROBOTICS20", value=20),
            Coupon(code="STUDENT50", value=50),
            Coupon(code="TEST1CENT", value=99),
        ]
        connection.executemany(
            "INSERT OR IGNORE INTO coupons (code, content_json) VALUES (?, ?)",
            [(coupon.code, coupon.model_dump_json()) for coupon in default_coupons],
        )

        # Sync any seed uploaded images
        seed_db = Path(__file__).resolve().parents[2] / "seed_data" / "aerobyte-content.sqlite3"
        if not seed_db.exists():
            seed_db = Path(__file__).resolve().parents[1] / "data" / "aerobyte-content.sqlite3"
        if seed_db.exists() and seed_db.resolve() != DATABASE_PATH.resolve():
            try:
                with sqlite3.connect(seed_db) as s_conn:
                    s_files = s_conn.execute("SELECT filename, content_type, data, created_at FROM uploaded_files").fetchall()
                    connection.executemany(
                        "INSERT OR IGNORE INTO uploaded_files (filename, content_type, data, created_at) VALUES (?, ?, ?, ?)",
                        s_files,
                    )
            except Exception:
                pass


def create_user(
    user_id: str,
    email: str,
    full_name: str,
    password_hash: str,
    created_at: str,
    is_verified: int = 1,
) -> None:
    with _connect() as connection:
        connection.execute(
            "INSERT INTO users (id, email, full_name, password_hash, created_at, is_verified) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, email.strip().casefold(), full_name.strip(), password_hash, created_at, is_verified),
        )


def find_user_by_email(email: str) -> Optional[dict[str, Any]]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT id, email, full_name, password_hash, created_at, is_verified, avatar_url, profile_json "
            "FROM users WHERE email = ? COLLATE NOCASE",
            (email.strip().casefold(),),
        ).fetchone()
    return dict(row) if row else None


def find_user_by_google_sub(google_sub: str) -> Optional[dict[str, Any]]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT id, email, full_name, password_hash, created_at, avatar_url, google_sub, profile_json "
            "FROM users WHERE google_sub = ?",
            (google_sub,),
        ).fetchone()
    return dict(row) if row else None


def create_google_user(
    user_id: str,
    email: str,
    full_name: str,
    password_hash: str,
    google_sub: str,
    created_at: str,
) -> None:
    with _connect() as connection:
        connection.execute(
            "INSERT INTO users (id, email, full_name, password_hash, created_at, google_sub) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                user_id,
                email.strip().casefold(),
                full_name.strip(),
                password_hash,
                created_at,
                google_sub,
            ),
        )


def link_google_user(user_id: str, google_sub: str) -> None:
    with _connect() as connection:
        row = connection.execute(
            "SELECT google_sub FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if row is None:
            raise ValueError("User account not found.")
        if row["google_sub"] not in (None, google_sub):
            raise ValueError("This account is linked to a different Google identity.")
        connection.execute(
            "UPDATE users SET google_sub = ?, is_verified = 1 WHERE id = ?",
            (google_sub, user_id),
        )


def find_user_by_id(user_id: str) -> Optional[dict[str, Any]]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT id, email, full_name, created_at, is_verified, avatar_url, google_sub, profile_json FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


def list_users() -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, email, full_name, created_at, is_verified, avatar_url, google_sub, profile_json "
            "FROM users ORDER BY created_at DESC"
        ).fetchall()
    users = []
    for row in rows:
        u = dict(row)
        raw_profile = u.get("profile_json") or "{}"
        profile_data = {}
        if isinstance(raw_profile, str):
            try:
                profile_data = json.loads(raw_profile)
            except Exception:
                profile_data = {}
        elif isinstance(raw_profile, dict):
            profile_data = raw_profile

        u["phone"] = profile_data.get("phone", "")
        u["telegram"] = profile_data.get("telegram", "")
        u["date_of_birth"] = profile_data.get("date_of_birth", "")
        u["location"] = profile_data.get("location", "")
        u["qualification"] = profile_data.get("qualification", "")
        u["qualification_other"] = profile_data.get("qualification_other", "")
        u["occupation"] = profile_data.get("occupation", "")
        u["experience"] = profile_data.get("experience", "")
        u["sign_in_method"] = "Google" if u.get("google_sub") else "Email / Password"
        users.append(u)
    return users


def admin_update_user(
    user_id: str,
    email: str,
    full_name: str,
    is_verified: int = 1,
    profile_data: Optional[dict[str, Any]] = None,
) -> Optional[dict[str, Any]]:
    with _connect() as connection:
        updates = ["email = ?", "full_name = ?", "is_verified = ?"]
        params: list[Any] = [email.strip().casefold(), full_name.strip(), int(is_verified)]
        if profile_data is not None:
            updates.append("profile_json = ?")
            params.append(json.dumps(profile_data, ensure_ascii=False))
        params.append(user_id)
        connection.execute(
            f"UPDATE users SET {', '.join(updates)} WHERE id = ?",
            tuple(params),
        )
    return find_user_by_id(user_id)


def admin_set_user_password(user_id: str, password_hash: str) -> bool:
    with _connect() as connection:
        cursor = connection.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (password_hash, user_id),
        )
        return bool(cursor.rowcount and cursor.rowcount > 0)


def admin_delete_user(user_id: str) -> bool:
    with _connect() as connection:
        connection.execute("DELETE FROM password_reset_tokens WHERE user_id = ?", (user_id,))
        connection.execute("DELETE FROM email_verification_tokens WHERE user_id = ?", (user_id,))
        cursor = connection.execute("DELETE FROM users WHERE id = ?", (user_id,))
        return bool(cursor.rowcount and cursor.rowcount > 0)


def update_user_profile(
    user_id: str,
    email: str,
    full_name: str,
    avatar_url: Optional[str] = None,
    profile_data: Optional[dict[str, Any]] = None,
) -> None:
    with _connect() as connection:
        updates = ["email = ?", "full_name = ?"]
        params = [email.strip().casefold(), full_name.strip()]
        if avatar_url is not None:
            updates.append("avatar_url = ?")
            params.append(avatar_url.strip())
        if profile_data is not None:
            updates.append("profile_json = ?")
            params.append(json.dumps(profile_data, ensure_ascii=False))
        params.append(user_id)
        connection.execute(
            f"UPDATE users SET {', '.join(updates)} WHERE id = ?",
            tuple(params),
        )


def update_user_avatar(user_id: str, avatar_url: str) -> None:
    with _connect() as connection:
        connection.execute(
            "UPDATE users SET avatar_url = ? WHERE id = ?",
            (avatar_url.strip(), user_id),
        )


def create_password_reset_token(token_hash: str, user_id: str, created_at: str, expires_at: str) -> None:
    with _connect() as connection:
        connection.execute("DELETE FROM password_reset_tokens WHERE user_id = ?", (user_id,))
        connection.execute(
            "INSERT INTO password_reset_tokens (token_hash, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (token_hash, user_id, created_at, expires_at),
        )


def delete_password_reset_token(token_hash: str) -> None:
    with _connect() as connection:
        connection.execute("DELETE FROM password_reset_tokens WHERE token_hash = ?", (token_hash,))


def password_reset_was_recently_requested(user_id: str, since: str) -> bool:
    with _connect() as connection:
        row = connection.execute(
            "SELECT 1 FROM password_reset_tokens WHERE user_id = ? AND created_at > ? LIMIT 1",
            (user_id, since),
        ).fetchone()
    return row is not None


def consume_password_reset_token(token_hash: str, now: str, password_hash: str) -> bool:
    with _connect() as connection:
        row = connection.execute(
            "SELECT user_id FROM password_reset_tokens WHERE token_hash = ? AND expires_at > ?",
            (token_hash, now),
        ).fetchone()
        if row is None:
            return False
        connection.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (password_hash, row["user_id"]),
        )
        connection.execute("DELETE FROM password_reset_tokens WHERE user_id = ?", (row["user_id"],))
        return True


def update_pending_user(user_id: str, full_name: str, password_hash: str) -> None:
    with _connect() as connection:
        connection.execute(
            "UPDATE users SET full_name = ?, password_hash = ? WHERE id = ? AND is_verified = 0",
            (full_name.strip(), password_hash, user_id),
        )


def create_email_verification_token(
    user_id: str,
    email: str,
    code_hash: str,
    token_hash: str,
    created_at: str,
    expires_at: str,
) -> None:
    with _connect() as connection:
        connection.execute("DELETE FROM email_verification_tokens WHERE user_id = ?", (user_id,))
        connection.execute(
            "INSERT INTO email_verification_tokens (user_id, email, code_hash, token_hash, created_at, expires_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, email.strip().casefold(), code_hash, token_hash, created_at, expires_at),
        )


def verify_user_email_by_code(email: str, code_hash: str, now: str) -> Optional[dict[str, Any]]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT user_id FROM email_verification_tokens "
            "WHERE email = ? COLLATE NOCASE AND code_hash = ? AND expires_at > ?",
            (email.strip().casefold(), code_hash, now),
        ).fetchone()
        if not row:
            return None
        user_id = row["user_id"]
        connection.execute("UPDATE users SET is_verified = 1 WHERE id = ?", (user_id,))
        connection.execute("DELETE FROM email_verification_tokens WHERE user_id = ?", (user_id,))
        user_row = connection.execute(
            "SELECT id, email, full_name, password_hash, created_at, is_verified, avatar_url, profile_json "
            "FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(user_row) if user_row else None


def verify_user_email_by_token(token_hash: str, now: str) -> Optional[dict[str, Any]]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT user_id FROM email_verification_tokens "
            "WHERE token_hash = ? AND expires_at > ?",
            (token_hash, now),
        ).fetchone()
        if not row:
            return None
        user_id = row["user_id"]
        connection.execute("UPDATE users SET is_verified = 1 WHERE id = ?", (user_id,))
        connection.execute("DELETE FROM email_verification_tokens WHERE user_id = ?", (user_id,))
        user_row = connection.execute(
            "SELECT id, email, full_name, password_hash, created_at, is_verified, avatar_url, profile_json "
            "FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(user_row) if user_row else None


def email_verification_was_recently_sent(user_id: str, since: str) -> bool:
    with _connect() as connection:
        row = connection.execute(
            "SELECT 1 FROM email_verification_tokens WHERE user_id = ? AND created_at > ? LIMIT 1",
            (user_id, since),
        ).fetchone()
    return row is not None


def list_courses() -> list[Course]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT content_json, order_index FROM courses ORDER BY order_index ASC, rowid ASC"
        ).fetchall()
    courses = []
    for row in rows:
        course = Course.model_validate_json(row["content_json"])
        course.order_index = row["order_index"]
        courses.append(course)
    return courses


def list_published_courses() -> list[Course]:
    return [course for course in list_courses() if course.status == "published"]


def find_course(course_id: str) -> Optional[Course]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT content_json, order_index FROM courses WHERE id = ? OR slug = ?",
            (course_id, course_id),
        ).fetchone()
    if not row:
        return None
    course = Course.model_validate_json(row["content_json"])
    course.order_index = row["order_index"]
    return course


def save_course(course: Course) -> None:
    with _connect() as connection:
        row = connection.execute("SELECT order_index FROM courses WHERE id = ?", (course.id,)).fetchone()
        order_index = row["order_index"] if row and row["order_index"] else (course.order_index or 0)
        if not order_index:
            max_row = connection.execute("SELECT MAX(order_index) as max_idx FROM courses").fetchone()
            order_index = (max_row["max_idx"] or 0) + 1 if max_row else 1
        course.order_index = order_index
        connection.execute(
            """
            INSERT INTO courses (id, slug, content_json, order_index) VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                slug = excluded.slug,
                content_json = excluded.content_json,
                order_index = excluded.order_index
            """,
            (course.id, course.slug, course.model_dump_json(), order_index),
        )


def delete_course(course_id: str) -> bool:
    with _connect() as connection:
        cursor = connection.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        return cursor.rowcount > 0


def create_course(course: Course) -> None:
    with _connect() as connection:
        max_row = connection.execute("SELECT MAX(order_index) as max_idx FROM courses").fetchone()
        order_index = (max_row["max_idx"] or 0) + 1 if max_row else 1
        course.order_index = order_index
        connection.execute(
            "INSERT INTO courses (id, slug, content_json, order_index) VALUES (?, ?, ?, ?)",
            (course.id, course.slug, course.model_dump_json(), order_index),
        )


def reorder_courses(course_ids: list[str]) -> None:
    with _connect() as connection:
        for index, course_id in enumerate(course_ids, start=1):
            row = connection.execute("SELECT content_json FROM courses WHERE id = ?", (course_id,)).fetchone()
            if row:
                course = Course.model_validate_json(row["content_json"])
                course.order_index = index
                connection.execute(
                    "UPDATE courses SET order_index = ?, content_json = ? WHERE id = ?",
                    (index, course.model_dump_json(), course_id),
                )
            else:
                connection.execute(
                    "UPDATE courses SET order_index = ? WHERE id = ?",
                    (index, course_id),
                )


def list_enrollments() -> list[EnrollmentRecord]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT content_json FROM enrollments ORDER BY rowid DESC"
        ).fetchall()
    return [EnrollmentRecord.model_validate_json(row["content_json"]) for row in rows]


def find_enrollment(enrollment_id: str) -> Optional[EnrollmentRecord]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT content_json FROM enrollments WHERE enrollment_id = ?",
            (enrollment_id,),
        ).fetchone()
    return EnrollmentRecord.model_validate_json(row["content_json"]) if row else None


def find_enrollments_by_email(email: str) -> list[EnrollmentRecord]:
    if not email or not email.strip():
        return []
    target = email.strip().casefold()
    return [
        record for record in list_enrollments()
        if record.email and record.email.strip().casefold() == target
    ]


def save_enrollment(record: EnrollmentRecord) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO enrollments (enrollment_id, transaction_id, content_json)
            VALUES (?, ?, ?)
            ON CONFLICT(enrollment_id) DO UPDATE SET content_json = excluded.content_json
            """,
            (record.enrollment_id, record.transaction_id, record.model_dump_json()),
        )


def list_coupons() -> list[Coupon]:
    with _connect() as connection:
        rows = connection.execute("SELECT content_json FROM coupons ORDER BY code").fetchall()
    return [Coupon.model_validate_json(row["content_json"]) for row in rows]


def find_coupon(code: str) -> Optional[Coupon]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT content_json FROM coupons WHERE code = ?", (code.upper(),)
        ).fetchone()
    return Coupon.model_validate_json(row["content_json"]) if row else None


def save_coupon(coupon: Coupon) -> None:
    normalized = coupon.model_copy(update={"code": coupon.code.strip().upper()})
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO coupons (code, content_json) VALUES (?, ?)
            ON CONFLICT(code) DO UPDATE SET content_json = excluded.content_json
            """,
            (normalized.code, normalized.model_dump_json()),
        )


def delete_coupon(code: str) -> bool:
    with _connect() as connection:
        cursor = connection.execute("DELETE FROM coupons WHERE code = ?", (code.upper(),))
        return cursor.rowcount > 0


def increment_coupon_usage(code: str) -> None:
    coupon = find_coupon(code)
    if coupon is None:
        return
    save_coupon(coupon.model_copy(update={"usage_count": coupon.usage_count + 1}))


def get_site_settings() -> SiteSettings:
    with _connect() as connection:
        row = connection.execute(
            "SELECT content_json FROM site_settings WHERE id = 1"
        ).fetchone()
    return SiteSettings.model_validate_json(row["content_json"])


def save_site_settings(settings: SiteSettings) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO site_settings (id, content_json) VALUES (1, ?)
            ON CONFLICT(id) DO UPDATE SET content_json = excluded.content_json
            """,
            (settings.model_dump_json(),),
        )


def log_admin_activity(action: str, details: str, created_at: str) -> None:
    with _connect() as connection:
        connection.execute(
            "INSERT INTO admin_activity (action, details, created_at) VALUES (?, ?, ?)",
            (action, details, created_at),
        )


def list_admin_activity(limit: int = 20) -> list[dict[str, str]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT action, details, created_at FROM admin_activity ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]

def save_uploaded_file(filename: str, content_type: str, data: bytes) -> None:
    now_iso = datetime.now(timezone.utc).isoformat()
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO uploaded_files (filename, content_type, data, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(filename) DO UPDATE SET
                content_type = excluded.content_type,
                data = excluded.data
            """,
            (filename, content_type, data, now_iso),
        )


def get_uploaded_file(filename: str) -> Optional[dict[str, Any]]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT filename, content_type, data, created_at FROM uploaded_files WHERE filename = ?",
            (filename,),
        ).fetchone()
        if not row:
            return None
        data = row["data"]
        if isinstance(data, memoryview):
            data = bytes(data)
        elif not isinstance(data, bytes):
            data = bytes(data)
        return {
            "filename": row["filename"],
            "content_type": row["content_type"],
            "data": data,
            "created_at": row["created_at"],
        }


def delete_uploaded_file(filename: str) -> None:
    with _connect() as connection:
        connection.execute("DELETE FROM uploaded_files WHERE filename = ?", (filename,))

def log_login_event(
    user_id: str,
    user_email: str,
    user_name: str,
    role: str,
    login_method: str,
    ip_address: str,
    user_agent: str,
    status: str = "success",
) -> None:
    now_cam = datetime.now(CAMBODIA_TZ).strftime("%b %d, %Y %I:%M %p")
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO login_logs (user_id, user_email, user_name, role, login_method, ip_address, user_agent, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id or "",
                user_email or "",
                user_name or "",
                role or "User",
                login_method or "Credentials",
                ip_address or "",
                user_agent or "",
                status or "success",
                now_cam,
            ),
        )


def log_visit_event(
    path: str,
    visitor_id: str,
    ip_address: str,
    user_agent: str,
    referrer: str = "",
    user_email: str = "",
    user_name: str = "",
) -> None:
    now_cam = datetime.now(CAMBODIA_TZ).strftime("%b %d, %Y %I:%M %p")
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO visit_logs (path, visitor_id, ip_address, user_agent, referrer, user_email, user_name, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                path or "/",
                visitor_id or "",
                ip_address or "",
                user_agent or "",
                referrer or "",
                user_email or "",
                user_name or "",
                now_cam,
            ),
        )
        if user_email and visitor_id:
            try:
                connection.execute(
                    """
                    UPDATE visit_logs
                    SET user_email = ?,
                        user_name = CASE WHEN user_name IS NULL OR user_name = '' THEN ? ELSE user_name END
                    WHERE visitor_id = ? AND (user_email IS NULL OR user_email = '')
                    """,
                    (user_email, user_name or user_email, visitor_id),
                )
            except Exception:
                pass


def get_traffic_summary() -> dict[str, Any]:
    today_prefix = datetime.now(CAMBODIA_TZ).strftime("%b %d, %Y")
    with _connect() as connection:
        total_visits_row = connection.execute("SELECT COUNT(*) AS total FROM visit_logs").fetchone()
        unique_visitors_row = connection.execute("SELECT COUNT(DISTINCT visitor_id) AS total FROM visit_logs").fetchone()
        total_logins_row = connection.execute("SELECT COUNT(*) AS total FROM login_logs").fetchone()
        
        today_visits_row = connection.execute(
            "SELECT COUNT(*) AS total FROM visit_logs WHERE created_at LIKE ?",
            (f"{today_prefix}%",),
        ).fetchone()
        today_logins_row = connection.execute(
            "SELECT COUNT(*) AS total FROM login_logs WHERE created_at LIKE ?",
            (f"{today_prefix}%",),
        ).fetchone()

        top_pages_rows = connection.execute(
            """
            SELECT path, COUNT(*) as count 
            FROM visit_logs 
            GROUP BY path 
            ORDER BY count DESC 
            LIMIT 10
            """
        ).fetchall()

    return {
        "total_visits": (total_visits_row["total"] if total_visits_row else 0) or 0,
        "unique_visitors": (unique_visitors_row["total"] if unique_visitors_row else 0) or 0,
        "total_logins": (total_logins_row["total"] if total_logins_row else 0) or 0,
        "today_visits": (today_visits_row["total"] if today_visits_row else 0) or 0,
        "today_logins": (today_logins_row["total"] if today_logins_row else 0) or 0,
        "top_pages": [{"path": r["path"], "count": r["count"]} for r in top_pages_rows],
    }


def list_login_logs(limit: int = 100, role: Optional[str] = None) -> list[dict[str, Any]]:
    with _connect() as connection:
        if role and role.strip() and role.lower() != "all":
            rows = connection.execute(
                "SELECT * FROM login_logs WHERE LOWER(role) = LOWER(?) ORDER BY id DESC LIMIT ?",
                (role.strip(), limit),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM login_logs ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
    return [dict(r) for r in rows]


def list_visit_logs(limit: int = 100) -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT * FROM visit_logs ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


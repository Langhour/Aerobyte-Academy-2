import os
import sys
from pathlib import Path

# Load .env if present in root or backend
for env_path in (
    Path(__file__).resolve().parent / ".env",
    Path(__file__).resolve().parent / "backend" / ".env",
):
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                key = k.strip()
                val = v.strip().strip("'\"")
                if key and val and not os.environ.get(key):
                    os.environ[key] = val

# Ensure backend directory is in sys.path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app

if __name__ == "__main__":
    import uvicorn
    # Check PORT, SERVER_PORT (Botkeep/Pterodactyl), or WEB_PORT
    raw_port = (
        os.environ.get("PORT")
        or os.environ.get("SERVER_PORT")
        or os.environ.get("WEB_PORT")
        or "8010"
    )
    port = int(raw_port)
    print(f"[AeroByte] Starting Uvicorn on 0.0.0.0:{port}...", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)

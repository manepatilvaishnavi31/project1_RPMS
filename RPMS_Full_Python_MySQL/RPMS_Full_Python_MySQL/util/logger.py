from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parents[1] / "activity_log.txt"

def log(message):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | {message}\n")

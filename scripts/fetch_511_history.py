"""Download one month of 511's history for the Bay Area: every transit agency's
timetable for that month plus stop_observations.txt, the time each vehicle
actually reached each stop.

    python scripts/fetch_511_history.py 2026-09

Saves data/raw/511/2026-09-so.zip (~575 MB zipped, ~3.4 GB unzipped).

Your 511 API key is read from the environment variable API_KEY_511, or from a
line `API_KEY_511=...` in a file named .env at the repo root (.env is in
.gitignore, so it never gets committed). The key is never printed.

511 allows 60 requests per hour per key, shared with everything else using it
(buni's collector uses ~55), and each month is one request.
"""

import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "https://api.511.org/transit/datafeeds?api_key={key}&operator_id=RG&historic={month}-so"


def api_key() -> str:
    key = os.environ.get("API_KEY_511", "")
    env = ROOT / ".env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.strip().startswith("API_KEY_511="):
                key = line.split("=", 1)[1].strip().strip("\"'")
    if not key:
        sys.exit("No 511 key: put API_KEY_511=<your key> in .env at the repo root.")
    return key


def main() -> None:
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}", sys.argv[1]):
        sys.exit("usage: python scripts/fetch_511_history.py YYYY-MM")
    month = sys.argv[1]
    out = ROOT / "data" / "raw" / "511" / f"{month}-so.zip"
    if out.exists():
        sys.exit(f"{out.relative_to(ROOT)} already exists")
    out.parent.mkdir(parents=True, exist_ok=True)
    part = out.with_suffix(".zip.part")
    req = urllib.request.Request(URL.format(key=api_key(), month=month), headers={"User-Agent": "buni-arrivals/0.1"})
    started, done = time.time(), 0
    try:
        with urllib.request.urlopen(req, timeout=120) as r, open(part, "wb") as f:
            total = int(r.headers.get("Content-Length") or 0)
            while chunk := r.read(1 << 20):
                f.write(chunk)
                done += len(chunk)
                pct = f" of {total / 1e6:.0f}" if total else ""
                print(f"\r{done / 1e6:.0f}{pct} MB", end="", flush=True)
    except urllib.error.HTTPError as e:  # the message never includes the key
        part.unlink(missing_ok=True)
        sys.exit(f"\n511 said {e.code} {e.reason}" + (" (hourly limit: try again later)" if e.code == 429 else ""))
    part.rename(out)
    print(f"\nsaved {out.relative_to(ROOT)} ({done / 1e6:.0f} MB in {time.time() - started:.0f} s)")


if __name__ == "__main__":
    main()

"""Download the pinned Fliar/Fliar BI CC BY-NC global funding sample.

The source release contains a 25% company-hash sample, not the full 80,911-round
dataset. Its license is non-commercial; see SOURCES.md before reuse.
"""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "data" / "raw" / "global_startup_funding_sample.csv"
SOURCE_COMMIT = "225b3e0e84e5ed4a45b5311b20760930cfde9c72"
URL = f"https://raw.githubusercontent.com/Busineessfree/global-startup-funding/{SOURCE_COMMIT}/global_startup_funding_sample.csv"
EXPECTED_SHA256 = "1f1602f2a8266418899457527aec906ab32f8e19b97375c06f673492ee7e03f0"


def main() -> None:
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    if DESTINATION.exists():
        existing = hashlib.sha256(DESTINATION.read_bytes()).hexdigest()
        if existing == EXPECTED_SHA256:
            print(f"Verified existing file: {DESTINATION}")
            return
    request = urllib.request.Request(URL, headers={"User-Agent": "VentureInsight/1.0 (educational dataset importer)"})
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"Source checksum mismatch: expected {EXPECTED_SHA256}, got {digest}; file not written.")
    temporary = DESTINATION.with_suffix(".csv.part")
    temporary.write_bytes(payload)
    temporary.replace(DESTINATION)
    print(f"Downloaded and verified {len(payload):,} bytes: {DESTINATION}")
    print("License: CC BY-NC 4.0; attribution: Fliar Research / Fliar BI.")


if __name__ == "__main__":
    main()

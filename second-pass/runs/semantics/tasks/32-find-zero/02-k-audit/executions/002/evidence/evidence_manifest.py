#!/usr/bin/env python3
"""Hash reviewer evidence and summarize recorded command exit markers."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path("/audit-output/evidence")
OUTPUT = ROOT / "evidence-manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    records = []
    for path in sorted(ROOT.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path == OUTPUT:
            continue
        record: dict[str, object] = {
            "name": path.name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        if path.suffix == ".log":
            text = path.read_text(errors="replace")
            exits = re.findall(r"EXIT_STATUS=(\d+)", text)
            command_exits = re.findall(r'COMMAND_EXIT_CODE="(\d+)"', text)
            record["exit_status_markers"] = [int(value) for value in exits]
            record["recorder_exit_markers"] = [
                int(value) for value in command_exits
            ]
            record["contains_top"] = "#Top" in text
            record["contains_stuck_claim"] = "WarnStuckClaimState" in text
        records.append(record)
    payload = {"record_count": len(records), "records": records}
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUTPUT}")
    print(f"records hashed: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

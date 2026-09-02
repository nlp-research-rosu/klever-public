#!/usr/bin/env python3
"""Read and inventory all launcher-required legacy generation records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path("/generation-evidence")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/generation_record_inventory.py")
    for name in (
        "invocation.json",
        "metrics.json",
        "usage.json",
        "codex-last.txt",
        "codex-output.log",
        "prompt.txt",
    ):
        path = ROOT / name
        text = path.read_text(errors="replace")
        print(
            f"READ {path}: bytes={len(text.encode())} "
            f"lines={len(text.splitlines())} sha256={sha(path)}"
        )
        if name.endswith(".json"):
            parsed = json.loads(text)
            print(f"  JSON_KEYS: {','.join(sorted(parsed))}")
        if name == "codex-output.log":
            for needle in (
                "apply_patch",
                "kprove",
                "krun",
                "#Top",
                "WarnStuckClaimState",
                "RESULT: KPROVE_PASSED",
            ):
                print(f"  COUNT {needle!r}: {text.count(needle)}")
        if name == "codex-last.txt":
            print(f"  FINAL_MARKER_PRESENT: {'RESULT: KPROVE_PASSED' in text}")
    print("GENERATION_RECORD_INVENTORY: PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Write deterministic SHA-256 manifest for final audit artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"
OUTPUT = EVIDENCE / "MANIFEST.sha256"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths = [ROOT / "REVIEW.md"]
    paths.extend(
        path
        for path in sorted(EVIDENCE.iterdir())
        if path.is_file() and path != OUTPUT
    )
    lines = []
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        lines.append(f"{digest(path)}  {relative}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifest_entries={len(lines)}")
    print(f"manifest_path={OUTPUT}")
    print(f"manifest_sha256={digest(OUTPUT)}")


if __name__ == "__main__":
    main()

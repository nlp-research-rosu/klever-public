#!/usr/bin/env python3
"""Write a deterministic SHA-256 manifest of preserved audit evidence."""

from __future__ import annotations

import hashlib
from pathlib import Path


root = Path("/audit-output/evidence")
output = root / "EVIDENCE_SHA256.txt"
lines: list[str] = []
for path in sorted(root.rglob("*")):
    if not path.is_file() or path == output:
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
output.write_text("\n".join(lines) + "\n")
print(f"manifest={output}")
print(f"files={len(lines)}")

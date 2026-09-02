#!/usr/bin/env python3
"""Write SHA-256 manifest for preserved evidence, excluding the manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


root = Path("/audit-output/evidence")
lines = []
for path in sorted(root.iterdir()):
    if not path.is_file() or path.name == "manifest.sha256":
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path.name}")
(root / "manifest.sha256").write_text("\n".join(lines) + "\n")
print(f"manifest_entries={len(lines)}")

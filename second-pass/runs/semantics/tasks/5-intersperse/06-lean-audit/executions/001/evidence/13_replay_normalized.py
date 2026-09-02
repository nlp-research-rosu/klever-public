#!/usr/bin/env python3
"""Confirm replay input-manifest difference is only the read-only mount prefix."""

from __future__ import annotations

import json
from pathlib import Path


selected = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
replayed = json.loads(
    Path("/tmp/audit-work/stage4-replay/input-manifest.json").read_text()
)

replayed_paths = replayed["required_k_files"]
assert all(path.startswith("/reference/k-proof/") for path in replayed_paths)
replayed["required_k_files"] = [
    "/frozen-k/" + path.removeprefix("/reference/k-proof/")
    for path in replayed_paths
]
assert replayed == selected
print(
    "PASS: input manifests are identical after replacing the audit mount "
    "prefix /reference/k-proof/ with generation-time /frozen-k/"
)

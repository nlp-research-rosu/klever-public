#!/usr/bin/env python3
"""Check the launcher-recorded mechanical checker and toolchain locks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    print(("PASS " if condition else "FAIL ") + message)
    if not condition:
        raise SystemExit(1)


audit = json.loads(Path("/audit-input.json").read_text())
lock_path = Path("/opt/humaneval/data/klean-audit-tools.lock.json")
lock = json.loads(lock_path.read_text())
require(sha(lock_path) == audit["audit"]["mechanical_checker_lock_sha256"], "mechanical checker lock hash matches audit input")
for relative, expected in sorted(lock["files"].items()):
    mounted = Path("/reference") / relative
    require(mounted.is_file() and sha(mounted) == expected, f"trusted checker file {relative}")

reference_toolchain = Path("/reference/klean-toolchain.lock.json")
image_toolchain = Path("/opt/humaneval/data/klean-toolchain.lock.json")
require(sha(reference_toolchain) == sha(image_toolchain), "mounted and audit-image toolchain locks are byte-identical")
toolchain = json.loads(reference_toolchain.read_text())
generator = json.loads(Path("/reference/klean-generation/generator-manifest.json").read_text())
require(generator["toolchain"] == toolchain, "generator manifest toolchain equals trusted lock")

preflight = json.loads(Path("/reference/klean-generation/preflight.json").read_text())
for diagnostic in preflight["diagnostics"]:
    tail = diagnostic["output_tail"]
    # Both stored outputs are shorter than check_generation's 4000-byte tail
    # limit, so the tail is the complete hashed output.
    require(len(tail) < 4000, f"stored {' '.join(diagnostic['command'])} output is complete")
    require(hashlib.sha256(tail.encode()).hexdigest() == diagnostic["output_sha256"], f"stored {' '.join(diagnostic['command'])} output hash")

print("TRUSTED_TOOL_AND_RECORDED_DIAGNOSTIC_HASHES_PASS")

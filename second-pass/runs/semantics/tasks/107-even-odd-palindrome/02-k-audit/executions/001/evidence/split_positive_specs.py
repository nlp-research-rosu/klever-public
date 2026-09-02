#!/usr/bin/env python3
"""Split the four submitted entry claims so each can be proved independently."""

from __future__ import annotations

import hashlib
from pathlib import Path


scratch = Path("/tmp/audit-work/reconstruction")
evidence = Path("/audit-output/evidence")
source = (scratch / "spec.k").read_text()

prefix = 'requires "verification.k"\n\nmodule SPEC\n  imports VERIFICATION\n\n'
suffix = "\n\nendmodule\n"
if not source.startswith(prefix) or not source.endswith(suffix):
    raise SystemExit("unexpected submitted spec.k framing")

body = source[len(prefix) : -len(suffix)]
parts = body.split("\n\n  claim\n")
if not parts or not parts[0].startswith("  claim\n"):
    raise SystemExit("unexpected first claim")
claims = [parts[0]] + ["  claim\n" + part for part in parts[1:]]
if len(claims) != 4:
    raise SystemExit(f"expected 4 claims, found {len(claims)}")

for index, claim in enumerate(claims, 1):
    module = f"SPEC-CLAIM-{index}"
    rendered = (
        'requires "verification.k"\n\n'
        f"module {module}\n"
        "  imports VERIFICATION\n\n"
        f"{claim}\n\n"
        "endmodule\n"
    )
    name = f"spec-claim-{index}.k"
    (scratch / name).write_text(rendered)
    (evidence / name).write_text(rendered)
    digest = hashlib.sha256(claim.encode()).hexdigest()
    print(f"{name} module={module} claim_sha256={digest}")

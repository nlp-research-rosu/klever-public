#!/usr/bin/env python3
"""Cross-check launcher metadata against independently inspected mounts."""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys


audit_input = json.loads(pathlib.Path("/audit-input.json").read_text())
campaign_lock = json.loads(pathlib.Path("/audit-campaign-lock.json").read_text())
lock_hash = hashlib.sha256(
    pathlib.Path("/audit-campaign-lock.json").read_bytes()
).hexdigest()

print(f"campaign_equal={audit_input['audit_campaign'] == campaign_lock}")
print(f"lock_sha256={lock_hash}")
print(
    "recorded_lock_sha256="
    f"{audit_input['hashes']['audit_campaign_lock_sha256']}"
)

required = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/generation-evidence/codex-trace",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
    "/candidate/prompt.py",
    "/candidate/py2mpy.py",
    "/candidate/solution.py",
    "/candidate/solution.mpy",
    "/candidate/semantic.k",
    "/candidate/verification.k",
    "/candidate/spec.k",
    "/candidate/prove.sh",
]

all_present = True
for name in required:
    path = pathlib.Path(name)
    expected_type = path.is_dir() if name.endswith("codex-trace") else path.is_file()
    okay = path.exists() and not path.is_symlink() and expected_type
    print(f"required={name} expected_type_non_symlink={okay}")
    all_present &= okay

reference_semantics = pathlib.Path("/reference/reference-semantics")
semantics_absent = not reference_semantics.exists() and not reference_semantics.is_symlink()
print(f"reference_semantics_absent={semantics_absent}")

input_pairs = [
    ("/candidate/prompt.py", "/reference/prompt.py"),
    ("/candidate/py2mpy.py", "/reference/py2mpy.py"),
]
input_matches = True
for candidate_name, trusted_name in input_pairs:
    candidate_bytes = pathlib.Path(candidate_name).read_bytes()
    trusted_bytes = pathlib.Path(trusted_name).read_bytes()
    equal = candidate_bytes == trusted_bytes
    input_matches &= equal
    print(
        f"byte_equal {candidate_name} {trusted_name}={equal} "
        f"sha256={hashlib.sha256(candidate_bytes).hexdigest()}"
    )

checks = [
    audit_input["audit_campaign"] == campaign_lock,
    lock_hash == audit_input["hashes"]["audit_campaign_lock_sha256"],
    all_present,
    semantics_absent,
    input_matches,
]
if not all(checks):
    sys.exit(1)

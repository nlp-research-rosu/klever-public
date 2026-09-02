#!/usr/bin/env python3
"""Recompute the pipeline-v3 manifest tree hashes with the harness algorithm."""

from pathlib import Path
import sys

sys.path.insert(0, "/opt/humaneval/tools")
from pipeline_contract import sha256_tree  # noqa: E402


checks = [
    (
        "/candidate",
        "generation-result.json outputs.workspace_sha256",
        "f8a9295f1f12ff25366a0c3eba30f6a8cf0865d89e46560b854375f4708c04b6",
    ),
    (
        "/candidate/reference-semantics",
        "task.json inputs.reference_semantics_sha256",
        "4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f",
    ),
    (
        "/reference/reference-semantics",
        "audit-input.json hashes.trusted_reference_semantics_manifest_sha256",
        "4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f",
    ),
    (
        "/generation-evidence/codex-trace",
        "usage.json source_trace_sha256",
        "b3ae09fd33690e1becbc98dcca8ea6935c1148ef62843c5e8dca65c83c79cfc8",
    ),
]

print("COMMAND: python3 /audit-output/evidence/01b_manifest_tree_hashes.py")
failed = False
for raw_path, field, expected in checks:
    actual = sha256_tree(Path(raw_path))
    matches = actual == expected
    failed |= not matches
    print(
        f"TREE path={raw_path} recorded_field={field} "
        f"expected={expected} actual={actual} match={matches}"
    )
raise SystemExit(1 if failed else 0)

#!/usr/bin/env python3
"""Recompute deterministic mounted-tree hashes with the pipeline algorithm."""

from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, "/opt/humaneval/tools")
import pipeline_contract  # noqa: E402
import klean_export  # noqa: E402


audit = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
checks = {
    "candidate_tree_sha256": Path("/candidate"),
    "candidate_reference_semantics_sha256": Path(
        "/candidate/reference-semantics"
    ),
    "trusted_reference_semantics_sha256": Path(
        "/reference/reference-semantics"
    ),
    "generation_codex_trace_sha256": Path(
        "/generation-evidence/codex-trace"
    ),
}
for field, path in checks.items():
    pipeline_actual = pipeline_contract.sha256_tree(path)
    content_actual = klean_export.tree_digest(path)
    expected = audit["hashes"][field]
    print(
        f"{field}: expected={expected}; "
        f"pipeline_sha256_tree={pipeline_actual}; "
        f"content_tree_digest={content_actual}; "
        f"pipeline_match={pipeline_actual == expected}; "
        f"content_match={content_actual == expected}"
    )

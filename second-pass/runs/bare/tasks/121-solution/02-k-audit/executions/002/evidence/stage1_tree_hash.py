#!/usr/bin/env python3
"""Recompute mounted tree hashes with the pipeline's recorded hash contract."""

from pathlib import Path
import sys

sys.path.insert(0, "/opt/humaneval/tools")
from pipeline_contract import sha256_tree


candidate = sha256_tree(Path("/candidate"))
trace = sha256_tree(Path("/generation-evidence/codex-trace"))
print(f"mounted_candidate_pipeline_sha256={candidate}")
print(
    "generation-result/invocation retained workspace sha256="
    "21f8d91bbf47e4943ac6cf5a1a82f04e4f4b735dac5e7acc9e95ff4be65d0e9c"
)
print(f"candidate_matches_retained_workspace={candidate == '21f8d91bbf47e4943ac6cf5a1a82f04e4f4b735dac5e7acc9e95ff4be65d0e9c'}")
print(f"mounted_trace_pipeline_sha256={trace}")
print(
    "usage source_trace_sha256="
    "357aa564fbf2d37f9068e22240c09ec739cce055c01254a37955f0484d0ff5ff"
)
print(f"trace_matches_usage_source={trace == '357aa564fbf2d37f9068e22240c09ec739cce055c01254a37955f0484d0ff5ff'}")

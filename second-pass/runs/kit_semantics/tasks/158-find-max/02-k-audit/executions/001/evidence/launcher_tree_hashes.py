#!/usr/bin/env python3
from pathlib import Path

from pipeline_contract import sha256_tree


for label, path in [
    ("candidate", Path("/candidate")),
    ("candidate_semantics", Path("/candidate/reference-semantics")),
    ("trusted_semantics", Path("/reference/reference-semantics")),
    ("generation_trace", Path("/generation-evidence/codex-trace")),
]:
    print(label, sha256_tree(path))

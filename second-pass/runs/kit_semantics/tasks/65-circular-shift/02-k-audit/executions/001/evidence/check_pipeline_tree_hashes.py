#!/usr/bin/env python3
"""Independently recompute pipeline-v3 aggregate tree hashes on mounted inputs."""

import importlib.util
import json
import sys
from pathlib import Path


def load_json(path: str) -> dict:
    with Path(path).open("r", encoding="utf-8") as stream:
        return json.load(stream)


contract_path = Path("/opt/humaneval/tools/pipeline_contract.py")
spec = importlib.util.spec_from_file_location("pipeline_contract", contract_path)
assert spec is not None and spec.loader is not None
contract = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = contract
spec.loader.exec_module(contract)

audit_input = load_json("/audit-input.json")
generation_result = load_json("/generation-result.json")
invocation = load_json("/generation-evidence/invocation.json")
task = load_json("/task.json")
usage = load_json("/generation-evidence/usage.json")

candidate_hash = contract.sha256_tree(Path("/candidate"))
candidate_expected = generation_result["outputs"]["workspace_sha256"]
assert candidate_hash == candidate_expected
assert candidate_hash == invocation["outputs"]["workspace_sha256"]

semantics_hash = contract.sha256_tree(Path("/reference/reference-semantics"))
semantics_expected = task["inputs"]["reference_semantics_sha256"]
assert semantics_hash == semantics_expected
assert (
    semantics_hash
    == audit_input["hashes"]["trusted_reference_semantics_manifest_sha256"]
)

trace_hash = contract.sha256_tree(Path("/generation-evidence/codex-trace"))
trace_expected = usage["source_trace_sha256"]
assert trace_hash == trace_expected

print(f"pipeline_contract={contract_path}")
print(f"candidate_pipeline_tree_sha256={candidate_hash} MATCH")
print(f"reference_semantics_pipeline_tree_sha256={semantics_hash} MATCH")
print(f"generation_trace_pipeline_tree_sha256={trace_hash} MATCH")
print(
    "launcher_candidate_snapshot_sha256="
    f"{audit_input['hashes']['candidate_tree_sha256']} RECORDED"
)
print(
    "launcher_reference_semantics_snapshot_sha256="
    f"{audit_input['hashes']['trusted_reference_semantics_sha256']} RECORDED"
)
print("RESULT: PASS")

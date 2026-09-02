#!/usr/bin/env python3
"""Recheck launcher records and mounted provenance without trusting claims."""

from __future__ import annotations

import hashlib
import json
import stat
import sys
from pathlib import Path


sys.path.insert(0, "/opt/humaneval/tools")
import pipeline_contract  # type: ignore  # launcher pipeline digest implementation


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text())
campaign_lock = json.loads(Path("/audit-campaign-lock.json").read_text())
hashes = audit_input["hashes"]

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_block_equal={audit_input['audit_campaign'] == campaign_lock}")
print(f"reference_semantics_absent={not Path('/reference/reference-semantics').exists()}")

required_files = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
for path in required_files:
    mode = path.lstat().st_mode
    print(
        f"required_file={path} regular={stat.S_ISREG(mode)} "
        f"symlink={stat.S_ISLNK(mode)} sha256={sha256(path)}"
    )

for directory in (
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
):
    mode = directory.lstat().st_mode
    print(
        f"required_directory={directory} directory={stat.S_ISDIR(mode)} "
        f"symlink={stat.S_ISLNK(mode)}"
    )

comparisons = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
}
for key, path in comparisons.items():
    actual = sha256(path)
    print(f"recorded_hash={key} match={actual == hashes[key]} actual={actual}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
for path in trace_files:
    if path.is_file():
        relative = path.relative_to("/generation-evidence").as_posix()
        expected = result["outputs"]["evidence"].get(relative)
        print(
            f"trace_file={relative} regular={not path.is_symlink()} "
            f"manifest_match={expected == sha256(path)} sha256={sha256(path)}"
        )

candidate_digest = pipeline_contract.sha256_tree(Path("/candidate"))
trace_digest = pipeline_contract.sha256_tree(Path("/generation-evidence/codex-trace"))
print(f"pipeline_candidate_tree_sha256={candidate_digest}")
print(
    "candidate_matches_stage1_workspace="
    f"{candidate_digest == result['outputs']['workspace_sha256'] == invocation['outputs']['workspace_sha256']}"
)
print(f"pipeline_trace_tree_sha256={trace_digest}")
print(
    "trace_matches_usage_source="
    f"{trace_digest == json.loads(Path('/generation-evidence/usage.json').read_text())['source_trace_sha256']}"
)

print(f"candidate_prompt_byte_equal={Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}")
print(f"candidate_translator_byte_equal={Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}")

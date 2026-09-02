#!/usr/bin/env python3
"""Independent Stage-1 checks over launcher-owned mounted inputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import sys

sys.path.insert(0, "/opt/humaneval")
from tools.pipeline_contract import sha256_tree  # noqa: E402


AUDIT_INPUT = Path("/audit-input.json")
document = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


required_files = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    required_files.append(usage)

required_dirs = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference"),
]

print(f"record_layout={document['record_layout']}")
print(f"semantics_mode={document['semantics_mode']}")
print(f"campaign_object_equal={document['audit_campaign'] == lock}")
for path in required_files:
    mode = path.lstat().st_mode
    print(
        f"required_file path={path} regular={stat.S_ISREG(mode)} "
        f"symlink={stat.S_ISLNK(mode)} sha256={digest(path)}"
    )
for path in required_dirs:
    mode = path.lstat().st_mode
    print(
        f"required_dir path={path} directory={stat.S_ISDIR(mode)} "
        f"symlink={stat.S_ISLNK(mode)}"
    )

recorded = document["hashes"]
checks = {
    "audit_campaign_lock_sha256": digest(Path("/audit-campaign-lock.json")),
    "run_manifest_sha256": digest(Path("/run.json")),
    "task_manifest_sha256": digest(Path("/task.json")),
    "stage1_result_sha256": digest(Path("/generation-result.json")),
    "stage1_invocation_sha256": digest(Path("/generation-evidence/invocation.json")),
    "generation_metrics_sha256": digest(Path("/generation-evidence/metrics.json")),
    "generation_codex_last_sha256": digest(Path("/generation-evidence/codex-last.txt")),
    "generation_codex_output_sha256": digest(Path("/generation-evidence/codex-output.log")),
    "generation_prompt_sha256": digest(Path("/generation-evidence/prompt.txt")),
    "canonical_sha256": digest(Path("/reference/canonical.py")),
    "trusted_prompt_sha256": digest(Path("/reference/prompt.py")),
    "trusted_translator_sha256": digest(Path("/reference/py2mpy.py")),
}
if usage.exists():
    checks["generation_usage_sha256"] = digest(usage)
for key, actual in checks.items():
    print(f"recorded_hash_check key={key} match={recorded[key] == actual} actual={actual}")

stage1 = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
candidate_pipeline_digest = sha256_tree(Path("/candidate"))
trace_pipeline_digest = sha256_tree(Path("/generation-evidence/codex-trace"))
print(f"candidate_pipeline_tree_sha256={candidate_pipeline_digest}")
print(
    "candidate_matches_stage1_workspace="
    f"{candidate_pipeline_digest == stage1['outputs']['workspace_sha256']}"
)
print(
    "candidate_matches_invocation_workspace="
    f"{candidate_pipeline_digest == invocation['retained_workspace_sha256']}"
)
print(f"trace_pipeline_tree_sha256={trace_pipeline_digest}")
if usage.exists():
    usage_doc = json.loads(usage.read_text(encoding="utf-8"))
    print(
        "trace_matches_usage_source="
        f"{trace_pipeline_digest == usage_doc['source_trace_sha256']}"
    )

candidate_prompt = Path("/candidate/prompt.py").read_bytes()
trusted_prompt = Path("/reference/prompt.py").read_bytes()
candidate_translator = Path("/candidate/py2mpy.py").read_bytes()
trusted_translator = Path("/reference/py2mpy.py").read_bytes()
print(f"candidate_prompt_byte_equal={candidate_prompt == trusted_prompt}")
print(f"candidate_translator_byte_equal={candidate_translator == trusted_translator}")
print(f"reference_semantics_present={Path('/reference/reference-semantics').exists()}")

proof_artifacts = [
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
]
for name in proof_artifacts:
    path = Path("/candidate") / name
    mode = path.lstat().st_mode
    print(
        f"proof_artifact name={name} regular={stat.S_ISREG(mode)} "
        f"symlink={stat.S_ISLNK(mode)} sha256={digest(path)}"
    )

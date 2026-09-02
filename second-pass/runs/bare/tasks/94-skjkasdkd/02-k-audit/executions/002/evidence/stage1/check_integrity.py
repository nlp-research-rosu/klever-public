#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


audit_input_path = Path("/audit-input.json")
audit_input = json.loads(audit_input_path.read_text())
lock_path = Path(audit_input["container_paths"]["audit_campaign_lock"])
campaign_lock = json.loads(lock_path.read_text())

print(f"audit_input_sha256={sha256(audit_input_path)}")
print(f"campaign_lock_sha256={sha256(lock_path)}")
print(
    "campaign_lock_recorded_match="
    + str(
        sha256(lock_path)
        == audit_input["hashes"]["audit_campaign_lock_sha256"]
    )
)
print(
    "campaign_block_exact_match="
    + str(campaign_lock == audit_input["audit_campaign"])
)

declared_paths = {
    "canonical_sha256": Path(audit_input["container_paths"]["canonical"]),
    "trusted_prompt_sha256": Path(audit_input["container_paths"]["trusted_prompt"]),
    "trusted_translator_sha256": Path(audit_input["container_paths"]["translator"]),
    "candidate_prompt_sha256": Path(audit_input["container_paths"]["candidate"]) / "prompt.py",
    "candidate_translator_sha256": Path(audit_input["container_paths"]["candidate"]) / "py2mpy.py",
    "run_manifest_sha256": Path(audit_input["container_paths"]["run_manifest"]),
    "task_manifest_sha256": Path(audit_input["container_paths"]["task_manifest"]),
    "stage1_result_sha256": Path(audit_input["container_paths"]["stage1_result"]),
    "stage1_invocation_sha256": Path(audit_input["container_paths"]["generation_manifest"]),
    "generation_metrics_sha256": Path(audit_input["container_paths"]["generation_metrics"]),
    "generation_codex_last_sha256": Path(audit_input["container_paths"]["generation_last"]),
    "generation_codex_output_sha256": Path(audit_input["container_paths"]["generation_output"]),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
}

all_hashes_match = True
for field, path in declared_paths.items():
    observed = sha256(path)
    expected = audit_input["hashes"][field]
    matches = observed == expected
    all_hashes_match &= matches
    print(
        f"{field}: path={path} observed={observed} expected={expected} match={matches}"
    )

candidate = Path(audit_input["container_paths"]["candidate"])
trusted_prompt = Path(audit_input["container_paths"]["trusted_prompt"])
trusted_translator = Path(audit_input["container_paths"]["translator"])
print(
    "candidate_prompt_byte_identical="
    + str((candidate / "prompt.py").read_bytes() == trusted_prompt.read_bytes())
)
print(
    "candidate_translator_byte_identical="
    + str((candidate / "py2mpy.py").read_bytes() == trusted_translator.read_bytes())
)
print(
    "trusted_reference_semantics_absent="
    + str(not Path("/reference/reference-semantics").exists())
)
print(
    "candidate_reference_semantics_absent="
    + str(not (candidate / "reference-semantics").exists())
)

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
]
if Path("/generation-evidence/usage.json").exists():
    required.append(Path("/generation-evidence/usage.json"))

required_ok = True
for path in required:
    present = path.exists()
    readable = os.access(path, os.R_OK)
    symlink = path.is_symlink()
    mode = stat.filemode(path.lstat().st_mode) if present else "MISSING"
    ok = present and readable and not symlink
    required_ok &= ok
    print(
        f"required path={path} present={present} readable={readable} "
        f"symlink={symlink} mode={mode} ok={ok}"
    )

print(f"all_declared_file_hashes_match={all_hashes_match}")
print(f"all_required_records_ok={required_ok}")

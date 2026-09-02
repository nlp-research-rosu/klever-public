#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_real_file(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_real_dir(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["mount_reference_semantics"] is False

required_files = [
    AUDIT_INPUT,
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
for path in required_files:
    require_real_file(path)

for path in (
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference"),
):
    require_real_dir(path)

assert not Path("/reference/reference-semantics").exists()

campaign_path = Path("/audit-campaign-lock.json")
campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
assert campaign == audit["audit_campaign"]
assert sha256(campaign_path) == audit["hashes"]["audit_campaign_lock_sha256"]

hash_checks = {
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
}
if Path("/generation-evidence/usage.json").exists():
    require_real_file(Path("/generation-evidence/usage.json"))
    hash_checks["/generation-evidence/usage.json"] = "generation_usage_sha256"

for raw_path, hash_key in hash_checks.items():
    observed = sha256(Path(raw_path))
    expected = audit["hashes"][hash_key]
    assert observed == expected, (raw_path, observed, expected)
    print(f"HASH_OK {hash_key} {observed} {raw_path}")

for key, raw_path in audit["container_paths"].items():
    path = Path(raw_path)
    if key in {"candidate", "generation_root", "generation_trace"}:
        require_real_dir(path)
    else:
        require_real_file(path)
    print(f"CONTAINER_PATH_OK {key} {path}")

for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), (
            f"linked or unsupported entry: {path}"
        )

result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
for relative, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_real_file(path)
    observed = sha256(path)
    assert observed == expected, (relative, observed, expected)
    print(f"RESULT_EVIDENCE_HASH_OK {observed} {relative}")

trace_paths = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert trace_paths, "empty structured trace"
trace_types: Counter[str] = Counter()
trace_payload_types: Counter[str] = Counter()
trace_lines = 0
for path in trace_paths:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            trace_lines += 1
            event_type = str(event.get("type"))
            payload_type = str((event.get("payload") or {}).get("type"))
            trace_types[event_type] += 1
            trace_payload_types[f"{event_type}/{payload_type}"] += 1
    print(f"TRACE_JSON_OK {path} lines={line_number} sha256={sha256(path)}")

print(f"TRACE_TOTAL_LINES {trace_lines}")
print(f"TRACE_TYPES {dict(sorted(trace_types.items()))}")
print(f"TRACE_PAYLOAD_TYPES {dict(sorted(trace_payload_types.items()))}")

candidate_files = []
for path in sorted(Path("/candidate").rglob("*")):
    if path.is_file() and not path.is_symlink():
        relative = path.relative_to("/candidate").as_posix()
        digest = sha256(path)
        candidate_files.append((relative, digest, path.stat().st_size))
        print(f"CANDIDATE_FILE {digest} {path.stat().st_size} {relative}")
print(f"CANDIDATE_REAL_FILE_COUNT {len(candidate_files)}")
print("PROVENANCE_CHECK_OK")

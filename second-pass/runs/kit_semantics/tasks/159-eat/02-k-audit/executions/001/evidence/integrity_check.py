#!/usr/bin/env python3
"""Independent, read-only integrity checks for the 159-eat audit mounts."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                result[relative] = ("symlink", os.readlink(path))
            elif path.is_dir():
                result[relative] = ("directory", None)
            elif path.is_file():
                result[relative] = ("file", digest(path))
            else:
                result[relative] = ("other", None)
    return result


def tree_manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(
        entries, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"problem_id={audit['problem_id']}")
print(f"audit_lock_sha256={digest(LOCK)}")
print(f"audit_lock_recorded={audit['hashes']['audit_campaign_lock_sha256']}")
print(f"audit_campaign_equals_lock={audit['audit_campaign'] == lock}")

required_pipeline_v3 = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "runtime-metrics.json",
    GENERATION / "usage.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
]
for path in required_pipeline_v3:
    print(
        "required_record"
        f" path={path} present={path.exists()}"
        f" regular_nonsymlink={regular_nonsymlink(path)}"
        f" sha256={digest(path) if regular_nonsymlink(path) else '-'}"
    )

declared_file_hashes = {
    LOCK: "audit_campaign_lock_sha256",
    REFERENCE / "canonical.py": "canonical_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "runtime-metrics.json": "generation_runtime_metrics_sha256",
    GENERATION / "usage.json": "generation_usage_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
}
for path, key in declared_file_hashes.items():
    actual = digest(path)
    expected = audit["hashes"][key]
    print(
        f"declared_hash key={key} path={path}"
        f" match={actual == expected} actual={actual} expected={expected}"
    )

print(
    "prompt_byte_identity="
    f"{(CANDIDATE / 'prompt.py').read_bytes() == (REFERENCE / 'prompt.py').read_bytes()}"
)
print(
    "translator_byte_identity="
    f"{(CANDIDATE / 'py2mpy.py').read_bytes() == (REFERENCE / 'py2mpy.py').read_bytes()}"
)

trusted_semantics = tree(REFERENCE / "reference-semantics")
candidate_semantics = tree(CANDIDATE / "reference-semantics")
print(f"trusted_semantics_entries={len(trusted_semantics)}")
print(f"candidate_semantics_entries={len(candidate_semantics)}")
print(f"semantics_tree_exact={trusted_semantics == candidate_semantics}")
print(
    "trusted_semantics_nonregular="
    f"{[key for key, value in trusted_semantics.items() if value[0] not in ('directory', 'file')]}"
)
print(
    "candidate_semantics_nonregular="
    f"{[key for key, value in candidate_semantics.items() if value[0] not in ('directory', 'file')]}"
)

candidate_full_tree = tree(CANDIDATE)
print(f"candidate_full_tree_entries={len(candidate_full_tree)}")
print(
    "candidate_full_tree_manifest_sha256_reviewer_scheme="
    f"{tree_manifest_digest(candidate_full_tree)}"
)
print(
    "candidate_full_tree_nonregular="
    f"{[key for key, value in candidate_full_tree.items() if value[0] not in ('directory', 'file')]}"
)
print(
    "trusted_semantics_manifest_sha256_reviewer_scheme="
    f"{tree_manifest_digest(trusted_semantics)}"
)

candidate_required = [
    CANDIDATE / name
    for name in (
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    )
]
for path in candidate_required:
    print(
        "candidate_required"
        f" path={path} present={path.exists()}"
        f" regular_nonsymlink={regular_nonsymlink(path)}"
        f" sha256={digest(path) if regular_nonsymlink(path) else '-'}"
    )

trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
print(f"trace_file_count={len(trace_files)}")
for path in trace_files:
    print(
        f"trace_file path={path} regular_nonsymlink={regular_nonsymlink(path)}"
        f" sha256={digest(path)}"
    )
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    function_names: Counter[str] = Counter()
    parse_errors = 0
    records = 0
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                parse_errors += 1
                continue
            records += 1
            top_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if payload.get("type") == "function_call":
                    function_names[str(payload.get("name"))] += 1
    print(
        f"trace_summary records={records} parse_errors={parse_errors}"
        f" top_types={dict(top_types)} payload_types={dict(payload_types)}"
        f" function_calls={dict(function_names)}"
    )

print("integrity_check_complete=true")

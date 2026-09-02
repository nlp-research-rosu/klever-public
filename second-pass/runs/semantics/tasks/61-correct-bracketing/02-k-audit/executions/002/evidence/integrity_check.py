#!/usr/bin/env python3
"""Independent, read-only integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check(condition: bool, description: str) -> None:
    print(f"{'OK' if condition else 'FAIL'}: {description}")
    if not condition:
        raise SystemExit(1)


def regular_file(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def tree_records(root: Path) -> list[tuple[str, str, str]]:
    records: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            records.append((rel, "symlink", os.readlink(path)))
        elif path.is_dir():
            records.append((rel, "directory", ""))
        elif path.is_file():
            records.append((rel, "file", sha256(path)))
        else:
            records.append((rel, "other", ""))
    return records


def manifest_digest(records: list[tuple[str, str, str]]) -> str:
    payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
hashes = audit["hashes"]

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
check(audit["record_layout"] == "legacy-selected-stage1", "declared record layout")
check(audit["semantics_mode"] == "SUPPLIED_SEMANTICS", "rendered semantics mode")
check(audit["audit_campaign"] == lock, "campaign lock exactly equals audit campaign block")
check(sha256(LOCK) == hashes["audit_campaign_lock_sha256"], "campaign lock SHA-256")

required_container_paths = {
    "audit_campaign_lock",
    "candidate",
    "canonical",
    "generation_last",
    "generation_manifest",
    "generation_metrics",
    "generation_output",
    "generation_root",
    "generation_trace",
    "run_manifest",
    "stage1_result",
    "task_manifest",
    "translator",
    "trusted_prompt",
}
check(
    required_container_paths <= set(audit["container_paths"]),
    "all launcher-declared container path keys are present",
)
for key in sorted(required_container_paths):
    path = Path(audit["container_paths"][key])
    check(path.exists(), f"mounted path exists: {key}={path}")

required_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
]
for path in required_records:
    check(regular_file(path), f"required legacy-selected-stage1 record is a regular file: {path}")
check(regular_file(GENERATION / "usage.json"), "optional usage.json is present and regular")
trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
check(bool(trace_files), "structured trace tree is nonempty")
check(
    all(path.is_dir() or regular_file(path) for path in trace_files),
    "structured trace contains only directories and regular files",
)

direct_hashes = {
    LOCK: "audit_campaign_lock_sha256",
    REFERENCE / "canonical.py": "canonical_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "usage.json": "generation_usage_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
}
for path, key in direct_hashes.items():
    check(regular_file(path), f"hashed input is a regular file: {path}")
    actual = sha256(path)
    print(f"SHA256 {actual}  {path}")
    check(actual == hashes[key], f"{path} matches audit-input hash field {key}")

check(
    (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes(),
    "candidate prompt is byte-identical to trusted prompt",
)
check(
    (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes(),
    "candidate translator is byte-identical to trusted translator",
)

trusted_semantics = REFERENCE / "reference-semantics"
candidate_semantics = CANDIDATE / "reference-semantics"
check(trusted_semantics.is_dir(), "trusted supplied semantics mount is present")
trusted_records = tree_records(trusted_semantics)
candidate_records = tree_records(candidate_semantics)
check(
    not any(kind == "symlink" for _, kind, _ in trusted_records + candidate_records),
    "neither supplied-semantics tree contains symlinks",
)
check(candidate_records == trusted_records, "candidate supplied semantics exactly matches trusted tree")
print(f"trusted_semantics_manifest_sha256={manifest_digest(trusted_records)}")
for rel, kind, value in trusted_records:
    print(f"SEMANTICS {kind} {rel} {value}")

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = GENERATION / rel
    check(regular_file(path), f"generation-result evidence exists as regular file: {rel}")
    check(sha256(path) == expected, f"generation-result evidence hash: {rel}")

trace_jsonl = sorted((GENERATION / "codex-trace").rglob("*.jsonl"))
check(len(trace_jsonl) == 1, "exactly one structured JSONL trace is mounted")
event_count = 0
for path in trace_jsonl:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            json.loads(line)
            event_count += 1
    print(f"TRACE {sha256(path)} lines={line_number} path={path}")
print(f"structured_trace_events={event_count}")

for path in [GENERATION / "codex-last.txt", GENERATION / "codex-output.log"]:
    data = path.read_bytes()
    data.decode("utf-8")
    print(f"READ {path} bytes={len(data)} lines={data.count(bytes([10]))}")

proof_artifacts = ["solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"]
for name in proof_artifacts:
    check(regular_file(CANDIDATE / name), f"required candidate proof artifact is regular: {name}")

candidate_records_all = tree_records(CANDIDATE)
check(
    not any(kind == "symlink" for _, kind, _ in candidate_records_all),
    "candidate tree contains no symlinks",
)
print(f"candidate_independent_manifest_sha256={manifest_digest(candidate_records_all)}")
for rel, kind, value in candidate_records_all:
    print(f"CANDIDATE {kind} {rel} {value}")

print("SUMMARY: all independently checked stage-1 integrity conditions passed")

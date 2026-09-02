#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Independent implementation of the pipeline's length-delimited tree hash."""
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"unsupported or linked entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def regular(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def real_directory(path: Path) -> bool:
    try:
        return stat.S_ISDIR(path.lstat().st_mode)
    except OSError:
        return False


def check(label: str, condition: bool, details: str = "") -> None:
    global failures
    status = "PASS" if condition else "FAIL"
    print(f"{status} {label}{': ' + details if details else ''}")
    failures += not condition


failures = 0
document = json.loads(AUDIT_INPUT.read_text())
hashes = document["hashes"]
paths = document["container_paths"]

print("COMMAND: python3 /audit-output/evidence/stage1_integrity.py")
check("record layout", document["record_layout"] == "legacy-selected-stage1",
      document["record_layout"])
check("semantics mode", document["semantics_mode"] == "GENERATED_SEMANTICS",
      document["semantics_mode"])

lock_path = Path(paths["audit_campaign_lock"])
lock = json.loads(lock_path.read_text())
check("campaign lock is a regular file", regular(lock_path))
check("campaign lock equals audit_campaign block", lock == document["audit_campaign"])
actual_lock_hash = sha256_file(lock_path)
check("campaign lock hash", actual_lock_hash == hashes["audit_campaign_lock_sha256"],
      actual_lock_hash)

required_regular = {
    "run manifest": Path(paths["run_manifest"]),
    "task manifest": Path(paths["task_manifest"]),
    "stage-1 result": Path(paths["stage1_result"]),
    "generation invocation": Path(paths["generation_manifest"]),
    "generation metrics": Path(paths["generation_metrics"]),
    "generation usage": Path("/generation-evidence/usage.json"),
    "generation last": Path(paths["generation_last"]),
    "generation output": Path(paths["generation_output"]),
    "generation prompt": Path("/generation-evidence/prompt.txt"),
    "canonical": Path(paths["canonical"]),
    "trusted prompt": Path(paths["trusted_prompt"]),
    "trusted translator": Path(paths["translator"]),
}
for label, path in required_regular.items():
    check(f"{label} is a regular file", regular(path), str(path))
check("candidate mount is a real directory", real_directory(Path(paths["candidate"])))
check("trace mount is a real directory", real_directory(Path(paths["generation_trace"])))

for root in (Path(paths["candidate"]), Path(paths["generation_root"])):
    linked = [str(p) for p in root.rglob("*") if p.is_symlink()]
    check(f"no symlinks below {root}", not linked, repr(linked))

expected_file_hashes = {
    Path(paths["run_manifest"]): hashes["run_manifest_sha256"],
    Path(paths["task_manifest"]): hashes["task_manifest_sha256"],
    Path(paths["stage1_result"]): hashes["stage1_result_sha256"],
    Path(paths["generation_manifest"]): hashes["stage1_invocation_sha256"],
    Path(paths["generation_metrics"]): hashes["generation_metrics_sha256"],
    Path("/generation-evidence/usage.json"): hashes["generation_usage_sha256"],
    Path(paths["generation_last"]): hashes["generation_codex_last_sha256"],
    Path(paths["generation_output"]): hashes["generation_codex_output_sha256"],
    Path("/generation-evidence/prompt.txt"): hashes["generation_prompt_sha256"],
    Path(paths["canonical"]): hashes["canonical_sha256"],
    Path(paths["trusted_prompt"]): hashes["trusted_prompt_sha256"],
    Path(paths["translator"]): hashes["trusted_translator_sha256"],
    Path("/candidate/prompt.py"): hashes["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): hashes["candidate_translator_sha256"],
}
for path, expected in expected_file_hashes.items():
    actual = sha256_file(path)
    check(f"recorded SHA-256 for {path}", actual == expected, actual)

check("candidate prompt byte-identical to trusted prompt",
      Path("/candidate/prompt.py").read_bytes() == Path(paths["trusted_prompt"]).read_bytes())
check("candidate translator byte-identical to trusted translator",
      Path("/candidate/py2mpy.py").read_bytes() == Path(paths["translator"]).read_bytes())
check("trusted reference semantics absent",
      not Path("/reference/reference-semantics").exists()
      and not Path("/reference/reference-semantics").is_symlink())
check("candidate reference-semantics absent",
      not Path("/candidate/reference-semantics").exists()
      and not Path("/candidate/reference-semantics").is_symlink())

proof_artifacts = [
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/semantic.k"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/prove.sh"),
]
for path in proof_artifacts:
    check(f"required candidate proof artifact is regular: {path.name}", regular(path))
    if regular(path):
        print(f"SHA256 {sha256_file(path)} {path}")

result = json.loads(Path(paths["stage1_result"]).read_text())
invocation = json.loads(Path(paths["generation_manifest"]).read_text())
for relative, expected in result["outputs"]["evidence"].items():
    path = Path(paths["generation_root"]) / relative
    actual = sha256_file(path)
    check(f"stage-1 result evidence hash {relative}", actual == expected, actual)
    check(f"invocation evidence hash {relative}",
          actual == invocation["outputs"]["evidence"][relative], actual)

candidate_pipeline_hash = pipeline_tree_hash(Path(paths["candidate"]))
trace_pipeline_hash = pipeline_tree_hash(Path(paths["generation_trace"]))
check("candidate tree matches generation retained-workspace hash",
      candidate_pipeline_hash == result["outputs"]["workspace_sha256"],
      candidate_pipeline_hash)
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
check("trace tree matches usage source_trace_sha256",
      trace_pipeline_hash == usage["source_trace_sha256"], trace_pipeline_hash)
print("LAUNCHER_RECORDED candidate_tree_sha256", hashes["candidate_tree_sha256"])
print("LAUNCHER_RECORDED generation_trace_sha256", hashes["generation_codex_trace_sha256"])

json_records = [
    AUDIT_INPUT,
    lock_path,
    Path(paths["run_manifest"]),
    Path(paths["task_manifest"]),
    Path(paths["stage1_result"]),
    Path(paths["generation_manifest"]),
    Path(paths["generation_metrics"]),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/legacy-run-input.json"),
    Path("/generation-evidence/legacy-metrics.json"),
]
for path in json_records:
    try:
        value = json.loads(path.read_text())
        check(f"valid JSON object: {path}", isinstance(value, dict))
    except Exception as error:
        check(f"valid JSON object: {path}", False, repr(error))

trace_files = sorted(Path(paths["generation_trace"]).rglob("*.jsonl"))
check("exactly one structured trace JSONL file", len(trace_files) == 1,
      repr([str(p) for p in trace_files]))
top_types: Counter[str | None] = Counter()
payload_types: Counter[str | None] = Counter()
trace_lines = 0
for path in trace_files:
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                event = json.loads(line)
            except Exception as error:
                check(f"valid trace JSON {path}:{line_number}", False, repr(error))
                continue
            top_types[event.get("type")] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[payload.get("type")] += 1
check("structured trace has events", trace_lines > 0, str(trace_lines))
print("TRACE_TOP_TYPES", dict(top_types))
print("TRACE_PAYLOAD_TYPES", dict(payload_types))
check("trace contains user message", payload_types["user_message"] >= 1)
check("trace contains completed task", payload_types["task_complete"] == 1)

print(f"SUMMARY failures={failures}")
print(f"EXIT_STATUS {1 if failures else 0}")
sys.exit(1 if failures else 0)

#!/usr/bin/env python3
"""Independent mounted-input and legacy-selected-stage1 provenance checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN = Path("/generation-evidence")
TRACE = GEN / "codex-trace"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def entry_type(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


def compare_tree(left: Path, right: Path) -> list[str]:
    problems: list[str] = []
    left_entries = {p.relative_to(left): p for p in left.rglob("*")}
    right_entries = {p.relative_to(right): p for p in right.rglob("*")}
    for rel in sorted(set(left_entries) | set(right_entries), key=str):
        lp = left_entries.get(rel)
        rp = right_entries.get(rel)
        if lp is None:
            problems.append(f"missing from candidate: {rel}")
            continue
        if rp is None:
            problems.append(f"additional candidate entry: {rel}")
            continue
        lt, rt = entry_type(lp), entry_type(rp)
        if lt != rt:
            problems.append(f"type mismatch {rel}: candidate={lt}, trusted={rt}")
            continue
        if lt == "symlink":
            problems.append(f"symlink forbidden in supplied-semantics tree: {rel}")
        elif lt == "file" and sha256(lp) != sha256(rp):
            problems.append(f"content mismatch: {rel}")
    return problems


data = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
print(f"record_layout={data.get('record_layout')}")
print(f"semantics_mode={data.get('semantics_mode')}")
print(f"campaign_block_exact_match={lock == data.get('audit_campaign')}")

hashes = data["hashes"]
checks = {
    "audit_campaign_lock_sha256": LOCK,
    "canonical_sha256": Path("/reference/canonical.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "generation_codex_last_sha256": GEN / "codex-last.txt",
    "generation_codex_output_sha256": GEN / "codex-output.log",
    "generation_metrics_sha256": GEN / "metrics.json",
    "generation_prompt_sha256": GEN / "prompt.txt",
    "generation_usage_sha256": GEN / "usage.json",
    "run_manifest_sha256": Path("/run.json"),
    "stage1_invocation_sha256": GEN / "invocation.json",
    "stage1_result_sha256": Path("/generation-result.json"),
    "task_manifest_sha256": Path("/task.json"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
}
all_ok = True
for key, path in checks.items():
    actual = sha256(path)
    expected = hashes[key]
    ok = actual == expected
    all_ok &= ok
    print(f"HASH {key}: {'OK' if ok else 'MISMATCH'} expected={expected} actual={actual}")

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GEN / "invocation.json",
    GEN / "metrics.json",
    GEN / "codex-last.txt",
    GEN / "codex-output.log",
    GEN / "prompt.txt",
    GEN / "usage.json",
]
required.extend(sorted(TRACE.rglob("*")))
for path in required:
    kind = entry_type(path)
    readable = os.access(path, os.R_OK)
    ok = kind in {"file", "dir"} and readable
    all_ok &= ok
    print(f"REQUIRED {path}: type={kind} readable={readable} ok={ok}")

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = GEN / rel
    actual = sha256(path)
    ok = actual == expected
    all_ok &= ok
    print(f"RESULT_OUTPUT {rel}: {'OK' if ok else 'MISMATCH'} expected={expected} actual={actual}")

trace_files = sorted(TRACE.rglob("*.jsonl"))
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
trace_lines = 0
trace_errors: list[str] = []
for trace_file in trace_files:
    with trace_file.open() as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                event = json.loads(line)
            except json.JSONDecodeError as err:
                trace_errors.append(f"{trace_file}:{line_number}: {err}")
                continue
            top_types[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
print(f"TRACE files={len(trace_files)} lines={trace_lines} json_errors={len(trace_errors)}")
print(f"TRACE top_types={dict(top_types)}")
print(f"TRACE payload_types={dict(payload_types)}")
for problem in trace_errors:
    print(f"TRACE_ERROR {problem}")
all_ok &= not trace_errors

candidate_prompt_match = Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
candidate_translator_match = Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print(f"candidate_prompt_byte_match={candidate_prompt_match}")
print(f"candidate_translator_byte_match={candidate_translator_match}")
all_ok &= candidate_prompt_match and candidate_translator_match

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = Path("/candidate/reference-semantics")
print(f"trusted_semantics_present={trusted_semantics.is_dir()}")
tree_problems = compare_tree(candidate_semantics, trusted_semantics)
print(f"supplied_semantics_tree_exact={not tree_problems}")
for problem in tree_problems:
    print(f"SEMANTICS_TREE_ERROR {problem}")
all_ok &= trusted_semantics.is_dir() and not tree_problems

candidate_symlinks = [str(path) for path in Path("/candidate").rglob("*") if path.is_symlink()]
print(f"candidate_symlinks={candidate_symlinks}")
all_ok &= not candidate_symlinks

proof_artifacts = ["solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"]
for name in proof_artifacts:
    path = Path("/candidate") / name
    ok = path.is_file() and not path.is_symlink() and os.access(path, os.R_OK)
    all_ok &= ok
    print(f"PROOF_ARTIFACT {name}: ok={ok}")

print(f"OVERALL_PROVENANCE_OK={all_ok}")
raise SystemExit(0 if all_ok else 1)

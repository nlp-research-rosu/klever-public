#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for the audit."""

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
TRACE = GEN / "codex-trace/2026/07/23/rollout-2026-07-23T06-21-08-019f8eb5-362d-7ac3-b26b-bb7e5f57964a.jsonl"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def regular_file(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISREG(mode) and not stat.S_ISLNK(mode)


def tree_digest(root: Path) -> str:
    """Reimplement the recorded length-delimited tree hash independently."""
    h = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
        h.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            h.update(size.to_bytes(8, "big"))
            h.update(path.read_bytes())
    return h.hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    problems: list[str] = []
    left_entries = {str(p.relative_to(left)): p for p in left.rglob("*")}
    right_entries = {str(p.relative_to(right)): p for p in right.rglob("*")}
    for rel in sorted(set(left_entries) | set(right_entries)):
        a = left_entries.get(rel)
        b = right_entries.get(rel)
        if a is None:
            problems.append(f"missing-left {rel}")
            continue
        if b is None:
            problems.append(f"additional-left {rel}")
            continue
        am = a.lstat().st_mode
        bm = b.lstat().st_mode
        ak = "symlink" if stat.S_ISLNK(am) else "dir" if stat.S_ISDIR(am) else "file" if stat.S_ISREG(am) else "other"
        bk = "symlink" if stat.S_ISLNK(bm) else "dir" if stat.S_ISDIR(bm) else "file" if stat.S_ISREG(bm) else "other"
        if ak != bk:
            problems.append(f"type {rel}: {ak} != {bk}")
        elif ak == "symlink":
            problems.append(f"symlink {rel}")
        elif ak == "file" and digest(a) != digest(b):
            problems.append(f"content {rel}")
    return problems


data = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
expected = data["hashes"]

required = [
    AUDIT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GEN / "invocation.json",
    GEN / "metrics.json",
    GEN / "codex-last.txt",
    GEN / "codex-output.log",
    GEN / "prompt.txt",
    GEN / "usage.json",
    TRACE,
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]

print("REQUIRED REGULAR NON-SYMLINK FILES")
for path in required:
    print(f"{'OK' if regular_file(path) else 'BAD'} {path}")

checks = {
    LOCK: expected["audit_campaign_lock_sha256"],
    Path("/run.json"): expected["run_manifest_sha256"],
    Path("/task.json"): expected["task_manifest_sha256"],
    Path("/generation-result.json"): expected["stage1_result_sha256"],
    GEN / "invocation.json": expected["stage1_invocation_sha256"],
    GEN / "metrics.json": expected["generation_metrics_sha256"],
    GEN / "codex-last.txt": expected["generation_codex_last_sha256"],
    GEN / "codex-output.log": expected["generation_codex_output_sha256"],
    GEN / "prompt.txt": expected["generation_prompt_sha256"],
    GEN / "usage.json": expected["generation_usage_sha256"],
    Path("/candidate/prompt.py"): expected["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): expected["candidate_translator_sha256"],
    Path("/reference/canonical.py"): expected["canonical_sha256"],
    Path("/reference/prompt.py"): expected["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): expected["trusted_translator_sha256"],
}

print("\nRECORDED FILE HASHES")
for path, want in checks.items():
    got = digest(path)
    print(f"{'MATCH' if got == want else 'MISMATCH'} {got} {path} expected={want}")

result = json.loads(Path("/generation-result.json").read_text())
trace_rel = str(TRACE.relative_to(GEN))
trace_expected = result["outputs"]["evidence"][trace_rel]
trace_got = digest(TRACE)
print(f"{'MATCH' if trace_got == trace_expected else 'MISMATCH'} {trace_got} {TRACE} expected={trace_expected}")

print("\nRECORDED MANIFEST-FRAMED TREE HASHES")
usage = json.loads((GEN / "usage.json").read_text())
tree_checks = {
    Path("/candidate"): result["outputs"]["workspace_sha256"],
    Path("/candidate/reference-semantics"): expected["trusted_reference_semantics_manifest_sha256"],
    Path("/reference/reference-semantics"): expected["trusted_reference_semantics_manifest_sha256"],
    GEN / "codex-trace": usage["source_trace_sha256"],
}
for path, want in tree_checks.items():
    got = tree_digest(path)
    print(f"{'MATCH' if got == want else 'MISMATCH'} {got} {path} expected={want}")

print("\nCAMPAIGN LOCK")
print(f"exact_json_match={lock == data['audit_campaign']}")
print(f"lock_file_hash_match={digest(LOCK) == expected['audit_campaign_lock_sha256']}")

print("\nTRUSTED-CANDIDATE BYTE CHECKS")
for candidate, trusted in [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
]:
    same = candidate.read_bytes() == trusted.read_bytes()
    print(f"{'IDENTICAL' if same else 'DIFFERENT'} {candidate} {trusted}")

tree_problems = compare_trees(
    Path("/candidate/reference-semantics"),
    Path("/reference/reference-semantics"),
)
print("\nREFERENCE SEMANTICS RECURSIVE COMPARISON")
print(f"problem_count={len(tree_problems)}")
for problem in tree_problems:
    print(problem)

print("\nREFERENCE SEMANTICS FILE HASHES")
root = Path("/reference/reference-semantics")
for path in sorted(root.rglob("*")):
    if path.is_file() and not path.is_symlink():
        print(f"{digest(path)}  {path.relative_to(root)}")

print("\nSTRUCTURED TRACE FULL-PARSE SUMMARY")
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_calls: list[tuple[str, str]] = []
tool_outputs = 0
assistant_messages: list[str] = []
line_count = 0
with TRACE.open(encoding="utf-8") as stream:
    for line_count, line in enumerate(stream, 1):
        item = json.loads(line)
        top_types[str(item.get("type"))] += 1
        payload = item.get("payload")
        if isinstance(payload, dict):
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if item.get("type") == "response_item" and payload_type == "function_call":
                tool_calls.append((str(payload.get("name")), str(payload.get("arguments"))))
            elif item.get("type") == "response_item" and payload_type == "function_call_output":
                tool_outputs += 1
            elif item.get("type") == "response_item" and payload_type == "message":
                if payload.get("role") == "assistant":
                    texts = []
                    for content in payload.get("content", []):
                        if isinstance(content, dict) and "text" in content:
                            texts.append(str(content["text"]))
                    if texts:
                        assistant_messages.append("\n".join(texts))

print(f"parsed_lines={line_count}")
print(f"top_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"function_calls={len(tool_calls)} function_outputs={tool_outputs}")
for index, (name, arguments) in enumerate(tool_calls, 1):
    flattened = " ".join(arguments.split())
    print(f"call[{index}] name={name} args={flattened[:320]}")
print(f"assistant_message_count={len(assistant_messages)}")
if assistant_messages:
    print("final_assistant_message=" + " ".join(assistant_messages[-1].split()))

print("\nCANDIDATE TREE FILE HASHES")
candidate_root = Path("/candidate")
for path in sorted(candidate_root.rglob("*")):
    mode = path.lstat().st_mode
    rel = path.relative_to(candidate_root)
    if stat.S_ISLNK(mode):
        print(f"SYMLINK {rel} -> {os.readlink(path)}")
    elif stat.S_ISREG(mode):
        print(f"{digest(path)}  {rel}")

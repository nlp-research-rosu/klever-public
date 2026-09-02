#!/usr/bin/env python3
"""Read and summarize all untrusted generation/provenance artifacts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


candidate = Path("/candidate")
reference = Path("/reference")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


required_files = [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
]

print("MODE_BOUNDARY")
hidden_semantics = reference / "reference-semantics"
print(
    f"/reference/reference-semantics exists={hidden_semantics.exists()} "
    f"is_symlink={hidden_semantics.is_symlink()}"
)

print("REQUIRED_ARTIFACTS")
for name in required_files:
    path = candidate / name
    kind = (
        "symlink"
        if path.is_symlink()
        else "file"
        if path.is_file()
        else "directory"
        if path.is_dir()
        else "missing"
    )
    size = path.stat().st_size if path.exists() else "-"
    digest = sha256(path) if path.is_file() and not path.is_symlink() else "-"
    print(f"{name}: kind={kind} size={size} sha256={digest}")

all_symlinks = [
    str(path)
    for path in candidate.rglob("*")
    if path.is_symlink()
]
print(f"candidate_recursive_symlink_count={len(all_symlinks)}")
for path in all_symlinks:
    print(f"SYMLINK {path} -> {os.readlink(path)}")

print("TRUSTED_IDENTITY")
for name in ("prompt.py", "py2mpy.py"):
    left = candidate / name
    right = reference / name
    same = (
        left.is_file()
        and right.is_file()
        and not left.is_symlink()
        and not right.is_symlink()
        and left.read_bytes() == right.read_bytes()
    )
    print(
        f"{name}: byte_identical={same} "
        f"candidate_sha256={sha256(left)} reference_sha256={sha256(right)}"
    )

print("UNTRUSTED_JSON_CLAIMS")
for name in ("run-input.json", "metrics.json"):
    path = candidate / name
    try:
        value = json.loads(path.read_text())
        print(f"{name}: valid_json=true value={json.dumps(value, sort_keys=True)}")
    except Exception as exc:
        print(f"{name}: valid_json=false error={type(exc).__name__}: {exc}")

print("UNTRUSTED_TEXT_CLAIMS")
for name in ("codex-last.txt", "codex-output.log"):
    path = candidate / name
    text = path.read_text(errors="replace")
    lines = text.splitlines()
    print(
        f"{name}: bytes={path.stat().st_size} lines={len(lines)} "
        f"top_mentions={text.count('#Top')} "
        f"kprove_mentions={text.lower().count('kprove')} "
        f"error_mentions={text.lower().count('error')} "
        f"timeout_mentions={text.lower().count('timeout')}"
    )
    if name == "codex-last.txt":
        print("codex-last.txt content begin")
        print(text.rstrip())
        print("codex-last.txt content end")
    else:
        print("codex-output.log final 20 lines begin")
        for line in lines[-20:]:
            print(line)
        print("codex-output.log final 20 lines end")

print("STRUCTURED_TRACE")
trace_files = sorted((candidate / "codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
print(f"trace_file_count={len(trace_files)}")
for path in trace_files:
    line_count = 0
    parse_errors = 0
    outer_types: dict[str, int] = {}
    payload_types: dict[str, int] = {}
    top_mentions = 0
    final_messages: list[str] = []
    with path.open(errors="replace") as stream:
        for line_count, line in enumerate(stream, 1):
            top_mentions += line.count("#Top")
            try:
                record = json.loads(line)
            except Exception:
                parse_errors += 1
                continue
            outer_type = str(record.get("type"))
            outer_types[outer_type] = outer_types.get(outer_type, 0) + 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                payload_types[payload_type] = payload_types.get(payload_type, 0) + 1
                if (
                    payload_type == "message"
                    and payload.get("role") == "assistant"
                    and payload.get("phase") == "final_answer"
                ):
                    final_messages.append(json.dumps(payload, ensure_ascii=False))
    print(
        f"{path}: bytes={path.stat().st_size} lines={line_count} "
        f"parse_errors={parse_errors} top_mentions={top_mentions} "
        f"outer_types={json.dumps(outer_types, sort_keys=True)} "
        f"payload_types={json.dumps(payload_types, sort_keys=True)}"
    )
    for message in final_messages:
        print(f"TRACE_FINAL_MESSAGE {message}")

print("TOP_LEVEL_INVENTORY")
for path in sorted(candidate.iterdir(), key=lambda item: item.name):
    kind = "symlink" if path.is_symlink() else "directory" if path.is_dir() else "file"
    print(f"{path.name}: {kind}")

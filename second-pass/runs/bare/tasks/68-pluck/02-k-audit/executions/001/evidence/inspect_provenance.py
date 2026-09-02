#!/usr/bin/env python3
"""Summarize untrusted generation records without executing their content."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def show_json(path: Path) -> None:
    print(f"\n== {path} ==")
    print(json.dumps(json.loads(path.read_text()), indent=2, sort_keys=True))


def summarize_text(path: Path, needles: tuple[str, ...]) -> None:
    lines = path.read_text(errors="replace").splitlines()
    print(f"\n== {path}: {len(lines)} lines, {path.stat().st_size} bytes ==")
    print("-- first 5 --")
    print("\n".join(lines[:5]))
    print("-- last 12 --")
    print("\n".join(lines[-12:]))
    for needle in needles:
        matches = [(i + 1, line) for i, line in enumerate(lines) if needle in line]
        print(f"-- {needle!r}: {len(matches)} matches; last 8 --")
        for line_no, line in matches[-8:]:
            print(f"{line_no}: {line[:1000]}")


required_files = (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "spec.k",
    "verification.k",
    "prove.sh",
)

print("== required artifact lstat ==")
for name in required_files:
    path = CANDIDATE / name
    if not path.exists() and not path.is_symlink():
        print(f"MISSING {path}")
    else:
        kind = "symlink" if path.is_symlink() else "file" if path.is_file() else "other"
        print(f"{kind} {path} size={path.lstat().st_size}")

print("\n== all candidate symlinks ==")
symlinks = []
for root, dirs, files in os.walk(CANDIDATE, followlinks=False):
    for name in dirs + files:
        path = Path(root, name)
        if path.is_symlink():
            symlinks.append(path)
print("\n".join(map(str, symlinks)) if symlinks else "(none)")

print("\n== trusted boundary ==")
reference_entries = sorted(p.relative_to(REFERENCE).as_posix() for p in REFERENCE.rglob("*"))
print(f"reference entries: {reference_entries}")
print(f"reference-semantics exists: {(REFERENCE / 'reference-semantics').exists()}")
for name in ("prompt.py", "py2mpy.py"):
    left = CANDIDATE / name
    right = REFERENCE / name
    print(
        f"{name}: candidate={digest(left)} trusted={digest(right)} "
        f"byte_equal={left.read_bytes() == right.read_bytes()}"
    )

show_json(CANDIDATE / "run-input.json")
show_json(CANDIDATE / "metrics.json")
summarize_text(CANDIDATE / "codex-last.txt", ("#Top", "KPROVE", "FAIL", "ERROR"))
summarize_text(
    CANDIDATE / "codex-output.log",
    ("kompile ", "krun ", "kprove ", "#Top", "WarnStuckClaimState", "[Error]"),
)

trace_paths = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
print(f"\n== structured traces: {len(trace_paths)} ==")
for trace_path in trace_paths:
    counts: collections.Counter[str] = collections.Counter()
    parsed = 0
    invalid = 0
    top_mentions = []
    finalish = []
    with trace_path.open(errors="replace") as stream:
        for line_no, line in enumerate(stream, 1):
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                invalid += 1
                continue
            parsed += 1
            counts[str(item.get("type", "<missing>"))] += 1
            payload = item.get("payload")
            payload_text = json.dumps(payload, sort_keys=True)
            if "#Top" in payload_text:
                top_mentions.append((line_no, payload_text[:1500]))
            if "final_answer" in payload_text or "KPROVE_PASSED" in payload_text:
                finalish.append((line_no, payload_text[:1500]))
    print(f"{trace_path}: parsed={parsed} invalid={invalid} types={dict(counts)}")
    print(f"#Top-bearing records={len(top_mentions)}")
    for line_no, text in top_mentions[-5:]:
        print(f"  line {line_no}: {text}")
    print(f"final-ish records={len(finalish)}")
    for line_no, text in finalish[-5:]:
        print(f"  line {line_no}: {text}")

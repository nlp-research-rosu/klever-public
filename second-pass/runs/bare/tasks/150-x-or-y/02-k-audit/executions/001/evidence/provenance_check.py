#!/usr/bin/env python3
import hashlib
import json
import os
from collections import Counter
from pathlib import Path

CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


required = [
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

print("GENERATED_SEMANTICS boundary")
ref_semantics = REFERENCE / "reference-semantics"
print(f"reference-semantics exists={ref_semantics.exists()} symlink={ref_semantics.is_symlink()}")

print("\nRequired candidate artifacts")
bad = []
for name in required:
    path = CANDIDATE / name
    kind = "missing"
    if path.is_symlink():
        kind = "symlink"
    elif path.is_file():
        kind = "regular-file"
    elif path.exists():
        kind = "wrong-type"
    print(f"{name}: {kind}" + (f" size={path.stat().st_size} sha256={digest(path)}" if kind == "regular-file" else ""))
    if kind != "regular-file":
        bad.append((name, kind))

print("\nTrusted identity checks")
for name in ("prompt.py", "py2mpy.py"):
    candidate = CANDIDATE / name
    trusted = REFERENCE / name
    same = candidate.read_bytes() == trusted.read_bytes()
    print(
        f"{name}: byte_identical={same} "
        f"candidate_sha256={digest(candidate)} trusted_sha256={digest(trusted)}"
    )
    if not same:
        bad.append((name, "changed"))

print("\nUntrusted metadata claims")
run_input = json.loads((CANDIDATE / "run-input.json").read_text())
metrics = json.loads((CANDIDATE / "metrics.json").read_text())
print("run-input=" + json.dumps(run_input, sort_keys=True))
print("metrics=" + json.dumps(metrics, sort_keys=True))
print("codex-last=" + json.dumps((CANDIDATE / "codex-last.txt").read_text()))
log_text = (CANDIDATE / "codex-output.log").read_text(errors="replace")
print(
    f"codex-output.log lines={len(log_text.splitlines())} "
    f"claims_top={log_text.count('#Top')} claims_result_marker={log_text.count('RESULT: KPROVE_PASSED')}"
)

trace_files = sorted((CANDIDATE / "codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file() or path.is_symlink()]
print(f"structured_trace_file_count={len(trace_files)}")
for path in trace_files:
    rel = path.relative_to(CANDIDATE)
    if path.is_symlink():
        print(f"trace {rel}: symlink")
        bad.append((str(rel), "symlink"))
        continue
    type_counts = Counter()
    payload_counts = Counter()
    malformed = 0
    with path.open() as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            type_counts[record.get("type")] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_counts[payload.get("type")] += 1
    print(
        f"trace {rel}: size={path.stat().st_size} sha256={digest(path)} "
        f"record_types={dict(type_counts)} payload_types={dict(payload_counts)} malformed={malformed}"
    )

top_entries = sorted(path.name for path in CANDIDATE.iterdir())
print("\nCandidate top-level entries (compiled/cache entries are untrusted and excluded from reconstruction)")
print(json.dumps(top_entries))
print(f"\nINTEGRITY_FAILURE_COUNT={len(bad)}")
for item in bad:
    print("INTEGRITY_FAILURE", item)

raise SystemExit(1 if bad or ref_semantics.exists() or ref_semantics.is_symlink() else 0)

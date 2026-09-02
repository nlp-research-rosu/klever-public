#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")

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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


failures = []
print("MODE: GENERATED_SEMANTICS")
reference_semantics = REFERENCE / "reference-semantics"
print(f"REFERENCE_SEMANTICS_EXISTS: {reference_semantics.exists()}")
if reference_semantics.exists() or reference_semantics.is_symlink():
    failures.append("forbidden trusted reference-semantics exists")

for name in required:
    path = CANDIDATE / name
    kind = "missing"
    if path.is_symlink():
        kind = "symlink"
        failures.append(f"{name}: symlink")
    elif path.is_file():
        kind = "regular-file"
    elif path.exists():
        kind = "mistyped-non-file"
        failures.append(f"{name}: mistyped-non-file")
    else:
        failures.append(f"{name}: missing")
    print(f"REQUIRED {name}: {kind}")

trace_files = sorted((CANDIDATE / "codex-trace").glob("**/*.jsonl"))
print(f"STRUCTURED_TRACE_COUNT: {len(trace_files)}")
for path in trace_files:
    print(f"STRUCTURED_TRACE: {path}")

for candidate_name, reference_name in [
    ("prompt.py", "prompt.py"),
    ("py2mpy.py", "py2mpy.py"),
]:
    candidate_path = CANDIDATE / candidate_name
    reference_path = REFERENCE / reference_name
    if candidate_path.is_file() and reference_path.is_file():
        candidate_hash = sha256(candidate_path)
        reference_hash = sha256(reference_path)
        equal = candidate_path.read_bytes() == reference_path.read_bytes()
        print(
            f"TRUSTED_COMPARE {candidate_name}: equal={equal} "
            f"candidate_sha256={candidate_hash} reference_sha256={reference_hash}"
        )
        if not equal:
            failures.append(f"{candidate_name}: changed from trusted input")

run_input = json.loads((CANDIDATE / "run-input.json").read_text())
print(f"RUN_INPUT_PROBLEM_ID: {run_input.get('problem_id')}")
print(f"RUN_INPUT_CONDITION: {run_input.get('condition')}")
recorded_prompt = run_input.get("inputs", {}).get("problem_prompt_sha256")
recorded_translator = run_input.get("inputs", {}).get("translator_sha256")
actual_prompt = sha256(REFERENCE / "prompt.py")
actual_translator = sha256(REFERENCE / "py2mpy.py")
print(f"RECORDED_PROMPT_HASH_MATCH: {recorded_prompt == actual_prompt}")
print(f"RECORDED_TRANSLATOR_HASH_MATCH: {recorded_translator == actual_translator}")

top_level = sorted(CANDIDATE.iterdir(), key=lambda p: p.name)
print("CANDIDATE_TOP_LEVEL:")
for path in top_level:
    if path.is_symlink():
        kind = "symlink"
    elif path.is_dir():
        kind = "directory"
    elif path.is_file():
        kind = "regular-file"
    else:
        kind = "other"
    print(f"  {kind} {path.name}")

print("EXCLUDED_CANDIDATE_BUILD_OUTPUTS: __pycache__/ verification-kompiled/")
print(f"INTEGRITY_FAILURE_COUNT: {len(failures)}")
for failure in failures:
    print(f"INTEGRITY_FAILURE: {failure}")
raise SystemExit(1 if failures else 0)

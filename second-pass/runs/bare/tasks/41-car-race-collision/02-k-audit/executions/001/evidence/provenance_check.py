#!/usr/bin/env python3
"""Read-only integrity checks for the candidate and trusted mounts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")

REQUIRED_REGULAR = [
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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def describe(path: Path) -> str:
    if path.is_symlink():
        return f"SYMLINK -> {path.readlink()}"
    if path.is_file():
        return f"regular sha256={sha256(path)} bytes={path.stat().st_size}"
    if path.is_dir():
        return "directory"
    if path.exists():
        return "other"
    return "MISSING"


def main() -> int:
    failures: list[str] = []
    print("SEMANTICS_MODE=GENERATED_SEMANTICS")
    reference_semantics = REFERENCE / "reference-semantics"
    print(f"{reference_semantics}: {describe(reference_semantics)}")
    if reference_semantics.exists() or reference_semantics.is_symlink():
        failures.append("generated-semantics mode forbids reference-semantics")

    print("\nREQUIRED CANDIDATE ARTIFACTS")
    for relative in REQUIRED_REGULAR:
        path = CANDIDATE / relative
        print(f"{path}: {describe(path)}")
        if path.is_symlink() or not path.is_file():
            failures.append(f"required regular file violation: {relative}")

    traces = sorted((CANDIDATE / "codex-trace").rglob("*"))
    trace_files = [path for path in traces if path.is_file() or path.is_symlink()]
    print("\nSTRUCTURED TRACE FILES")
    if not trace_files:
        print("NONE")
    for path in trace_files:
        print(f"{path}: {describe(path)}")
        if path.is_symlink() or not path.is_file():
            failures.append(f"trace is not a regular file: {path}")
            continue
        with path.open("r", encoding="utf-8") as stream:
            count = 0
            for count, line in enumerate(stream, 1):
                json.loads(line)
        print(f"parsed_jsonl_records={count}")

    print("\nTRUSTED BYTE COMPARISONS")
    for name in ["prompt.py", "py2mpy.py"]:
        candidate_path = CANDIDATE / name
        reference_path = REFERENCE / name
        same = (
            candidate_path.is_file()
            and not candidate_path.is_symlink()
            and reference_path.is_file()
            and candidate_path.read_bytes() == reference_path.read_bytes()
        )
        print(f"{name}: byte_identical={same}")
        if not same:
            failures.append(f"trusted input mismatch: {name}")

    run_input_path = CANDIDATE / "run-input.json"
    metrics_path = CANDIDATE / "metrics.json"
    if run_input_path.is_file() and not run_input_path.is_symlink():
        run_input = json.loads(run_input_path.read_text(encoding="utf-8"))
        print("\nRUN INPUT CLAIMS")
        print(json.dumps(run_input, sort_keys=True))
        prompt_claim = run_input["inputs"]["problem_prompt_sha256"]
        translator_claim = run_input["inputs"]["translator_sha256"]
        print(f"prompt_hash_claim_matches={prompt_claim == sha256(REFERENCE / 'prompt.py')}")
        print(
            "translator_hash_claim_matches="
            f"{translator_claim == sha256(REFERENCE / 'py2mpy.py')}"
        )
        if prompt_claim != sha256(REFERENCE / "prompt.py"):
            failures.append("run-input prompt hash claim is false")
        if translator_claim != sha256(REFERENCE / "py2mpy.py"):
            failures.append("run-input translator hash claim is false")

    if metrics_path.is_file() and not metrics_path.is_symlink():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        print("\nMETRICS CLAIMS")
        print(json.dumps(metrics, sort_keys=True))

    print("\nTOP-LEVEL CANDIDATE INVENTORY")
    for path in sorted(CANDIDATE.iterdir()):
        print(f"{path.name}: {describe(path)}")

    print("\nINTEGRITY_FAILURES")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python programs."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import Callable


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "fresh-semantic-llvm-kompiled"
CASES = [
    ("documented-example", "o o| .| o| o| .| .| .| .| o o"),
    ("empty-boundary", ""),
    ("separator-only", " "),
    ("whole-branch", "o"),
    ("half-branch", "o|"),
    ("quarter-branch", ".|"),
    ("repeated-separator", "o  .|"),
    ("leading-separator", " o"),
    ("trailing-separator", "o "),
]


def load_entry(path: Path, name: str) -> Callable[[str], list[int]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_music


def parse_k_result(output: str) -> list[int]:
    match = re.search(r"<result>\s*(.*?)\s*</result>", output, flags=re.DOTALL)
    if match is None:
        raise ValueError("missing <result> cell")
    return [int(value) for value in re.findall(r"pyInt\s*\(\s*(-?\d+)\s*\)", match.group(1))]


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "audit_canonical")
    candidate = load_entry(WORK / "solution.py", "audit_candidate")
    failures = 0
    for label, value in CASES:
        argv = [
            "krun",
            "solution.mpy",
            "--definition",
            str(DEFINITION),
            f'-cINPUT="{value}"',
        ]
        completed = subprocess.run(
            argv,
            cwd=WORK,
            check=False,
            capture_output=True,
            text=True,
        )
        combined = completed.stdout + completed.stderr
        try:
            k_value = parse_k_result(combined)
            parse_error = None
        except ValueError as exc:
            k_value = None
            parse_error = str(exc)
        candidate_value = candidate(value)
        canonical_value = canonical(value)
        k_terminated = bool(re.search(r"<k>\s*\.K\s*</k>", combined, flags=re.DOTALL))
        candidate_match = completed.returncode == 0 and k_terminated and k_value == candidate_value
        canonical_match = completed.returncode == 0 and k_terminated and k_value == canonical_value
        if not candidate_match:
            failures += 1
        print(
            json.dumps(
                {
                    "label": label,
                    "input": value,
                    "command": shlex.join(argv),
                    "exit_status": completed.returncode,
                    "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
                    "stderr": completed.stderr[-1000:],
                    "k_terminated": k_terminated,
                    "parse_error": parse_error,
                    "k_result": k_value,
                    "candidate_python": candidate_value,
                    "canonical_python": canonical_value,
                    "matches_candidate": candidate_match,
                    "matches_canonical": canonical_match,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    print(f"candidate_semantics_mismatch_count={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

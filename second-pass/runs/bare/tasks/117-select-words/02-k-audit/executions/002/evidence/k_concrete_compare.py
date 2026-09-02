#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with both Python programs."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/117-select-words-audit")
DEFINITION = SCRATCH / "semantic-fresh-kompiled"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.select_words


def parse_words(output: str) -> list[str]:
    match = re.search(r"<result>(.*?)</result>", output, flags=re.DOTALL)
    if match is None:
        raise AssertionError("krun output has no <result> cell")
    result = match.group(1)
    if "pyList" not in result:
        raise AssertionError(f"result is not a pyList: {result!r}")
    return [json.loads(token) for token in re.findall(r'"(?:[^"\\]|\\.)*"', result)]


canonical = load_entry(Path("/reference/canonical.py"), "k_compare_canonical")
candidate = load_entry(Path("/candidate/solution.py"), "k_compare_candidate")

CASES = [
    ("normal-prompt", "Mary had a little lamb", 3),
    ("empty", "", 0),
    ("spaces-only", "    ", 0),
    ("runs-leading-trailing", "  a   bc  ", 0),
    ("vowel-branch", "AEIOU aei", 0),
    ("consonant-branch", "bcdf xyz", 4),
    ("exclude-branch", "bcdf xyz", 2),
    ("uppercase", "HELLO world", 3),
    ("n-too-large", "a bb ccc", 9),
]

failures = 0
for label, source, n in CASES:
    command = [
        "krun",
        str(SCRATCH / "solution.mpy"),
        "--definition",
        str(DEFINITION),
        f"-cS={json.dumps(source)}",
        f"-cN={n}",
    ]
    run = subprocess.run(command, text=True, capture_output=True)
    print("CASE", label)
    print("COMMAND", shlex.join(command))
    print("EXIT", run.returncode)
    print("STDOUT")
    print(run.stdout.rstrip())
    if run.stderr:
        print("STDERR")
        print(run.stderr.rstrip())
    try:
        k_value = parse_words(run.stdout)
    except Exception as error:
        k_value = f"PARSE ERROR: {error}"
    canonical_value = canonical(source, n)
    candidate_value = candidate(source, n)
    print("K-VALUE", repr(k_value))
    print("CANONICAL", repr(canonical_value))
    print("CANDIDATE", repr(candidate_value))
    case_ok = (
        run.returncode == 0
        and "<k>\n    .K\n  </k>" in run.stdout
        and k_value == canonical_value == candidate_value
    )
    print("CASE-RESULT", "PASS" if case_ok else "FAIL")
    print()
    failures += not case_ok

print("TOTAL", len(CASES))
print("FAILURES", failures)
raise SystemExit(1 if failures else 0)

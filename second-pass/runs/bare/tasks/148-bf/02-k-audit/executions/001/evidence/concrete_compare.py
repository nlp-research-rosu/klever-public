#!/usr/bin/env python3
"""Compare freshly rebuilt generated K semantics with both Python functions."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


CASES = (
    ("Jupiter", "Neptune"),
    ("Earth", "Mercury"),
    ("Mercury", "Uranus"),
    ("Mercury", "Mercury"),
    ("Mercury", "Venus"),
    ("Neptune", "Mercury"),
    ("Pluto", "Earth"),
    ("Earth", "Pluto"),
    ("", "Neptune"),
    ("☿", "Neptune"),
)


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.bf


def parse_k_result(output: str) -> tuple[str, ...]:
    match = re.search(
        r"<result>\s*tupleValue\s*\((.*?)\.StringValues\s*\)\s*</result>",
        output,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"could not locate final tupleValue in output:\n{output}")
    quoted_tokens = re.findall(r'"(?:\\.|[^"\\])*"', match.group(1))
    return tuple(json.loads(token) for token in quoted_tokens)


def main() -> None:
    canonical = load_function("trusted_canonical_k_compare", Path("/reference/canonical.py"))
    generated = load_function(
        "candidate_solution_k_compare",
        Path("/tmp/audit-work/rebuild/solution.py"),
    )
    definition = Path("/tmp/audit-work/rebuild/semantic-audit-kompiled")
    for first, second in CASES:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            str(definition),
            "-cPLANET1=" + json.dumps(first, ensure_ascii=True),
            "-cPLANET2=" + json.dumps(second, ensure_ascii=True),
        ]
        print("$ " + shlex.join(command))
        completed = subprocess.run(
            command,
            cwd="/tmp/audit-work/rebuild",
            check=False,
            text=True,
            capture_output=True,
        )
        print(f"exit={completed.returncode}")
        if completed.stderr:
            print(completed.stderr, end="")
        assert completed.returncode == 0
        k_value = parse_k_result(completed.stdout)
        canonical_value = canonical(first, second)
        generated_value = generated(first, second)
        print(
            f"inputs=({first!r}, {second!r}) "
            f"K={k_value!r} canonical={canonical_value!r} "
            f"generated={generated_value!r}"
        )
        assert k_value == canonical_value == generated_value
    print(f"concrete K/Python comparisons={len(CASES)} mismatch_count=0")


if __name__ == "__main__":
    main()

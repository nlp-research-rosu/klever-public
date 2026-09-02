#!/usr/bin/env python3
"""Compare rebuilt K execution with candidate and trusted Python behavior."""

from __future__ import annotations

import importlib.util
import ast
import json
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.split_words


def parse_k_value(output: str):
    integer = re.search(r"\bVInt \( (-?[0-9]+) \)", output)
    if integer:
        return int(integer.group(1))
    if "VList (" in output:
        encoded_strings = re.findall(
            r'\bVStr \( ("(?:[^"\\]|\\.)*") \)', output
        )
        return [ast.literal_eval(encoded) for encoded in encoded_strings]
    raise AssertionError(f"could not parse final K value: {output}")


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/concrete_semantics_compare.py")
    candidate = load_entry(WORK / "solution.py", "candidate_for_k_compare")
    canonical = load_entry(
        Path("/tmp/audit-work/trusted/canonical.py"), "canonical_for_k_compare"
    )
    cases = [
        "Hello world!",
        "Hello,world!",
        "abcdef",
        "",
        " ",
        ",",
        "a,b c",
        "a,,b,",
        "left\tright",
        "left\u2003right",
        "bdfhjlnprtvxz",
        "acegikmoqsuwy",
        "ê",
        "\u00a0a\u3000b",
    ]
    mismatches = 0
    for text in cases:
        command = [
            "krun",
            "solution.mpy",
            "--definition",
            "concrete-kompiled",
            f"-cINPUT={json.dumps(text, ensure_ascii=False)}",
        ]
        completed = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        k_value = parse_k_value(completed.stdout) if completed.returncode == 0 else None
        python_value = candidate(text)
        trusted_value = canonical(text)
        matches_candidate = completed.returncode == 0 and k_value == python_value
        mismatches += int(not matches_candidate)
        escaped = text.encode("unicode_escape").decode("ascii")
        print(
            f"INPUT={escaped!r} K_EXIT={completed.returncode} "
            f"K={k_value!r} CANDIDATE_PY={python_value!r} "
            f"CANONICAL_PY={trusted_value!r} "
            f"K_MATCHES_CANDIDATE={matches_candidate}"
        )
    print(f"K_CANDIDATE_MISMATCHES: {mismatches}")
    raise SystemExit(1 if mismatches else 0)


if __name__ == "__main__":
    main()

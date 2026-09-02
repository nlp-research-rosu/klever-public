#!/usr/bin/env python3
"""Run the freshly built generated semantics and compare it with both Pythons."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import re
import shlex
import subprocess
import sys


ROOT = Path("/tmp/audit-work/118-get-closest-vowel")
SOURCE = ROOT / "candidate-src"
DEFINITION = ROOT / "build" / "concrete-kompiled"


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def python_outcome(function, word: str):
    try:
        return ("return", function(word))
    except BaseException as error:
        return ("raise", type(error).__name__, str(error))


def decode_k_result(output: str):
    match = re.search(r"<k>\s*(.*?)\s*</k>", output, flags=re.DOTALL)
    if not match:
        return ("unparsed", output[:500])
    k_cell = " ".join(match.group(1).split())
    if k_cell == "pyStr ( .Chars ) ~> .K":
        return ("return", "")
    vowel = re.fullmatch(
        r"pyStr \( snoc \( \.Chars , vow \( v_([aeiouAEIOU]) \) \) \) ~> \.K",
        k_cell,
    )
    if vowel:
        return ("return", vowel.group(1))
    return ("residual", k_cell)


def main() -> int:
    canonical = load_entry(ROOT / "reference" / "canonical.py", "canonical_kcheck")
    candidate = load_entry(SOURCE / "solution.py", "candidate_kcheck")
    cases = [
        "",
        "b",
        "bb",
        "bbb",
        "bab",
        "baa",
        "aab",
        "yogurt",
        "FULL",
        "quick",
        "babcc",
        "cbaad",
        "b" * 1000,
    ]
    k_vs_canonical = 0
    k_vs_candidate = 0
    for index, word in enumerate(cases):
        argument = f'word("{word}")'
        command = [
            "krun",
            str(SOURCE / "solution.mpy"),
            f"-cARG={argument}",
            "--definition",
            str(DEFINITION),
            "--output",
            "pretty",
        ]
        print(f"CASE={index} LENGTH={len(word)} SHA256={hashlib.sha256(word.encode()).hexdigest()}")
        print(f"COMMAND={shlex.join(command)}")
        run = subprocess.run(
            command,
            cwd=SOURCE,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
            check=False,
        )
        k_result = decode_k_result(run.stdout)
        canonical_result = ("return", canonical(word))
        candidate_result = python_outcome(candidate, word)
        print(f"KRUN_EXIT_STATUS={run.returncode}")
        print(f"K_RESULT={k_result!r}")
        print(f"CANONICAL_RESULT={canonical_result!r}")
        print(f"CANDIDATE_PYTHON_RESULT={candidate_result!r}")
        if run.returncode != 0 or k_result != canonical_result:
            k_vs_canonical += 1
        if run.returncode != 0 or k_result != candidate_result:
            k_vs_candidate += 1
    print(f"TOTAL_CASES={len(cases)}")
    print(f"K_VS_CANONICAL_MISMATCHES={k_vs_canonical}")
    print(f"K_VS_CANDIDATE_PYTHON_MISMATCHES={k_vs_candidate}")
    return 1 if k_vs_canonical or k_vs_candidate else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with both Python programs."""

from __future__ import annotations

import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path
from types import ModuleType
from typing import Callable


SCRATCH = Path("/tmp/audit-work/98-count-upper-audit-20260726")
DEFINITION = SCRATCH / "fresh-semantic-kompiled"
RESULT_PATTERN = re.compile(r"intVal\s*\(\s*(-?[0-9]+)\s*\)")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def python_outcome(function: Callable[[str], int], value: str) -> tuple[str, object]:
    try:
        return ("return", function(value))
    except BaseException as error:
        return ("raise", type(error).__name__)


def k_outcome(value: str) -> tuple[tuple[str, object], str]:
    input_term = json.dumps(value, ensure_ascii=False)
    command = [
        "krun",
        "solution.mpy",
        f"-cINPUT={input_term}",
        "--definition",
        str(DEFINITION),
    ]
    print(f"KRUN_COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
        check=False,
    )
    output = completed.stdout
    if completed.returncode != 0:
        return ("krun-error", completed.returncode), output
    matches = RESULT_PATTERN.findall(output)
    if len(matches) != 1:
        return ("unparsed", output.strip()), output
    return ("return", int(matches[0])), output


def display(value: str) -> str:
    if len(value) <= 60:
        return repr(value)
    return repr(value[:30]) + f"...(len={len(value)})"


def main() -> int:
    canonical = load_module("trusted_canonical_for_k", SCRATCH / "canonical.py")
    generated = load_module("generated_solution_for_k", SCRATCH / "solution.py")
    cases = [
        ("documented", "aBCdEf"),
        ("documented", "abcdefg"),
        ("documented", "dBBE"),
        ("empty-base", ""),
        ("one-char-vowel", "A"),
        ("one-char-nonvowel", "Z"),
        ("odd-index-ignored", "xA"),
        ("later-even-vowel", "xxA"),
        ("all-uppercase-vowels", "AEIOU"),
        ("unicode-codepoints", "😀A😀E"),
        ("long-over-recursion-limit", "A" * 2001),
    ]

    k_vs_canonical = 0
    k_vs_generated = 0
    for category, value in cases:
        canonical_result = python_outcome(canonical.count_upper, value)
        generated_result = python_outcome(generated.count_upper, value)
        k_result, raw = k_outcome(value)
        if k_result != canonical_result:
            k_vs_canonical += 1
        if k_result != generated_result:
            k_vs_generated += 1
        compact_raw = " ".join(raw.split())
        if len(compact_raw) > 240:
            compact_raw = compact_raw[:240] + "... <truncated>"
        print(
            f"CASE category={category} input={display(value)} "
            f"canonical={canonical_result!r} generated={generated_result!r} "
            f"k={k_result!r} raw={compact_raw!r}"
        )

    print(f"case_count={len(cases)}")
    print(f"k_vs_canonical_mismatch_count={k_vs_canonical}")
    print(f"k_vs_generated_mismatch_count={k_vs_generated}")
    return 1 if k_vs_canonical or k_vs_generated else 0


if __name__ == "__main__":
    raise SystemExit(main())

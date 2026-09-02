#!/usr/bin/env python3
"""Run the clean generated semantics and compare final results to both CPython entries."""

from __future__ import annotations

import ast
import importlib.util
import json
import pathlib
import re
import shlex
import subprocess
from collections.abc import Callable


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[list[str]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "concatenate")


def main() -> int:
    canonical = load_entry(pathlib.Path("/reference/canonical.py"), "krun_canonical")
    generated = load_entry(
        pathlib.Path("/tmp/audit-work/fresh/solution.py"), "krun_generated"
    )
    program = "/tmp/audit-work/fresh/solution.mpy"
    definition = "/tmp/audit-work/fresh/concrete-kompiled"
    cases = [
        ("empty-loop-zero-iterations", [], "lVal(.StrList)"),
        ("singleton-empty", [""], 'lVal("" :: .StrList)'),
        ("singleton-nonempty", ["boundary"], 'lVal("boundary" :: .StrList)'),
        ("documented-abc", ["a", "b", "c"], 'lVal("a" :: "b" :: "c" :: .StrList)'),
        (
            "empty-elements",
            ["", "hello", "", " world"],
            'lVal("" :: "hello" :: "" :: " world" :: .StrList)',
        ),
        (
            "prefix-empty-suffix",
            ["prefix", "", "suffix"],
            'lVal("prefix" :: "" :: "suffix" :: .StrList)',
        ),
        ("unicode", ["β", "🙂"], 'lVal("β" :: "🙂" :: .StrList)'),
    ]
    failures = 0
    for label, python_input, k_argument in cases:
        command = [
            "krun",
            program,
            "--definition",
            definition,
            f"-cARG={k_argument}",
        ]
        run = subprocess.run(command, text=True, capture_output=True, check=False)
        print(f"COMMAND: {shlex.join(command)}")
        print(f"EXIT_STATUS: {run.returncode}")
        print("STDOUT_BEGIN")
        print(run.stdout, end="")
        print("STDOUT_END")
        if run.stderr:
            print("STDERR_BEGIN")
            print(run.stderr, end="")
            print("STDERR_END")

        result_matches = re.findall(
            r"<result>\s*sVal\s*\(\s*(\"(?:\\.|[^\"\\])*\")\s*\)\s*</result>",
            run.stdout,
        )
        k_value = ast.literal_eval(result_matches[-1]) if result_matches else None
        # K's pretty-printer renders UTF-8 bytes as \xHH escapes. JSON decoding
        # gives the byte values as Latin-1 code points, so restore the UTF-8
        # text when that representation is used.
        if k_value is not None and all(ord(character) <= 255 for character in k_value):
            try:
                k_value = k_value.encode("latin-1").decode("utf-8")
            except UnicodeDecodeError:
                pass
        canonical_value = canonical(python_input)
        generated_value = generated(python_input)
        closed_k = re.search(r"<k>\s*\.K\s*</k>", run.stdout) is not None
        matches = (
            run.returncode == 0
            and closed_k
            and k_value == canonical_value
            and k_value == generated_value
        )
        failures += int(not matches)
        print(
            json.dumps(
                {
                    "label": label,
                    "python_input": python_input,
                    "canonical": canonical_value,
                    "generated": generated_value,
                    "k_result": k_value,
                    "closed_k": closed_k,
                    "matches": matches,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
    print(json.dumps({"summary": {"cases": len(cases), "failures": failures}}))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

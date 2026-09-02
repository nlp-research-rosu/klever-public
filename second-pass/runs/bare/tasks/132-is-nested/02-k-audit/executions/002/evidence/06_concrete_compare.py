#!/usr/bin/env python3
"""Execute the fresh generated K semantics and compare with both Python programs."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/132-is-nested")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


canonical = load_function(Path("/reference/canonical.py"), "concrete_canonical_132")
submitted = load_function(ROOT / "solution.py", "concrete_submitted_132")

cases = [
    "",
    "[",
    "]",
    "[[",
    "]]",
    "[]",
    "][",
    "[[]",
    "[[[]",
    "[[]]",
    "[]]]]]]][[[[[]",
    "[][]",
    "[[][]]",
    "[[]][[",
    "[[[[]]]]",
    "]]][[[[]]]][[[",
    "[[]]]",
    "[][[[]]]",
]


def k_input(text: str) -> str:
    tokens = ["lbr" if character == "[" else "rbr" for character in text]
    return " ".join(tokens + [".BString"])


def main() -> None:
    mismatches = 0
    for index, text in enumerate(cases):
        expected_canonical = canonical(text)
        expected_submitted = submitted(text)
        command = [
            "krun",
            "solution.mpy",
            f"-cINPUT={k_input(text)}",
            "--definition",
            "audit-semantic-kompiled",
        ]
        completed = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, check=False
        )
        expected_fragment = f"boolVal ( {'true' if expected_canonical else 'false'} )"
        observed = expected_fragment in completed.stdout
        print(f"CASE {index} input={text!r}")
        print("COMMAND: " + " ".join(repr(part) for part in command))
        print(
            f"canonical={expected_canonical} submitted={expected_submitted} "
            f"krun_exit={completed.returncode} expected_fragment={expected_fragment!r} "
            f"fragment_observed={observed}"
        )
        result_lines = [
            line.strip()
            for line in completed.stdout.splitlines()
            if "boolVal" in line or "<result>" in line
        ]
        print(f"bounded_result_lines={result_lines[:4]!r}")
        if completed.stderr:
            print(f"bounded_stderr={completed.stderr[:1000]!r}")
        if (
            completed.returncode != 0
            or expected_canonical != expected_submitted
            or not observed
        ):
            mismatches += 1
    print(f"concrete_cases={len(cases)} mismatch_count={mismatches}")
    assert mismatches == 0
    print("FRESH_GENERATED_SEMANTICS_CONCRETE_OK")


if __name__ == "__main__":
    main()

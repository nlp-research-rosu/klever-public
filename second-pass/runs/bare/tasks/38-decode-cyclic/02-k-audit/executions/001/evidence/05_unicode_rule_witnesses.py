#!/usr/bin/env python3
"""Focused false-conclusion witnesses for the generated Python string rules."""

from __future__ import annotations

import ast
import importlib.util
import json
import re
import subprocess
from pathlib import Path

ROOT = Path("/tmp/audit-work/38-decode-cyclic-audit")
TEST_ROOT = ROOT / "unicode-witnesses"
TRANSLATOR = ROOT / "trusted/py2mpy.py"
DEFINITION = ROOT / "build-concrete/semantic-llvm-kompiled"

CASES = [
    ("builtinLen semantic.k:106-107", "len_program.py", "中", 1, 3),
    ("indexApply semantic.k:109-114", "index_program.py", "中", "中", None),
    (
        "bounded slice semantic.k:116-122",
        "bounded_slice_program.py",
        "中x",
        "中",
        None,
    ),
    (
        "tail slice semantic.k:124-129",
        "tail_slice_program.py",
        "中x",
        "x",
        None,
    ),
]

INT_RE = re.compile(r"<result>\s*pyInt\s*\(\s*(-?\d+)\s*\)\s*</result>",
                    re.DOTALL)
STR_RE = re.compile(
    r'<result>\s*pyStr\s*\(\s*("(?:\\.|[^"\\])*")\s*\)\s*</result>',
    re.DOTALL,
)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_k_string_bytes(token: str) -> bytes:
    return ast.literal_eval(token).encode("latin-1")


def main() -> int:
    failures = []
    observed = []
    for number, (rule, filename, value, expected_python, expected_k_int) in enumerate(
        CASES, 1
    ):
        py_path = TEST_ROOT / filename
        mpy_path = py_path.with_suffix(".mpy")
        translate = ["python3", str(TRANSLATOR), str(py_path)]
        print("$ " + " ".join(json.dumps(piece) for piece in translate)
              + " > " + str(mpy_path))
        with mpy_path.open("w", encoding="utf-8") as output:
            translated = subprocess.run(
                translate, text=True, stdout=output, stderr=subprocess.PIPE,
                check=False
            )
        print(translated.stderr.rstrip())
        print(f"[exit {translated.returncode}]")
        if translated.returncode != 0:
            failures.append({"rule": rule, "failure": "translation failed"})
            continue

        module = load(py_path, f"unicode_witness_{number}")
        python_value = module.decode_cyclic(value)
        command = [
            "krun",
            str(mpy_path),
            "-cS=" + json.dumps(value, ensure_ascii=False),
            "--definition",
            str(DEFINITION),
        ]
        print("$ " + " ".join(json.dumps(piece) for piece in command))
        proc = subprocess.run(command, text=True, capture_output=True, check=False)
        output = proc.stdout + proc.stderr
        print(output.rstrip())
        print(f"[exit {proc.returncode}]")

        if expected_k_int is not None:
            match = INT_RE.search(output)
            k_observed = int(match.group(1)) if match else None
            witness_holds = (
                proc.returncode == 0
                and python_value == expected_python
                and k_observed == expected_k_int
                and k_observed != python_value
            )
            record = {
                "rule": rule,
                "input": value,
                "python_result": python_value,
                "k_result": k_observed,
                "false_conclusion_witness": witness_holds,
            }
        else:
            match = STR_RE.search(output)
            k_bytes = parse_k_string_bytes(match.group(1)) if match else None
            python_bytes = python_value.encode("utf-8")
            witness_holds = (
                proc.returncode == 0
                and python_value == expected_python
                and k_bytes is not None
                and k_bytes != python_bytes
            )
            record = {
                "rule": rule,
                "input": value,
                "python_result": python_value,
                "python_utf8_hex": python_bytes.hex(),
                "k_string_bytes_hex": k_bytes.hex() if k_bytes is not None else None,
                "k_bytes_are_valid_utf8": (
                    False if k_bytes is None else _valid_utf8(k_bytes)
                ),
                "false_conclusion_witness": witness_holds,
            }
        print("witness=" + json.dumps(record, ensure_ascii=True, sort_keys=True))
        observed.append(record)
        if not witness_holds:
            failures.append(record)

    print(f"focused_witnesses={len(observed)} failures={len(failures)}")
    if failures:
        print(json.dumps(failures, ensure_ascii=True, sort_keys=True))
    return 1 if failures else 0


def _valid_utf8(value: bytes) -> bool:
    try:
        value.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())

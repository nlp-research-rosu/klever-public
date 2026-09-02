#!/usr/bin/env python3
"""Run the freshly compiled generated semantics and compare observable results."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable


WORK = Path("/tmp/audit-work")
DEFINITION = WORK / "execution-llvm-kompiled"
PROGRAM = WORK / "solution.mpy"


def load_function(path: Path, module_name: str) -> Callable[[str], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_palindrome


def python_outcome(function: Callable[[str], str], value: str) -> dict[str, Any]:
    try:
        result = function(value)
        return {
            "kind": "return",
            "length": len(result),
            "sha256": hashlib.sha256(
                result.encode("utf-8", "surrogatepass")
            ).hexdigest(),
            "value": result if len(result) <= 80 else None,
        }
    except BaseException as error:
        return {
            "kind": "raise",
            "type": type(error).__name__,
            "message": str(error),
        }


def k_outcome(value: str) -> tuple[dict[str, Any], list[str]]:
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        "-cINPUT=" + json.dumps(value, ensure_ascii=False),
        "--color",
        "off",
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        return {
            "kind": "krun-error",
            "exit": completed.returncode,
            "output_tail": completed.stdout[-2000:],
        }, command

    match = re.search(
        r'<result>\s*strVal \( ("(?:\\.|[^"\\])*") \) ~> \.K\s*</result>',
        completed.stdout,
        flags=re.DOTALL,
    )
    if match is None:
        return {
            "kind": "parse-error",
            "exit": completed.returncode,
            "output_tail": completed.stdout[-2000:],
        }, command

    # K's printer escapes the UTF-8 bytes of String tokens as \xHH.  Decode
    # those bytes explicitly so invalid UTF-8 produced by byte-wise operations
    # remains visible rather than being mistaken for a Python string.
    result_bytes = ast.literal_eval("b" + match.group(1))
    try:
        result = result_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        return {
            "kind": "return-invalid-utf8",
            "byte_length": len(result_bytes),
            "sha256": hashlib.sha256(result_bytes).hexdigest(),
            "decode_error": str(error),
            "k_token": match.group(1),
        }, command
    return {
        "kind": "return",
        "length": len(result),
        "sha256": hashlib.sha256(
            result.encode("utf-8", "surrogatepass")
        ).hexdigest(),
        "value": result if len(result) <= 80 else None,
    }, command


def main() -> int:
    canonical = load_function(Path("/reference/canonical.py"), "krun_oracle")
    candidate = load_function(WORK / "solution.py", "krun_candidate")
    cases = [
        ("empty", ""),
        ("one-char", "a"),
        ("first-recursive", "ab"),
        ("prompt-cat", "cat"),
        ("prompt-cata", "cata"),
        ("palindrome", "xyx"),
        ("repeated-recursion", "aabb"),
        ("unicode", "a🙂b"),
        ("python-recursion-boundary", "a" * 1200 + "b"),
    ]

    k_oracle_mismatches = 0
    k_candidate_mismatches = 0
    for name, value in cases:
        k_result, command = k_outcome(value)
        oracle_result = python_outcome(canonical, value)
        candidate_result = python_outcome(candidate, value)
        k_oracle_match = k_result == oracle_result
        k_candidate_match = k_result == candidate_result
        k_oracle_mismatches += int(not k_oracle_match)
        k_candidate_mismatches += int(not k_candidate_match)
        print("KRUN_COMMAND " + json.dumps(command, ensure_ascii=True))
        print(
            json.dumps(
                {
                    "name": name,
                    "input_length": len(value),
                    "k": k_result,
                    "oracle": oracle_result,
                    "candidate_python": candidate_result,
                    "k_matches_oracle": k_oracle_match,
                    "k_matches_candidate_python": k_candidate_match,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )

    print(
        "SUMMARY "
        + json.dumps(
            {
                "case_count": len(cases),
                "k_oracle_mismatch_count": k_oracle_mismatches,
                "k_candidate_mismatch_count": k_candidate_mismatches,
            },
            sort_keys=True,
        )
    )
    return 1 if k_oracle_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())

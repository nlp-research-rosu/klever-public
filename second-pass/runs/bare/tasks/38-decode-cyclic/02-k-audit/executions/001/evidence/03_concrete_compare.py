#!/usr/bin/env python3
"""Compare fresh K execution of the submitted .mpy with both Python programs."""

from __future__ import annotations

import importlib.util
import ast
import json
import re
import subprocess
from pathlib import Path

MPY = Path("/tmp/audit-work/38-decode-cyclic-audit/candidate-src/solution.mpy")
DEFINITION = Path(
    "/tmp/audit-work/38-decode-cyclic-audit/build-concrete/"
    "semantic-llvm-kompiled"
)
CANDIDATE = Path(
    "/tmp/audit-work/38-decode-cyclic-audit/candidate-src/solution.py"
)
CANONICAL = Path("/reference/canonical.py")

CASES = [
    "",
    "a",
    "ab",
    "abc",
    "abcd",
    "abcde",
    "abcdef",
    "abcdefg",
    "abcdefgh",
    "bca",
    "bcaefdgh",
    "\x00a",
    "\n\t\r",
    "中",
    "中ab",
    "éß中",
    "🙂🙃",
    "🙂🙃😉x",
]

RESULT_RE = re.compile(
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


def parse_k_string(token: str) -> tuple[str | None, str]:
    """Decode K's byte-escaped String display back to Python Unicode.

    The LLVM backend prints UTF-8 bytes as ``\\xNN`` escapes.  A byte sequence
    that cannot be decoded as UTF-8 is itself evidence that byte slicing split
    a Python code point.
    """
    displayed = ast.literal_eval(token)
    raw = displayed.encode("latin-1")
    try:
        return raw.decode("utf-8"), raw.hex()
    except UnicodeDecodeError:
        return None, raw.hex()


def main() -> int:
    submitted = load(CANDIDATE, "submitted_for_k_compare")
    canonical = load(CANONICAL, "trusted_for_k_compare")
    failures = []
    for value in CASES:
        # Raw non-ASCII avoids JSON surrogate-pair escapes, which K correctly
        # rejects as illegal standalone Unicode scalar values.
        config_arg = "-cS=" + json.dumps(value, ensure_ascii=False)
        command = [
            "krun",
            str(MPY),
            config_arg,
            "--definition",
            str(DEFINITION),
        ]
        print("$ " + " ".join(json.dumps(piece) for piece in command))
        proc = subprocess.run(command, text=True, capture_output=True, check=False)
        output = proc.stdout + proc.stderr
        print(output.rstrip())
        print(f"[exit {proc.returncode}]")
        match = RESULT_RE.search(output)
        if not match:
            failures.append(
                {"input": value, "failure": "could not parse K result",
                 "exit": proc.returncode, "output": output[-2000:]}
            )
            continue
        k_result, k_bytes_hex = parse_k_string(match.group(1))
        python_result = submitted.decode_cyclic(value)
        canonical_result = canonical.decode_cyclic(value)
        comparison = {
            "input": value,
            "k": k_result,
            "submitted_python": python_result,
            "trusted_canonical": canonical_result,
            "k_bytes_hex": k_bytes_hex,
            "all_equal": (
                proc.returncode == 0
                and k_result == python_result == canonical_result
            ),
        }
        print("comparison=" + json.dumps(comparison, ensure_ascii=True,
                                         sort_keys=True))
        if not comparison["all_equal"]:
            failures.append(comparison)
    print(f"cases={len(CASES)} failures={len(failures)}")
    if failures:
        print("failures=" + json.dumps(failures, ensure_ascii=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

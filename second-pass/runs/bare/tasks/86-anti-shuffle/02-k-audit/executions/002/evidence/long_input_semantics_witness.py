#!/usr/bin/env python3
"""Compare K's modeled return with real Python on a recursion-limit witness."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/anti-shuffle")
VALUE = "a" * 1100


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observed(function) -> tuple[str, str]:
    try:
        value = function(VALUE)
        return (
            "return",
            f"len={len(value)} sha256={hashlib.sha256(value.encode()).hexdigest()}",
        )
    except BaseException as error:
        return ("raise", f"{type(error).__name__}: {error}")


def main() -> int:
    canonical = load("canonical_long", WORK / "trusted/canonical.py").anti_shuffle
    generated = load("generated_long", WORK / "solution.py").anti_shuffle
    print(f"input_len={len(VALUE)}")
    print(f"input_sha256={hashlib.sha256(VALUE.encode()).hexdigest()}")
    print(f"canonical={observed(canonical)!r}")
    print(f"generated_python={observed(generated)!r}")

    k_input = '"' + VALUE + '"'
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "audit-semantics-kompiled",
        f"-cINPUT={k_input}",
    ]
    print(
        "COMMAND: krun solution.mpy --definition audit-semantics-kompiled "
        f"-cINPUT=<K string len={len(k_input)}>"
    )
    result = subprocess.run(
        command,
        cwd=WORK,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    print(f"K_EXIT_STATUS={result.returncode}")
    if result.stderr:
        print("K_STDERR=" + result.stderr.strip())
    matches = re.findall(r"<result>\s*\"([a]*)\"\s*</result>", result.stdout)
    if len(matches) != 1:
        print("K_RESULT_PARSE_FAILED")
        print(result.stdout[-4000:])
        return 2
    value = matches[0]
    print(
        "k_modeled_result="
        f"return len={len(value)} sha256={hashlib.sha256(value.encode()).hexdigest()}"
    )
    return 0 if result.returncode == 0 and value == VALUE else 1


if __name__ == "__main__":
    raise SystemExit(main())

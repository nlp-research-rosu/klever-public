#!/usr/bin/env python3
"""Check that each entry claim contains the submitted MPY program and ground it."""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path
from typing import Callable


WORK = Path("/tmp/audit-work/33-sort-third")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


def remove_insignificant_whitespace(text: str) -> str:
    output: list[str] = []
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
            output.append(character)
        elif not character.isspace():
            output.append(character)
    if in_string:
        raise ValueError("unterminated string")
    return "".join(output)


def extract_claim_programs(spec_text: str) -> list[str]:
    programs: list[str] = []
    for k_cell in re.findall(r"<k>(.*?)</k>", spec_text, flags=re.DOTALL):
        prefix, marker, _ = k_cell.partition("=> .K")
        if not marker:
            raise ValueError("entry <k> cell has no => .K")
        start = prefix.find("Module(")
        if start < 0:
            raise ValueError("entry <k> cell has no Module term")
        programs.append(prefix[start:].strip())
    return programs


def contract(values: list[int]) -> list[int]:
    selected = sorted(values[::3])
    result = list(values)
    result[::3] = selected
    return result


def main() -> int:
    submitted = remove_insignificant_whitespace(
        (WORK / "solution.mpy").read_text(encoding="utf-8")
    )
    programs = extract_claim_programs((WORK / "spec.k").read_text(encoding="utf-8"))
    print(f"ENTRY_CLAIM_COUNT={len(programs)}")
    print(f"SUBMITTED_NORMALIZED_SHA256={hashlib.sha256(submitted.encode()).hexdigest()}")
    pinning_failures = 0
    for index, program in enumerate(programs, 1):
        normalized = remove_insignificant_whitespace(program)
        identical = normalized == submitted
        print(
            f"CLAIM_{index}_PROGRAM_SHA256="
            f"{hashlib.sha256(normalized.encode()).hexdigest()} IDENTICAL={identical}"
        )
        pinning_failures += int(not identical)

    canonical = load_entry(WORK / "canonical.py", "stage4_canonical")
    candidate = load_entry(WORK / "solution.py", "stage4_candidate")
    witnesses = [
        # Satisfies the universal claim; also covers the zero-length boundary.
        [],
        # Satisfies both the universal claim and fixed example claim 2.
        [5, 6, 3, 4, 8, 9, 2],
        # Satisfies both the universal claim and fixed example claim 3.
        [1, 2, 3],
        # Additional universal-claim witness with negative/distinct outcomes.
        [-1, 7, 8, -3, 9, 10, -2],
    ]
    witness_failures = 0
    for index, values in enumerate(witnesses, 1):
        claimed = contract(values)
        canonical_result = canonical(list(values))
        candidate_result = candidate(list(values))
        passed = claimed == canonical_result == candidate_result
        print(
            f"WITNESS_{index}: START=<k>submitted-solution.mpy</k> "
            f"<input>VList{tuple(values)!r}</input> <result>.K</result>"
        )
        print(
            f"WITNESS_{index}: CLAIMED={claimed!r} "
            f"CANONICAL={canonical_result!r} CANDIDATE={candidate_result!r} "
            f"PASS={passed}"
        )
        witness_failures += int(not passed)

    failures = pinning_failures + witness_failures
    print(f"FAILURE_COUNT={failures}")
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())

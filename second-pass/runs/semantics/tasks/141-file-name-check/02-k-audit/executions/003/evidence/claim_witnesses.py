#!/usr/bin/env python3
"""Exhibit concrete satisfying inputs for all six submitted entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


def observations(value: str) -> dict[str, object]:
    return {
        "charCount(dot)": value.count("."),
        "isLen": len(value),
        "headCode": ord(value[0]) if value else None,
        "latinCode": bool(value)
        and ("A" <= value[0] <= "Z" or "a" <= value[0] <= "z"),
        "suffix4": value[-4:],
        "allowedSuffix": value[-4:] in {".txt", ".exe", ".dll"},
        "digitCount": sum("0" <= character <= "9" for character in value),
        "IntSeq": [ord(character) for character in value],
    }


def precondition(claim: int, obs: dict[str, object]) -> bool:
    dots = int(obs["charCount(dot)"])
    length = int(obs["isLen"])
    latin = bool(obs["latinCode"])
    suffix = bool(obs["allowedSuffix"])
    digits = int(obs["digitCount"])
    if claim == 1:
        return dots != 1
    if claim == 2:
        return dots == 1 and length < 5
    if claim == 3:
        return dots == 1 and length >= 5 and not latin
    if claim == 4:
        return dots == 1 and length >= 5 and latin and not suffix
    if claim == 5:
        return dots == 1 and length >= 5 and latin and suffix and digits > 3
    if claim == 6:
        return dots == 1 and length >= 5 and latin and suffix and digits <= 3
    raise ValueError(claim)


def main() -> int:
    canonical = load_function("canonical_witness", Path("/reference/canonical.py"))
    candidate = load_function(
        "candidate_witness",
        Path("/tmp/audit-work/reconstruction/solution.py"),
    )
    witnesses = {
        1: ("", "No"),
        2: (".txt", "No"),
        3: ("1.txt", "No"),
        4: ("a.bin", "No"),
        5: ("a1234.txt", "No"),
        6: ("a123.txt", "Yes"),
    }
    errors = 0
    for claim, (value, claimed_result) in witnesses.items():
        obs = observations(value)
        holds = precondition(claim, obs)
        actual_candidate = candidate(value)
        actual_canonical = canonical(value)
        print(f"claim={claim} input={value!r}")
        print(f"  observations={obs}")
        print(f"  precondition_holds={holds}")
        print(f"  claimed_result={claimed_result!r}")
        print(f"  candidate_result={actual_candidate!r}")
        print(f"  canonical_result={actual_canonical!r}")
        if not (
            holds
            and claimed_result == actual_candidate
            and claimed_result == actual_canonical
        ):
            errors += 1
    print(f"witness_errors={errors}")
    return int(errors != 0)


if __name__ == "__main__":
    raise SystemExit(main())

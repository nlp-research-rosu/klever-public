#!/usr/bin/env python3
"""Mechanical entry-program pinning checks and concrete claim witnesses."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
from collections.abc import Callable


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[list[str]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "concatenate")


def compact(text: str) -> str:
    return "".join(text.split())


def fold(accumulator: str, remaining: list[str]) -> str:
    value = accumulator
    for item in remaining:
        value += item
    return value


def main() -> int:
    mpy_path = pathlib.Path("/tmp/audit-work/fresh/solution.mpy")
    spec_path = pathlib.Path("/tmp/audit-work/fresh/spec.k")
    mpy_bytes = mpy_path.read_bytes()
    mpy = compact(mpy_bytes.decode("utf-8"))
    spec = compact(spec_path.read_text(encoding="utf-8"))

    entry_prefix = f'load({mpy})~>invoke("concatenate",lVal(INPUT:StrList))=>.K'
    loop_body = (
        'Assign(Name("result"),'
        'BinOp("+",Name("result"),Name("string")))'
    )
    loop_control = (
        f'loop("string",ITEMS:StrList,{loop_body})'
        '~>(Return(Name("result")).PyStmts)~>cleanup=>.K'
    )
    checks = {
        "entry_contains_exact_submitted_mpy": entry_prefix in spec,
        "actual_program_contains_loop_body": loop_body in mpy,
        "loop_claim_contains_actual_body_and_suffix": loop_control in spec,
        "entry_result_is_constrained": (
            '<result>noResult=>sVal(concatAcc("",INPUT))</result>' in spec
        ),
        "loop_result_is_constrained": (
            '<result>noResult=>sVal(concatAcc(ACC,ITEMS))</result>' in spec
        ),
    }
    print(
        json.dumps(
            {
                "pinning": checks,
                "solution_mpy_sha256": hashlib.sha256(mpy_bytes).hexdigest(),
                "entry_needle": entry_prefix,
                "loop_needle": loop_control,
            },
            sort_keys=True,
        )
    )

    canonical = load_entry(pathlib.Path("/reference/canonical.py"), "witness_canonical")
    generated = load_entry(
        pathlib.Path("/tmp/audit-work/fresh/solution.py"), "witness_generated"
    )

    complete_input = ["a", "b", "c"]
    entry_expected = fold("", complete_input)
    entry_witness = {
        "claim": "SPEC.concatenate-correct",
        "precondition": "no explicit requires; exact initial six-cell configuration",
        "substitution": {"INPUT": complete_input},
        "claimed_result": entry_expected,
        "canonical_result": canonical(complete_input),
        "generated_result": generated(complete_input),
    }
    entry_witness["all_equal"] = len(
        {
            entry_witness["claimed_result"],
            entry_witness["canonical_result"],
            entry_witness["generated_result"],
        }
    ) == 1
    print(json.dumps(entry_witness, sort_keys=True))

    # This is also a reachable loop-head state after the first iteration on
    # ["a", "b", "c"]: ACC and CURRENT are "a", and ITEMS is ["b", "c"].
    loop_expected = fold("a", ["b", "c"])
    loop_witness = {
        "claim": "SPEC.concatenate-loop",
        "precondition": "no explicit requires; exact loop-head six-cell configuration",
        "substitution": {
            "ITEMS": ["b", "c"],
            "ACC": "a",
            "_CURRENT": "a",
            "_ALL": complete_input,
            "_FUN": 'function("concatenate", "strings", submitted-body)',
        },
        "reachable_from_entry_input": complete_input,
        "claimed_result": loop_expected,
        "canonical_result": canonical(complete_input),
        "generated_result": generated(complete_input),
    }
    loop_witness["all_equal"] = len(
        {
            loop_witness["claimed_result"],
            loop_witness["canonical_result"],
            loop_witness["generated_result"],
        }
    ) == 1
    print(json.dumps(loop_witness, sort_keys=True))

    return 0 if all(checks.values()) and entry_witness["all_equal"] and loop_witness["all_equal"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Check hard-coded program identity and exhibit satisfying claim witnesses."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/123-get-odd-collatz")
SOLUTION_MPY = ROOT / "proof-src" / "solution.mpy"
VERIFICATION_K = ROOT / "proof-src" / "verification.k"
SPEC_K = ROOT / "proof-src" / "spec.k"
CANONICAL_PY = ROOT / "trusted" / "canonical.py"
GENERATED_PY = ROOT / "proof-src" / "solution.py"


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def balanced_term(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unbalanced Module term")


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\.Exprs|[A-Za-z_#][A-Za-z0-9_#-]*|-?\d+|[(),]')


def normalized_tokens(text: str) -> list[str]:
    # `.Exprs` is the K list unit, and the surface parser also accepts its
    # omission in an empty variadic argument position.
    return [token for token in TOKEN.findall(text) if token != ".Exprs"]


def main() -> None:
    verification_text = VERIFICATION_K.read_text(encoding="utf-8")
    solution_text = SOLUTION_MPY.read_text(encoding="utf-8")
    spec_text = SPEC_K.read_text(encoding="utf-8")
    module_start = verification_text.index("Module(")
    embedded_module = balanced_term(verification_text, module_start)
    submitted_tokens = normalized_tokens(solution_text)
    embedded_tokens = normalized_tokens(embedded_module)

    print(
        json.dumps(
            {
                "program_pinning": {
                    "solution_mpy": str(SOLUTION_MPY),
                    "verification_k": str(VERIFICATION_K),
                    "normalized_token_identity": submitted_tokens == embedded_tokens,
                    "submitted_token_count": len(submitted_tokens),
                    "embedded_token_count": len(embedded_tokens),
                    "solution_mpy_is_required_by_proof_source": bool(
                        re.search(
                            r'requires\s+"[^"]*solution\.mpy"',
                            verification_text + "\n" + spec_text,
                        )
                    ),
                    "mechanism": "hard-coded MPY Module term in #getOddCollatz",
                }
            },
            sort_keys=True,
        )
    )
    if submitted_tokens != embedded_tokens:
        print(
            json.dumps(
                {
                    "submitted_tokens": submitted_tokens,
                    "embedded_tokens": embedded_tokens,
                },
                sort_keys=True,
            )
        )

    entry_arguments = re.findall(r"<k>\s*#getOddCollatz\(([^)]*)\)", spec_text)
    print(
        json.dumps(
            {
                "entry_claims": {
                    "arguments": entry_arguments,
                    "has_symbolic_argument": any(
                        not re.fullmatch(r"-?\d+", argument.strip())
                        for argument in entry_arguments
                    ),
                    "collatzResult_occurrences_in_spec": spec_text.count(
                        "collatzResult"
                    ),
                }
            },
            sort_keys=True,
        )
    )

    canonical = load(CANONICAL_PY, "stage4_canonical")
    generated = load(GENERATED_PY, "stage4_generated")

    witness_records = [
        {
            "claim": "odd-step",
            "precondition_witness": {"N": 3, "A": []},
            "claimed_one_step": {"n": 10, "A": [3]},
            "direct_one_step": {"n": 3 * 3 + 1, "A": [3]},
        },
        {
            "claim": "even-step",
            "precondition_witness": {"N": 2, "A": []},
            "claimed_one_step": {"n": 1, "A": []},
            "direct_one_step": {"n": 2 // 2, "A": []},
        },
        {
            "claim": "exit-step",
            "precondition_witness": {
                "n": 1,
                "A": [3, 5],
                "caller_scope": {},
                "sorted_unshadowed": True,
            },
            "claimed_result_sequence": [1, 3, 5],
            "canonical_input_3": canonical.get_odd_collatz(3),
            "generated_input_3": generated.get_odd_collatz(3),
        },
    ]
    for value, unsorted_trace in [
        (1, [1]),
        (5, [5, 1]),
        (6, [3, 5, 1]),
        (7, [7, 11, 17, 13, 5, 1]),
    ]:
        witness_records.append(
            {
                "claim": f"case-{value}",
                "precondition_witness": {
                    "input": value,
                    "initial_env": 0,
                    "empty_user_scope": True,
                    "empty_heap": True,
                },
                "claimed_unsorted_trace": unsorted_trace,
                "claimed_sorted_result": sorted(unsorted_trace),
                "canonical_result": canonical.get_odd_collatz(value),
                "generated_result": generated.get_odd_collatz(value),
            }
        )
    print(json.dumps({"witnesses": witness_records}, sort_keys=True))


if __name__ == "__main__":
    main()

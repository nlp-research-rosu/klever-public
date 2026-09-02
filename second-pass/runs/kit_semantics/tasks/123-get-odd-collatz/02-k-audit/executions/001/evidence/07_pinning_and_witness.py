"""Mechanical body comparison and concrete satisfying-state witnesses."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from typing import Callable


def balanced_call(text: str, marker: str) -> str:
    start = text.index(marker)
    open_paren = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced constructor at {marker!r}")


def normalized(term: str) -> str:
    compact = re.sub(r"\s+", "", term)
    compact = compact.replace("ListExpr()", "ListExpr(.Exprs)")
    compact = compact.replace(
        'Call(Attribute(Name("odds"),"sort"),)',
        'Call(Attribute(Name("odds"),"sort"),.Exprs)',
    )
    return compact


def load_entry(path: str, module_name: str) -> Callable[[int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_odd_collatz


def collatz_trace(n: int) -> list[int]:
    result = [n]
    while n > 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        result.append(n)
    return result


def main() -> None:
    submitted_text = Path("/candidate/solution.mpy").read_text(encoding="utf-8")
    spec_text = Path("/candidate/spec.k").read_text(encoding="utf-8")
    marker = 'FuncDef("get_odd_collatz"'
    submitted = balanced_call(submitted_text, marker)
    claimed = balanced_call(spec_text, marker)
    submitted_normalized = normalized(submitted)
    claimed_normalized = normalized(claimed)
    print(f"submitted_funcdef_count={submitted_text.count(marker)}")
    print(f"claim_funcdef_count={spec_text.count(marker)}")
    print(f"normalized_constructor_body_equal={submitted_normalized == claimed_normalized}")
    print(f"submitted_normalized_sha256_input_length={len(submitted_normalized)}")
    print(f"claimed_normalized_sha256_input_length={len(claimed_normalized)}")
    if submitted_normalized != claimed_normalized:
        raise SystemExit(1)

    canonical = load_entry("/reference/canonical.py", "canonical_witness_123")
    generated = load_entry("/candidate/solution.py", "generated_witness_123")
    for n in (1, 2, 3, 5):
        trace = collatz_trace(n)
        odd_without_last = [value for value in trace[:-1] if value % 2 == 1]
        claimed_result = sorted(odd_without_last + [1])
        canonical_result = canonical(n)
        generated_result = generated(n)
        print(
            "witness",
            {
                "N": n,
                "loop_precondition_state": {
                    "S": n,
                    "current_N": n,
                    "trace_T": [n],
                    "odds_A": [],
                    "HO": 0,
                    "HT": 1,
                },
                "terminal_trace": trace,
                "claimed_result": claimed_result,
                "canonical_result": canonical_result,
                "generated_result": generated_result,
                "all_equal": (
                    claimed_result == canonical_result == generated_result
                ),
            },
        )
        if claimed_result != canonical_result or claimed_result != generated_result:
            raise SystemExit(1)


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""Compare fresh module-loaded closures with proof-alias expansions."""

from pathlib import Path
import re


CONCRETE_LOG = Path("/audit-output/evidence/10_run_concrete.log")
PROOF_RESIDUAL_LOG = Path(
    "/audit-output/evidence/18_vacuity_proof_expected_failure.log"
)


def closure(text: str, binding: str) -> str:
    marker = f'"{binding}" |-> closureVal'
    marker_at = text.index(marker)
    start = text.index("closureVal", marker_at)
    open_at = text.index("(", start)
    depth = 0
    quoted = False
    escaped = False
    for index in range(open_at, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                raw = text[start : index + 1]
                return re.sub(r"\s+", " ", raw).strip()
    raise ValueError(f"unclosed closure for {binding}")


def main() -> int:
    concrete = CONCRETE_LOG.read_text()
    proof = PROOF_RESIDUAL_LOG.read_text()
    mismatches = 0
    for binding in ["_is_prime", "prime_fib"]:
        concrete_closure = closure(concrete, binding)
        proof_closure = closure(proof, binding)
        same = concrete_closure == proof_closure
        print(
            f"BINDING={binding} EXACT_NORMALIZED_CLOSURE_MATCH={same} "
            f"concrete_chars={len(concrete_closure)} proof_chars={len(proof_closure)}"
        )
        if not same:
            mismatches += 1
    print(f"CLOSURE_MISMATCHES={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())

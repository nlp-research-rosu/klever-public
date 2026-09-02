#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/95-check-dict-case-audit
status=0

printf '%s\n' 'COMMAND: constructor-level comparison of program.k and regenerated solution.mpy'
PYTHONDONTWRITEBYTECODE=1 python3 - "$scratch" <<'PY'
import hashlib
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
mpy = (root / "regenerated-solution.mpy").read_text(encoding="utf-8").strip()
program = (root / "program.k").read_text(encoding="utf-8")
marker = "rule solutionProgram => "
if marker not in program:
    raise SystemExit("missing solutionProgram rule")
rhs = program.split(marker, 1)[1].rsplit("endmodule", 1)[0].strip()

def strip_k_whitespace(term: str) -> str:
    result = []
    quoted = False
    escaped = False
    for character in term:
        if quoted:
            result.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
            result.append(character)
        elif not character.isspace():
            result.append(character)
    if quoted:
        raise ValueError("unterminated string")
    return "".join(result)

normalized_mpy = strip_k_whitespace(mpy)
normalized_rhs = strip_k_whitespace(rhs)
print(f"normalized_mpy_sha256={hashlib.sha256(normalized_mpy.encode()).hexdigest()}")
print(f"normalized_program_rhs_sha256={hashlib.sha256(normalized_rhs.encode()).hexdigest()}")
print(f"constructor_terms_equal={normalized_mpy == normalized_rhs}")
if normalized_mpy != normalized_rhs:
    raise SystemExit(1)

spec = (root / "spec.k").read_text(encoding="utf-8")
claim_count = len(re.findall(r"(?m)^\s*claim\s*$", spec))
has_requires = bool(re.search(r"(?m)^\s+requires\b", spec))
has_ensures = bool(re.search(r"(?m)^\s+ensures\b", spec))
has_typed_variable = bool(re.search(r"\b[A-Z][A-Za-z0-9_]*\s*:", spec))
print(f"claim_count={claim_count}")
print(f"has_requires_clause={has_requires}")
print(f"has_ensures_clause={has_ensures}")
print(f"has_typed_symbolic_variable={has_typed_variable}")

def claim_bodies(text: str) -> list[str]:
    starts = list(
        re.finditer(r"(?m)^\s*claim(?:\s+\[[^\]]+\]:)?\s*$", text)
    )
    bodies = []
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else text.rfind("endmodule")
        bodies.append(strip_k_whitespace(text[match.end():end]))
    return bodies

labeled = Path("/audit-output/evidence/spec-labeled.k").read_text(encoding="utf-8")
original_bodies = claim_bodies(spec)
labeled_bodies = claim_bodies(labeled)
print(f"labeled_claim_count={len(labeled_bodies)}")
print(f"labeled_claim_bodies_equal={original_bodies == labeled_bodies}")
if original_bodies != labeled_bodies:
    raise SystemExit(1)
PY
pin_status=$?
printf 'PINNING_CHECK_EXIT=%s\n' "$pin_status"
if [[ "$pin_status" -ne 0 ]]; then
  status=1
fi

printf '%s\n' 'COMMAND: python3 claim_witnesses.py SCRATCH'
PYTHONDONTWRITEBYTECODE=1 python3 \
  /audit-output/evidence/claim_witnesses.py \
  "$scratch"
witness_status=$?
printf 'CLAIM_WITNESSES_EXIT=%s\n' "$witness_status"
if [[ "$witness_status" -ne 0 ]]; then
  status=1
fi

printf 'ADEQUACY_SCRIPT_STATUS=%s\n' "$status"
exit "$status"

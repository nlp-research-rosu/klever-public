#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/130-tri-audit
definition="$audit_work/verification-proof-kompiled"
cd "$audit_work" || exit 2

printf 'COMMAND: kast submitted solution.mpy to canonical KORE\n'
kast --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Program \
  --output kore \
  solution.mpy > submitted-program.kore
submitted_status=$?
printf 'SUBMITTED_KAST_EXIT_STATUS=%s\n' "$submitted_status"

printf 'COMMAND: kast expanded solutionProgram macro to canonical KORE\n'
kast --definition "$definition" \
  --module TRI-VERIFICATION \
  --sort Program \
  --expand-macros \
  --output kore \
  --expression solutionProgram > claimed-program.kore
claimed_status=$?
printf 'CLAIMED_KAST_EXIT_STATUS=%s\n' "$claimed_status"

printf 'COMMAND: cmp -s submitted-program.kore claimed-program.kore\n'
cmp -s submitted-program.kore claimed-program.kore
pin_status=$?
printf 'PROGRAM_PIN_CMP_EXIT_STATUS=%s\n' "$pin_status"
sha256sum submitted-program.kore claimed-program.kore
wc -c submitted-program.kore claimed-program.kore

printf '\nGROUND SUBSTITUTIONS\n'
python3 - <<'PY'
import importlib.util
from pathlib import Path

root = Path("/tmp/audit-work/130-tri-audit")
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

candidate = load("candidate_substitution", root / "solution.py")
canonical = load("canonical_substitution", root / "canonical.py")
for n in (0, 1, 2, 3, 6, 25):
    candidate_value = candidate.tri(n)
    canonical_value = canonical.tri(n)
    print(
        f"N={n} PRECONDITION_N_GE_0={n >= 0} "
        f"CANDIDATE={candidate_value} CANONICAL={canonical_value} "
        f"NUMERIC_EQUAL={candidate_value == canonical_value}"
    )
PY
substitution_status=$?
printf 'GROUND_SUBSTITUTION_EXIT_STATUS=%s\n' "$substitution_status"

if [[ "$submitted_status" -ne 0 || "$claimed_status" -ne 0 ||
      "$pin_status" -ne 0 || "$substitution_status" -ne 0 ]]; then
  exit 1
fi


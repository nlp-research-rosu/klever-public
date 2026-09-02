#!/usr/bin/env bash
set -u

status=0
work=/tmp/audit-work/rebuild
definition="$work/proof-kompiled"
submitted_kore=/audit-output/evidence/stage4_submitted_program.kore
macro_kore=/audit-output/evidence/stage4_claim_program_macro.kore

echo '$ kast solution.mpy --definition proof-kompiled --module FIBFIB --sort Pgm --expand-macros --output kore --output-file /audit-output/evidence/stage4_submitted_program.kore'
kast "$work/solution.mpy" \
  --definition "$definition" \
  --module FIBFIB \
  --sort Pgm \
  --expand-macros \
  --output kore \
  --output-file "$submitted_kore"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ kast --expression fibfibProgram --definition proof-kompiled --module FIBFIB --sort Pgm --expand-macros --output kore --output-file /audit-output/evidence/stage4_claim_program_macro.kore'
kast \
  --expression fibfibProgram \
  --definition "$definition" \
  --module FIBFIB \
  --sort Pgm \
  --expand-macros \
  --output kore \
  --output-file "$macro_kore"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ sha256sum submitted-program.kore claim-program-macro.kore'
sha256sum "$submitted_kore" "$macro_kore"

echo '$ cmp -s submitted-program.kore claim-program-macro.kore'
cmp -s "$submitted_kore" "$macro_kore"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ wc -c submitted-program.kore claim-program-macro.kore'
wc -c "$submitted_kore" "$macro_kore"

echo '$ cp reviewer ground spec to scratch and kprove it'
cp --no-dereference /audit-output/evidence/spec-ground.k "$work/spec-ground.k"
(
  cd "$work" || exit 1
  echo '$ kprove spec-ground.k --definition proof-kompiled --spec-module FIBFIB-SPEC-GROUND'
  kprove spec-ground.k \
    --definition proof-kompiled \
    --spec-module FIBFIB-SPEC-GROUND
)
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ compare the N=5 claimed return with both Python implementations'
python3 - <<'PY'
import importlib.util
from pathlib import Path

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib

canonical = load("canonical_ground", Path("/tmp/audit-work/reference-src/canonical.py"))
generated = load("generated_ground", Path("/tmp/audit-work/candidate-src/solution.py"))
n = 5
claimed = 4
print(f"N={n} precondition_0_le_N={0 <= n}")
print(f"claimed={claimed} canonical={canonical(n)} generated={generated(n)}")
print(f"all_equal={claimed == canonical(n) == generated(n)}")
if claimed != canonical(n) or claimed != generated(n):
    raise SystemExit(1)
PY
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo "overall_exit=$status"
exit "$status"

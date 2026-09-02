#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
definition="$work/fresh-verification-kompiled"
overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    overall=1
  fi
}

printf 'STAGE 4 ADEQUACY, PINNING, AND SATISFYING WITNESSES\n'
run python3 "$evidence/extract_claim_modules.py"

run kast --definition "$definition" --module MPY-SYNTAX --sort Module \
  --output json --output-file "$evidence/stage4-solution-module.kast.json" \
  "$work/solution.mpy"

for number in 1 2 3 4; do
  run kast --definition "$definition" --module MPY-SYNTAX --sort Module \
    --output json --output-file "$evidence/stage4-claim-module-$number.kast.json" \
    "$work/extracted-claim-modules/claim-module-$number.program.mpy"
  run cmp -s "$evidence/stage4-solution-module.kast.json" \
    "$evidence/stage4-claim-module-$number.kast.json"
done

run sha256sum "$evidence/stage4-solution-module.kast.json" \
  "$evidence/stage4-claim-module-1.kast.json" \
  "$evidence/stage4-claim-module-2.kast.json" \
  "$evidence/stage4-claim-module-3.kast.json" \
  "$evidence/stage4-claim-module-4.kast.json"
run python3 "$evidence/stage4_witness.py"

printf '\nDOCUMENTED SUPPLIED-MODEL REPRESENTATION-GAP WITNESS\n'
run python3 "$work/model-gap-decimal.py"
printf '\n$ cd %q && python3 py2mpy.py model-gap-decimal.py > model-gap-decimal.mpy\n' "$work"
(cd "$work" && python3 py2mpy.py model-gap-decimal.py > model-gap-decimal.mpy)
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then
  overall=1
fi

# The supplied model has no Decimal value/builtin/import binding. A normal
# model run is therefore expected to stop before .K; this observation is not
# treated as a failure of this audit script.
printf '\n$ cd %q && krun model-gap-decimal.mpy --definition fresh-runtime-kompiled\n' "$work"
(cd "$work" && krun model-gap-decimal.mpy --definition fresh-runtime-kompiled)
rc=$?
printf '[observational exit %d; inspect final <k>/<exc>/<exit-code> above]\n' "$rc"

run rg -n 'syntax Val|Decimal|ImportFrom' \
  "$work/reference-semantics/semantics/core.k" \
  "$work/reference-semantics/semantics/controls.k" \
  "$work/reference-semantics/semantics/builtins.k"

exit "$overall"

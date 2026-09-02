#!/usr/bin/env bash
set -u

record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return "$status"
}

overall=0
work=/tmp/audit-work/124-valid-date

record bash -c \
  'head -n 40 /audit-output/evidence/03_concrete_tests.py | cmp - /tmp/audit-work/124-valid-date/solution.py' \
  || overall=1
record env PYTHONDONTWRITEBYTECODE=1 python3 \
  /audit-output/evidence/03_concrete_tests.py \
  || overall=1

printf 'COMMAND: python3 %q %q > %q\n' \
  "$work/trusted/py2mpy.py" \
  /audit-output/evidence/03_concrete_tests.py \
  "$work/reviewer-concrete-tests.mpy"
python3 "$work/trusted/py2mpy.py" \
  /audit-output/evidence/03_concrete_tests.py \
  > "$work/reviewer-concrete-tests.mpy"
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
if (( status != 0 )); then overall=1; fi

record kompile "$work/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/runtime-fresh-kompiled" \
  || overall=1

record krun "$work/reviewer-concrete-tests.mpy" \
  --definition "$work/runtime-fresh-kompiled" \
  || overall=1

record bash -c \
  'awk "/^\\/\\/ BEGIN SOLUTION-MPY$/{copy=1;next} /^\\/\\/ END SOLUTION-MPY$/{copy=0} copy" /tmp/audit-work/124-valid-date/verification.k > /tmp/audit-work/124-valid-date/embedded-solution.mpy' \
  || overall=1
printf 'COMMAND: kast %q --definition %q --input program --output json > %q\n' \
  "$work/solution.mpy" \
  "$work/runtime-fresh-kompiled" \
  "$work/solution.kast.json"
kast "$work/solution.mpy" \
  --definition "$work/runtime-fresh-kompiled" \
  --input program \
  --output json > "$work/solution.kast.json"
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
if (( status != 0 )); then overall=1; fi
printf 'COMMAND: kast %q --definition %q --input program --output json > %q\n' \
  "$work/embedded-solution.mpy" \
  "$work/runtime-fresh-kompiled" \
  "$work/embedded-solution.kast.json"
kast "$work/embedded-solution.mpy" \
  --definition "$work/runtime-fresh-kompiled" \
  --input program \
  --output json > "$work/embedded-solution.kast.json"
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
if (( status != 0 )); then overall=1; fi
record cmp "$work/solution.kast.json" "$work/embedded-solution.kast.json" || overall=1
record sha256sum "$work/solution.kast.json" "$work/embedded-solution.kast.json" || overall=1

record kompile --backend haskell "$work/verification.k" \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/verification-fresh-kompiled" \
  || overall=1

record kprove "$work/spec.k" \
  --definition "$work/verification-fresh-kompiled" \
  --spec-module SPEC \
  --claims SPEC.valid-date-non10 \
  || overall=1

record kprove "$work/spec.k" \
  --definition "$work/verification-fresh-kompiled" \
  --spec-module SPEC \
  --claims SPEC.valid-date-ten \
  || overall=1

record kprove "$work/spec.k" \
  --definition "$work/verification-fresh-kompiled" \
  --spec-module SPEC \
  || overall=1

printf 'OVERALL_STATUS: %d\n' "$overall"
exit "$overall"

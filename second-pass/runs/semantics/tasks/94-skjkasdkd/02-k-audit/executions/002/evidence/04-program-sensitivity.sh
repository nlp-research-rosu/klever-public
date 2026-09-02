#!/usr/bin/env bash
set -u

evidence=/audit-output/evidence
overall=0

{
  echo "COMMAND: translate materially changed submitted function"
  python3 py2mpy.py solution-program-mut.py > solution-program-mut.mpy
  rc=$?
  echo "EXIT_STATUS=$rc"
} > "$evidence/04-program-mut-translate.log" 2>&1
(( rc == 0 )) || overall=1

{
  echo "COMMAND: compile definition with only solutionModule changed"
  kompile verification-program-mut.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module VERIFICATION \
    --output-definition program-mut-kompiled \
    -I .
  rc=$?
  echo "EXIT_STATUS=$rc"
} > "$evidence/04-program-mut-kompile.log" 2>&1
(( rc == 0 )) || overall=1

{
  echo "COMMAND: mechanically pin changed submitted term to changed claim term"
  kast --definition program-mut-kompiled --module VERIFICATION \
    --sort Module --expand-macros --output kore \
    solution-program-mut.mpy --output-file solution-program-mut.kore
  first_rc=$?
  kast --definition program-mut-kompiled --module VERIFICATION \
    --sort Module --expand-macros --output kore \
    solution-module-symbol.mpy --output-file solution-module-program-mut.kore
  second_rc=$?
  cmp solution-program-mut.kore solution-module-program-mut.kore
  cmp_rc=$?
  sha256sum solution-program-mut.kore solution-module-program-mut.kore \
    /tmp/audit-work/reconstruction/solution.kore
  if cmp -s solution-program-mut.kore \
    /tmp/audit-work/reconstruction/solution.kore; then
    changed_rc=1
  else
    changed_rc=0
  fi
  echo "changed_term_status=$changed_rc"
  echo "pin_cmp_status=$cmp_rc"
} > "$evidence/04-program-mut-kast-pin.log" 2>&1
(( first_rc == 0 && second_rc == 0 && cmp_rc == 0 && changed_rc == 0 )) \
  || overall=1

{
  echo "COMMAND: prove false result 2 for changed actual body on [2]"
  kprove program-mut-ground.k \
    --definition program-mut-kompiled \
    --spec-module PROGRAM-MUT-GROUND \
    --output pretty
  rc=$?
  echo "EXIT_STATUS=$rc"
} > "$evidence/04-program-mut-ground.log" 2>&1
ground_rc=$rc
if (( ground_rc == 0 )); then
  echo "unexpected: changed-program false result closed"
  overall=1
elif rg -q 'WarnStuckClaimState|cannot be rewritten further' \
  "$evidence/04-program-mut-ground.log" \
  && rg -q '<k>|1' "$evidence/04-program-mut-ground.log"; then
  echo "expected: changed actual program term invalidates result 2"
else
  echo "unexpected ground sensitivity failure mode"
  overall=1
fi

{
  echo "COMMAND: rerun end-to-end theorem after changing only actual program term"
  kprove spec-program-mut.k \
    --definition program-mut-kompiled \
    --spec-module SPEC \
    --claims SPEC.main-correct,SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
    --trusted SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
    --output pretty
  rc=$?
  echo "EXIT_STATUS=$rc"
} > "$evidence/04-program-mut-main.log" 2>&1
main_rc=$rc
if (( main_rc == 0 )); then
  echo "unexpected: end-to-end theorem insensitive to changed actual term"
  overall=1
elif rg -q 'WarnStuckClaimState|cannot be rewritten further' \
  "$evidence/04-program-mut-main.log"; then
  echo "expected: end-to-end theorem is sensitive to changed actual term"
else
  echo "unexpected main sensitivity failure mode"
  overall=1
fi

echo "FINAL_STATUS=$overall"
exit "$overall"

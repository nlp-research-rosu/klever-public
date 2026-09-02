#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/105-by-length/recon
overall=0
for name in \
  bridge-witness-programs.k \
  bridge-witness-fixed.k \
  bridge-witness-extended.k \
  bridge-witness-correct-spec.k \
  bridge-witness-false-spec.k \
  bridge-witness-fixed-false-spec.k
do
  cp "/audit-output/evidence/$name" "$scratch/$name"
done

printf 'COMMAND: cd %s && kompile bridge-witness-fixed.k --backend haskell --main-module LOOP-WITNESS-FIXED --syntax-module MPY-SYNTAX --output-definition bridge-fixed-kompiled\n' "$scratch"
(
  cd "$scratch" || exit 90
  kompile bridge-witness-fixed.k \
    --backend haskell \
    --main-module LOOP-WITNESS-FIXED \
    --syntax-module MPY-SYNTAX \
    --output-definition bridge-fixed-kompiled
)
fixed_compile_rc=$?
printf 'FIXED_KOMPILE_EXIT_STATUS: %s\n' "$fixed_compile_rc"
if (( fixed_compile_rc != 0 )); then
  overall=1
fi

if (( fixed_compile_rc == 0 )); then
  printf 'COMMAND: cd %s && kprove bridge-witness-correct-spec.k --definition bridge-fixed-kompiled --spec-module LOOP-WITNESS-CORRECT-SPEC\n' "$scratch"
  (
    cd "$scratch" || exit 90
    set -o pipefail
    kprove bridge-witness-correct-spec.k \
      --definition bridge-fixed-kompiled \
      --spec-module LOOP-WITNESS-CORRECT-SPEC \
      2>&1 | tee bridge-fixed-correct.stdout
  )
  fixed_correct_rc=$?
  if rg -x '#Top' "$scratch/bridge-fixed-correct.stdout" >/dev/null; then
    fixed_correct_top_rc=0
  else
    fixed_correct_top_rc=1
  fi

  printf 'COMMAND (expected proof failure): cd %s && kprove bridge-witness-fixed-false-spec.k --definition bridge-fixed-kompiled --spec-module LOOP-WITNESS-FIXED-FALSE-SPEC\n' "$scratch"
  (
    cd "$scratch" || exit 90
    set -o pipefail
    kprove bridge-witness-fixed-false-spec.k \
      --definition bridge-fixed-kompiled \
      --spec-module LOOP-WITNESS-FIXED-FALSE-SPEC \
      2>&1 | tee bridge-fixed-false.stdout
  )
  fixed_false_rc=$?
  if rg 'WarnStuckClaimState' "$scratch/bridge-fixed-false.stdout" >/dev/null; then
    fixed_false_stuck_rc=0
  else
    fixed_false_stuck_rc=1
  fi
else
  fixed_correct_rc=99
  fixed_correct_top_rc=99
  fixed_false_rc=99
  fixed_false_stuck_rc=99
fi
printf 'FIXED_CORRECT_KPROVE_EXIT_STATUS: %s\n' "$fixed_correct_rc"
printf 'FIXED_CORRECT_TOP_CHECK_EXIT_STATUS: %s\n' "$fixed_correct_top_rc"
printf 'FIXED_FALSE_KPROVE_EXIT_STATUS_EXPECTED_NONZERO: %s\n' "$fixed_false_rc"
printf 'FIXED_FALSE_STUCK_CHECK_EXIT_STATUS: %s\n' "$fixed_false_stuck_rc"
if (( fixed_correct_rc != 0 || fixed_correct_top_rc != 0 )); then
  overall=1
fi
if (( fixed_false_rc == 0 || fixed_false_stuck_rc != 0 )); then
  overall=1
fi

printf 'COMMAND: cd %s && kompile bridge-witness-extended.k --backend haskell --main-module LOOP-WITNESS-EXTENDED --syntax-module MPY-SYNTAX --output-definition bridge-extended-kompiled\n' "$scratch"
(
  cd "$scratch" || exit 90
  kompile bridge-witness-extended.k \
    --backend haskell \
    --main-module LOOP-WITNESS-EXTENDED \
    --syntax-module MPY-SYNTAX \
    --output-definition bridge-extended-kompiled
)
extended_compile_rc=$?
printf 'EXTENDED_KOMPILE_EXIT_STATUS: %s\n' "$extended_compile_rc"
if (( extended_compile_rc != 0 )); then
  overall=1
fi

if (( extended_compile_rc == 0 )); then
  printf 'COMMAND (false claims should not close in a sound extension): cd %s && kprove bridge-witness-false-spec.k --definition bridge-extended-kompiled --spec-module LOOP-WITNESS-FALSE-SPEC\n' "$scratch"
  (
    cd "$scratch" || exit 90
    set -o pipefail
    kprove bridge-witness-false-spec.k \
      --definition bridge-extended-kompiled \
      --spec-module LOOP-WITNESS-FALSE-SPEC \
      2>&1 | tee bridge-extended-false.stdout
  )
  extended_false_rc=$?
  if rg -x '#Top' "$scratch/bridge-extended-false.stdout" >/dev/null; then
    extended_false_top_rc=0
  else
    extended_false_top_rc=1
  fi
else
  extended_false_rc=99
  extended_false_top_rc=99
fi
printf 'EXTENDED_FALSE_KPROVE_EXIT_STATUS: %s\n' "$extended_false_rc"
printf 'EXTENDED_FALSE_TOP_CHECK_EXIT_STATUS: %s\n' "$extended_false_top_rc"
if (( extended_false_rc != 0 || extended_false_top_rc != 0 )); then
  overall=1
fi

printf 'AUDIT_INTERPRETATION: fixed semantics proves result 2 and rejects 99; proof-local bridges prove the false result 99 for the same integer-list executions.\n'
printf 'EXIT_STATUS: %s\n' "$overall"
exit "$overall"

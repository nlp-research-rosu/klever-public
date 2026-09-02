#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/105-by-length/recon
overall=0

printf 'COMMAND: python3 /audit-output/evidence/make_program_pinning_spec.py\n'
python3 /audit-output/evidence/make_program_pinning_spec.py
pinning_generator_rc=$?
printf 'PINNING_GENERATOR_EXIT_STATUS: %s\n' "$pinning_generator_rc"

if (( pinning_generator_rc == 0 )); then
  printf 'COMMAND: cd %s && kprove program-pinning-spec.k --definition verification-kompiled --spec-module PROGRAM-PINNING-SPEC\n' "$scratch"
  (
    cd "$scratch" || exit 90
    set -o pipefail
    kprove program-pinning-spec.k \
      --definition verification-kompiled \
      --spec-module PROGRAM-PINNING-SPEC \
      2>&1 | tee program-pinning.stdout
  )
  pinning_rc=$?
  if rg -x '#Top' "$scratch/program-pinning.stdout" >/dev/null; then
    pinning_top_rc=0
  else
    pinning_top_rc=1
  fi
else
  pinning_rc=99
  pinning_top_rc=99
fi
printf 'PINNING_KPROVE_EXIT_STATUS: %s\n' "$pinning_rc"
printf 'PINNING_TOP_CHECK_EXIT_STATUS: %s\n' "$pinning_top_rc"
if (( pinning_generator_rc != 0 || pinning_rc != 0 || pinning_top_rc != 0 )); then
  overall=1
fi

printf 'COMMAND: python3 /audit-output/evidence/make_body_mutation.py\n'
python3 /audit-output/evidence/make_body_mutation.py
mutation_generator_rc=$?
printf 'BODY_MUTATION_GENERATOR_EXIT_STATUS: %s\n' "$mutation_generator_rc"
if (( mutation_generator_rc != 0 )); then
  overall=1
fi
cp /audit-output/evidence/body-mutation-spec.k "$scratch/body-mutation-spec.k"

if (( mutation_generator_rc == 0 )); then
  printf 'COMMAND: cd %s && kompile body-mutated-verification.k --backend haskell --main-module BY-LENGTH-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled\n' "$scratch"
  (
    cd "$scratch" || exit 90
    kompile body-mutated-verification.k \
      --backend haskell \
      --main-module BY-LENGTH-VERIFICATION \
      --syntax-module MPY-SYNTAX \
      --output-definition body-mutated-kompiled
  )
  mutation_compile_rc=$?
else
  mutation_compile_rc=99
fi
printf 'BODY_MUTATION_KOMPILE_EXIT_STATUS: %s\n' "$mutation_compile_rc"
if (( mutation_compile_rc != 0 )); then
  overall=1
fi

if (( mutation_compile_rc == 0 )); then
  printf 'COMMAND (expected proof failure): cd %s && kprove body-mutation-spec.k --definition body-mutated-kompiled --spec-module BODY-MUTATION-SPEC\n' "$scratch"
  (
    cd "$scratch" || exit 90
    set -o pipefail
    kprove body-mutation-spec.k \
      --definition body-mutated-kompiled \
      --spec-module BODY-MUTATION-SPEC \
      2>&1 | tee body-mutation.stdout
  )
  mutation_prove_rc=$?
  if rg 'WarnStuckClaimState' "$scratch/body-mutation.stdout" >/dev/null; then
    mutation_stuck_rc=0
  else
    mutation_stuck_rc=1
  fi
else
  mutation_prove_rc=99
  mutation_stuck_rc=99
fi
printf 'BODY_MUTATION_KPROVE_EXIT_STATUS_EXPECTED_NONZERO: %s\n' "$mutation_prove_rc"
printf 'BODY_MUTATION_STUCK_CHECK_EXIT_STATUS: %s\n' "$mutation_stuck_rc"
if (( mutation_prove_rc == 0 || mutation_stuck_rc != 0 )); then
  overall=1
fi

printf 'EXIT_STATUS: %s\n' "$overall"
exit "$overall"

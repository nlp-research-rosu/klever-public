#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/105-by-length/recon
overall=0

printf 'COMMAND: python3 /audit-output/evidence/make_program_pinning_spec.py\n'
python3 /audit-output/evidence/make_program_pinning_spec.py
generator_rc=$?
printf 'PINNING_GENERATOR_EXIT_STATUS: %s\n' "$generator_rc"
if (( generator_rc != 0 )); then
  overall=1
fi

if (( generator_rc == 0 )); then
  printf 'COMMAND: cd %s && kprove program-pinning-spec.k --definition verification-kompiled --spec-module PROGRAM-PINNING-SPEC\n' "$scratch"
  (
    cd "$scratch" || exit 90
    set -o pipefail
    kprove program-pinning-spec.k \
      --definition verification-kompiled \
      --spec-module PROGRAM-PINNING-SPEC \
      2>&1 | tee program-pinning-configured.stdout
  )
  prove_rc=$?
  if rg -x '#Top' "$scratch/program-pinning-configured.stdout" >/dev/null; then
    top_rc=0
  else
    top_rc=1
  fi
else
  prove_rc=99
  top_rc=99
fi
printf 'PINNING_KPROVE_EXIT_STATUS: %s\n' "$prove_rc"
printf 'PINNING_TOP_CHECK_EXIT_STATUS: %s\n' "$top_rc"
if (( prove_rc != 0 || top_rc != 0 )); then
  overall=1
fi
printf 'EXIT_STATUS: %s\n' "$overall"
exit "$overall"

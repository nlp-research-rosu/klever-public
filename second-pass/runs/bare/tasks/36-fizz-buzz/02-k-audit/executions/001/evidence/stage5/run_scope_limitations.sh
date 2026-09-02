#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/semantic-scope
CONCRETE_DEF=/tmp/audit-work/reconstruction/semantic-llvm

run_shell() {
  local command_text="$1"
  printf 'COMMAND: %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  return 0
}

run_shell "mkdir -p '$SCRATCH'"
run_shell "cp /audit-output/evidence/stage5/floor-probe.mpy '$SCRATCH/floor-probe.mpy'"
run_shell "cp /audit-output/evidence/stage5/mod-probe.mpy '$SCRATCH/mod-probe.mpy'"
run_shell "sed -n '1233,1265p' /usr/include/kframework/builtin/domains.md"

printf 'OUT-OF-SUBMITTED-PROGRAM SCOPE PROBE: NEGATIVE FLOOR DIVISION\n'
run_shell "krun '$SCRATCH/floor-probe.mpy' -cN=-3 --definition '$CONCRETE_DEF'"
run_shell "python3 -c \"print('CPYTHON_-3_FLOOR_10:', -3 // 10)\""

printf 'OUT-OF-SUBMITTED-PROGRAM SCOPE PROBE: NEGATIVE MODULUS\n'
run_shell "krun '$SCRATCH/mod-probe.mpy' -cN=-3 --definition '$CONCRETE_DEF'"
run_shell "python3 -c \"print('CPYTHON_-3_MOD_10:', -3 % 10)\""

printf '%s\n' \
  'These probes are not the submitted program.' \
  'They document that SEM-10/SEM-11 are only adequate for the nonnegative' \
  'operands established by the submitted program control flow.'


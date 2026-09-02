#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work
cp /audit-output/evidence/04_pile_module.term pile-module.term

(
  echo 'COMMAND: kast solution.mpy --definition audit-verification-kompiled --module PILE-VERIFICATION --sort Module --expand-macros --output kore > solution.kore'
  kast solution.mpy \
    --definition audit-verification-kompiled \
    --module PILE-VERIFICATION \
    --sort Module \
    --expand-macros \
    --output kore > solution.kore
  status=$?
  echo "EXIT_STATUS: ${status}"
  exit "${status}"
) > /audit-output/evidence/04c_kast_solution.log 2>&1
solution_status=$?

(
  echo 'COMMAND: kast pile-module.term --definition audit-verification-kompiled --module PILE-VERIFICATION --sort Module --expand-macros --output kore > pile-module.kore'
  kast pile-module.term \
    --definition audit-verification-kompiled \
    --module PILE-VERIFICATION \
    --sort Module \
    --expand-macros \
    --output kore > pile-module.kore
  status=$?
  echo "EXIT_STATUS: ${status}"
  exit "${status}"
) > /audit-output/evidence/04d_kast_macro.log 2>&1
macro_status=$?

(
  echo 'COMMAND: cmp -s solution.kore pile-module.kore'
  cmp -s solution.kore pile-module.kore
  status=$?
  echo "EXIT_STATUS: ${status}"
  echo 'COMMAND: sha256sum solution.kore pile-module.kore'
  sha256sum solution.kore pile-module.kore
  hash_status=$?
  echo "EXIT_STATUS(sha256sum): ${hash_status}"
  exit "${status}"
) > /audit-output/evidence/04e_program_pinning_cmp.log 2>&1
cmp_status=$?

echo "solution_kast_status=${solution_status}"
echo "macro_kast_status=${macro_status}"
echo "kore_cmp_status=${cmp_status}"

if (( solution_status != 0 || macro_status != 0 || cmp_status != 0 )); then
  exit 1
fi

#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/31-is-prime-audit
echo 'COMMAND: python3 trusted py2mpy.py k_boundary_tests.py > k_boundary_tests.mpy'
python3 "${work}/py2mpy.py" /audit-output/evidence/k_boundary_tests.py \
  > "${work}/k_boundary_tests.mpy"
translate_status=$?
echo "EXIT_STATUS (translation): ${translate_status}"

echo 'COMMAND: krun k_boundary_tests.mpy --definition fresh runtime-kompiled'
timeout 300 krun "${work}/k_boundary_tests.mpy" \
  --definition "${work}/runtime-kompiled"
run_status=$?
echo "EXIT_STATUS (krun): ${run_status}"

if [[ ${translate_status} -ne 0 || ${run_status} -ne 0 ]]; then exit 1; fi
exit 0

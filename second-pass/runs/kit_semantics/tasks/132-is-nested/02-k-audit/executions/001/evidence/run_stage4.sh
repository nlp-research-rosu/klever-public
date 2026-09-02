#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/132-is-nested-review || exit 90

run_or_stop() {
  echo "\$ $*"
  "$@"
  local status=$?
  echo "EXIT_STATUS: ${status}"
  if [ "${status}" -ne 0 ]; then
    exit "${status}"
  fi
}

echo '$ python3 /audit-output/evidence/extract_spec_program.py > spec-program-module.mpy'
python3 /audit-output/evidence/extract_spec_program.py > spec-program-module.mpy
extract_status=$?
echo "EXIT_STATUS: ${extract_status}"

run_or_stop kast solution.mpy \
  --definition verification-kompiled-fresh \
  --output json \
  --output-file solution.kast.json

run_or_stop kast spec-program-module.mpy \
  --definition verification-kompiled-fresh \
  --output json \
  --output-file spec-program.kast.json

run_or_stop cmp solution.kast.json spec-program.kast.json
run_or_stop sha256sum solution.kast.json spec-program.kast.json
run_or_stop python3 /audit-output/evidence/concrete_claim_substitution.py

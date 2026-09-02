#!/usr/bin/env bash
set -uo pipefail
set -x

krun /tmp/audit-work/pinning/verify-two-spaces.mpy \
  --definition /tmp/audit-work/build/pinning2-kompiled \
  '-cINPUT=""'
fix_witness_status=$?

krun /tmp/audit-work/pinning/verify-drop-two-spaces-a.mpy \
  --definition /tmp/audit-work/build/pinning2-kompiled \
  '-cINPUT=""'
drop_witness_status=$?

python3 -c 'import sys; sys.path.insert(0, "/tmp/audit-work/candidate"); import solution; print("generated fix_spaces two spaces:", repr(solution.fix_spaces("  "))); print("generated _drop_spaces two spaces a:", repr(solution._drop_spaces("  a")))'
generated_python_status=$?

python3 -c 'import sys; sys.path.insert(0, "/tmp/audit-work/reference"); import canonical; print("canonical fix_spaces two spaces:", repr(canonical.fix_spaces("  "))); print("canonical fix_spaces two spaces a:", repr(canonical.fix_spaces("  a")))'
canonical_python_status=$?

set +x
printf 'fix_claim_witness_exit=%s\n' "$fix_witness_status"
printf 'drop_claim_witness_exit=%s\n' "$drop_witness_status"
printf 'generated_python_witness_exit=%s\n' "$generated_python_status"
printf 'canonical_python_witness_exit=%s\n' "$canonical_python_status"

if (( fix_witness_status != 0 ||
      drop_witness_status != 0 ||
      generated_python_status != 0 ||
      canonical_python_status != 0 )); then
  exit 1
fi

#!/usr/bin/env bash
set -uo pipefail
cd /tmp/audit-work

echo 'COMMAND: expand submitted translated module'
echo 'kast submitted-solution.mpy --definition replay-verification-kompiled --module VERIFICATION --expand-macros --output kore'
kast submitted-solution.mpy \
  --definition replay-verification-kompiled \
  --module VERIFICATION \
  --expand-macros \
  --output kore \
  > submitted-expanded.kore
submitted_status=$?
echo "EXIT: $submitted_status"

echo 'COMMAND: expand the claim macro program'
echo 'kast /audit-output/evidence/claim-program.mpy --definition replay-verification-kompiled --module VERIFICATION --expand-macros --output kore'
kast /audit-output/evidence/claim-program.mpy \
  --definition replay-verification-kompiled \
  --module VERIFICATION \
  --expand-macros \
  --output kore \
  > claim-expanded.kore
claim_status=$?
echo "EXIT: $claim_status"

echo 'COMMAND: cmp submitted-expanded.kore claim-expanded.kore'
cmp submitted-expanded.kore claim-expanded.kore
cmp_status=$?
echo "EXIT: $cmp_status"
sha256sum submitted-expanded.kore claim-expanded.kore

exit $((submitted_status || claim_status || cmp_status))

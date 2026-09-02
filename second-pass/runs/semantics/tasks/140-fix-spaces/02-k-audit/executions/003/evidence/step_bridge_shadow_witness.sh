#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/140-fix-spaces/source
cd "$scratch" || exit 90
failures=0

echo '$ fixed semantics must produce result="" and spaces=1'
kprove bridge-shadow-witness.k \
  --definition fresh-proof-base-kompiled \
  --spec-module FIXED-SHADOW-OUTCOME-SPEC
fixed_status=$?
echo "exit=$fixed_status"

echo '$ fixed semantics must reject the candidate bridge conclusion'
kprove bridge-shadow-witness.k \
  --definition fresh-proof-base-kompiled \
  --spec-module BRIDGE-SHADOW-OUTCOME-SPEC
fixed_false_status=$?
echo "exit=$fixed_false_status (nonzero expected)"

echo '$ bridge-enabled semantics proves the false bridge conclusion on the same state'
kprove bridge-shadow-witness.k \
  --definition fresh-proof-main-kompiled \
  --spec-module BRIDGE-SHADOW-OUTCOME-SPEC
bridge_status=$?
echo "exit=$bridge_status"

echo '$ fixed semantics with char=" " and shadow ord=97 takes the non-space branch'
kprove bridge-shadow-witness.k \
  --definition fresh-proof-base-kompiled \
  --spec-module FIXED-SHADOW-SPACE-OUTCOME-SPEC
fixed_space_status=$?
echo "exit=$fixed_space_status"

echo '$ fixed semantics rejects the candidate space-bridge conclusion'
kprove bridge-shadow-witness.k \
  --definition fresh-proof-base-kompiled \
  --spec-module BRIDGE-SHADOW-SPACE-OUTCOME-SPEC
fixed_space_false_status=$?
echo "exit=$fixed_space_false_status (nonzero expected)"

echo '$ bridge-enabled semantics proves the false space-bridge conclusion'
kprove bridge-shadow-witness.k \
  --definition fresh-proof-main-kompiled \
  --spec-module BRIDGE-SHADOW-SPACE-OUTCOME-SPEC
bridge_space_status=$?
echo "exit=$bridge_space_status"

if [ "$fixed_status" -ne 0 ] ||
   [ "$fixed_false_status" -eq 0 ] ||
   [ "$bridge_status" -ne 0 ] ||
   [ "$fixed_space_status" -ne 0 ] ||
   [ "$fixed_space_false_status" -eq 0 ] ||
   [ "$bridge_space_status" -ne 0 ]; then
  failures=1
fi

echo "audit_check_failures=$failures"
exit "$failures"

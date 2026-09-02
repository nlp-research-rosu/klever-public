#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/75-is-multiply-prime/work

# True must short-circuit before the deliberately unsupported Int expression.
krun /audit-output/evidence/short-circuit-true.mpy \
  --definition concrete-kompiled \
  -cARG=0 | tee short-circuit-true.out
rg -U '<result>[[:space:]]*Bool \( true \)[[:space:]]*</result>' \
  short-circuit-true.out

# False must expose the unsupported tail rather than fabricate a Boolean.
set +e
krun /audit-output/evidence/short-circuit-false.mpy \
  --definition concrete-kompiled \
  -cARG=0 2>&1 | tee short-circuit-false.out
false_tail_status=${PIPESTATUS[0]}
set -e
echo "false_tail_exit=${false_tail_status}"
test "${false_tail_status}" -ne 0
rg -U 'evalBool[[:space:]]*\([[:space:]]*Int \( 123 \)' \
  short-circuit-false.out

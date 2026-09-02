#!/usr/bin/env bash
set -euo pipefail
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/35-max-element

test ! -e audit-semantic-kompiled
test ! -e audit-verification-kompiled

kompile semantic.k \
  --backend llvm \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-kompiled

export PYTHONDONTWRITEBYTECODE=1
python3 /audit-output/evidence/concrete_k_compare.py

set +e
krun solution.mpy \
  --definition audit-semantic-kompiled \
  --color off \
  -cARGS='[]' \
  > /audit-output/evidence/stage3-empty-krun.raw.log 2>&1
empty_krun_status=$?
set -e
echo "EMPTY_KRUN_EXIT=$empty_krun_status"
sed -n '1,120p' /audit-output/evidence/stage3-empty-krun.raw.log
test "$empty_krun_status" -ne 0

kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

claim_count=$(rg -c '^[[:space:]]*claim([[:space:]]|$)' spec.k)
echo "POSITIVE_CLAIM_COUNT=$claim_count"
test "$claim_count" -eq 3

set +e
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  > /audit-output/evidence/stage3-positive-kprove.raw.log 2>&1
positive_kprove_status=$?
set -e
echo "POSITIVE_KPROVE_EXIT=$positive_kprove_status"
sed -n '1,160p' /audit-output/evidence/stage3-positive-kprove.raw.log
test "$positive_kprove_status" -eq 0
test "$(tr -d '\r' < /audit-output/evidence/stage3-positive-kprove.raw.log)" = "#Top"

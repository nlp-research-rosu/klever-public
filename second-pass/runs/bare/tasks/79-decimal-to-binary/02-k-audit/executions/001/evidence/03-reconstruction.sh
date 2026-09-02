#!/usr/bin/env bash
set -u

overall=0
run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

run kompile --version
run kprove --version
run krun --version
run test ! -e /tmp/audit-work/build-concrete/concrete-kompiled
run test ! -e /tmp/audit-work/build-proof/verification-kompiled

run kompile \
  /tmp/audit-work/build-concrete/semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/build-concrete/concrete-kompiled

run kompile \
  /tmp/audit-work/build-proof/verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/build-proof/verification-kompiled

run python3 /audit-output/evidence/split_claims.py

for number in 1 2 3 4 5; do
  run kprove \
    "/tmp/audit-work/build-proof/spec-claim-${number}.k" \
    --definition /tmp/audit-work/build-proof/verification-kompiled \
    --spec-module "AUDIT-SPEC-CLAIM-${number}"
done

run kprove \
  /tmp/audit-work/build-proof/spec.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module SPEC

run python3 /audit-output/evidence/concrete_compare.py

printf '[script exit %d]\n' "$overall"
exit "$overall"

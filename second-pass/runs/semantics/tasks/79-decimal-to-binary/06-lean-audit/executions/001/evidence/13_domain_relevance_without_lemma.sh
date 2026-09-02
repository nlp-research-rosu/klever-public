#!/usr/bin/env bash
set -euo pipefail

audit_no_domain_dir=/tmp/audit-work/k-no-domain
cd "$audit_no_domain_dir"

echo '$ diff -u /reference/k-proof/verification.k /tmp/audit-work/k-no-domain/verification.k'
diff -u /reference/k-proof/verification.k verification.k || true

echo '$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

echo '$ kprove spec.k --definition verification-kompiled --spec-module SPEC --output pretty'
set +e
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty
audit_kprove_code=$?
set -e
echo "kprove_exit_code=$audit_kprove_code"
if [[ "$audit_kprove_code" -eq 0 ]]; then
  echo 'unexpected success without the classified domain lemma' >&2
  exit 96
fi
echo 'EXPECTED_FAILURE_WITHOUT_DOMAIN_LEMMA = PASS'

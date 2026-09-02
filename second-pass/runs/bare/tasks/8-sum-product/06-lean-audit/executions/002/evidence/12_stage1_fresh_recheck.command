set -euo pipefail
audit_work=$(mktemp -d /tmp/audit-work/stage1-recheck.XXXXXX)
printf 'workdir=%s\n' "$audit_work"
cp /reference/k-proof/semantic.k "$audit_work/semantic.k"
cp /reference/k-proof/verification.k "$audit_work/verification.k"
cp /reference/k-proof/spec.k "$audit_work/spec.k"
cd "$audit_work"
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SUM-PRODUCT-SPEC

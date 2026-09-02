#!/usr/bin/env bash
set -euo pipefail

fixed=/audit-output/evidence/fixed-concrete-configuration.out
extended=/audit-output/evidence/extended-concrete-configuration.out

krun /tmp/audit-work/concrete-audit.mpy \
  --definition /tmp/audit-work/src/audit-runtime-kompiled \
  > "$fixed"

krun /tmp/audit-work/concrete-audit.mpy \
  --definition /tmp/audit-work/src/audit-verification-kompiled \
  > "$extended"

cmp "$fixed" "$extended"
sha256sum "$fixed" "$extended"
printf 'FIXED_VS_PROOF_EXTENDED_CONFIGURATION=BYTE_IDENTICAL\n'

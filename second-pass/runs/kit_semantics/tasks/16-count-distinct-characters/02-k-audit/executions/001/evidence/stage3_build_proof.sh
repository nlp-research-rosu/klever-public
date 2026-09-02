#!/usr/bin/env bash
set -u
set -o pipefail

exec > >(tee /audit-output/evidence/stage3-build-proof.log) 2>&1
set -x

cd /tmp/audit-work/reconstruction || exit 90

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
build_status=$?
printf 'fresh_haskell_kompile_exit=%d\n' "$build_status"

exit "$build_status"

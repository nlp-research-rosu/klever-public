#!/usr/bin/env bash
set -uo pipefail
PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cd /tmp/audit-work/34-unique

kompile candidate-source/semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition concrete-kompiled
concrete_status=$?

kompile candidate-source/verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition proof-kompiled
proof_status=$?

set +x
printf 'CONCRETE_BUILD_EXIT_STATUS=%s\n' "$concrete_status"
printf 'PROOF_BUILD_EXIT_STATUS=%s\n' "$proof_status"
if (( concrete_status || proof_status )); then
  exit 1
fi
exit 0

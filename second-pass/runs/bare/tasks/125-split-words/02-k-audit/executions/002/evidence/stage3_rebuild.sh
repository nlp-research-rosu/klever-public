#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/candidate
cd "$work" || exit 1

echo 'COMMAND: find /tmp/audit-work/candidate -maxdepth 1 -name "*-kompiled" -print'
find "$work" -maxdepth 1 -name '*-kompiled' -print
find_status=$?
echo "EXIT_STATUS: $find_status"

if [[ -e concrete-kompiled || -e proof-kompiled ]]; then
  echo 'ERROR: fresh output definition path unexpectedly exists'
  exit 1
fi

echo 'COMMAND: kompile verification.k --backend llvm --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition concrete-kompiled'
kompile verification.k \
  --backend llvm \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
llvm_status=$?
echo "EXIT_STATUS: $llvm_status"
if (( llvm_status != 0 )); then
  exit "$llvm_status"
fi

echo 'COMMAND: kompile verification.k --backend haskell --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
haskell_status=$?
echo "EXIT_STATUS: $haskell_status"
exit "$haskell_status"

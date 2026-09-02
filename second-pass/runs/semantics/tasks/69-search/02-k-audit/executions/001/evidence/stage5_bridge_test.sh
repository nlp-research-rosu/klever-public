#!/usr/bin/env bash
set -u

overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
}

printf '\nFixed-semantics concrete witness (expected to return 2, never 99):\n'
run bash -o pipefail -c \
  'python3 /reference/py2mpy.py /audit-output/evidence/bridge_context.py > /tmp/audit-work/69-search/bridge-context.mpy'
run /usr/bin/krun bridge-context.mpy --definition runtime-kompiled --output none

printf '\nFalse claim with candidate bridge enabled (unsoundly expected to close):\n'
run /usr/bin/kprove \
  bridge-unsound-spec.k \
  --definition verification-kompiled \
  --spec-module BRIDGE-UNSOUND-SPEC

printf '\nRebuild identical proof source with only the bridge removed:\n'
run /usr/bin/kompile \
  verification-no-bridge.k \
  --backend haskell \
  --main-module SEARCH-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-no-bridge-kompiled

printf '\nSame false claim without bridge (expected meaningful proof failure):\n'
printf '$ /usr/bin/kprove bridge-unsound-no-bridge-spec.k --definition verification-no-bridge-kompiled --spec-module BRIDGE-UNSOUND-NO-BRIDGE-SPEC\n'
/usr/bin/kprove \
  bridge-unsound-no-bridge-spec.k \
  --definition verification-no-bridge-kompiled \
  --spec-module BRIDGE-UNSOUND-NO-BRIDGE-SPEC \
  2>&1 | tee /audit-output/evidence/stage5_no_bridge_failure.log
status=${PIPESTATUS[0]}
printf '[exit %d; nonzero expected]\n' "$status"
if (( status == 0 )); then
  printf 'ERROR: fixed semantics proved the false claim\n'
  overall=1
fi
if ! rg -q 'WarnStuckClaimState|implication check.*failed|cannot be rewritten further' \
     /audit-output/evidence/stage5_no_bridge_failure.log; then
  printf 'ERROR: expected unmet-obligation diagnostic absent\n'
  overall=1
fi

exit "$overall"

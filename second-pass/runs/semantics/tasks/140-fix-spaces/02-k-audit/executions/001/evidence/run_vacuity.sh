#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
scratch=/tmp/audit-work/140-fix-spaces
log=/audit-output/evidence/vacuity.log

cd "$scratch" || exit 2

{
  printf '$ kprove spec-vacuity.k --definition proof-main-kompiled --spec-module FIX-SPACES-MAIN-VACUITY\n'
} > "$log"
kprove spec-vacuity.k \
  --definition proof-main-kompiled \
  --spec-module FIX-SPACES-MAIN-VACUITY >> "$log" 2>&1
status=$?
printf '[exit %d; expected nonzero]\n' "$status" >> "$log"
printf 'vacuity_exit=%d expected=nonzero\n' "$status"

if [[ "$status" -eq 0 ]]; then
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$log"; then
  exit 2
fi
exit 0

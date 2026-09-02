#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/candidate-src/proof-kompiled
submitted=/tmp/audit-work/candidate-src/solution.mpy
claimed=/audit-output/evidence/04_claim-program.mpy

printf '%s\n' '$ kast --definition "$definition" "$submitted" --output kast > /tmp/audit-work/submitted.kast'
kast --definition "$definition" "$submitted" --output kast \
  > /tmp/audit-work/submitted.kast
printf '[exit %d]\n' "$?"

printf '%s\n' '$ kast --definition "$definition" "$claimed" --output kast > /tmp/audit-work/claimed.kast'
kast --definition "$definition" "$claimed" --output kast \
  > /tmp/audit-work/claimed.kast
printf '[exit %d]\n' "$?"

printf '%s\n' '$ cmp -s /tmp/audit-work/submitted.kast /tmp/audit-work/claimed.kast'
cmp -s /tmp/audit-work/submitted.kast /tmp/audit-work/claimed.kast
printf '[exit %d]\n' "$?"

printf '%s\n' '$ sha256sum /tmp/audit-work/submitted.kast /tmp/audit-work/claimed.kast'
sha256sum /tmp/audit-work/submitted.kast /tmp/audit-work/claimed.kast
printf '[exit %d]\n' "$?"

printf '%s\n' '$ sed -n 1,80p /tmp/audit-work/submitted.kast'
sed -n '1,80p' /tmp/audit-work/submitted.kast
printf '[exit %d]\n' "$?"

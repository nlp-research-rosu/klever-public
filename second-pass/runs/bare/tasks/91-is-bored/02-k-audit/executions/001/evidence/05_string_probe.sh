#!/usr/bin/env bash
set -u

work=/tmp/audit-work/string-probe
status=0

printf '%s\n' 'COMMAND: mkdir -p /tmp/audit-work/string-probe'
mkdir -p "$work"
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || exit 1

if [[ ! -d "$work/string-probe-kompiled" ]]; then
  printf '%s\n' 'COMMAND: timeout 120s kompile /audit-output/evidence/string-probe.k --backend haskell --syntax-module STRING-PROBE-SYNTAX --main-module STRING-PROBE --output-definition /tmp/audit-work/string-probe/string-probe-kompiled'
  timeout 120s kompile /audit-output/evidence/string-probe.k \
    --backend haskell \
    --syntax-module STRING-PROBE-SYNTAX \
    --main-module STRING-PROBE \
    --output-definition "$work/string-probe-kompiled"
  code=$?
  printf 'EXIT: %s\n' "$code"
  (( code == 0 )) || status=1
else
  printf '%s\n' 'REUSE: reviewer-built /tmp/audit-work/string-probe/string-probe-kompiled'
fi

for term in 'Probe("AI")' 'Probe("\u00a0I")' 'Probe("\u2003I")'; do
  printf 'COMMAND: krun term=%s --definition string-probe-kompiled\n' "$term"
  krun --definition "$work/string-probe-kompiled" -cPGM="$term"
  code=$?
  printf 'EXIT: %s\n' "$code"
  (( code == 0 )) || status=1
done

exit "$status"

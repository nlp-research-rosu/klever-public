#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

source_dir=/tmp/audit-work/11-string-xor/source
definition=/tmp/audit-work/11-string-xor/build/bridge-free-kompiled

echo 'COMMAND: bash /audit-output/evidence/05_bridge_free_identity.sh'
echo 'COMMAND: confirm bridge-free definition has no exec shortcut, priority, or prependResult'
if rg -n 'priority|prependResult|^[[:space:]]*rule exec' "$source_dir/bridge-free.k"; then
  echo 'ERROR: bridge-free definition contains an operational acceleration'
  exit 1
fi
echo 'operational_accelerations_present=false'

echo 'COMMAND: expand solutionProgramCore to KORE and compare with submitted solution.mpy KORE'
kast \
  --definition "$definition" \
  --module XOR-BRIDGE-FREE \
  --sort Module \
  --expand-macros \
  --output kore \
  --expression solutionProgramCore \
  > /tmp/audit-work/11-string-xor/bridge-free-program.kore
kast \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  "$source_dir/solution.mpy" \
  > /tmp/audit-work/11-string-xor/bridge-free-submitted.kore
cmp \
  /tmp/audit-work/11-string-xor/bridge-free-program.kore \
  /tmp/audit-work/11-string-xor/bridge-free-submitted.kore
sha256sum \
  /tmp/audit-work/11-string-xor/bridge-free-program.kore \
  /tmp/audit-work/11-string-xor/bridge-free-submitted.kore
echo 'bridge_free_constructor_level_program_identity=true'

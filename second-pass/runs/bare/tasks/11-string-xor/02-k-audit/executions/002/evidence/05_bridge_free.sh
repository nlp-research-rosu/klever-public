#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

source_dir=/tmp/audit-work/11-string-xor/source
definition=/tmp/audit-work/11-string-xor/build/bridge-free-kompiled

echo 'COMMAND: bash /audit-output/evidence/05_bridge_free.sh'
echo 'COMMAND: kompile bridge-free.k --main-module XOR-BRIDGE-FREE --syntax-module MPY-SYNTAX --backend haskell --output-definition /tmp/audit-work/11-string-xor/build/bridge-free-kompiled'
kompile "$source_dir/bridge-free.k" \
  --main-module XOR-BRIDGE-FREE \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "$definition"

cd "$source_dir"
echo 'COMMAND: kprove spec-bridge-free.k --spec-module XOR-BRIDGE-FREE-SPEC --definition /tmp/audit-work/11-string-xor/build/bridge-free-kompiled --output pretty'
kprove spec-bridge-free.k \
  --spec-module XOR-BRIDGE-FREE-SPEC \
  --definition "$definition" \
  --output pretty

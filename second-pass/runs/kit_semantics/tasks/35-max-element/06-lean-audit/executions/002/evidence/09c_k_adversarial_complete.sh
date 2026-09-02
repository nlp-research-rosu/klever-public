#!/usr/bin/env bash
set -euo pipefail
set -x

definition=/tmp/audit-work/max-float-test-repro-kompiled
test ! -e "$definition"
kompile /audit-output/evidence/max-float-test.k \
  --backend llvm \
  --main-module MAX-FLOAT-TEST \
  --syntax-module MAX-FLOAT-TEST-SYNTAX \
  --output-definition "$definition"
krun --definition "$definition" -cPGM=nanLeft
krun --definition "$definition" -cPGM=nanRight

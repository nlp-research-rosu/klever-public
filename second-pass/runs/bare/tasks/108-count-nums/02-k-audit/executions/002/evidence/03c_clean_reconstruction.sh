#!/usr/bin/env bash
set -eu
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT_STATUS=%s\n" "$status"' EXIT
set -x

REBUILD=/tmp/audit-work/108-count-nums-clean-rebuild
test ! -e "$REBUILD"
mkdir "$REBUILD"
cp /candidate/solution.py "$REBUILD/solution.py"
cp /candidate/solution.mpy "$REBUILD/solution.submitted.mpy"
cp /candidate/semantic.k "$REBUILD/semantic.k"
cp /candidate/verification.k "$REBUILD/verification.k"
cp /candidate/spec.k "$REBUILD/spec.k"
cp /reference/py2mpy.py "$REBUILD/py2mpy.py"
cd "$REBUILD"

python3 py2mpy.py solution.py > solution.mpy
cmp solution.submitted.mpy solution.mpy
test ! -e semantic-kompiled
test ! -e verification-kompiled

kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled

krun solution.mpy --definition semantic-kompiled -cARG='list()' \
  | grep -F 'IntV ( 0 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0
krun solution.mpy --definition semantic-kompiled -cARG='list(-1, 11, -11)' \
  | grep -F 'IntV ( 1 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0
krun solution.mpy --definition semantic-kompiled \
  -cARG='list(-123, -100, -99, 0, 10)' \
  | grep -F 'IntV ( 2 ) ~> .K'
test "${PIPESTATUS[0]}" -eq 0

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

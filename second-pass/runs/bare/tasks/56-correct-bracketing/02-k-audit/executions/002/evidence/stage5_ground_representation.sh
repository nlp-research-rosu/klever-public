#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/proof || exit 90

printf 'COMMAND: kompile seq-test-definition.k --backend llvm --main-module SEQ-TEST --syntax-module SEQ-TEST-SYNTAX --output-definition seq-test-llvm-kompiled\n'
kompile seq-test-definition.k \
  --backend llvm \
  --main-module SEQ-TEST \
  --syntax-module SEQ-TEST-SYNTAX \
  --output-definition seq-test-llvm-kompiled
build_exit=$?
printf 'surrogate test definition kompile exit=%s\n' "$build_exit"
if (( build_exit != 0 )); then
  exit 1
fi

python3 /audit-output/evidence/ground_representation_test.py
test_exit=$?
printf 'ground representation test exit=%s\n' "$test_exit"
exit "$test_exit"

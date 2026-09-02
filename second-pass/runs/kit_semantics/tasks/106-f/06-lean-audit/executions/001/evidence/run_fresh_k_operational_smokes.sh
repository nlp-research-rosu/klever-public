#!/usr/bin/env bash
set -u

output=/tmp/audit-work/k-runtime-106f

echo '$ kompile --backend llvm /reference/k-proof/reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/k-runtime-106f'
kompile --backend llvm \
  /reference/k-proof/reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$output"
compile_status=$?
echo "kompile_exit=$compile_status"
test "$compile_status" -eq 0 || exit "$compile_status"

for input in \
  /audit-output/evidence/k-smoke-negative-3.mpy \
  /audit-output/evidence/k-smoke-zero.mpy \
  /audit-output/evidence/k-smoke-five.mpy \
  /audit-output/evidence/k-smoke-body-mutation-total-100.mpy
do
  echo "\$ krun $input --definition $output --output pretty"
  krun "$input" --definition "$output" --output pretty
  run_status=$?
  echo "krun_exit=$run_status"
  test "$run_status" -eq 0 || exit "$run_status"
done

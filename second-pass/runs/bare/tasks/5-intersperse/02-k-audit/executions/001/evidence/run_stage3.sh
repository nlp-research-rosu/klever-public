#!/usr/bin/env bash
set -u

log="/audit-output/evidence/stage3-reconstruction.log"
scratch="/tmp/audit-work/reconstruction"
exec >"$log" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run rm -rf "$scratch/semantic-fresh-kompiled"
run rm -rf "$scratch/verification-fresh-kompiled"
run kompile "$scratch/semantic.k" --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition "$scratch/semantic-fresh-kompiled"
for input in run-empty.mpy run-single.mpy run-pair.mpy run-example.mpy run-negative.mpy; do
  run krun "$scratch/$input" --definition "$scratch/semantic-fresh-kompiled"
done
run bash -c 'cd /tmp/audit-work/reconstruction && python3 -c '"'"'import solution; cases=[([],4),([7],99),([7,8],99),([1,2,3],4),([-1,2,-3,4],-9)]; print([(xs,d,solution.intersperse(xs,d)) for xs,d in cases])'"'"
run kompile "$scratch/verification.k" --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition "$scratch/verification-fresh-kompiled"
run kprove "$scratch/spec.k" --definition "$scratch/verification-fresh-kompiled" --spec-module SPEC

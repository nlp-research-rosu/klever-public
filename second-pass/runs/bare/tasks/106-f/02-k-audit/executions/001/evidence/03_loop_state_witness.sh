#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/106-f
source_dir="$work/source"
definition="$work/build/audit-loop-witness-kompiled"
evidence=/audit-output/evidence
export PATH="$HOME/.nix-profile/bin:$PATH"

if [ -e "$definition" ]; then
  echo 'FRESHNESS_FAILURE: audit-loop-witness-kompiled already exists'
  exit 98
fi

echo 'COMMAND: build reachable loop-state witness harness'
(
  cd "$source_dir" &&
  kompile audit-loop-witness.k \
    --main-module AUDIT-LOOP-WITNESS \
    --syntax-module AUDIT-LOOP-WITNESS \
    --backend llvm \
    --output-definition "$definition"
) 2>&1 | tee "$evidence/03_kompile_loop_witness.log"
build_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $build_status" | tee -a "$evidence/03_kompile_loop_witness.log"
if [ "$build_status" -ne 0 ]; then
  exit "$build_status"
fi

echo 'COMMAND: execute real solutionLoop from I=3,N=5,F=2,T=3,L=[1,2]'
(
  cd "$source_dir" &&
  krun loop-state-witness.mpy \
    -cINPUT=5 \
    --definition "$definition" \
    --output pretty
) 2>&1 | tee "$evidence/03_loop_state_witness_krun.log"
run_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $run_status" | tee -a "$evidence/03_loop_state_witness_krun.log"
exit "$run_status"

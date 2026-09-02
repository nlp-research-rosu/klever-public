#!/usr/bin/env bash
set -u

log="/audit-output/evidence/stage6-nonvacuity.log"
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

run sed -n 1,240p "$scratch/spec-vacuity.k"
run kprove "$scratch/spec-vacuity.k" --definition "$scratch/verification-fresh-kompiled" --spec-module SPEC-VACUITY --dry-run
run kprove "$scratch/spec-vacuity.k" --definition "$scratch/verification-fresh-kompiled" --spec-module SPEC-VACUITY
run krun "$scratch/run-pair.mpy" --definition "$scratch/semantic-fresh-kompiled"
run bash -c 'cd /tmp/audit-work/reconstruction && python3 -c '"'"'import canonical, solution; x=[7,8]; d=99; print("witness_input=",x,"delimiter=",d,"mutated_claim_result=",[7,100,8],"canonical=",canonical.intersperse(list(x),d),"solution=",solution.intersperse(list(x),d))'"'"

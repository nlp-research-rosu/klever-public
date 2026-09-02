#!/usr/bin/env bash
set -u

log="/audit-output/evidence/stage4-pinning.log"
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

run python3 /audit-output/evidence/program_pinning.py
run kast "$scratch/solution.mpy" --definition "$scratch/verification-fresh-kompiled" --module MPY-SYNTAX --sort Pgm --output kore --output-file /audit-output/evidence/submitted-program.kore
run rm -rf /tmp/audit-work/kprove-pinning
run mkdir -p /tmp/audit-work/kprove-pinning
run kprove "$scratch/spec.k" --definition "$scratch/verification-fresh-kompiled" --spec-module SPEC --dry-run --temp-dir /tmp/audit-work/kprove-pinning
run bash -c 'cp /tmp/audit-work/kprove-pinning/.kprove-*/spec.kore /audit-output/evidence/spec-dry-run.kore'
run python3 /audit-output/evidence/kore_pinning.py
run rg -n '^[[:space:]]*claim([[:space:]]|$)' "$scratch/spec.k"
run kprove "$scratch/spec-ground.k" --definition "$scratch/verification-fresh-kompiled" --spec-module SPEC-GROUND
run bash -c 'cd /tmp/audit-work/reconstruction && python3 -c '"'"'import canonical, solution; x=[7,8]; d=99; print("input=",x,"delimiter=",d,"spec_result=",[7,99,8],"canonical=",canonical.intersperse(list(x),d),"solution=",solution.intersperse(list(x),d))'"'"

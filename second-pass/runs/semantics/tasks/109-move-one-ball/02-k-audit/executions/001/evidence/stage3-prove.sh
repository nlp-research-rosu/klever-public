#!/usr/bin/env bash
set +e

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n\n' "$status"
  return "$status"
}

cd /tmp/audit-work/109-move-one-ball/candidate || exit 90
export PATH="$HOME/.nix-profile/bin:$PATH"

run kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.move-one-ball-loop-induction \
  --output pretty
induction_status=$?

run kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.move-one-ball-loop-induction,SPEC.move-one-ball-loop-entry \
  --output pretty
entry_with_dependency_status=$?

run kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.move-one-ball-loop-induction,SPEC.move-one-ball-loop-entry,SPEC.move-one-ball-correct \
  --output pretty
correct_with_dependencies_status=$?

printf 'loop_induction_status=%d\n' "$induction_status"
printf 'loop_entry_with_dependency_status=%d\n' "$entry_with_dependency_status"
printf 'correct_with_dependencies_status=%d\n' "$correct_with_dependencies_status"
if (( induction_status != 0 || entry_with_dependency_status != 0 || correct_with_dependencies_status != 0 )); then
  exit 1
fi

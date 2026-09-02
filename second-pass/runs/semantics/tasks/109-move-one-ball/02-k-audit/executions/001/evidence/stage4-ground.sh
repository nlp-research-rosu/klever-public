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

run python3 -c 'from solution import move_one_ball; print(move_one_ball([]), move_one_ball([3,4,5,1,2]), move_one_ball([3,5,4,1,2]))'
candidate_status=$?

run python3 -c 'import importlib.util; s=importlib.util.spec_from_file_location("canonical","/reference/canonical.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.move_one_ball([]), m.move_one_ball([3,4,5,1,2]), m.move_one_ball([3,5,4,1,2]))'
canonical_status=$?

run kprove spec-ground-adequacy.k \
  --definition verification-kompiled \
  --spec-module SPEC-GROUND-ADEQUACY \
  --output pretty
k_status=$?

printf 'candidate_python_status=%d\n' "$candidate_status"
printf 'canonical_python_status=%d\n' "$canonical_status"
printf 'ground_k_status=%d\n' "$k_status"
if (( candidate_status != 0 || canonical_status != 0 || k_status != 0 )); then
  exit 1
fi

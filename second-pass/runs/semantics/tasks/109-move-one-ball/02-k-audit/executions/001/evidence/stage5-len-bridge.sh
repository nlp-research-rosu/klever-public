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

run python3 -c 'print(len([10, 20]), len([10, 20]) == 1)'
python_status=$?

run kprove spec-len-bridge-witness.k \
  --definition verification-kompiled \
  --spec-module SPEC-LEN-BRIDGE-WITNESS \
  --output pretty
witness_status=$?

run kprove spec-len-bridge-opposite.k \
  --definition verification-kompiled \
  --spec-module SPEC-LEN-BRIDGE-OPPOSITE \
  --output pretty
opposite_status=$?

printf 'python_status=%d\n' "$python_status"
printf 'false_conclusion_witness_status=%d\n' "$witness_status"
printf 'opposite_expected_result_status=%d\n' "$opposite_status"

if (( python_status != 0 || witness_status != 0 || opposite_status == 0 )); then
  exit 1
fi

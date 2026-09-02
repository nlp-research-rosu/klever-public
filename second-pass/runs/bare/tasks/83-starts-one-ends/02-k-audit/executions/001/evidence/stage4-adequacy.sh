#!/usr/bin/env bash
set -u

work=/tmp/audit-work/review-83
status=0

echo "command: cp /audit-output/evidence/adequacy-ground.k $work/adequacy-ground.k"
cp /audit-output/evidence/adequacy-ground.k "$work/adequacy-ground.k"
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

cd "$work" || exit 99
for claim in ADEQUACY-GROUND.witness-n-one ADEQUACY-GROUND.witness-n-two; do
  echo "command: kprove adequacy-ground.k --definition fresh-verification-kompiled --spec-module ADEQUACY-GROUND --claims $claim"
  output=$(kprove adequacy-ground.k \
    --definition fresh-verification-kompiled \
    --spec-module ADEQUACY-GROUND \
    --claims "$claim" 2>&1)
  rc=$?
  printf '%s\n' "$output"
  echo "exit: $rc"
  if (( rc == 0 )) && grep -Fxq '#Top' <<<"$output"; then
    echo "ground claim result: CLOSED"
  else
    echo "ground claim result: NOT CLOSED"
    status=1
  fi
done

echo "command: python3 /audit-output/evidence/ground_witness.py"
python3 /audit-output/evidence/ground_witness.py
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "script_exit: $status"
exit "$status"

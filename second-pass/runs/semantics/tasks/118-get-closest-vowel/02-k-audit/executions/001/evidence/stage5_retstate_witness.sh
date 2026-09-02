#!/usr/bin/env bash
set -u

cd /tmp/audit-work/run-118 || exit 70
cp /audit-output/evidence/bridge-retstate-witness.k .
cp /audit-output/evidence/bridge-retstate-witness-no-bridge.k .
overall=0
counter=100

run_bounded() {
  counter=$((counter + 1))
  out="/tmp/audit-work/run-118/.audit-command-${counter}.log"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$out" 2>&1
  rc=$?
  lines=$(wc -l <"$out")
  printf '[output lines %d]\n' "$lines"
  if (( lines <= 220 )); then
    sed -n '1,220p' "$out"
  else
    sed -n '1,150p' "$out"
    printf '[... %d lines omitted ...]\n' "$((lines - 220))"
    tail -n 70 "$out"
  fi
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

echo '== Candidate bridge fabricates a result with an already-pending return =='
run_bounded kprove bridge-retstate-witness.k \
  --definition audit-proof-kompiled \
  --spec-module AUDIT-BRIDGE-RETSTATE
bridge_rc=$?
if (( bridge_rc != 0 )); then
  echo 'UNEXPECTED: exact bridge witness did not close'
  overall=1
fi

echo '== Supplied execution without the bridge cannot reach that result =='
run_bounded kprove bridge-retstate-witness-no-bridge.k \
  --definition audit-no-bridge-v2-kompiled \
  --spec-module AUDIT-BRIDGE-RETSTATE-NO-BRIDGE
fixed_rc=$?
if (( fixed_rc == 0 )); then
  echo 'UNEXPECTED: bridge-free execution reached the fabricated result'
  overall=1
else
  echo 'EXPECTED: bridge-free execution is stuck with retV(7), not at str(.IntSeq)'
fi

exit "$overall"

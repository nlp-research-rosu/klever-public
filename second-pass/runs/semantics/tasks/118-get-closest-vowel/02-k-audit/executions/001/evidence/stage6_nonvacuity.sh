#!/usr/bin/env bash
set -u

cd /tmp/audit-work/run-118 || exit 70
cp /audit-output/evidence/spec-vacuity.k ./spec-vacuity.k
overall=0
counter=80

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
  if (( lines <= 240 )); then
    sed -n '1,240p' "$out"
  else
    sed -n '1,160p' "$out"
    printf '[... %d lines omitted ...]\n' "$((lines - 240))"
    tail -n 80 "$out"
  fi
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

echo '== The false claim parses and lowers successfully =='
run_bounded kprove spec-vacuity.k \
  --definition audit-proof-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run
dry_rc=$?
if (( dry_rc != 0 )); then
  echo 'ERROR: false mutation did not build'
  overall=1
fi

echo '== The reachable false result obligation must be rejected =='
run_bounded kprove spec-vacuity.k \
  --definition audit-proof-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
proof_rc=$?
if (( proof_rc == 0 )); then
  echo 'ERROR: false mutation unexpectedly closed'
  overall=1
else
  echo 'EXPECTED: false result mutation failed after successful lowering'
fi

exit "$overall"

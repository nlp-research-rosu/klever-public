#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/04_generate_reachable_slice_cases.py > /tmp/audit-work/slice-reachable.k\n'
python3 /audit-output/evidence/04_generate_reachable_slice_cases.py \
  > /tmp/audit-work/slice-reachable.k
generate_rc=$?
printf '[exit %d]\n' "$generate_rc"
if (( generate_rc != 0 )); then
  exit "$generate_rc"
fi

printf '$ cp -a /tmp/audit-work/slice-reachable.k /audit-output/evidence/04_slice_reachable.k\n'
cp -a \
  /tmp/audit-work/slice-reachable.k \
  /audit-output/evidence/04_slice_reachable.k
copy_rc=$?
printf '[exit %d]\n' "$copy_rc"
if (( copy_rc != 0 )); then
  exit "$copy_rc"
fi

printf '$ kprove /tmp/audit-work/slice-reachable.k --definition /tmp/audit-work/base-semantics-kompiled --spec-module SLICE-REACHABLE --output pretty\n'
kprove /tmp/audit-work/slice-reachable.k \
  --definition /tmp/audit-work/base-semantics-kompiled \
  --spec-module SLICE-REACHABLE \
  --output pretty
prove_rc=$?
printf '[exit %d]\n' "$prove_rc"
exit "$prove_rc"

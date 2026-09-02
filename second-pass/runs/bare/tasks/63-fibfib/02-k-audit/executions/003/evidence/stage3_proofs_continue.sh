#!/usr/bin/env bash
set -u

candidate_src=/tmp/audit-work/63-fibfib/candidate-src
evidence=/audit-output/evidence
overall=0
cd "$candidate_src" || exit 125

printf '%s\n' \
  'COMMAND: timeout 120s kprove spec.k --definition proof-kompiled --spec-module FIBFIB-SPEC --claims FIBFIB-SPEC.loop-invariant -w none'
loop_log="$evidence/stage3_kprove_loop-invariant.log"
timeout 120s kprove spec.k \
  --definition proof-kompiled \
  --spec-module FIBFIB-SPEC \
  --claims FIBFIB-SPEC.loop-invariant \
  -w none >"$loop_log" 2>&1
loop_status=$?
printf 'EXIT: %s\n' "$loop_status"
sed -n '1,320p' "$loop_log"
if (( loop_status != 0 )) || ! grep -qx '#Top' "$loop_log"; then overall=1; fi

printf '%s\n' \
  'COMMAND: timeout 120s kprove spec.k --definition proof-kompiled --spec-module FIBFIB-SPEC -w none'
all_log="$evidence/stage3_kprove_all.log"
timeout 120s kprove spec.k \
  --definition proof-kompiled \
  --spec-module FIBFIB-SPEC \
  -w none >"$all_log" 2>&1
all_status=$?
printf 'EXIT: %s\n' "$all_status"
sed -n '1,320p' "$all_log"
if (( all_status != 0 )) || ! grep -qx '#Top' "$all_log"; then overall=1; fi

printf 'STAGE3_PROOFS_EXIT: %s\n' "$overall"
exit "$overall"

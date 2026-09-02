#!/usr/bin/env bash
set -uo pipefail
cd /tmp/audit-work

echo 'COMMAND: independent loop claim'
echo 'kprove spec.k --definition replay-verification-kompiled --spec-module SPEC --claims SPEC.filter-loop'
kprove spec.k \
  --definition replay-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.filter-loop
loop_status=$?
echo "EXIT: $loop_status"

echo 'COMMAND: aggregate target proof, no trust flag'
echo 'kprove spec.k --definition replay-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition replay-verification-kompiled \
  --spec-module SPEC
aggregate_status=$?
echo "EXIT: $aggregate_status"

echo 'COMMAND: entry isolation composed with the independently proved loop claim'
echo 'kprove spec.k --definition replay-verification-kompiled --spec-module SPEC --claims SPEC.filter-loop,SPEC.special-filter --trusted SPEC.filter-loop'
kprove spec.k \
  --definition replay-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.filter-loop,SPEC.special-filter \
  --trusted SPEC.filter-loop
entry_status=$?
echo "EXIT: $entry_status"

echo 'COMMAND: ground satisfying witnesses'
echo 'kprove spec-ground.k --definition replay-verification-kompiled --spec-module SPEC-GROUND'
kprove spec-ground.k \
  --definition replay-verification-kompiled \
  --spec-module SPEC-GROUND
ground_status=$?
echo "EXIT: $ground_status"

exit $((loop_status || aggregate_status || entry_status || ground_status))

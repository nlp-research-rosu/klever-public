#!/usr/bin/env bash
set -u
set -o pipefail
set -x

evidence=/audit-output/evidence
overall=0

grep -q 'NoExc' "$evidence/stage3_concrete_krun.log"
status=$?
printf 'CONCRETE_NOEXC_CHECK_EXIT=%s\n' "$status"
(( status == 0 )) || overall=1

grep -qx '#Top' "$evidence/stage3_loop_proof.log"
status=$?
printf 'LOOP_TOP_CHECK_EXIT=%s\n' "$status"
(( status == 0 )) || overall=1

grep -qx '#Top' "$evidence/stage3_call_proof.log"
status=$?
printf 'CALL_TOP_CHECK_EXIT=%s\n' "$status"
(( status == 0 )) || overall=1

printf 'RESULT_CHECK_OVERALL_EXIT=%s\n' "$overall"
exit "$overall"

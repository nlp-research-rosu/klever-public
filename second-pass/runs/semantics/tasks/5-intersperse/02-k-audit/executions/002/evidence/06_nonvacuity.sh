#!/usr/bin/env bash
set -u
set -o pipefail

scratch=/tmp/audit-work/5-intersperse
evidence=/audit-output/evidence
overall=0

printf 'Mutation: prepend delimiter D to the required returned list\n'
printf 'Concrete falsifying satisfying input: NUMBERS=.ValSeq, D=4\n'
printf 'Actual/claimed original output: .ValSeq; mutated obligation: vCons(4,.ValSeq)\n'

cp "$evidence/06_spec_vacuity.k" "$scratch/06_spec_vacuity.k"

printf 'COMMAND kprove %s --definition %s --spec-module AUDIT-SPEC-VACUITY\n' \
  "$scratch/06_spec_vacuity.k" \
  "$scratch/verification-kompiled"
kprove "$scratch/06_spec_vacuity.k" \
  --definition "$scratch/verification-kompiled" \
  --spec-module AUDIT-SPEC-VACUITY \
  > "$evidence/06_kprove_vacuity.log" 2>&1
prove_status=$?
printf 'EXIT %d\n' "$prove_status"
printf 'OUTPUT_BEGIN\n'
tail -n 180 "$evidence/06_kprove_vacuity.log"
printf 'OUTPUT_END\n'

if [[ "$prove_status" -eq 0 ]]; then
  printf 'BAD mutation unexpectedly exited zero\n'
  overall=1
fi
if grep -Fxq '#Top' "$evidence/06_kprove_vacuity.log"; then
  printf 'BAD mutation unexpectedly printed exact #Top\n'
  overall=1
else
  printf 'OK no exact #Top\n'
fi
if grep -q 'WarnStuckClaimState' "$evidence/06_kprove_vacuity.log"; then
  printf 'OK reached stuck claim residual\n'
else
  printf 'BAD missing stuck claim residual\n'
  overall=1
fi
if grep -Fq 'vCons ( D:Int' "$evidence/06_kprove_vacuity.log"; then
  printf 'OK residual mentions the changed delimiter-bearing obligation\n'
else
  printf 'BAD residual does not expose changed obligation\n'
  overall=1
fi
if grep -Fq '[Error] Prover: backend terminated because' "$evidence/06_kprove_vacuity.log"; then
  printf 'OK expected proof failure diagnostic\n'
else
  printf 'BAD failure was not the expected unmet proof obligation\n'
  overall=1
fi

printf 'NONVACUITY_SCRIPT_STATUS=%d\n' "$overall"
exit "$overall"

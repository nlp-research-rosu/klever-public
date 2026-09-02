#!/usr/bin/env bash
set -uo pipefail
set -x

scratch=/tmp/audit-work/candidate-src
raw=/tmp/audit-work/stage4-raw
mkdir -p "$raw"
overall=0

python3 /audit-output/evidence/adequacy_substitution.py \
  > "$raw/substitution.log" 2>&1
python_status=$?
printf 'COMMAND: python3 /audit-output/evidence/adequacy_substitution.py\n'
printf 'EXIT[substitution]=%s\n' "$python_status"
sed -n '1,160p' "$raw/substitution.log"
if (( python_status != 0 )); then
  overall=1
fi

kprove /audit-output/evidence/adequacy-witness.k \
  --definition "$scratch/audit-verification-kompiled" \
  --spec-module AUDIT-ADEQUACY \
  > "$raw/kprove-adequacy.log" 2>&1
k_status=$?
printf '%s\n' \
  'COMMAND: kprove /audit-output/evidence/adequacy-witness.k --definition /tmp/audit-work/candidate-src/audit-verification-kompiled --spec-module AUDIT-ADEQUACY'
printf 'EXIT[kprove-adequacy]=%s\n' "$k_status"
sed -n '1,180p' "$raw/kprove-adequacy.log"
grep -Fx '#Top' "$raw/kprove-adequacy.log"
top_status=$?
printf 'TOP-CHECK[kprove-adequacy]=%s\n' "$top_status"
if (( k_status != 0 || top_status != 0 )); then
  overall=1
fi

printf 'STAGE4_OVERALL=%s\n' "$overall"
exit "$overall"

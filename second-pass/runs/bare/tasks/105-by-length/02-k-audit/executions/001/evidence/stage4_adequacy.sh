#!/usr/bin/env bash
set +e
set -x

python3 /audit-output/evidence/program_pinning.py
pinning_exit=$?
printf 'program pinning exit: %s\n' "$pinning_exit"

rg -n '^[[:space:]]*(claim|requires|ensures)\\b|<k>|<program>|<input>|<result>' \
  /tmp/audit-work/source/spec.k
claim_shape_exit=$?
printf 'claim shape inventory exit: %s\n' "$claim_shape_exit"

# The concrete comparisons include satisfying ground instances of the entry
# claim (empty, singleton/mixed valid integers, and invalid integers).
python3 /audit-output/evidence/concrete_semantics_compare.py
ground_witness_exit=$?
printf 'ground satisfying-witness comparisons exit: %s\n' "$ground_witness_exit"

if [ "$pinning_exit" -ne 0 ] || [ "$claim_shape_exit" -ne 0 ] || [ "$ground_witness_exit" -ne 0 ]; then
  exit 1
fi
exit 0

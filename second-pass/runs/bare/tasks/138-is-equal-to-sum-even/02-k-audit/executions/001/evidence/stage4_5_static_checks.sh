#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@"
  status=$?
  set -e
  printf '[exit %d]\n' "$status"
  return "$status"
}

run_allow_nonzero() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@"
  status=$?
  set -e
  printf '[exit %d; nonzero allowed for absence check]\n' "$status"
}

set -e
source_dir=/tmp/audit-work/review-138/candidate-src
definition=/tmp/audit-work/review-138/build/semantic-kompiled

run nl -ba "$source_dir/solution.mpy"
run nl -ba "$source_dir/semantic.k"
run nl -ba "$source_dir/verification.k"
run nl -ba "$source_dir/spec.k"
run python3 /audit-output/evidence/check_program_pinning.py

run rg -n \
  '^(\s*)(syntax|configuration|rule|claim)|\[(function|total|functional|simplification|concrete|priority)' \
  "$source_dir/semantic.k" "$source_dir/verification.k" "$source_dir/spec.k"

run_allow_nonzero rg -n \
  '\[(priority|simplification|concrete|anywhere|opaque|macro|alias|assoc|comm|idem)' \
  "$source_dir/semantic.k" "$source_dir/verification.k"

run krun "$source_dir/solution.mpy" \
  --definition "$definition" \
  -cN=8
run krun "$source_dir/solution-body-mutated.mpy" \
  --definition "$definition" \
  -cN=8

run python3 -c 'from importlib.util import module_from_spec, spec_from_file_location; p="/tmp/audit-work/review-138/reference-src/canonical.py"; s=spec_from_file_location("canonical_witness",p); m=module_from_spec(s); s.loader.exec_module(m); print({"entry_general_N":8,"necessity_A_B_C_D":[2,2,2,2],"sufficiency_N":8,"examples":[4,6,8],"canonical_results":{n:m.is_equal_to_sum_even(n) for n in [4,6,8]}})'
run python3 -c 'from importlib.util import module_from_spec, spec_from_file_location; p="/tmp/audit-work/review-138/candidate-src/solution.py"; s=spec_from_file_location("candidate_witness",p); m=module_from_spec(s); s.loader.exec_module(m); print({"entry_general_N":8,"necessity_sum":sum([2,2,2,2]),"sufficiency_witnesses":[8-6,2,2,2],"candidate_results":{n:m.is_equal_to_sum_even(n) for n in [4,6,8]}})'

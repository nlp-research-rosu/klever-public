#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction/work

cmp /candidate/solution.py "$work/solution.py"
solution_py_status=$?
cmp /candidate/solution.mpy "$work/solution.mpy"
solution_mpy_status=$?
cmp /candidate/spec.k "$work/spec.k"
spec_status=$?
cmp /candidate/verification.k "$work/verification.k"
verification_status=$?
diff --no-dereference -qr /reference/reference-semantics "$work/reference-semantics"
semantics_status=$?

printf 'candidate_solution_py_cmp_exit=%d\n' "$solution_py_status"
printf 'candidate_solution_mpy_cmp_exit=%d\n' "$solution_mpy_status"
printf 'candidate_spec_cmp_exit=%d\n' "$spec_status"
printf 'candidate_verification_cmp_exit=%d\n' "$verification_status"
printf 'trusted_semantics_recursive_diff_exit=%d\n' "$semantics_status"

if [[ "$solution_py_status" -ne 0 ||
      "$solution_mpy_status" -ne 0 ||
      "$spec_status" -ne 0 ||
      "$verification_status" -ne 0 ||
      "$semantics_status" -ne 0 ]]; then
  exit 1
fi

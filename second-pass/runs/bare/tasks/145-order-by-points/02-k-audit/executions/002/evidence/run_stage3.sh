#!/usr/bin/env bash
set -u
set -x

cd /tmp/audit-work/reconstruction || exit 90

cp /audit-output/evidence/spec-labeled.k ./spec-labeled.k
copy_labeled_rc=$?

kompile semantic.k \
  --backend haskell \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
concrete_build_rc=$?

run_one() {
  case_name=$1
  input_term=$2
  krun solution.mpy \
    -cINPUT="$input_term" \
    --definition concrete-kompiled
  case_rc=$?
  printf 'krun_case=%s exit=%d\n' "$case_name" "$case_rc"
  return "$case_rc"
}

run_one empty 'ListExpr()'
krun_empty_rc=$?
run_one prompt 'ListExpr(Int(1), Int(11), Int(-1), Int(-11), Int(-12))'
krun_prompt_rc=$?
run_one branches 'ListExpr(Int(0), Int(-1), Int(1), Int(-10), Int(10), Int(99), Int(-99))'
krun_branches_rc=$?
run_one stability 'ListExpr(Int(5), Int(5), Int(-5), Int(-5), Int(14), Int(41), Int(-14), Int(-41))'
krun_stability_rc=$?
run_one recursive 'ListExpr(Int(29), Int(-7), Int(11), Int(-100), Int(20), Int(-11))'
krun_recursive_rc=$?

python3 -c 'import solution; cases=[[],[1,11,-1,-11,-12],[0,-1,1,-10,10,99,-99],[5,5,-5,-5,14,41,-14,-41],[29,-7,11,-100,20,-11]]; [print(f"python_case={x!r} output={solution.order_by_points(x)!r}") for x in cases]'
python_compare_rc=$?

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
proof_build_rc=$?

claim_failures=0
for claim in \
  c01-score-neg12 \
  c02-score-neg11 \
  c03-score-neg1 \
  c04-score-11 \
  c05-invoke \
  c06-sort-empty \
  c07-sort-single \
  c08-insert-le \
  c09-insert-gt \
  c10-example \
  c11-empty \
  c12-stability \
  c13-is-ordered
do
  kprove spec-labeled.k \
    --definition verification-kompiled \
    --spec-module SPEC-LABELED \
    --claims "SPEC-LABELED.label($claim)"
  claim_rc=$?
  printf 'claim=%s exit=%d\n' "$claim" "$claim_rc"
  if test "$claim_rc" -ne 0; then
    claim_failures=$((claim_failures + 1))
  fi
done

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
original_spec_rc=$?

set +x
printf 'copy_labeled_exit=%d\n' "$copy_labeled_rc"
printf 'concrete_build_exit=%d\n' "$concrete_build_rc"
printf 'krun_empty_exit=%d\n' "$krun_empty_rc"
printf 'krun_prompt_exit=%d\n' "$krun_prompt_rc"
printf 'krun_branches_exit=%d\n' "$krun_branches_rc"
printf 'krun_stability_exit=%d\n' "$krun_stability_rc"
printf 'krun_recursive_exit=%d\n' "$krun_recursive_rc"
printf 'python_compare_exit=%d\n' "$python_compare_rc"
printf 'proof_build_exit=%d\n' "$proof_build_rc"
printf 'claim_failures=%d\n' "$claim_failures"
printf 'original_spec_exit=%d\n' "$original_spec_rc"

test "$copy_labeled_rc" -eq 0 \
  && test "$concrete_build_rc" -eq 0 \
  && test "$krun_empty_rc" -eq 0 \
  && test "$krun_prompt_rc" -eq 0 \
  && test "$krun_branches_rc" -eq 0 \
  && test "$krun_stability_rc" -eq 0 \
  && test "$krun_recursive_rc" -eq 0 \
  && test "$python_compare_rc" -eq 0 \
  && test "$proof_build_rc" -eq 0 \
  && test "$claim_failures" -eq 0 \
  && test "$original_spec_rc" -eq 0

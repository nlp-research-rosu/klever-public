#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

audit_work=/tmp/audit-work/audit149
overall=0
cd "$audit_work"

test ! -e semantic-kompiled
test ! -e verification-kompiled

python3 /audit-output/evidence/generate_concrete_cases.py "$audit_work"

kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled \
  -w none
status=$?
printf 'SEMANTICS_KOMPILE_EXIT=%s\n' "$status"
if (( status != 0 )); then overall=1; fi

for run_file in audit-*.run; do
  case_name=${run_file#audit-}
  case_name=${case_name%.run}
  krun "$run_file" --definition semantic-kompiled \
    > "audit-${case_name}.krun.out" 2>&1
  status=$?
  printf 'KRUN_EXIT case=%s status=%s\n' "$case_name" "$status"
  sed -n '1,80p' "audit-${case_name}.krun.out"
  if (( status != 0 )); then
    overall=1
  elif ! grep -Fq -f "audit-${case_name}.expected" \
      "audit-${case_name}.krun.out"; then
    printf 'KRUN_EXPECTATION_MISMATCH case=%s expected=%s\n' \
      "$case_name" "$(cat "audit-${case_name}.expected")"
    overall=1
  else
    printf 'KRUN_MATCH case=%s expected=%s\n' \
      "$case_name" "$(cat "audit-${case_name}.expected")"
  fi
done

kompile verification.k \
  --main-module SORTED-LIST-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled \
  -w none
status=$?
printf 'VERIFICATION_KOMPILE_EXIT=%s\n' "$status"
if (( status != 0 )); then overall=1; fi

claims=(
  universal-correctness
  base
  symbolic-two
  symbolic-two-reverse
  symbolic-three
  prompt-example-one
  prompt-example-two
)
for claim_name in "${claims[@]}"; do
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC \
    --claims "$claim_name" \
    --output pretty \
    -w none \
    > "audit-claim-${claim_name}.out" 2>&1
  status=$?
  printf 'KPROVE_EXIT claim=%s status=%s\n' "$claim_name" "$status"
  sed -n '1,120p' "audit-claim-${claim_name}.out"
  if (( status != 0 )); then
    overall=1
  elif ! grep -Fxq '#Top' "audit-claim-${claim_name}.out"; then
    printf 'KPROVE_MISSING_TOP claim=%s\n' "$claim_name"
    overall=1
  else
    printf 'KPROVE_TOP claim=%s\n' "$claim_name"
  fi
done

printf 'STAGE3_OVERALL=%s\n' "$overall"
exit "$overall"

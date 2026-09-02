#!/usr/bin/env bash
set -uo pipefail

printf '$ python3 /audit-output/evidence/split_positive_claims.py\n'
python3 /audit-output/evidence/split_positive_claims.py
split_status=$?
printf 'EXIT STATUS: %d\n' "$split_status"
if (( split_status != 0 )); then
  exit 1
fi

passed=0
failed=0
for claim_number in $(seq -w 1 26); do
  claim_file="/audit-output/evidence/positive-claims/claim-0${claim_number}.k"
  claim_module="SPEC-CLAIM-0${claim_number}"
  claim_log="/audit-output/evidence/positive-claims/claim-0${claim_number}.log"
  printf '$ kprove %q -I /tmp/audit-work/25-factorize --definition fresh-verification-kompiled --spec-module %q\n' \
    "$claim_file" "$claim_module"
  kprove "$claim_file" \
    -I /tmp/audit-work/25-factorize \
    --definition fresh-verification-kompiled \
    --spec-module "$claim_module" > "$claim_log" 2>&1
  status=$?
  top_count=$(grep -c '^#Top$' "$claim_log" || true)
  sed -n '1,80p' "$claim_log"
  printf 'EXIT STATUS: %d; #Top lines: %d\n' "$status" "$top_count"
  if (( status == 0 && top_count >= 1 )); then
    passed=$((passed + 1))
  else
    failed=$((failed + 1))
  fi
done

printf 'POSITIVE_CLAIMS_PASSED=%d\n' "$passed"
printf 'POSITIVE_CLAIMS_FAILED=%d\n' "$failed"
if (( passed != 26 || failed != 0 )); then
  exit 1
fi

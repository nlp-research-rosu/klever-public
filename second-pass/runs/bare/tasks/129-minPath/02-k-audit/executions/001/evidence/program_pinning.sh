#!/usr/bin/env bash
set +e

work=/tmp/audit-work/candidate-src
direct_output=/tmp/audit-work/direct-program-depth1.out
alias_output=/tmp/audit-work/solutionProgram-depth2.out
direct_errors=/tmp/audit-work/direct-program-depth1.err
alias_errors=/tmp/audit-work/solutionProgram-depth2.err
grid='grid2(1,2,3,4)'

printf '%s\n' \
  "DIRECT_COMMAND: krun solution.mpy --definition verification-kompiled-fresh -cGRID=$grid -cKLEN=5 --depth 1 --output pretty"
krun "$work/solution.mpy" \
  --definition "$work/verification-kompiled-fresh" \
  -cGRID="$grid" \
  -cKLEN=5 \
  --depth 1 \
  --output pretty \
  > "$direct_output" 2> "$direct_errors"
direct_status=$?
printf 'DIRECT_EXIT=%s\n' "$direct_status"

printf '%s\n' \
  "ALIAS_COMMAND: krun solutionProgram.mpy --definition verification-kompiled-fresh -cGRID=$grid -cKLEN=5 --depth 2 --output pretty"
krun "$work/solutionProgram.mpy" \
  --definition "$work/verification-kompiled-fresh" \
  -cGRID="$grid" \
  -cKLEN=5 \
  --depth 2 \
  --output pretty \
  > "$alias_output" 2> "$alias_errors"
alias_status=$?
printf 'ALIAS_EXIT=%s\n' "$alias_status"

printf '%s\n' '=== EXPECTED DEPTH WARNINGS ==='
sed -n '1,20p' "$direct_errors"
sed -n '1,20p' "$alias_errors"

sha256sum "$direct_output" "$alias_output"
diff -u "$direct_output" "$alias_output"
diff_status=$?
printf 'NORMALIZED_CONFIGURATION_DIFF_EXIT=%s\n' "$diff_status"

if [ "$direct_status" -eq 0 ] && [ "$alias_status" -eq 0 ] && [ "$diff_status" -eq 0 ]; then
  exit 0
fi
exit 1

#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/137-compare-one-audit
raw_log="$work/scientific-krun.raw.log"

printf '%s\n' 'PYTHON EXPECTED: solution.compare_one("1e2", 99) returns "1e2"'
printf '%s\n' 'COMMAND: timeout --signal=TERM --kill-after=2 8 krun solution.mpy --definition concrete-kompiled -cA=pyStr("1e2") -cB=pyInt(99) --output pretty'
timeout --signal=TERM --kill-after=2 8 \
  krun "$work/solution.mpy" \
    --definition "$work/concrete-kompiled" \
    '-cA=pyStr("1e2")' \
    '-cB=pyInt(99)' \
    --output pretty \
  > "$raw_log" 2>&1
status=$?
printf 'KRUN SCIENTIFIC_STRING EXIT: %s\n' "$status"
sed -n '1,160p' "$raw_log"

# This is a negative coverage probe: successful K execution would be surprising
# but is not encoded as the shell script's own success criterion.
printf '%s\n' 'STAGE3_SCIENTIFIC_PROBE_COMPLETE'
exit 0

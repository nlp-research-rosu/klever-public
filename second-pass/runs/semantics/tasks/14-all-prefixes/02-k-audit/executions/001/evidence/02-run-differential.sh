#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/02-differential.py'
printf ' /reference/canonical.py'
printf ' /tmp/audit-work/proof-audit.Dl0nBZ/candidate/solution.py'
printf ' /audit-output/evidence/differential-inputs.json'
printf ' /audit-output/evidence/differential-results.json\n'

python3 /audit-output/evidence/02-differential.py \
  /reference/canonical.py \
  /tmp/audit-work/proof-audit.Dl0nBZ/candidate/solution.py \
  /audit-output/evidence/differential-inputs.json \
  /audit-output/evidence/differential-results.json
status=$?
printf '[exit %d]\n' "$status"
exit "$status"

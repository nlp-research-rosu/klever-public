#!/usr/bin/env bash
set -u -o pipefail

root=/tmp/audit-work/58-common-audit

printf '$ python3 -c %q\n' \
  'import sys; sys.path[:0]=["/tmp/audit-work/58-common-audit/trusted","/tmp/audit-work/58-common-audit/candidate"]; import canonical, solution; print("canonical", canonical.common(["beta","alpha"],["alpha"])); print("candidate", solution.common(["beta","alpha"],["alpha"]))'
python3 -c 'import sys; sys.path[:0]=["/tmp/audit-work/58-common-audit/trusted","/tmp/audit-work/58-common-audit/candidate"]; import canonical, solution; print("canonical", canonical.common(["beta","alpha"],["alpha"])); print("candidate", solution.common(["beta","alpha"],["alpha"]))'
python_status=$?
printf '[exit %d]\n' "$python_status"

printf '\n$ krun %q --definition %q -cL1=%q -cL2=%q\n' \
  "$root/candidate/solution.mpy" \
  "$root/semantic-kompiled-audit" \
  'list("beta","alpha")' \
  'list("alpha")'
krun "$root/candidate/solution.mpy" \
  --definition "$root/semantic-kompiled-audit" \
  -cL1='list("beta","alpha")' \
  -cL2='list("alpha")'
k_status=$?
printf '[exit %d]\n' "$k_status"

if [[ "$python_status" -eq 0 && "$k_status" -ne 0 ]]; then
  printf 'EXPECTED_SCOPE_REJECTION\n'
  exit 0
fi
printf 'UNEXPECTED_SCOPE_PROBE_RESULT\n'
exit 1

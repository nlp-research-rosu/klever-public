#!/bin/sh
set -eu

printf '%s\n' 'AUDIT_MODE'
printenv AUDIT_MODE
printf '%s\n' 'CANDIDATE_PATH_STATUS'
if [ -e /candidate ]; then
  printf '%s\n' 'present'
else
  printf '%s\n' 'absent'
fi
printf '%s\n' 'VERIFICATION.K'
nl -ba /reference/k-proof/verification.k
printf '%s\n' 'SPEC.K'
nl -ba /reference/k-proof/spec.k
printf '%s\n' 'SOURCE_SOLUTION.PY'
nl -ba /reference/k-proof/solution.py
printf '%s\n' 'INT_SEMANTICS'
nl -ba /reference/k-proof/reference-semantics/semantics/int.k
printf '%s\n' 'WHILE_SEMANTICS'
sed -n '76,88p' /reference/k-proof/reference-semantics/semantics/controls.k
printf '%s\n' 'ABS_SEMANTICS'
sed -n '40,47p' /reference/k-proof/reference-semantics/semantics/builtins.k
printf '%s\n' 'PROOF_COMMANDS'
nl -ba /reference/k-proof/prove.sh

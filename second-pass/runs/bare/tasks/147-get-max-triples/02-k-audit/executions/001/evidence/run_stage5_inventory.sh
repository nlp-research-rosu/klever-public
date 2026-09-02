#!/usr/bin/env bash
set -u

echo '$ find /candidate -maxdepth 1 -type f -name "*.k" -printf "%f\n" | sort'
find /candidate -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort
status=$?
echo "exit_status=$status"

echo '$ sha256sum /candidate/semantic.k /candidate/verification.k /candidate/spec.k /tmp/audit-work/audit147/semantic.k /tmp/audit-work/audit147/verification.k /tmp/audit-work/audit147/spec.k'
sha256sum \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /tmp/audit-work/audit147/semantic.k \
  /tmp/audit-work/audit147/verification.k \
  /tmp/audit-work/audit147/spec.k
status=$?
echo "exit_status=$status"

echo '$ nl -ba /tmp/audit-work/audit147/semantic.k'
nl -ba /tmp/audit-work/audit147/semantic.k
status=$?
echo "exit_status=$status"

echo '$ nl -ba /tmp/audit-work/audit147/verification.k'
nl -ba /tmp/audit-work/audit147/verification.k
status=$?
echo "exit_status=$status"

echo '$ nl -ba /tmp/audit-work/audit147/spec.k'
nl -ba /tmp/audit-work/audit147/spec.k
status=$?
echo "exit_status=$status"

echo '$ rg -n "syntax|configuration|rule|claim|function|total|functional|opaque|priority|simplification|strict|seqstrict" /tmp/audit-work/audit147/{semantic.k,verification.k,spec.k}'
rg -n \
  'syntax|configuration|rule|claim|function|total|functional|opaque|priority|simplification|strict|seqstrict' \
  /tmp/audit-work/audit147/{semantic.k,verification.k,spec.k}
status=$?
echo "exit_status=$status"
exit "$status"

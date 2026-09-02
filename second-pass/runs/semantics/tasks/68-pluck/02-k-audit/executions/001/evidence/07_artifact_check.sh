#!/usr/bin/env bash
set +e

echo '$ find /audit-output/evidence -maxdepth 1 -printf "%y %f %s bytes -> %l\\n" | sort'
find /audit-output/evidence -maxdepth 1 -printf '%y %f %s bytes -> %l\n' | sort
find_rc=${PIPESTATUS[0]}
echo "exit=$find_rc"

echo '$ for f in /audit-output/evidence/*.sh; do bash -n "$f"; done'
syntax_rc=0
for f in /audit-output/evidence/*.sh; do
  bash -n "$f" || syntax_rc=1
done
echo "exit=$syntax_rc"

echo '$ tail -n 2 /audit-output/REVIEW.md'
tail -n 2 /audit-output/REVIEW.md
tail_rc=$?
echo "exit=$tail_rc"

echo '$ test "$(grep -c "^VERDICT:" /audit-output/REVIEW.md)" -eq 1'
test "$(grep -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1
verdict_rc=$?
echo "exit=$verdict_rc"

echo '$ test "$(grep -c "^LEGITIMACY:" /audit-output/REVIEW.md)" -eq 1'
test "$(grep -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1
legitimacy_rc=$?
echo "exit=$legitimacy_rc"

if (( find_rc != 0 || syntax_rc != 0 || tail_rc != 0 || verdict_rc != 0 || legitimacy_rc != 0 )); then
  exit 1
fi

#!/usr/bin/env bash
set -uo pipefail

echo '$ python3 /audit-output/evidence/05-static-review/rule_inventory.py'
python3 /audit-output/evidence/05-static-review/rule_inventory.py
status=$?
echo "exit_status=$status"
test "$status" -eq 0 || exit "$status"

echo
echo '$ rg -n "car_race_collision|N \\*Int N" reference-semantics verification.k'
cd /tmp/audit-work/candidate-src
rg -n 'car_race_collision|N \*Int N' reference-semantics verification.k
scan_status=$?
echo "exit_status=$scan_status (1 means no task-answer occurrence)"
test "$scan_status" -eq 1 || exit 91

echo
echo '$ rg -n "^(\\s*)(syntax|rule|claim|context|configuration)" verification.k'
rg -n '^(\s*)(syntax|rule|claim|context|configuration)' verification.k
extension_status=$?
echo "exit_status=$extension_status (1 means no proof-local sentence)"
test "$extension_status" -eq 1 || exit 92

echo
echo '$ sha256sum /audit-output/evidence/05-static-review/rule_inventory.tsv'
sha256sum /audit-output/evidence/05-static-review/rule_inventory.tsv
status=$?
echo "exit_status=$status"
exit "$status"

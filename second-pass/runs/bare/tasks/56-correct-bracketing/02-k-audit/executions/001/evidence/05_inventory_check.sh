#!/usr/bin/env bash
set -u

echo 'AUDITOR COMMAND: list every .k file at candidate root'
find /candidate -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: enumerate local declaration/rule/claim starts'
rg -n '^[[:space:]]*(syntax|configuration|rule|claim)\b' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: search for soundness-relevant K attributes'
rg -n '\[(function|total|functional|simplification|concrete|priority|owise|macro|alias)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: count rule starts by file'
for file in /candidate/semantic.k /candidate/verification.k
do
  count=$(rg -c '^[[:space:]]*rule\b' "$file")
  echo "$file rule_starts=$count"
done
status=$?
echo "EXIT STATUS: $status"

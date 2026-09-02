#!/usr/bin/env bash
set +e

printf '%s\n' '$ python3 /audit-output/evidence/05_decisions.py > /audit-output/evidence/05_rule_decisions.csv'
python3 /audit-output/evidence/05_decisions.py \
  > /audit-output/evidence/05_rule_decisions.csv \
  2> /audit-output/evidence/05_rule_decisions.counts
printf '[exit %d]\n' "$?"

printf '%s\n' '$ cat /audit-output/evidence/05_rule_decisions.counts'
cat /audit-output/evidence/05_rule_decisions.counts
printf '[exit %d]\n' "$?"

printf '%s\n' '$ tail -n +2 /audit-output/evidence/05_rule_decisions.csv | wc -l'
tail -n +2 /audit-output/evidence/05_rule_decisions.csv | wc -l
printf '[exit %d]\n' "$?"

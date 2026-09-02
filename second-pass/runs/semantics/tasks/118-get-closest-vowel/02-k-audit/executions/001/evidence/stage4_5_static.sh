#!/usr/bin/env bash
set -u

overall=0
run_to_log() {
  label=$1
  shift
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    overall=1
  fi
}

echo '== Concrete satisfiable entry witnesses and result substitution =='
run_to_log witnesses python3 /audit-output/evidence/adequacy_witnesses.py

echo '== Exhaustive declaration and rule inventory =='
printf '$ python3 /audit-output/evidence/rule_inventory.py > /audit-output/evidence/rule_inventory.tsv\n'
python3 /audit-output/evidence/rule_inventory.py > /audit-output/evidence/rule_inventory.tsv
rc=$?
printf '[exit %d]\n' "$rc"
(( rc == 0 )) || overall=1
run_to_log inventory-lines wc -l /audit-output/evidence/rule_inventory.tsv
run_to_log inventory-kinds awk -F '\t' 'NR>1 { count[$4]++ } END { for (kind in count) print kind, count[kind] }' /audit-output/evidence/rule_inventory.tsv
run_to_log inventory-decisions awk -F '\t' 'NR>1 { count[$7]++ } END { for (decision in count) print decision, count[decision] }' /audit-output/evidence/rule_inventory.tsv

echo '== Function/total/functional/opaque/priority/simplification declarations =='
run_to_log attribute-inventory sh -c 'awk -F "\t" '\''NR==1 || $5 != "" { print }'\'' /audit-output/evidence/rule_inventory.tsv'

exit "$overall"

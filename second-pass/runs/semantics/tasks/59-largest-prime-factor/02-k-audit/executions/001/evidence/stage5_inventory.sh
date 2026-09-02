#!/usr/bin/env bash
set -u

echo '$ python3 /audit-output/evidence/k_inventory.py > k_inventory.tsv'
python3 /audit-output/evidence/k_inventory.py \
  > /audit-output/evidence/k_inventory.tsv
inventory_status=$?
echo "exit=$inventory_status"

echo '$ inventory category counts'
awk -F '\t' '
  NR > 1 && $1 !~ /^#/ { kinds[$3]++; rel[$5]++; disp[$6]++ }
  END {
    for (k in kinds) print "kind[" k "]=" kinds[k]
    for (k in rel) print "relevance[" k "]=" rel[k]
    for (k in disp) print "disposition[" k "]=" disp[k]
  }
' /audit-output/evidence/k_inventory.tsv | LC_ALL=C sort
echo "exit=$?"

echo '$ declarations carrying total, function, macro, simplification, priority, concrete, or no-evaluators'
awk -F '\t' '
  NR > 1 && $4 ~ /(total|function|macro|simplification|priority|concrete|no-evaluators)/ {
    print $1 ":" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6
  }
' /audit-output/evidence/k_inventory.tsv
echo "exit=$?"

exit "$inventory_status"

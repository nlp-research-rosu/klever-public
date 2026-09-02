#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage5_static_review.log
exec >"$log" 2>&1

run() {
  echo "COMMAND: $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  return "$status"
}

echo "STAGE 5 RULE-BY-RULE STATIC SOUNDNESS REVIEW"
run python3 /audit-output/evidence/stage5_inventory.py || exit $?

run wc -l /audit-output/evidence/stage5_rule_inventory.tsv

echo "COMMAND: count required inventory categories"
for kind in syntax rule context configuration; do
  count=$(awk -F '\t' -v value="$kind" 'NR > 1 && $5 == value { n += 1 } END { print n + 0 }' \
    /audit-output/evidence/stage5_rule_inventory.tsv)
  echo "kind=$kind count=$count"
done
for attribute in function functional total opaque/no-evaluators priority simplification; do
  count=$(awk -F '\t' -v value="$attribute" \
    'NR > 1 { n += ("," $6 ",") ~ ("," value ",") } END { print n + 0 }' \
    /audit-output/evidence/stage5_rule_inventory.tsv)
  echo "attribute=$attribute count=$count"
done
unreviewed=$(awk -F '\t' 'NR > 1 && $7 == "" { n += 1 } END { print n + 0 }' \
  /audit-output/evidence/stage5_rule_inventory.tsv)
echo "records_without_disposition=$unreviewed"
echo "EXIT: 0"

run sha256sum \
  /audit-output/evidence/stage5_rule_inventory.tsv \
  /audit-output/evidence/stage5_proof_local_review.md

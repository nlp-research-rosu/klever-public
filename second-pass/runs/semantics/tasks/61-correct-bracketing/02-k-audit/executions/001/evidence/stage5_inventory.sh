#!/usr/bin/env bash
set +e

inventory=/audit-output/evidence/rule-inventory.txt
printf '$ python3 /audit-output/evidence/rule_inventory.py /tmp/audit-work/candidate-src/reference-semantics /tmp/audit-work/candidate-src/verification.k /tmp/audit-work/candidate-src/spec.k > %s\n' "$inventory"
python3 /audit-output/evidence/rule_inventory.py \
  /tmp/audit-work/candidate-src/reference-semantics \
  /tmp/audit-work/candidate-src/verification.k \
  /tmp/audit-work/candidate-src/spec.k \
  > "$inventory"
rc=$?
printf 'EXIT_STATUS=%d\n' "$rc"
sha256sum "$inventory"
printf 'SHA256_EXIT_STATUS=%d\n' "$?"
wc -l -c "$inventory"
printf 'WC_EXIT_STATUS=%d\n' "$?"
grep -E '^(GRAND_COUNTS|ATTRIBUTE_COUNTS)=' "$inventory"
printf 'COUNT_EXIT_STATUS=%d\n' "$?"
exit "$rc"

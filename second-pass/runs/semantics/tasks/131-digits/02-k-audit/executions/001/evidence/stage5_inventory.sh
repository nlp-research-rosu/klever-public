#!/usr/bin/env bash
set -u

LOG_FILE=/audit-output/evidence/stage5_inventory.log
: > "$LOG_FILE"

printf 'COMMAND: python3 /audit-output/evidence/build_rule_inventory.py\n' >> "$LOG_FILE"
python3 /audit-output/evidence/build_rule_inventory.py >> "$LOG_FILE" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status" >> "$LOG_FILE"

printf 'COMMAND: sha256sum /audit-output/evidence/rule_inventory.md /audit-output/evidence/rule_inventory.json\n' >> "$LOG_FILE"
sha256sum \
  /audit-output/evidence/rule_inventory.md \
  /audit-output/evidence/rule_inventory.json >> "$LOG_FILE" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status" >> "$LOG_FILE"

printf 'COMMAND: python3 /audit-output/evidence/classify_rule_inventory.py\n' >> "$LOG_FILE"
python3 /audit-output/evidence/classify_rule_inventory.py >> "$LOG_FILE" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status" >> "$LOG_FILE"

printf 'COMMAND: sha256sum /audit-output/evidence/rule_review.tsv\n' >> "$LOG_FILE"
sha256sum /audit-output/evidence/rule_review.tsv >> "$LOG_FILE" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status" >> "$LOG_FILE"

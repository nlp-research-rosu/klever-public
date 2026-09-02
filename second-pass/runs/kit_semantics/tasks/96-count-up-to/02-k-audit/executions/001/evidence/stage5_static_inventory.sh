#!/usr/bin/env bash
set -euo pipefail
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

python3 /audit-output/evidence/build_rule_inventory.py
echo "RULE_INVENTORY_GENERATION_EXIT=$?"

wc -l -c /audit-output/evidence/rule_inventory.md \
  /audit-output/evidence/used_construct_mapping.md

rg -n '\[(function|total|functional|macro|macro-rec|symbol|priority|simplification|owise|concrete|no-evaluators)' \
  /tmp/audit-work/reconstruction/reference-semantics \
  /tmp/audit-work/reconstruction/verification.k \
  /tmp/audit-work/reconstruction/spec.k
echo "ATTRIBUTE_INVENTORY_SCAN_EXIT=$?"

rg -n '^\s*(syntax|configuration|context|rule|claim|alias)\b' \
  /tmp/audit-work/reconstruction/reference-semantics \
  /tmp/audit-work/reconstruction/verification.k \
  /tmp/audit-work/reconstruction/spec.k | wc -l
echo "SOURCE_DIRECTIVE_COUNT_EXIT=$?"

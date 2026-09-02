#!/usr/bin/env bash
set -euo pipefail

sources=(
  /tmp/audit-work/rebuild/semantic.k
  /tmp/audit-work/rebuild/solution-program.k
  /tmp/audit-work/rebuild/verification.k
  /tmp/audit-work/rebuild/spec.k
  /tmp/audit-work/rebuild/definition.k
)

printf 'SOURCE_HASHES:\n'
sha256sum "${sources[@]}"

printf 'NUMBERED_LOCAL_SOURCES:\n'
for source in "${sources[@]}"; do
  printf 'FILE %s\n' "$source"
  nl -ba "$source"
done

printf 'DECLARATION_AND_RULE_LINES:\n'
rg -n \
  '^\s*(requires|module|imports|syntax|configuration|rule|claim)|\[(function|total|functional|simplification|concrete|priority|owise|anywhere)' \
  "${sources[@]}"

printf 'SPECIAL_ATTRIBUTE_COUNTS:\n'
for attribute in function total functional simplification concrete priority owise anywhere; do
  count=$( { rg -o "\\[$attribute\\]|[, ]$attribute[,\\]]" "${sources[@]}" || true; } | wc -l )
  printf '%s=%d\n' "$attribute" "$count"
done

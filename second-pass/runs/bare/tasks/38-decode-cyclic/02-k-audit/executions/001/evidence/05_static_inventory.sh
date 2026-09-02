#!/usr/bin/env bash
set -u

src=/tmp/audit-work/38-decode-cyclic-audit/candidate-src
overall=0

printf 'Complete numbered local K sources\n'
for file in "$src/semantic.k" "$src/verification.k" "$src/spec.k"; do
  printf '\n$ nl -ba %s\n' "$file"
  nl -ba "$file"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then overall=1; fi
done

printf '\nDeclaration/rule/claim index\n'
printf '$ rg -n declarations-and-attributes %s\n' "$src"
rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim)|\[(function|total|functional|simplification|concrete|priority|owise|anywhere|trusted)' \
  "$src/semantic.k" "$src/verification.k" "$src/spec.k"
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '\nCounts (multi-line rule and claim headers only)\n'
for file in "$src/semantic.k" "$src/verification.k" "$src/spec.k"; do
  rules=$(rg -c '^[[:space:]]*rule ' "$file" || true)
  claims=$(rg -c '^[[:space:]]*claim ' "$file" || true)
  syntax=$(rg -c '^[[:space:]]*syntax ' "$file" || true)
  printf '%s syntax_headers=%s rule_headers=%s claim_headers=%s\n' \
    "$file" "${syntax:-0}" "${rules:-0}" "${claims:-0}"
done

printf '\nConstructors present in submitted solution.mpy\n'
printf '$ rg -o constructor-pattern solution.mpy | sort | uniq -c\n'
rg -o '[A-Za-z][A-Za-z0-9]*\(' "$src/solution.mpy" \
  | sed 's/($//' | sort | uniq -c
status=${PIPESTATUS[0]}
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '\nForbidden/exceptional proof-extension attributes (empty is expected)\n'
printf '$ rg -n priority-or-opaque-or-trusted local K sources\n'
rg -n \
  '\[(priority|owise|anywhere|trusted|concrete|functional)|opaque|priority\(' \
  "$src/semantic.k" "$src/verification.k" "$src/spec.k"
status=$?
printf '[exit %d; exit 1 means no matches]\n' "$status"
if [ "$status" -gt 1 ]; then overall=1; fi

printf '\nOverall inventory script status: %d\n' "$overall"
exit "$overall"

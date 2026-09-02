#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/31-is-prime-audit
cd "${work}" || exit 125
failures=0

run_checked() {
  description=$1
  shift
  echo "COMMAND (${description}):"
  printf ' %q' "$@"
  echo
  "$@"
  status=$?
  echo "EXIT_STATUS (${description}): ${status}"
  if [[ ${status} -ne 0 ]]; then
    failures=$((failures + 1))
  fi
}

run_checked inventory \
  python3 /audit-output/evidence/rule_inventory.py

echo 'COMMAND (parse-solution): kast ... solution.regenerated.mpy --output json'
kast --definition proof-base-kompiled \
  --module VERIFICATION-BASE \
  --sort Module \
  solution.regenerated.mpy \
  --expand-macros \
  --output json > solution.parsed.json
status=$?
echo "EXIT_STATUS (parse-solution): ${status}"
if [[ ${status} -ne 0 ]]; then failures=$((failures + 1)); fi

for item in entryBody:Stmts primeCond:Expr primeLoopBody:Stmts; do
  name=${item%%:*}
  sort=${item##*:}
  case "${name}" in
    entryBody) expression='#entryBody'; output=entry-body.expanded.json ;;
    primeCond) expression='#primeCond'; output=prime-cond.expanded.json ;;
    primeLoopBody) expression='#primeLoopBody'; output=prime-loop-body.expanded.json ;;
  esac
  echo "COMMAND (expand-${name}): kast --expression ${expression} --sort ${sort} --expand-macros --output json"
  kast --definition proof-base-kompiled \
    --module VERIFICATION-BASE \
    --sort "${sort}" \
    --expression "${expression}" \
    --expand-macros \
    --output json > "${output}"
  status=$?
  echo "EXIT_STATUS (expand-${name}): ${status}"
  if [[ ${status} -ne 0 ]]; then failures=$((failures + 1)); fi
done

run_checked constructor-comparison \
  python3 /audit-output/evidence/constructor_compare.py \
    solution.parsed.json \
    entry-body.expanded.json \
    prime-cond.expanded.json \
    prime-loop-body.expanded.json

echo "FAILURE_COUNT: ${failures}"
if [[ ${failures} -ne 0 ]]; then
  exit 1
fi
exit 0

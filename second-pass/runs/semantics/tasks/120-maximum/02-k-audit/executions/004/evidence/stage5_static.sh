#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/maximum-120-audit
EVIDENCE=/audit-output/evidence
status=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then status=1; fi
}

printf 'Generate exhaustive line-addressed declaration/rule inventory:\n'
printf '\n$ python3 %s/inventory_k.py > %s/rule-inventory.jsonl\n' "$EVIDENCE" "$EVIDENCE"
python3 "$EVIDENCE/inventory_k.py" > "$EVIDENCE/rule-inventory.jsonl"
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi
run tail -n 1 "$EVIDENCE/rule-inventory.jsonl"
run sha256sum "$EVIDENCE/rule-inventory.jsonl"
run wc -l -c "$EVIDENCE/rule-inventory.jsonl"

printf '\nGenerate fixed deterministic proof-side K differential program:\n'
printf '\n$ python3 %s/generate_k_differential.py > %s/k-differential.py\n' "$EVIDENCE" "$EVIDENCE"
python3 "$EVIDENCE/generate_k_differential.py" > "$EVIDENCE/k-differential.py"
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi
printf '\n$ (cd %s && python3 py2mpy.py %s/k-differential.py > k-differential.mpy)\n' "$WORK" "$EVIDENCE"
(cd "$WORK" && python3 py2mpy.py "$EVIDENCE/k-differential.py" > k-differential.mpy)
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi
run sha256sum "$EVIDENCE/k-differential.py" "$WORK/k-differential.mpy"
run rg -c '^assert ' "$EVIDENCE/k-differential.py"

printf '\nExecute all embedded Python-oracle assertions under fresh supplied K semantics:\n'
run krun "$WORK/k-differential.mpy" --definition "$WORK/runtime-kompiled"

exit "$status"

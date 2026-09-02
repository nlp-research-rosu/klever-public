#!/usr/bin/env bash
set -u

task_dir=/tmp/audit-work/139-special-factorial
inventory=/audit-output/evidence/rule_inventory.tsv

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf 'STAGE 5 EXHAUSTIVE STATIC INVENTORY\n'
printf '$ python3 /audit-output/evidence/k_inventory.py > %q\n' "$inventory"
python3 /audit-output/evidence/k_inventory.py > "$inventory"
rc=$?
printf '[exit %d]\n' "$rc"
run tail -n 5 "$inventory"
run wc -l -c "$inventory"

printf 'Proof-local extension attributes\n'
run rg -n \
  'syntax|rule|priority|simplification|concrete|no-evaluators|functional|total|owise' \
  "$task_dir/verification.k"

printf 'All opaque no-evaluator declarations in fixed supplied semantics\n'
run rg -n 'no-evaluators' \
  "$task_dir/reference-semantics/semantics.k" \
  "$task_dir/reference-semantics/semantics"

printf 'All priority rules in fixed supplied semantics\n'
run rg -n -F 'priority(' \
  "$task_dir/reference-semantics/semantics.k" \
  "$task_dir/reference-semantics/semantics"

printf 'All simplification declarations/rules in submitted K sources\n'
run rg -n 'simplification' \
  "$task_dir/reference-semantics/semantics.k" \
  "$task_dir/reference-semantics/semantics" \
  "$task_dir/verification.k" \
  "$task_dir/spec.k"

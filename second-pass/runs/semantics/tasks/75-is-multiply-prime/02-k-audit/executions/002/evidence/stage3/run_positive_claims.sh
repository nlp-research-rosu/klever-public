#!/usr/bin/env bash
set -euo pipefail

task_dir=/tmp/audit-work/75-is-multiply-prime
runner=/audit-output/evidence/run_logged.sh
log_dir=/audit-output/evidence/stage3/positive-claims

modules=(
  SPEC-NEGATIVE
  SPEC-02-11
  SPEC-12-21
  SPEC-22-31
  SPEC-32-41
  SPEC-42-51
  SPEC-52-61
  SPEC-62-71
  SPEC-72-81
  SPEC-82-91
  SPEC-92-99
)

mkdir -p "$log_dir"
cd "$task_dir"
for module in "${modules[@]}"; do
  echo "RUNNING $module"
  "$runner" "$log_dir/$module.log" \
    kprove spec.k \
      --definition verification-kompiled \
      --spec-module "$module"
  status=$?
  top_count=$(rg -c '^#Top$' "$log_dir/$module.log" || true)
  echo "RESULT $module exit=$status top_count=$top_count"
done

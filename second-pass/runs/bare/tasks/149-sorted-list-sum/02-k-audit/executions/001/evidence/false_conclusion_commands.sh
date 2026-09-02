#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

audit_work=/tmp/audit-work/audit149
cd "$audit_work"
cp /audit-output/evidence/spec-unicode-false-conclusion.k \
  spec-unicode-false-conclusion.k

kprove spec-unicode-false-conclusion.k \
  --definition verification-kompiled \
  --spec-module SPEC-UNICODE-FALSE-CONCLUSION \
  --claims emoji-retained \
  --output pretty \
  -w none
proof_status=$?
printf 'FALSE_CONCLUSION_KPROVE_EXIT=%s\n' "$proof_status"

PYTHONDONTWRITEBYTECODE=1 python3 -c \
  'from solution import sorted_list_sum; print("CPYTHON_GENERATED_RESULT=", sorted_list_sum(["😀"]))'
python_status=$?
printf 'CPYTHON_EXIT=%s\n' "$python_status"

if (( proof_status != 0 || python_status != 0 )); then
  exit 1
fi

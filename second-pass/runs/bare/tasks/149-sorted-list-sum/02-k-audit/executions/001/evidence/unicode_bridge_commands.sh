#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

audit_work=/tmp/audit-work/audit149
cd "$audit_work"
cp /audit-output/evidence/spec-unicode-source-literal.k \
  spec-unicode-source-literal.k

kprove spec-unicode-source-literal.k \
  --definition verification-kompiled \
  --spec-module SPEC-UNICODE-SOURCE-LITERAL \
  --claims source-emoji-filtered \
  --output pretty \
  -w none
source_status=$?
printf 'SOURCE_LITERAL_KPROVE_EXIT=%s\n' "$source_status"

krun audit-emoji_single.run --definition verification-kompiled
runtime_status=$?
printf 'RUNTIME_PROGRAM_PARSE_EXIT=%s\n' "$runtime_status"

exit $(( source_status != 0 || runtime_status != 0 ))

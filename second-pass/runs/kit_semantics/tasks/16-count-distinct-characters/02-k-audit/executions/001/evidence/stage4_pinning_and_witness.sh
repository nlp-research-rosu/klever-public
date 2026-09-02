#!/usr/bin/env bash
set -u
set -o pipefail

exec > >(tee /audit-output/evidence/stage4-pinning-and-witness.log) 2>&1
set -x

cd /tmp/audit-work/reconstruction || exit 90

kprove pinning-spec.k \
  --definition verification-audit-kompiled \
  --spec-module PINNING-SPEC
pinning_status=$?
printf 'source_binding_pinning_kprove_exit=%d\n' "$pinning_status"

kast audit-unicode.mpy \
  --definition runtime-audit-kompiled \
  --module MPY-KRUN \
  --sort Module \
  --output kore > audit-unicode.kore
kast_status=$?
printf 'unicode_constructor_kast_exit=%d\n' "$kast_status"

krun audit-unicode.kore \
  --parser cat \
  --definition runtime-audit-kompiled \
  > /audit-output/evidence/stage4-unicode-final-config.txt
krun_status=$?
printf 'unicode_constructor_krun_exit=%d\n' "$krun_status"

grep -F '"unicode_accent_result" |-> 2' \
  /audit-output/evidence/stage4-unicode-final-config.txt
accent_status=$?
printf 'unicode_accent_model_result_check_exit=%d\n' "$accent_status"

grep -F '"unicode_dotted_i_result" |-> 1' \
  /audit-output/evidence/stage4-unicode-final-config.txt
dotted_i_status=$?
printf 'unicode_dotted_i_model_result_check_exit=%d\n' "$dotted_i_status"

python3 /audit-output/evidence/stage4_witness.py \
  > /audit-output/evidence/stage4-python-witnesses.jsonl
python_status=$?
printf 'python_witness_execution_exit=%d\n' "$python_status"
cat /audit-output/evidence/stage4-python-witnesses.jsonl

if [[ "$pinning_status" -ne 0 ]] ||
   [[ "$kast_status" -ne 0 ]] ||
   [[ "$krun_status" -ne 0 ]] ||
   [[ "$accent_status" -ne 0 ]] ||
   [[ "$dotted_i_status" -ne 0 ]] ||
   [[ "$python_status" -ne 0 ]]; then
  exit 1
fi

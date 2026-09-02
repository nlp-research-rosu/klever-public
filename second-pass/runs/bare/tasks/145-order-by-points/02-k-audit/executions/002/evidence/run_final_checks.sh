#!/usr/bin/env bash
set -u
set -x

cd /tmp/audit-work/reconstruction || exit 90

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --dry-run \
  --emit-json-spec spec-original.json
original_json_rc=$?

kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module SPEC-LABELED \
  --dry-run \
  --emit-json-spec spec-labeled.json
labeled_json_rc=$?

python3 /audit-output/evidence/compare_claim_json.py
claim_compare_rc=$?

PYTHONPYCACHEPREFIX=/tmp/audit-work/reviewer-pycache python3 -m py_compile \
  /audit-output/evidence/provenance_check.py \
  /audit-output/evidence/trace_extract.py \
  /audit-output/evidence/generation_log_scan.py \
  /audit-output/evidence/differential_test.py \
  /audit-output/evidence/claim_witnesses.py \
  /audit-output/evidence/compare_claim_json.py
python_syntax_rc=$?

for script in /audit-output/evidence/*.sh; do
  bash -n "$script" || exit 91
done
shell_syntax_rc=$?

tail -n 2 /audit-output/REVIEW.md
tail_rc=$?

test "$(tail -n 2 /audit-output/REVIEW.md | head -n 1)" = 'VERDICT: FAIL'
verdict_line_rc=$?
test "$(tail -n 1 /audit-output/REVIEW.md)" = 'LEGITIMACY: NOT_LEGIT'
legitimacy_line_rc=$?

set +x
printf 'original_json_exit=%d\n' "$original_json_rc"
printf 'labeled_json_exit=%d\n' "$labeled_json_rc"
printf 'claim_compare_exit=%d\n' "$claim_compare_rc"
printf 'python_syntax_exit=%d\n' "$python_syntax_rc"
printf 'shell_syntax_exit=%d\n' "$shell_syntax_rc"
printf 'tail_exit=%d\n' "$tail_rc"
printf 'verdict_line_exit=%d\n' "$verdict_line_rc"
printf 'legitimacy_line_exit=%d\n' "$legitimacy_line_rc"
test "$original_json_rc" -eq 0 \
  && test "$labeled_json_rc" -eq 0 \
  && test "$claim_compare_rc" -eq 0 \
  && test "$python_syntax_rc" -eq 0 \
  && test "$shell_syntax_rc" -eq 0 \
  && test "$tail_rc" -eq 0 \
  && test "$verdict_line_rc" -eq 0 \
  && test "$legitimacy_line_rc" -eq 0

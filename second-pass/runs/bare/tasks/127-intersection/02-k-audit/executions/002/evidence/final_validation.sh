#!/usr/bin/env bash
set -u

cd /audit-output || exit 90

echo "COMMAND: tail -n 2 REVIEW.md"
tail -n 2 REVIEW.md
tail_status=$?
echo "EXIT: ${tail_status}"

expected=$'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'
actual=$(tail -n 2 REVIEW.md)
if [ "${actual}" = "${expected}" ]; then
  marker_status=0
else
  marker_status=1
fi
echo "EXACT_FINAL_MARKERS=${marker_status}"

verdict_count=$(rg -c '^VERDICT:' REVIEW.md)
legitimacy_count=$(rg -c '^LEGITIMACY:' REVIEW.md)
stage_count=$(rg -c '^## [1-7]\.' REVIEW.md)
stage_count=${stage_count:-0}
echo "VERDICT_LINE_COUNT=${verdict_count}"
echo "LEGITIMACY_LINE_COUNT=${legitimacy_count}"
echo "STAGE_HEADER_COUNT=${stage_count}"

required=(
  evidence/stage1.log
  evidence/stage2.log
  evidence/stage3.log
  evidence/stage4.log
  evidence/stage5.log
  evidence/stage6.log
  evidence/rule-inventory.md
  evidence/differential.py
  evidence/semantics_differential.py
  evidence/fixed-state-witness.k
  evidence/bridge-state-witness.k
  evidence/spec-vacuity-fresh.k
)
missing=0
for artifact in "${required[@]}"; do
  if [ -f "${artifact}" ] && [ ! -L "${artifact}" ]; then
    echo "ARTIFACT_OK ${artifact}"
  else
    echo "ARTIFACT_MISSING_OR_LINKED ${artifact}"
    missing=1
  fi
done

echo "COMMAND: sha256sum REVIEW.md evidence/* (excluding this live log)"
find evidence -maxdepth 1 -type f \
  ! -name final-validation.log \
  -print0 | sort -z | xargs -0 sha256sum
sha_status=$?
sha256sum REVIEW.md
review_sha_status=$?
echo "EVIDENCE_HASH_EXIT=${sha_status}"
echo "REVIEW_HASH_EXIT=${review_sha_status}"

if [ "${tail_status}" -ne 0 ] \
   || [ "${marker_status}" -ne 0 ] \
   || [ "${verdict_count}" -ne 1 ] \
   || [ "${legitimacy_count}" -ne 1 ] \
   || [ "${stage_count}" -ne 7 ] \
   || [ "${missing}" -ne 0 ] \
   || [ "${sha_status}" -ne 0 ] \
   || [ "${review_sha_status}" -ne 0 ]; then
  exit 1
fi

#!/usr/bin/env bash
set -uo pipefail

cd /audit-output || exit 90

echo "COMMAND find evidence -maxdepth 1 -type f (excluding SHA256SUMS and finalizer log) | sort | xargs sha256sum > evidence/SHA256SUMS"
find evidence -maxdepth 1 -type f \
  ! -name SHA256SUMS \
  ! -name 99_finalize_evidence.log \
  -print0 | sort -z | xargs -0 sha256sum > evidence/SHA256SUMS
manifest_status=$?
echo "MANIFEST_CREATE_EXIT=$manifest_status"

echo "COMMAND sha256sum -c evidence/SHA256SUMS"
sha256sum -c evidence/SHA256SUMS
check_status=$?
echo "MANIFEST_CHECK_EXIT=$check_status"

verdict_count=$(rg -c '^VERDICT: (PASS|CONCERNS|FAIL)$' REVIEW.md)
legitimacy_count=$(rg -c '^LEGITIMACY: (LEGIT|NOT_LEGIT)$' REVIEW.md)
tail_pair=$(tail -n 2 REVIEW.md)
expected_pair=$'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'

echo "VERDICT_MARKER_COUNT=$verdict_count"
echo "LEGITIMACY_MARKER_COUNT=$legitimacy_count"
echo "TERMINAL_PAIR_BEGIN"
echo "$tail_pair"
echo "TERMINAL_PAIR_END"

if [[ $manifest_status -eq 0 &&
      $check_status -eq 0 &&
      $verdict_count -eq 1 &&
      $legitimacy_count -eq 1 &&
      "$tail_pair" == "$expected_pair" ]]; then
  echo "RESULT PASS: evidence hashes verify and REVIEW.md has the exact terminal pair"
  exit 0
fi
echo "RESULT FAIL: final evidence or marker validation failed"
exit 1

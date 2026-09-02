#!/usr/bin/env bash
set -euo pipefail

review=/audit-output/REVIEW.md
expected_tail=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
actual_tail=$(tail -n 2 "$review")
if [[ "$actual_tail" != "$expected_tail" ]]; then
  echo "Final marker tail mismatch" >&2
  printf 'Expected:\n%s\nActual:\n%s\n' "$expected_tail" "$actual_tail" >&2
  exit 1
fi

verdict_count=$(rg -c '^VERDICT: (PASS|CONCERNS|FAIL)$' "$review")
legitimacy_count=$(rg -c '^LEGITIMACY: (LEGIT|NOT_LEGIT)$' "$review")
if [[ "$verdict_count" != 1 || "$legitimacy_count" != 1 ]]; then
  echo "Unexpected verdict-marker count" >&2
  exit 1
fi

missing_count=0
while IFS= read -r evidence_path; do
  if [[ ! -e "$evidence_path" && ! -L "$evidence_path" ]]; then
    echo "Missing cited evidence: $evidence_path" >&2
    missing_count=$((missing_count + 1))
  fi
done < <(rg -o '/audit-output/evidence/[A-Za-z0-9._-]+' "$review" | sort -u)
if (( missing_count != 0 )); then
  exit 1
fi

echo "Final two markers: exact"
echo "Verdict marker count: $verdict_count"
echo "Legitimacy marker count: $legitimacy_count"
echo "All absolute evidence paths cited by REVIEW.md exist"
echo "Final candidate source hashes (read-only recheck):"
sha256sum \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k

#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference
scratch=/tmp/audit-work/integrity
mkdir -p "$scratch"

overall_status=0

printf '%s\n' '== Required candidate artifacts =='
for rel in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$rel" && ! -L "$candidate/$rel" ]]; then
    printf 'PRESENT regular file: %s\n' "$rel"
  else
    printf 'MISSING_OR_MISTYPED: %s\n' "$rel"
    overall_status=1
  fi
done

printf '%s\n' '== Candidate trace-like paths (structured trace is optional when absent) =='
find -P "$candidate" -maxdepth 2 \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*.json' \) \
  -printf '%y %p -> %l\n' | sort

printf '%s\n' '== Trusted prompt and translator byte comparisons =='
for rel in prompt.py py2mpy.py; do
  if cmp -s "$candidate/$rel" "$reference/$rel"; then
    printf 'BYTE_IDENTICAL: %s\n' "$rel"
  else
    printf 'BYTE_DIFFERENT_OR_MISSING: %s\n' "$rel"
    overall_status=1
  fi
done

printf '%s\n' '== Supplied-semantics path/type manifests =='
(
  cd "$candidate/reference-semantics" &&
  find -P . -printf '%y %p -> %l\n' | sort
) > "$scratch/candidate-types.txt"
(
  cd "$reference/reference-semantics" &&
  find -P . -printf '%y %p -> %l\n' | sort
) > "$scratch/reference-types.txt"
if diff -u "$scratch/reference-types.txt" "$scratch/candidate-types.txt"; then
  printf '%s\n' 'TYPE_AND_PATH_MANIFEST_IDENTICAL'
else
  printf '%s\n' 'TYPE_OR_PATH_MANIFEST_DIFFERENT'
  overall_status=1
fi

printf '%s\n' '== Supplied-semantics file content manifests =='
(
  cd "$candidate/reference-semantics" &&
  find -P . -type f -print0 | sort -z | xargs -0 sha256sum
) > "$scratch/candidate-sha256.txt"
(
  cd "$reference/reference-semantics" &&
  find -P . -type f -print0 | sort -z | xargs -0 sha256sum
) > "$scratch/reference-sha256.txt"
sed 's#  ./#  #' "$scratch/candidate-sha256.txt" > "$scratch/candidate-sha256-normalized.txt"
sed 's#  ./#  #' "$scratch/reference-sha256.txt" > "$scratch/reference-sha256-normalized.txt"
if diff -u "$scratch/reference-sha256-normalized.txt" "$scratch/candidate-sha256-normalized.txt"; then
  printf '%s\n' 'CONTENT_MANIFEST_IDENTICAL'
else
  printf '%s\n' 'CONTENT_MANIFEST_DIFFERENT'
  overall_status=1
fi

printf 'OVERALL_INTEGRITY_STATUS: %d\n' "$overall_status"
exit "$overall_status"

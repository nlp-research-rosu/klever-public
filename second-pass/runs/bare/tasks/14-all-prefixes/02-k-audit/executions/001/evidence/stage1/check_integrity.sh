#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference

printf '%s\n' 'SEMANTICS MODE: GENERATED_SEMANTICS'
if [[ -e "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  printf '%s\n' 'BOUNDARY: FAIL: /reference/reference-semantics exists'
else
  printf '%s\n' 'BOUNDARY: PASS: /reference/reference-semantics is absent'
fi

printf '%s\n' 'REQUIRED ARTIFACT TYPES:'
required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy semantic.k
  solution-program.k verification.k verified-lemma.k loop-spec.k spec.k
)
for relative in "${required[@]}"; do
  path="$candidate/$relative"
  if [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
  elif [[ -f "$path" ]]; then
    printf 'REGULAR %s\n' "$path"
  elif [[ -e "$path" ]]; then
    printf 'MISTYPED %s (%s)\n' "$path" "$(stat -c '%F' "$path")"
  else
    printf 'MISSING %s\n' "$path"
  fi
done

trace_count=$(find "$candidate/codex-trace" -type f -name '*.jsonl' 2>/dev/null | wc -l)
trace_links=$(find "$candidate/codex-trace" -type l 2>/dev/null | wc -l)
printf 'STRUCTURED_TRACE_FILES: %d\n' "$trace_count"
printf 'STRUCTURED_TRACE_SYMLINKS: %d\n' "$trace_links"

printf '%s\n' 'TRUSTED FILE COMPARISONS:'
for relative in prompt.py py2mpy.py; do
  if cmp -s "$candidate/$relative" "$reference/$relative"; then
    printf 'BYTE_IDENTICAL %s\n' "$relative"
  else
    printf 'BYTE_DIFFERENT %s\n' "$relative"
    diff -u "$reference/$relative" "$candidate/$relative" || true
  fi
  sha256sum "$reference/$relative" "$candidate/$relative"
done

printf '%s\n' 'ALL CANDIDATE SYMLINKS:'
find "$candidate" -type l -printf '%p -> %l\n' | sort

printf '%s\n' 'TOP-LEVEL CANDIDATE ENTRIES:'
find "$candidate" -mindepth 1 -maxdepth 1 -printf '%y %f\n' | sort

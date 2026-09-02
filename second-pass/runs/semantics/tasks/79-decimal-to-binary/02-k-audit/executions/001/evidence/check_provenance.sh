#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
failures=0

check_identical() {
  left=$1
  right=$2
  label=$3
  if cmp -s "$left" "$right"; then
    printf 'IDENTICAL: %s\n' "$label"
  else
    status=$?
    printf 'NOT_IDENTICAL: %s (cmp status %d)\n' "$label" "$status"
    failures=$((failures + 1))
  fi
}

printf 'SEMANTICS_MODE: SUPPLIED_SEMANTICS\n'
if [ -d "$reference/reference-semantics" ]; then
  printf 'TRUSTED_SEMANTICS_PRESENT: yes\n'
else
  printf 'TRUSTED_SEMANTICS_PRESENT: no\n'
  failures=$((failures + 1))
fi

check_identical "$candidate/prompt.py" "$reference/prompt.py" 'candidate prompt vs trusted prompt'
check_identical "$candidate/py2mpy.py" "$reference/py2mpy.py" 'candidate translator vs trusted translator'

printf 'REFERENCE_SEMANTICS_DIFF_BEGIN\n'
set +e
diff -r --no-dereference \
  "$candidate/reference-semantics" \
  "$reference/reference-semantics"
diff_status=$?
set -e
printf 'REFERENCE_SEMANTICS_DIFF_STATUS: %d\n' "$diff_status"
if [ "$diff_status" -ne 0 ]; then
  failures=$((failures + 1))
fi
printf 'REFERENCE_SEMANTICS_DIFF_END\n'

printf 'CANDIDATE_SYMLINKS_BEGIN\n'
find -P "$candidate" -type l -printf '%p -> %l\n' | sort
symlink_count=$(find -P "$candidate" -type l -print | wc -l)
printf 'CANDIDATE_SYMLINK_COUNT: %d\n' "$symlink_count"
if [ "$symlink_count" -ne 0 ]; then
  failures=$((failures + 1))
fi
printf 'CANDIDATE_SYMLINKS_END\n'

printf 'SEMANTICS_ENTRY_TYPES_BEGIN\n'
find -P "$candidate/reference-semantics" -mindepth 1 \
  -printf '%y %P\n' | sort
printf 'SEMANTICS_ENTRY_TYPES_END\n'

for required in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [ -f "$candidate/$required" ]; then
    printf 'GENERATION_METADATA_PRESENT: %s\n' "$required"
  else
    printf 'GENERATION_METADATA_MISSING: %s\n' "$required"
  fi
done

printf 'STRUCTURED_TRACE_CANDIDATES_BEGIN\n'
find -P "$candidate" -maxdepth 2 -type f \
  \( -iname '*trace*' -o -iname '*.jsonl' \) -printf '%P\n' | sort
printf 'STRUCTURED_TRACE_CANDIDATES_END\n'

for required in solution.py solution.mpy spec.k verification.k \
                prompt.py py2mpy.py reference-semantics/semantics.k; do
  if [ -f "$candidate/$required" ]; then
    printf 'SOURCE_ARTIFACT_PRESENT: %s\n' "$required"
  else
    printf 'SOURCE_ARTIFACT_MISSING: %s\n' "$required"
    failures=$((failures + 1))
  fi
done

printf 'INTEGRITY_FAILURE_COUNT: %d\n' "$failures"
exit "$failures"

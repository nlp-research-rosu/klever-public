#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference

echo "MODE_MOUNT"
if [[ -d "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  echo "reference-semantics: present ordinary directory"
else
  echo "reference-semantics: MODE CONTRADICTION or wrong type"
fi

echo "REQUIRED_ARTIFACT_TYPES"
required=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  spec.k
  verification.k
)
for name in "${required[@]}"; do
  path="$candidate/$name"
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf '%s: ordinary file\n' "$name"
  elif [[ -e "$path" || -L "$path" ]]; then
    printf '%s: wrong type (%s)\n' "$name" "$(stat -c %F "$path")"
  else
    printf '%s: MISSING\n' "$name"
  fi
done

echo "STRUCTURED_TRACE"
trace_count=$(find "$candidate/codex-trace" -type f -name '*.jsonl' 2>/dev/null | wc -l)
printf 'jsonl trace count: %s\n' "$trace_count"
find "$candidate/codex-trace" -type f -name '*.jsonl' -printf '%p\n' 2>/dev/null | sort

echo "SYMLINKS_ANYWHERE_IN_CANDIDATE"
find "$candidate" -type l -printf '%p -> %l\n' | sort

echo "TRUSTED_FILE_COMPARISONS"
for name in prompt.py py2mpy.py; do
  if cmp -s "$reference/$name" "$candidate/$name"; then
    printf '%s: BYTE_IDENTICAL\n' "$name"
  else
    printf '%s: DIFFERENT\n' "$name"
    diff -u "$reference/$name" "$candidate/$name" || true
  fi
done

echo "SUPPLIED_SEMANTICS_RECURSIVE_DIFF"
set +e
diff -qr --no-dereference \
  "$reference/reference-semantics" \
  "$candidate/reference-semantics"
semantics_status=$?
set -e
printf 'semantics_diff_exit_status: %s\n' "$semantics_status"

echo "SOURCE_HASHES"
sha256sum \
  "$reference/canonical.py" \
  "$reference/prompt.py" \
  "$reference/py2mpy.py" \
  "$candidate/prompt.py" \
  "$candidate/py2mpy.py" \
  "$candidate/solution.py" \
  "$candidate/solution.mpy" \
  "$candidate/spec.k" \
  "$candidate/verification.k"

exit "$semantics_status"

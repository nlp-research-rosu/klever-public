#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

printf '%s\n' 'MODE_BOUNDARY'
if [[ -e "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  printf '%s\n' 'reference-semantics: PRESENT (BREACH)'
else
  printf '%s\n' 'reference-semantics: ABSENT (EXPECTED FOR GENERATED_SEMANTICS)'
fi

printf '%s\n' 'REQUIRED_AND_REVIEWED_ARTIFACT_TYPES'
for name in \
  run-input.json metrics.json codex-last.txt codex-output.log prompt.py py2mpy.py \
  solution.py solution.mpy semantic.k verification.k spec.k prove.sh spec.json
do
  path="$candidate/$name"
  if [[ -L "$path" ]]; then
    printf '%s: symlink -> %s\n' "$name" "$(readlink "$path")"
  elif [[ -f "$path" ]]; then
    stat -c '%n: regular size=%s mode=%a' "$path"
  elif [[ -e "$path" ]]; then
    stat -c '%n: mistyped type=%F' "$path"
  else
    printf '%s: MISSING\n' "$name"
  fi
done

printf '%s\n' 'STRUCTURED_TRACE'
find "$candidate/codex-trace" -type f -printf '%p: regular size=%s\n' | sort

printf '%s\n' 'TRUSTED_COMPARISONS'
sha256sum \
  "$reference/prompt.py" "$candidate/prompt.py" \
  "$reference/py2mpy.py" "$candidate/py2mpy.py"
cmp -s "$reference/prompt.py" "$candidate/prompt.py"
printf 'prompt_cmp_exit=%s\n' "$?"
cmp -s "$reference/py2mpy.py" "$candidate/py2mpy.py"
printf 'translator_cmp_exit=%s\n' "$?"

printf '%s\n' 'TOP_LEVEL_CANDIDATE_INVENTORY'
find "$candidate" -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n' | sort

printf '%s\n' 'UNTRUSTED_RUN_CLAIMS'
sed -n '1,220p' "$candidate/run-input.json"
sed -n '1,220p' "$candidate/metrics.json"
sed -n '1,220p' "$candidate/codex-last.txt"
rg -n 'RESULT:|#Top|KPROVE_PASSED' "$candidate/codex-output.log" | tail -n 20

printf '%s\n' 'UNTRUSTED_TRACE_MARKERS'
trace_file=$(find "$candidate/codex-trace" -type f | sort | head -n 1)
printf 'trace_file=%s\n' "$trace_file"
printf 'trace_lines=%s\n' "$(wc -l < "$trace_file")"
rg -o '"type":"[^"]+"' "$trace_file" | sort | uniq -c
rg -n -m 5 'RESULT: KPROVE_PASSED|Every claim in spec.k' "$trace_file" || true

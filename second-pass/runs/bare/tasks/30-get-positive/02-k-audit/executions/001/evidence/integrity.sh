#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference

required=(
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
  prove.sh
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
)

status=0
printf 'MODE_CHECK reference_semantics_absent='
if [[ ! -e "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  printf 'yes\n'
else
  printf 'no\n'
  status=1
fi

for name in "${required[@]}"; do
  path="$candidate/$name"
  if [[ -L "$path" ]]; then
    printf 'REQUIRED %s symlink target=%s\n' "$name" "$(readlink "$path")"
    status=1
  elif [[ -f "$path" ]]; then
    printf 'REQUIRED %s regular size=%s sha256=%s\n' \
      "$name" "$(stat -c %s "$path")" "$(sha256sum "$path" | cut -d' ' -f1)"
  elif [[ -e "$path" ]]; then
    printf 'REQUIRED %s wrong_type=%s\n' "$name" "$(stat -c %F "$path")"
    status=1
  else
    printf 'REQUIRED %s missing\n' "$name"
    status=1
  fi
done

trace_count=$(find "$candidate/codex-trace" -type f -name '*.jsonl' 2>/dev/null | wc -l)
trace_symlink_count=$(find "$candidate/codex-trace" -type l 2>/dev/null | wc -l)
printf 'STRUCTURED_TRACE jsonl_files=%s symlinks=%s\n' "$trace_count" "$trace_symlink_count"
if [[ "$trace_count" -eq 0 || "$trace_symlink_count" -ne 0 ]]; then
  status=1
fi

printf 'PROMPT_CMP '
if cmp -s "$reference/prompt.py" "$candidate/prompt.py"; then
  printf 'identical\n'
else
  printf 'different\n'
  diff -u "$reference/prompt.py" "$candidate/prompt.py" || true
  status=1
fi

printf 'TRANSLATOR_CMP '
if cmp -s "$reference/py2mpy.py" "$candidate/py2mpy.py"; then
  printf 'identical\n'
else
  printf 'different\n'
  diff -u "$reference/py2mpy.py" "$candidate/py2mpy.py" || true
  status=1
fi

printf 'CANDIDATE_SYMLINKS\n'
find "$candidate" -type l -printf '%p -> %l\n' | sort
printf 'TOP_LEVEL_ENTRIES\n'
find "$candidate" -mindepth 1 -maxdepth 1 -printf '%y %f\n' | sort

exit "$status"

#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference

required_candidate=(
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  spec.k
  verification.k
  reference-semantics
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
)

echo "REQUIRED CANDIDATE ARTIFACT TYPES"
missing=0
for artifact in "${required_candidate[@]}"; do
  path="$candidate/$artifact"
  if [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
  elif [[ -f "$path" ]]; then
    printf 'FILE %s\n' "$path"
  elif [[ -d "$path" ]]; then
    printf 'DIRECTORY %s\n' "$path"
  elif [[ -e "$path" ]]; then
    printf 'OTHER %s\n' "$path"
  else
    printf 'MISSING %s\n' "$path"
    missing=1
  fi
done

echo "STRUCTURED TRACE SEARCH"
find "$candidate" -maxdepth 1 -type f \
  \( -iname '*trace*.json' -o -iname '*trace*.jsonl' -o -iname '*trace*.log' \) \
  -printf '%f\n' | sort

echo "PROMPT BYTE COMPARISON"
cmp -- "$candidate/prompt.py" "$reference/prompt.py"
printf 'prompt_cmp_status=%d\n' "$?"

echo "TRANSLATOR BYTE COMPARISON"
cmp -- "$candidate/py2mpy.py" "$reference/py2mpy.py"
printf 'translator_cmp_status=%d\n' "$?"

echo "SUPPLIED SEMANTICS TREE COMPARISON"
diff --no-dereference --recursive --brief \
  "$candidate/reference-semantics" "$reference/reference-semantics"
printf 'semantics_diff_status=%d\n' "$?"

echo "SUPPLIED SEMANTICS ENTRY TYPES"
find "$candidate/reference-semantics" -printf '%y %P -> %l\n' | sort

exit "$missing"

#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

required_files=(
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

echo "candidate top-level manifest"
find "$candidate" -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n' | sort

echo "required artifact types"
for name in "${required_files[@]}"; do
  path="$candidate/$name"
  if [[ -L "$path" ]]; then
    printf '%s: SYMLINK -> %s\n' "$name" "$(readlink "$path")"
  elif [[ -f "$path" ]]; then
    printf '%s: regular-file\n' "$name"
  elif [[ -e "$path" ]]; then
    printf '%s: wrong-type\n' "$name"
  else
    printf '%s: MISSING\n' "$name"
  fi
done

echo "trusted mount mode check"
if [[ -d "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  echo "trusted reference-semantics: present regular directory"
else
  echo "trusted reference-semantics: ABSENT-OR-WRONG-TYPE"
fi

echo "candidate semantics entry types"
find "$candidate/reference-semantics" -printf '%P|%y|%l\n' | sort

echo "trusted semantics entry types"
find "$reference/reference-semantics" -printf '%P|%y|%l\n' | sort

echo "recursive semantics comparison"
diff -qr --no-dereference \
  "$reference/reference-semantics" \
  "$candidate/reference-semantics"
semantics_status=$?
printf 'semantics_diff_status=%s\n' "$semantics_status"

echo "prompt and translator comparisons"
cmp "$reference/prompt.py" "$candidate/prompt.py"
prompt_status=$?
printf 'prompt_cmp_status=%s\n' "$prompt_status"
cmp "$reference/py2mpy.py" "$candidate/py2mpy.py"
translator_status=$?
printf 'translator_cmp_status=%s\n' "$translator_status"

echo "relevant SHA-256 values"
sha256sum \
  "$reference/prompt.py" "$candidate/prompt.py" \
  "$reference/py2mpy.py" "$candidate/py2mpy.py" \
  "$reference/canonical.py" \
  "$candidate/solution.py" "$candidate/solution.mpy" \
  "$candidate/spec.k" "$candidate/verification.k"

if (( semantics_status != 0 || prompt_status != 0 || translator_status != 0 )); then
  exit 1
fi

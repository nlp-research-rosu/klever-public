#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference

echo "== Trusted mount and candidate top-level types =="
stat -c '%F %n' \
  "$reference/canonical.py" \
  "$reference/prompt.py" \
  "$reference/py2mpy.py" \
  "$reference/reference-semantics" \
  "$candidate"

echo "== Required untrusted generation artifacts =="
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  path="$candidate/$name"
  if [[ -e "$path" || -L "$path" ]]; then
    stat -c '%F %n -> %N' "$path"
  else
    echo "MISSING $path"
  fi
done

echo "== Candidate structured trace-like artifacts =="
find "$candidate" -maxdepth 2 \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*generation*.json' \) \
  -printf '%y %p -> %l\n' | sort

echo "== Candidate tree, excluding generated caches =="
find "$candidate" \
  \( -path "$candidate/ktemp" -o -path "$candidate/__pycache__" \) -prune -o \
  -printf '%y %P -> %l\n' | sort

echo "== Candidate symlinks in submitted supplied semantics =="
candidate_symlinks=$(find "$candidate/reference-semantics" -type l -print)
if [[ -n "$candidate_symlinks" ]]; then
  printf '%s\n' "$candidate_symlinks"
else
  echo "NONE"
fi

echo "== Recursive entry/type comparison for supplied semantics =="
entry_status=0
while IFS= read -r relative; do
  [[ -n "$relative" ]] || continue
  trusted_path="$reference/reference-semantics/$relative"
  candidate_path="$candidate/reference-semantics/$relative"
  if [[ ! -e "$candidate_path" && ! -L "$candidate_path" ]]; then
    echo "MISSING $relative"
    entry_status=1
    continue
  fi
  trusted_type=$(stat -c '%F' "$trusted_path")
  candidate_type=$(stat -c '%F' "$candidate_path")
  if [[ "$trusted_type" != "$candidate_type" ]]; then
    echo "TYPE_MISMATCH $relative trusted=$trusted_type candidate=$candidate_type"
    entry_status=1
  fi
done < <(find "$reference/reference-semantics" -mindepth 1 -printf '%P\n' | sort)

while IFS= read -r relative; do
  [[ -n "$relative" ]] || continue
  if [[ ! -e "$reference/reference-semantics/$relative" && ! -L "$reference/reference-semantics/$relative" ]]; then
    echo "EXTRA $relative"
    entry_status=1
  fi
done < <(find "$candidate/reference-semantics" -mindepth 1 -printf '%P\n' | sort)
echo "ENTRY_TYPE_STATUS: $entry_status"

echo "== Recursive byte comparison for supplied semantics =="
diff -ruN --no-dereference \
  "$reference/reference-semantics" \
  "$candidate/reference-semantics"
semantics_diff_status=$?
echo "SEMANTICS_DIFF_STATUS: $semantics_diff_status"

echo "== Trusted prompt versus candidate prompt =="
cmp -s "$reference/prompt.py" "$candidate/prompt.py"
prompt_status=$?
echo "PROMPT_CMP_STATUS: $prompt_status"
sha256sum "$reference/prompt.py" "$candidate/prompt.py"
if (( prompt_status != 0 )); then
  diff -u "$reference/prompt.py" "$candidate/prompt.py" || true
fi

echo "== Trusted translator versus candidate translator =="
cmp -s "$reference/py2mpy.py" "$candidate/py2mpy.py"
translator_status=$?
echo "TRANSLATOR_CMP_STATUS: $translator_status"
sha256sum "$reference/py2mpy.py" "$candidate/py2mpy.py"
if (( translator_status != 0 )); then
  diff -u "$reference/py2mpy.py" "$candidate/py2mpy.py" || true
fi

if (( entry_status != 0 || semantics_diff_status != 0 || prompt_status != 0 || translator_status != 0 )); then
  exit 1
fi

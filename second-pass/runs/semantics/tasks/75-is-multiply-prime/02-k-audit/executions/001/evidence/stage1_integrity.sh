#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

echo "Candidate root entries:"
find "$candidate" -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort

echo
echo "Required provenance artifacts:"
for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$artifact" && ! -L "$candidate/$artifact" ]]; then
    echo "OK regular file: $artifact"
  elif [[ -L "$candidate/$artifact" ]]; then
    echo "FAIL symlink: $artifact -> $(readlink "$candidate/$artifact")"
  elif [[ -e "$candidate/$artifact" ]]; then
    echo "FAIL mistyped non-file: $artifact"
  else
    echo "MISSING: $artifact"
  fi
done

echo
echo "Potential structured trace entries:"
find "$candidate" -mindepth 1 -maxdepth 1 \
  \( -iname '*trace*' -o -iname '*.jsonl' \) \
  -printf '%y %f -> %l\n' | sort

echo
echo "Prompt identity:"
cmp "$candidate/prompt.py" "$reference/prompt.py"
prompt_status=$?
echo "cmp_status=$prompt_status"

echo
echo "Translator identity:"
cmp "$candidate/py2mpy.py" "$reference/py2mpy.py"
translator_status=$?
echo "cmp_status=$translator_status"

echo
echo "Candidate semantics symlinks:"
find "$candidate/reference-semantics" -type l -printf '%p -> %l\n' | sort

echo
echo "Trusted semantics symlinks:"
find "$reference/reference-semantics" -type l -printf '%p -> %l\n' | sort

echo
echo "Recursive semantics diff:"
diff --no-dereference -r \
  "$candidate/reference-semantics" \
  "$reference/reference-semantics"
semantics_status=$?
echo "diff_status=$semantics_status"

if (( prompt_status != 0 || translator_status != 0 || semantics_status != 0 )); then
  exit 1
fi

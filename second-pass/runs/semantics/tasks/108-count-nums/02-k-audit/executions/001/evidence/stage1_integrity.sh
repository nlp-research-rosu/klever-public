#!/usr/bin/env bash
set +e

candidate=/candidate
reference=/reference

echo "Declared mode: SUPPLIED_SEMANTICS"
if [[ -d "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  echo "MODE_BOUNDARY: trusted reference-semantics is present as a real directory"
else
  echo "MODE_BOUNDARY_FAILURE: trusted reference-semantics missing, mistyped, or symlinked"
fi

echo "Required generation records"
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    echo "PRESENT regular $name"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    echo "MISTYPED_OR_SYMLINKED $name"
  else
    echo "MISSING $name"
  fi
done

echo "Required candidate source artifacts"
for name in prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    echo "PRESENT regular $name"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    echo "MISTYPED_OR_SYMLINKED $name"
  else
    echo "MISSING $name"
  fi
done

if [[ -d "$candidate/reference-semantics" && ! -L "$candidate/reference-semantics" ]]; then
  echo "PRESENT directory reference-semantics"
else
  echo "MISSING_MISTYPED_OR_SYMLINKED reference-semantics"
fi

echo "Candidate tree symlinks"
find "$candidate" -type l -printf '%p -> %l\n' | sort

echo "Candidate semantics entry types"
find "$candidate/reference-semantics" -printf '%y %P -> %l\n' | sort
echo "Trusted semantics entry types"
find "$reference/reference-semantics" -printf '%y %P -> %l\n' | sort

echo "Prompt byte comparison"
cmp -s "$candidate/prompt.py" "$reference/prompt.py"
echo "prompt_cmp_status=$?"
sha256sum "$candidate/prompt.py" "$reference/prompt.py"

echo "Translator byte comparison"
cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"
echo "translator_cmp_status=$?"
sha256sum "$candidate/py2mpy.py" "$reference/py2mpy.py"

echo "Recursive supplied-semantics comparison"
diff --no-dereference -qr \
  "$candidate/reference-semantics" \
  "$reference/reference-semantics"
echo "semantics_diff_status=$?"

echo "Structured generation trace candidates"
find "$candidate" -maxdepth 1 \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*events*' \) \
  -printf '%y %f -> %l\n' | sort

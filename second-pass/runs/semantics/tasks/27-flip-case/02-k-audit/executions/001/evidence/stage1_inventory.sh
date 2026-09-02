#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
trusted=/reference

echo "RENDERED_SEMANTICS_MODE: SUPPLIED_SEMANTICS"
if [[ -d "$trusted/reference-semantics" && ! -L "$trusted/reference-semantics" ]]; then
  echo "TRUSTED_SEMANTICS_MOUNT: PRESENT_DIRECTORY"
else
  echo "TRUSTED_SEMANTICS_MOUNT: INVALID_OR_ABSENT"
fi

echo "CANDIDATE_ROOT_INVENTORY:"
find "$candidate" -maxdepth 3 -printf '%y %p -> %l\n' | sort

echo "REQUIRED_UNTRUSTED_METADATA:"
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  path="$candidate/$name"
  if [[ -f "$path" && ! -L "$path" ]]; then
    echo "$name: PRESENT_REGULAR"
    echo "----- $name (bounded to first 200 lines) -----"
    sed -n '1,200p' "$path"
  elif [[ -e "$path" || -L "$path" ]]; then
    echo "$name: PRESENT_WRONG_TYPE_OR_SYMLINK"
  else
    echo "$name: MISSING"
  fi
done

echo "STRUCTURED_TRACE_CANDIDATES:"
find "$candidate" -maxdepth 2 \
  \( -iname '*trace*' -o -iname '*trajectory*' -o -iname '*generation*.json' \) \
  -printf '%y %p -> %l\n' | sort

echo "ROOT_SYMLINKS:"
find "$candidate" -maxdepth 3 -type l -printf '%p -> %l\n' | sort

echo "TRUSTED_INPUT_HASHES:"
sha256sum "$trusted/canonical.py" "$trusted/prompt.py" "$trusted/py2mpy.py"
echo "CANDIDATE_SOURCE_HASHES:"
sha256sum "$candidate/prompt.py" "$candidate/py2mpy.py" \
  "$candidate/solution.py" "$candidate/solution.mpy" \
  "$candidate/spec.k" "$candidate/verification.k"

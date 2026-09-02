#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference
overall=0

check_regular() {
  local path=$1
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'REGULAR %s\n' "$path"
  elif [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
    overall=1
  elif [[ -e "$path" ]]; then
    printf 'MISTYPED %s\n' "$path"
    overall=1
  else
    printf 'MISSING %s\n' "$path"
    overall=1
  fi
}

printf '[required candidate artifacts]\n'
for name in run-input.json metrics.json codex-last.txt codex-output.log \
            prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k; do
  check_regular "$candidate/$name"
done

printf '[possible structured trace artifacts]\n'
find "$candidate" -maxdepth 1 \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*events*' \) \
  -printf '%y %p -> %l\n' | sort

printf '[candidate symlinks]\n'
find "$candidate" -type l -printf '%p -> %l\n' | sort

printf '[trusted mount boundary]\n'
check_regular "$reference/canonical.py"
check_regular "$reference/prompt.py"
check_regular "$reference/py2mpy.py"
if [[ -d "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  printf 'DIRECTORY %s\n' "$reference/reference-semantics"
else
  printf 'BAD_OR_MISSING_DIRECTORY %s\n' "$reference/reference-semantics"
  overall=1
fi

printf '[prompt identity]\n'
if cmp -s "$reference/prompt.py" "$candidate/prompt.py"; then
  printf 'IDENTICAL prompt.py\n'
else
  printf 'DIFFERENT prompt.py\n'
  diff -u "$reference/prompt.py" "$candidate/prompt.py" || true
  overall=1
fi

printf '[translator identity]\n'
if cmp -s "$reference/py2mpy.py" "$candidate/py2mpy.py"; then
  printf 'IDENTICAL py2mpy.py\n'
else
  printf 'DIFFERENT py2mpy.py\n'
  diff -u "$reference/py2mpy.py" "$candidate/py2mpy.py" || true
  overall=1
fi

printf '[supplied semantics identity and entry types]\n'
if diff -r --no-dereference "$reference/reference-semantics" \
                              "$candidate/reference-semantics"; then
  printf 'IDENTICAL reference-semantics tree\n'
else
  printf 'DIFFERENT reference-semantics tree\n'
  overall=1
fi

python3 - "$reference/reference-semantics" "$candidate/reference-semantics" <<'PY'
import os
import stat
import sys

for root in sys.argv[1:]:
    print(f"TYPES {root}")
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in sorted(dirnames + filenames):
            path = os.path.join(dirpath, name)
            mode = os.lstat(path).st_mode
            if stat.S_ISREG(mode):
                kind = "file"
            elif stat.S_ISDIR(mode):
                kind = "dir"
            elif stat.S_ISLNK(mode):
                kind = "symlink"
            else:
                kind = "other"
            print(kind, os.path.relpath(path, root))
PY

exit "$overall"

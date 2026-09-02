#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

printf 'SEMANTICS MODE: SUPPLIED_SEMANTICS\n'
if [[ -d "$reference/reference-semantics" ]]; then
  printf 'trusted semantics mount: PRESENT\n'
else
  printf 'trusted semantics mount: MISSING\n'
fi

printf '\nCandidate inventory (type, path, symlink target):\n'
find "$candidate" -printf '%y %p -> %l\n' | LC_ALL=C sort

printf '\nRequired untrusted-generation artifacts:\n'
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    printf '%s: regular file\n' "$name"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    printf '%s: present but wrong type or symlink\n' "$name"
  else
    printf '%s: MISSING\n' "$name"
  fi
done

printf '\nCandidate symlinks:\n'
find "$candidate" -type l -printf '%p -> %l\n' | LC_ALL=C sort

printf '\nTrusted/candidate prompt comparison:\n'
sha256sum "$reference/prompt.py" "$candidate/prompt.py"
cmp "$reference/prompt.py" "$candidate/prompt.py"
printf 'prompt cmp status: %d\n' "$?"

printf '\nTrusted/candidate translator comparison:\n'
sha256sum "$reference/py2mpy.py" "$candidate/py2mpy.py"
cmp "$reference/py2mpy.py" "$candidate/py2mpy.py"
printf 'translator cmp status: %d\n' "$?"

printf '\nTrusted/candidate supplied-semantics recursive comparison:\n'
diff --no-dereference -r "$reference/reference-semantics" "$candidate/reference-semantics"
printf 'semantics diff status: %d\n' "$?"

printf '\nTrusted semantics entry types:\n'
find "$reference/reference-semantics" -printf '%y %P -> %l\n' | LC_ALL=C sort
printf '\nCandidate semantics entry types:\n'
find "$candidate/reference-semantics" -printf '%y %P -> %l\n' | LC_ALL=C sort

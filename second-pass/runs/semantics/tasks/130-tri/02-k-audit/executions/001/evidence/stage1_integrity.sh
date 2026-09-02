#!/usr/bin/env bash
set -u

echo '$ test -d /reference/reference-semantics'
test -d /reference/reference-semantics
echo "exit=$?"

echo '$ find -P /reference/reference-semantics -printf "%y %P -> %l\n" | sort'
find -P /reference/reference-semantics -printf '%y %P -> %l\n' | sort
echo "exit=${PIPESTATUS[0]}"

echo '$ find -P /candidate/reference-semantics -printf "%y %P -> %l\n" | sort'
find -P /candidate/reference-semantics -printf '%y %P -> %l\n' | sort
echo "exit=${PIPESTATUS[0]}"

echo '$ diff -ruN --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -ruN --no-dereference /reference/reference-semantics /candidate/reference-semantics
echo "exit=$?"

for name in prompt.py py2mpy.py; do
  echo "\$ cmp /reference/$name /candidate/$name"
  cmp "/reference/$name" "/candidate/$name"
  echo "exit=$?"
done

echo '$ test ! -L on every candidate source-tree entry'
symlinks="$(find -P /candidate -type l -print)"
if [ -n "$symlinks" ]; then
  printf '%s\n' "$symlinks"
  echo 'exit=1'
else
  echo 'no symlinks'
  echo 'exit=0'
fi

for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  echo "\$ stat /candidate/$name"
  stat -c '%F %s bytes %n' "/candidate/$name" 2>&1
  echo "exit=$?"
done

echo '$ find -P /candidate -maxdepth 2 -type f \( -iname "*trace*" -o -iname "*.jsonl" -o -iname "*.json" \) -printf "%P\n" | sort'
find -P /candidate -maxdepth 2 -type f \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*.json' \) -printf '%P\n' | sort
echo "exit=${PIPESTATUS[0]}"

echo '$ sha256sum selected trusted and candidate sources'
sha256sum \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/prove.sh
echo "exit=$?"

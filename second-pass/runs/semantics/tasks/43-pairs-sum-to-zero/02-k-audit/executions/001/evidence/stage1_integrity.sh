#!/usr/bin/env bash
set +e

echo '$ find /candidate -maxdepth 5 -printf "%y %p -> %l\n" | sort'
find /candidate -maxdepth 5 -printf '%y %p -> %l\n' | sort
echo "exit=$?"

echo '$ find /reference -maxdepth 5 -printf "%y %p -> %l\n" | sort'
find /reference -maxdepth 5 -printf '%y %p -> %l\n' | sort
echo "exit=$?"

echo '$ required provenance artifacts'
for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  path="/candidate/$artifact"
  if test -e "$path" || test -L "$path"; then
    stat -c '%F %n -> %N' "$path"
  else
    echo "MISSING $path"
  fi
done

echo '$ structured generation trace search'
find /candidate -maxdepth 5 \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*.json' \
     -o -iname '*.log' -o -iname '*codex*' \) \
  -printf '%y %p -> %l\n' | sort
echo "exit=$?"

echo '$ cmp /candidate/prompt.py /reference/prompt.py'
cmp /candidate/prompt.py /reference/prompt.py
echo "exit=$?"

echo '$ cmp /candidate/py2mpy.py /reference/py2mpy.py'
cmp /candidate/py2mpy.py /reference/py2mpy.py
echo "exit=$?"

echo '$ diff -ruN --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -ruN --no-dereference \
  /reference/reference-semantics /candidate/reference-semantics
echo "exit=$?"

echo '$ non-regular entries under supplied semantics trees'
find /candidate/reference-semantics \
  ! -type d ! -type f -printf 'CANDIDATE_NONREGULAR %y %p -> %l\n'
find /reference/reference-semantics \
  ! -type d ! -type f -printf 'REFERENCE_NONREGULAR %y %p -> %l\n'
echo "exit=$?"

echo '$ SHA-256 of trusted and candidate provenance-sensitive trees'
find /reference/reference-semantics -type f -print0 |
  sort -z |
  xargs -0 sha256sum
find /candidate/reference-semantics -type f -print0 |
  sort -z |
  xargs -0 sha256sum
sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py
echo "exit=$?"

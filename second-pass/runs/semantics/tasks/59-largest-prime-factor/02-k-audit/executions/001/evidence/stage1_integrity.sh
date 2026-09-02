#!/usr/bin/env bash
set -u

candidate=/candidate
trusted=/reference

echo '$ find /candidate -maxdepth 1 -printf ...'
find "$candidate" -maxdepth 1 -printf '%y %m %f -> %l\n' | LC_ALL=C sort
echo "exit=$?"

echo '$ required provenance files'
status=0
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  path="$candidate/$name"
  if [ -f "$path" ] && [ ! -L "$path" ]; then
    echo "PRESENT regular $name"
  elif [ -e "$path" ] || [ -L "$path" ]; then
    echo "MISTYPED_OR_SYMLINKED $name"
    status=1
  else
    echo "MISSING $name"
    status=1
  fi
done
echo "required_provenance_status=$status"

echo '$ structured trace candidates'
find "$candidate" -maxdepth 1 \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*generation*.json' \) \
  -printf '%y %f -> %l\n' | LC_ALL=C sort
echo "exit=$?"

for pair in 'prompt.py prompt.py' 'py2mpy.py py2mpy.py'; do
  set -- $pair
  echo "\$ cmp -s /candidate/$1 /reference/$2"
  cmp -s "$candidate/$1" "$trusted/$2"
  cmp_status=$?
  echo "exit=$cmp_status"
  if [ "$cmp_status" -ne 0 ]; then
    diff -u "$trusted/$2" "$candidate/$1" || true
  fi
done

echo '$ candidate reference-semantics file-type manifest'
(
  cd "$candidate/reference-semantics" &&
  find . -printf '%y %P -> %l\n' | LC_ALL=C sort
)
echo "exit=$?"

echo '$ trusted reference-semantics file-type manifest'
(
  cd "$trusted/reference-semantics" &&
  find . -printf '%y %P -> %l\n' | LC_ALL=C sort
)
echo "exit=$?"

echo '$ diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -r --no-dereference "$trusted/reference-semantics" "$candidate/reference-semantics"
diff_status=$?
echo "exit=$diff_status"

echo '$ sha256sum trusted and candidate integrity inputs'
sha256sum \
  "$trusted/prompt.py" "$candidate/prompt.py" \
  "$trusted/py2mpy.py" "$candidate/py2mpy.py" \
  "$trusted/reference-semantics/semantics.k" \
  "$candidate/reference-semantics/semantics.k"
echo "exit=$?"

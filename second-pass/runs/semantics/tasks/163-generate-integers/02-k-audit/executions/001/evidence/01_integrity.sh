#!/usr/bin/env bash
set -u
set -o pipefail

candidate=/candidate
reference=/reference

echo 'CMD: find -P /candidate -printf "%y %m %s %p -> %l\n" | sort'
find -P "$candidate" -printf '%y %m %s %p -> %l\n' | sort
echo "EXIT: ${PIPESTATUS[0]}"

echo 'CMD: inspect required provenance artifacts and structured traces'
for path in \
  "$candidate/run-input.json" \
  "$candidate/metrics.json" \
  "$candidate/codex-last.txt" \
  "$candidate/codex-output.log"
do
  if [[ -e "$path" || -L "$path" ]]; then
    stat -c '%F %n -> %N' "$path"
  else
    echo "MISSING: $path"
  fi
done
find -P "$candidate" -maxdepth 2 -type f \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*.json' \) -print
echo "EXIT: $?"

echo 'CMD: cmp -s /reference/prompt.py /candidate/prompt.py'
cmp -s "$reference/prompt.py" "$candidate/prompt.py"
echo "EXIT: $?"

echo 'CMD: cmp -s /reference/py2mpy.py /candidate/py2mpy.py'
cmp -s "$reference/py2mpy.py" "$candidate/py2mpy.py"
echo "EXIT: $?"

echo 'CMD: find -P /candidate/reference-semantics -type l -print'
find -P "$candidate/reference-semantics" -type l -print
echo "EXIT: $?"

echo 'CMD: diff -u <(trusted semantics path/type inventory) <(candidate semantics path/type inventory)'
diff -u \
  <(cd "$reference/reference-semantics" && find -P . -printf '%P\t%y\n' | sort) \
  <(cd "$candidate/reference-semantics" && find -P . -printf '%P\t%y\n' | sort)
echo "EXIT: $?"

echo 'CMD: diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -r --no-dereference \
  "$reference/reference-semantics" \
  "$candidate/reference-semantics"
echo "EXIT: $?"

echo 'CMD: sha256sum trusted/candidate prompt, translator, and semantics files'
sha256sum \
  "$reference/prompt.py" "$candidate/prompt.py" \
  "$reference/py2mpy.py" "$candidate/py2mpy.py" \
  "$reference/reference-semantics/semantics.k" \
  "$candidate/reference-semantics/semantics.k"
echo "EXIT: $?"

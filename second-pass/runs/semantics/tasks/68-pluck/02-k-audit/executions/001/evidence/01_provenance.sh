#!/usr/bin/env bash
set +e

echo '$ find /candidate -maxdepth 4 -printf "%y %p -> %l\\n" | sort'
find /candidate -maxdepth 4 -printf '%y %p -> %l\n' | sort
echo "exit=${PIPESTATUS[0]}"

echo '$ find /reference -maxdepth 5 -printf "%y %p -> %l\\n" | sort'
find /reference -maxdepth 5 -printf '%y %p -> %l\n' | sort
echo "exit=${PIPESTATUS[0]}"

echo '$ test -d /reference/reference-semantics'
test -d /reference/reference-semantics
echo "exit=$?"

echo '$ find /candidate -type l -print'
find /candidate -type l -print
echo "exit=$?"

echo '$ cmp -s /candidate/prompt.py /reference/prompt.py'
cmp -s /candidate/prompt.py /reference/prompt.py
echo "exit=$?"

echo '$ cmp -s /candidate/py2mpy.py /reference/py2mpy.py'
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
echo "exit=$?"

echo '$ diff --no-dereference -r /reference/reference-semantics /candidate/reference-semantics'
diff --no-dereference -r /reference/reference-semantics /candidate/reference-semantics
echo "exit=$?"

echo '$ sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py'
sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py
echo "exit=$?"

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  echo "\$ test -f /candidate/$artifact"
  test -f "/candidate/$artifact"
  echo "exit=$?"
done

echo '$ find /candidate -maxdepth 2 -type f \( -iname "*trace*" -o -iname "*.jsonl" \) -print'
find /candidate -maxdepth 2 -type f \( -iname '*trace*' -o -iname '*.jsonl' \) -print
echo "exit=$?"

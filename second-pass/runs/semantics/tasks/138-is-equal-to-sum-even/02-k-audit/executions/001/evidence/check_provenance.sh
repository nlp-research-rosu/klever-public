#!/usr/bin/env bash
set -uo pipefail

echo "COMMAND: find /reference -printf '%y %p -> %l\\n' | sort"
find /reference -printf '%y %p -> %l\n' | sort
echo "EXIT_STATUS: ${PIPESTATUS[0]}"

echo "COMMAND: find /candidate -printf '%y %p -> %l\\n' | sort"
find /candidate -printf '%y %p -> %l\n' | sort
echo "EXIT_STATUS: ${PIPESTATUS[0]}"

for required in run-input.json metrics.json codex-last.txt codex-output.log; do
  echo "COMMAND: test -f /candidate/$required"
  test -f "/candidate/$required"
  status=$?
  echo "EXIT_STATUS: $status"
done

echo "COMMAND: find /candidate -maxdepth 1 -type f \\( -iname '*trace*' -o -iname '*.jsonl' \\) -print"
find /candidate -maxdepth 1 -type f \( -iname '*trace*' -o -iname '*.jsonl' \) -print
echo "EXIT_STATUS: ${PIPESTATUS[0]}"

echo "COMMAND: cmp -s /reference/prompt.py /candidate/prompt.py"
cmp -s /reference/prompt.py /candidate/prompt.py
echo "EXIT_STATUS: $?"

echo "COMMAND: cmp -s /reference/py2mpy.py /candidate/py2mpy.py"
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
echo "EXIT_STATUS: $?"

echo "COMMAND: diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics"
diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
echo "EXIT_STATUS: $?"

echo "COMMAND: find /candidate/reference-semantics -type l -print"
find /candidate/reference-semantics -type l -print
echo "EXIT_STATUS: ${PIPESTATUS[0]}"

echo "COMMAND: sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py"
sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py
echo "EXIT_STATUS: ${PIPESTATUS[0]}"

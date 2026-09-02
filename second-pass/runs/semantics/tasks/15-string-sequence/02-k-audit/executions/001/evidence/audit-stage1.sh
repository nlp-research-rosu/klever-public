#!/usr/bin/env bash
set -uo pipefail

echo "COMMAND: reject candidate symlinks/special entries; inspect required provenance; compare trusted prompt/translator and supplied semantics"
rc=0

echo "Candidate symlinks or non-regular/non-directory entries:"
find /candidate \( -type l -o \( ! -type f ! -type d \) \) -printf '%y %p -> %l\n'
if [[ -n "$(find /candidate \( -type l -o \( ! -type f ! -type d \) \) -print -quit)" ]]; then
  rc=1
fi

echo "Required provenance files:"
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "/candidate/$name" ]]; then
    echo "PRESENT /candidate/$name"
  else
    echo "MISSING /candidate/$name"
  fi
done

echo "Structured generation trace candidates:"
find /candidate -maxdepth 1 -type f \( -iname '*trace*' -o -iname '*.jsonl' \) -printf '%p\n'

echo "Prompt identity:"
cmp -s /candidate/prompt.py /reference/prompt.py
status=$?
echo "cmp /candidate/prompt.py /reference/prompt.py EXIT=$status"
if (( status != 0 )); then rc=1; fi
sha256sum /candidate/prompt.py /reference/prompt.py

echo "Translator identity:"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
status=$?
echo "cmp /candidate/py2mpy.py /reference/py2mpy.py EXIT=$status"
if (( status != 0 )); then rc=1; fi
sha256sum /candidate/py2mpy.py /reference/py2mpy.py

echo "Supplied-semantics recursive diff:"
diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
status=$?
echo "diff EXIT=$status"
if (( status != 0 )); then rc=1; fi

echo "Trusted semantics special entries:"
find /reference/reference-semantics \( -type l -o \( ! -type f ! -type d \) \) -printf '%y %p -> %l\n'

echo "Candidate semantics sha256:"
find /candidate/reference-semantics -type f -print0 |
  LC_ALL=C sort -z |
  xargs -0 sha256sum

echo "OVERALL_INTEGRITY_EXIT=$rc"
exit "$rc"

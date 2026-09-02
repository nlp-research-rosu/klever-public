#!/usr/bin/env bash
set -u
set -x

for claimed in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log
do
  if test -f "$claimed"; then
    stat "$claimed"
    sed -n '1,240p' "$claimed"
  else
    echo "MISSING_CLAIMED_ARTIFACT: $claimed"
  fi
done

find /candidate -maxdepth 2 \( -iname '*trace*' -o -iname '*generation*' \) \
  -printf '%y %p -> %l\n' | sort

find /candidate -printf '%y %P -> %l\n' | sort
find /reference/reference-semantics -printf '%y %P -> %l\n' | sort

diff -ruN --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics
echo "SEMANTICS_DIFF_EXIT=$?"

cmp -s /reference/prompt.py /candidate/prompt.py
echo "PROMPT_CMP_EXIT=$?"
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
echo "TRANSLATOR_CMP_EXIT=$?"

sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py

sed -n '1,260p' /candidate/proof-output.log
sed -n '1,260p' /candidate/prove.sh

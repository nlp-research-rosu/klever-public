#!/usr/bin/env bash
set -uo pipefail

echo "REFERENCE INVENTORY"
find /reference -printf '%y %P -> %l\n' | LC_ALL=C sort

echo "CANDIDATE INVENTORY"
find /candidate -printf '%y %P -> %l\n' | LC_ALL=C sort

echo "CANDIDATE SYMLINKS"
find /candidate -type l -printf '%P -> %l\n' | LC_ALL=C sort

echo "REQUIRED GENERATION METADATA"
for audit_name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "/candidate/$audit_name" && ! -L "/candidate/$audit_name" ]]; then
    printf 'PRESENT regular %s\n' "$audit_name"
  elif [[ -e "/candidate/$audit_name" || -L "/candidate/$audit_name" ]]; then
    printf 'PRESENT wrong-type-or-symlink %s\n' "$audit_name"
  else
    printf 'MISSING %s\n' "$audit_name"
  fi
done

echo "STRUCTURED TRACE CANDIDATES"
find /candidate -maxdepth 1 -type f \
  \( -iname '*trace*.json' -o -iname '*trace*.jsonl' -o -iname '*trace*.log' \) \
  -printf '%P\n' | LC_ALL=C sort

echo "PROMPT COMPARISON"
cmp -s /candidate/prompt.py /reference/prompt.py
printf 'prompt_cmp_status=%d\n' "$?"
sha256sum /candidate/prompt.py /reference/prompt.py

echo "TRANSLATOR COMPARISON"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'translator_cmp_status=%d\n' "$?"
sha256sum /candidate/py2mpy.py /reference/py2mpy.py

echo "SUPPLIED SEMANTICS RECURSIVE COMPARISON"
diff --no-dereference -r /reference/reference-semantics /candidate/reference-semantics
printf 'semantics_diff_status=%d\n' "$?"

echo "SUPPLIED SEMANTICS HASHES"
(
  cd /reference/reference-semantics
  find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
)
(
  cd /candidate/reference-semantics
  find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
)

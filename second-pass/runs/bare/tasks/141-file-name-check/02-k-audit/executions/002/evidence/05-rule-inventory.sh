#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/141-file-name-check
cd "$SCRATCH" || exit 1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run nl -ba semantic.k
run nl -ba verification.k
run nl -ba spec.k

run rg -n '^[[:space:]]*syntax\b|^[[:space:]]*configuration\b|^[[:space:]]*rule\b|^[[:space:]]*claim\b' \
  semantic.k verification.k spec.k

run rg -n '\[(?:[^]]*\b(?:function|total|functional|symbol|concrete|simplification|simplifier|priority|owise|anywhere|macro|alias|trusted)\b[^]]*)\]' \
  semantic.k verification.k spec.k

run rg -n '\[(?:[^]]*\b(?:simplification|simplifier|priority|owise|anywhere|macro|alias|trusted)\b[^]]*)\]' \
  semantic.k verification.k spec.k

run python3 -c '
import re
from collections import Counter
from pathlib import Path

text = Path("solution.mpy").read_text()
constructors = re.findall(r"\b([A-Z][A-Za-z0-9]*)\s*\(", text)
for name, count in sorted(Counter(constructors).items()):
    print(name, count)
'

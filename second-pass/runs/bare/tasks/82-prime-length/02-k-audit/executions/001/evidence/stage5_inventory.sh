#!/usr/bin/env bash
set -euo pipefail

echo "== complete reviewed K sources =="
for source in semantic.k verification.k spec.k; do
  echo "----- $source -----"
  nl -ba "$source"
done

echo "== local declarations, configuration, rules, and claims =="
rg -n \
  '^\s*(syntax|configuration|rule|claim)\b|\[(function|functional|total|simplification|concrete|priority|owise|macro)' \
  semantic.k verification.k spec.k

echo "== potentially proof-relevant attributes and symbols =="
for needle in \
  function functional total simplification concrete priority owise macro \
  anywhere hook impure opaque claim rule
do
  printf '%s: ' "$needle"
  rg -n -i "\\b${needle}\\b" semantic.k verification.k spec.k || true
done

echo "== constructors and tokens visibly used by submitted solution.mpy =="
python3 - solution.submitted.mpy <<'PY'
import collections
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
constructors = collections.Counter(re.findall(r"\b([A-Z][A-Za-z0-9]*)\s*\(", text))
strings = collections.Counter(re.findall(r'"(?:[^"\\]|\\.)*"', text))
print("constructors", dict(sorted(constructors.items())))
print("string_tokens", dict(sorted(strings.items())))
PY

echo "== candidate K/helper source inventory =="
find /candidate -maxdepth 2 -type f \
  \( -name '*.k' -o -name '*.md' \) \
  -printf '%p\n' | sort

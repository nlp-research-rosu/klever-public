#!/usr/bin/env bash
set -u

required=(
  /candidate/run-input.json
  /candidate/metrics.json
  /candidate/codex-last.txt
  /candidate/codex-output.log
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/semantic.k
  /candidate/spec.k
  /candidate/verification.k
)

status=0
echo "REQUIRED ARTIFACT TYPES"
for path in "${required[@]}"; do
  if [[ ! -e "$path" && ! -L "$path" ]]; then
    printf 'MISSING %s\n' "$path"
    status=1
  elif [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
    status=1
  elif [[ ! -f "$path" ]]; then
    printf 'MISTYPED %s: %s\n' "$path" "$(stat -c '%F' "$path")"
    status=1
  else
    printf 'REGULAR %s\n' "$path"
  fi
done

echo
echo "FULL CANDIDATE INVENTORY"
find /candidate -printf '%y %p -> %l\n' | sort

echo
echo "STRUCTURED TRACE FILES"
find /candidate/codex-trace -type f -printf '%p\n' 2>/dev/null | sort

echo
echo "TRUSTED REFERENCE INVENTORY"
find /reference -printf '%y %p -> %l\n' | sort

echo
echo "GENERATED_SEMANTICS BOUNDARY"
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  echo "BREACH: /reference/reference-semantics exists"
  status=2
else
  echo "OK: /reference/reference-semantics does not exist"
fi

echo
echo "PROMPT COMPARISON"
if cmp -s /candidate/prompt.py /reference/prompt.py; then
  echo "IDENTICAL: candidate prompt.py"
else
  echo "CHANGED: candidate prompt.py"
  diff -u /reference/prompt.py /candidate/prompt.py || true
  status=1
fi

echo
echo "TRANSLATOR COMPARISON"
if cmp -s /candidate/py2mpy.py /reference/py2mpy.py; then
  echo "IDENTICAL: candidate py2mpy.py"
else
  echo "CHANGED: candidate py2mpy.py"
  diff -u /reference/py2mpy.py /candidate/py2mpy.py || true
  status=1
fi

echo
echo "SOURCE HASHES"
sha256sum \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/spec.k \
  /candidate/verification.k

exit "$status"

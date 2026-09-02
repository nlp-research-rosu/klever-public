#!/usr/bin/env bash
set -u

required=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
)

echo "REFERENCE SEMANTICS BOUNDARY"
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  echo "BREACH: /reference/reference-semantics exists"
  stat -c '%F %a %n -> %N' /reference/reference-semantics
else
  echo "OK: /reference/reference-semantics is absent"
fi

echo
echo "REQUIRED CANDIDATE ARTIFACT TYPES"
for name in "${required[@]}"; do
  path="/candidate/${name}"
  if [[ -L "$path" ]]; then
    echo "SYMLINK $path -> $(readlink "$path")"
  elif [[ -f "$path" ]]; then
    stat -c 'REGULAR %a %s %n' "$path"
  elif [[ -e "$path" ]]; then
    stat -c 'MISTYPED %F %a %s %n' "$path"
  else
    echo "MISSING $path"
  fi
done

echo
echo "STRUCTURED TRACE"
if [[ -d /candidate/codex-trace ]]; then
  find /candidate/codex-trace -type l -printf 'SYMLINK %p -> %l\n'
  find /candidate/codex-trace -type f -printf 'REGULAR %m %s %p\n' | sort
else
  echo "ABSENT /candidate/codex-trace"
fi

echo
echo "TRUSTED FILE COMPARISONS"
for pair in \
  '/candidate/prompt.py /reference/prompt.py' \
  '/candidate/py2mpy.py /reference/py2mpy.py'
do
  set -- $pair
  if cmp -s "$1" "$2"; then
    echo "BYTE_IDENTICAL $1 $2"
  else
    echo "DIFFERENT $1 $2"
    cmp -l "$1" "$2" | head -20
  fi
  sha256sum "$1" "$2"
done

echo
echo "CANDIDATE TOP-LEVEL INVENTORY"
find /candidate -maxdepth 1 -mindepth 1 -printf '%y %m %s %f -> %l\n' | sort

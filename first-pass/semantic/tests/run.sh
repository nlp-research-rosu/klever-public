#!/usr/bin/env bash
# Validate reference/src/semantics.k against every SEMANTICS test. For each
# tests/semantics/<case>/<case>.py:
#   - run it in CPython (the oracle: the asserts must hold in real Python), and
#   - run <case>.mpy in K, which PASSES only if the program runs to completion:
#     the <k> cell reduces to .K (no stuck term / no parse error) AND no AssertionError.
# A weak "grep AssertionError" check is NOT enough — a parse error or a stuck config
# (e.g. an unparseable node, or a missing rule) leaves no AssertionError yet is a real
# failure, so we require <k> => .K explicitly.
# Regenerate a .mpy after editing its .py:
#   python3 scripts/py2mpy.py tests/semantics/<case>/<case>.py > .../<case>.mpy
# (Proof tests live under tests/verification/ — run those with tests/verify.sh.)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # reference/tests
SRC="$(dirname "$HERE")/src"                            # reference/src
DEF="$SRC/semantics-kompiled"
[ -d "$DEF" ] || kompile "$SRC/semantics.k" --backend llvm \
  --main-module MPY-CONCRETE --syntax-module MPY-SYNTAX --output-definition "$DEF"
rc=0
for py in "$HERE"/semantics/*/*.py; do
  n="$(basename "$py" .py)"; d="$(dirname "$py")"
  if ! python3 "$py" >/dev/null 2>&1; then printf "  %-16s PY-FAIL\n" "$n"; rc=1; continue; fi
  out="$(krun "$d/$n.mpy" --definition "$DEF" 2>&1)"
  flat="$(printf '%s' "$out" | tr -d '[:space:]')"     # collapse whitespace for cell matching
  if printf '%s' "$flat" | grep -q '<k>.K</k>' && ! printf '%s' "$flat" | grep -q 'AssertionError'; then
    printf "  %-16s ok\n" "$n"
  else
    if   printf '%s' "$out"  | grep -q 'Parse error';   then why="K-PARSE"   # unparseable .mpy node
    elif printf '%s' "$flat" | grep -q 'AssertionError'; then why="K-ASSERT"  # K disagrees with CPython
    else why="K-STUCK"; fi                                                    # no rule applied (e.g. bad call)
    printf "  %-16s %s\n" "$n" "$why"; rc=1
  fi
done
[ $rc = 0 ] && echo "ALL PASS" || echo "FAILURES"
exit $rc

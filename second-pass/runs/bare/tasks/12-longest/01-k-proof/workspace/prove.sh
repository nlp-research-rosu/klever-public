#!/usr/bin/env bash
set -euo pipefail

# Recreate the translated program and the Haskell definition used by both
# concrete execution and symbolic proof.
python3 py2mpy.py solution.py > solution.mpy
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --warnings none

# Exercise the translated solution, including the empty case, growth, and a
# later equal-length string that must not replace the first maximum.
EMPTY_RESULT="$(krun solution.mpy \
  --definition verification-kompiled \
  -cARGS='listVal()' \
  --pattern '<out> noneVal </out>' \
  --output pretty)"
printf '%s\n' "$EMPTY_RESULT"
test "$EMPTY_RESULT" = '#Top'

GROWTH_RESULT="$(krun solution.mpy \
  --definition verification-kompiled \
  -cARGS='listVal(strVal("a"),strVal("bb"),strVal("ccc"))' \
  --pattern '<out> strVal("ccc") </out>' \
  --output pretty)"
printf '%s\n' "$GROWTH_RESULT"
test "$GROWTH_RESULT" = '#Top'

TIE_RESULT="$(krun solution.mpy \
  --definition verification-kompiled \
  -cARGS='listVal(strVal("aa"),strVal("b"),strVal("cc"))' \
  --pattern '<out> strVal("aa") </out>' \
  --output pretty)"
printf '%s\n' "$TIE_RESULT"
test "$TIE_RESULT" = '#Top'

# This single positive proof command proves every claim in spec.k.  Lowering
# the backend log level suppresses expected warnings for the deliberately
# uninterpreted symbolic string-at-index function.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty \
  --warnings none \
  --haskell-backend-command 'kore-exec --log-level error'

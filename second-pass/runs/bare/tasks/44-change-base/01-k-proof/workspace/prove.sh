#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

krun solution.mpy -cX=8 -cBASE=3 --definition verification-kompiled \
  --pattern '<k> strVal("22") ~> .K </k>'
krun solution.mpy -cX=8 -cBASE=2 --definition verification-kompiled \
  --pattern '<k> strVal("1000") ~> .K </k>'
krun solution.mpy -cX=7 -cBASE=2 --definition verification-kompiled \
  --pattern '<k> strVal("111") ~> .K </k>'
krun solution.mpy -cX=1234 -cBASE=7 --definition verification-kompiled \
  --pattern '<k> strVal("3412") ~> .K </k>'

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

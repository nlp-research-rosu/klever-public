#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 py2mpy.py solution.py > solution.mpy
printf '%s  %s\n' \
  '11366253bbb1d88f6881db189674885fb00045eb3fa69b16ad69c45d07077774' \
  'solution.mpy' | sha256sum --check

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

krun solution.mpy -cARG=-3 --definition verification-kompiled
krun solution.mpy -cARG=0 --definition verification-kompiled
krun solution.mpy -cARG=5 --definition verification-kompiled
krun solution.mpy -cARG=12 --definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

cp solution.py .concrete_tests.py
printf '%s\n' '' \
  'assert valid_date("03-11-2000") == True' \
  'assert valid_date("15-01-2012") == False' \
  'assert valid_date("04-0-2040") == False' \
  'assert valid_date("06-04-2020") == True' \
  'assert valid_date("06/04/2020") == False' \
  'assert valid_date("") == False' \
  'assert valid_date("02-29-2023") == True' \
  'assert valid_date("02-30-2023") == False' \
  'assert valid_date("04-30-2040") == True' \
  'assert valid_date("04-31-2040") == False' \
  'assert valid_date("01-31-0000") == True' \
  'assert valid_date("00-01-2000") == False' \
  'assert valid_date("12-00-2000") == False' \
  'assert valid_date("12-31-20x0") == False' \
  'assert valid_date("12-31-20000") == False' >> .concrete_tests.py
python3 py2mpy.py .concrete_tests.py > .concrete_tests.mpy
krun .concrete_tests.mpy --definition runtime-kompiled
rm -f .concrete_tests.py .concrete_tests.mpy

kompile verification.k \
  --backend haskell \
  --main-module VALID-DATE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module VALID-DATE-SPEC

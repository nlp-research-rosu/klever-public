#!/usr/bin/env bash
set -u

work=/tmp/audit-work/final-reconstruction
candidate=/candidate
trusted=/reference

mkdir "$work"
cp "$candidate/solution.py" "$candidate/solution.mpy" \
  "$candidate/semantic.k" "$candidate/verification.k" \
  "$candidate/spec.k" "$work/"
cp "$trusted/py2mpy.py" "$work/"
cd "$work" || exit 1

run() {
  echo "$ $*"
  "$@"
  local status=$?
  echo "EXIT_STATUS=$status"
  test "$status" -eq 0 || exit "$status"
}

run kompile --version

echo '$ python3 py2mpy.py solution.py > regenerated-solution.mpy'
python3 py2mpy.py solution.py > regenerated-solution.mpy
status=$?
echo "EXIT_STATUS=$status"
test "$status" -eq 0 || exit "$status"
run cmp -s regenerated-solution.mpy solution.mpy

run kompile semantic.k --backend haskell \
  --main-module MINI-PYTHON \
  --syntax-module MINI-PYTHON-SYNTAX \
  --output-definition semantic-audit-kompiled

run kompile verification.k --backend haskell \
  --main-module ROMAN-VERIFICATION \
  --syntax-module MINI-PYTHON-SYNTAX \
  --output-definition verification-audit-kompiled

run kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module ROMAN-SPEC

echo '$ kast solution.mpy ... --output kast > submitted.kast'
kast solution.mpy \
  --definition verification-audit-kompiled \
  --module ROMAN-VERIFICATION \
  --sort Pgm \
  --output kast > submitted.kast
status=$?
echo "EXIT_STATUS=$status"
test "$status" -eq 0 || exit "$status"

echo '$ kast --expression romanProgram ... --expand-macros > claim.kast'
kast --expression romanProgram \
  --definition verification-audit-kompiled \
  --module ROMAN-VERIFICATION \
  --sort Pgm \
  --expand-macros \
  --output kast > claim.kast
status=$?
echo "EXIT_STATUS=$status"
test "$status" -eq 0 || exit "$status"
run cmp -s submitted.kast claim.kast
run wc -c submitted.kast claim.kast
run sha256sum submitted.kast claim.kast

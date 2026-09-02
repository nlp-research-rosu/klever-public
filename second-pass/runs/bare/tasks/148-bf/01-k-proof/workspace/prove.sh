#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 generate_proof_artifacts.py

python3 - <<'PY'
from solution import bf

planets = (
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
)
samples = planets + ("Pluto", "", "mercury")
for first in samples:
    for second in samples:
        if first in planets and second in planets:
            lo = min(planets.index(first), planets.index(second)) + 1
            hi = max(planets.index(first), planets.index(second))
            expected = planets[lo:hi]
        else:
            expected = ()
        assert bf(first, second) == expected
print("Python reference partition: passed")
PY

kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled

krun solution.mpy \
  --definition semantic-kompiled \
  -cPLANET1='"Jupiter"' \
  -cPLANET2='"Neptune"'
krun solution.mpy \
  --definition semantic-kompiled \
  -cPLANET1='"Earth"' \
  -cPLANET2='"Mercury"'
krun solution.mpy \
  --definition semantic-kompiled \
  -cPLANET1='"Mercury"' \
  -cPLANET2='"Uranus"'
krun solution.mpy \
  --definition semantic-kompiled \
  -cPLANET1='"Pluto"' \
  -cPLANET2='"Earth"'

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module BF-SPEC

if kprove mutation-spec.k \
  --definition verification-kompiled \
  --spec-module MUTATION-SPEC
then
  echo "ERROR: deliberately false mutation claim unexpectedly proved" >&2
  exit 1
else
  echo "Mutation probe: rejected as expected"
fi

#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

proof_tmp="$(mktemp -d)"
trap 'rm -rf -- "$proof_tmp"' EXIT

# Recreate and check the submitted translator output.
python3 py2mpy.py solution.py > "$proof_tmp/solution.mpy"
cmp solution.mpy "$proof_tmp/solution.mpy"

# Required concrete LLVM definition.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

# Exercise the exact solution source through the translator and LLVM runtime.
cp solution.py "$proof_tmp/concrete.py"
printf '%s\n' \
  '' \
  'assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")' \
  'assert bf("Earth", "Mercury") == ("Venus",)' \
  'assert bf("Mercury", "Uranus") == ("Venus", "Earth", "Mars", "Jupiter", "Saturn")' \
  'assert bf("Neptune", "Jupiter") == ("Saturn", "Uranus")' \
  'assert bf("Earth", "Earth") == ()' \
  'assert bf("Pluto", "Earth") == ()' \
  'assert bf("Earth", "Pluto") == ()' \
  >> "$proof_tmp/concrete.py"
python3 py2mpy.py "$proof_tmp/concrete.py" > "$proof_tmp/concrete.mpy"
krun "$proof_tmp/concrete.mpy" \
  --definition runtime-kompiled \
  --output none

# Symbolic definition: BF-VERIFICATION imports the supplied MPY modules only.
kompile verification.k \
  --backend haskell \
  --main-module BF-VERIFICATION \
  --syntax-module BF-VERIFICATION \
  --output-definition verification-kompiled

# This is the required positive target-proof command.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module BF-SPEC \
  | tee "$proof_tmp/kprove.out"
grep -qx '#Top' "$proof_tmp/kprove.out"

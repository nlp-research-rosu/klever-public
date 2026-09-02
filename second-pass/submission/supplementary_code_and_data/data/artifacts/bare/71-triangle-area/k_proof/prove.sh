#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Recreate the fixed translator output and require the checked-in AST to match.
cmp solution.mpy <(python3 py2mpy.py solution.py)

# Sanity-check the executable Python implementation against the prompt examples
# and the additional valid cases used by the K claims.
python3 - <<'PY'
from solution import triangle_area

assert triangle_area(3, 4, 5) == 6.00
assert triangle_area(1, 2, 10) == -1
assert triangle_area(5, 12, 13) == 30.00
assert triangle_area(2, 2, 2) == 1.73
PY

PROOF_BUILD="$(mktemp -d "$SCRIPT_DIR/.prove-build.XXXXXX")"
cleanup() {
  rm -rf -- "$PROOF_BUILD"
}
trap cleanup EXIT

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  -o "$PROOF_BUILD/verification-kompiled"

# Exercise both contract outcomes and the rounding algorithm via krun.
valid_output="$(krun solution.mpy \
  -cARGS='Args(VInt(3), VInt(4), VInt(5))' \
  -d "$PROOF_BUILD/verification-kompiled" --output pretty)"
printf '%s\n' "$valid_output"
grep -Fq 'VRounded ( 600 )' <<<"$valid_output"

invalid_output="$(krun solution.mpy \
  -cARGS='Args(VInt(1), VInt(2), VInt(10))' \
  -d "$PROOF_BUILD/verification-kompiled" --output pretty)"
printf '%s\n' "$invalid_output"
grep -Fq 'VInt ( -1 )' <<<"$invalid_output"

rounded_output="$(krun solution.mpy \
  -cARGS='Args(VInt(2), VInt(2), VInt(2))' \
  -d "$PROOF_BUILD/verification-kompiled" --output pretty)"
printf '%s\n' "$rounded_output"
grep -Fq 'VRounded ( 173 )' <<<"$rounded_output"

# This is the required positive target-proof command.  It proves every claim
# in spec.k in one invocation and must print #Top.
kprove spec.k \
  -d "$PROOF_BUILD/verification-kompiled" \
  --smt-timeout 10000

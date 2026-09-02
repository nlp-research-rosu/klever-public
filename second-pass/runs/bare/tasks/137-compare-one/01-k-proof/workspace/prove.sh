#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the exact constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# verification.k imports semantic.k, so this compiles the semantics plus the
# exact solution-term macro used by spec.k.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Ensure the term proved in spec.k is exactly the translation in solution.mpy.
proof_tmp_dir="$(mktemp -d ./k-proof.XXXXXX)"
trap 'rm -r "$proof_tmp_dir"' EXIT
kast solution.mpy \
  -d verification-kompiled -m MPY-SYNTAX -s Pgm \
  --expand-macros -o kore > "$proof_tmp_dir/solution.kore"
kast -e 'theSolution' \
  -d verification-kompiled -m VERIFICATION -s Pgm \
  --expand-macros -o kore > "$proof_tmp_dir/proof-term.kore"
cmp "$proof_tmp_dir/solution.kore" "$proof_tmp_dir/proof-term.kore"

# Exercise every example from prompt.py through the K semantics. The grep
# checks make an unexpected result fail the script while displaying the value.
krun solution.mpy -d verification-kompiled \
  -cA='pyInt(1)' -cB='pyFloat(25, 10)' --output pretty \
  | sed -n '/<result>/,/<\/result>/p' \
  | tee /dev/stderr | grep -F 'pyFloat ( 25 , 10 )'

krun solution.mpy -d verification-kompiled \
  -cA='pyInt(1)' -cB='pyStr("2,3")' --output pretty \
  | sed -n '/<result>/,/<\/result>/p' \
  | tee /dev/stderr | grep -F 'pyStr ( "2,3" )'

krun solution.mpy -d verification-kompiled \
  -cA='pyStr("5,1")' -cB='pyStr("6")' --output pretty \
  | sed -n '/<result>/,/<\/result>/p' \
  | tee /dev/stderr | grep -F 'pyStr ( "6" )'

krun solution.mpy -d verification-kompiled \
  -cA='pyStr("1")' -cB='pyInt(1)' --output pretty \
  | sed -n '/<result>/,/<\/result>/p' \
  | tee /dev/stderr | grep -F 'pyNone'

# Positive target proof: all claims in spec.k must close. Success prints #Top.
kprove spec.k -d verification-kompiled -sm SPEC --output pretty

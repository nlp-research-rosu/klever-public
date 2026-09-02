#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Build the supplied concrete semantics exactly as requested.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

# Exercise representative ordinary, subtractive, mixed-place, and boundary
# inputs through the LLVM semantics.
smoke_dir="$(mktemp -d /tmp/int-to-mini-roman.XXXXXX)"
cleanup() {
  if [[ -n "${smoke_dir:-}" && -d "$smoke_dir" ]]; then
    rm -rf -- "$smoke_dir"
  fi
}
trap cleanup EXIT

cp solution.py "$smoke_dir/smoke.py"
printf '%s\n' \
  '' \
  'assert int_to_mini_roman(1) == "i"' \
  'assert int_to_mini_roman(4) == "iv"' \
  'assert int_to_mini_roman(9) == "ix"' \
  'assert int_to_mini_roman(19) == "xix"' \
  'assert int_to_mini_roman(152) == "clii"' \
  'assert int_to_mini_roman(426) == "cdxxvi"' \
  'assert int_to_mini_roman(944) == "cmxliv"' \
  'assert int_to_mini_roman(1000) == "m"' \
  >> "$smoke_dir/smoke.py"
python3 py2mpy.py "$smoke_dir/smoke.py" > "$smoke_dir/smoke.mpy"
krun "$smoke_dir/smoke.mpy" --definition runtime-kompiled --output none
echo "KRUN_SMOKE_PASSED"

# First prove every finite helper case and all arithmetic index bounds against
# MPY without importing the helper-call summaries.
kompile verification.k \
  --backend haskell \
  --main-module ROMAN-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition lemma-kompiled
kprove spec.k \
  --definition lemma-kompiled \
  --spec-module ROMAN-LEMMA-SPEC

# Then use those proved lemmas to prove the universal entry-point claim.
kompile verification.k \
  --backend haskell \
  --main-module ROMAN-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module ROMAN-SPEC

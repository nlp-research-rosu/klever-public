#!/usr/bin/env bash
set -euo pipefail

# Recreate every translated program with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-empty.py > concrete-empty.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Check the ordinary Python behavior against CPython's hashlib.
python3 - <<'PY'
import hashlib
from solution import string_to_md5

tests = (
    "",
    "Hello world",
    "abc",
    "The quick brown fox jumps over the lazy dog",
)
for text in tests:
    expected = None if text == "" else hashlib.md5(text.encode("utf-8")).hexdigest()
    assert string_to_md5(text) == expected
PY

# Concrete execution uses exactly the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

# The empty branch completes and leaves empty_result bound to noneV.
empty_state="$(
  krun concrete-empty.mpy \
    --definition runtime-kompiled
)"
printf '%s\n' "$empty_state"
rg -q '"empty_result" \\|-> noneV' <<<"$empty_state"

# A bounded nonempty run reaches the supplied opaque MD5 oracle with the
# "Hello world" code sequence.  The next rewrite would ask LLVM to evaluate
# md5hexCodes, which intentionally has [no-evaluators] in the reference.
oracle_state="$(
  krun concrete-tests.mpy \
    --definition runtime-kompiled \
    --depth 82 \
    --statistics
)"
printf '%s\n' "$oracle_state"
rg -q 'md5Obj' <<<"$oracle_state"
rg -Fq 'iCons ( 72 , iCons ( 101' <<<"$oracle_state"

# Symbolic proofs import MPY (not MPY-CONCRETE) through verification.k.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# This single positive target command proves every claim in spec.k.
kprove \
  --definition verification-kompiled \
  --spec-module SPEC \
  spec.k

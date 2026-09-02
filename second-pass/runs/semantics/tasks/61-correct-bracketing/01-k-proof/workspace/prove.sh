#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$script_dir"

# Recreate the submitted constructor program with the required translator.
python3 py2mpy.py solution.py > solution.mpy

# Build the required concrete semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

# Exercise the exact submitted source through translation and LLVM execution.
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cp solution.py "$smoke_dir/smoke.py"
printf '%s\n' \
  '' \
  'assert correct_bracketing("")' \
  'assert not correct_bracketing("(")' \
  'assert correct_bracketing("()")' \
  'assert correct_bracketing("(()())")' \
  'assert not correct_bracketing(")(()")' \
  'assert not correct_bracketing("())")' \
  'assert correct_bracketing("()()")' \
  >> "$smoke_dir/smoke.py"
python3 py2mpy.py "$smoke_dir/smoke.py" > "$smoke_dir/smoke.mpy"
krun "$smoke_dir/smoke.mpy" --definition runtime-kompiled

# Build the unmodified MPY semantics plus pure mathematical oracle.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Prove the universal inductive claim (the entry case is B = 0).
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims loop

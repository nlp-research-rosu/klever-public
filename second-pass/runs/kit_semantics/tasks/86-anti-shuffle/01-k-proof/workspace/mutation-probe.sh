#!/usr/bin/env bash
set -euo pipefail

probe_dir=$(mktemp -d)
case "$probe_dir" in
  /tmp/*) ;;
  *) echo "unexpected temporary directory: $probe_dir" >&2; exit 2 ;;
esac
trap 'rm -rf -- "$probe_dir"' EXIT

cp solution.py py2mpy.py generate_program_module.py \
   verification.k spec.k "$probe_dir/"
ln -s "$PWD/reference-semantics" "$probe_dir/reference-semantics"

# Material mutation: the final word is replaced by the literal "X".
sed -i 's/^    result += word$/    result += "X"/' "$probe_dir/solution.py"

(
  cd "$probe_dir"
  python3 py2mpy.py solution.py > solution.mpy
  python3 generate_program_module.py
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-kompiled
  if kprove spec.k \
      --definition verification-kompiled \
      --spec-module SPEC; then
    echo "UNEXPECTED: mutated body proved" >&2
    exit 1
  fi
)

echo "EXPECTED FAILURE: generated-body mutation invalidated the proof"

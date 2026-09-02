#!/usr/bin/env bash
set -euxo pipefail

root=/tmp/audit-work/99-closest-integer-audit
mutant="$root/pinning-mutant"

if [[ -e "$mutant" ]]; then
  echo "refusing to reuse existing pinning-mutant directory" >&2
  exit 65
fi

mkdir -p "$mutant"
cp -a "$root/candidate/reference-semantics" "$mutant/"
cp -a "$root/candidate/verification.k" "$root/candidate/spec.k" "$mutant/"
cp -a /audit-output/evidence/04_mutant_solution.py "$mutant/solution.py"
python3 "$root/trusted/py2mpy.py" "$mutant/solution.py" > "$mutant/solution.mpy"

cd "$mutant"
kompile verification.k \
  --backend haskell \
  --main-module CLOSEST-INTEGER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module CLOSEST-INTEGER-SPEC
python3 -c 'import solution; print(solution.closest_integer("10"))'

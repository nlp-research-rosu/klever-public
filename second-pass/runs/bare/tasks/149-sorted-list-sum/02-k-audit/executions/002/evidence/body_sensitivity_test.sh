#!/usr/bin/env bash
set -euo pipefail

source_root=/tmp/audit-work/reconstruction
mutation_root=/tmp/audit-work/body-mutation
mkdir -p "$mutation_root"
cp \
  "$source_root/semantic.k" \
  "$source_root/verification.k" \
  "$source_root/spec.k" \
  "$source_root/make_solution_k.py" \
  "$source_root/trusted-py2mpy.py" \
  "$mutation_root/"
cp /audit-output/evidence/body-mutation-solution.py "$mutation_root/solution.py"

(
  cd "$mutation_root"
  python3 trusted-py2mpy.py solution.py > solution.mpy
  python3 make_solution_k.py > solution-program.k
  sha256sum solution.py solution.mpy solution-program.k
  kompile verification.k \
    --main-module SORTED-LIST-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --backend haskell \
    --output-definition body-proof-kompiled \
    -w none
)
printf 'BODY_MUTATION_BUILD_EXIT=0\n'

set +e
(
  cd "$mutation_root"
  kprove spec.k \
    --definition body-proof-kompiled \
    --spec-module SPEC \
    --claims universal-correctness \
    --output pretty
) > "$mutation_root/body-mutation-kprove.out" 2>&1
status=$?
set -e
sed -n '1,160p' "$mutation_root/body-mutation-kprove.out"
printf 'BODY_MUTATION_PROOF_EXIT=%d\n' "$status"
if [ "$status" -eq 0 ]; then
  printf 'UNEXPECTED_BODY_INSENSITIVITY=true\n'
  exit 1
fi
grep -Fq 'WarnStuckClaimState' "$mutation_root/body-mutation-kprove.out"
printf 'EXPECTED_BODY_SENSITIVITY_CONFIRMED=true\n'

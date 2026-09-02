#!/usr/bin/env bash
set -uo pipefail

source_root=/tmp/audit-work/candidate
mutation_root=/tmp/audit-work/body-mutation
mutation_definition=/tmp/audit-work/runs/body-mutation-kompiled

mkdir -p "$mutation_root"
cp "$source_root/semantic.k" "$mutation_root/semantic.k"
cp "$source_root/verification.k" "$mutation_root/verification.k"
cp "$source_root/spec.k" "$mutation_root/spec.k"

# Change the actual constructor term executed by every claim: an opening
# parenthesis now decrements depth.
sed -i \
  '0,/AugAssign(Name("depth"), "+", Int(1))/s//AugAssign(Name("depth"), "-", Int(1))/' \
  "$mutation_root/verification.k"
mutation_status=$?
echo "COMMAND[mutate-body]: replace the first depth += 1 constructor with depth -= 1"
echo "EXIT[mutate-body]: $mutation_status"
diff -u "$source_root/verification.k" "$mutation_root/verification.k"
diff_status=$?
echo "EXIT[expected-diff]: $diff_status"

echo "COMMAND[kompile]: kompile verification.k --main-module MPY-VERIFICATION --syntax-module MPY-VERIFICATION --backend haskell --output-definition $mutation_definition"
(
  cd "$mutation_root" &&
  kompile verification.k \
    --main-module MPY-VERIFICATION \
    --syntax-module MPY-VERIFICATION \
    --backend haskell \
    --output-definition "$mutation_definition"
)
build_status=$?
echo "EXIT[kompile]: $build_status"

echo "COMMAND[kprove]: kprove $mutation_root/spec.k --definition $mutation_definition --spec-module SPEC"
kprove "$mutation_root/spec.k" \
  --definition "$mutation_definition" \
  --spec-module SPEC
proof_status=$?
echo "EXIT[kprove]: $proof_status"

if [[ "$mutation_status" -eq 0 && "$diff_status" -eq 1 && "$build_status" -eq 0 && "$proof_status" -ne 0 ]]; then
  echo "BODY_SENSITIVITY=PASS"
  exit 0
fi
echo "BODY_SENSITIVITY=FAIL"
exit 1

#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/106-f
source_dir="$work/source"
definition="$work/build/verification-body-mutation-kompiled"
evidence=/audit-output/evidence
export PATH="$HOME/.nix-profile/bin:$PATH"

if [ -e "$definition" ]; then
  echo 'FRESHNESS_FAILURE: body-mutation definition already exists'
  exit 98
fi

echo 'COMMAND: preserve exact body mutation and show source diffs'
cp -p "$source_dir/verification-body-mutation.k" "$evidence/verification-body-mutation.k"
cp -p "$source_dir/spec-body-mutation.k" "$evidence/spec-body-mutation.k"
diff -u "$source_dir/verification.k" "$source_dir/verification-body-mutation.k" || true
diff -u "$source_dir/spec.k" "$source_dir/spec-body-mutation.k" || true

echo 'FALSE WITNESS: N=1; original returns [1], total-initialized-to-1 body returns [2]'
python3 - <<'PY'
def original(n):
    result, factorial, total, i = [], 1, 0, 1
    while i <= n:
        factorial *= i
        total += i
        result += [factorial if i % 2 == 0 else total]
        i += 1
    return result

def mutated(n):
    result, factorial, total, i = [], 1, 1, 1
    while i <= n:
        factorial *= i
        total += i
        result += [factorial if i % 2 == 0 else total]
        i += 1
    return result

print(f"original(1)={original(1)!r}")
print(f"mutated(1)={mutated(1)!r}")
PY
witness_status=$?
echo "EXIT_STATUS: $witness_status"

echo 'COMMAND: fresh Haskell build with one body constant mutated'
(
  cd "$source_dir" &&
  kompile verification-body-mutation.k \
    --main-module VERIFICATION-BODY-MUTATION \
    --syntax-module MPY-SYNTAX \
    --backend haskell \
    --output-definition "$definition"
) 2>&1 | tee "$evidence/06_kompile_body_mutation.log"
build_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $build_status" | tee -a "$evidence/06_kompile_body_mutation.log"
if [ "$build_status" -ne 0 ]; then
  exit "$build_status"
fi

echo 'COMMAND: prove unchanged theorem about mutated body (expected failure)'
(
  cd "$source_dir" &&
  timeout 180 kprove spec-body-mutation.k \
    --definition "$definition" \
    --spec-module SPEC-BODY-MUTATION \
    --output pretty
) 2>&1 | tee "$evidence/06_kprove_body_mutation.log"
proof_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $proof_status" | tee -a "$evidence/06_kprove_body_mutation.log"

echo 'COMMAND: verify expected stuck-claim residual'
rg -n 'WarnStuckClaimState|implication check|expectedCompletion|ListItem' \
  "$evidence/06_kprove_body_mutation.log"
residual_status=$?
echo "EXIT_STATUS: $residual_status"

if [ "$witness_status" -eq 0 ] && \
   [ "$proof_status" -ne 0 ] && \
   [ "$proof_status" -ne 124 ] && \
   [ "$residual_status" -eq 0 ]; then
  echo 'BODY_SENSITIVITY_RESULT: PASS'
  exit 0
fi
echo 'BODY_SENSITIVITY_RESULT: FAIL'
exit 1

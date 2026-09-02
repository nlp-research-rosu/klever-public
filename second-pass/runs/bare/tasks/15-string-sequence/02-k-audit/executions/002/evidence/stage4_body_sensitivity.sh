#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/body-mutation
export PATH="/home/agent/.nix-profile/bin:$PATH"
mkdir -p "$scratch"
cp /tmp/audit-work/reconstruction/semantic.k "$scratch/semantic.k"
cp /tmp/audit-work/reconstruction/spec.k "$scratch/spec.k"
cp /audit-output/evidence/verification-body-mutant.k "$scratch/verification.k"

printf 'COMMAND: bash /audit-output/evidence/stage4_body_sensitivity.sh\n'
printf '%s\n' \
  'MUTATION: targetBody initializes result to "X" instead of "0"; this changes the targetProgram() term executed by every entry claim.'
printf 'WITNESS: n=0 has mutant result "X", but the claimed result is "0".\n'
printf 'COMMAND: cd %s && kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-mutant-kompiled\n' \
  "$scratch"
(
  cd "$scratch" || exit 1
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-mutant-kompiled
)
build_status=$?
printf 'mutant_kompile_exit=%s\n' "$build_status"

printf 'COMMAND: cd %s && kprove spec.k --definition %s/verification-mutant-kompiled --spec-module SPEC\n' \
  "$scratch" "$scratch"
output="$(
  cd "$scratch" &&
  kprove spec.k \
    --definition "$scratch/verification-mutant-kompiled" \
    --spec-module SPEC \
    2>&1
)"
proof_status=$?
printf '%s\n' "$output"
printf 'mutant_kprove_exit=%s\n' "$proof_status"
residual_status=1
if printf '%s\n' "$output" | rg 'WarnStuckClaimState|implication check' >/dev/null; then
  residual_status=0
fi
printf 'meaningful_stuck_residual=%s\n' "$((1 - residual_status))"

final_status=0
if [[
  "$build_status" != 0 ||
  "$proof_status" == 0 ||
  "$residual_status" != 0
]]; then
  final_status=1
fi
printf 'SCRIPT_EXIT=%s\n' "$final_status"
exit "$final_status"

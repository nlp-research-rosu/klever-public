#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
definition="$scratch/verification-haskell-kompiled"
cp /audit-output/evidence/pinning.k "$scratch/pinning.k"
cp /audit-output/evidence/target-program-normalized.mpy \
  "$scratch/target-program-normalized.mpy"

printf 'COMMAND: bash /audit-output/evidence/stage4_pinning.sh\n'
printf '%s\n' \
  'LINK 1: trusted translator regeneration is byte-identical to submitted solution.mpy (stage2-fidelity.log)'
printf '%s\n' \
  'LINK 2: KORE parses of solution.mpy and the explicit targetProgram RHS agree'
cmp -s "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"
cmp_status=$?
printf 'submitted_vs_regenerated_cmp_exit=%s\n' "$cmp_status"
printf 'COMMAND: cd %s && kast solution.mpy --definition %s --module MPY-SYNTAX --sort Module --output kore --output-file solution.kore\n' \
  "$scratch" "$definition"
(
  cd "$scratch" || exit 1
  kast solution.mpy \
    --definition "$definition" \
    --module MPY-SYNTAX \
    --sort Module \
    --output kore \
    --output-file solution.kore
)
solution_kast_status=$?
printf 'solution_kast_exit=%s\n' "$solution_kast_status"
printf 'COMMAND: cd %s && kast target-program-normalized.mpy --definition %s --module MPY-SYNTAX --sort Module --output kore --output-file target-program.kore\n' \
  "$scratch" "$definition"
(
  cd "$scratch" || exit 1
  kast target-program-normalized.mpy \
    --definition "$definition" \
    --module MPY-SYNTAX \
    --sort Module \
    --output kore \
    --output-file target-program.kore
)
target_kast_status=$?
printf 'target_kast_exit=%s\n' "$target_kast_status"
cmp -s "$scratch/solution.kore" "$scratch/target-program.kore"
kore_cmp_status=$?
printf 'solution_vs_target_kore_cmp_exit=%s\n' "$kore_cmp_status"
sha256sum "$scratch/solution.kore" "$scratch/target-program.kore"
printf 'COMMAND: cd %s && kprove pinning.k --definition %s --spec-module PINNING --claims PINNING.program-constructor-equality\n' \
  "$scratch" "$definition"
output="$(
  cd "$scratch" &&
  kprove pinning.k \
    --definition "$definition" \
    --spec-module PINNING \
    --claims PINNING.program-constructor-equality \
    2>&1
)"
proof_status=$?
printf '%s\n' "$output"
printf 'kprove_exit=%s\n' "$proof_status"
top_status=1
if printf '%s\n' "$output" | rg -x '#Top' >/dev/null; then
  top_status=0
fi
printf 'exact_top_line=%s\n' "$((1 - top_status))"
final_status=0
if [[
  "$cmp_status" != 0 ||
  "$solution_kast_status" != 0 ||
  "$target_kast_status" != 0 ||
  "$kore_cmp_status" != 0 ||
  "$proof_status" != 0 ||
  "$top_status" != 0
]]; then
  final_status=1
fi
printf 'SCRIPT_EXIT=%s\n' "$final_status"
exit "$final_status"

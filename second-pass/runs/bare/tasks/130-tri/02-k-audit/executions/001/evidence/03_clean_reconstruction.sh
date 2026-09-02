#!/usr/bin/env bash
set -u
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

root=/tmp/audit-work/130-tri
src="$root/candidate"
build="$root/build"
overall=0

test ! -e "$build/concrete-kompiled"
kompile "$src/semantic.k" \
  --backend llvm \
  --main-module TRI-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build/concrete-kompiled"
concrete_build_status=$?
printf 'concrete_build_status=%s\n' "$concrete_build_status"
if (( concrete_build_status != 0 )); then overall=1; fi

test ! -e "$build/verification-kompiled"
kompile "$src/verification.k" \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build/verification-kompiled"
proof_build_status=$?
printf 'proof_build_status=%s\n' "$proof_build_status"
if (( proof_build_status != 0 )); then overall=1; fi

for n in 0 1 2 3 6 10; do
  krun "$src/solution.mpy" -cN="$n" \
    --definition "$build/concrete-kompiled"
  run_status=$?
  printf 'concrete_n=%s status=%s\n' "$n" "$run_status"
  if (( run_status != 0 )); then overall=1; fi
done

translated_ast="$(
  kast --definition "$build/verification-kompiled" \
    --module MPY-SYNTAX --sort Program --output kore "$src/solution.mpy"
)"
translated_status=$?
proved_ast="$(
  kast --definition "$build/verification-kompiled" \
    --module TRI-VERIFICATION --sort Program --expand-macros --output kore \
    --expression solutionProgram
)"
proved_status=$?
test "$translated_ast" = "$proved_ast"
ast_identity_status=$?
printf 'translated_kast_status=%s proved_kast_status=%s ast_identity_status=%s\n' \
  "$translated_status" "$proved_status" "$ast_identity_status"
if (( translated_status != 0 || proved_status != 0 || ast_identity_status != 0 )); then
  overall=1
fi

for item in \
  spec-eval-call.k:AUDIT-SPEC-EVAL-CALL \
  spec-run.k:AUDIT-SPEC-RUN \
  spec-value-zero.k:AUDIT-SPEC-VALUE-ZERO \
  spec-value-one.k:AUDIT-SPEC-VALUE-ONE \
  spec-value-even.k:AUDIT-SPEC-VALUE-EVEN \
  spec-value-odd-recurrence.k:AUDIT-SPEC-VALUE-ODD-RECURRENCE
do
  spec_name="${item%%:*}"
  module_name="${item#*:}"
  kprove "/audit-output/evidence/positive-claims/$spec_name" \
    --definition "$build/verification-kompiled" \
    --spec-module "$module_name"
  proof_status=$?
  printf 'positive_claim=%s module=%s status=%s\n' \
    "$spec_name" "$module_name" "$proof_status"
  if (( proof_status != 0 )); then overall=1; fi
done

printf 'overall_status=%s\n' "$overall"
exit "$overall"

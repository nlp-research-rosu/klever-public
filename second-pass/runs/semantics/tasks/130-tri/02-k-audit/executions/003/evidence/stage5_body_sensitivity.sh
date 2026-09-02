#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/130-tri-audit
evidence=/audit-output/evidence
mutant="$scratch/verification-body-mutant2.k"
mutant_spec="$scratch/spec-body-mutant2.k"
definition="$scratch/verification-body-mutant2-kompiled"
build_log="$evidence/stage5_body_mutant2_build.full.log"
proof_log="$evidence/stage5_body_mutant2_loop.full.log"
overall=0

printf 'MUTATION: executed even branch value := 2 + i // 2 (original is 1 + i // 2)\n'
printf 'SATISFYING_WITNESS: loop I=2 R=1; the first iteration should append 2, mutant appends 3\n'
printf 'COMMAND: mechanically substitute the macro body constructor in verification.k\n'
sed 's|BinOp("+", Int(1), BinOp("//", Name("i"), Int(2)))|BinOp("+", Int(2), BinOp("//", Name("i"), Int(2)))|' \
  "$scratch/verification.k" > "$mutant"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi
cp "$mutant" "$evidence/verification_body_mutant2.k"

change_count=$(diff -u "$scratch/verification.k" "$mutant" \
  | grep -F -e '-           BinOp("+", Int(1)' -e '+           BinOp("+", Int(2)' \
  | wc -l)
printf 'MUTATED_DIFF_RELEVANT_LINE_COUNT: %s\n' "$change_count"
diff -u "$scratch/verification.k" "$mutant" | sed -n '1,80p'
if [[ "$change_count" -ne 2 ]]; then overall=1; fi

sed '1c requires "/tmp/audit-work/130-tri-audit/verification-body-mutant2.k"' \
  "$scratch/spec.k" > "$mutant_spec"
cp "$mutant_spec" "$evidence/spec_body_mutant2.k"

printf '\nCOMMAND: kompile body-mutant proof definition\n'
kompile "$mutant" \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition" >"$build_log" 2>&1
status=$?
printf 'EXIT_STATUS: %d EXPECTED: 0\n' "$status"
sed -n '1,160p' "$build_log"
if [[ "$status" -ne 0 ]]; then overall=1; fi

printf '\nCOMMAND: compare expanded original and mutant executed TriFunctionBody terms\n'
kast --definition "$definition" --module TRI-VERIFICATION --sort Stmts \
  --expand-macros --expression TriFunctionBody --output json \
  > "$evidence/stage5_body_mutant2_expanded.json"
status=$?
printf 'MUTANT_KAST_EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi
cmp -s "$evidence/stage4_macro_body.json" "$evidence/stage5_body_mutant2_expanded.json"
same_status=$?
printf 'EXPANDED_BODY_CMP_EXIT_STATUS: %d EXPECTED: nonzero\n' "$same_status"
sha256sum "$evidence/stage4_macro_body.json" "$evidence/stage5_body_mutant2_expanded.json"
if [[ "$same_status" -eq 0 ]]; then overall=1; fi

printf '\nCOMMAND: kprove mutated loop claim (expected meaningful failure)\n'
kprove "$mutant_spec" \
  --definition "$definition" \
  --spec-module TRI-LOOP-SPEC \
  --output pretty >"$proof_log" 2>&1
status=$?
printf 'EXIT_STATUS: %d EXPECTED: nonzero\n' "$status"
if [[ $(wc -l < "$proof_log") -le 240 ]]; then
  sed -n '1,240p' "$proof_log"
else
  sed -n '1,120p' "$proof_log"
  printf '%s\n' '... OUTPUT BOUNDED; FULL LOG PRESERVED ...'
  tail -n 120 "$proof_log"
fi
if [[ "$status" -eq 0 ]]; then overall=1; fi
if ! grep -q 'WarnStuckClaimState' "$proof_log"; then overall=1; fi

printf '\nSTAGE5_BODY_SENSITIVITY_EXIT_STATUS: %d\n' "$overall"
exit "$overall"

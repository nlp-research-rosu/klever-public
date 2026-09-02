# Reviewer command record

All commands ran in `/audit-output` or the fresh scratch directory
`/tmp/audit-work/119-match-parens`. Candidate-provided kompiled directories
were never copied.

## Stage 1

```bash
python3 /audit-output/evidence/provenance_check.py 2>&1 \
  | tee /audit-output/evidence/stage1_provenance.log
```

Exit 0. The script checked all required pipeline-v3 records, all recorded
single-file hashes, the campaign-lock block/hash, the stage-result output map,
the prompt and translator, the complete supplied-semantics trees and every
structured-trace JSON line.

## Stage 2

```bash
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.submitted.mpy
sha256sum solution.py solution.submitted.mpy solution.regenerated.mpy
```

Each command exited 0. The submitted and regenerated MPY hashes were both
`002e09688dd1147a9fbf1d96a609099902188fee759cb8d41ef8d9ac9775f4ed`.

```bash
python3 /audit-output/evidence/differential_audit.py 2>&1 \
  | tee /audit-output/evidence/stage2_differential.log
```

Exit 0: 12 named branch/boundary cases plus all 20,481 parenthesis-string
pairs with combined length at most 10, zero mismatches.

## Stage 3

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

Exit 0; output is in `stage3_kompile_llvm.log`.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

Exit 0; output is in `stage3_kompile_haskell.log`.

```bash
python3 -c 'import ast,pathlib; a=ast.parse(pathlib.Path("solution.py").read_text()).body[0]; b=ast.parse(pathlib.Path("concrete_harness.py").read_text()).body[0]; assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False); print("harness_function_AST_identity: PASS")'
python3 py2mpy.py concrete_harness.py > concrete_harness.mpy
krun concrete_harness.mpy --definition concrete-kompiled --output json \
  | python3 check_krun_json.py
```

All exited 0. The concrete final state was empty `<k>`, `NoExc`, exit code 0.

```bash
kprove spec.k --definition proof-kompiled --spec-module SPEC \
  --claims SPEC.loop-first
kprove spec.k --definition proof-kompiled --spec-module SPEC \
  --claims SPEC.loop-second
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

Each exited 0 and printed `#Top`; bounded outputs are in the three
`stage3_kprove_*.log` files.

## Stages 4 and 5

```bash
python3 /audit-output/evidence/program_pinning_check.py 2>&1 \
  | tee /audit-output/evidence/stage4_program_pinning.log
python3 /audit-output/evidence/claim_witnesses.py 2>&1 \
  | tee /audit-output/evidence/stage4_claim_witnesses.log
```

Both exited 0. The constructor comparison covered 177 normalized body nodes
and the three ground substitutions agreed with both Python implementations.

```bash
rg -n '^\s*(configuration|syntax|rule|context|claim|alias)\b|\[(function|total|functional|simplification|priority|owise|anywhere|macro|macro-rec|symbol|concrete)' \
  verification.k spec.k reference-semantics/semantics.k \
  reference-semantics/semantics/*.k \
  > /audit-output/evidence/stage5_rule_inventory.txt
```

Exit 0. The inventory contains 1,023 source/attribute hits covering 236 syntax
declaration starts, 711 rule starts, five contexts, three claims, 45 priority
attributes, two simplification attributes, and 25 symbol declarations. Per-file
counts are in `stage5_inventory_counts.log`.

The body-sensitivity mutation was produced mechanically from the scratch spec:

```bash
sed -e 's/^module SPEC$/module SPEC-BODY-REVIEW/' \
  -e 's/            Return(Str("No")),/            Return(Str("Yes")),/' \
  spec.k > spec-body-review.k
kprove spec-body-review.k --definition proof-kompiled \
  --spec-module SPEC-BODY-REVIEW
```

The generated file is `spec_body_mutation_review.k`. `kprove` exited 1 with
`WarnStuckClaimState`; the residual showed the mutated `Yes` on the branch
where both concatenations have nonzero final balance.

## Stage 6

The fresh result mutation was produced mechanically from the scratch spec:

```bash
sed -e 's/^module SPEC$/module SPEC-FALSE-RESULT-REVIEW/' \
  -e 's/ensures ?RESULT ==K matchAnswer(A, B)/ensures ?RESULT ==K str(iCons(78, iCons(111, .IntSeq)))/' \
  spec.k > spec-false-result-review.k
kprove spec-false-result-review.k --definition proof-kompiled \
  --spec-module SPEC-FALSE-RESULT-REVIEW --dry-run
kprove spec-false-result-review.k --definition proof-kompiled \
  --spec-module SPEC-FALSE-RESULT-REVIEW
```

The generated file is `spec_false_result_review.k`. Dry-run exited 0. The real
proof exited 1 with `WarnStuckClaimState`; the residual showed actual `Yes`
against demanded `No` under the satisfiable parenthesis-only precondition.

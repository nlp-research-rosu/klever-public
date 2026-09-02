# Reviewer commands and statuses

Unless a different directory is stated, commands ran from
`/tmp/audit-work/150-x-or-y-review`. Each `stage*.log` is a bounded `script`
typescript whose footer records `COMMAND_EXIT_CODE`.

## Stage 1

From `/audit-output`:

```sh
script -q -e -c 'python3 /audit-output/evidence/check_provenance.py' /audit-output/evidence/stage1-provenance.log
```

Exit 0.

## Stage 2

```sh
script -q -e -c 'python3 py2mpy.py solution.py > solution.regenerated.mpy && cmp -s solution.regenerated.mpy solution.mpy && sha256sum solution.regenerated.mpy solution.mpy' /audit-output/evidence/stage2-regeneration.log
```

Exit 0.

From `/audit-output`:

```sh
script -q -e -c 'python3 /audit-output/evidence/differential_test.py' /audit-output/evidence/stage2-differential.log
```

Exit 0.

## Stage 3

```sh
script -q -e -c 'command -v kup; command -v kompile; command -v krun; command -v kprove; kompile --version; kprove --version; python3 --version; python3 py2mpy.py concrete_audit.py > concrete_audit.mpy; sha256sum concrete_audit.py concrete_audit.mpy' /audit-output/evidence/stage3-toolchain-and-translation.log
script -q -e -c 'kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition llvm-kompiled' /audit-output/evidence/stage3-kompile-llvm.log
script -q -e -c 'krun concrete_audit.mpy --definition llvm-kompiled' /audit-output/evidence/stage3-krun-concrete.log
script -q -e -c 'kompile verification.k --backend haskell --main-module X-OR-Y-VERIFICATION --syntax-module X-OR-Y-VERIFICATION --output-definition verification-kompiled' /audit-output/evidence/stage3-kompile-verification.log
script -q -e -c 'kprove spec.k --definition verification-kompiled --spec-module X-OR-Y-LOOP-SPEC --claims loop_correct' /audit-output/evidence/stage3-kprove-loop.log
script -q -e -c 'kompile verification.k --backend haskell --main-module X-OR-Y-SUMMARY --syntax-module X-OR-Y-SUMMARY --output-definition summary-kompiled' /audit-output/evidence/stage3-kompile-summary.log
script -q -e -c 'kprove spec.k --definition summary-kompiled --spec-module X-OR-Y-MAIN-SPEC --claims main_correct' /audit-output/evidence/stage3-kprove-main.log
```

Every command exited 0. Both positive `kprove` commands printed `#Top`.

## Stage 4

Constructor parsing:

```sh
kast solution.mpy --definition verification-kompiled --module X-OR-Y-VERIFICATION --sort Module --expand-macros --output json --output-file solution.kast.json
kast --expression xOrYBody --definition verification-kompiled --module X-OR-Y-VERIFICATION --sort Stmts --expand-macros --output json --output-file macro-body.kast.json
kast --expression '#xOrY(7, 34, 12)' --definition verification-kompiled --module X-OR-Y-VERIFICATION --sort KItem --expand-macros --output json --output-file entry.kast.json
script -q -e -c 'python3 /audit-output/evidence/constructor_compare.py' /audit-output/evidence/stage4-constructor-compare.log
script -q -e -c 'kprove adequacy-ground.k --definition summary-kompiled --spec-module X-OR-Y-ADEQUACY-GROUND' /audit-output/evidence/stage4-ground-claims.log
```

All exited 0; the ground proof printed `#Top`.

The first body probe below was an invalid attempt, preserved but not used as
evidence:

```sh
script -q -e -c 'kprove body-sensitivity.k --definition verification-kompiled --spec-module X-OR-Y-BODY-SENSITIVITY' /audit-output/evidence/stage4-body-sensitivity.log
```

Exit 113 (proof-module syntax/rule structural error).

The corrected, separately compiled body mutation:

```sh
script -q -e -c 'kompile body-mutation-verification.k --backend haskell --main-module X-OR-Y-BODY-MUT-VERIFICATION --syntax-module X-OR-Y-BODY-MUT-VERIFICATION --output-definition body-mutated-kompiled' /audit-output/evidence/stage4-kompile-body-sensitivity.log
script -q -e -c 'kprove body-sensitivity.k --definition body-mutated-kompiled --spec-module X-OR-Y-BODY-SENSITIVITY' /audit-output/evidence/stage4-body-sensitivity-valid.log
```

Compile exit 0. Proof exit 1 with `WarnStuckClaimState`; residual result is
`1`, while the original obligation requires `2`.

## Stage 5

From `/audit-output`:

```sh
script -q -e -c 'python3 /audit-output/evidence/build_rule_inventory.py && sha256sum /audit-output/evidence/rule-inventory.tsv' /audit-output/evidence/stage5-rule-inventory.log
script -q -e -c 'python3 /audit-output/evidence/compare_loop_claim_rule.py' /audit-output/evidence/stage5-loop-bridge-separation.log
```

Both exit 0.

## Stage 6

```sh
script -q -e -c 'kprove spec-vacuity.k --definition summary-kompiled --spec-module X-OR-Y-SPEC-VACUITY --dry-run' /audit-output/evidence/stage6-vacuity-dry-run.log
script -q -e -c 'kprove spec-vacuity.k --definition summary-kompiled --spec-module X-OR-Y-SPEC-VACUITY' /audit-output/evidence/stage6-vacuity-proof.log
```

Dry-run exit 0. Proof exit 1 with `WarnStuckClaimState`; residual result is
`34`, while the mutated postcondition requires `12`.

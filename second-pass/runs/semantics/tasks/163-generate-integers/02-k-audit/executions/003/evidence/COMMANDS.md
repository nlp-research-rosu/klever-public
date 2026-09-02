# Reviewer command ledger

All commands were run inside the audit container. Each referenced transcript was
captured with `script --return --quiet --command '<command>' <log>`, whose final
line records `COMMAND_EXIT_CODE`.

## Stage 1 — integrity and generation records

Working directory: `/audit-output`

```bash
python3 /audit-output/evidence/integrity_check.py
# exit 0; stage1-integrity.log

python3 /audit-output/evidence/trace_summary.py
# exit 0; stage1-trace-summary.log
```

## Stage 2 — translation and differential fidelity

Working directory: `/tmp/audit-work`

```bash
bash -lc "python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy; cmp --verbose regenerated-solution.mpy solution.mpy; sha256sum regenerated-solution.mpy solution.mpy"
# exit 0; stage2-translation.log

python3 /audit-output/evidence/differential_test.py
# exit 0; stage2-differential.log
```

## Stage 3 — clean reconstruction

Working directory: `/tmp/audit-work`

```bash
bash -lc "kompile --version; krun --version; kprove --version; python3 trusted-py2mpy.py audit_concrete_tests.py > audit_concrete_tests.mpy; sha256sum audit_concrete_tests.py audit_concrete_tests.mpy"
# exit 0; stage3-toolchain-and-test-generation.log

kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
# exit 0; stage3-kompile-llvm.log

krun audit_concrete_tests.mpy --definition audit-runtime-kompiled
# exit 0; stage3-krun-independent.log

kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled
# exit 0; stage3-kompile-haskell.log

kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --smt-timeout 10000
# exit 0, output #Top; stage3-kprove-positive.log
```

## Stage 4 — real-program pinning and witnesses

Working directory: `/tmp/audit-work`

```bash
bash -lc "kast --definition audit-verification-kompiled --module VERIFICATION --sort Module --expand-macros --expression solutionModule --output kore --output-file /audit-output/evidence/stage4-claim-program.kore; kast --definition audit-verification-kompiled --module VERIFICATION --sort Module --expand-macros solution.mpy --output kore --output-file /audit-output/evidence/stage4-submitted-program.kore; cmp --verbose /audit-output/evidence/stage4-claim-program.kore /audit-output/evidence/stage4-submitted-program.kore; sha256sum /audit-output/evidence/stage4-claim-program.kore /audit-output/evidence/stage4-submitted-program.kore"
# exit 0; stage4-program-pinning.log

kprove /audit-output/evidence/spec-witnesses.k --definition audit-verification-kompiled --spec-module SPEC-WITNESSES --smt-timeout 10000
# exit 0, output #Top; stage4-ground-witnesses.log
```

## Stage 5 — exhaustive inventory and body sensitivity

Working directory: `/audit-output` for inventory; `/tmp/audit-work` otherwise.

```bash
python3 /audit-output/evidence/rule_inventory.py
# exit 0; stage5-inventory-generation.log

kompile /audit-output/evidence/verification-body-mutation.k --backend haskell --main-module VERIFICATION-BODY-MUTATION --syntax-module MPY-SYNTAX --output-definition audit-body-mutation-kompiled
# exit 0; stage5-body-mutation-build.log

kprove /audit-output/evidence/spec-body-mutation.k --definition audit-body-mutation-kompiled --spec-module SPEC-BODY-MUTATION --smt-timeout 10000
# expected exit 1 with WarnStuckClaimState; stage5-body-mutation-proof.log
```

## Stage 6 — fresh non-vacuity mutation

Working directory: `/tmp/audit-work`

```bash
kprove /audit-output/evidence/spec-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY --dry-run
# exit 0; stage6-vacuity-dry-run.log

kprove /audit-output/evidence/spec-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY --smt-timeout 10000
# expected exit 1 with WarnStuckClaimState; stage6-vacuity-proof.log
```

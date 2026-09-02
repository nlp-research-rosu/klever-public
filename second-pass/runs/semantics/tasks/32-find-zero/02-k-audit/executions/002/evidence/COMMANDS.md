# Audit command record

Unless stated otherwise, the command ran in `/tmp/audit-work/candidate`.
Each referenced log is a `script -q -e` transcript and ends with both
`EXIT_STATUS=<n>` and the recorder's `COMMAND_EXIT_CODE`.

| Stage | Exact command | Exit | Evidence |
|---|---|---:|---|
| 1 | `python3 /audit-output/evidence/integrity_check.py` | 0 | `stage1-integrity.log` |
| 1 | `python3 /audit-output/evidence/inspect_generation.py` | 0 | `stage1-generation-inspection.log` |
| toolchain | `command -v kup; command -v kompile; command -v krun; command -v kprove; kompile --version; krun --version; kprove --version` | 0 | `toolchain.log` |
| 2 | `python3 /audit-output/evidence/fidelity_check.py` | 0 | `stage2-fidelity.log` |
| 2 | `python3 /audit-output/evidence/differential_test.py` | 0 | `stage2-differential.log` |
| 3 | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | 0 | `stage3-kompile-verification.log` |
| 3 | `kprove --definition audit-verification-kompiled --spec-module SPEC spec.k` | 0, `#Top` | `stage3-kprove-all-claims.log` |
| 3 | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | 0 | `stage3-kompile-runtime.log` |
| 3 | `krun concrete_tests.mpy --definition audit-runtime-kompiled --output none` | 0 | `stage3-krun-examples.log` |
| 3 | `krun expansion_test.mpy --definition audit-runtime-kompiled --output none` | 0 | `stage3-krun-expansion.log` |
| 3 | `python3 /audit-output/evidence/make_positive_claim_splits.py` | 0 | `stage3-make-claim-splits.log` |
| 3 | `kprove --definition audit-verification-kompiled --spec-module AUDIT-SPEC-RESULT audit-spec-result.k` | 0, `#Top` | `stage3-kprove-result-claim.log` |
| 3 | `kprove --definition audit-verification-kompiled --spec-module AUDIT-SPEC-APPROX audit-spec-approx.k` | 0, `#Top` | `stage3-kprove-approx-claim.log` |
| 4 | `python3 /audit-output/evidence/program_pinning_check.py` | 0 | `stage4-program-pinning.log` |
| 4 | `kprove --definition audit-verification-kompiled --spec-module AUDIT-GROUND-SPEC audit-ground-spec.k` | 0, `#Top` | `stage4-ground-kprove.log` |
| 5 | `python3 /audit-output/evidence/make_audit_variants.py` | 0 | `stage5-make-variants.log` |
| 5 | `python3 /audit-output/evidence/bridge_witness.py` | 0 | `stage5-bridge-witness.log` |
| 5 | `python3 /audit-output/evidence/k_rule_inventory.py` | 0 | `stage5-inventory-command.log`, `stage5-rule-inventory.json` |
| 5 | `kompile audit-no-bridges-verification.k --backend haskell --main-module AUDIT-NO-BRIDGES-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-no-bridges-kompiled` | 0 | `stage5-no-bridges-kompile.log` |
| 5 | `kprove --definition audit-no-bridges-kompiled --spec-module AUDIT-NO-BRIDGES-SPEC audit-no-bridges-spec.k` | 1, expected stuck claim | `stage5-no-bridges-kprove.log` |
| 6 | `python3 /audit-output/evidence/make_vacuity_mutation.py` | 0 | `stage6-make-mutation.log` |
| 6 | `kprove --definition audit-verification-kompiled --spec-module AUDIT-SPEC-VACUITY --dry-run audit-spec-vacuity.k` | 0 | `stage6-mutation-dry-run.log` |
| 6 | `kprove --definition audit-verification-kompiled --spec-module AUDIT-SPEC-VACUITY audit-spec-vacuity.k` | 1, expected stuck claim | `stage6-mutation-kprove.log` |

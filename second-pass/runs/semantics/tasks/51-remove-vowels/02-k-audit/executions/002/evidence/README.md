# Audit evidence index

- Stage 1: `integrity_check.py`, `stage1-integrity.log`,
  `trace_summary.py`, `stage1-trace-summary.log`
- Stage 2: `differential_test.py`, `stage2-differential.log`,
  `stage2-translation-fidelity.log`
- Stage 3: `stage3-toolchain.log`, `stage3-llvm-build.log`,
  `stage3-concrete-tests.log`, `stage3-haskell-build.log`,
  `stage3-kprove-all.log`
- Stage 4: `stage4-program-pinning.log`, `claim_witnesses.py`,
  `stage4-claim-witnesses.log`
- Stage 5: `k_inventory.py`, `stage5-k-inventory.json`,
  `stage5-k-inventory.log`, `rule_decisions.py`,
  `stage5-rule-decisions.json`, `stage5-rule-decisions.log`,
  `stage5-used-construct-map.md`
- Bridge validation: `connection-verification.k`, `connection-spec.k`,
  `stage5-bridgefree-build.log`, `stage5-bridgefree-kprove.log`
- Sensitivity: `verification-bridge-mutant.k`,
  `spec-bridge-mutant.k`, `stage5-opposite-bridge-build.log`,
  `stage5-opposite-bridge-kprove.log`,
  `verification-body-mutant.k`, `spec-body-mutant.k`,
  `stage5-body-sensitivity-build.log`,
  `stage5-body-sensitivity-kprove.log`
- Stage 6: `spec-vacuity.k`, `stage6-vacuity-witness.md`,
  `stage6-vacuity-dry-run.log`, `stage6-vacuity-kprove.log`

Every command log is produced by `run_logged.sh` and records the exact
argument vector, working directory, bounded output, and exit status.

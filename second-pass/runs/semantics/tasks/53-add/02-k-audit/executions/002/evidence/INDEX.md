# Reviewer evidence index

All commands were run against `/tmp/audit-work/53-add-clean`; no
candidate-provided compiled definition or cache was used.

- Stage 1: `provenance_check.py`, `01-provenance-check.log`,
  `trace_summary.py`, `01-generation-trace-summary.log`
- Stage 2: `differential_test.py`, `02-python-differential.log`,
  `02-translation-identity.log`
- Stage 3: `03-tool-versions.log`, `03-kompile-llvm.log`,
  `03-krun-concrete-tests.log`, `03-kompile-haskell.log`,
  `03-kprove-positive.log`
- Stage 4: `term_pinning_check.py`, `04-term-pinning.log`,
  `spec-instances.k`, `04-kprove-satisfying-instances.log`
- Stage 5: `k_rule_inventory.py`, `05-rule-inventory.log`,
  `verification-body-mutation.k`, `spec-body-mutation.k`,
  `05-kompile-body-mutation.log`, `05-kprove-body-mutation.log`
- Stage 6: `spec-vacuity-reviewer.k`, `06-vacuity-dry-run.log`,
  `06-kprove-vacuity-mutation.log`
- Shared logging helper: `run_and_log.sh`

Every command log begins with its working directory and shell-escaped command
and ends with `EXIT_STATUS`. The two expected-failure proof logs end in status
1 and contain reachable `WarnStuckClaimState` residuals; all positive build,
execution, proof, and integrity logs end in status 0.

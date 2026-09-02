# Audit evidence index

Every `.log` was produced by `run_logged.sh`, which records the exact argv,
working directory, UTC timestamps, and process exit status.

## Decisive evidence

- `stage1_integrity.log`: required-file/type checks; prompt/translator identity;
  no symlinks; exact supplied-semantics tree comparison.
- `stage1_untrusted_claims.log`: hashes and bounded summaries of all required
  provenance claims and the complete structured trace.
- `stage2_translation.log`: trusted translator regeneration and byte comparison.
- `stage2_differential.py`, `stage2_differential.log`: 3,018 deterministic
  canonical-vs-generated Python comparisons.
- `stage3_kompile_*.log`: fresh LLVM/Haskell definitions built only in scratch.
- `fresh-concrete.py`, `fresh-concrete.mpy`,
  `stage3_concrete_source_identity.log`, `stage3_krun_concrete.log`: the
  concrete harness contains the submitted function byte-for-byte, then executes
  normal, boundary, duplicate, sorting, and large-integer assertions in K.
- `stage3_connection_suite.log`, `stage3_target_suite.log`,
  `stage3_ground_bridge_suite.log`: all positive suites print `#Top`, exit 0.
- `reviewer-pinning-spec.k`, `stage4_pinning_retry.log`: regenerated literal
  body loads to the exact closure macro used by the entry claim.
- `stage4_witnesses.md`: satisfiable claim witnesses and concrete substitutions.
- `rule_inventory.tsv`, `inventory_k.py`, `inventory_counts.py`,
  `stage5_inventory_generation.log`, `stage5_inventory_counts_retry.log`:
  exhaustive 971-entry declaration/rule/claim inventory.
- `reviewer-fixed-control-spec.k`, `reviewer-bridge-control-spec.k`,
  `stage5_fixed_control.log`, `stage5_bridge_control.log`: fixed-vs-bridge value,
  continuation, and assignment-footprint comparisons.
- `reviewer-opposite-spec.k`, `stage5_opposite_value.log`: the opposite
  `allOddResult(1)` interpretation is rejected with a stuck claim.
- `reviewer-body-mutation.k`, `stage5_body_mutation_{dry_run,proof}.log`: fresh
  inverted-parity body mutation builds, then fails at the expected value.
- `reviewer-spec-vacuity.k`, `stage6_mutation_{dry_run,proof}.log`: fresh false
  whole-function result mutation builds, then fails at the result obligation.
- `stage5_dependency_check_retry.log`: connection definition imports no
  `verification.k` bridge.

## Retained diagnostics, not verdict inputs

- `stage3_claim_connection_digit_loop_general.log` succeeded, but the following
  dependency-stripped selected-claim run was interrupted; see
  `stage3_diagnostic_interruption.md`,
  `stage3_claim_connection_digit_loop_positive.log`, and
  `stage3_prove_all_summary.log`.
- `stage4_pinning.log` is the first parser-normalization attempt;
  `stage4_pinning_retry.log` is the corrected successful run.
- `stage5_dependency_check.log` matched the filename text inside comments;
  `stage5_dependency_check_retry.log` performs the exact `requires` check.
- `stage5_inventory_counts.log` contains a discarded malformed `awk` summary;
  `stage5_inventory_counts_retry.log` is the correct Python-generated summary.

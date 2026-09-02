# Reviewer evidence index

All commands were run from `/audit-output` or the clean source-only scratch
copy `/tmp/audit-work/8-sum-product`. `run-captured.sh` records the exact
argument vector, working directory, complete bounded output, and exit status.

- `stage1-records.log`: required pipeline-v3 records and generation prompt/last message.
- `stage1-integrity.log`: independent hashes, campaign comparison, required-record checks,
  tree hashes, recursive supplied-semantics comparison, and proof-artifact types.
- `stage1-generation-trace-summary.log`: full JSONL parse, event/call inventory, and
  full `codex-output.log` scan summary.
- `stage2-translation.log`: trusted regeneration and byte comparison.
- `differential_test.py`, `stage2-differential.log`: independent canonical comparison,
  preserved generation policy, inputs digest, and results.
- `stage3-tool-versions.log`, `stage3-kompile-llvm.log`,
  `stage3-kompile-haskell.log`: clean tool/build reconstruction.
- `stage3-krun-candidate-smoke.log`: fresh concrete semantics output.
- `stage3-kprove-loop-invariant.log`, `stage3-kprove-all-positive.log`:
  fresh positive proof runs.
- `pinning_check.py`, `stage4-constructor-pinning.log`: mechanical constructor-level
  source/translation/claim identity.
- `spec-ground-witness.k`, `stage4-ground-witness-kprove.log`,
  `stage4-ground-witness-python.log`: satisfying entry witness.
- `spec-body-sensitivity-reviewer.k`, `stage4-body-sensitivity.log`: actual executed-body
  mutation and expected result residual.
- `inventory_k.py`, `stage5-rule-inventory.log`: exhaustive 949-entry source inventory.
- `stage5-material-semantics.log`, `stage5-static-review.md`: relevant fixed rules and
  rule-by-rule proof-local decisions.
- `spec-baseline-connections.k`, `stage5-kompile-baseline-haskell.log`,
  `stage5-kprove-baseline-connections.log`: bridge-free fixed-semantics connections.
- `spec-helper-values.k`, `spec-helper-opposite.k`,
  `stage5-kprove-helper-values.log`, `stage5-kprove-helper-opposite.log`:
  result-bearing helper values and rejected opposite interpretation.
- `stage5-task-answer-separation.log`: no task-specific declaration in the trusted
  baseline and no proof-local operational cell rule.
- `spec-fresh-vacuity-reviewer.k`, `stage6-fresh-mutation-dry-run.log`,
  `stage6-fresh-mutation-kprove.log`: fresh buildable false-result mutation and expected
  stuck residual.

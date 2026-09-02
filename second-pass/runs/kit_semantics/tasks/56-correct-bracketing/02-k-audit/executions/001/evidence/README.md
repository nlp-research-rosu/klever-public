# Reviewer evidence index

All commands were run by the auditor. `run_logged.sh` records the shell-escaped
command, working directory, bounded output, and exit status.

## Stage 1

- `integrity_check.sh`, `integrity.log`: required-file checks, direct hashes,
  campaign-object comparison, trusted/candidate byte comparisons, symlink/type
  checks, and reviewer tree-manifest hashes.
- `generation_trace_summary.pl`, `generation-trace-summary.log`: complete JSONL
  validation, event inventory, recorded generator commands, and untrusted final
  claims.

## Stage 2

- `differential_test.py`, `differential.log`: 8,674 independent
  candidate-versus-canonical cases.
- `translation-identity.log`: trusted translation and byte comparison.

## Stage 3

- `concrete_probe.py`, `concrete-probe-translation.log`: exact-body comparison
  and trusted probe translation.
- `kompile-llvm.log`, `krun-concrete-probe.log`: fresh concrete definition and
  execution.
- `kompile-haskell.log`, `kprove-loop.log`, `kprove-full-spec.log`: fresh proof
  definition and positive target proofs.

## Stages 4–5

- `pinning_check.py`, `pinning-check.log`: constructor-level function-binding
  and body comparison.
- `claim_witnesses.py`, `claim-witnesses.log`: concrete satisfying
  substitutions.
- `rule_inventory.sh`, `rule-inventory.log`: exhaustive supplied and
  proof-local declaration/rule inventory.

## Stage 6

- `spec-audit-vacuity.k`, `vacuity-dry-run.log`,
  `kprove-fresh-vacuity.log`: fresh false-result mutation; build succeeds and
  proof fails on the expected contrary result.
- `spec-audit-body-mutation.k`, `body-mutation-dry-run.log`,
  `kprove-body-mutation.log`: fresh mutation of the closure term actually
  executed; build succeeds and the original result obligation fails.

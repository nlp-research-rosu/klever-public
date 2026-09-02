# Evidence index

All commands that determine an audit result were run through `run_logged.sh`;
each corresponding log records the shell-escaped command and `[exit_status]`.
Reviewer-authored sources are retained beside the logs.

| Area | Evidence |
|---|---|
| Toolchain and source inventory | `01-toolchain-and-inventory.log`, `04-source-review.log` |
| Supplied-semantics integrity | `check_tree_integrity.py`, `02-supplied-semantics-integrity.log` |
| Provenance checks | `03-provenance-comparison.log` |
| Isolated scratch copy | `05-scratch-copy.log` |
| Trusted translation identity | `06-translation-identity.log` |
| Differential behavior | `differential_test.py`, `differential-inputs.jsonl`, `07-differential.log` |
| Semantic source and exhaustive inventory | `08-proof-relevant-semantics.log`, `inventory_k.py`, `20-rule-inventory.tsv`, `21-opaque-and-priority-scan.log`, `22-execution-slice-source.log`, `28-inventory-cross-check.log` |
| Clean builds | `09-build-runtime.log`, `10-build-proof.log` |
| Positive claims | `spec-labeled.k`, `11-kprove-all-positive.log`, `12-kprove-max-acc.log`, `13-kprove-universal-with-lemma.log`, `14-kprove-example-one.log`, `15-kprove-example-two.log` |
| Concrete and satisfying witness | `concrete_semantics_tests.py`, `spec-ground-witness.k`, `16-generate-concrete-harness.log` through `19-python-ground-witness.log` |
| False-result non-vacuity | `spec-vacuity.k`, `23-vacuity-dry-run.log`, `24-vacuity-kprove-expected-failure.log` |
| Program-body sensitivity | `verification-body-mutated.k`, `spec-body-sensitivity.k`, `25-build-body-mutated.log` through `27-body-sensitivity-expected-failure.log` |
| Bridge-free iterator connection | `connection-verification.k`, `connection-step-spec.k`, `29-build-bridge-free-connection.log`, `31-kprove-bridge-free-step-connection.log` |
| Final report validation and manifest | `validate_report.py`, `32-final-report-validation.log`, `33-evidence-sha256.log` |

Two diagnostic attempts are retained but are not used as audit gates:

- `diagnostic-universal-without-lemma-interrupted.log` records a run in which
  claim filtering removed the auxiliary max-accumulator claim; the reviewer
  interrupted it with shell status 130. The correctly dependency-closed
  universal run is `13-kprove-universal-with-lemma.log`.
- `diagnostic-expanded-fold-untyped-stuck.log` records an over-broad reviewer
  connection claim whose `ValSeq` inversion admitted a non-`Int` head. The
  complete empty/cons iterator connection was narrowed and independently
  closed in `31-kprove-bridge-free-step-connection.log`.

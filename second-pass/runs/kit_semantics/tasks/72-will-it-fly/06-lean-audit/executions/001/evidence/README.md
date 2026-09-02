# Audit evidence index

The final judgment is in [`../REVIEW.md`](../REVIEW.md). Evidence files are
numbered in the order the audit developed; failed setup attempts are retained
so the record is complete.

## Principal evidence

- `00-audit-mode.txt`: launcher mode and selected input paths.
- `01-producer-hashes.txt`, `23-producer-provenance-verification.txt`:
  mandatory Stage 4 producer-source, image, manifest, and trusted-tool
  provenance checks.
- `02-reconstructed-inventory.json`, `03-inventory-bijection.txt`: trusted
  reconstruction of all 38 verification-closure rules and the exact protected
  Stage 3 identity comparison.
- `24-independent-classification.tsv`,
  `25-classification-reconciliation.txt`, `28-simplification-policy.txt`:
  independent rule classification and policy checks.
- `05-connection-proofs.txt`, `29-derived-proof-isolation.txt`: fresh K proofs
  and module-isolation evidence for the three derived lemmas.
- `06-recorded-hash-verification.txt`: independent audit-input and mounted-tree
  hash verification.
- `10-preflight-rerun.json`: successful rerun of the mandated trusted Stage 4
  preflight.
- `22-stage4-independent-integrity.txt`,
  `26-obligation-mathematical-judgment.md`: source-rule/obligation bijection,
  fixed-target identity, and independent mathematical relevance review.
- `14-stage5-clean-build-final.log`: complete successful `lake clean` and
  `lake build` output from the corrected fresh project.
- `15-target-and-candidate-integrity.txt`,
  `17-trusted-proof-gate.json`: target, candidate-source, and trusted final-gate
  results.
- `16-print-axioms.txt`, `30-axiom-accounting.txt`: exact Lean declaration and
  axiom output plus trust reconciliation.
- `27-target-parameter-audit.tsv`,
  `21-operational-bridge-tests-with-mutations.txt`: all 18 target-parameter
  definitions, ground tests, adversarial tests, and counterfactual mutations.

## Environment diagnosis retained for reproducibility

- `07-preflight-rerun.json`: initial preflight failure before project checking.
- `08-toolchain-diagnosis.txt`, `proc-self-check.c`: diagnosis of the audit
  sandbox's missing `/proc/<getpid()>/exe`.
- `lean-proc-self-shim.c`, `09-lean-shim-build-and-test.txt`: narrow readlink
  compatibility shim and its validation.
- `11-stage5-audit-path.txt`, `12-stage5-clean-build.log`: first incorrectly
  nested copy attempt.
- `13-stage5-audit-path-final.txt`: corrected fresh project path.
- `18-operational-bridge-tests.txt` through
  `20-operational-bridge-tests-final.txt`: intermediate test-harness attempts;
  `21-...` is the successful final run.

`SHA256SUMS` authenticates the completed evidence files and `REVIEW.md`.

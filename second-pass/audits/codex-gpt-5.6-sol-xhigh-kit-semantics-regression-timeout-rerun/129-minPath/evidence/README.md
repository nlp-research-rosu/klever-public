# Reviewer evidence index

All executable reconstruction occurred in `/tmp/audit-work/reconstruction`.
Candidate-built `runtime-kompiled/` and `verification-kompiled/` directories
were not copied or used.

- `toolchain.log`: installed K command paths and versions.
- `stage1_integrity.sh`, `stage1-integrity.log`: required artifact, symlink,
  prompt/translator identity, and recursive supplied-semantics checks.
- `stage1-untrusted-claims.log`: bounded extraction of the untrusted run
  metadata, last report, generation log, and structured-trace metadata.
- `stage2_fidelity.sh`, `stage2-fidelity.log`: trusted retranslation and
  byte-identity check plus the independent differential run.
- `stage2_differential.py`, `stage2-inputs.json`: exact 897 valid test inputs,
  out-of-contract characterization inputs, canonical comparison, and
  exhaustive legal-path oracle.
- `stage3-claim-inventory.log`: positive-claim discovery.
- `stage3_concrete.py`: reviewer-authored concrete harness.
- `stage3-translate-concrete.log`: trusted translation of the reviewer
  concrete harness.
- `stage3-runtime-build.log`, `stage3-concrete-run.log`: fresh LLVM definition
  and concrete execution.
- `stage3-proof-build.log`, `stage3-positive-target-examples.log`: fresh
  Haskell definition and independent positive proof.
- `stage4_adequacy.py`, `stage4-adequacy.log`: parsed-KAST program pinning,
  body-mutation sensitivity, and exact ground-claim witnesses.
- `stage5_inventory.py`, `stage5-rule-inventory.tsv`: exhaustive local K
  declaration/rule inventory with source hashes, flags, and per-record
  classification.
- `stage5-attribute-audit.log`: opaque, total, functional, simplification, and
  priority inventories.
- `stage6_false_witness.py`, `stage6-false-witness.log`: independent evidence
  that the reviewer mutation is false.
- `audit-spec-vacuity.k`: exact reviewer-authored false-result mutation.
- `stage6-dry-run.log`, `stage6-false-proof.log`: successful mutation
  compilation and expected stuck proof with `AssertionError`.
- `run_logged.sh`: command logger used throughout; every log records the exact
  command and exit status.

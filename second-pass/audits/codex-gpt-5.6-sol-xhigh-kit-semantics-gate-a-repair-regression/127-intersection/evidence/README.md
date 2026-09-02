# Audit evidence index

- `00_environment.log`: host, Python, and K tool versions.
- `01_integrity.sh`, `01_integrity.log`: required artifact types, symlinks,
  trusted prompt/translator comparison, recursive supplied-semantics comparison,
  and hashes.
- `01_provenance_summary.py`, `01_provenance_claims.log`: bounded parse and
  summary of untrusted generation metadata, logs, and structured trace.
- `02_translation_identity.log`: trusted retranslation and byte comparison.
- `02_differential_inputs.json`, `02_differential.py`,
  `02_differential.log`: deterministic independent Python differential test.
- `03_runtime_build.log`, `03_concrete_prepare.log`,
  `03_concrete_krun.log`: fresh LLVM build and concrete execution.
- `03_verification_build.log`, `03_kprove_divisor_loop.log`,
  `03_kprove_complete_spec.log`: fresh Haskell build and positive proofs.
- `04_body_pinning.py`, `04_claim_witnesses.py`,
  `04_pinning_and_witnesses.log`: exact translated-body pinning and satisfying
  claim witnesses.
- `04_body_mutation_check.log`: independently rerun implementation-body
  sensitivity probe.
- `05_build_rule_inventory.sh`, `05_rule_inventory.tsv`,
  `05_numbered_k_sources.txt`, `05_static_assessment.md`: exhaustive static
  inventory, numbered sources, attributes/opaque symbols, and decisions.
- `06_spec_vacuity_fresh.k`, `06_mutation_build.log`,
  `06_mutation_proof.log`: reviewer-authored false result mutation, successful
  dry-run build, and expected stuck proof residual.

# Evidence index

The numbered `.log` files are terminal transcripts. JSON and source helpers are
also retained so that the mechanical conclusions can be reproduced.

- `00_inputs_and_mode.log`: launcher mode, mounted inputs, and audit-input
  capture.
- `01_producer_provenance.log` through `07_trusted_tree_hashes.log`: producer
  file hashes, image identity, hash algorithms, and recorded tree hashes.
- `08_inventory_contract_source.log` through
  `13_inventory_classification_index.log`: trusted inventory implementation,
  frozen K source/specs, operational rules, and all 36 reconstructed identities.
- `reconstructed-inventory.json`: complete trusted inventory reconstruction.
- `independent-classification.md`: rule-by-rule independent classification.
- `14_preflight_rerun.log` through `28_lean_app_path_shim_build.log`: diagnosis
  of the sandbox `/proc` PID-namespace issue and validation of the narrow
  executable-path shim. The early failed Lean probes are environmental, not
  proof results.
- `lean_app_path_shim.c`: exact source of that shim.
- `29_preflight_rerun_with_shim.log` and `preflight-return.json`: required
  `check_generation` rerun, clean build, hashes, trust count, and fixed target.
- `30_generated_obligations_and_trust.log` through
  `34_audit_input_stage4_target.log`: generated obligation, datatype,
  injection, sidecar, and audit-input target evidence.
- `35_candidate_source_inspection.log`: complete candidate source and forbidden
  declaration/token scan.
- `36_stage5_clean_build.log`: fresh-project `lake clean` and `lake build`,
  including pre/post source hashes.
- `37_print_axioms.log`: exact `#print axioms Proof.final` output.
- `38_stage5_trust_contract.log`: trusted final-gate implementation and
  trust-inventory accounting rules.
- `40_bridge_adversarial_tests.log`: 15 successful operational-bridge examples.
- `42_counterfactual_mutations_valid.log`: six separating witnesses rejecting
  constant definitions. Logs `39` and `41` retain superseded harness-setup
  mistakes.
- `43_trusted_stage5_mechanical_gate.log` and `final-gate-return.json`: trusted
  candidate gate rerun.
- `44_connection_derived_lemma_rerun.log`: independent Stage 1 connection proof,
  returning `#Top`.
- `46_independent_stage4_check.log`: successful stdlib-only manifest,
  obligation, parameter, producer, and target check. Log `45` retains the
  superseded first checker run, which referenced a nonexistent optional audit
  field and was corrected without changing any audited input.
- `independent_stage4_check.py`: exact source of the independent Stage 4 check.
- `47_mounted_recorded_hashes.log`: mounted Stage 1, Stage 2, Stage 3, Stage 4,
  Stage 5, and producer hashes compared with `/audit-input.json`.

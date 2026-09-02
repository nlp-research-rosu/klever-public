# Audit command/evidence index

The numbered `.log` files are terminal transcripts. They include the invoked
commands, combined stdout/stderr, and exit codes where material.

| Evidence | Purpose |
|---|---|
| `00_launcher_and_file_inventory.log` | Capture `AUDIT_MODE`, launcher input, mounts, and initial file inventory. |
| `03_provenance_inventory_reconstruction_correct_hash_contract.log` | Run `provenance_inventory_check.py` with `PYTHONPATH=/reference`; hash both producer files; verify image/source manifests; reconstruct all 22 K rules and compare the protected inventory bijectively. |
| `07_check_generation_returned_evidence_with_proc_compat.log` | Required direct call to `tools.klean_preflight.check_generation` with the three requested inputs and trusted lock file; records the returned evidence. |
| `08_generated_sources_and_obligations.log` | Dump Stage 4 manifests, obligation map, trust inventory, and generated Lean sources. |
| `09_stage4_integrity_and_target_identity.log` | Run `stage4_integrity_check.py`; independently recompute mounted hashes, obligation/source bijection, exact translations, parameter bindings, and target hashes. |
| `11_fresh_lake_clean_and_build_complete.log` | Run `lake clean` and `lake build` in the fresh proof project and retain complete combined output. |
| `12_trusted_mechanical_proof_gate.log` | Run `tools.klean_final_gate.check_proof_candidate`; exact target/definition/forbidden-token checks plus another clean build and axiom parse. |
| `13_exact_axioms_and_target_identity.log` | Run Lean on `#print axioms Proof.final` and a type-ascription check against the fixed target. |
| `14_axiom_reconciliation.log` | Reconcile the two printed dependencies against the trusted inventory and built-in permitted Lean principles. The final `rg` intentionally found no literal trust-escape token and therefore returned 1; the JSON reconciliation immediately above it passed. |
| `21_final_candidate_target_shadow_and_hash_checks.log` | Re-run candidate structure checks; verify no target shadow, no forbidden tokens, exact copied `Proof.lean`, exact post-build `Base` tree, and exact target identity. |
| `22_operational_bridge_source_and_successful_compile.log` | Record the full adversarial bridge test source and compile it with Lean. |
| `23_trusted_full_mechanical_gate.log` | Run the complete launcher-bound trusted final gate. It returns `status: PASS`; its `semantic_classification: NOT_EVALUATED` is expected because the present review supplies the independent semantic judgment. |
| `24_frozen_program_spec_and_operational_semantics.log` | Capture the frozen verification rules, source solution, specification, relevant operational semantics, and Stage 1 proof script used for the independent classification/bridge judgment. |
| `25_final_review_validation.log` | Verify that `REVIEW.md` has exactly one allowed final pair and ends with the required PASS/LEGIT lines. |

Supporting executable audit sources are
`provenance_inventory_check.py`, `stage4_integrity_check.py`,
`final_candidate_integrity.py`, and `run_fresh_lean_build.py`.
`INDEPENDENT_CLASSIFICATION.md` records the independent judgment for every
inventory entry.

## Preserved diagnostic attempts

No failed attempt was deleted:

- `01_producer_provenance.log` is an initial display attempt that used an
  unsuitable `jq` query.
- `02_provenance_inventory_reconstruction.log` initially applied the generated
  Lean tree-digest contract to the producer source bundle. The corrected
  pipeline tree-hash contract is in `03_...`, and matches the launcher.
- `04_check_generation_returned_evidence.log` and
  `05_lean_toolchain_resolution.log` record a PID-namespace/procfs mismatch
  that prevented Lean from locating its own executable.
- `06_proc_pid_compat_and_lean_smoke.log` compiles and hashes the narrow
  `proc_pid_compat.c` compatibility shim, verifies the pinned Lean version,
  and runs a clean generated-project build. The shim only maps Lean's
  `getpid()` lookup to the PID visible through `/proc/self`; it does not alter
  generated or candidate source.
- `15_...` through `19_...` retain early adversarial-test elaboration failures.
  `20_...` is the first clean exit, and `22_...` is the self-contained final
  transcript with the exact successful source and command.

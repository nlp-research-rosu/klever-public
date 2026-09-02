# Evidence index

All commands ran from `/tmp/audit-work/reconstruction` unless the log records a
different `WORKDIR`. Every command log records the exact argv, bounded combined
output, and exit status.

| Evidence | Purpose | Status |
|---|---|---:|
| `01_candidate_inventory.log` | Candidate file types, names, and symlink targets | 0 |
| `02_trusted_inventory.log` | Trusted mount file types and names | 0 |
| `03_semantics_tree_diff.log` | Recursive no-dereference candidate/trusted semantics comparison | 0 |
| `04_prompt_diff.log` | Candidate/trusted prompt byte comparison | 0 |
| `05_translator_diff.log` | Candidate/trusted translator byte comparison | 0 |
| `06_provenance_presence.log` | Required provenance and structured-trace presence | 1, expected missing-file finding |
| `07_regenerate_solution_mpy.log` | Trusted translator regeneration | 0 |
| `08_solution_mpy_identity.log` | Regenerated/submitted `.mpy` byte identity | 0 |
| `09_differential.log` | Independent canonical/candidate differential test | 0 |
| `10_k_versions.log` | Fresh toolchain versions | 0 |
| `11_runtime_kompile.log` | Fresh LLVM supplied-semantics build | 0 |
| `12_concrete_smoke.log` | Candidate smoke artifact execution, used only as secondary evidence | 0 |
| `13_verification_kompile.log` | Fresh Haskell proof-definition build | 0 |
| `14_positive_claim.log` | Sole target claim proof; contains `#Top` | 0 |
| `16_pinning_and_ground_values.log` | Exact term/call pinning, satisfiable state, ground results | 0 |
| `17_body_mutation_kompile.log` | Body-sensitivity definition build | 0 |
| `18_body_mutation_proof_expected_failure.log` | Body-sensitivity stuck residual | 1, expected proof failure |
| `19_vacuity_dry_run.log` | False-postcondition mutation parse/build | 0 |
| `20_vacuity_proof_expected_failure.log` | False-postcondition stuck residual | 1, expected proof failure |
| `21_inventory_regeneration.log` | Final exhaustive inventory generation | 0 |
| `22_harness_translation.log` | Trusted translation of reviewer harness | 0 |
| `23_independent_concrete_harness.log` | Fresh concrete execution on ground cases | 0 |
| `24_scratch_source_identity.log` | Scratch/candidate source identity after tests | 0 |
| `25_source_hashes.log` | Hashes of every reconstructed source | 0 |

Reviewer-authored source evidence:

- `differential_test.py` with `differential_inputs.json`
- `pinning_check.py`
- `k_rule_inventory.py`
- `concrete_harness.py` and its trusted translation `concrete_harness.mpy`
- `verification-body-mut.k` and `spec-body-mut.k`
- `spec-vacuity.k`
- `STATIC_RULE_INVENTORY.md`
- `STATIC_REVIEW_DECISIONS.md`
- `run_logged.sh`

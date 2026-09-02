# Evidence index

The definitive audit runs are:

- `02_mechanical_reconstruction_corrected.log`: launcher-bound hashes, producer attestation, all 55 reconstructed rules and normalized hashes, all classifications, all 15 source/Lean obligation pairs, and target hashes. Ends with `ALL MECHANICAL RECONSTRUCTION CHECKS PASSED`.
- `07_klean_preflight_pass.log`: direct call to `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`; records status `PASS`, 15 obligations, target identity, and successful generated-project clean/build.
- `08_fresh_lake_clean_build.log`: separate fresh proof-mode copy below `/tmp/audit-work`, followed by literal `lake clean; lake build`; ends `Build completed successfully`.
- `09_print_axioms.log`: exact `#check Proof.final` and `#print axioms Proof.final` output.
- `10_k_float_oracle.log`: ground outputs from a newly compiled K `FLOAT.max` oracle for NaN, signed-zero, ordinary, and infinity cases.
- `12_adversarial_lean_pass.log`: successful compilation of the independent adversarial and counterfactual Lean test suite in `AdversarialAudit.lean` (zero diagnostics).
- `13_final_gate.log` and `13_final_gate.json`: trusted final-gate command, full result, status `PASS`, target identity, clean/build results, and used axioms.
- `14_operational_bridge.log`: all 27 target parameters, exact candidate definitions, KORE symbols, source-rule links, and independent operational interpretation.
- `15_identity_and_trust.log`: generated/fresh/launcher target equality, candidate tree identity, no target shadow, forbidden-token scan, exact theorem statement, and axiom reconciliation.

Helper sources are preserved as `audit_checks.py`, `run_preflight.py`, `bridge_audit.py`, and `identity_and_trust_audit.py`.

## Environment note

This container's PID namespace did not expose `/proc/<pid>/exe`, causing the pinned Lean launcher to report that it could not detect its configuration. The narrow `proc_exe_shim.c` workaround intercepts only `readlink` calls for `/proc/*/exe` and returns the already pinned Lean 4.22 tool path. It does not intercept file reads or writes and does not alter candidate or provenance inputs. Its source and compiled artifact are retained; their SHA-256 values are respectively `8154dbd289b8ec126c68ab0aac0699c83d7b8cdef457a84e3b4839d5c501e55e` and `5be8020b4f6484f89887a857da5f7c21cf6652f4a1b66599e36628e2b11e09d8`.

Logs `01`, `03`–`06`, and `11` preserve earlier audit-script/environment retries. They are not used for the verdict; the issue in each was corrected without changing any mounted input, and the definitive reruns above all exited successfully.

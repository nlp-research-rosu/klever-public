# Audit command ledger

All paths below are inside `/audit-output/evidence`. Files produced with
`script -q -e -c ...` contain the invoked command, raw combined output, and
exit status metadata.

1. `00_launcher_and_files.txt`
   - Printed `AUDIT_MODE`.
   - Attempted to format `/audit-input.json` with unavailable `jq`.
   - Enumerated mounted inputs and confirmed `/candidate` is absent.
2. `01_inputs_manifests_and_producer_hashes.txt`
   - Formatted the launcher and Stage 4 JSON inputs with Python.
   - Ran `sha256sum` on the two mounted generation-time producer files.
3. `02_frozen_stage1_and_classification.txt`
   - Printed numbered `verification.k`, `spec.k`, `solution.py`, `prove.sh`,
     and the protected Stage 3 classification.
4. `03_inventory_reconstruction_command.txt`
   - Ran `tools.k_rule_inventory.inventory_verification` with
     `PYTHONPATH=/reference`.
   - The returned canonical inventory is also preserved as
     `03_inventory_reconstruction.json`.
5. `04_inventory_bijection.txt`
   - Ran the trusted Stage 3 contract validator and independent ordered,
     unique, missing, and extra ID comparisons.
6. `05_semantic_dependencies_search.txt`
   - Searched the frozen source and semantics for `rdAcc` dependencies,
     list counting, concatenation, and append.
7. `06_recorded_hashes_and_producer_provenance.txt`
   - Ran `verify_recorded_hashes.py`.
   - Verified the signed launcher envelope; every recorded Stage 1 source
     hash; Stage 1, Stage 2, Stage 3, Stage 4, generated-project, and producer
     bundle hashes; exact producer file hashes; generator image binding; and
     classification-only candidate absence.
8. `07_preflight_command.txt`
   - First exact `tools.klean_preflight.check_generation` attempt.
   - Failed at `lake clean` because Lean could not locate its installation in
     the sandbox PID namespace. No proof or generation verdict was taken from
     this environmental failure.
9. `08_toolchain_resolution.txt` through `11_lean_sysroot_probe.txt`
   - Resolved and probed the pinned Lean/Lake installation.
   - Established that direct sysroot selection alone did not repair Lean's
     `/proc/<virtual-pid>/exe` lookup.
10. `12_proc_exe_compat_build_and_probe.txt`
    - Initial compatibility-shim compilation attempt; rejected by `-Werror`.
11. `13_proc_exe_compat_successful_probe.txt`
    - Compiled the corrected `proc_exe_compat.c`.
    - Confirmed Lean 4.22.0 commit
      `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and the matching Lake version.
12. `14_preflight_command.txt`
    - Reran the exact trusted `check_generation` call with only the
      `/proc/<pid>/exe` compatibility preload.
    - Returned `KLEAN_NO_OBLIGATIONS`; `lake clean` and `lake build` both
      exited 0.
    - The returned JSON is also preserved as
      `14_preflight_returned_evidence.json`.
13. `15_operational_semantics_bridge.txt`
    - Printed the relevant frozen for-loop, list-iteration, `count`, and
      `append` rules with source line numbers.
14. `16_independent_stage4_audit.txt`
    - Ran `independent_stage4_audit.py`.
    - Independently checked the empty domain set, exact empty obligation map,
      absence of duplicates and vacuous conjuncts, target absence, all
      cross-manifest hash bindings, exact rerun reproduction, and Stage 5
      absence.
15. `17_semantic_recurrence_check.txt`
    - Ran `semantic_recurrence_check.py`.
    - Compared `rdAcc` with an independently implemented frequency oracle on
      1,097 adversarial inputs and tested two counterfactual mutations.

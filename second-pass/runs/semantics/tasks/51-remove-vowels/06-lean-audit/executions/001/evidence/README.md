# Evidence index and material commands

All mounted candidate and provenance content was treated as untrusted data.
Only `/reference/tools` code and the authenticated Stage 4 producer sources
were executed as verification tooling.

The important commands were:

```text
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py

PYTHONPATH=/reference python3 -c \
  '... tools.k_rule_inventory.inventory_verification(Path("/reference/k-proof")) ...'

PYTHONPATH=/reference python3 -c \
  '... tools.lemma_discovery_contract.validate_trust_boundary(
         Path("/reference/k-proof"),
         Path("/reference/lemma-discovery.json")) ...'

PYTHONPATH=/reference python3 -c \
  '... tools.klean_preflight.check_generation(
         Path("/reference/k-proof"),
         Path("/reference/lemma-discovery.json"),
         Path("/reference/klean-generation"),
         toolchain_lock=Path("/reference/klean-toolchain.lock.json")) ...'

cd /tmp/audit-work/stage5-proof-audit.ya9zyF
lake clean
lake build
lake env lean AuditAxioms.lean
lake env lean AuditBridgeTests.lean

PYTHONPATH=/reference python3 -c \
  '... tools.klean_final_gate.evaluate_proof_candidate(
         Path("/reference/klean-generation"), Path("/candidate")) ...'
```

For every Lean command, the environment selected the locked toolchain at
`/opt/elan/toolchains/leanprover--lean4---v4.22.0`. The sandbox hides
`/proc/<current-pid>/exe` while exposing `/proc/self/exe`; Lean 4.22 reads the
former. `lean_proc_exe_compat.c` is the complete compatibility shim used to
redirect only that exact self-executable `readlink`. Evidence files 14, 18,
and 20 preserve the initial environment failures; file 22 is the successful
required preflight after the narrowly scoped fix.

Key evidence:

- `04_reconstructed_inventory.json`: canonical spans, normalized hashes,
  source-rule IDs, and whole inventory hash.
- `05_inventory_bijection_check.json`: exact ordered Stage 3 bijection.
- `07_stage4_producer_provenance_verdict.json`: producer hashes and immutable
  image-ID check.
- `22_rerun_check_generation_pass.json`: required fresh preflight result.
- `35_target_identity_and_candidate_integrity.json`: target, Base, and
  forbidden-token checks.
- `40_independent_obligation_bijection.json`: independent obligation mapping.
- `29_lake_clean_complete.txt` and `30_lake_build_complete.txt`: complete fresh
  proof build outputs.
- `31_print_axioms_proof_final_exact.txt`: exact `#print axioms` result.
- `34_axiom_reconciliation.json`: trust reconciliation.
- `AuditBridgeTests.lean` and
  `44_operational_bridge_and_nonvacuity_tests_pass.txt`: adversarial and
  counterfactual operational-bridge evidence.
- `39_trusted_final_mechanical_gate.json`: independent trusted mechanical gate.

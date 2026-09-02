# Evidence index

All `.log` files are raw `script(1)` transcripts containing the command and
complete captured output. Helper programs are retained beside their outputs.

- `00_producer_gate.{py,log}`: producer-file/tree hashes and immutable image ID.
- `01_rule_inventory.log`: trusted reconstruction of every local-closure rule.
- `02_inventory_compare.{py,log}`: ordered bijection with Stage 3.
- `03_hash_binding.{py,log}`: signed-resolution, mounted-tree, and 795 Stage 1
  per-file hashes.
- `04_preflight_rerun.log`: fresh trusted `check_generation` result.
- `05_stage4_bijection.{py,log}`: exact domain-rule/obligation bijection and
  generated-target identity.
- `06_fresh_copy_and_scan.log`: fresh Stage 5 setup and pre-build Base hash.
- `07_lake_clean.log`, `08_lake_build.log`: mandated clean build.
- `09_print_axioms.log`: exact `#print Proof.final` and
  `#print axioms Proof.final` output.
- `10_stage5_mechanical_check.log`: trusted Stage 5 mechanical gate.
- `11_bridge_ground_checks.log`: independently written ground/boundary checks.
- `12_mut_constant_bridges.log`: constant bridges are rejected.
- `13_mut_vacuous_guard.log`: false guard counterfactual demonstrates vacuity
  sensitivity that must be handled by the operational audit.
- `14_mut_shared_primitives.log`: shared-symbol counterfactual demonstrates why
  primitive definitions require independent review.
- `15_postbuild_identity.{py,log}`: post-build target bytes/hash, exact final
  statement, no shadowing, and candidate-only forbidden-token scan.
- `16_kprove_bridge_free_connections.log`: bridge-free fixed-semantics K claims.
- `17_axiom_reconcile.{py,log}`: exact axiom reconciliation.
- `18_environment_scope.log`, `lean_proc_self_shim.c`: documented PID-namespace
  workaround and mount-scope check.

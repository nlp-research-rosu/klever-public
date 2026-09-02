# Audit command manifest

All Python checks that import trusted audit tooling used
`PYTHONPATH=/reference`. Lean/Lake commands used the independently compiled
`/tmp/audit-work/lean_proc_exe_shim.so` only to resolve sandbox-hidden
`/proc/*/exe` links to the lockfile-pinned Lean 4.22.0 executables.

| Purpose | Command | Result evidence |
|---|---|---|
| Audit context | `python3 -c '<read /audit-input.json and AUDIT_MODE>'` | `00a-audit-context.log` (exit 0) |
| Producer integrity | `PYTHONPATH=/reference python3 check_producer_integrity.py` | `01-producer-integrity-correct-algorithm.log` (PASS, exit 0) |
| Rule reconstruction | `PYTHONPATH=/reference python3 reconstruct_inventory.py` | `02-inventory-reconstruction.log` (PASS, exit 0) |
| Shim build | `cc -shared -fPIC -O2 -Wall -Wextra -ldl lean_proc_exe_shim.c -o /tmp/audit-work/lean_proc_exe_shim.so` followed by pinned `lean --version` and `lake --version` | `05-independent-lean-shim-build.log` (exit 0) |
| Trusted Stage 4 preflight | `PYTHONPATH=/reference LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so python3 run_stage4_preflight.py` | `06-stage4-preflight-rerun-success.log` (PASS, exit 0; includes the checker's exact `lake clean` and `lake build` commands and complete output) |
| Independent Stage 4 integrity | `PYTHONPATH=/reference python3 check_stage4_integrity.py` | `07-stage4-integrity.log` (PASS, exit 0) |
| Fresh Stage 5 clean | `LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake clean` in `/tmp/audit-work/stage5-clean-project` | `09-stage5-lake-clean.log` (exit 0) |
| Fresh Stage 5 build | `LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake build` in `/tmp/audit-work/stage5-clean-project` | `10-stage5-lake-build.log` (exit 0) |
| Exact final type and axioms | `LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake env lean AxiomAudit.lean` | `11-proof-final-axioms.log` (exit 0) |
| Axiom reconciliation | `PYTHONPATH=/reference python3 reconcile_axioms.py` | `12-axiom-reconciliation.log` (PASS, exit 0) |
| Candidate/static target gate | `PYTHONPATH=/reference python3 check_candidate_static.py` | `13-candidate-static-and-target.log` (PASS, exit 0) |
| Bridge examples | `LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake env lean BridgeAudit.lean` | `14b-bridge-adversarial-examples-passing.log` (exit 0) |
| Constant-nsScan mutation | `LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake build` in `/tmp/audit-work/mutation-nsscan` | `16-counterfactual-nsscan-constant.log` (expected exit 1) |
| Identity-map mutation | `LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake build` in `/tmp/audit-work/mutation-map` | `17-counterfactual-map-identity.log` (expected exit 1) |
| Constant-membership mutation | `LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake build` in `/tmp/audit-work/mutation-membership` | `19-counterfactual-membership-vacuity.log` (expected exit 1) |

The exact mutation diffs are retained in
`15b-counterfactual-nsscan-diff.log`,
`15c-counterfactual-map-diff.log`, and
`18b-counterfactual-membership-diff.log`.

# Raw command and result index

Unless stated otherwise, commands ran with working directory `/audit-output`.
Each linked log is an unedited `script(1)` transcript with its exit code.

| Purpose | Exact substantive command | Result |
|---|---|---|
| Authenticate producer sources | `PYTHONPATH=/reference python3 /audit-output/evidence/authenticate_producers.py` | [01-producer-authentication.log](/audit-output/evidence/01-producer-authentication.log) |
| Reconstruct and compare the rule inventory | `PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py` | [02-inventory-reconstruction.log](/audit-output/evidence/02-inventory-reconstruction.log) |
| Initial preflight attempt | `PYTHONPATH=/reference python3 /audit-output/evidence/rerun_preflight.py` | [03a-preflight-initial-procfs-failure.log](/audit-output/evidence/03a-preflight-initial-procfs-failure.log) |
| Compile the procfs compatibility shim and verify the pinned tools | `cc -shared -fPIC -O2 -Wall -Wextra -Werror -o /tmp/audit-work/proc_self_exe_fix.so /audit-output/evidence/proc_self_exe_fix.c -ldl && LD_PRELOAD=/tmp/audit-work/proc_self_exe_fix.so lean --version && LD_PRELOAD=/tmp/audit-work/proc_self_exe_fix.so lake --version` | [03b-lean-procfs-workaround.log](/audit-output/evidence/03b-lean-procfs-workaround.log) |
| Required trusted preflight rerun | `LD_PRELOAD=/tmp/audit-work/proc_self_exe_fix.so PYTHONPATH=/reference python3 /audit-output/evidence/rerun_preflight.py` | [03-preflight-rerun.log](/audit-output/evidence/03-preflight-rerun.log) |
| Recheck launcher, manifest, file, and tree hashes plus obligation/target bijection | `PYTHONPATH=/reference python3 /audit-output/evidence/verify_hashes_and_generation.py` | [04-hashes-generation-bijection.log](/audit-output/evidence/04-hashes-generation-bijection.log) |
| Display frozen source | `nl -ba /reference/k-proof/solution.py` | [05a-frozen-source.log](/audit-output/evidence/05a-frozen-source.log) |
| Display frozen claims | `nl -ba /reference/k-proof/spec.k` | [05b-frozen-spec.log](/audit-output/evidence/05b-frozen-spec.log) |
| Display loop semantics | `nl -ba /reference/k-proof/reference-semantics/semantics/controls.k \| sed -n "62,108p"` | [05c-operational-loop-semantics.log](/audit-output/evidence/05c-operational-loop-semantics.log) |
| Display string semantics | `nl -ba /reference/k-proof/reference-semantics/semantics/str.k \| sed -n "7,41p"` | [05d-operational-string-semantics.log](/audit-output/evidence/05d-operational-string-semantics.log) |
| Display list/append semantics | `nl -ba /reference/k-proof/reference-semantics/semantics/list.k \| sed -n "8,55p"` | [05e-operational-list-semantics.log](/audit-output/evidence/05e-operational-list-semantics.log) |
| Display operator semantics | `nl -ba /reference/k-proof/reference-semantics/semantics/operators.k \| sed -n "10,42p"` | [05f-operational-operator-semantics.log](/audit-output/evidence/05f-operational-operator-semantics.log) |
| Apply the independent per-rule classification | `PYTHONPATH=/reference python3 /audit-output/evidence/independent_classification.py` | [06-independent-classification.log](/audit-output/evidence/06-independent-classification.log) |
| Run adversarial summary-state checks and counterfactuals | `python3 /audit-output/evidence/semantic_summary_check.py` | [07-semantic-adversarial-check.log](/audit-output/evidence/07-semantic-adversarial-check.log) |
| Display authenticated producer routing logic | `sed -n "1536,1655p" /reference/generation-tools/klean_export.py` | [08a-generation-obligation-routing.log](/audit-output/evidence/08a-generation-obligation-routing.log) |
| Display generated lemma module | `nl -ba /reference/klean-generation/generated/Klean117SelectWords/Lemmas.lean` | [08b-generated-target-absence.log](/audit-output/evidence/08b-generated-target-absence.log) |
| Display obligation map | `nl -ba /reference/klean-generation/generated/obligation-map.json` | [08c-obligation-map.log](/audit-output/evidence/08c-obligation-map.log) |
| Confirm absence of Stage 5 candidate | `find /candidate -maxdepth 1 -print` | [08d-candidate-absence.log](/audit-output/evidence/08d-candidate-absence.log) |

The read-only audit helpers used by those commands are preserved beside the
logs. They do not import or execute `solution.py` or any prior review artifact.

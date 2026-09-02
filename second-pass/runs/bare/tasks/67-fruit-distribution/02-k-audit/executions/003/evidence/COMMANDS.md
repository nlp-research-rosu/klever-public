# Reviewer command index

All paths below are container paths. Full bounded output and inner command
lines are in the named log.

| Purpose | Exact top-level command | Exit | Log |
|---|---|---:|---|
| provenance | `python3 /audit-output/evidence/01_provenance_check.py` | 0 | `01_provenance_check.log` |
| generation records | `python3 /audit-output/evidence/01_generation_record_scan.py` | 0 | `01_generation_record_scan.log` |
| translation | `python3 /reference/py2mpy.py /tmp/audit-work/fruit67/candidate/solution.py > /tmp/audit-work/fruit67/regenerated-solution.mpy`; then `cmp -s /tmp/audit-work/fruit67/regenerated-solution.mpy /tmp/audit-work/fruit67/candidate/solution.mpy` | 0, 0 | `02_translation_identity.log` |
| differential | `python3 /audit-output/evidence/02_differential.py` | 0 | `02_differential.log` |
| fresh builds/proof | `bash /audit-output/evidence/03_rebuild.sh` | 0 | `03_rebuild.log` |
| concrete K/Python comparison | `python3 /audit-output/evidence/03_concrete_compare.py` | 0 | `03_concrete_compare.log` |
| constructor pinning/body mutation | `bash /audit-output/evidence/04_pinning_and_body_sensitivity.sh` | 0 (the expected mutated `kprove` exits 1) | `04_pinning_and_body_sensitivity.log` |
| rule inventory | `bash /audit-output/evidence/04_rule_inventory.sh` | 0 | `04_rule_inventory.log` |
| `findString` witness | `bash /audit-output/evidence/05_find_hook_witness.sh` | 0 | `05_find_hook_witness.log` |
| repeated-space string claim | `bash /audit-output/evidence/05_string_boundary_claim.sh` | 0 (the expected boundary `kprove` exits 1) | `05_string_boundary_claim.log` |
| fresh false result mutation | `bash /audit-output/evidence/06_nonvacuity.sh` | 0 (the expected mutated `kprove` exits 1) | `06_nonvacuity.log` |

`03_concrete_matrix.log` and `03_llvm_normal_witness.log` preserve preliminary
LLVM crash/timeout observations. They are not used as candidate-verdict gates;
the terminating direct-hook comparison in `05_find_hook_witness.log` is the
bounded backend discrepancy evidence.

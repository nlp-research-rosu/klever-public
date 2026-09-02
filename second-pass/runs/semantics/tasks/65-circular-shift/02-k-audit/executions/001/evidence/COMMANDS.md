# Executed command ledger

All build and proof commands ran against source copies under
`/tmp/audit-work`; no candidate-provided compiled definition was copied.
The named logs contain the complete bounded output.

| Purpose | Exact command | Status | Evidence |
|---|---|---:|---|
| Provenance | `script -q -e -c '/audit-output/evidence/01_provenance.sh' /audit-output/evidence/01_provenance.log` | 0 | `01_provenance.log` |
| MPY identity + differential | `script -q -e -c '/audit-output/evidence/02_fidelity.sh' /audit-output/evidence/02_fidelity.log` | 0 | `02_fidelity.log` |
| Fresh LLVM build | `script -q -e -c '/audit-output/evidence/03_build_runtime.sh' /audit-output/evidence/03_build_runtime.log` | 0 | `03_build_runtime.log` |
| Fresh concrete execution | `script -q -e -c '/audit-output/evidence/03_run_concrete.sh' /audit-output/evidence/03_run_concrete.log` | 0 | `03_run_concrete.log` |
| Fresh Haskell build | `script -q -e -c '/audit-output/evidence/03_build_proof.sh' /audit-output/evidence/03_build_proof.log` | 0 | `03_build_proof.log` |
| Normal claim | `script -q -e -c '/audit-output/evidence/03_prove_claim.sh CIRCULAR-SHIFT-SPEC.normal-shift' /audit-output/evidence/03_prove_normal.log` | 0, `#Top` | `03_prove_normal.log` |
| Oversize claim | `script -q -e -c '/audit-output/evidence/03_prove_claim.sh CIRCULAR-SHIFT-SPEC.oversize-shift' /audit-output/evidence/03_prove_oversize.log` | 0, `#Top` | `03_prove_oversize.log` |
| Adequacy witnesses | `script -q -e -c 'python3 /audit-output/evidence/04_adequacy.py' /audit-output/evidence/04_adequacy.log` | 0 | `04_adequacy.log` |
| Inventory generation | `python3 /audit-output/evidence/05_static_inventory.py > /audit-output/evidence/05_static_inventory.tsv` | 0 | `05_inventory_generation.log` |
| Per-row assessment | `python3 /audit-output/evidence/05_rule_assessment.py > /audit-output/evidence/05_rule_assessment.tsv` | 0 | `05_inventory_generation.log` |
| Program-body sensitivity | `script -q -e -c '/audit-output/evidence/05_program_body_sensitivity.sh' /audit-output/evidence/05_program_body_sensitivity.log` | wrapper 0; build 0; expected proof 1 | `05_program_body_sensitivity.log` |
| False-result non-vacuity | `script -q -e -c '/audit-output/evidence/06_nonvacuity.sh' /audit-output/evidence/06_nonvacuity.log` | wrapper 0; dry-run 0; expected proof 1 | `06_nonvacuity.log` |
| Remove `intCodes` abstraction | `script -q -e -c '/audit-output/evidence/07_without_intcodes.sh' /audit-output/evidence/07_without_intcodes.log` | build 0; proof 1 | `07_without_intcodes.log` |

The scripts themselves print the exact inner `kompile`, `krun`, and `kprove`
commands and their individual exit statuses. The two expected proof failures
both contain `WarnStuckClaimState` and the unmet result equality; neither is a
parse, import, build, timeout, or backend failure.

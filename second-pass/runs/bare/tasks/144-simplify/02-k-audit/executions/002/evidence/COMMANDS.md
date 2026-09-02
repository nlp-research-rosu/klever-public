# Audit command/status index

All paths are the mounted audit paths. Shell scripts use `set -x`, so their
logs contain the exact expanded commands as executed.

| Stage | Exact outer command | Outer exit | Important inner status |
|---|---|---:|---|
| 1 | `/audit-output/evidence/stage1_integrity.py` | 0 | All integrity assertions passed. |
| 2 | `/audit-output/evidence/run_stage2.sh` | 0 | `cmp` and differential test both 0. |
| 3 build | `/audit-output/evidence/run_stage3_build.sh` | 0 | Both `kompile` commands 0. |
| 3 concrete | `/audit-output/evidence/run_stage3_concrete.sh` | 0 | Six `krun`/Python comparisons passed. |
| 3 general | `cd /tmp/audit-work/reconstruction && kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.simplify-general` | 0 | `#Top`. |
| 3 example true | `cd /tmp/audit-work/reconstruction && kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.example-true` | 0 | `#Top`. |
| 3 example false one | `cd /tmp/audit-work/reconstruction && kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.example-false-one` | 0 | `#Top`. |
| 3 example false two | `cd /tmp/audit-work/reconstruction && kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.example-false-two` | 0 | `#Top`. |
| 4 pinning | `/audit-output/evidence/program_pinning.py` | 0 | Parsed constructor equality true. |
| 4 body mutation | `/audit-output/evidence/run_stage4_body_mutation.sh` | 0 | Inner `kprove` exit 1, expected stuck result mismatch. |
| 5 inventory | `/audit-output/evidence/run_stage5_inventory.sh` | 0 | 32 semantic rules, 4 verification rules, 4 claims. |
| 5 bridge checks | `/audit-output/evidence/run_stage5_bridge_checks.sh` | 0 | Each bridge-free `kprove` exit 1 with a symbolic unmet equality. |
| 5 long input | `/audit-output/evidence/long_input_semantics.py` | 0 | Python `ValueError`; `krun` exit 0/result true. |
| 6 mutation | `/audit-output/evidence/run_stage6_nonvacuity.sh` | 0 | Inner `kprove` exit 1 with actual true versus mutated false. |

The corresponding logs are named `stage*.log` in this directory. Failed
reviewer-script formulations retained with `_attemptN` suffixes are not used
as candidate evidence.

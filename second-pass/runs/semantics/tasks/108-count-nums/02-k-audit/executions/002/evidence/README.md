# Reviewer evidence index

All commands were run from `/tmp/audit-work/reconstruction` unless noted.
Candidate-provided compiled definitions and caches were not copied.

| Stage | Reviewer command/artifact | Result |
|---|---|---|
| 1 | `python3 /audit-output/evidence/audit_integrity.py` | exit 0; `INTEGRITY_CHECK=PASS` in `01-integrity.log` |
| 1 | `python3 /audit-output/evidence/inspect_generation_trace.py` | exit 0; complete 661-record trace and 80,135-line output log indexed |
| 2 | `python3 py2mpy.py solution.py > regenerated-solution.mpy`; `cmp -s regenerated-solution.mpy solution.mpy` | both exit 0; byte identity |
| 2 | `python3 /audit-output/evidence/differential_test.py` | exit 0; 9,421 arrays; zero mismatches |
| 3 | `/audit-output/evidence/run_positive_proofs.sh` | exit 0; fresh LLVM run plus eight fresh Haskell proof commands |
| 4 | `python3 /audit-output/evidence/constructor_identity.py` | exit 0; all four bodies/closures and helper bindings constructor-identical |
| 4 | `kprove audit-witness-spec.k --definition audit-loop-base-kompiled --spec-module AUDIT-WITNESS-SPEC` | exit 0; `#Top` |
| 5 | `/audit-output/evidence/run_bridge_witnesses.sh` | exit 0 as an audit driver; all expected fixed/extended outcomes observed |
| 5 | `python3 /audit-output/evidence/build_rule_inventory.py` | exit 0; 1,210-row exhaustive inventory |
| 6 | `kprove spec-vacuity-audit.k --definition audit-count-loop-kompiled --spec-module COUNT-NUMS-VACUITY-AUDIT --dry-run` | exit 0 |
| 6 | `kprove spec-vacuity-audit.k --definition audit-count-loop-kompiled --spec-module COUNT-NUMS-VACUITY-AUDIT` | exit 1 with `WarnStuckClaimState`, as expected |

The exact `kompile`, `krun`, and `kprove` argument vectors and exit statuses
are recorded at the top of the corresponding `03-*.log`, `05-*.log`, and
`06-*.log` files. Logs are bounded by the reviewer drivers; no positive proof
result was inferred from a candidate log.

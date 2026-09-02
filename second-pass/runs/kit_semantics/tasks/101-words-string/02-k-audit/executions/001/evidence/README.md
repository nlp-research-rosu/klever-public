# Reviewer evidence index

All execution and mutation work occurred below
`/tmp/audit-work/reconstruction`. Candidate compiled definitions were not used.

| Stage | Reviewer artifact | Recorded result |
|---|---|---|
| 1 | `verify_provenance.py`, `stage1-provenance.log` | All required mounts, file hashes, pipeline tree hashes, semantics entries, and symlink checks pass |
| 1 | `inspect_generation_records.py`, `stage1-generation-record-inspection.log` | All pipeline-v3 generation records and 221 structured trace events inspected as untrusted history |
| 2 | `differential_test.py`, `run_stage2.sh`, `stage2-program-fidelity.log` | Trusted translation byte identity; 24,431 cases, zero mismatches |
| 3 | `run_stage3.sh`, `stage3-clean-reconstruction.log` | Fresh LLVM/Haskell builds exit 0; concrete run exit 0; target proof `#Top`, exit 0 |
| 4 | `extract_claim_program.py`, `ground_result_check.py`, `stage4-pinning.log` | Mechanically extracted claim module has identical constructor AST; seven ground substitutions agree |
| 5 | `build_rule_inventory.py`, `rule-inventory.md` | Exhaustive 1,073-record source inventory with a decision for every declaration/rule |
| 6 | `audit-spec-vacuity.k`, `audit-spec-body-sensitivity.k`, `run_mutations.sh`, `stage6-mutations.log` | Both dry-runs exit 0; both false proofs exit 1 for visible result mismatches |
| 6 | `stage6-mutations-development.log` | Retained exploratory unsupported mutation; explicitly not used as evidence |

The exact commands and per-command statuses are printed in the corresponding
stage logs. `manifest.sha256` hashes the final reviewer-authored evidence set.

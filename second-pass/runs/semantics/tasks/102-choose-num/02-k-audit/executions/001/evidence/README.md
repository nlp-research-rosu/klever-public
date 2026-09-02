# Reviewer evidence index

All source builds and mutations ran under `/tmp/audit-work/102-choose-num`.
Candidate-provided compiled definitions and caches were not copied or used.

| Audit activity | Reviewer artifact | Transcript | Terminal status |
|---|---|---|---:|
| Provenance and supplied-semantics integrity | `01_provenance.sh` | `01_provenance.log` | 0 (individual missing-file probes are recorded as 1) |
| Trusted translation and differential testing | `differential_test.py`, `02_program_fidelity.sh` | `02_program_fidelity.log` | 0 |
| Fresh LLVM build and concrete execution | `concrete_audit.py`, `03_concrete_rebuild.sh` | `03_concrete_rebuild.log` | 0 |
| Fresh Haskell build and five independent positive claims | `04_proof_rebuild.sh` | `04_proof_rebuild.log` | 0 |
| Ground witnesses for every claim | `claim_witnesses.py`, `05_claim_witnesses.sh` | `05_claim_witnesses.log` | 0 |
| Exact translated-body pinning | `program_pinning.py`, `05b_program_pinning.sh` | `05b_program_pinning.log` | 0 |
| Fresh false-result mutation | `spec-vacuity.k`, `06_nonvacuity.sh` | `06_nonvacuity.log` | 1, expected proof rejection after dry-run exit 0 |
| Exhaustive static inventory | `rule_inventory.py`, `rule_inventory.md`, `07_static_inventory.sh` | `07_static_inventory.log` | 0 |
| Independent body-sensitivity mutation | `verification-body-mutation.k`, `spec-body-mutation.k`, `08_body_sensitivity.sh` | `08_body_sensitivity.log` | 1, expected proof rejection after build/dry-run exit 0 |

The shell transcripts print each exact nested command and its exit status. The
two status-1 transcripts are successful negative tests: both show
`WarnStuckClaimState` and an unmet result equality, not a parser, import, build,
timeout, or infrastructure failure.

# Auditor evidence index

All commands were run against source copied to
`/tmp/audit-work/reconstruction`. Candidate-provided compiled definitions and
caches were not copied or used.

| Stage | Primary command record | Supporting auditor artifacts |
|---|---|---|
| 1 | `01_integrity.sh`, `01_integrity.log` | Independent mounted-input hashes, record-layout checks, JSONL validation, symlink checks, recursive supplied-semantics comparison |
| 2 | `02_fidelity.sh`, `02_fidelity.log` | `differential_test.py` |
| 3 | `03_reconstruction.sh`, `03_reconstruction.log` | `k_concrete_tests.py` |
| 4–5 | `04_inventory.sh`, `04_inventory.log`; `05_adequacy_extensions.sh`, `05_adequacy_extensions.log`; `06_static_checks.sh`, `06_static_checks.log` | `rule_inventory.py`, `claim_witness.py`, bridge specs, constructor JSONs, body mutation, `extension_equation_checks.py` |
| 6 | `07_nonvacuity.sh`, `07_nonvacuity.log` | `spec-vacuity.k` |

The files ending in `_initial.log`, `_interrupted.log`, or
`spec-vacuity-initial.k` preserve exploratory attempts. They are not cited as
positive evidence. In particular, the initial vacuity mutation encountered an
unrelated unsupported float hook and was rejected; the final loop-summary
mutation is the valid non-vacuity test.

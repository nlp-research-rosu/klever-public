# Reviewer evidence index

All executed candidate sources were copied to
`/tmp/audit-work/0-has-close-elements`; no candidate compiled definition or
cache was copied or used. Logs are deliberately bounded by the reviewer
scripts.

| Stage | Reviewer artifacts | Result |
|---|---|---|
| 1 | `stage1_integrity.sh`, `stage1-integrity.log` | trusted mount present; prompt/translator/semantics exact; no symlinks or special entries |
| 2 | `differential_audit.py`, `differential-inputs.json`, `stage2_fidelity.sh`, `stage2-fidelity.log` | translator byte identity; 12,903 canonical comparisons; zero mismatches |
| 3 | `stage3_reconstruct.sh`, `stage3-build-*.log`, `stage3-prove-*.log` | fresh LLVM and three Haskell builds; four exact `#Top`, exit 0 |
| 4 | `concrete_audit.py`, `stage4_witness.py`, `stage4_adequacy.sh`, `stage4-*.log` | actual module poststate, nine LLVM assertions, and three satisfying witnesses agree |
| 5 | `rule_inventory.py`, `rule-inventory.md`, `rule-assessment.md`, `used-construct-map.md`, `operational-context.k`, `bridge-body-mutation.k`, `stage5_static_and_context.sh`, `stage5-*.log` | exhaustive inventory; four fixed/extended context proofs close; changed body fails at `j=2` |
| 6 | `nonvacuity-mutation.k`, `stage6_nonvacuity.sh`, `stage6-*.log` | mutation dry-run exit 0; proof exit 1 with `WarnStuckClaimState` and `<k>false` |
| 7 | `toolchain_versions.sh`, `toolchain-versions.log`, `MANIFEST.sha256` | environment and evidence hashes |

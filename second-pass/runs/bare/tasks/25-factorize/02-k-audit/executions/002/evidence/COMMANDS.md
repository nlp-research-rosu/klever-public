# Reviewer command/status index

All source builds and executions used the scratch copy at
`/tmp/audit-work/25-factorize`. Candidate-provided compiled definitions and
caches were not present or reused.

| Stage | Exact command | Exit/status |
|---|---|---|
| 1 | `bash /audit-output/evidence/run_stage1.sh > /audit-output/evidence/stage1_integrity.log 2>&1` | 0; `STAGE1_INTEGRITY_RESULT=PASS` |
| 2 | `bash /audit-output/evidence/run_stage2.sh > /audit-output/evidence/stage2_program_fidelity.log 2>&1` | wrapper 0; translation/cmp 0; differential 1 because two intended-domain mismatches were found |
| 3 build | `bash /audit-output/evidence/run_stage3_build.sh > /audit-output/evidence/stage3_build.log 2>&1` | 0; both Haskell definitions built |
| 3 LLVM | `kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition fresh-semantic-llvm-kompiled` | 0; see `stage3_llvm_build.log` |
| 3 concrete | `python3 /audit-output/evidence/compare_generated_semantics.py > /audit-output/evidence/stage3_concrete_execution.log 2>&1` | 1 because K disagreed with actual `solution.py` at `n=1000003`; all `krun` subprocesses exited 0 |
| 3 claims | `bash /audit-output/evidence/run_positive_claims.sh > /audit-output/evidence/stage3_positive_claims.log 2>&1` | 0; 26/26 individual claims exited 0 with `#Top` |
| 4 pinning | `bash /audit-output/evidence/run_stage4_pinning.sh > /audit-output/evidence/stage4_pinning.log 2>&1` | wrapper 0; AST comparison/build 0; body-sensitivity proof 1 as expected |
| 4 witnesses | `python3 /audit-output/evidence/claim_witnesses.py > /audit-output/evidence/stage4_claim_witnesses.log 2>&1` | 0; all 26 substitutions match |
| 5 inventory | `python3 /audit-output/evidence/static_k_inventory.py > /audit-output/evidence/stage5_static_inventory.md 2>&1` | 0; 37 declarations and 62 rules |
| 6 | `bash /audit-output/evidence/run_stage6_vacuity.sh > /audit-output/evidence/stage6_fresh_vacuity.log 2>&1` | wrapper 0; dry-run/build 0; false proof 1 with expected stuck obligation |

Nested exact commands, exit statuses, and bounded relevant outputs are printed
in the corresponding stage logs.

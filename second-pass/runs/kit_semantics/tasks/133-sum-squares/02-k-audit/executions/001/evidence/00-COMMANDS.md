# Reviewer command index

All scripts use `set -x` or print every check they perform. Terminal transcripts
were captured with `script -q -e -c ...`, whose footer records the wrapper exit.

| Stage | Exact top-level command | Exit/result |
|---|---|---|
| 1 | `python3 /audit-output/evidence/01_provenance_audit.py` | 0; `PROVENANCE_AUDIT_OK` |
| 1 | `python3 /audit-output/evidence/01_trace_call_inventory.py` | 0; one 272-line JSONL trace read completely |
| 2 | `bash /audit-output/evidence/02_program_fidelity.sh` | 0; translation `cmp` 0 and 3,055 differential cases with zero mismatches |
| 3 | `bash /audit-output/evidence/03_clean_rebuild.sh` | 0; fresh LLVM/Haskell builds, `krun` 0, focused loop `kprove` 0/`#Top`, all-claims `kprove` 0/`#Top` |
| 4 | `bash /audit-output/evidence/04_pinning_ground.sh` | 0; constructor identity and two ground claims `#Top` |
| 4 | `bash /audit-output/evidence/04_body_sensitivity.sh` | wrapper 0; mutated positive proof exits 1 with `WarnStuckClaimState` and `sumCeilSquares(VS)+1 != sumCeilSquares(VS)` |
| 5 | `python3 /audit-output/evidence/05_rule_inventory.py` | 0; 935 exhaustive entries |
| 5 | `bash /audit-output/evidence/05_ceil_bridge.sh` | 0; 75 CPython-oracle assertions execute in K with `.K`, `NoExc`, semantic exit 0 |
| 6 | `bash /audit-output/evidence/06_nonvacuity.sh` | wrapper 0; mutation dry-run 0, mutation proof 1 with reachable residual 14 against destination 15 |

`03-clean-rebuild-attempt1-reviewer-test-error.log` is retained because the
first reviewer concrete witness accidentally asserted 10 instead of
`ceil(2.0000000000000004)^2 + ceil(-2.4)^2 = 13`. The runtime correctly
rejected it. The corrected test was followed by deletion of only the newly
generated scratch LLVM definition and a full clean rebuild.

`05-ceil-bridge-attempt1-parser-oom.log` is retained because the first bridge
suite used an impractically large 359-assertion AST and the K Java parser was
killed with exit 137 before execution. The same deterministic boundary test
was reduced to 75 cases and then completed successfully. Neither failed
reviewer-authored attempt is used as evidence against the candidate.

# Command/status index

The detailed stdout/stderr appears in the named log. Commands ran from
`/tmp/audit-work/37-sort-even` unless noted.

| Stage | Exact core command | Status/result | Log |
|---|---|---|---|
| 1 | `command -v kompile; kompile --version; command -v kprove; kprove --version; command -v krun; krun --version` | all present; K 7.1.293 | `toolchain.txt` |
| 1 | `python3 /audit-output/evidence/inspect_provenance.py` | exit 0; campaign exact; required records/hashes/trace valid | `stage1-provenance-full.txt` |
| 1 | `sha256sum` over launcher records, trusted inputs, candidate prompt/translator, and every declared evidence file | all per-file hashes match | `stage1-hashes-and-trace-shape.txt` |
| 2 | `python3 /reference/py2mpy.py /tmp/audit-work/37-sort-even/solution.py > /tmp/audit-work/37-sort-even/regenerated-solution.mpy` | exit 0 | `stage2-fidelity-and-differential.txt` |
| 2 | `cmp -s regenerated-solution.mpy solution.mpy` | exit 0, byte-identical | `stage2-fidelity-and-differential.txt` |
| 2 | `python3 /audit-output/evidence/differential_test.py` | exit 0; 98,672 cases, zero mismatch/contract failures | `stage2-fidelity-and-differential.txt` |
| 3 | `kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition semantic-kompiled` | exit 0; non-exhaustive `headInt` warning | `stage3-kompile-semantic-llvm.log` |
| 3 | `krun solution.mpy -cINPUT='<case>' --definition semantic-kompiled` | seven integer cases exit 0 and match Python | `stage3-concrete-krun.log` |
| 3/5 | `krun solution.mpy -cINPUT='pyList(ListItem("b") ListItem("odd") ListItem("a"))' --definition semantic-kompiled` | exit 113 at `headInt` | `stage3-noninteger-krun.log` |
| 3 | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 | `stage3-kompile-verification-haskell.log` |
| 3 | `kprove spec.k --definition verification-kompiled --spec-module SPEC -w none` | exit 0, `#Top` | `stage3-kprove-all.log` |
| 3 | `kprove ... --claims <leaf-label> -w none` | each example, `even`, `insert`, and `rebuild` leaf exits 0, `#Top` | `stage3-individual-kprove.log` |
| 3 | `kprove ... --claims insert-correct,sort-correct -w none` | exit 0, `#Top` | `stage3-dependency-closure-kprove.log` |
| 3 | `kprove ... --claims even-correct,insert-correct,sort-correct,rebuild-correct,top-correct -w none` | exit 0, `#Top` | `stage3-dependency-closure-kprove.log` |
| 4 | `kast solution.mpy --definition verification-kompiled --sort Program --output pretty` and `krun solutionProgram.term --term --definition verification-kompiled --output pretty`, then `cmp -s` | comparison exit 0; identical constructor presentation | `stage4-constructor-pinning.txt` |
| 4 | mutated embedded `sort_even` body; `kompile ... --output-definition verification-mutated-kompiled` | build exit 0 | `stage4-body-sensitivity.log` |
| 4 | `kprove spec.k --definition verification-mutated-kompiled --spec-module SPEC --claims prompt-example -w none` | exit 1 as expected | `stage4-body-sensitivity.log` |
| 4 | `python3 /audit-output/evidence/claim_witnesses.py` | exit 0; ten satisfying witnesses | `stage4-claim-witnesses.txt` |
| 6 | `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run` | exit 0 | `stage6-vacuity-final.log` |
| 6 | `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY` | exit 1, `WarnStuckClaimState`, failed implication | `stage6-vacuity-final.log` |

Two direct wrong-constructor mutation attempts built but ended in
`DecidePredicateUnknown`; they were rejected as non-vacuity evidence. Their
logs are retained as `stage6-vacuity.log` and `stage6-vacuity-valid.log`.
`stage6-vacuity-final.log` is the qualifying mutation.

The isolated diagnostic `--claims sort-correct` excludes its necessary
`insert-correct` theorem and fails; an isolated `top-correct` run was
interrupted after it kept unfolding without its helpers. These are retained in
`stage3-individual-kprove.log`. The dependency-closure and all-claims commands
above are the positive reconstructions.

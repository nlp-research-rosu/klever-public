# Reproducible audit commands

K toolchain observed: `K version v7.1.293`.

All candidate-source builds ran from `/tmp/audit-work/reconstruction` unless a
different working directory is shown. `script -q -e -c ... LOG` captured each
bounded log and its `COMMAND_EXIT_CODE`.

| Stage | Exact command | Exit | Log/result |
|---|---|---:|---|
| Provenance | `python3 /audit-output/evidence/provenance_check.py` | 0 | `01-provenance.log` |
| Regeneration | `python3 /tmp/audit-work/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy` | 0 | `02-program-fidelity.log` |
| Byte identity | `cmp /tmp/audit-work/reconstruction/solution.regenerated.mpy /tmp/audit-work/reconstruction/solution.mpy` | 0 | `02-program-fidelity.log` |
| Differential | `python3 /audit-output/evidence/differential_test.py` | 0 | `02-program-fidelity.log` |
| LLVM build | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | 0 | `03a-kompile-llvm.log` |
| Base proof build | `kompile verification.k --backend haskell --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition audit-verification-base-kompiled` | 0 | `03b-kompile-base.log` |
| Full proof build | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | 0 | `03c-kompile-full.log` |
| Loop proof | `kprove spec.k --definition audit-verification-base-kompiled --spec-module LOOP-SPEC --claims loop-correct --output pretty` | 0, `#Top` | `03d-kprove-loop.log` |
| Entry proof | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims intersection-correct --output pretty` | 0, `#Top` | `03e-kprove-intersection.log` |
| Reviewer concrete translation | `python3 /tmp/audit-work/py2mpy.py audit-concrete-tests.py > audit-concrete-tests.mpy` | 0 | `03f-krun-concrete.log` |
| Reviewer concrete run | `krun audit-concrete-tests.mpy --definition audit-runtime-kompiled --output pretty` | 0, `.K`/`NoExc` | `03f-krun-concrete.log` |
| Constructor normalization | `kast solution-body.mpy --definition audit-verification-base-kompiled --module MPY-SYNTAX --sort Stmts --input program --output pretty --color off --output-file solution-body.normalized.k` | 0 | generated input to `constructor-pinning.k` |
| Constructor pinning | `kprove constructor-pinning.k --definition audit-verification-base-kompiled --spec-module CONSTRUCTOR-PINNING-SPEC --claims constructor-pinning --output pretty` | 0, `#Top` | `04a-constructor-pinning.log` |
| Ground substitutions | `python3 /audit-output/evidence/ground_substitutions.py` | 0 | `04b-ground-substitutions.log` |
| Inventory | `python3 /audit-output/evidence/inventory_k.py > /audit-output/evidence/rule-inventory.tsv` | 0 | 1,120 source sentences plus summary |
| Assessment ledger | `python3 /audit-output/evidence/assess_inventory.py > /audit-output/evidence/rule-assessment.tsv` | 0 | one disposition per inventoried sentence |
| Body-mutant build (cwd `/tmp/audit-work/body-mutant`) | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutant-kompiled` | 0 | `05b-body-mutant-kompile.log` |
| Body-sensitivity proof (same cwd) | `kprove spec.k --definition body-mutant-kompiled --spec-module SPEC --claims intersection-correct --output pretty` | 1, expected stuck claim | `05c-body-mutant-kprove.log` |
| False-postcondition parse/build | `kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY --claims false-postcondition --dry-run --output pretty` | 0 | `06a-vacuity-dry-run.log` |
| False-postcondition proof | `kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY --claims false-postcondition --output pretty` | 1, expected stuck claim | `06b-vacuity-kprove.log` |

The body mutation is exactly the one-line diff in
`05a-body-mutation.diff`: `Int(1)` becomes `Int(2)` in the condition of
`intersectionBody`. The false postcondition is preserved as `spec-vacuity.k`.

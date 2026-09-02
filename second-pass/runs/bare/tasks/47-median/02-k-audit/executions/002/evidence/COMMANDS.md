# Reviewer command ledger

Unless stated otherwise, K commands ran in
`/tmp/audit-work/candidate-src`. Output logs include the reported exit status.

| Purpose | Exact material command | Exit | Log |
|---|---|---:|---|
| Mounted integrity | `python3 /audit-output/evidence/stage1_integrity.py` | 0 on corrected rerun | `stage1_integrity-rerun.log` |
| Trace inspection | `python3 /audit-output/evidence/trace_summary.py` | 0 | `generation_trace_summary.log` |
| Trusted regeneration | `python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy`; `cmp -s regenerated-solution.mpy solution.mpy` | 0 | `translation_identity.log` |
| Python differential | `python3 /audit-output/evidence/differential.py` | 1 (81 intended mismatches) | `differential.log` |
| Concrete definition | `kompile --backend llvm semantic.k --main-module MEDIAN-SEMANTICS --syntax-module MEDIAN-SYNTAX --output-definition concrete-kompiled` | 0 | `build-concrete.log` |
| Proof definition | `kompile --backend haskell semantic.k --main-module SEMANTIC --syntax-module MEDIAN-SYNTAX --output-definition proof-kompiled` | 0 | `build-proof.log` |
| All submitted claims | `kprove spec.k --definition proof-kompiled --spec-module SPEC` | 0, `#Top` | `kprove-all-positive.log` |
| Main claim alone | `kprove spec-labeled.k --definition proof-kompiled --spec-module SPEC-LABELED --claims SPEC-LABELED.main` | 0, `#Top` | `kprove-main-rerun.log` |
| Odd example alone | `kprove spec-labeled.k --definition proof-kompiled --spec-module SPEC-LABELED --claims SPEC-LABELED.example-odd` | 0, `#Top` | `kprove-example-odd.log` |
| Even example alone | `kprove spec-labeled.k --definition proof-kompiled --spec-module SPEC-LABELED --claims SPEC-LABELED.example-even` | 0, `#Top` | `kprove-example-even.log` |
| Concrete semantics | `bash /audit-output/evidence/run_concrete_checks.sh` | 0 overall; length 0/2 `krun` cases each 113 | `concrete_checks.log` |
| Body sensitivity | `kprove spec-body-mutation.k --definition proof-kompiled --spec-module SPEC-BODY-MUTATION --claims SPEC-BODY-MUTATION.main` | 1, expected stuck equality | `body-mutation-kprove.log` |
| OOB false-normal-return witness | `kprove spec-oob-totality-witness.k --definition proof-kompiled --spec-module SPEC-OOB-TOTALITY-WITNESS` | 0, `#Top` | `oob-totality-witness-kprove.log` |
| False-post parse/build | `kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.main --dry-run` | 0 | `vacuity-dry-run.log` |
| False-post proof | `kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.main` | 1, expected `WarnStuckClaimState` | `vacuity-kprove.log` |

The initial integrity script run exited 1 because the reviewer used the
nonexistent `Path.lexists` method; the corrected script uses
`os.path.lexists`. The initial filtered-main replay exited 113 because a
label-attribute spelling was unused by this K version; the declaration-label
rerun above is the material per-claim result. Both failed reviewer attempts are
retained as `stage1_integrity.log` and `kprove-main.log`.

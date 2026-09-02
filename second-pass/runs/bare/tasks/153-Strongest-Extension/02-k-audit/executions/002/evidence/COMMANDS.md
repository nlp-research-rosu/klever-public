# Audit command index

All candidate source inputs were copied to
`/tmp/audit-work/153-strongest-extension` before these commands. No
candidate-provided compiled definition or cache was copied.

## Integrity and fidelity

```bash
bash /audit-output/evidence/stage1/run-stage1.sh
# exit 0; full output: stage1/integrity.log

bash /audit-output/evidence/stage2/run-stage2.sh
# exit 1 because the independent differential found mismatches;
# translator regeneration and cmp both exited 0.
# full output: stage2/stage2.log
```

## Fresh definitions and positive proofs

```bash
kompile --backend llvm semantic.k \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled
# exit 0; stage3/kompile-llvm.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
# exit 0; stage3/kompile-haskell.log

kprove spec.k --definition verification-kompiled --spec-module SPEC
# output #Top; exit 0; stage3/kprove-all.log

bash /audit-output/evidence/stage3/run-individual-claims.sh
# all seven selected claims output #Top and exit 0;
# stage3/kprove-<label>.log

bash /audit-output/evidence/stage3/run-concrete.sh
# exit 0; stage3/concrete-execution.log
```

The individual-claim run uses `stage3/spec-labeled.k`, a mechanically identical
copy of `spec.k` with labels only. Each executed command is echoed in its log.

## Pinning and body sensitivity

```bash
bash /audit-output/evidence/stage4/run-pinning.sh
# exit 0; KORE cmp exit 0; stage4/pinning-and-witnesses.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
# run in body-mutation scratch; exit 0; stage4/body-mutation-kompile.log

kprove spec.k --definition verification-kompiled --spec-module SPEC
# run in body-mutation scratch; exit 1 with returned
# Slices.SErviNGSliCes changed to Slices:SErviNGSliCes;
# stage4/body-mutation-kprove.log
```

## Static witnesses and non-vacuity

```bash
bash /audit-output/evidence/stage5/run-static-index.sh
# exit 0; stage5/static-index.log

bash /audit-output/evidence/stage5/run-unicode-lower-witness.sh
# exit 0; demonstrates K/Python result divergence;
# stage5/unicode-lower-witness.log

bash /audit-output/evidence/stage6/run-nonvacuity.sh
# dry-run exit 0; false-result proof exit 1 as expected;
# wrapper exit 0; stage6/nonvacuity.log
```

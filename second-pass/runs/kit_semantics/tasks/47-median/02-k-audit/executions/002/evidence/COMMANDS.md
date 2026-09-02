# Independent audit command index

All commands below were run with working directory
`/tmp/audit-work/median47` unless an absolute path says otherwise. Candidate
compiled definitions and caches were not copied into this directory.

## Stage 1

```sh
python3 /audit-output/evidence/stage1_integrity.py
```

Exit `0`; authoritative log: `stage1-integrity-rerun.log`.

The first execution, preserved as `stage1-integrity.log`, exited `1` because
the reviewer script used nonexistent `Path.lexists`. The script was corrected
to use `os.path.lexists` and rerun. That reviewer-side error is unrelated to
the candidate.

## Stage 2

```sh
bash stage2_translate.sh
python3 /audit-output/evidence/stage2_differential.py
```

Both exited `0`; logs: `stage2-translation.log` and
`stage2-differential.log`.

## Stage 3

```sh
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Exit `0`; log: `stage3-kompile.log`.

A separate clean concrete definition was also built and run:

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-stage3-kompiled
krun audit-smoke.mpy \
  --definition audit-runtime-stage3-kompiled --output none
```

Both commands exited `0`; logs: `stage3-concrete-kompile.log` and
`stage3-concrete-smoke.log`.

Each positive claim was run independently:

```sh
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-odd
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-even-int-int
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-even-int-bool
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-even-bool-int
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-even-bool-bool
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-even-float-float
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-even-int-float
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-even-float-int
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-even-bool-float
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.median-even-float-bool
```

Every command exited `0` and printed `#Top`. The ten corresponding logs are
named `stage3-proof-<claim>.log`.

## Stage 4

```sh
python3 /audit-output/evidence/stage4_pinning.py
```

Exit `0`; authoritative log: `stage4-pinning-rerun.log`.

The first execution, preserved as `stage4-pinning.log`, exited `1` because the
reviewer script expected an unquoted translator argument. The comparison was
corrected to the translator's actual quoted constructor and rerun. This was a
reviewer-side error.

```sh
kompile --backend haskell audit-verification-mutated.k \
  --main-module AUDIT-VERIFICATION-MUTATED \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-mutated-kompiled
kprove audit-body-sensitivity-spec.k \
  --definition audit-mutated-kompiled \
  --spec-module AUDIT-BODY-SENSITIVITY-SPEC --dry-run
kprove audit-body-sensitivity-spec.k \
  --definition audit-mutated-kompiled \
  --spec-module AUDIT-BODY-SENSITIVITY-SPEC
```

The build and dry run exited `0`. The real proof exited `1` with
`WarnStuckClaimState` and residual `<k> 0 ~> .K </k>`, as expected after
changing the executed odd return to `0`. Logs:
`stage4-body-mutant-kompile.log`, `stage4-body-mutant-dry-run.log`, and
`stage4-body-mutant-proof.log`.

## Stage 5

```sh
python3 /audit-output/evidence/stage5_inventory.py
python3 /audit-output/evidence/stage5_dispositions.py
```

Both exited `0`; authoritative inventory and per-item decision ledger:
`stage5-rule-inventory-rerun.log` and `stage5-rule-dispositions.log`.
`stage5-rule-inventory.log` is a superseded first inventory whose statement
boundary parser omitted some trailing attributes; the corrected inventory
retains every complete statement and attribute.

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
python3 py2mpy.py audit-smoke.py > audit-smoke.mpy
krun audit-smoke.mpy --definition audit-runtime-kompiled --output none
bash stage5_unicode_gap.sh
```

The LLVM build, translation, and smoke execution exited `0`. The Unicode
wrapper exited `0` after recording the intended divergence: CPython returned
`'b'`, while its inner fresh-model `krun` exited `113` stuck at
`strToCodes("\xc3\xa9")`. Logs: `stage5-llvm-kompile.log`,
`stage5-smoke-translate.log`, `stage5-smoke-krun.log`, and
`stage5-unicode-gap.log`.

## Stage 6

```sh
kprove audit-false-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-SPEC --dry-run
kprove audit-false-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-SPEC
```

The dry run exited `0`. The real proof exited `1` with
`WarnStuckClaimState`; execution reached residual `<k> 5 ~> .K </k>` while
the mutated postcondition required `6`. Logs: `stage6-false-dry-run.log` and
`stage6-false-proof.log`.

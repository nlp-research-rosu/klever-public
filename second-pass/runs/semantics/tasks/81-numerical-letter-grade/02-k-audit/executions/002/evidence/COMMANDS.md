# Audit command index

All commands ran from `/tmp/audit-work/candidate` unless noted.

## Integrity and source fidelity

- `python3 /audit-output/evidence/stage1_integrity.py` — exit 0; log `stage1_integrity.log`.
- `python3 /audit-output/evidence/stage1_generation_summary.py` — exit 0; log `stage1_generation_summary.log`.
- `python3 py2mpy.py solution.py > solution.regenerated.mpy`; `cmp -s solution.regenerated.mpy solution.mpy` — both exit 0; log `stage2_translation.log`.
- `python3 /audit-output/evidence/differential_test.py` — exit 0; log `stage2_differential.log`.

## Clean reconstruction

- `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` — exit 0.
- `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` — exit 0.
- `krun smoke.mpy --definition runtime-kompiled --output pretty` — exit 0, final `NoExc`, K exit-code cell 0.
- `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.empty` — `#Top`, exit 0.
- `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.a-plus` — `#Top`, exit 0.
- `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.a` — `#Top`, exit 0.
- `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.loop-maps-all-numeric-grades` — `#Top`, exit 0.
- `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.function-maps-all-numeric-grades,SPEC.loop-maps-all-numeric-grades` — `#Top`, exit 0.
- `kprove spec.k --definition verification-kompiled --spec-module SPEC` — `#Top`, exit 0.

The diagnostic that selected only `SPEC.function-maps-all-numeric-grades`
excluded the required loop circularity and was reviewer-interrupted with status
130 after 6m20s. It was not a submitted positive command; the claim closes in
its dependency set and in the submitted all-claims command.

## Pinning and static audit

- `python3 /audit-output/evidence/pinning_compare.py` — exit 0; expanded macro body equals trusted-translated body.
- `python3 /audit-output/evidence/static_inventory.py --json > /audit-output/evidence/static_inventory.json` — exit 0.
- `python3 /audit-output/evidence/static_inventory.py` — exit 0; 973 outer sentences inventoried.

## Oracle and body-sensitivity witnesses

- `kompile oracle-witness.k --backend llvm --main-module ORACLE-WITNESS --syntax-module MPY-SYNTAX --output-definition oracle-witness-kompiled` — exit 0.
- `krun oracle-real.mpy --definition runtime-kompiled --output pretty` — process/K exit 0, `NoExc`.
- `krun oracle-false.mpy --definition runtime-kompiled --output pretty` — process/K exit 1, `AssertionError`.
- `krun oracle-real.mpy --definition oracle-witness-kompiled --output pretty` — process/K exit 1, `AssertionError`.
- `krun oracle-false.mpy --definition oracle-witness-kompiled --output pretty` — process/K exit 0, `NoExc`.
- `kompile verification-body-mutant.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-body-mutant-kompiled` — exit 0.
- `kprove spec-body-mutant.k --definition verification-body-mutant-kompiled --spec-module SPEC-BODY-MUTANT --claims SPEC-BODY-MUTANT.a-plus` — expected `WarnStuckClaimState`, exit 1.

## Fresh non-vacuity mutation

- `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run` — exit 0.
- `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY` — expected `WarnStuckClaimState`, exit 1.

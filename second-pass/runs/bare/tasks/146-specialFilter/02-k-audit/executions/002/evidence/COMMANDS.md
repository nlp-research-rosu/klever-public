# Reviewer command record

All commands were run against copied sources in
`/tmp/audit-work/candidate-src`; candidate-provided compiled definitions and
caches were not copied or used. Logs named below are bounded `script(1)`
captures whose trailers record `COMMAND_EXIT_CODE`.

## Toolchain and integrity

```sh
kompile --version && kprove --version && krun --version && python3 --version
# exit 0; 00-toolchain.log

python3 /audit-output/evidence/integrity_audit.py
# exit 0; 01-integrity.log
```

## Translation and differential checks

```sh
python3 py2mpy.py solution.py > solution.regenerated.mpy &&
  cmp -s solution.regenerated.mpy solution.mpy &&
  sha256sum solution.regenerated.mpy solution.mpy
# exit 0; 02-regeneration.log

python3 /audit-output/evidence/differential_test.py
# exit 0; 02-differential.log (4,108 checks, zero mismatches)

python3 /audit-output/evidence/constructor_compare.py
# exit 0; 04-constructor-compare-fixed.log
```

The first constructor-comparison attempt exited 1
(`04-constructor-compare.log`) because it compared the translator's omitted
empty-list spelling textually against `.Stmts`. The corrected mechanical
comparison normalizes exactly that K list-unit spelling and nothing else.

## Fresh builds and concrete execution

```sh
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-audit-kompiled
# exit 0; 03-kompile-semantic.log

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-audit-kompiled
# exit 0; 03-kompile-verification.log

krun solution.mpy --definition semantic-audit-kompiled
# exit 0; 03-krun-submitted-module.log

krun run-normal.mpy --definition semantic-audit-kompiled
# exit 0; 03-krun-normal.log; intVal(1)

krun run-empty.mpy --definition semantic-audit-kompiled
# exit 0; 03-krun-empty.log; intVal(0)

krun run-boundaries.mpy --definition semantic-audit-kompiled
# exit 0; 03-krun-boundaries.log; intVal(4)

krun run-huge.mpy --definition semantic-audit-kompiled
# exit 0; 03-krun-huge.log; intVal(1)

krun example1.mpy --definition verification-audit-kompiled
# exit 0; 04-krun-sftest-example1.log; intVal(1)

krun example2.mpy --definition verification-audit-kompiled
# exit 0; 04-krun-sftest-example2.log; intVal(2)
```

The four matching Python oracle pairs `(canonical, submitted)` were
`(1,1), (0,0), (4,4), (1,1)` in
`03-python-concrete-oracle.log`.

## Positive proofs

```sh
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
# exit 0, #Top; 03-kprove-all.log
```

The submitted claims were mechanically copied and given labels `c01` through
`c11` in `spec-labelled.k`. Each exact command below exited 0 and printed
`#Top`:

```sh
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c01
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c02
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c03
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c04
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c05
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c06
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c07
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c08
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c09
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c10
kprove spec-labelled.k --definition verification-audit-kompiled \
  --spec-module SPEC-LABELLED --claims SPEC-LABELLED.c11
```

The corresponding logs are `03-kprove-c01-fixed.log` and
`03-kprove-c02.log` through `03-kprove-c11.log`. The preliminary use of
`[label(c01)]` was rejected as an unused filter with exit 113
(`03-kprove-c01.log`); this was reviewer labeling instrumentation, not a
candidate proof failure.

## Adequacy and body sensitivity

```sh
python3 /audit-output/evidence/precondition_witnesses.py
# exit 0; 04-precondition-witnesses.log

python3 /audit-output/evidence/coverage_gap_witnesses.py
# exit 0; 04-coverage-gap.log

kompile verification-body-mutant.k --backend haskell \
  --main-module VERIFICATION-BODY-MUTANT \
  --syntax-module VERIFICATION-BODY-MUTANT \
  --output-definition verification-body-mutant-kompiled
# exit 0; 04-kompile-body-mutation.log

kprove spec-body-mutant.k \
  --definition verification-body-mutant-kompiled \
  --spec-module SPEC-BODY-MUTANT
# exit 1 as expected; 04-kprove-body-mutation.log
# residual result intVal(0), destination intVal(1)
```

## Static probes

```sh
rg -n "^[[:space:]]*(syntax|configuration|rule|claim)|\
\[(function|total|functional|simplification|concrete|owise|priority)" \
  semantic.k verification.k spec.k
# exit 0; 05-rule-inventory.log

krun run-negative-division.mpy --definition semantic-audit-kompiled
# exit 0; 05-negative-division.log; K result intVal(-1)

krun run-negative-modulo.mpy --definition semantic-audit-kompiled
# exit 0; 05-negative-modulo.log; K result intVal(-1)

python3 -c 'print("python_-3_floor_div_2=", -3 // 2); print("python_-3_mod_2=", -3 % 2)'
# exit 0; 05-python-negative-arithmetic.log; Python result -2 and 1

krun run-unsupported-bin.mpy --definition semantic-audit-kompiled
# exit 0; 05-totality-gap.log; residual #bin("*", intVal(1), intVal(2))
```

## Fresh false-result mutation

```sh
kprove spec-vacuity.k --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY --dry-run
# exit 0; 06-vacuity-dry-run.log

kprove spec-vacuity.k --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY
# exit 1 as expected; 06-vacuity-kprove.log
# WarnStuckClaimState with reachable intVal(1), mutated destination intVal(0)
```

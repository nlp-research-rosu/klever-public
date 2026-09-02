# Audit command record

All paths below are container paths. `script -q -e -c 'COMMAND' LOG` was used
to preserve terminal output and the command exit status; the listed command is
the inner command that was executed. Logs named below contain the actual output.

## Stage 1

Working directory: `/audit-output`

```sh
python3 /audit-output/evidence/integrity_check.py
python3 /audit-output/evidence/trace_summary.py
find /candidate -maxdepth 1 -type f -print0 | sort -z | xargs -0 sha256sum
```

All exited 0. Logs: `stage1-integrity.log`,
`stage1-trace-summary.log`, and `stage1-candidate-files-sha256.log`.

## Stage 2

Working directory: `/audit-output`

```sh
python3 /tmp/audit-work/160-do-algebra/reference/py2mpy.py /tmp/audit-work/160-do-algebra/candidate/solution.py > /tmp/audit-work/160-do-algebra/regenerated-solution.mpy
cmp /tmp/audit-work/160-do-algebra/regenerated-solution.mpy /tmp/audit-work/160-do-algebra/candidate/solution.mpy
sha256sum /tmp/audit-work/160-do-algebra/regenerated-solution.mpy /tmp/audit-work/160-do-algebra/candidate/solution.mpy
python3 /audit-output/evidence/differential_test.py
```

All exited 0. Logs: `stage2-translation.log` and
`stage2-differential.log`.

## Stage 3

Build working directory:
`/tmp/audit-work/160-do-algebra/candidate`

```sh
kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/160-do-algebra/concrete-kompiled
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/160-do-algebra/proof-kompiled
kprove spec.k --definition /tmp/audit-work/160-do-algebra/proof-kompiled --spec-module SPEC
bash /audit-output/evidence/run_positive_claims.sh
bash /audit-output/evidence/run_semantics_cases.sh
```

All exited 0. The aggregate proof printed `#Top`; the per-claim runner printed
`#Top` and exit 0 for each of the six claims. Logs:
`stage3-kompile-concrete.log`, `stage3-kompile-proof.log`,
`stage3-kprove-all.log`, `stage3-kprove-individual.log`, and
`stage3-concrete-execution.log`.

## Stage 4

```sh
python3 /audit-output/evidence/program_term_compare.py
kprove audit-witness-spec.k --definition /tmp/audit-work/160-do-algebra/proof-kompiled --spec-module AUDIT-WITNESS-SPEC
kprove audit-body-mutation-spec.k --definition /tmp/audit-work/160-do-algebra/proof-kompiled --spec-module AUDIT-BODY-MUTATION-SPEC --dry-run
kprove audit-body-mutation-spec.k --definition /tmp/audit-work/160-do-algebra/proof-kompiled --spec-module AUDIT-BODY-MUTATION-SPEC
```

The comparison and witness exited 0; the witness printed `#Top`. The body
mutation dry-run exited 0. Its proof exited 1 with `WarnStuckClaimState`, as
expected. Logs: `stage4-program-term.log`,
`stage4-satisfying-witness.log`, `stage4-body-mutation-dry-run.log`, and
`stage4-body-mutation-proof.log`.

## Stage 5

```sh
rg -n '^[[:space:]]*(module|imports|syntax|configuration|rule|claim)' semantic.k verification.k spec.k
kprove audit-divzero-summary-spec.k --definition /tmp/audit-work/160-do-algebra/proof-kompiled --spec-module AUDIT-DIVZERO-SUMMARY-SPEC
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/160-do-algebra/oracle-mutation-kompiled
kprove audit-labeled-spec.k --definition /tmp/audit-work/160-do-algebra/oracle-mutation-kompiled --spec-module AUDIT-LABELED-SPEC --claims AUDIT-LABELED-SPEC.entry
krun solution.mpy --definition /tmp/audit-work/160-do-algebra/oracle-mutation-kompiled -cOPS='ops(Op("+", Op("*", Op("-", .Ops))))' -cOPERANDS='ints(Num(2, Num(3, Num(4, Num(5, .Ints)))))'
bash /audit-output/evidence/large_integer_witness.sh
```

The division-by-zero summary claim printed `#Top`. The deliberately wrong
`pyEval := 0` definition built, and the unchanged entry claim still printed
`#Top`; its concrete prompt execution returned 0 while trusted Python returned
9. The large-integer witness exited 0 as a diagnostic: K returned the 4301
digit operand plus zero, while both trusted and candidate Python raised
`ValueError`. Logs: `stage5-rule-inventory.log`,
`stage5-divzero-summary-proof.log`, `stage5-oracle-mutation-build.log`,
`stage5-oracle-mutation-proof.log`, `stage5-oracle-mutation-witness.log`, and
`stage5-large-integer-witness.log`.

## Stage 6

```sh
kprove audit-vacuity.k --definition /tmp/audit-work/160-do-algebra/proof-kompiled --spec-module AUDIT-VACUITY --dry-run
kprove audit-vacuity.k --definition /tmp/audit-work/160-do-algebra/proof-kompiled --spec-module AUDIT-VACUITY
```

The dry-run exited 0. The proof exited 1 with `WarnStuckClaimState` at
`answer(-1)` versus the false target `answer(0)`, as expected. Logs:
`stage6-vacuity-dry-run.log` and `stage6-vacuity-proof.log`.

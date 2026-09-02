# Auditor command index

All commands below ran from `/tmp/audit-work/scratch/proof` unless another
directory is shown. The corresponding `script(1)` transcript records its
command line, output, and terminating exit status.

## Stage 1

- `python3 /audit-output/evidence/stage1/check_integrity.py` — exit 0;
  `stage1/integrity.log`.
- `sed -n "1,220p" ...` over the pipeline-v3 records — exit 0;
  `stage1/records.log`.
- `sed -n "1,180p" /generation-evidence/prompt.txt` — exit 0;
  `stage1/generation-prompt.log`.
- `python3 /audit-output/evidence/stage1/inspect_trace.py` — exit 0 after
  parsing/indexing all 615 JSONL events; `stage1/trace-index.log`.
- `python3 /audit-output/evidence/stage1/inspect_generation_output.py` — exit
  0 after reading/indexing all 53,479 lines; `stage1/generation-output-index.log`.

## Stage 2

- `python3 py2mpy.py solution.py > solution.regenerated.mpy` — exit 0.
- `cmp -s solution.mpy solution.regenerated.mpy` — exit 0;
  `stage2/mpy-byte-identity.log`.
- `sha256sum solution.mpy solution.regenerated.mpy solution.py py2mpy.py canonical.py`
  — exit 0; `stage2/source-hashes.log`.
- `python3 /audit-output/evidence/stage2/differential_intended.py` — exit 0,
  34,349 cases, zero mismatches; `stage2/differential-intended.log`.
- `python3 /audit-output/evidence/stage2/differential.py` — exit 1, preserving
  the broader Int/Bool/Float/Decimal/Fraction exploration and 1,384
  canonical-versus-candidate mismatches; `stage2/differential.log`.

## Stage 3

- `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-rebuilt`
  — exit 0; `stage3/kompile-runtime.log`.
- `krun concrete-reconstruction.mpy --definition runtime-rebuilt` — exit 0
  with `.K`, `NoExc`, and exit code 0; `stage3/krun-concrete.log`.
- `kompile verification.k --backend haskell --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition verification-base-rebuilt`
  — exit 0; `stage3/kompile-verification-base.log`.
- `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-rebuilt`
  — exit 0; `stage3/kompile-verification.log`.
- `kprove connection-spec.k --definition verification-base-rebuilt --spec-module CONNECTION-SPEC`
  — exit 0 and `#Top`; `stage3/kprove-connection-all.log`.
- Individual `kprove ... --claims CONNECTION-SPEC.<label>` runs for all six
  connection claims and `--claims SPEC.count-loop` — each exit 0 and `#Top`;
  `stage3/kprove-positive-claims.log`. The subsequent diagnostic
  `--claims SPEC.exchange` was interrupted with exit 130 after 23 minutes
  because filtering removed its required loop circularity.
- `kprove spec.k --definition verification-rebuilt --spec-module SPEC` — exit
  0 and `#Top`, proving both `SPEC.count-loop` and the dependent
  `SPEC.exchange`; `stage3/kprove-spec-all.log`.

## Stage 4

- `kast solution.mpy --definition verification-rebuilt --module VERIFICATION --sort Module --expand-macros --output json --output-file solution.expanded.json`
  — exit 0.
- `kast /audit-output/evidence/stage4/exchange-program.term --definition verification-rebuilt --module VERIFICATION --sort Module --expand-macros --output json --output-file claim-program.expanded.json`
  — exit 0.
- `cmp -s solution.expanded.json claim-program.expanded.json` — exit 0;
  `stage4/program-term-identity.log`.
- `kprove ground-spec.k --definition verification-rebuilt --spec-module GROUND-SPEC`
  — exit 0 and `#Top`; `stage4/kprove-ground.log`.
- `python3 /audit-output/evidence/stage4/ground-python.py` — exit 0 and both
  implementations return `YES`; `stage4/ground-python.log`.
- `kprove body-mutation-spec.k --definition verification-rebuilt --spec-module BODY-MUTATION-SPEC`
  — expected exit 1 with a reached `NO` term against required `YES`;
  `stage4/kprove-body-mutation.log`.

## Stage 5

- `python3 /audit-output/evidence/stage5/build_rule_inventory.py` — exit 0,
  1,162 declarations inventoried; `stage5/rule-inventory-build.log`.
- `python3 /audit-output/evidence/stage5/classify_rule_inventory.py` — exit 0,
  every inventory row classified; `stage5/rule-review-build.log`.
- `kompile verification.k --backend llvm --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-runtime-rebuilt`
  — exit 0; `stage5/kompile-verification-runtime.log`.
- `python3 /audit-output/evidence/stage5/numeric_bridge_tests.py` — exit 0;
  `stage5/python-numeric-bridge.log`.
- `krun numeric-bridge-tests.mpy --definition verification-runtime-rebuilt`
  — exit 0 with `.K`, `NoExc`, and exit code 0;
  `stage5/krun-numeric-bridge.log`.
- `kprove opposite-even-spec.k --definition verification-base-rebuilt --spec-module OPPOSITE-EVEN-SPEC`
  — expected exit 1, residual `true` versus `false`;
  `stage5/kprove-opposite-even.log`.
- `kprove opposite-odd-spec.k --definition verification-base-rebuilt --spec-module OPPOSITE-ODD-SPEC`
  — expected exit 1, residual `false` versus `true`;
  `stage5/kprove-opposite-odd.log`.

## Stage 6

- `python3 /audit-output/evidence/stage6/reviewer-vacuity-witness.py` — exit 0;
  `stage6/witness.log`.
- `kprove reviewer-vacuity.k --definition verification-rebuilt --spec-module REVIEWER-VACUITY --dry-run`
  — exit 0, establishing successful parsing/build; `stage6/kprove-vacuity-dry-run.log`.
- `kprove reviewer-vacuity.k --definition verification-rebuilt --spec-module REVIEWER-VACUITY`
  — expected exit 1 with `WarnStuckClaimState` at reached `YES` versus
  required `NO`; `stage6/kprove-vacuity.log`.

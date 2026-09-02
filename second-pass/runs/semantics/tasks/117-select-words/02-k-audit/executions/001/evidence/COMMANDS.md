# Reviewer command record

All commands were run from the scratch copy or read-only mounts as stated.
Dynamic command transcripts are in the adjacent `.log` files.

## Stage 1

```bash
python3 /audit-output/evidence/stage1_integrity.py
python3 /audit-output/evidence/stage1_generation_records.py
```

The commands' exit statuses and complete output are recorded in
`stage1-integrity.log` and `stage1-generation-records.log`.

## Stage 2

```bash
bash /audit-output/evidence/stage2_fidelity.sh
```

This regenerates `solution.regenerated.mpy` in the scratch workspace using the
trusted translator, checks byte identity with the submitted translation, and
runs the independent differential suite. The exit status and complete output
are in `stage2-fidelity.log`.

## Stage 3

```bash
cd /tmp/audit-work/proof
python3 py2mpy.py /audit-output/evidence/stage3_concrete.py \
  > stage3_concrete.mpy
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
krun stage3_concrete.mpy --definition runtime-audit-kompiled
kompile verification.k --backend haskell \
  --main-module SELECT-WORDS-VERIFICATION \
  --syntax-module SELECT-WORDS-VERIFICATION \
  --output-definition verification-audit-kompiled
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SELECT-WORDS-SPEC \
  --claims SELECT-WORDS-SPEC.select-loop
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SELECT-WORDS-SPEC \
  --claims SELECT-WORDS-SPEC.select-loop-entry
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SELECT-WORDS-SPEC \
  --claims SELECT-WORDS-SPEC.select-words-correct
```

Each command has its own `stage3-*.log` transcript containing the exit status
and complete bounded output.

The isolated `select-loop-entry` filter was interrupted after 20 minutes of
active CPU use; its empty transcript and reviewer-recorded exit 130 are
accounted for in `stage3-kprove-select-loop-entry.status`. The required unfiltered
positive command was then run as:

```bash
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SELECT-WORDS-SPEC
```

It returned `#Top` and exit 0; see `stage3-kprove-all.log`.

## Stage 4

```bash
cd /tmp/audit-work/proof
kast --definition verification-audit-kompiled \
  --module SELECT-WORDS-VERIFICATION --sort Module --expand-macros \
  --output json --output-file solution-module.json solution.mpy
kast --definition verification-audit-kompiled \
  --module SELECT-WORDS-VERIFICATION --sort Module --expand-macros \
  --output json --output-file claim-module.json \
  --expression selectWordsModule
cmp -s solution-module.json claim-module.json
python3 /audit-output/evidence/stage4_witness.py
```

Constructor-level identity is recorded in `stage4-constructor-pinning.log`;
the concrete adequacy witness is in `stage4-witness.log`.

For body sensitivity, the reviewer changed the macro-expanded executed return
statement from `Return(Name("result"))` to `Return(Name("n"))`, rebuilt a
separate definition, and ran:

```bash
cd /tmp/audit-work/body-mutation
kompile verification.k --backend haskell \
  --main-module SELECT-WORDS-VERIFICATION \
  --syntax-module SELECT-WORDS-VERIFICATION \
  --output-definition verification-body-mutated-kompiled
kprove spec.k --definition verification-body-mutated-kompiled \
  --spec-module SELECT-WORDS-SPEC
```

The exact mutation is `stage4_body_mutation.diff`; build/proof transcripts are
`stage4-body-kompile.log` and `stage4-body-kprove.log`.

## Stage 5

```bash
python3 /audit-output/evidence/stage5_rule_inventory.py
```

The complete inventory of configuration, syntax, contexts, rules, attributes,
and claims from all 24 supplied-semantics source files plus candidate
`verification.k` and `spec.k` is in `stage5-rule-inventory.log`.
The corresponding candidate-local rule-by-rule judgments and fixed-semantics
construct map are in `stage5_candidate_assessment.md`.

## Stage 6

```bash
cd /tmp/audit-work/proof
kprove spec-vacuity.k --definition verification-audit-kompiled \
  --spec-module SELECT-WORDS-SPEC-VACUITY --dry-run
kprove spec-vacuity.k --definition verification-audit-kompiled \
  --spec-module SELECT-WORDS-SPEC-VACUITY
```

The exact false result mutation is `stage6_false_mutation.diff`. The dry-run
build transcript is `stage6-vacuity-dry-run.log`; the expected proof failure
and residual are in `stage6-vacuity-kprove.log`.

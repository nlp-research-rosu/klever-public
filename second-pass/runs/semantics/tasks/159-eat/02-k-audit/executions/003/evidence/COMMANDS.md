# Reproduction commands

All commands ran in the audit container with K 7.1.293 and Python 3.10.12.
Positive exit statuses and bounded output are in the adjacent `.log` files.

## Provenance and source fidelity

```bash
python3 /audit-output/evidence/check_provenance.py

python3 /tmp/audit-work/159-eat/trusted/py2mpy.py \
  /tmp/audit-work/159-eat/candidate-source/solution.py \
  > /tmp/audit-work/159-eat/fresh/regenerated-solution.mpy
cmp -s /tmp/audit-work/159-eat/fresh/regenerated-solution.mpy \
  /tmp/audit-work/159-eat/candidate-source/solution.mpy

python3 /audit-output/evidence/differential_test.py \
  /tmp/audit-work/159-eat/trusted/canonical.py \
  /tmp/audit-work/159-eat/candidate-source/solution.py
```

Results: provenance exit 0; translator exit 0 and `cmp` exit 0; differential
exit 0 with 4,108,019 comparisons and zero mismatches.

## Fresh concrete definition and execution

```bash
kompile \
  /tmp/audit-work/159-eat/candidate-source/reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/159-eat/fresh/runtime-kompiled

python3 /audit-output/evidence/make_concrete_harness.py \
  /tmp/audit-work/159-eat/candidate-source/solution.mpy \
  /tmp/audit-work/159-eat/fresh/solution-concrete-harness.mpy

krun /tmp/audit-work/159-eat/fresh/solution-concrete-harness.mpy \
  --definition /tmp/audit-work/159-eat/fresh/runtime-kompiled
```

Results: all exit 0. The final configuration has `.K`, `NoExc`, exit code 0,
and all eleven asserted results allocated in the heap.

## Fresh proof definition and every positive claim

```bash
kompile /tmp/audit-work/159-eat/candidate-source/verification.k \
  --backend haskell --main-module EAT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/159-eat/fresh/verification-kompiled

python3 /audit-output/evidence/split_positive_claims.py \
  /tmp/audit-work/159-eat/candidate-source/spec.k \
  /tmp/audit-work/159-eat/candidate-source

kprove /tmp/audit-work/159-eat/candidate-source/spec-branch-1.k \
  --definition /tmp/audit-work/159-eat/fresh/verification-kompiled \
  --spec-module EAT-SPEC-BRANCH-1

kprove /tmp/audit-work/159-eat/candidate-source/spec-branch-2.k \
  --definition /tmp/audit-work/159-eat/fresh/verification-kompiled \
  --spec-module EAT-SPEC-BRANCH-2

kprove /tmp/audit-work/159-eat/candidate-source/spec.k \
  --definition /tmp/audit-work/159-eat/fresh/verification-kompiled \
  --spec-module EAT-SPEC
```

Results: build exit 0. Each branch and the combined original spec print
`#Top` and exit 0.

## Constructor pinning and satisfying witnesses

```bash
python3 /audit-output/evidence/constructor_pinning.py \
  /tmp/audit-work/159-eat/trusted/py2mpy.py \
  /tmp/audit-work/159-eat/candidate-source/solution.py \
  /tmp/audit-work/159-eat/candidate-source/verification.k \
  /tmp/audit-work/159-eat/candidate-source

kprove /tmp/audit-work/159-eat/candidate-source/pinning-spec.k \
  --definition /tmp/audit-work/159-eat/fresh/verification-kompiled \
  --spec-module EAT-PINNING-SPEC

python3 /audit-output/evidence/claim_witnesses.py \
  /tmp/audit-work/159-eat/trusted/canonical.py \
  /tmp/audit-work/159-eat/candidate-source/solution.py
```

Results: normalized constructor terms compare equal; the pinning claim prints
`#Top` and exits 0; both branch witnesses agree in canonical Python, candidate
Python, and the claimed K heap value.

## Static inventory

```bash
python3 /audit-output/evidence/inventory_k_rules.py \
  /candidate/reference-semantics /candidate/verification.k \
  /audit-output/evidence/rule_inventory.md
```

Result: exit 0; 25 source files and 930 source-level entries inventoried,
including 696 rules and 228 syntax declarations.

## Body-sensitivity mutation

The scratch copy changes the first true-branch body expression from
`number + need` to `number - need`.

```bash
kompile /tmp/audit-work/159-eat/body-mutant/verification.k \
  --backend haskell --main-module EAT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition \
  /tmp/audit-work/159-eat/body-mutant-build/verification-kompiled

kprove /tmp/audit-work/159-eat/body-mutant/spec.k \
  --definition \
  /tmp/audit-work/159-eat/body-mutant-build/verification-kompiled \
  --spec-module EAT-SPEC
```

Results: build exit 0; proof exit 1 with `WarnStuckClaimState` and the expected
failed implication `NUMBER -Int NEED = NUMBER +Int NEED`.

## Fresh false-postcondition mutation

```bash
python3 /audit-output/evidence/make_false_postcondition.py \
  /tmp/audit-work/159-eat/candidate-source/spec.k \
  /tmp/audit-work/159-eat/candidate-source/spec-vacuity.k

kprove /tmp/audit-work/159-eat/candidate-source/spec-vacuity.k \
  --definition /tmp/audit-work/159-eat/fresh/verification-kompiled \
  --spec-module EAT-SPEC-VACUITY --dry-run

kprove /tmp/audit-work/159-eat/candidate-source/spec-vacuity.k \
  --definition /tmp/audit-work/159-eat/fresh/verification-kompiled \
  --spec-module EAT-SPEC-VACUITY
```

Results: generator exit 0; dry run exit 0; proof exit 1 with
`WarnStuckClaimState` and the expected failed implication
`NUMBER +Int NEED +Int 1 = NUMBER +Int NEED`.

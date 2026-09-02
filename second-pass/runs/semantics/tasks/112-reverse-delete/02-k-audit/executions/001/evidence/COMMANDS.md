# Audit command record

All commands were run from a clean source copy rooted at
`/tmp/audit-work/review-112/reconstruction` unless another working directory is
shown. Candidate-built definitions and caches were not copied.

## Toolchain

```sh
command -v kompile
command -v kprove
kompile --version
kprove --version
```

Status: all 0. Both tools reported K v7.1.337, build date 2026-06-18.
Output: `toolchain.log`.

## Integrity

```sh
python3 /audit-output/evidence/integrity_check.py
```

Status: 0. Output: `integrity-result.log`.

An additional direct recursive comparison was run:

```sh
diff -r --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics
```

Status: 0; no output.

## Trusted translation and Python differential

```sh
python3 /reference/py2mpy.py \
  /tmp/audit-work/review-112/source/solution.py \
  > /tmp/audit-work/review-112/regenerated-solution.mpy
cmp /tmp/audit-work/review-112/regenerated-solution.mpy \
    /tmp/audit-work/review-112/source/solution.mpy
```

Statuses: translator 0, `cmp` 0. Output: `translation-result.log`.

```sh
python3 /audit-output/evidence/differential_test.py \
  --canonical /reference/canonical.py \
  --generated /tmp/audit-work/review-112/source/solution.py \
  --inputs-output /audit-output/evidence/differential-inputs.json
```

Status: 0. Output: `differential-result.log`.

```sh
python3 /audit-output/evidence/satisfying_witnesses.py
python3 /audit-output/evidence/pinning_check.py
```

Statuses: 0, 0. Outputs: `satisfying-witnesses.log`,
`pinning-result.log`.

## Fresh concrete definition and execution

The first nine lines of `concrete_harness.py` were compared byte-for-byte with
the submitted `solution.py` before translation (`cmp` status 0).

```sh
python3 /reference/py2mpy.py concrete_harness.py > concrete_harness.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_harness.mpy --definition runtime-kompiled
```

Statuses: translator 0, `kompile` 0, `krun` 0. Outputs:
`runtime-kompile.log`, `concrete-krun.log`.

## Fresh proof definitions and positive claims

```sh
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module LOOP-SPEC
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Statuses: 0, 0, 0. Both proof commands printed `#Top`. Outputs:
`verification-kompile.log`, `loop-proof-full-definition.log`,
`entry-proof.log`.

The loop connection theorem was also checked against a definition that excludes
the installed summary rule:

```sh
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC
```

Statuses: 0, 0. The proof printed `#Top`. Outputs:
`verification-base-kompile.log`, `loop-proof-base-definition.log`.

## Static inventory

```sh
python3 /audit-output/evidence/k_rule_inventory.py \
  --semantics-root /reference/reference-semantics \
  --verification /candidate/verification.k \
  --spec /candidate/spec.k \
  --json-output /audit-output/evidence/k-inventory.json \
  --markdown-output /audit-output/evidence/k-inventory.md
python3 /audit-output/evidence/assess_k_inventory.py \
  --inventory /audit-output/evidence/k-inventory.json \
  --json-output /audit-output/evidence/k-inventory-assessed.json \
  --markdown-output /audit-output/evidence/k-inventory-assessed.md
```

Statuses: 0, 0. Outputs: `k-inventory-run.log`,
`k-inventory-assessment-run.log`. A direct count of statement starts and
inventory records produced 942 for both.

## Operational bridge checks

```sh
kprove bridge-context-spec.k \
  --definition verification-base-kompiled \
  --spec-module BRIDGE-CONTEXT-SPEC
kprove bridge-context-spec.k \
  --definition verification-kompiled \
  --spec-module BRIDGE-CONTEXT-SPEC
```

Statuses: 0, 0. Both printed `#Top`; the post-loop assignment to `after` is
preserved. Outputs: `bridge-context-base.log`, `bridge-context-full.log`.

```sh
kprove body-sensitivity-spec.k \
  --definition verification-kompiled \
  --spec-module BODY-SENSITIVITY-SPEC
```

Status: 1 as expected. Output: `body-sensitivity-proof.log`, containing
`WarnStuckClaimState` and a residual in which two retained distinct characters
produce `true` in the mutated body where the unchanged summary requires the
palindrome comparison.

## Fresh non-vacuity mutation

```sh
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run \
  > /tmp/audit-work/review-112/vacuity-dry-run.kore
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Statuses: dry-run 0; proof 1 as expected. Outputs:
`vacuity-dry-run.log`, `vacuity-proof.log`. The latter contains
`WarnStuckClaimState` and the failed equality between the actual Boolean and its
negation.

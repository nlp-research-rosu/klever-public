# Reviewer command record

All commands were run from `/audit-output` unless another working directory is
shown. Exit statuses are recorded in the corresponding log or in this file.

## Toolchain

```bash
{ python3 --version; kompile --version; kprove --version; krun --version; } \
  > /audit-output/evidence/toolchain.log 2>&1
```

Exit status: recorded as `toolchain.status`.

## Stage 1

```bash
python3 /audit-output/evidence/integrity_check.py \
  > /audit-output/evidence/stage1-integrity.log 2>&1
```

Exit status: recorded as `stage1-integrity.status`.

## Stage 2: trusted translation

```bash
bash /audit-output/evidence/stage2_regenerate.sh \
  > /audit-output/evidence/stage2-regenerate.log 2>&1
```

Exit status: recorded as `stage2-regenerate.status`.

## Stage 2: differential execution

```bash
python3 /audit-output/evidence/differential_test.py \
  > /audit-output/evidence/stage2-differential.log 2>&1
```

Exit status: recorded as `stage2-differential.status`.

## Stage 3: fresh definitions

Working directory: `/tmp/audit-work/reconstruction`

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled \
  > /audit-output/evidence/stage3-kompile-llvm.log 2>&1
```

Exit status: recorded as `stage3-kompile-llvm.status`.

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled \
  > /audit-output/evidence/stage3-kompile-haskell.log 2>&1
```

Exit status: recorded as `stage3-kompile-haskell.status`.

## Stage 3: fresh concrete execution

Working directory: `/tmp/audit-work/reconstruction`

```bash
sed -n '1,22p' /audit-output/evidence/concrete_harness.py \
  | cmp --silent solution.py -
```

Exit status: recorded as `stage3-harness-prefix.status`.

```bash
python3 /reference/py2mpy.py /audit-output/evidence/concrete_harness.py \
  > /audit-output/evidence/concrete_harness.mpy
```

Exit status: recorded as `stage3-harness-translate.status`.

```bash
krun /audit-output/evidence/concrete_harness.mpy \
  --definition runtime-audit-kompiled \
  > /audit-output/evidence/stage3-krun-harness.log 2>&1
```

Exit status: recorded as `stage3-krun-harness.status`.

## Stage 3: independently selected positive claims

```bash
python3 /audit-output/evidence/split_positive_specs.py \
  > /audit-output/evidence/stage3-split-positive-specs.log 2>&1
```

Exit status: recorded as `stage3-split-positive-specs.status`.

Working directory: `/tmp/audit-work/reconstruction`

```bash
kprove spec-claim-1.k --definition verification-audit-kompiled \
  --spec-module SPEC-CLAIM-1 \
  > /audit-output/evidence/stage3-kprove-claim-1.log 2>&1
kprove spec-claim-2.k --definition verification-audit-kompiled \
  --spec-module SPEC-CLAIM-2 \
  > /audit-output/evidence/stage3-kprove-claim-2.log 2>&1
kprove spec-claim-3.k --definition verification-audit-kompiled \
  --spec-module SPEC-CLAIM-3 \
  > /audit-output/evidence/stage3-kprove-claim-3.log 2>&1
kprove spec-claim-4.k --definition verification-audit-kompiled \
  --spec-module SPEC-CLAIM-4 \
  > /audit-output/evidence/stage3-kprove-claim-4.log 2>&1
```

Each exit status is recorded in the correspondingly numbered `.status` file.

The exact unsplit submitted spec was also run:

```bash
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC \
  > /audit-output/evidence/stage3-kprove-full-spec.log 2>&1
```

Exit status: recorded as `stage3-kprove-full-spec.status`.

## Stage 4: program pin and ground postconditions

```bash
python3 /audit-output/evidence/make_program_pin_spec.py
```

Exit status: recorded as `stage4-make-program-pin.status`.

Working directory: `/tmp/audit-work/reconstruction`

```bash
kprove spec-program-pin.k --definition verification-audit-kompiled \
  --spec-module SPEC-PROGRAM-PIN \
  > /audit-output/evidence/stage4-program-pin.log 2>&1
```

Exit status: recorded as `stage4-program-pin.status`.

This first pin attempt exited `113` at parsing because internal `.Stmts`
notation cannot be embedded in a program-surface claim. It is retained as a
discarded experiment and is not relied upon.

The successful parser-level identity check was:

```bash
python3 /audit-output/evidence/extract_verification_program.py \
  > /audit-output/evidence/stage4-extract-program.log 2>&1 &&
kast /audit-output/evidence/regenerated-solution.mpy \
  --definition runtime-audit-kompiled --sort Module --output kore \
  --output-file /audit-output/evidence/regenerated-solution.kore &&
kast /audit-output/evidence/verification-expanded.mpy \
  --definition runtime-audit-kompiled --sort Module --output kore \
  --output-file /audit-output/evidence/verification-expanded.kore &&
cmp --silent /audit-output/evidence/regenerated-solution.kore \
  /audit-output/evidence/verification-expanded.kore
```

Exit status: recorded as `stage4-kast-program-identity.status`.

```bash
python3 /audit-output/evidence/ground_claim_check.py \
  > /audit-output/evidence/stage4-ground-claims.log 2>&1
```

Exit status: recorded as `stage4-ground-claims.status`.

## Stage 5: exhaustive static inventory

```bash
python3 /audit-output/evidence/inventory_k_rules.py \
  > /audit-output/evidence/stage5-rule-inventory.log 2>&1
```

Exit status: recorded as `stage5-rule-inventory.status`. The generated
`rule-inventory.md` contains all 1,115 top-level declarations from the supplied
root/helper files and `verification.k`, including 708 rules, 234 syntax
declarations, all attributes, contexts, imports, and configuration.

## Stage 6: fresh non-vacuity mutation

Working directory: `/tmp/audit-work/reconstruction`

```bash
cp /audit-output/evidence/spec-vacuity-audit.k spec-vacuity-audit.k
kprove spec-vacuity-audit.k --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run \
  > /audit-output/evidence/stage6-vacuity-dry-run.log 2>&1
```

The copy and dry-run exit statuses are recorded in
`stage6-vacuity-copy.status` and `stage6-vacuity-dry-run.status`.

```bash
kprove spec-vacuity-audit.k --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  > /audit-output/evidence/stage6-vacuity-proof.log 2>&1
```

The expected nonzero exit status is recorded in
`stage6-vacuity-proof.status`.

```bash
python3 /audit-output/evidence/mutation_witness.py \
  > /audit-output/evidence/stage6-mutation-witness.log 2>&1
```

Exit status: recorded as `stage6-mutation-witness.status`.

## Final package consistency

```bash
python3 /audit-output/evidence/verify_audit_outputs.py \
  > /audit-output/evidence/final-consistency.log 2>&1
```

Exit status: recorded as `final-consistency.status`.

## Evidence manifest

```bash
{ sha256sum /audit-output/REVIEW.md;
  find /audit-output/evidence -maxdepth 1 -type f ! -name SHA256SUMS -print0 \
    | sort -z | xargs -0 sha256sum; } \
  > /audit-output/evidence/SHA256SUMS
```

Exit status: recorded as `manifest.status`.

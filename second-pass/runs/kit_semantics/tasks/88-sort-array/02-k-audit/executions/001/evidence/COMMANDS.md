# Reviewer command record

All commands below were run against copied sources in
`/tmp/audit-work/reconstruction`; candidate-provided compiled definitions were
never used. Full bounded outputs are in the named logs.

## Toolchain

```bash
kompile --version
kprove --version
krun --version
python3 --version
```

Observed: K `v7.1.293`, Python `3.10.12`.

## Stage 1

Working directory: `/audit-output`.

```bash
python3 /audit-output/evidence/audit_integrity.py
```

Exit 0. See `stage1-integrity.log`.

## Stage 2

Working directory: `/tmp/audit-work/reconstruction`.

```bash
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
python3 /audit-output/evidence/audit_differential.py
```

All exited 0. See `stage2-fidelity.log`.

## Stage 3

Working directory: `/tmp/audit-work/reconstruction`.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled

python3 py2mpy.py concrete_cases.py > concrete_cases.mpy
krun concrete_cases.mpy --definition fresh-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled

kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.empty

kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.nonempty
```

The builds and corrected concrete run exited 0. Each proof exited 0 and printed
`#Top`. See `stage3-kompile-llvm.log`, `stage3-concrete.log`,
`stage3-kompile-haskell.log`, `stage3-kprove-empty.log`, and
`stage3-kprove-nonempty.log`.

The preserved `stage3-concrete-attempt1-reviewer-error.log` is an auditor test
authoring error: `[3,1,2,1]` was initially given an ascending expected result
despite its even endpoint sum. The expectation was corrected to `[3,2,1,1]`
before the successful run.

## Stage 4

Working directory: `/tmp/audit-work/reconstruction`.

```bash
kast solution.mpy --definition fresh-verification-kompiled \
  --output json --output-file solution-kast.json

kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --dry-run --emit-json-spec spec-all.json

python3 /audit-output/evidence/audit_pinning.py
python3 /audit-output/evidence/adequacy_witness.py
```

All exited 0. See `stage4-pinning-adequacy.log`.

## Stage 5

Working directory: `/audit-output`.

```bash
python3 /audit-output/evidence/audit_rule_inventory.py
```

Exit 0. See `stage5-inventory.log` and `rule-inventory.md`.

## Stage 6

Working directory: `/tmp/audit-work/reconstruction`.

```bash
kprove spec-audit-false.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-FALSE-SPEC --dry-run

kprove spec-audit-false.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-FALSE-SPEC
```

Dry run exited 0. The proof exited 1 with `WarnStuckClaimState` and an actual
result `[2,0]` against the false target `[0,2]`. See
`stage6-mutation-dry-run.log`, `stage6-mutation-proof.log`, and
`stage6-mutation-validation.log`.

## Stage 7 supporting differential

Working directory: `/tmp/audit-work/reconstruction`.

```bash
python3 /audit-output/evidence/audit_k_differential.py
```

Exit 0: 344 cases in 22 fresh LLVM batches, zero mismatches against the trusted
canonical function. See `stage7-k-differential.log`.

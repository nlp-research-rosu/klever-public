# Reviewer command ledger

All commands were run from the stated working directory against sources copied
to `/tmp/audit-work/proof`. Candidate-provided compiled definitions and caches
were not copied or used. ANSI-colored output is preserved in the named bounded
logs.

## Stage 1

Working directory: `/audit-output`.

```sh
python3 /audit-output/evidence/integrity_check.py
```

Exit 0. Full output: `stage1-integrity.log`.

```sh
python3 /audit-output/evidence/generation_record_summary.py
```

Exit 0. Full output: `stage1-generation-record-summary.log`.

Tool observations:

```sh
kompile --version
kprove --version
```

Each exited 0 and reported K `v7.1.293`.

## Stage 2

Working directory: `/tmp/audit-work/proof`.

```sh
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
sha256sum solution.py solution.mpy regenerated-solution.mpy
```

All exited 0. `solution.mpy` and the regenerated file both had SHA-256
`dfeb6ac63836b0ff5014334a279dd1e5f625a17de4a5aba7e45e034ccab07b8a`.
Full output: `stage2-regeneration.log`.

```sh
python3 /audit-output/evidence/differential_test.py
```

Exit 1 because the script intentionally rejects any ordinary-domain mismatch.
It ran 2,518 ordinary cases and found the preserved large-integer mismatch.
Full output: `stage2-differential.log`.

## Stage 3

Working directory: `/tmp/audit-work/proof`.

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0. Full output: `stage3-kompile-llvm.log`.

```sh
krun smoke.mpy --definition runtime-kompiled
```

Exit 0; final configuration had `.K`, `NoExc`, and exit code 0. Full output:
`stage3-krun-smoke.log`.

```sh
kompile verification.k \
  --backend haskell \
  --main-module TRIANGLE-AREA-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0. Full output: `stage3-kompile-haskell.log`.

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module TRIANGLE-AREA-SPEC
```

Exit 0 and printed `#Top`. Full output: `stage3-kprove-positive.log`.

## Stage 4

```sh
python3 /audit-output/evidence/constructor_identity.py
```

Exit 0. Full output: `stage4-constructor-identity.log`.

```sh
python3 /audit-output/evidence/ground_witness.py
```

Exit 0. Full output: `stage4-ground-witness.log`.

Working directory: `/tmp/audit-work/proof`.

```sh
python3 py2mpy.py overflow-witness.py > overflow-witness.mpy
python3 overflow-witness.py
```

Both exited 0. The submitted CPython implementation returned `1e308` and its
assertion passed. Output: `stage4-python-submitted-overflow.log`.

```sh
python3 -c "import sys; sys.path.insert(0, \"/reference\"); from canonical import triangle_area; print(triangle_area(10 ** 308, 2))"
```

Exit 1 with `OverflowError`. Output: `stage4-python-canonical-overflow.log`.

```sh
krun overflow-witness.mpy --definition runtime-kompiled
```

Exit 1 with modeled `AssertionError` and `<exit-code> 1 </exit-code>`, showing
the supplied concrete `divII` equation does not reproduce the submitted
CPython result. Output: `stage4-krun-overflow.log`.

Body-sensitivity definition:

```sh
kompile verification-body-mutated.k \
  --backend haskell \
  --main-module TRIANGLE-AREA-BODY-MUTATION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutation-kompiled
```

Exit 0. Output: `stage4-body-mutation-kompile.log`.

```sh
kprove spec-body-mutated.k \
  --definition body-mutation-kompiled \
  --spec-module TRIANGLE-AREA-BODY-MUTATION-SPEC
```

Expected exit 1 with `WarnStuckClaimState`; the residual is
`divII(A +Int H, 2) == divII(A *Int H, 2)`. Output:
`stage4-body-mutation-kprove.log`.

## Stage 5

```sh
python3 /audit-output/evidence/build_rule_inventory.py \
  > /audit-output/evidence/stage5-rule-inventory.md
```

Exit 0. The exhaustive inventory contains 228 syntax declarations, 696 rules,
five contexts, one configuration, and one claim.

## Stage 6

Working directory: `/tmp/audit-work/proof`.

```sh
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module TRIANGLE-AREA-SPEC-VACUITY-AUDIT
```

Expected exit 1 with `WarnStuckClaimState`; the residual is
`divII(A *Int H +Int 1, 2) == divII(A *Int H, 2)`. Full output:
`stage6-false-postcondition-kprove.log`.

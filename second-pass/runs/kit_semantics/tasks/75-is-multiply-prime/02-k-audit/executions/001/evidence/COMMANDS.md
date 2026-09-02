# Audit command record

Scratch directory: `/tmp/audit-work/75-audit-vYfTjU`.

All source copied into scratch came from `/candidate` or the trusted
`/reference` mounts. Candidate `*-kompiled` directories were not copied or
used.

## Provenance and integrity

```bash
python3 /audit-output/evidence/provenance_check.py
```

Exit `0`; `PROVENANCE_CHECK_EXIT=0`; full output:
`provenance-integrity.log`.

## Translation and differential fidelity

```bash
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
sha256sum solution.mpy regenerated-solution.mpy
```

Both exits `0`; both SHA-256 values
`2ed20f37c9f9cc534ea932248a2599788f3e6de80cc7303669d627aef0439709`;
full output: `translation-fidelity.log`.

```bash
python3 /audit-output/evidence/differential_test.py canonical.py solution.py
```

Exit `0`; 134 inputs; zero mismatches; full input list and result:
`differential-test.log`.

## Fresh concrete build and execution

The reviewer-authored `concrete_driver.py` was copied into scratch and
translated with:

```bash
python3 py2mpy.py concrete_driver.py > concrete_driver.mpy
```

Exit `0`.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit `0`; `LLVM_KOMPILE_EXIT=0`; full output:
`fresh-llvm-build.log`.

```bash
krun solution.mpy --definition runtime-kompiled
```

Exit `0`; `KRUN_SOLUTION_EXIT=0`; final `.K`, `NoExc`, exit code `0`;
full output: `fresh-krun-solution.log`.

```bash
krun concrete_driver.mpy --definition runtime-kompiled
```

Exit `0`; `KRUN_DRIVER_EXIT=0`; all eight assertions passed; final `.K`,
`NoExc`, exit code `0`; full output: `fresh-krun-driver.log`.

## Fresh symbolic build and positive proof

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit `0`; `HASKELL_KOMPILE_EXIT=0`; full output:
`fresh-haskell-build.log`.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.is-multiply-prime
```

Exit `0`; output contains `#Top`; `KPROVE_POSITIVE_EXIT=0`; full output:
`fresh-positive-proof.log`.

## Pinning and contract checks

```bash
python3 /audit-output/evidence/claim_pinning_check.py \
  solution.mpy spec.k canonical.py solution.py
```

Exit `0`; exact constructor equality, formal precondition/result parsing, and
five satisfying witnesses all passed; full output: `claim-pinning.log`.

```bash
python3 /audit-output/evidence/contract_set_check.py spec.k
```

Exit `0`; the independently enumerated set of products of three primes below
100 exactly equals the 22 postcondition values; full output:
`contract-set-check.log`.

## Exhaustive static inventory

```bash
python3 /audit-output/evidence/k_inventory.py \
  reference-semantics/semantics.k reference-semantics/semantics/*.k \
  verification.k spec.k > /audit-output/evidence/k-rule-inventory.md

python3 /audit-output/evidence/classify_k_inventory.py \
  reference-semantics/semantics.k reference-semantics/semantics/*.k \
  verification.k spec.k > /audit-output/evidence/classified-k-inventory.tsv
```

Both exits `0`. Inventory totals: 227 syntax declarations, one
configuration, five contexts, 695 rules, and one claim (929 items total).
Assessment: `rule-assessment.md`.

## Fresh non-vacuity mutation

The preserved mutation is `spec-audit-vacuity.k`; only its module/claim names
and final result disjunct (`A ==Int 99` to `A ==Int 97`) differ from the
positive spec.

```bash
kprove spec-audit-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-AUDIT-VACUITY \
  --claims SPEC-AUDIT-VACUITY.audit-false-postcondition \
  --dry-run
```

Exit `0`; `MUTATION_DRY_RUN_EXIT=0`; full output:
`fresh-vacuity-dry-run.log`.

```bash
kprove spec-audit-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-AUDIT-VACUITY \
  --claims SPEC-AUDIT-VACUITY.audit-false-postcondition
```

Exit `1` as expected; `WarnStuckClaimState` and failed implication; witness
`A=99` satisfies `A<100`, the real program returns true, and the mutation
requires false. Full output: `fresh-vacuity-proof.log`.

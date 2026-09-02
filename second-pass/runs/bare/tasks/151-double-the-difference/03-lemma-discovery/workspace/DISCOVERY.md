# Trust-boundary classification

The canonical inventory contains 10 rules, all in the `VERIFICATION` module.
Every rule is classified exactly once as `DEFINITION`.

The first two rules expose named proof terms:

- `loopBody` expands to the translated loop statement tree.
- `solutionProgram` expands to the translated module tree used by the
  end-to-end claim.

The remaining rules define the mathematical summary used by the claims:

- The two complementary `selectedSquare` equations define the selected and
  ignored integer cases.
- The six `oddSquareFold` equations define its empty-list case and its
  recurrence for integer, float, true boolean, false boolean, and nested-list
  elements.

These rules are equations and recurrences for newly introduced terms. They are
not ordinary execution rules and do not assert extra reusable mathematical
facts beyond those definitions. Consequently, the canonical inventory has no
rules classified as `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The Stage 1 evidence in `/reference/k-proof/prove.sh` first compiles
`verification.k` as module `VERIFICATION`, so all 10 inventory rules are
already present in `verification-kompiled`. It then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

That command proves the loop-invariant and end-to-end claims in `spec.k`; it
does not first prove any inventory rule against a module from which that exact
rule is absent. Thus no inventory rule satisfies the required ordering and
exact-correspondence test for a proved derived lemma.

## Domain lemmas

The domain-lemma set is empty. No canonical rule is classified as
`DOMAIN_LEMMA`, and the inventory reports no rule carrying the
`simplification` attribute.

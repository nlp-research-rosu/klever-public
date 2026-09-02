# Trust-boundary discovery

The canonical inventory contains 13 rules from the `VERIFICATION` module. Each
is classified exactly once and in canonical inventory order in
`trust-boundary.json`.

## Definitions

Ten rules are definitions:

- `solutionLoopBody`, `solutionBody`, and `solutionClosure` expand named proof
  terms into the exact constructor-level program representation.
- The two `allInts` rules structurally define the integer-list precondition.
- `intProjection(I:Int) => I` defines the projection on its intended integer
  domain.
- `oddAtEvenPositions` and the three `oddAtEvenAcc` equations define the
  mathematical summary used by the invariant and final postcondition.

These rules are equations, macro expansions, base cases, or recursive cases;
they do not assert independent domain facts.

## Operational verification rules

Three guarded, priority-40 rules rewrite the `<k>` cell for `%`, `+`, and `*`.
They are classified as `OPERATIONAL_RULE` because they directly specify
execution of `BinOp` terms in the verification model when `isInt(V)` holds.
They bridge the symbolic `Val` representation to `intProjection(V)` and are
not summary-function equations.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications. Stage 1's
`prove.sh` first compiles `verification.k` in its entirety into
`verification-kompiled`, then invokes:

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

That invocation proves the `loop-invariant` and `solution-correct` claims with
all 13 inventory rules already present. There is no earlier proof against a
module omitting any inventory rule, no later installation of an exact proved
statement as a reusable rule, and therefore no Stage 1 evidence satisfying the
required ordering for a separately proved derived lemma.

## Domain lemmas

The domain-lemma set is empty. No inventory rule carries the `simplification`
attribute, and none is an additional mathematical fact outside the
definitions and operational verification rules described above.

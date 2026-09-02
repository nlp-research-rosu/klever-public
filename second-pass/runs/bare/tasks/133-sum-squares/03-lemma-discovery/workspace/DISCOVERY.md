# Trust-boundary discovery

The canonical inventory identifies four rules in the local verification-module
closure, all from module `VERIFICATION`. All four are classified as
`DEFINITION`:

- `squareCeil(V) => ceilInt(V) *Int ceilInt(V)` defines the named
  ceiling-square summary.
- `sumSquares(VS) => sumSquaresFrom(0, VS)` defines the public list summary by
  initializing its accumulator.
- `sumSquaresFrom(A, nil) => A` is the base equation of the accumulator
  recurrence.
- `sumSquaresFrom(A, cons(V, VS)) => ...` is the step equation of that
  recurrence.

These rules define mathematical summaries used in the reachability claims.
They are not execution or observation transitions, so none is an
`OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical inventory.
Stage 1's `prove.sh` first runs:

```sh
kompile verification.k \
  --backend haskell \
  --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION
```

It then invokes `kprove spec.k --definition verification-kompiled`. Thus all
four inventory rules are already present in the compiled definition used by
the proof. Stage 1 does prove the claims in `spec.k`, including the
`all-numeric-lists` claim and the `loop-invariant` claim, but it does not first
prove any inventory rule against a module omitting that rule and then reuse an
exact corresponding rule. Consequently, no inventory rule satisfies the
required `PROVED_DERIVED_LEMMA` ordering criterion.

## Domain lemmas

The domain-lemma set is empty. No canonical inventory rule asserts an
additional mathematical fact beyond the defining equations above, and no
inventory rule carries the `simplification` attribute.

# Trust-boundary discovery

The exhaustive canonical inventory contains one rule, from `VERIFICATION`.
It is classified as `PROVED_DERIVED_LEMMA`.

## Separately proved derived lemma

`rule-73f9484c2d5d4a2650340be4aa44fdeb23887916e674aa08b16de37c95cfb1fe`
is the reusable Euclidean-loop summary. Its Stage 1 proof evidence is:

1. `prove.sh` first compiles `loop-verification.k` as
   `LOOP-VERIFICATION`. That module imports `semantic.k` and `gcd-spec.k`; it
   does not import `verification.k` and therefore does not contain the
   inventoried summary rule.
2. `prove.sh` then runs `kprove loop-spec.k --definition loop-kompiled`.
   The claim in `loop-spec.k` has the same loop AST, nonnegative-input
   precondition, and environment transformation to `gcdSpec(A, B)`, zero
   `b`, and `finalR(B, R0)`.
3. Only after that proof succeeds does `prove.sh` compile `verification.k`.
   The inventoried rule is the reusable continuation-framed form of the
   proved state transformer; `priority(40)` controls its application and
   does not add a mathematical postcondition.
4. The resulting verification definition is then used for the separate
   whole-program proof in `spec.k`.

No inventoried rule carries the `simplification` attribute. The canonical
inventory contains no other local rule requiring classification.

The domain-lemma set is empty.

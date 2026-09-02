# Trust-boundary discovery

## Canonical scope

`/reference/rule-inventory.json` is the exhaustive canonical inventory used for
this classification. Its inventory hash is
`c7d4c5b3a7bc27a03f386a579a0214d8e3d8c738efff051f731036e5290aa152`,
and it contains two rules, both in module `VERIFICATION`. The output preserves
their inventory order and classifies each `source_rule_id` exactly once.

Rules from the supplied reference semantics, the `solutionProgram` equation in
`program.k`, reachability claims in `spec.k`, and generated backend rules are
not canonical inventory entries and therefore are not added to
`trust-boundary.json`.

## Rule classifications

### Empty-sequence equation

`rule-5ea09376a68c388fa472315e5a536792a41ff43051dca71cb26ead91d202a76d`
is classified as `DEFINITION`. It is the base equation
`sumCeilSquares(.ValSeq) => 0` of the `[function, total]` mathematical fold.
It introduces the summary's value on the empty sequence and neither rewrites a
Python computation nor supplies an independent mathematical theorem.

### Cons-sequence equation

`rule-681871636bed54428193956727088b21b492bc6c75570d01a289f5f5e087030a`
is classified as `DEFINITION`. It is the structurally decreasing recurrence
for `sumCeilSquares(vCons(V, VS))`, defining the summary as
`ceilF(V) *Int ceilF(V)` plus the summary of `VS`. It names the result that the
fixed-semantics loop computes. It is not an operational observation rule and
does not add an algebraic/domain fact beyond the definition itself.

The two equations are constructor-disjoint and exhaustive for `ValSeq`; the
recursive equation descends on the tail. Neither canonical rule carries the
`simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` compiles `verification.k` with both canonical equations
already present, then proves `SPEC.loop-inv` and the complete `SPEC` claims.
The corresponding `kprove-loop.out` and `kprove.out` files each contain
`#Top`. This proves the reachability claims under the compiled theory, but it
does not demonstrate the required ordering for a separately proved derived
rule: no canonical rule's exact statement is first proved against a module
that omits that rule and only then added. The proved loop invariant is a claim
in `spec.k`, not a canonical rule entry.

## Domain lemmas

The domain-lemma set is empty. Neither canonical rule is an extra trusted
mathematical fact; both are equations defining the recursive summary.

## Classification counts

- `DEFINITION`: 2
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

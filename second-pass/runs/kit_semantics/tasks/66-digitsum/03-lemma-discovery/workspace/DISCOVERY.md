# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory
SHA-256:

```text
a4e81b7526afaf06451faab8a91e569389fec6f0afd1a15ea730072963212557
```

It contains two rules, both from the local `VERIFICATION` module. They are
classified exactly once and in canonical inventory order in
`trust-boundary.json`.

## Rule classifications

1. `rule-e470dad5bcaab0cce73635a8c1bc13a406d112c55527ad14e4ae9317461108c4`
   is `DEFINITION`. It is the empty-sequence base equation
   `digitSumIS(.IntSeq) => 0` for the total recursive mathematical summary.
   It has no configuration cells, continuation, state transition, or
   simplification attribute.

2. `rule-b3786e0b561f5d76d2d73d69b0306d78d399d738da6b14efa48ef6eb76a56060`
   is `DEFINITION`. It is the nonempty-sequence recurrence for `digitSumIS`;
   it defines the head contribution using the fixed model's uppercase
   condition and structurally recurs on `REST`. It does not rewrite a program
   term or state an additional cross-symbol mathematical fact. It also has no
   simplification attribute.

Together the two constructor cases are disjoint and exhaustive for `IntSeq`.
They define the proof's named result summary. The operational Python rules are
imported from the supplied reference semantics and are not members of the
canonical local verification-module inventory.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical inventory.
Stage 1 `prove.sh` compiles `verification.k` with both inventory rules already
present and then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The recorded `proof-positive.log` contains `#Top`, but this ordering proves the
reachability claims under the two defining equations; it does not first prove
either exact rule against a module that omits that rule. Therefore neither rule
qualifies as `PROVED_DERIVED_LEMMA`. The proved loop circularity in `spec.k` is
a claim, not a canonical inventory rule, and is not added to the JSON.

## Domain lemmas

The domain-lemma set is empty. Neither canonical rule is an additional trusted
mathematical fact: both are equations defining `digitSumIS`.

The operational-rule set within this canonical inventory is also empty.

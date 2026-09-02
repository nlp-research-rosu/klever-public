# Rule trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory
SHA-256
`01a612e13f79b9f6a231be1502c29934494444339c9f77c964b5837379e003af`.
It contains two rules, and both are classified exactly once in inventory order
in `trust-boundary.json`.

## Classification

Both rules are `DEFINITION`.

- `rule-82445bea9adcbbe979699c705f558f66f814a969deb1b899bcc8356b74b84d31`
  is the guarded base equation for the total `finishPile` function. For
  `I >=Int N`, it defines the summary value as the accumulated sequence `A`.
- `rule-63431e432f0bf08d6bc0c04732f82fcd4f0d71ba7458f65345b9c101ef3654d8`
  is the guarded recursive equation for `finishPile`. For `I <Int N`, it
  defines the summary by appending `N +Int (2 *Int I)` and recurring with
  `I +Int 1`.

Together, the disjoint guards define the base and recursive cases of the named
mathematical list summary declared `[function, total]`. Neither rule matches a
`<k>` cell or any other configuration cell, so neither is an
`OPERATIONAL_RULE`. Neither rule carries the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived rules in the canonical inventory.

Stage 1's `prove.sh` first compiles `verification.k` with both `finishPile`
equations already present and then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The recorded `proof.out` is `#Top`, but Stage 1 has no earlier proof against a
module omitting either inventory rule and no later step adding an exactly
corresponding reusable rule. Consequently, neither inventory rule satisfies
the required ordering for `PROVED_DERIVED_LEMMA`.

The `pile-loop` item discussed as a derived reachability lemma in Stage 1's
`PROOF.md` is a claim in `spec.k`, not a rule in the canonical
verification-module inventory. It therefore receives no rule classification
here.

## Domain lemmas

The domain-lemma set is empty. No canonical rule adds a trusted mathematical
fact beyond the equations defining `finishPile`.

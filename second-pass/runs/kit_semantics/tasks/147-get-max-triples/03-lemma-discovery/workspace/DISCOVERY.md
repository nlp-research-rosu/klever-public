# Trust-boundary rule discovery

The canonical inventory hash is
`97e6022f17f451a5f99cac62e3030189934e65106ea945ffd1d51f7a67b6ebf5`.
It contains three rules, and `trust-boundary.json` preserves their inventory
order and classifies each source rule ID exactly once.

## Classifications

All three rules are `DEFINITION`:

1. `rule-7f4fda07af964878549fb6179e4214215094e6afdc0f799801aef078770bc8f4`
   is the sole equation for the `[function, total]` symbol
   `zeroResidueCount`. It defines that named arithmetic summary using the
   reference semantics' floor-division normal form.
2. `rule-da6a4e2936c513bfd13e5a5dabe3f487b5f2fc80dad7975a6a8838c23f087590`
   is the sole equation for the `[function, total]` symbol `chooseThree`. It
   defines the named `X*(X-1)*(X-2)//6` summary in `pyMod`/`/Int` form.
3. `rule-f0b13856a8dad7aae0ba7cb74d4c557bf3d05dd316341f9923211e2c0e60ee6c`
   is the sole equation for the `[function, total]` symbol
   `expectedTriples`. It defines the postcondition summary by composing the
   other two definitions.

These equations rewrite only their proof-summary symbols. They contain no K
configuration cells and do not execute, intercept, or observe the Python
machine state, so none is an `OPERATIONAL_RULE`. Their equations give the
meanings of newly named proof terms rather than asserting independent facts
about previously defined operations, so none is a `DOMAIN_LEMMA`. The
inventory reports an empty attribute list for every rule; in particular, there
are no `simplification` rules requiring separate treatment.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` with all three inventory
rules present and then runs the single positive target command:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The remaining `kprove` commands are expected-failure postcondition and body
mutations. Stage 1 contains no earlier proof against a module omitting one of
the inventory rules, followed by reuse of an exactly corresponding proved
statement. Consequently, no rule meets the required evidence ordering for
`PROVED_DERIVED_LEMMA`.

## Domain-lemma set

The domain-lemma set is empty.

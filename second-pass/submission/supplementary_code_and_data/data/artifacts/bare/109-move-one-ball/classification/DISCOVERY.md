# Trust-boundary discovery

The canonical inventory contains 11 rules, all from
`HUMAN-EVAL-VERIFICATION`. Every rule is classified as `DEFINITION`.
The inventory has no rules carrying the `simplification` attribute.

## Classification basis

The rules at verification lines 16–30 are equations or structural
recurrences for mathematical helper functions:

- `length` has empty and recursive-list equations.
- `last` has singleton and recursive-list equations.
- `dropBit` has complementary conditional equations for descent and
  non-descent cases.
- `dropsFrom` is a base-and-step fold that counts descents from a predecessor.
- `cyclicDrops` defines the empty case and reduces a nonempty circle to
  `dropsFrom`.

The final rule at verification line 34 is also a `DEFINITION`: it defines the
named proof predicate `rotationSortable` to mean that `cyclicDrops` is at most
one. Its source comment records the intended correspondence with a sortable
right rotation for distinct integers, but the rule itself is a defining
equation, not a separately established reusable lemma.

None of these rules is an `OPERATIONAL_RULE`. They do not step the Python
machine configuration or observe an execution state; those rules live in
`semantic.k`, outside the launcher-declared canonical verification-module
inventory.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The Stage 1 evidence does not contain the required prove-before-introduction
ordering for any inventory rule. `prove.sh` first compiles `semantic.k`;
`semantic.k` imports `verification.k`, so all 11 inventory rules are already
present in the compiled definition. The script then invokes `kprove` once on
the claims in `spec.k`. There is no earlier proof against a module omitting an
inventory rule, followed by introduction of an exactly corresponding rule.
Consequently, the successful Stage 1 claims cannot reclassify any of these
preloaded definitions as proved derived lemmas.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. No canonical inventory rule is an additional
mathematical fact layered on top of the defined functions; every entry is part
of the equations that define those functions or the named proof predicate.

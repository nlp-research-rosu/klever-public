# K proof trust-boundary discovery

## Canonical scope

This classification uses `/reference/rule-inventory.json` as the exhaustive
canonical inventory. Its copied inventory digest is:

```text
057e543a7a1bec5cd371a17815bc2bf5cf7813d6a73f548b5382fd60ad6293e2
```

The inventory contains eight rules, all from the `VERIFICATION` module. Each
canonical `source_rule_id` appears exactly once in `trust-boundary.json`, in
canonical inventory order.

## Definitions

Six rules are `DEFINITION`:

- `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08`
  and
  `rule-6316a60ea115abdbe8e03d39d302e43ceea73cd9fedd27a98872c76b5b811b42`
  are the empty and cons equations defining the structural `allInts`
  predicate.
- `rule-537b55658be09522e9ef565d2ec69183fd6fbd782b54c8d1b5dd24667acbd3aa`
  and
  `rule-a4eb647db56262adb78bb0c7a909b63ee0acc886d9d451ca5de28976ba45ea55`
  are the base and recursive equations defining `kadaneCurrent`.
- `rule-0fb2ff70d1d771be4491e1d1d3d07c7bb4778cb5ac74c239f4b9ade2421d3d71`
  and
  `rule-db274c9f572feeb0ce3aedc0579c3303eb84577ca9baa4e5034eed5a969803f6`
  are the base and recursive equations defining `kadaneMinimum`.

These equations introduce or recursively define named structural and
mathematical summaries. They are not additional reusable facts about imported
semantic symbols.

## Operational rules

The canonical verification-module inventory contains no `OPERATIONAL_RULE`.
None of its eight entries is an ordinary execution or observation rule over
configuration cells; the inventory consists of definitions and two
proof-local simplification facts.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 supplies no evidence with the required ordering. In
`/reference/k-proof/prove.sh`, `verification.k` is compiled before the positive
`kprove spec.k` command, so both simplification rules are already in the theory
used to close the claims. No earlier command proves either exact rule statement
against a module that omits it. The concrete `krun` assertions,
`differential_test.py`, false-postcondition probe, and body-mutation probe are
useful validation evidence, but they are not universal, rule-free proofs of
the exact simplification statements.

Consequently, the Stage 1 prose description of these rules as derived lemmas
does not qualify them for `PROVED_DERIVED_LEMMA` under the requested evidence
standard.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly two rules:

- `rule-2944c4d3c7bc5a2d260f24ca8fd4234701fa8f82f00db7ca3317fa06458082b5`
  simplifies guarded `applyBin("+", I:Int, V:Val)` to integer addition.
- `rule-7749c9857edd14009417bdaa86b5d4b1c229fa0013cc411eaf35ed3a49ed0842`
  simplifies guarded two-argument `applyBuiltin("min", V:Val, I:Int, .Vals)`
  to `minInt`.

Both rules carry the `simplification` attribute. They rewrite imported
semantic symbols rather than define new named summaries, and Stage 1 does not
first prove their exact statements in a rule-free module. They are therefore
classified as trusted `DOMAIN_LEMMA`s, as required by the allowed
simplification-rule classifications.

## Classification totals

- `DEFINITION`: 6
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 2

Total: 8 canonical rules.

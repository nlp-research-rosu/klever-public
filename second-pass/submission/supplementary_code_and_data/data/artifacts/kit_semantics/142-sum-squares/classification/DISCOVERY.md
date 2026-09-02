# Rule trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory
SHA-256
`6439ddecb014c1e9198717de95f81e55c2a88c70397d51f90541a880f782765e`.
It contains 19 rules from `VERIFICATION`. Every canonical `source_rule_id`
appears exactly once and in canonical order in `trust-boundary.json`.

## Classification method

Rules introducing the program-body macros, predicates, projection helper,
branch summary, or recursive accumulator summary are `DEFINITION`. These rules
give equations, recurrences, macro expansions, or structural cases for newly
named proof terms.

No inventoried rule is an `OPERATIONAL_RULE`. The macros define syntax, the
summary rules are pure functions, and the rules over the existing cast and
`applyBin` operations carry `simplification`. Per the required classification
constraint, those simplification rules are classified as definitions when they
define a proof-local helper and as domain lemmas when they assert an additional
fact about an existing operation or a reusable property.

The following five rules are `DOMAIN_LEMMA`:

- `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
  characterizes `#Ceil` of the pre-existing partial Val-to-Int cast.
- `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d`
  rewrites that pre-existing cast back to the proof-local total projection.
- `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081`
  asserts projection idempotence.
- `rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4`
  supplies guarded symbolic multiplication dispatch over `Val`.
- `rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc`
  supplies guarded symbolic addition dispatch over `Val`.

These are additional mathematical facts used by simplification. Stage 1 gives
ground comparisons and negative probes for them, but those checks are not
universal proofs of the exact rules and therefore do not change their
classification.

The domain-lemma set is **not empty**; it contains exactly the five rule IDs
listed above.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1 runs:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --trusted SPEC.loop-invariant
```

Both commands use `verification-kompiled`, which was built from the complete
`verification.k` containing all 19 canonical rules. None first proves an exact
inventoried rule statement against a module that omits that rule.

The first command separately proves the reachability claim
`SPEC.loop-invariant`, and the second command uses that claim as trusted. That
claim is not a rule in the canonical inventory, so it is not eligible for a
rule classification here. Likewise, `spec-projection-vacuity.k` only rejects
the false ground result `projectIntTotal(2) => 3`; it does not prove any exact
projection or dispatch rule against a rule-free module.

Consequently, Stage 1 supplies no ordering-and-correspondence evidence meeting
the required standard for `PROVED_DERIVED_LEMMA`.

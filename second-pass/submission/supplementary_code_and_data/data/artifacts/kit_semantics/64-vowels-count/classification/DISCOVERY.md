# Trust-boundary discovery

## Canonical scope

The sole classification authority is
`/reference/rule-inventory.json`, whose `inventory_sha256` is
`016f23d6c21435b58eea72f72774ef91166fc2d422c670009b869717cfea0da7`.
It declares `VERIFICATION` as the only local verification module and contains
exactly two rules. The mounted `verification.k` SHA-256,
`6bc684e38c7c1dfc4d991fa29f3d68c911d06824d5715b4a8a599cdd25c408c9`,
matches the inventory metadata.

Rules imported from the supplied reference semantics are outside this
canonical local-rule inventory and therefore are not added to or classified
in `trust-boundary.json`.

## Classifications

| Inventory position | Source rule | Classification | Reason |
|---:|---|---|---|
| 0 | `rule-ad7d69a43b55c7d713eb912ef35d6d9c5b48ec3b76133d9058d939e165530edf` | `DEFINITION` | This rule is the empty-sequence equation for the declared total function `vowelsTail`. It defines the terminal `y`/`Y` contribution and has no operational configuration or observation pattern. |
| 1 | `rule-5ef4c64339248ffdcfe1ebbeb14f7c7490e1d2b6b56b81a6718dfd908e382af8` | `DEFINITION` | This rule is the constructor-step recurrence for `vowelsTail`. It defines the current character's contribution and descends structurally to `REST`; it does not replace a `<k>` computation. |

The two equations cover the two `IntSeq` constructors used by the total
summary. Their canonical `attributes` arrays are empty, so neither carries
the `simplification` attribute. No operational or observation rule appears
in the inventory.

Classification totals:

- `DEFINITION`: 2
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The domain-lemma set is empty.

## Separately proved derived lemmas

There are no separately proved derived rules in the canonical inventory.

Stage 1 `prove.sh` compiles `verification.k` at lines 16–19, with both
`vowelsTail` equations already present, before either proof command. It then
proves `SPEC.loop-inv` at lines 20–23 and the complete `SPEC` module at lines
24–26 against that compiled definition. There is no earlier proof against a
module omitting either inventory rule, and there is no later reusable rule
whose exact statement corresponds to such an earlier proof. Consequently,
neither equation qualifies as `PROVED_DERIVED_LEMMA`.

`SPEC.loop-inv` is separately exercised by `kprove`, but it is a reachability
claim in `spec.k`, not a canonical inventory rule with a `source_rule_id`.
It therefore does not create a `PROVED_DERIVED_LEMMA` entry in this
rule-classification output.

## Coverage checks

- Canonical rule count: 2.
- Output rule count: 2.
- Distinct canonical `source_rule_id` count: 2.
- Distinct output `source_rule_id` count: 2.
- Output order is identical to inventory order.
- Every canonical rule is classified exactly once.
- No noncanonical rule, theorem, or replacement formulation is present in
  `trust-boundary.json`.

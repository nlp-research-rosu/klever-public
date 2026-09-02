# Trust-boundary discovery

## Canonical scope

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`8562989cb1139eab0ae6201ecdb15f1af6a793bb508e807029a8c1e23f45801e`.
It contains exactly one rule. `trust-boundary.json` preserves that sole
`source_rule_id` in inventory order and classifies it exactly once.

The inventory rule has only the `priority(40)` attribute. It does not carry
`simplification`, so the special restriction on simplification rules does not
apply.

## Classification

| Canonical rule | Classification | Reason |
|---|---|---|
| `rule-d4a0ca7c71bd8004730d058283a2e7c70fe73c82b0044f80eda2cfa19e148b41` | `PROVED_DERIVED_LEMMA` | Its complete loop, return, and frame-cleanup statement was proved successfully against a definition that did not contain the rule, before the rule was compiled into the final verification definition. |

The rule has an operational role—it accelerates the remaining loop and call
cleanup—but the Stage 2 classification is `PROVED_DERIVED_LEMMA`, rather than
`OPERATIONAL_RULE`, because the mounted evidence satisfies the stricter
proof-before-use criterion.

## Separately proved derived lemmas

There is exactly one separately proved derived lemma:
`rule-d4a0ca7c71bd8004730d058283a2e7c70fe73c82b0044f80eda2cfa19e148b41`.

The Stage 1 evidence is:

1. **Exact statement correspondence.** The claim at
   `/reference/k-proof/loop-connection-spec.k:6` and the rule at
   `/reference/k-proof/verification.k:10` have the same rewrite, guard,
   continuation, bindings, cells, frames, and result. Removing only the
   claim/rule wrapper and their respective nonlogical attributes
   (`filter-loop-connection` and `priority(40)`) makes their normalized text
   identical.
2. **Rule-free proof definition.**
   `/reference/k-proof/loop-connection-spec.k` requires and imports
   `VERIFICATION-CORE`. `/reference/k-proof/verification-core.k` requires
   `domain.k` and does not require or import `verification.k`; consequently,
   the canonical `VERIFICATION` rule is absent from the definition used for
   the connection proof.
3. **Proof-before-use ordering.** In `/reference/k-proof/prove.sh:37`,
   `verification-core.k` is compiled as `loop-connection-kompiled`, and at
   line 41 the exact connection claim is proved against that definition.
   Only later, at line 46, is `verification.k` compiled with the rule for the
   final target proof.
4. **Positive proof result.** `/reference/k-proof/PROOF.md:253` records the
   `VERIFICATION-CORE` compilation and the corresponding `kprove
   loop-connection-spec.k` command; line 260 records `#Top, exit 0`.

No other canonical rule is present, so there are no canonical
`DEFINITION` or `OPERATIONAL_RULE` entries.

**The domain-lemma set is empty.** No canonical rule is classified as
`DOMAIN_LEMMA`.

# Trust-boundary discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`, with:

- schema version: `2`
- inventory SHA-256:
  `204f58f331c4d67162af18c6fd2169b721f142d31a4e056becaa1424420ddd12`
- verification module: `VERIFICATION`
- canonical rules: 13
- rules carrying `simplification`: 0

The mounted `verification.k` SHA-256 is
`07cbc3fc57044faf70fbbe6c0856dcb214633c5746bf13666c513e4efec91a01`,
which exactly matches the canonical inventory's `verification_sha256`.

`trust-boundary.json` preserves all 13 canonical `source_rule_id` values once
each and in inventory order.

## Classification result

| Classification | Count |
|---|---:|
| `DEFINITION` | 13 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

All rules are `DEFINITION`:

- `decodeLoopBody` and `decodeFunctionBody` are macro equations expanding
  named proof terms to exact translated AST fragments. They do not match an
  execution configuration or add an observation to the Python model.
- The four `decodedResult` rules are the exhaustive base and recursive cases
  of the complete-group accumulator recurrence.
- The four `decodedTail` rules are the exhaustive base and recursive cases
  defining the final zero-to-two-code suffix.
- `decodeCodes` defines the overall mathematical summary by composing
  `decodedResult` and `decodedTail`.
- The two `finalLoopChar` rules define the exact final loop-target value by a
  structurally decreasing recurrence.

None of the rules matches a `<k>` cell or otherwise supplies ordinary language
execution or observation behavior, so the `OPERATIONAL_RULE` set is empty.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `/reference/k-proof/prove.sh` first compiles `verification.k`—with
all 13 canonical rules already present—into `verification-kompiled`, and then
runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

That command proves the reachability claims in `spec.k` under the already
compiled definitions. Stage 1 contains no earlier proof command against a
module omitting any canonical rule, and no later admission of an exactly
corresponding reusable rule. The loop claims are proof claims, not canonical
rules in this inventory. Consequently, no inventory entry satisfies the strict
ordering and exact-correspondence requirements for
`PROVED_DERIVED_LEMMA`.

The concrete tests, differential tests, and negative mutation probes in
`prove.sh` provide validation evidence but do not separately prove an inventory
rule.

## Domain lemmas

The domain-lemma set is empty.

No canonical rule states an additional algebraic, sequence, arithmetic, or
other mathematical fact beyond defining its own macro or summary symbol. In
particular, the finalized verification module contains no simplification
lemmas, associativity lemmas, identity lemmas, opaque result axioms, or
execution-bypassing rules.

## Resulting trust boundary

Within the canonical local verification-module closure, trust is limited to
the truthfulness and totality of the 13 definitional macro/recurrence equations.
No extra domain fact is trusted, no local operational rule extends the supplied
execution model, and no rule is credited as separately proved without the
required Stage 1 proof ordering.

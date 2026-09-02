# Trust-boundary discovery

## Canonical inventory

The launcher-generated `/reference/rule-inventory.json` is the exhaustive
source for this classification. It records:

- schema version: `2`
- verification module: `VERIFICATION`
- verification modules in the local closure: `VERIFICATION`
- inventory SHA-256:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- canonical rule count: `0`

Because the canonical `rules` array is empty, there are no
`source_rule_id` values to classify. `trust-boundary.json` therefore preserves
inventory order with an empty array and classifies every canonical rule exactly
once, vacuously.

## Classification result

| Classification | Count | Explanation |
|---|---:|---|
| `DEFINITION` | 0 | The canonical inventory contains no defining rule. |
| `OPERATIONAL_RULE` | 0 | The canonical inventory contains no operational rule. |
| `PROVED_DERIVED_LEMMA` | 0 | The canonical inventory contains no reusable rule with the required prior proof evidence. |
| `DOMAIN_LEMMA` | 0 | The canonical inventory contains no additional trusted mathematical fact. |

There are no inventoried rules carrying the `simplification` attribute, so the
requirement that every such rule be classified as `DEFINITION` or
`DOMAIN_LEMMA` is satisfied.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The mounted Stage 1 `prove.sh` compiles `verification.k`, proves the ten target
claims in `spec.k`, and runs two expected-failure validation probes. It does not
first prove the exact statement of a reusable rule against a module lacking
that rule and then build the target proof with the rule present. The target
claims and negative probes are not evidence for classifying any rule as
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty.

## Scope discipline

The mounted Stage 1 workspace contains rules in files outside the canonical
inventory, including the generated closure definition in `program.k` and the
supplied reference semantics. They were not added to the classification:
the task explicitly makes `/reference/rule-inventory.json` exhaustive and
canonical for the local verification-module closure. No theorem, Lean
statement, replacement rule, or alternative formulation was added to the JSON.

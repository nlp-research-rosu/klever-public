# Rule and lemma discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`, schema version 2,
with inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
Its `rules` array is empty and its local verification-module closure contains
only `VERIFICATION`.

The mounted `/reference/k-proof/verification.k` has the SHA-256 recorded by the
inventory. It only imports the supplied `MPY` semantics and declares no rules.
The imported fixed semantics is not added to this classification because the
launcher-generated canonical inventory contains no such `source_rule_id`
entries.

## Classifications

All zero canonical rules are represented exactly once, in inventory order, by
the empty `rules` array in `trust-boundary.json`.

| Classification | Count | Explanation |
|---|---:|---|
| `DEFINITION` | 0 | The canonical inventory contains no defining equations, recurrences, macros, or structural helpers. |
| `OPERATIONAL_RULE` | 0 | It contains no local execution or observation rules. |
| `PROVED_DERIVED_LEMMA` | 0 | It contains no reusable local rules and no rule has separate proof evidence. |
| `DOMAIN_LEMMA` | 0 | It contains no additional trusted mathematical facts. |

There are no simplification-attributed rules, so the special classification
constraint for such rules is satisfied vacuously.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `/reference/k-proof/prove.sh` compiles `verification.k` and proves the
single target claim in `spec.k`. It also runs two expected-failure mutation
probes. It does not first prove the exact statement of any reusable rule
against a module omitting that rule, and no reusable rule appears in the
canonical inventory. Therefore no entry qualifies as
`PROVED_DERIVED_LEMMA`.

## Domain-lemma set

The domain-lemma set is empty.

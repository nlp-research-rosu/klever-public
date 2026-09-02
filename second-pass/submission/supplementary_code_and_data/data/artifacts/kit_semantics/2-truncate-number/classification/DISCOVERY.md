# Trust-boundary rule discovery

## Canonical scope

The exhaustive source for this classification is
`/reference/rule-inventory.json`. It identifies schema version 2, inventory
SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
the verification module `VERIFICATION`, and an empty `rules` array.

The mounted `verification.k` corroborates that result: `VERIFICATION` only
imports the supplied `MPY` semantics and declares no local rules. Because the
canonical inventory is exhaustive, rules in the separately supplied reference
semantics are outside this local verification-rule classification.

## Classification result

There are zero canonical rules, so the complete per-class counts are:

| Classification | Count | Reason |
|---|---:|---|
| `DEFINITION` | 0 | No local equations, recurrences, macros, or structural helpers are inventoried. |
| `OPERATIONAL_RULE` | 0 | No local execution or observation rules are inventoried. |
| `PROVED_DERIVED_LEMMA` | 0 | No local reusable rules are inventoried, and Stage 1 contains no rule-first proof ordering. |
| `DOMAIN_LEMMA` | 0 | No additional local mathematical facts are inventoried. |

The empty `rules` array in `trust-boundary.json` therefore classifies every
canonical `source_rule_id` exactly once, preserves inventory order, and adds no
non-canonical entries. The restriction on rules carrying the
`simplification` attribute is vacuously satisfied because no canonical rule
has any attributes.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `prove.sh` compiles `verification.k` once and then proves the single
target module `SPEC`. It does not first prove an exact reusable rule against a
module lacking that rule and later rebuild the target definition with the rule
present. The two additional `kprove` commands are expected-failure
postcondition and body-mutation probes; neither establishes a reusable rule.
Consequently there is no Stage 1 proof evidence meeting the required ordering
and exact-correspondence test for `PROVED_DERIVED_LEMMA`.

## Domain-lemma set

The domain-lemma set is empty.

Stage 1 does document `floatMod` as a value-level trust boundary in the fixed
reference semantics. It is not a rule in the launcher-generated canonical
local inventory, so it is not added to or classified in
`trust-boundary.json`.

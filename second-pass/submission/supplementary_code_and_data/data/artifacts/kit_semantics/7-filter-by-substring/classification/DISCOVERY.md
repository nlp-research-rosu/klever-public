# Trust-boundary discovery

The canonical source is `/reference/rule-inventory.json`, with inventory hash
`2f18e093bb2959170b6ba00673e017fa9cb2ff9e0454b57a271bf5cbda4bf7ce`.
It contains eight rules, and `trust-boundary.json` preserves their inventory
order and classifies each `source_rule_id` exactly once.

## Classification summary

| Classification | Count |
|---|---:|
| `DEFINITION` | 7 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 1 |

The two `strCodes` rules are the constructor and default equations for a
proof-local total projection. The two `allStrVS` rules are the base and
structural recurrence for the proof's string-list domain predicate. The three
`filterAcc` rules are the base, contained-element, and excluded-element
equations defining the mathematical filter summary. These seven rules are
`DEFINITION`, including the two `filterAcc` recurrences carrying the
`simplification` attribute.

No canonical rule is classified as `OPERATIONAL_RULE`. The inventory contains
proof-local summary equations and one added simplification fact; it does not
list an ordinary source-language execution or observation rule.

## Domain lemma

The domain-lemma set is **not empty**. It contains exactly:

- `rule-ce7624945e06d02ae5606649e897ef6ded8e343e6c0ed28075613044c8e40503`
  — the guarded `applyCmp("in", str(P), V)` operand-normalization rule.

This rule has the `simplification` attribute and rewrites the already existing
`applyCmp` operation rather than defining a new proof-local summary symbol.
It is therefore an additional mathematical fact used by symbolic execution.
Under the allowed classifications, it is a `DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are **no separately proved derived lemmas** in the canonical inventory.

Stage 1's `prove.sh` first kompiles `verification.k`, which already contains
all eight inventoried rules, and only then invokes `kprove`. In particular,
`spec-value-check.k` begins with `requires "verification.k"` and imports
`VERIFICATION`, so its ground `strCodes` and membership checks are proved in a
module that already contains the guarded `applyCmp` simplification. Those
checks are useful validation evidence, but they neither prove the exact
inventoried rule nor establish the required proof-before-rule ordering against
a module that omits it.

Consequently, the Stage 1 comment and `PROOF.md` description calling the
normalization rule a “derived lemma” do not justify
`PROVED_DERIVED_LEMMA` under the classification contract for this stage.

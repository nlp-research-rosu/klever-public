# Trust-boundary discovery

The canonical source is `/reference/rule-inventory.json`, with inventory
SHA-256
`3a844e06bb98623cebec0bc8d33bff0ee48cd1eea0e9f7e65cb1d75248df894a`.
It contains two rules. `trust-boundary.json` preserves their inventory order
and classifies each `source_rule_id` exactly once.

## Classifications

| Inventory position | Source rule | Classification | Reason |
|---:|---|---|---|
| 0 | `rule-f119e21baa3b2f3f958217ae41d31a07cd861a77cd3db592e16dcd4824e16c2b` | `DEFINITION` | The rule expands the nullary `splitWordsBody` proof term into the exact Python-AST constructor sequence. This is a structural/macro definition; after expansion, the imported reference semantics performs execution. |
| 1 | `rule-fe0451a4b26ebe826c1c4ca94a4c96c37fda6ea9eb2e8665a649f842a712f5cb` | `DEFINITION` | The rule defines `oddAlphabetCount(CS)` by an unconditional equation whose right-hand side is the sum of the thirteen singleton-letter `cntSub` computations. It is a mathematical summary definition rather than an extra fact about a separately defined symbol. |

Neither inventory rule has the `simplification` attribute. Neither rule is an
ordinary execution/observation rule: `splitWordsBody` only names syntax, and
`oddAlphabetCount` only names a value expression. Therefore the
`OPERATIONAL_RULE` set is empty.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications.

The mounted Stage 1 `prove.sh` first compiles `verification.k` as module
`VERIFICATION`; that file already contains both canonical rules. It then proves
the target `spec.k` against that compiled definition. The vacuity probe uses
the same definition. The later mutation build compiles
`mutation-verification.k`, whose module imports `VERIFICATION`, so it also
contains both canonical rules.

Consequently, Stage 1 has no command that:

1. compiles a module excluding either canonical rule;
2. proves the exact statement of that excluded rule; and
3. only afterward admits the rule for the target proof.

The positive target proof and the two expected-failure mutation probes are
useful validation evidence, but they do not satisfy the required ordering and
exact-correspondence test for a separately proved derived lemma.

## Domain lemmas

The domain-lemma set is empty. Both canonical rules are definitional
expansions, and the inventory contains no additional trusted mathematical fact.

## Completeness check

- Canonical rule count: 2.
- Output rule count: 2.
- Duplicate `source_rule_id` values: none.
- Missing canonical rules: none.
- Extra rules: none.
- Inventory order preserved: yes.

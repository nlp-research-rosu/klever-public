# Trust-boundary discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`, with embedded
inventory digest:

```text
4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
```

Its `rules` array is empty and its local verification-module closure contains
only `VERIFICATION`. Accordingly, `trust-boundary.json` contains an empty
`rules` array. This classifies every canonical `source_rule_id` exactly once in
inventory order, vacuously, without adding rules imported from the fixed
reference semantics or treating the target reachability claim as an
inventoried rule.

## Classification results

| Classification | Count | Explanation |
|---|---:|---|
| `DEFINITION` | 0 | The canonical closure contains no defining equation, recurrence, macro rule, or structural helper. |
| `OPERATIONAL_RULE` | 0 | The canonical closure contains no local execution or observation rule. Operational behavior comes from the fixed imported `MPY` semantics, whose rules are absent from the canonical local inventory. |
| `PROVED_DERIVED_LEMMA` | 0 | No reusable rule is separately proved and then introduced. |
| `DOMAIN_LEMMA` | 0 | No additional mathematical rule is trusted to close the proof. |

There are no canonical rules carrying the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The mounted `verification.k` only imports `MPY` and declares no rules.
The mounted `prove.sh` compiles that import-only verification module and runs
`kprove` on `SPEC.multiply-correct`; it contains no earlier proof of an exact
reusable rule against a module omitting that rule. The Stage 1 `PROOF.md`
likewise records that there are no proof-local functions, equations,
simplification rules, ordinary rewrites, operational bridges, or auxiliary
claims. Thus no inventory entry qualifies as `PROVED_DERIVED_LEMMA`.

## Domain-lemma boundary

The domain-lemma set is empty. The finalized proof relies on the supplied
reference semantics and K's builtin theories, but it adds no inventoried
mathematical fact to the local verification-module closure.

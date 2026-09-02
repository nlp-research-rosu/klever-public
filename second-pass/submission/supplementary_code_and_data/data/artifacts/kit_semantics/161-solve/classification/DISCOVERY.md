# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`:

`8e830da1fd92fcf9ad97885fd223cc1c66ee296544b87724dddfa010b5d7117e`

It contains 14 rules, all of which are classified exactly once and in canonical
inventory order in `trust-boundary.json`.

## Classification summary

| Classification | Count | Basis |
|---|---:|---|
| `DEFINITION` | 13 | Two macro expansions and eleven equations/recurrences defining `charAlpha`, `alphaAcc`, `toggleAcc`, `lastChar`, and `solveResult`. |
| `OPERATIONAL_RULE` | 0 | The canonical local inventory contains no ordinary model-execution or observation rules. |
| `PROVED_DERIVED_LEMMA` | 0 | No reusable rule was first proved in `prove.sh` against a rule-free module before being admitted to the main verification definition. |
| `DOMAIN_LEMMA` | 1 | The one-character/nonempty constructor-disjointness simplification is an additional mathematical fact used by symbolic simplification. |

The rules marked `simplification` within the `alphaAcc` and `toggleAcc`
recurrences are `DEFINITION` because they are guarded defining equations, not
additional facts. The remaining simplification is classified as
`DOMAIN_LEMMA`.

## Separately proved statement and ordering evidence

The only inventory rule with separate Stage 1 proof evidence is:

`rule-387d11f8474864387ce45c90f1ba7bc44da2dcb0e552a8b7845434062e527a49`

Its exact constructor-disjointness content appears in
`lemma-spec.k` as claim `one-char-is-not-empty`. The claim imports
`LEMMA-VERIFICATION`, whose module imports only the supplied `MPY` semantics and
does not contain the inventory rule. Stage 1 records `#Top` with exit 0 and
`WarnTrivialClaim` for this claim.

However, the ordering in Stage 1 `prove.sh` is:

1. lines 14–17 compile `verification.k`, which already contains the
   simplification rule;
2. lines 19–21 run the main `spec.k` proof using that definition; and only then
3. lines 23–30 compile the rule-free lemma definition and prove
   `lemma-spec.k`.

Therefore the rule was separately proved, but it was not **first proved**
before admission and use. It does not qualify as `PROVED_DERIVED_LEMMA` under
the required ordering criterion. Its canonical classification is
`DOMAIN_LEMMA`.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly the single
constructor-disjointness rule identified above. No other canonical inventory
rule is a domain lemma.

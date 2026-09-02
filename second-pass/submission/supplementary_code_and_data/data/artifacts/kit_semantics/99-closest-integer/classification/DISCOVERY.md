# Trust-boundary discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`. It identifies
`VERIFICATION` as the local verification module, records inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and contains an empty `rules` array.

There are therefore zero canonical `source_rule_id` values to classify. The
output `rules` array is empty, so every canonical rule is represented exactly
once in inventory order.

## Classification results

| Classification | Count | Explanation |
|---|---:|---|
| `DEFINITION` | 0 | The canonical verification-module closure contains no defining equations, recurrences, macro expansions, or structural helper rules. |
| `OPERATIONAL_RULE` | 0 | It contains no local execution or observation rules. |
| `PROVED_DERIVED_LEMMA` | 0 | It contains no reusable local rules and hence no candidate derived lemmas. |
| `DOMAIN_LEMMA` | 0 | It contains no additional trusted mathematical rules. |

No canonical rule carries the `simplification` attribute.

## Stage 1 corroboration

The mounted `/reference/k-proof/verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It adds no local rules. The mounted `prove.sh` compiles that module and proves
the claims in `spec.k`; it contains no preliminary proof of a reusable rule
against a rule-free module followed by installation of the exact proved rule.
The claims in `spec.k` are reachability claims, not entries in the canonical
local-rule inventory.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Consequently there is no Stage
1 rule-free derivation and exact rule-correspondence evidence to cite.

## Domain lemmas

The domain-lemma set is empty.

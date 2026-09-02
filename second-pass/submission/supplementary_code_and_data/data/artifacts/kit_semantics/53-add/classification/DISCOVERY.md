# Trust-boundary rule discovery

## Canonical inventory

The launcher-generated `/reference/rule-inventory.json` is treated as the
exhaustive inventory of rules in the local verification-module closure. It
records:

- schema version: `2`
- inventory SHA-256:
  `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- verification module: `VERIFICATION`
- canonical rule count: `0`

Accordingly, `trust-boundary.json` contains an empty `rules` array. This
classifies every canonical rule exactly once, in inventory order: there are no
canonical rule entries to classify.

## Classification results

| Classification | Count | Explanation |
|---|---:|---|
| `DEFINITION` | 0 | The local verification closure contains no equations, recurrences, macro expansions, or structural proof helpers. |
| `OPERATIONAL_RULE` | 0 | The canonical inventory contains no local execution or observation rules. |
| `PROVED_DERIVED_LEMMA` | 0 | No reusable local rule was separately proved before being added to a proof module. |
| `DOMAIN_LEMMA` | 0 | No additional trusted mathematical fact occurs as a local rule. |

There are also no canonical rules carrying the `simplification` attribute, so
the special `DEFINITION`-or-`DOMAIN_LEMMA` constraint is vacuous.

## Stage 1 evidence

The mounted `/reference/k-proof/verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It declares no rule, equation, simplification rule, macro, helper, or auxiliary
claim. This agrees with the canonical empty inventory.

The mounted `/reference/k-proof/prove.sh` compiles that extension-free
verification module, proves the target claim in `spec.k`, and runs two expected
failure mutation probes. It has no earlier `kprove` phase that proves the exact
statement of a reusable rule against a module lacking that rule.

Therefore, the set of separately proved derived lemmas is **empty**. There is
no Stage 1 proof evidence for any `PROVED_DERIVED_LEMMA` because no such local
rule exists. The target reachability claim in `spec.k` is not a rule in the
canonical inventory and is not reclassified as a derived lemma.

The domain-lemma set is explicitly **empty**.

## Boundary interpretation

The supplied `MPY` semantics contains operational and definitional rules, but
the launcher did not include those rules in the canonical local
verification-module inventory. Per the benchmark instruction that the
launcher inventory is exhaustive and canonical, this discovery does not add,
copy, or independently enumerate imported reference-semantics rules.

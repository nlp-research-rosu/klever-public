# Trust-boundary discovery

## Canonical scope

The sole classification source is
`/reference/rule-inventory.json`, with inventory SHA-256
`c38d770ae0a9652b812217694490b3b0706fee0fe43a7d38653391e673572a78`.
It contains 19 rules, in order, from the canonical verification-module closure
`MAX-FILL-SUMMARY`. `trust-boundary.json` preserves that order and classifies
each canonical `source_rule_id` exactly once.

Classification counts are:

- `DEFINITION`: 18
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 1

## Classification reasoning

The projection, predicate, fold-summary, cost-summary, and loop-target rules
are equations or structurally descending recurrences that define named proof
terms:

- `definedProjectInt`, the guarded orientations and collapse equations for
  `projectInt`, `rowVals`, and `isListVal`;
- the base and recursive equations of `allBinary` and `allRows`;
- the base and recursive equations of `rowSum`, `gridCost`, and `finalRow`;
- the disjoint positive and nonpositive defining cases of `bucketCost`.

These 18 rules are `DEFINITION`. This includes the five simplification rules
that orient or collapse the named projection terms: they define those proof
terms rather than state independently established reusable facts.

No canonical rule rewrites a `<k>` execution configuration or adds an
observation rule to the verification model, so the canonical inventory has no
`OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules in the canonical inventory.

Stage 1 did separately prove two connection claims:

1. `fixed-int-of` at
   `/reference/k-proof/connection-spec.k:9`, whose statement is
   `intOf(I:Int) => I`.
2. `fixed-sum-dispatch` at
   `/reference/k-proof/connection-spec.k:12`, whose statement is the fixed
   `#applyK` transition for an argument already shaped as `list(VS)`.

The proof ordering is recorded at
`/reference/k-proof/prove.sh:36`: it first compiles
`MAX-FILL-SUMMARY` as `connection-kompiled`, then runs `kprove` on
`connection-spec.k` at line 40. The run prints `#Top` in
`/reference/k-proof/prove.log:285`.

Neither connection claim exactly corresponds to any canonical inventory rule.
The downstream generalized `intOf` and `sum` dispatch twins occur only in
`MAX-FILL-VERIFICATION` at
`/reference/k-proof/verification.k:81` and line 88, respectively; that module
is outside the canonical inventory. Their statements also differ from the two
connection claims. Consequently, the Stage 1 connection evidence does not
permit any of the 19 canonical rules to be labeled
`PROVED_DERIVED_LEMMA`. In particular, comments calling projection rules
“lemmas” are not proof evidence, and every canonical simplification rule is
classified only as `DEFINITION` or `DOMAIN_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`,
  the simplification rule characterizing
  `#Ceil({V:Val}:>Int)` as the conjunction of `definedProjectInt(V)` and
  `#Ceil(V)`.

This rule states an additional fact about the definedness domain of K's
built-in partial cast. It is present in `MAX-FILL-SUMMARY` before the Stage 1
connection claims are proved, and no bridge-free Stage 1 command first proves
its exact statement. It is therefore a trusted `DOMAIN_LEMMA`, not a proved
derived lemma.

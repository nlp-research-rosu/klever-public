# Trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` contains 42 rules
in `VERIFICATION-BASE` and reports inventory SHA-256
`009e8ed17e488802f3e2dd33c4513a337ffb64265a0cd9ad1aefcef93e2f9c86`.
`trust-boundary.json` preserves that order and classifies each canonical
`source_rule_id` exactly once.

## Classification summary

| Classification | Count | Meaning in this inventory |
|---|---:|---|
| `DEFINITION` | 38 | Structural encodings and predicates, exact AST macros, and equations or recurrences defining proof summaries |
| `OPERATIONAL_RULE` | 0 | The canonical local closure contains no added ordinary execution or observation rule |
| `PROVED_DERIVED_LEMMA` | 0 | No reusable rule is first proved against a module that excludes it |
| `DOMAIN_LEMMA` | 4 | Unproved no-confusion/inversion facts for the `numVals` embedding |

All 22 rules carrying the `simplification` attribute obey the required
restriction: 18 are classified `DEFINITION`, and 4 are classified
`DOMAIN_LEMMA`.

## Definitions

The following groups are definitions rather than additional mathematical
facts:

- `numVals`, `numLen`, `lastNonZero`, and `validCoeffs` define the symbolic
  coefficient representation and its precondition.
- `polyStep`, `polyBody`, `expandCond`, `expandBody`, `bisectCond`,
  `bisectBody`, `findZeroBody`, and `solutionModule` are named macro expansions
  for exact translated MPY syntax.
- `polyAcc`, `polyValue`, `polyPower`, and `polyLast` define structural
  polynomial-loop summaries.
- `bracketBegin` and `bracketEnd` define the two projections of the expansion
  loop's endpoint pair.
- `bisectFrom` defines the guarded bisection recurrence, and `solveFrom`
  defines its composition with the endpoint summaries.

The Stage 1 reachability claims connect several of these summaries to program
execution, but that connection does not change the recurrence equations
themselves from definitions into separately proved reusable lemmas.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly these four
`simplification` rules:

1. `rule-0dfb3ea463a2e10ce61e8445bcf95e2aa2d4748b432b47ccd1f9825f8cca2630`
   — inversion of `numVals(NS) = .ValSeq`.
2. `rule-f684bfbef1c0219f754e562f1888c8a1b7236498affdcf8c5681f52ef8e6175f`
   — injectivity of `numVals`.
3. `rule-4f3a4fc13d02a156f3a8d695f13fdac54badb56cceabf4cbe100c7ea4aca4d57`
   — inversion of an integer-headed embedded sequence.
4. `rule-f2662dddafe1054c19c3ddaf31b8c9e9a8971c2baafdf6d7f8bfb1785b1ff321`
   — inversion of a float-headed embedded sequence.

These are plausible constructor no-confusion consequences, but the requested
classification depends on mounted proof evidence, not plausibility. Stage 1
does not first prove their exact statements in a module without them.
Consequently they are trusted mathematical facts for this classification.

## Separately proved derived lemmas

There are **no separately proved derived lemmas** in the canonical rule
inventory.

The ordering in `/reference/k-proof/prove.sh` is decisive:

```text
kompile verification.k --main-module VERIFICATION-BASE ...
kprove spec.k --definition verification-base-kompiled ...
```

The `kompile` command includes all 42 inventory rules before any of the five
positive `kprove` commands. Every positive proof therefore runs against a
definition already containing the four inversion/injectivity
simplifications. There is no compilation of a module excluding one of those
rules, no prior `kprove` of any rule's exact statement, and no later
installation of a proved rule.

The claims `poly-loop-empty`, `poly-loop-int`, `poly-loop-float`,
`expand-loop`, `bisect-head`, `bisect-loop`, `find-load`, and `find-init` are
proved reachability claims in `spec.k`. They are not rules in the canonical
inventory and do not establish the required proof-before-installation ordering
for any inventory rule. In particular, the Stage 1 report's informal
description of the four `numVals` simplifications as “derived lemmas” is not
sufficient for the stricter `PROVED_DERIVED_LEMMA` classification requested
here.

## Operational rules

No canonical rule is classified `OPERATIONAL_RULE`. The inventory is limited
to the local verification-module rules: its source-program terms are exact
macros, while the execution rules themselves come from the supplied MPY
semantics and do not appear among these 42 canonical entries.

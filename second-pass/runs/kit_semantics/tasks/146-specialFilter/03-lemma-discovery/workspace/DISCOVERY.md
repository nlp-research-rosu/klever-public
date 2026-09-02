# Trust-boundary discovery

## Inventory basis

The sole classification source is the launcher-generated
`/reference/rule-inventory.json`. Its canonical `inventory_sha256` is
`12d01103d80c6a489390efcbe9d1f159bccf941a293215593306572eb7a48336`.
It contains 23 unique rules, all in the local `VERIFICATION` module. The output
preserves that inventory order and includes every `source_rule_id` exactly
once.

The classification totals are:

- `DEFINITION`: 19
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 4

All 13 rules carrying a `simplification` or `simplification(10)` attribute are
classified as either `DEFINITION` or `DOMAIN_LEMMA`.

## Definitions

The following families are definitions because they introduce exact macro
expansions, structural predicates, named proof terms, or mathematical
recurrences:

- `filterBody()` and `specialFilterStmts()` expand named syntax matching the
  translated program.
- The two `allInts` equations define the admissible sequence predicate.
- `definedProjectInt` defines the projection guard.
- The guarded `projectIntTotal(V) => {V}:>Int` equation, the Int collapse, and
  idempotence define and normalize the fresh `projectIntTotal` proof term.
- `firstDecimalCode`, `lastDecimalCode`, `firstDigitOdd`, `lastDigitOdd`, and
  `isSpecial` define the per-integer mathematical summaries.
- The six `specialCount` equations are the base and disjoint recursive cases
  of the aggregate mathematical summary.

The `simplification` attribute does not change the classification of the
projection normalization or `specialCount` recurrences: their left-hand sides
are fresh named proof terms whose values those equations define.

## Domain lemmas

The domain-lemma set is **not empty**. It consists of exactly four rules:

1. `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
   characterizes `#Ceil` of the pre-existing partial `Val :> Int` cast.
2. `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d`
   adds the reverse simplification orientation from that pre-existing cast to
   `projectIntTotal`.
3. `rule-b16fd6610afeba9b173c4b9ae74c4766789b5284e03220a93a65bb86fd2ce505`
   adds the guarded dynamic-`Val` simplification twin for `applyCmp(">")`.
4. `rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d`
   adds the guarded dynamic-`Val` simplification twin for
   `applyBuiltin("str")`.

These rules simplify pre-existing logical or semantic symbols rather than only
defining a fresh summary. They are material to symbolic sort refinement. Since
they carry `simplification`, they cannot be classified as operational rules;
and because Stage 1 supplies no qualifying prior proof, they remain trusted
domain lemmas.

## Operational rules

The canonical local closure contains no `OPERATIONAL_RULE`. In particular, the
two rules mentioning `applyCmp` and `applyBuiltin` are simplification axioms,
so the explicit classification constraint routes them to `DOMAIN_LEMMA`
rather than `OPERATIONAL_RULE`. The inventory contains no ordinary local
`<k>`-cell execution or observation rule.

## Separately proved derived lemmas

There are **no separately proved derived lemmas**.

Stage 1's `prove.sh` first compiles the complete `verification.k`, containing
all 23 canonical rules, into `verification-kompiled`. It then runs the positive
`kprove spec.k` command and the negative probes against that already extended
definition. It never:

1. constructs a module that omits one of the candidate rules;
2. proves that candidate rule's exact statement against the rule-free module;
   and then
3. recompiles or imports the proved statement for the target proof.

The `#Top` result for `spec.k`, the loop circularity, concrete smoke tests,
differential tests, and expected-failure mutations validate the target proof
and provide empirical sensitivity evidence, but none establishes the required
prove-before-import ordering for a `PROVED_DERIVED_LEMMA`. Comments in
`verification.k` and the Stage 1 narrative calling projection or dispatch
rules “derived” therefore do not alter their classification.

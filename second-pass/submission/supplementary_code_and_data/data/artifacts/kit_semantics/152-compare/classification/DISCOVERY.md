# Trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` has schema version
2, inventory SHA-256
`d8bd26fb5a8a3ab592d3a04b2906a8b05d6f56ff89b9a6ba116f3876d9a6e5b8`,
and five rules. All five rules are in module `VERIFICATION`; none carries the
`simplification` attribute.

## Classification result

All five canonical rules are classified as `DEFINITION`:

- `rule-29a9419a5013224a8657110320f5222d8360897d1c1ad05d5b21b9a8a070d15a`
  is the left-empty equation for the newly named `sameIntLists` structural
  predicate.
- `rule-4c226b697298ea8f665e9c7a275c999f5ca1704cf1bffeda3ab4c575a950d681`
  is its nonempty/empty mismatch equation.
- `rule-23a1b598b8aca7e64fdbbbdf6c2eba606e3434ffea5d8b33eb5ff9c67a39d82f`
  is its recursive nonempty/nonempty equation. The integer and non-reference
  conjuncts are part of the definition of this newly introduced domain
  predicate; the rule does not rewrite an existing mathematical proposition.
- `rule-35d6b10b3b07c6654b6990fa450ff659514b515f9afb5c4ddcd292c7a52a4d4e`
  is the base equation for the newly named `compareAcc` result summary.
- `rule-b6a35c28b2d565d80431890d82ed0b37f41b8e521dd15d430123581b67f0d014`
  is the recursive `compareAcc` equation. It defines the summary by appending
  the supplied-semantics term for the current absolute difference and
  descending on both input tails.

These rules define proof terms and do not match operational cells or replace
program execution, so no canonical rule is an `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no separately proved derived rules.

The Stage 1 `/reference/k-proof/prove.sh` compiles `verification.k` directly,
with all five inventory rules already present, and then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

`/reference/k-proof/prove.log` records `#Top` for that complete proof
definition. It does not record a prior proof of any inventory rule's exact
statement against a module that excludes that rule. Consequently none of the
five rules meets the required ordering for `PROVED_DERIVED_LEMMA`, regardless
of descriptive language elsewhere in Stage 1.

The `compare-loop-step` item described as a derived reachability
lemma/circularity in Stage 1 `PROOF.md` is a claim in `spec.k`, not a rule in
the canonical rule inventory, and therefore is not an entry in
`trust-boundary.json`.

## Domain lemmas

The domain-lemma set is empty. No canonical rule states an additional trusted
mathematical fact used to close the proof; the inventory consists solely of
the defining cases for `sameIntLists` and `compareAcc`.

## Completeness

`trust-boundary.json` preserves canonical inventory order and contains each of
the five `source_rule_id` values exactly once. It contains no theorem,
replacement statement, Lean content, or alternative formulation.

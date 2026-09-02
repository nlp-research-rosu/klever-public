# Trust-boundary discovery

## Canonical inventory result

`/reference/rule-inventory.json` is the exhaustive inventory specified by the
launcher. It identifies schema version 2, inventory digest
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
the local verification module `VERIFICATION`, and an empty canonical `rules`
array.

Accordingly, `trust-boundary.json` contains an empty `rules` array. This
classifies every canonical rule exactly once in inventory order: there are zero
canonical rules to classify.

## Classification counts

- `DEFINITION`: 0
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The domain-lemma set is explicitly **empty**.

## Stage 1 evidence

The mounted `/reference/k-proof/verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It declares no rules, equations, recurrences, macros, simplification rules, or
other proof-local helpers. This agrees with the canonical inventory.

`/reference/k-proof/spec.k` contains the target reachability claim
`SPEC.is-palindrome`. A claim is not a rule listed by the canonical inventory,
so it is not added to or reformulated in `trust-boundary.json`.

The imported `MPY` reference semantics and generated backend rules are also not
added: the launcher-provided inventory is authoritative and names only the
local `VERIFICATION` closure represented by its empty `rules` array.

## Separately proved derived lemmas

There are **no separately proved derived lemmas**.

Stage 1's `/reference/k-proof/prove.sh` compiles `VERIFICATION` and proves
`spec.k`, while `/reference/k-proof/prove-run.out` records the target proof's
`#Top` result and the expected failures of two validation mutations. It does
not first prove the exact statement of any reusable rule against a module that
omits that rule, and `verification.k` contains no candidate reusable rule.
Therefore no item qualifies as `PROVED_DERIVED_LEMMA`.

## Simplification-rule constraint

The canonical inventory contains no rule carrying the `simplification`
attribute. The requirement that every such rule be classified only as
`DEFINITION` or `DOMAIN_LEMMA` is therefore satisfied vacuously.

The Stage 1 mount was inspected read-only; no Stage 1 artifact was edited or
copied.

# Trust-boundary classification

The canonical inventory contains 12 rules, all in the `VERIFICATION` module. Each rule is classified exactly once in `trust-boundary.json`, in canonical inventory order.

## Definitions

The first three rules are structural definitions for named proof terms:

- `loopBody` expands to the constructor AST of the loop body.
- `solutionBody` expands to the constructor sequence of the function body.
- `theSolution` expands to the module containing the target function.

The remaining nine rules are the complete defining equations of `scan(Int, BString)`. The empty-string equation is its base case, and the other eight equations give the recurrence for states 0 through 3 on `lbr` and `rbr`. Together they define the mathematical reference automaton used by the claims. They do not assert facts beyond that definition.

Accordingly, all 12 inventory rules are `DEFINITION`. There are no `OPERATIONAL_RULE` entries in the canonical inventory; execution rules live outside the launcher-declared verification-module inventory and are not added to this classification.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `prove.sh` first compiles `verification.k` with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX
```

It then proves the claims in `spec.k` against that already-compiled definition:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Thus every inventoried rule is already present in the proof definition. Stage 1 contains no earlier proof of any inventoried rule's exact statement against a module that omits that rule, so no rule meets the required `PROVED_DERIVED_LEMMA` ordering criterion. The four loop-invariant claims and the end-to-end claim in `spec.k` are proof claims, not rules in the canonical inventory.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule is an additional trusted mathematical fact used to close the proof; the mathematical `scan` rules are its defining recurrence.

No inventoried rule carries the `simplification` attribute.

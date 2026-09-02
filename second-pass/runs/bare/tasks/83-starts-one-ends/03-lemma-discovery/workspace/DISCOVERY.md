# Trust-boundary discovery

The canonical inventory identifies six rules, all from the `VERIFICATION` module. Each rule is classified as `DEFINITION` because it is an equation defining a named mathematical summary used by the specification:

- `decimalMiddles(K)` abbreviates the number of assignments to `K` decimal positions as `10 ^Int K`.
- `startsWithOne(N)`, `endsWithOne(N)`, and `startsAndEndsWithOne(N)` define the three component counts for the inclusion-exclusion calculation when `N > 1`.
- `qualifyingCount(1)` defines the one-digit base case.
- `qualifyingCount(N)` defines the multi-digit result as the start count plus the end count minus their overlap.

These are specification equations for newly introduced summary functions. They are not execution or observation transitions, so no canonical rule is an `OPERATIONAL_RULE`. The canonical entries have empty attribute lists, so none carries the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` first compiles `verification.k` as module `VERIFICATION`; that file already contains all six inventory rules. It then runs `kprove spec.k --definition verification-kompiled`. The saved `proof-output.txt` ends in `#Top`, establishing the two program-correctness claims relative to the already-compiled definitions. It does not show any inventory rule's exact statement being proved first against a module from which that rule is absent, so none meets the required admission ordering.

## Domain lemmas

The domain-lemma set is empty. No canonical rule states an additional trusted fact about pre-existing mathematical operations; the counting content is introduced through the named specification definitions above.

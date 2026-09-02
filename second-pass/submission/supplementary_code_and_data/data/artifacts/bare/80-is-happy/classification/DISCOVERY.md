# Trust-boundary discovery

The canonical inventory hash is `e04c1af4b26723a5714f4f85dc6110990a90f9cef9e8a9a8821d48c8f3ac92f9`. Its ten rules are all from the `VERIFICATION` module, and every one is classified exactly once in inventory order.

## Classification basis

All ten rules are `DEFINITION`:

- `#distinct3` is a named mathematical-summary equation expanding pairwise distinctness into three comparisons.
- The four `#allTriples` rules are the three base cases and recursive case of one recurrence over the inductive string representation.
- The four `#happy` rules define the three short-string cases and the length-at-least-three case of the prompt predicate.
- `#solution` expands a named proof term into the exact constructor tree used by the claims.

These rules define functions or proof syntax. They are not ordinary execution/observation transitions, so the inventory contains no `OPERATIONAL_RULE` entries. The execution rules used by Stage 1 reside in `semantic.k`, outside the canonical inventory's listed local verification modules.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence in `prove.sh` first compiles `verification.k` with all ten inventoried rules already present, and then runs the single command `kprove spec.k --definition verification-kompiled`. That command proves the claims in `spec.k`; it does not first prove the exact statement of any inventoried rule against a module omitting that rule and later add the rule. Consequently, none meets the required ordering or exact-correspondence test for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule adds a separate mathematical fact beyond the defining equations and proof-term expansion described above, and none carries the `simplification` attribute.

# Trust-boundary discovery

The canonical inventory hash is
`47dc6902f30db03423bbce78fba305f79eeb2082c170535707b55aa35d51303d`.
The inventory contains two rules, both from `VERIFICATION`, and neither rule
carries the `simplification` attribute.

## Classifications

1. `rule-259271eac22df31da5442025e304bd2f6d2ba0dd1b9a82b0d0000ac062b8f3cd`
   is a `DEFINITION`. Its left-hand side is the named structural helper
   `startsOneEndsBody`; its right-hand side expands that helper to the
   translated statement sequence for the finalized implementation. This is a
   definition of the proof term used in the initial function closure, not an
   additional mathematical fact.

2. `rule-565589a3e4823e29c1250cdf77d45455a605950437a4a7c40cbe97ef94b43c69`
   is an `OPERATIONAL_RULE`. It rewrites the harness command
   `#invokeStartsOneEnds(N)` to the model-level call of `starts_one_ends` with
   `N`. This connects each claim to ordinary execution under the supplied
   Python semantics.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules. Stage 1's `prove.sh` compiles
`verification.k` and then proves the claims in `spec.k` against that compiled
definition. It does not first prove the exact statement of either inventoried
rule against a module from which that rule is absent. Consequently, the Stage
1 ordering and exact-correspondence requirement for a separately proved
derived lemma is not met by either rule.

## Domain lemmas

The domain-lemma set is empty. Neither inventoried rule asserts an additional
mathematical fact used to close the proof: one defines the embedded program
body and the other performs verification-model invocation.

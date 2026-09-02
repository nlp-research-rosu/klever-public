# Trust-boundary discovery

The canonical inventory contains three rules, all from `VERIFICATION`.

The rule defining `sumFourPositiveEvens(N)` is classified as `DEFINITION`.
It introduces the named contract summary by expanding it to the arithmetic
condition `N >= 8` and `N % 2 == 0`.

The rule defining `canonicalWitnessesAreValid(N)` is also classified as
`DEFINITION`. It expands a named proof term into the checks that the canonical
four summands `N - 6, 2, 2, 2` are positive and even and sum to `N`.

The `checkCanonicalWitnesses(N)` cell rewrite is classified as
`OPERATIONAL_RULE`. It is an execution/observation step in the verification
model: the command is removed from `<k>`, and its Boolean observation is placed
in `<result>`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules. Stage 1's `prove.sh` first compiles
`verification.k` as the `VERIFICATION` definition and then runs `kprove`
against that compiled definition. Consequently, every inventoried rule is
already present in the proof definition. Although `spec.k` proves claims about
the contract and canonical witnesses, the Stage 1 evidence does not first
prove the exact statement of any inventoried reusable rule against a module
that omits that rule.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule is an additional trusted
mathematical fact used to close the proof.

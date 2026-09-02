# Trust-boundary classification

The exhaustive canonical inventory contains two rules, both from the
`VERIFICATION` module:

- `rule-84a0db9c987c24ad93dcfb91a4deaa38c9077791aa141b3417212a69f3dcf48c`
  is `DEFINITION` because it gives the base-case equation for the named
  mathematical summary `fibMath`.
- `rule-da5d86dd353aec918d6e03a13c4d58e6661da94353a37d075cd57cb69d879e4d`
  is `DEFINITION` because it gives the recursive equation for `fibMath`.

Neither rule is an `OPERATIONAL_RULE`: both define the mathematical summary
used as the proof result rather than a program-execution transition. Neither
is a `DOMAIN_LEMMA`: no additional mathematical fact appears in the canonical
inventory.

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1 `prove.sh` compiles
`verification.k`, including both inventoried rules, before running any proof.
Its first positive `kprove` command separately proves the `SPEC.fib-invoke`
claim from `spec.k`; that claim is not an inventoried rule, and there is no
evidence of either inventoried rule first being proved against a module that
omits it.

The domain-lemma set is empty.

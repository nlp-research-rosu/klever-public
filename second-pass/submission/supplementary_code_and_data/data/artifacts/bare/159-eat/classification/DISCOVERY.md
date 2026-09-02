# Trust-boundary discovery

The canonical inventory contains four rules, in `VERIFICATION`, and each is a
definition:

- The two `carrotContract` rules are the disjoint sufficient-stock and
  insufficient-stock equations defining the named mathematical summary used
  on the right-hand side of the symbolic claims.
- The `validInput` rule defines the named input predicate by expanding it to
  the three ranges stated in the prompt.
- The `solutionProgram` rule is a structural helper that defines the named
  proof term as the exact constructor tree represented by `solution.mpy`.

None of these rules is an operational execution rule. Execution is supplied by
the separate `SEMANTIC` module, whose rules are not entries in the canonical
verification-module inventory.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` first runs
`kompile verification.k --main-module VERIFICATION`, which places all four
inventory rules in `verification-kompiled`, and only afterward runs
`kprove spec.k --definition verification-kompiled`. Thus Stage 1 contains no
proof in a module that omits one of these rules and then establishes that
rule's exact statement before reuse. The claims in `spec.k` prove program
behavior against the already-defined contract; they do not separately derive
an inventory rule.

## Domain lemmas

The domain-lemma set is empty. No inventory rule asserts an additional
mathematical fact used to close the proof; all four only define named summaries
or proof terms.

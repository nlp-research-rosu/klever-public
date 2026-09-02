# Trust-boundary classification

The canonical inventory contains five rules, all in `VERIFICATION`, and all
five are classified as `DEFINITION`.

The first three rules are the exhaustive conditional equations of the
`lpfSpec(N, F)` mathematical recurrence:

1. return `N` when `F * F > N`;
2. divide `N` by `F` and recur when `F` divides `N`; and
3. advance `F` and recur when `F` does not divide `N`.

These equations define the mathematical summary against which execution is
verified; they do not assert additional facts about an independently defined
summary.

The other two rules are macro expansions. `factorLoop` defines a named proof
term for the translated loop AST, and `solutionModule` defines a named proof
term for the complete translated function AST. They are structural
definitions, not operational execution rules.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` first compiles
the complete `verification.k`, already containing all five inventoried rules,
and then runs one `kprove` command over `spec.k`. It does not first prove the
exact statement of any inventoried rule against a module from which that rule
is absent. Therefore none satisfies the required proof-before-inclusion
ordering.

The `OPERATIONAL_RULE` set is empty because the canonical inventory contains
only the summary recurrence and named AST macros; execution rules reside
outside the inventoried verification-module set.

The `DOMAIN_LEMMA` set is explicitly empty. No inventoried rule is an
additional trusted mathematical fact used to close the proof.

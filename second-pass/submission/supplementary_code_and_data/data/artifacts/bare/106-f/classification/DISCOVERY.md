# Trust-boundary discovery

The canonical inventory hash is
`dd2b2a30dbe254268b8c8164d328afa35d11a8baab4cb1187bcd9ade25c58863`.
The inventory contains 12 rules, all from the `VERIFICATION` module. Every
inventory rule is classified exactly once and in canonical inventory order in
`trust-boundary.json`.

## Definitions

All 12 rules are `DEFINITION`:

- The two `mathFactorial` rules define its zero case and positive recurrence.
- The two `mathTriangle` rules define its zero case and positive recurrence.
- The two `expectedAt` rules define the even-index factorial case and the
  odd-index triangular-sum case.
- The `expected` rule initializes the expected-list summary.
- The three `expectedCompletion` rules define its terminating, even-index, and
  odd-index cases.
- `solutionLoop` and `solution` are macro expansions defining named proof
  terms for the translated loop and complete program AST.

These are equations, recurrences, or macro expansions. They do not assert
additional mathematical facts beyond the meanings assigned to their named
symbols.

## Operational rules

The canonical inventory contains no `OPERATIONAL_RULE` entries. The execution
rules in `semantic.k` are part of the imported `SEMANTIC` module, but they are
not entries in the launcher-generated canonical inventory, whose listed
verification-module set is only `VERIFICATION`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1's `prove.sh` first compiles `verification.k` as module
`VERIFICATION`, which already contains every one of the 12 inventoried rules.
It then invokes `kprove` on `spec.k`. That invocation proves the
`loop-invariant` and `main-correct` claims, but neither claim is an inventoried
reusable rule. No Stage 1 command first proves the exact statement of any
inventoried rule against a module from which that rule is absent.

The `diff` command in `prove.sh` establishes that the `solution` macro expands
to the same KORE AST as `solution.mpy`; it is a structural equality check, not
a proof that turns either macro rule into a proved derived lemma.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule is classified as
`DOMAIN_LEMMA`, and the inventory contains no rule carrying the
`simplification` attribute.

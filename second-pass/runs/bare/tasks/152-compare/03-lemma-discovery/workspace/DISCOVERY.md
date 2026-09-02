# Trust-boundary discovery

The canonical inventory hash is
`420faefde3ec2d8bbe14ddc4b8e7750c06010ddc67a860e683a4c930fdcc1036`.
It contains four rules, and each is classified exactly once in inventory
order in `trust-boundary.json`.

## Definitions

`rule-1a31d186612bdc6749d37d6c3da77977158f53c4e73aacb83ebba762c6f45847`
is the expansion of the named `solutionProgram` term into the constructor AST
recorded in `solution.mpy`. It defines which program the claim executes.

The other three rules are the exhaustive cases used to define the
mathematical summary `expected`:

- `rule-ae62c27ad3424040225a1c94838f791abd610e6519a372c5656fbe1ebabf000e`
  is the empty-list base case.
- `rule-a4545b542cd0f8ff08024b166bf6bd722fa870b2dc67958768c7594c623b6919`
  is the recursive negative-difference case.
- `rule-0b6e8a0b23d3e6470229df58b00bdcac1c3030a0cc6c9fca317f8aae915af200`
  is the recursive nonnegative-difference case.

These are equations and recurrences defining named proof terms. They are not
ordinary execution transitions, and their use does not assert a separate
mathematical fact beyond the chosen definition of the expected-output summary.
Accordingly, all four inventory entries are `DEFINITION`; there are no
`OPERATIONAL_RULE` entries in this canonical inventory.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` with
`--main-module VERIFICATION`, so all four inventoried rules are already in the
proof definition. It then invokes:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

That command proves the final reachability claim in `SPEC`; it does not first
prove any inventoried rule against a module lacking that rule. No earlier
`kprove` command, separate lemma specification, proof artifact, or ordering
evidence establishes an exact inventoried rule before adding it to
`VERIFICATION`. Thus no rule satisfies the required
`PROVED_DERIVED_LEMMA` evidence standard.

## Domain lemmas

The domain-lemma set is empty. None of the inventoried rules is an additional
trusted mathematical fact used to close the proof, and none carries the
`simplification` attribute.

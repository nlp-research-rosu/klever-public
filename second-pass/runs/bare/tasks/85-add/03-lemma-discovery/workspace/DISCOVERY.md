# Trust-boundary discovery

The canonical inventory has SHA-256
`79de0306317a61b82b483fed021938b7146250da18ba1985f791f21447f3fbc0`
and contains four rules, all from the `VERIFICATION` module. The
classification follows that inventory exactly and does not add rules found
elsewhere in the mounted workspace.

## Definitions

The first three rules are the complete recursive definition of
`oddIndexEvenSum`:

- `rule-940cbb884f9549b397e4342d4b98cd65a90514a5dadf0988995ebb63c4863972`
  defines the empty-list base case.
- `rule-b4e4b9f0f331e113d779f71be515c2b912214b2b80719d0c13599380fd3a1b6e`
  defines the singleton-list base case.
- `rule-7de63c270a73ef33e344bdabda30fae520cdb4a14ebb626e728c947d8b5313a9`
  defines the pairwise recurrence. The second member of each pair is at an
  odd zero-based index, and the recurrence continues on the remaining
  sequence.

The fourth rule,
`rule-4cd1ac867a395f614e8596c8ea01245b129a1d692ce9079a67f6e5573bde5845`,
is the macro expansion defining the named term `solutionProgram`. Stage 1's
`prove.sh` additionally compares its macro-expanded KORE representation with
the freshly translated `solution.mpy`, but the rule remains a definition of a
named proof term rather than a derived lemma.

No canonical rule is an operational execution rule. The canonical inventory
contains only the mathematical-summary equations and proof-term macro above.

## Proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence does not contain the required prove-before-use ordering
for any inventory rule. `prove.sh` first compiles `verification.k` as module
`VERIFICATION`, so all four canonical rules are already present in the
definition. It then invokes `kprove spec.k` to prove the recursive-call
summary and end-to-end claims. Those claims are not installed afterward as
rules in a later verification module, and none exactly corresponds to a
canonical inventory rule. Consequently, no inventory entry qualifies as
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. None of the four inventory rules asserts an
additional trusted mathematical fact: three define the contract summary and
one expands a macro. The inventory also contains no rule carrying the
`simplification` attribute.

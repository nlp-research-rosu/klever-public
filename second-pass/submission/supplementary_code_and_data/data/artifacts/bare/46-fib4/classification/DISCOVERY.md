# Trust-boundary classification

The canonical inventory contains seven rules, all from the `VERIFICATION`
module. Every rule is classified as `DEFINITION`.

## Definitions

The first two rules are the complete case split defining the mathematical
summary `advanceTo`:

- When `I > N`, the rolling computation has finished and its result is the
  current fourth window value `D`.
- When `I <= N`, the summary shifts `(A, B, C, D)` to
  `(B, C, D, A + B + C + D)`, increments `I`, and continues.

The remaining five rules define `fib4Spec`. Four equations give the contract's
base values at indices 0 through 3. The guarded equation for `N >= 4` defines
the summary by starting `advanceTo` with `(0, 0, 2, 0)` at index 4.

These are mathematical summary equations, not Python execution or observation
rules, so none is classified as `OPERATIONAL_RULE`. The inventory records an
empty attribute list for every rule; in particular, none carries the
`simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` first runs
`kompile semantic.k`; `semantic.k` imports `VERIFICATION`, so all seven
inventoried rules are already present in the compiled definition. The script
then invokes `kprove` once against that definition. It does not first prove
the exact statement of any inventoried rule against a module lacking that
rule, and it performs no later recompilation or rule insertion. Thus Stage 1
provides no evidence satisfying the required ordering for a separately proved
derived lemma.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule is an additional
mathematical fact trusted to close the proof; all seven define the two named
mathematical summaries used by the specification.

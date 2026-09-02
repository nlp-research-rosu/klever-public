# K proof trust-boundary discovery

The canonical inventory contains nine rules, all in the local
`MPY-VERIFICATION-BASE` / `MPY-VERIFICATION` closure. Each inventory rule is
classified exactly once and in canonical inventory order in
`trust-boundary.json`.

## Definitions

Eight rules are `DEFINITION`:

- The three `keptAcc` equations define the forward filtering accumulator:
  the empty-input base case, deletion case, and retention/append case.
- The three `reversedKeptAcc` equations define the reverse filtering
  accumulator: the empty-input base case, deletion case, and
  retention/prepend case.
- The two `lastCharacter` equations define the loop target's final value for
  empty and nonempty remaining sequences.

The four rules carrying the `simplification` attribute are conditional
recurrences for `keptAcc` and `reversedKeptAcc`. They are defining equations,
so they are classified as `DEFINITION`, as required.

There are no inventory rules classified as `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules supported by the finalized Stage 1
evidence.

The loop-summary rule
`rule-00095a0636462ee35f07d6cfe2315557d18e9db58d43983c60cf4c9478d9c6f6`
textually corresponds to the claim in `LOOP-SPEC`, apart from being a rule
with a `priority(40)` attribute. The source comment also calls it proved.
However, the finalized `prove.sh` does not first prove that statement against
a semantic definition that excludes the rule:

1. Lines 20–24 compile `verification.k` with
   `--main-module MPY-VERIFICATION`.
2. `MPY-VERIFICATION` contains the loop-summary rule and imports
   `MPY-VERIFICATION-BASE`.
3. Lines 27–29 run the `LOOP-SPEC` claim against that same
   `verification-kompiled` definition.
4. Selecting `--spec-module LOOP-SPEC` selects the specification claims; it
   does not supply evidence of a separately compiled operational definition
   whose main-module closure omits the summary rule.

Thus the apparent ordering of the two `kprove` commands is insufficient:
the candidate rule is already in the definition used by the first command.
No Stage 1 command compiles `MPY-VERIFICATION-BASE` as the semantic main
module and proves the claim against that rule-free definition.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly the loop-summary
rule
`rule-00095a0636462ee35f07d6cfe2315557d18e9db58d43983c60cf4c9478d9c6f6`.
This rule summarizes arbitrary execution of the filtering loop and updates
the proof accumulators and final loop-target value. The later `SPEC` proof
imports `MPY-VERIFICATION` and relies on this summary. Because the finalized
evidence does not establish it in a rule-free definition, it is an additional
trusted mathematical fact at the proof boundary.

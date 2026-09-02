# Trust-boundary discovery

The canonical inventory contains two rules from module `VERIFICATION`. Both are classified as `DEFINITION` because together they define the mathematical summary `belowZeroFrom`:

- `rule-fcdc37ffe1758064b9da7c725e0ad61a78f240a75ea058014581fdc375edabf6` is the base equation. An empty operation list has no negative prefix, so the summary is `false`.
- `rule-8b7947851f91e86a240db6f33eb6cf303d12fbe3055e203d3b910d4df3445b39` is the recursive equation. It tests whether adding the head operation makes the balance negative and otherwise applies the same summary to the tail with the updated balance.

Neither rule has the `simplification` attribute. Neither is an `OPERATIONAL_RULE`: they define the independent mathematical result used in the proof rather than a program execution or observation step.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1 `prove.sh` first compiles `verification.k` as module `VERIFICATION`, with both inventoried rules already present, and then invokes `kprove` on `SPEC.entry-reaches-loop` and `SPEC.loop-correct`. It does not prove either inventoried rule against a module lacking that rule and subsequently install an exactly corresponding reusable rule. Therefore neither rule meets the evidence requirement for `PROVED_DERIVED_LEMMA`.

The domain-lemma set is empty. No inventoried rule asserts an additional mathematical fact beyond the defining equations of `belowZeroFrom`.

# Trust-boundary classification

The canonical inventory contains six rules, all in `FIBFIB-VERIFICATION`. Every rule is classified as `DEFINITION`:

- `loopCondition`, `loopBody`, and `fibfibProgram` expand named proof terms into the translated AST fragments consumed by the operational semantics.
- The three `fibfibMath` rules define the mathematical summary through its two base regions and its recurrence.

No inventory rule is an `OPERATIONAL_RULE`: the inventory contains proof-term and mathematical-summary definitions, while the ordinary execution rules live in the semantics module outside this inventory.

There are no separately proved derived lemmas. Stage 1 `prove.sh` invokes `kprove` once on `spec.k`, proving `program-correct` and `loop-invariant` in the same specification. It does not first prove the exact statement of any inventory rule against a module lacking that rule and then reuse it, so no rule qualifies as `PROVED_DERIVED_LEMMA`.

The domain-lemma set is empty; none of the inventory rules supplies an additional trusted mathematical fact beyond the definitions.

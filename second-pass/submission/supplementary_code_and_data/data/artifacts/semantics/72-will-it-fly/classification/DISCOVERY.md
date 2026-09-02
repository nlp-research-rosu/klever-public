# Trust-boundary discovery

The canonical inventory contains 14 rules, all from the Stage 1
`VERIFICATION` module. The classifications preserve the inventory order.

## Definitions

Twelve rules are `DEFINITION`s:

- The three `allInts` equations define the admissible integer-list domain.
- The two `sumIntVS` equations define the mathematical sum summary.
- The two `snocVS` and two `reverseVS` equations define sequence append-at-end
  and reversal structurally.
- `willItFlyResult`, `willItFlyModule`, and `willItFlyClosure` expand named
  proof terms into the translated expression, module, and closure structures.

These rules introduce recurrences or expand names; they do not assert a bridge
between an existing execution operation and its mathematical summary.

## Domain lemmas

The domain-lemma set is **not empty**. It consists of exactly:

- `rule-e8f739bf08317e883904eb65ce494f7a330c76031451acc8eea4e8073068f5e0`,
  which summarizes `doSlice(list(VS), noB, noB, someB(-1))` as
  `list(reverseVS(VS))` for an arbitrary value sequence.
- `rule-8c6fd5f43e6635bfa3e7668c921b0d8e3f46d6d1de6484989e3107ed21ffcc0c`,
  which summarizes the supplied `#sumAcc` fold over an arbitrary all-integer
  list as `sumIntVS(VS)`.

Both are additional mathematical facts used to make arbitrary symbolic
sequences reducible. Their `priority(40)` attributes control rewriting
priority but do not constitute proof evidence.

## Proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1 `prove.sh` compiles `verification.k` into
`verification-kompiled` and only then invokes `kprove spec.k` against that
definition. Consequently, both summary rules above are already present in the
definition used to prove the three final claims. There is no earlier
`kprove` command, proof module omitting either rule, or exact claim establishing
either statement before reuse.

## Operational rules and simplification attributes

No inventory rule is classified as `OPERATIONAL_RULE`: the ordinary Python
execution machinery is imported from the supplied reference semantics and is
outside this local verification-rule inventory. The two local rules that
mention existing operations are summary facts rather than ordinary execution
steps.

No canonical inventory rule carries the `simplification` attribute.

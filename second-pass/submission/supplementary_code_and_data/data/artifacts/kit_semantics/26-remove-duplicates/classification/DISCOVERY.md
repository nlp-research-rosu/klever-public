# Trust-boundary discovery

## Scope and canonical inventory

The exhaustive source of rules for this classification is
`/reference/rule-inventory.json`, with canonical inventory SHA-256:

```text
999a94a14a4ee59a8507f036df83415964d63647ddc55c2c8a288c2eb762ccd2
```

It contains four rules, all in the local `VERIFICATION` module. Each canonical
`source_rule_id` appears exactly once in `trust-boundary.json`, in inventory
order. Imported reference-semantics rules are not added because the launcher
inventory is expressly exhaustive for this task.

## Classifications

| Inventory order | Source rule | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Base equation `allInts(.ValSeq) => true`, defining the predicate on the empty sequence. |
| 2 | `rule-bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0` | `DEFINITION` | Recursive equation defining `allInts` on `vCons` from `isInt` on the head and `allInts` on the tail. |
| 3 | `rule-6c55d502b263cd9488fb4d13c18990fa8865f154bf5db922ef461ae84c961308` | `DEFINITION` | Base equation defining `rdAcc` when no input remains. |
| 4 | `rule-7614bf9bc54b61933d1cbd1d534bb404043cb2a80c42f36e07b6cf7486cf642d` | `DEFINITION` | Recursive equation defining `rdAcc` by the count-one conditional and recursion on the remaining tail. |

The two equations for `allInts` are exhaustive, disjoint structural cases for
a named domain predicate. The two equations for `rdAcc` are exhaustive,
disjoint structural cases for a named mathematical accumulator; the recursive
case uses a Boolean conditional and descends through `REST`. None matches a
`<k>` computation or configuration cell, so none is an `OPERATIONAL_RULE`.

No inventoried rule carries the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical inventory.

The mounted Stage 1 `prove.sh` first kompiles `verification.k` as module
`VERIFICATION`, which already contains all four inventoried rules, and only
then runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.remove-duplicates-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Both commands print `#Top` in the mounted evidence, but neither proves an exact
inventoried rule against a module that omits that rule. The first proves the
loop reachability claim in `spec.k`; that claim is not one of the four
canonical rule entries. Therefore no entry satisfies the required ordering
and exact-correspondence conditions for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No canonical rule asserts an additional
mathematical fact trusted solely to close the proof; all four rules are
defining equations.

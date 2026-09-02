# Independent rule classification

The local verification-module closure is `VERIFICATION-BASE`,
`VERIFICATION-MEMBER`, then `VERIFICATION`. It contains 11 rules.

| Source rule | Span | Classification | Independent reason |
|---|---:|---|---|
| `rule-fecd0d...` | 8 | `DEFINITION` | Empty-sequence base equation for the named membership summary `memberVS`. |
| `rule-01ca47...` | 9-11 | `DEFINITION` | Unequal-head recursive equation for `memberVS`; it decreases the sequence. The `simplification` attribute is attached to a defining equation. |
| `rule-5a42fa...` | 12-14 | `DEFINITION` | Equal-head defining equation for `memberVS`. The guard complements the preceding case, and the `simplification` attribute is attached to a defining equation. |
| `rule-e701b8...` | 18-19 | `DEFINITION` | Present-element defining branch of `appendUnique`. |
| `rule-f72f44...` | 20-22 | `DEFINITION` | Absent-element defining branch of `appendUnique`; the guard complements the preceding branch. |
| `rule-6455f8...` | 26 | `DEFINITION` | Empty-input base equation for the accumulator recurrence `dedupFromVS`. |
| `rule-92a60f...` | 27-28 | `DEFINITION` | Recursive `dedupFromVS` equation; it consumes one input element and threads `appendUnique`. |
| `rule-3d2b32...` | 32 | `DEFINITION` | Empty-input base equation for the named loop-target summary `lastFromVS`. |
| `rule-2fc3eb...` | 33 | `DEFINITION` | Recursive `lastFromVS` equation; it consumes one element and retains the latest target value. |
| `rule-968e63...` | 41-43 | `PROVED_DERIVED_LEMMA` | Exact `#memberAcc` execution summary. The identical arbitrary-continuation claim first proves under `VERIFICATION-BASE`, whose closure excludes this rule; the independent rerun returned `#Top`. |
| `rule-e25655...` | 52-75 | `PROVED_DERIVED_LEMMA` | Exact source-loop execution summary including continuation, environment, scope update, target value, and heap update. The identical claim first proves under `VERIFICATION-MEMBER`, whose closure excludes this rule; the independent rerun returned `#Top`. |

## Operational comparison

The supplied semantics reduces list iteration one head at a time
(`list.k:9-10`), membership through `#memberAcc` and `==K`
(`list.k:57-67`), `for` loops through `#loop` with target binding and body
execution (`controls.k:62-75`), and `append` by the exact in-place heap update
(`list.k:52-55`). The source body (`solution.py:3-7`) initializes an empty
accumulator, tests `x not in result`, and appends only absent elements.

Consequently:

- `memberVS` is the same structural fold as `#memberAcc`.
- `appendUnique` is exactly the two branches of the source conditional plus
  `append` heap update.
- `dedupFromVS` is the loop recurrence over the remaining input and current
  accumulator.
- `lastFromVS` is exactly the final value retained in the loop target `x`.

These are named summaries/recurrences, not human-facing domain theorems. The
two operational-looking rules are valid derived lemmas because their exact
statements are machine-proved before insertion. None is an ordinary unproved
operational rule, and none asserts uniqueness, ordering, membership, or another
postcondition property as an unproved domain fact.

## Domain set

The independently reclassified `DOMAIN_LEMMA` set is genuinely empty. Both
`simplification` rules are `DEFINITION`, satisfying the classification rule.
No irrelevant or disguised domain lemma exists in this closure.

# Independent rule classification

All rules are in the single local verification closure module `VERIFICATION`.
None has a `<k>` cell or an MPY execution-form head. Searches across the frozen
K sources find these eight proof-local symbols only in `verification.k` and in
the two reachability claims of `spec.k`.

| Rules | Classification | Independent semantic reason |
|---|---|---|
| `nonNegativeVals`, lines 10-13 (3 rules) | `DEFINITION` | Constructor-complete definition of the theorem's nonnegative-integer input predicate. Empty, integer head, and `owise` non-integer head are exhaustive. It does not assert a consequence about an already-defined predicate. |
| `nextRepeated`, lines 18-21 (2 rules) | `DEFINITION` | Guard-complete definition of one counter update. Equality increments; its negation resets to one. The guards are complementary. |
| `scanPrevious`, lines 24-26 (2 rules) | `DEFINITION` | Base/step structural recurrence for the last prior value; the step strictly descends on the `ValSeq` tail. |
| `scanRepeated`, lines 29-31 (2 rules) | `DEFINITION` | Base/step structural recurrence for the final adjacent-run count, using `nextRepeated` and descending on the tail. |
| `scanValue`, lines 34-36 (2 rules) | `DEFINITION` | Base/step structural recurrence for the last loop-bound value, descending on the tail. |
| `duplicateOK`, lines 39-42 (2 rules) | `DEFINITION` | Base/step Boolean recurrence saying no scanned step makes the adjacent-run count exceed two. It descends on the tail and is not a theorem about some separately defined occurrence predicate. |
| `scanDuplicates`, lines 46-47 (1 rule) | `DEFINITION` | Exhaustive named summary combining the prior Boolean result with the suffix duplicate recurrence. It preserves an already-false result. |
| `sortedWithAtMostTwo`, lines 53-56 (1 rule) | `DEFINITION` | Guarded named contract predicate: equality with the supplied `sortVS` value conjoined with the duplicate summary. This merely unfolds the target name; it states no ordering/permutation fact about `sortVS` and proves no proposition. |

Independent totals:

- `DEFINITION`: 15
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

There are no `[simplification]` rules. The only rule attribute in the inventory
is `[owise]` on the non-integer case of `nonNegativeVals`.

Mathematical relevance: on the formal nonnegative-integer domain, the source
first sets `result` to `lst == sorted(lst)`. The recurrences then preserve that
Boolean while tracking adjacent runs and force it false at count three. If the
input is sorted, equal values are contiguous, so no run of three is equivalent
to every value occurring at most twice. If it is unsorted, the sorting conjunct
is already false. Thus every summary is relevant to source execution or the
postcondition, while no independent mathematical lemma is embedded among them.

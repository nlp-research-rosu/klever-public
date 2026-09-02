# Independent classification

| # | Lines | Classification | Independent basis |
|---:|:---:|---|---|
| 1 | 8–30 | `DEFINITION` | Macro for the exact translated loop body. |
| 2 | 33–39 | `DEFINITION` | Macro for the exact translated function body. |
| 3 | 42–43 | `DEFINITION` | Macro for the translated function definition. |
| 4 | 47 | `DEFINITION` | Empty-sequence equation for the named `allInts` predicate. |
| 5 | 48–49 | `DEFINITION` | Descending recurrence for `allInts`. |
| 6 | 54 | `DEFINITION` | Defining equation for the fresh named predicate `definedProjectInt`. |
| 7 | 59–61 | `DOMAIN_LEMMA` | A theorem-like definedness fact about the pre-existing partial Int projection; it does not define its LHS. |
| 8 | 63–65 | `DEFINITION` | Guarded defining equation for the fresh `projectIntTotal` helper. |
| 9 | 67–69 | `DOMAIN_LEMMA` | Reverse rewrite of the pre-existing projection to the fresh helper under the Int-definedness guard. |
| 10 | 71–72 | `DEFINITION` | Constructor/collapse equation defining `projectIntTotal` on an actual `Int`. |
| 11 | 74–75 | `DOMAIN_LEMMA` | Idempotence is a property of the helper, not a constructor case or recurrence. |
| 12 | 80–83 | `DOMAIN_LEMMA` | Proof-local symbolic extension of the fixed `applyBin("*", Int, Int)` rule to `Val` operands under explicit Int guards. |
| 13 | 85–88 | `DOMAIN_LEMMA` | Proof-local symbolic extension of fixed Int addition to a guarded symbolic `Val`. |
| 14 | 92–94 | `DEFINITION` | First guarded equation of the named contribution summary. |
| 15 | 95–98 | `DEFINITION` | Second disjoint guarded equation of the named contribution summary. |
| 16 | 99–102 | `DEFINITION` | Third disjoint guarded equation of the named contribution summary. |
| 17 | 108 | `DEFINITION` | Base equation of the named accumulator recurrence. |
| 18 | 109–114 | `DEFINITION` | Descending recurrence over the sequence tail. |
| 19 | 115–117 | `DEFINITION` | Complementary off-domain totalization equation for the named helper. |

No entry is an `OPERATIONAL_RULE`: none is an ordinary configuration/cell
execution or observation rule in the local verification module.  The two
`applyBin` rules are simplification facts added specifically for symbolic
execution and therefore must be classified as definitions or domain lemmas;
because they rewrite a pre-existing operational symbol rather than define a
fresh summary, they are domain lemmas.

No entry is a `PROVED_DERIVED_LEMMA`.  `prove.sh` compiles the complete
`VERIFICATION` module once, with every rule already present, before proving the
loop claim and then the target claims.  There is no earlier proof of any exact
rule against a module from which that rule was removed.

All seven rules carrying `simplification` or `simplification(10)` are in the
permitted classes: rules 8 and 10 are definitions; rules 7, 9, and 11–13 are
domain lemmas.

The five domain lemmas are materially relevant.  Rules 7, 9, and 11 connect
symbolic `Val` elements guarded by `allInts` to the Int projection used by the
summary.  Rule 12 is exercised by `value * value` and the nested multiplication
in the cube branch.  Rule 13 is exercised by every `result += contribution`.
The idempotence rule normalizes projections created by nested symbolic
multiplication.  None is a human-facing result lemma or an assertion of the
sum-of-squares postcondition.

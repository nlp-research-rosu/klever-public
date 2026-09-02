# Independent classification judgment

| Rule | Independent class | Reason |
|---|---|---|
| `rule-fcdc37…abf6`, `VERIFICATION:11` | `DEFINITION` | Base equation for the fresh total summary `belowZeroFrom`; it assigns `false` to the empty `IntList`. It does not rewrite a configuration or assert a theorem about a pre-existing symbol. |
| `rule-8b7947…5b39`, `VERIFICATION:12-16` | `DEFINITION` | Recursive equation for the same fresh summary. It updates the balance, returns `true` exactly when the updated balance is negative, and otherwise recurses on the structurally smaller tail. |

The two constructor patterns are disjoint and cover `IntList`. The recursive
call descends to the list tail. The equations exactly mirror the operational
sequence in `semantic.k`: the loop binds the head to `<current>`, the
`AugAssign` rule adds it to `<balance>`, and the comparison rule tests the new
balance using strict `<Int 0`; early return produces `BoolV(true)`, while loop
exhaustion reaches `BoolV(false)`.

Neither rule is an `OPERATIONAL_RULE`: neither mentions `<k>`, `<balance>`,
`<current>`, `<result>`, or any operational continuation. Neither is a
`PROVED_DERIVED_LEMMA`: no such classification is claimed and neither is a
previously proved rule later reintroduced. Neither is a `DOMAIN_LEMMA`: both
define a fresh named proof summary instead of adding mathematical facts about
existing domains. Both are relevant because `SPEC.loop-correct` places
`belowZeroFrom(B, OPS)` in the final result, and its recurrence matches the
source program's running-prefix condition.

No inventoried rule has a `simplification` attribute.

Independent domain-lemma set: empty.

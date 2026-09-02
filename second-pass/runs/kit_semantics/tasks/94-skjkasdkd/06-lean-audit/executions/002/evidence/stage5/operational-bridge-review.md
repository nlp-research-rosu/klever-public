# Operational-bridge review

Each row is tied to the exact `target.parameters` entry checked in `candidate-integrity-check.log`. The fixed MPY meanings come from `semantics/int.k`, `semantics/bool.k`, `semantics/operators.k`, generated injections, and the frozen `verification.k` definitions/domain rules. Candidate comments were not used as authority.

| Target parameter | Candidate definition | Independent operational comparison |
|---|---|---|
| `«_-Int_»` | `x - y` | Exact K `-Int`; positive and negative cases pass. |
| `_andBool_` | `x && y` | Exact K Boolean conjunction. |
| `«_>Int_»` | `decide (x > y)` | Exact K integer `>Int`, including equality boundary. |
| `«_>=Int_»` | `decide (x ≥ y)` | Exact K integer `>=Int`, including equality boundary. |
| `«_<Int_»` | `decide (x < y)` | Exact K integer `<Int`, including negative operands. |
| `«_<=Int_»` | `decide (x ≤ y)` | Exact K integer `<=Int`, including equality. |
| `«_==Int_»` | `x == y` | Exact K integer equality. |
| `«_=/=Int_»` | `!(x == y)` | Exact K integer disequality. |
| `«_%Int_»` | `Int.tmod x y` | Exact K truncating `%Int`; `-13 %Int 10 = -3` distinguishes it from Python modulo. |
| `«_+Int_»` | `x + y` | Exact K integer addition. |
| `«_/Int_»` | `Int.tdiv x y` | Exact K truncating `/Int`; the used decimal quotient has positive divisor 10. |
| `applyBin` | `Operational.applyBinaryModel` | Its integer/integer `%` arm returns injected `pyMod`; its `+` arm returns injected addition, exactly matching rules 16–17 and source execution. Tests include a negative dividend. Unused partial/unsupported K domains are not invoked by any bound rule. |
| `applyCmp` | `Operational.applyComparisonModel` | Integer/integer `>`, `>=`, and `<` arms call exact integer comparison, matching rules 13–15. Tests exercise true, false, and equality cases. |
| `definedProjectInt` | `(projectValueIntOption value).isSome` | True exactly on `SortVal.inj_SortInt`; false on a Boolean value, matching `isInt(V)` for this frozen cast domain. |
| `digitSum` | `digitSumModel` | `0` for nonpositive input and recursive base-10 digit sum for positive input, exactly rules 29–30. Tests produce 10 for 181 and 25 for 4597. |
| `isInt` | two singleton-K-sequence integer injection patterns | Exact generated sort-predicate behavior for direct and `Val`-mediated integer injection; false for Boolean and nonsingleton K sequences. |
| `primeTail` | `primeTailModel` | Exact three-way K definition: false below 2, true at/after `N`, otherwise reject a divisor or recur at `D+1`. Prime 7, composite 9, below-domain, and completed cases pass. |
| `«project:Int»` | `projectKIntOption term |>.getD 0` | Returns the exact integer on the rule's defined singleton-K projection domain. The default is outside the guarded K domain and cannot discharge a guarded equality incorrectly. |
| `projectIntTotal` | integer option projection with default 0 | Returns the exact embedded integer wherever `definedProjectInt=true`; its arbitrary totalization outside that guard is consistent with the K `total,no-evaluators` symbol and is not used by the frozen source precondition. |
| `pyMod` | `tmod (tmod x y + y) y` | Textually and operationally the frozen rule `((x %Int y)+Int y)%Int y`; tests give 7 for `(-13,10)` and -7 for `(13,-10)`. |
| `«project:Int?»` | `projectKIntOption` | `some I` exactly on defined integer projections and `none` on a Boolean projection, preserving the source `#Ceil` condition. |

The executable adversarial suite contains 38 bridge/boundary checks, all true, and seven counterfactual checks, all true. The counterfactuals distinguish the candidate from a constant-false `primeTail`, identity `digitSum`, hard-coded projection, truncating-only Python modulo, constant comparison, left-identity binary operation, and constant-false `isInt`. This directly rules out the convenient-definition failure modes even where a narrow equation could otherwise underconstrain a parameter.

# Independent obligation judgment

The independently classified domain set has exactly seven rules. The generated
target has exactly seven ordered, unique conjuncts, one per rule.

1. `rule-ec583...bb9f` exports the guarded Int projection equality. Its Lean
   guard is the exact nested `andBool` form from `verification.k`, and both
   sides are the corresponding KORE projection and `projectIntTotal`.
2. `rule-90eb...a28` exports definedness of the Int projection as
   `project:Int?.isSome ↔ isInt = true ∧ True`. The `True` is the faithful
   image of `#Ceil(V)` for a Lean value `V : SortVal`; it is not a separate
   target conjunct and the remaining definedness equivalence is nontrivial.
3. `rule-3905...c4e` is the same guarded value equality for Bool.
4. `rule-223d...a83` is the corresponding Bool projection-definedness fact.
5. `rule-aea3...b72e` is the Float projection equality under the exact
   `floatV(V)` guard.
6. `rule-725c...068` is the corresponding Float projection-definedness fact.
7. `rule-8231...0e92` is the exact `intOf(V) = intLikeTotal(V)` equation under
   `integralV(V)`.

All seven facts are relevant to the frozen source body
`q == q[::-1] and sum(q) <= w`: the Int/Bool facts support the supplied
integer/Boolean `sum` fold and the Float facts support the supplied mixed
numeric fold. None is the palindrome or sum-bound postcondition itself.

The generated theorem is relational. In particular, coordinated constant
implementations of `project:Int` and `projectIntTotal` can satisfy their value
equality while being operationally false. `OperationalBridgeTests.lean`
exhibits that counterfactual and separately tests the candidate's actual
definitions against ground operational meanings.

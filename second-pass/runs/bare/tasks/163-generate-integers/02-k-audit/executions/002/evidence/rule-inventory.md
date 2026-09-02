# Reviewer rule and declaration inventory

Scope: all local declarations and rules in the candidate's `semantic.k`,
`verification.k`, and `spec.k`. There are no generated helper K files.
Imported K builtin modules are accounted for separately as trusted primitives.

## `semantic.k`: local syntax

`MPY-SYNTAX` declares:

1. `Program ::= Module(Stmts)` (line 8).
2. `Stmts ::= List{Stmt, ""}` (line 10).
3. `Stmt ::= FuncDef(String, Params, Stmts)` (line 11).
4. `Stmt ::= Assign(Expr, Expr)` (line 12).
5. `Stmt ::= If(Expr, Stmts, Stmts)` (line 13).
6. `Stmt ::= Return(Expr)` (line 14).
7. `Params ::= Params(Strings)` (line 16).
8. `Strings ::= List{String, ","}` (line 17).
9. `Expr ::= Name(String)` (line 19).
10. `Expr ::= Int(Int)` (line 20).
11. `Expr ::= ListExpr(Exprs)` (line 21).
12. `Expr ::= Compare(Expr, CmpOps)` (line 22).
13. `Expr ::= BinOp(String, Expr, Expr)` (line 23).
14. `Exprs ::= List{Expr, ","}` (line 24).
15. `CmpOps ::= List{CmpOp, ","}` (line 25).
16. `CmpOp ::= CmpOp(String, Expr)` (line 26).

`MPY` declares:

17. `Input ::= pair(Int, Int)` (line 37).
18. `Value ::= intVal(Int)` (line 38).
19. `Value ::= boolVal(Bool)` (line 38).
20. `Value ::= listVal(List)` (line 38).
21. `Result ::= "noResult"` (line 39).
22. `Result ::= Value` (line 39).
23. `KItem ::= exec(Stmts)` (line 41).
24. `KItem ::= execStmt(Stmt)` (line 42).
25. `KItem ::= eval(Expr)` (line 43).
26. `KItem ::= assignTo(String)` (line 44).
27. `KItem ::= binRight(String, Value)` (line 45).
28. `KItem ::= cmpLeft(String, Expr)` (line 46).
29. `KItem ::= cmpRight(String, Value)` (line 47).
30. `KItem ::= choose(Stmts, Stmts)` (line 48).
31. `KItem ::= "returnValue"` (line 49).
32. `Value ::= evalPlaceholder(Expr)` (line 89).

The configuration at lines 51-57 has one `<py>` wrapper and four state cells:
`<k>` (current `Program`/computation), `<input>` (the two integer arguments),
`<env>` (a K `Map`), and `<result>` (initially `noResult`). Every cell is read
or written by at least one rule.

There are no local syntax macros, aliases, priorities, opaque declarations,
`total` declarations, `functional` declarations, simplification rules, or
concrete-only rules in `semantic.k`.

## `semantic.k`: all 21 ordinary rules

| ID | Lines | Rule role | Reviewer assessment on the submitted program |
|---|---:|---|---|
| S1 | 59-62 | Recognize the exact `generate_integers(a,b)` binding, start its body, and bind configuration inputs to `a` and `b` in an initially empty environment. | Exact entry-point invocation model for the submitted one-function module. It does not summarize or skip the body. |
| S2 | 64 | `exec(.Stmts) => .K`. | Correct end of a statement sequence. |
| S3 | 65 | Split a nonempty statement list into its head and remaining sequence. | Correct source-order sequencing; concrete threshold tests confirm the list order. |
| S4 | 67 | Begin `Name` assignment by evaluating its RHS. | Correct evaluation order for every submitted assignment. |
| S5 | 68-69 | Store the computed value under the target name. | Correct local-map update for the submitted name targets. |
| S6 | 71-72 | Evaluate an `If` guard before choosing a branch. | Correct guard-before-branch order. |
| S7 | 73 | Execute the then-list when the guard is true. | Correct. |
| S8 | 74 | Execute the else-list when the guard is false. | Correct. |
| S9 | 76 | Evaluate a returned expression. | Correct for the submitted final return. |
| S10 | 77-78 | Consume `returnValue` and write the returned value into `<result>`. | Correct in the submitted context, where `Return` is the last statement and no call/control frame remains. The rule is not a general early-return semantics; that unused language context is excluded. |
| S11 | 80 | Evaluate an integer literal to `intVal`. | Correct. |
| S12 | 81-82 | Look up a name in `<env>`. | Correct for all submitted names, each of which is initialized before use. |
| S13 | 83 | Evaluate the empty list literal. | Correct. |
| S14 | 84 | Evaluate a singleton integer list literal. | Correct and covers every nonempty list literal in this program. |
| S15 | 86-87 | Schedule binary-expression left operand first and retain the right expression in an internal placeholder. | Correct left-to-right scheduling. |
| S16 | 90-91 | After the left value is obtained, evaluate the retained right expression. | Correct; `evalPlaceholder` is a defined internal constructor, not an opaque result. |
| S17 | 92-93 | Concatenate two evaluated K lists for operator `"+"`, preserving left-before-right order. | Correct for every submitted binary operation; concrete executions check order. |
| S18 | 95-96 | Schedule a singleton comparison's left operand first. | Correct. |
| S19 | 97-98 | Evaluate the comparison's right operand after the left. | Correct. |
| S20 | 99-101 | Produce true for integer `<=` when `LEFT <=Int RIGHT`. | Correct. The apparent reversed pattern names reflect continuation layout: the retained left value is the argument of `cmpRight`, while the newly evaluated right value is at the front of `<k>`. |
| S21 | 102-104 | Produce false for integer `<=` when the preceding condition is false. | Correct, disjoint from and jointly exhaustive with S20 over K integers. |

`evalPlaceholder` is syntactically a `Value` so it can be retained in
`binRight`; no rule returns it as a source result on any submitted execution.
The exact program contains no early return, multi-element literal, non-name
assignment, chained comparison, operator other than list `+` or integer `<=`,
function call, exception path, loop, I/O, heap, or allocation.

## Construct coverage map for `solution.mpy`

| Submitted constructor | Declaration | Behavioral rules |
|---|---|---|
| `Module` | syntax 1 | S1 |
| `FuncDef` and `Params("a","b")` | syntax 3, 7, 8 | S1 |
| statement lists | syntax 2 | S2-S3 |
| `Assign(Name(...), ...)` | syntax 4, 9 | S4-S5, S12 |
| `If` | syntax 5 | S6-S8 |
| final `Return` | syntax 6 | S9-S10 |
| `Int` | syntax 10 | S11 |
| empty and singleton-integer `ListExpr` | syntax 11, 14 | S13-S14 |
| singleton `Compare(..., CmpOp("<=", ...))` | syntax 12, 15, 16 | S18-S21 |
| `BinOp("+", list, list)` | syntax 13 | S15-S17 |

Every constructor in the regenerated `solution.mpy` is covered, and no rule
fabricates a submitted-program result for an unmodeled used constructor.

## `verification.k`: local declarations and all rules

1. `List ::= expectedDigit(Int, Int, Int) [function]` (line 6).
2. `List ::= expected(Int, Int) [function]` (line 7).
3. V1 (lines 9-11): `expectedDigit(A,B,D)` is `[D]` exactly when `D` lies
   inclusively between the two endpoints in either orientation.
4. V2 (lines 12-15): it is the empty list under the Boolean negation of V1's
   condition.
5. V3 (lines 17-21): `expected(A,B)` concatenates the four digit summaries for
   `D = 2,4,6,8` in ascending order.

V1 and V2 have complementary, disjoint guards over K integers. V3 is
unconditional and terminating. Neither function is opaque, neither replaces
program execution, and neither appears in any operational rule. They are
truthful definitional summaries used only in the destination. No local rule has
`total`, `functional`, `simplification`, `concrete`, or priority attributes.

Because the claim requires positive endpoints, digit `0` cannot lie between
them. Thus `2,4,6,8` are exactly all even decimal digits relevant to the
contract.

## `spec.k`

There is one reachability claim, `generate-integers-correct` (lines 6-80), and
no other claim or rule. It starts from the complete submitted program term,
`pair(A,B)`, empty environment, and `noResult`; it requires `A >Int 0` and
`B >Int 0`. Its destination consumes `<k>` and requires both local `result` and
`<result>` to equal `listVal(expected(A,B))`.

The claim contains no omitted cell, RHS-only/free result variable, implication
postcondition, auxiliary circularity, loop summary, simplification, priority,
oracle, operational bridge, or opaque symbol.

# Exhaustive local K inventory

Sources inventoried: `/candidate/semantic.k`, `/candidate/verification.k`,
and `/candidate/spec.k`. The mechanical declaration extraction is in
`static_declaration_extract.log`.

## Syntax, configuration, and attributes

`MPY-SYNTAX` declares every one of these productions:

1. `Pgm ::= Module(Stmt)`.
2. `Stmt ::= FuncDef(String, Params, Stmt) | Return(Expr)`.
3. `Params ::= Params(String)`.
4. `Expr ::= Name(String) | Int(Int) | BinOp(String, Expr, Expr) |
   Compare(Expr, CmpOp) | Subscript(Expr, Slice) |
   ListComp(Expr, CompFor) | Call(Expr, Expr)`.
5. `CmpOp ::= CmpOp(String, Expr)`.
6. `Slice ::= Slice(Bound, Bound, Bound)`.
7. `Bound ::= NoBound | Expr`.
8. `CompFor ::= CompFor(Expr, Expr, Expr)`.
9. `Ints ::= nil | cons(Int, Ints)`.

`MPY` adds:

10. `Val ::= intVal(Int) | boolVal(Bool) | listVal(Ints)`.
11. `Env ::= emptyEnv | bind(String, Val, Env)`.
12. `KItem ::= run(Pgm, Ints, Ints, Int) | result(Int)`.
13. `[function] lookup(String, Env) : Val`.
14. `[function] eval(Expr, Env) : Val`.
15. `[function] asInt(Val) : Int`.
16. `[function] asBool(Val) : Bool`.
17. `[function] asInts(Val) : Ints`.
18. `[function] everyOther(Ints) : Ints`.
19. `[function] testAt(Expr, String, Int, String, Ints) : Bool`.
20. `[function] valueAt(Expr, String, Int, String, Ints) : Int`.

`VERIFICATION` adds:

21. `[function] solutionProgram : Pgm`.
22. `[function] expected(Ints, Int) : Int`.

The sole configuration is
`<k> run($PGM, $INPUT, $INPUT, 0) </k>`; there are no state, heap, stack,
I/O, exception, or allocation cells. That is sufficient for this pure
integer-list program. There are no local `[total]`, `[functional]`,
`[simplification]`, `[concrete]`, priority, `owise`, opaque, fresh, or
uninterpreted declarations. None of the ten local functions is declared
total; unsupported values therefore stop visibly instead of being fabricated.

## Rule-by-rule review

| ID | Exact local rule(s) | Classification and complete target judgment |
|---|---|---|
| S1 | `lookup(X, bind(X,V,_)) => V` | Environment head lookup; correct and supplies ordinary lexical shadowing. |
| S2 | `lookup(X, bind(Y,_,ENV)) => lookup(X,ENV)` when `X =/=String Y` | Guard is disjoint from S1 and recursion descends. There is intentionally no `emptyEnv` equation. |
| S3 | `eval(Int(I),_) => intVal(I)` | Literal evaluation; correct. |
| S4 | `eval(Name(X),ENV) => lookup(X,ENV)` | Name lookup; correct for the only bindings used. |
| S5 | `%` evaluation via unguarded `modInt` | **Unsound over its complete declared domain.** On the submitted program’s reachable literal divisor `+2`, Euclidean `modInt` equals Python `%` for every integer dividend, including negatives. But the rule accepts arbitrary right expressions. The trusted translator maps `1 % x` to this rule; with valid input `x=-2`, Python produces `-1` while K’s `1 modInt -2` produces `1`. The complete translated witness `sum([x for x in lst[::2] if 1 % x != 1])` returns `-2` in Python but `0` under this semantics on `[-2]` (`stage5_mod_rule_witness.log`). Thus this is a concrete false result enabled on the declared non-empty integer-list domain. It needed a positive-divisor guard or a Python-remainder definition. Per the Kit extension contract, the bad case cannot be excused as off the immutable program path because the imported equation is globally asserted and reusable. |
| S6 | `!=` evaluation via `=/=Int` | Both reachable operands are integers; correct. |
| S7 | `eval(Subscript(BASE, Slice(NoBound,NoBound,Int(2))),ENV)` using `everyOther` | Correct list slice for finite `Ints`; base is evaluated first as a K function. This helper is not called by the compound `run` rules, which implement the same pair-skipping transition directly. |
| S8–S10 | `asInt(intVal(I))`, `asBool(boolVal(B))`, `asInts(listVal(IS))` | Correct disjoint partial projections. Wrong-tag cases stop. |
| S11 | `everyOther(nil) => nil` | Correct empty slice. |
| S12 | `everyOther(cons(I,nil)) => cons(I,nil)` | Correct singleton slice. |
| S13 | `everyOther(cons(I,cons(_,IS))) => cons(I,everyOther(IS))` | Correct zero-based pair step; structurally descends by two cells and is disjoint from S11/S12. |
| S14 | `testAt` builds `x` then `lst` bindings and evaluates the condition | For the exact program, `VAR="x"` and `PARAM="lst"` are distinct, the comprehension variable correctly shadows the parameter, and the unchanged original argument is used for `lst`. |
| S15 | `valueAt` builds the same environment and evaluates the body | Same binding analysis as S14. The exact body is `Name("x")`, so this yields the current selected integer. |
| S16 | Empty-cursor `run` returns `ACC` | Models termination of `sum` over the empty remaining slice and preserves the framed continuation. Body and condition are correctly not evaluated. |
| S17 | Singleton, true guard: result is `ACC + valueAt(...)` | Correct filter/body/sum order. The condition is evaluated before the body. |
| S18 | Singleton, false guard: result is `ACC` | Correctly skips body evaluation when the filter is false. Guard is the Boolean complement of S17. |
| S19 | Two-or-more cursor, true guard: add the first and recurse on `REST` | Correctly consumes source positions 0 and 1, retaining only position 0 as `lst[::2]` requires. It evaluates filter before body and preserves `PGM`, `ORIGINAL`, continuation, and accumulator. |
| S20 | Two-or-more cursor, false guard: recurse without adding | Complement of S19, with the same two-cell descent and state preservation. |
| V1 | `solutionProgram => Module(FuncDef(...))` | Definitional name for the exact submitted constructor term. The mechanical 87-token comparison and trusted regeneration both match. It does not replace a running term. |
| V2 | `expected(nil,ACC) => ACC` | Mathematical empty/base case; correct. |
| V3 | Singleton odd case adds `I` | Correct for `I modInt 2 != 0`. |
| V4 | Singleton even case preserves `ACC` | Guard is disjoint from and exhaustive with V3 for integers. |
| V5 | Pair-plus odd case adds `I` and recurses on `IS` | Correct even-position recurrence and two-cell descent. |
| V6 | Pair-plus even case preserves `ACC` and recurses | Complement of V5. |

`SPEC` contains four claims, not rules: three displayed examples and one
unbounded `Ints`/`ACC` loop-summary claim. Each was selected and proved
independently in `stage3_reconstruction.log`.

## Constructor-to-rule coverage and control

The submitted term contains `Module`, `FuncDef`, `Params`, `Return`, `Call`,
`Name("sum")`, `ListComp`, `CompFor`, `Name("x")`, `Subscript`,
`Name("lst")`, `Slice(NoBound,NoBound,Int(2))`, `Compare`, `BinOp("%",...)`,
`CmpOp("!=",...)`, and integer literals. S16–S20 match the complete compound
module/function/return/call/comprehension/slice shape. They leave only the
body and filter to S14/S15, which in turn exercise S3–S6 and S8/S9 plus S1/S2.
Pair removal implements the slice and iteration order. No source operation has
observable heap, output, allocation, mutation, exception, or abrupt-control
effects on the declared integer-list domain.

The five `run` rules partition cursor shape into empty, singleton, and
two-or-more; the latter two shapes split on complementary Boolean guards.
Their only recursive transitions remove two cells, so there is no overlap,
priority dependency, or non-descent. The source program is pure, so the single
`<k>` cell exposes its complete observable state.

The compound `run` rules are the generated core semantics for this submitted
IR fragment, not proof-local rules layered over a hidden fixed semantics.
Their connection to Python is therefore a reviewed semantics trust boundary:
the list-induction argument above is universal for finite `Ints`, while
`stage3_semantics_compare_retry.log` supplies finite branch/boundary evidence.

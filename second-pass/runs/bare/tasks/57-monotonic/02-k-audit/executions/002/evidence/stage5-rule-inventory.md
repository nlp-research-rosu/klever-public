# Exhaustive local syntax and rule inventory

Sources inventoried: the immutable candidate copies `semantic.k`,
`verification.k`, and `spec.k` in `/tmp/audit-work/57-monotonic`. There are no
additional candidate K helper files.

## Local syntax declarations

`SEMANTIC-SYNTAX` declares:

1. `Pgm`: `Module(Stmts)`.
2. `Stmts`: separator-free `List{Stmt, ""}`.
3. `Stmt`: `FuncDef(String, Params, Stmts)` and `Return(Expr)`.
4. `Strings`: comma-separated `List{String, ","}`.
5. `Params`: `Params(Strings)`.
6. `Exprs`: comma-separated `List{Expr, ","}`.
7. `CmpOps`: comma-separated `List{CmpOp, ","}`.
8. `Expr`: `Name(String)`, `Bool(Bool)`, `BoolOp(String, Exprs)`,
   `Compare(Expr, CmpOps)`, `Call(Expr, Exprs)`, and
   `KwArg(String, Expr)`.
9. `CmpOp`: `CmpOp(String, Expr)`.
10. `IntList`: `nil` and `cons(Int, IntList)`.
11. `Val`: `boolVal(Bool)` and `listVal(IntList)`.

`SEMANTIC` additionally declares:

12. `Fun`: `function(Params, Stmts)`.
13. `Env`: `env(String, Val)`.
14. Function `#findFunction(String, Stmts) : Fun`.
15. Ordinary `KItem` `#run(Pgm, Val)`.
16. Functions `#apply(String, Val, Stmts)`,
    `#applyFunction(Fun, Val, Stmts)`, `#exec(Stmts, Env, Stmts)`,
    `#eval(Expr, Env, Stmts)`, `#equals(Val, Val)`, and
    `#boolOr(Val, Val)`, all returning `Val`.
17. Function `#asIntList(Val) : IntList`.
18. Functions `#sortInts(IntList)` and `#insertInt(Int, IntList)`,
    returning `IntList`.
19. Functions `#reverseInts(IntList)` and
    `#appendInts(IntList, IntList)`, returning `IntList`.
20. Function `#eqIntLists(IntList, IntList) : Bool`.

`VERIFICATION` additionally declares:

21. Function constant `solutionProgram : Pgm`.
22. Function `#monotonicSpec(IntList) : Val`.

There are no local `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
`[macro]`, priority, or opaque declarations. Every symbol listed as a function
has `[function]`; `#run` is the sole locally declared ordinary operational
`KItem`. The imported K Boolean, integer, string, and generated list machinery
is outside this local inventory and is listed in the trust ledger.

## Rules in `semantic.k`

The numbering below is exhaustive.

1. `#findFunction(F, FuncDef(F, P, BODY) _REST) => function(P, BODY)`.
   Correct for the actual one-definition module; returns the matching body.
2. `#findFunction` skips a head whose name `G` differs from `F`.
   The guard is disjoint from rule 1. It is unused on the exact submitted
   one-function module after the first match.
3. `#run(Module(FUNS), ARG) => #apply("monotonic", ARG, FUNS)`.
   Correctly selects the requested entry point in the fixed submitted module.
4. `#apply` finds `F` and passes the result to `#applyFunction`.
5. `#applyFunction(function(Params(P), BODY), ARG, FUNS)` creates
   `env(P, ARG)` and executes `BODY`. This exactly covers the one-parameter
   submitted function.
6. `#exec(Return(E) _REST, ENV, FUNS) => #eval(E, ENV, FUNS)`.
   Correct Python return control for the actual body; there is no following
   statement in that body.
7. `#eval(Name(N), env(N, V), _FUNS) => V`.
   Correct lookup for the exact one-binding environment.
8. `#eval(Bool(B), _ENV, _FUNS) => boolVal(B)`.
   Correct literal evaluation.
9. `#eval(BoolOp("or", E1, E2), ENV, FUNS)` evaluates both and calls
   `#boolOr`. This is eager rather than short-circuiting, but both operands in
   the exact submitted body are pure, total comparisons on every claimed
   finite integer list. It therefore preserves result, state, control, and
   exceptions on the claim domain.
10. `#boolOr(boolVal(B1), boolVal(B2))` uses K `orBool`. Correct for the two
    Boolean comparison results.
11. `#eval(Compare(E1, CmpOp("==", E2)), ...)` evaluates the two expressions
    and calls `#equals`. This is the exact one-comparison shape used twice.
12. `#equals(listVal(L1), listVal(L2))` uses structural `#eqIntLists`.
    Correct Python list equality for integer elements.
13. Ascending `Call(Name("sorted"), E)` evaluates `E`, unwraps the integer
    list, and applies `#sortInts`. The exact module has no rebinding of
    `sorted`, and `E` is the pure parameter lookup.
14. `Call(Name("sorted"), E, KwArg("reverse", Bool(true)))` applies
    `#reverseInts(#sortInts(...))`. This is exactly the second call shape; the
    keyword value is a literal, so omitting a separate expression-evaluation
    step has no observable effect.
15. `#asIntList(listVal(L)) => L`. Correct on every reachable call.
16. `#sortInts(nil) => nil`.
17. `#sortInts(cons(I, L)) => #insertInt(I, #sortInts(L))`.
    Rules 16–17 are constructor-exhaustive and structurally descending.
18. `#insertInt(I, nil) => cons(I, nil)`.
19. At a nonempty list, insert before `J` when `I <=Int J`.
20. Otherwise retain `J` and recurse when `I >Int J`.
    Rules 19–20 have mutually exclusive and exhaustive integer guards; rule 20
    descends structurally. Together rules 16–20 implement ascending insertion
    sort over mathematical integers.
21. `#reverseInts(nil) => nil`.
22. Reverse a cons by reversing its tail and appending its head singleton.
23. `#appendInts(nil, L2) => L2`.
24. Append a cons by retaining its head and recursively appending its tail.
    Rules 21–24 are constructor-exhaustive and structurally descending.
25. `#eqIntLists(nil, nil) => true`.
26. `#eqIntLists(nil, cons(...)) => false`.
27. `#eqIntLists(cons(...), nil) => false`.
28. Two cons lists are equal iff heads are `==Int` and tails recursively equal.
    Rules 25–28 are constructor-exhaustive, nonoverlapping, and descending.

No rule in this list is labeled unsound on the intended finite-integer subdomain,
so there is no false-conclusion witness to report for a semantic rule. The
semantics is intentionally not a general Python semantics. In particular,
first-match function lookup would not model Python's rebinding behavior for a
different module containing repeated definitions, and many accepted syntax
forms are only partially evaluated. Those configurations are not reachable
from the fixed submitted module and are not used to prove a general language
theorem.

## Rules in `verification.k`

29. `solutionProgram => Module(FuncDef(...))` is a definitional program
    constant. A reviewer token comparison found exact identity with the trusted
    translator output (82 tokens and the same token SHA-256). It names rather
    than skips the submitted body, and the body-sensitivity test shows its
    execution matters.
30. `#monotonicSpec(L)` is the Boolean disjunction of equality with ascending
    insertion sort and equality with the reverse of ascending insertion sort.
    This is a definitional postcondition, not an operational bridge. For a
    finite list over a total integer order, the two disjuncts are respectively
    equivalent to nondecreasing and nonincreasing order. That elementary
    equivalence is reviewed informally rather than proved as a separate K
    theorem.

Neither rule is opaque. The value-bearing operations in rule 30 reduce through
the exhaustive equations above.

## Claims in `spec.k`

1. Universally, for `L : IntList`, executing the exact program on `listVal(L)`
   reaches `#monotonicSpec(L)`. It has implicit precondition `true`.
2. The increasing prompt list reaches `boolVal(true)`, precondition `true`.
3. The nonmonotonic prompt list reaches `boolVal(false)`, precondition `true`.
4. The decreasing prompt list reaches `boolVal(true)`, precondition `true`.

The configuration contains only `<k>`. The submitted computation is pure:
there is no source-visible mutation, I/O, exception handler, heap identity test,
or alias observation requiring another cell. Python's allocation of a fresh
list for `sorted` is unobservable in this body because the list is used only in
structural equality.

## Used-construct coverage map

| Submitted constructor/operation | Declaration and behavior |
| --- | --- |
| `Module` | `Pgm` declaration; rules 3–5 |
| `FuncDef`, `Params` | `Stmt`/`Params`; rules 1, 4, 5 |
| `Return` | `Stmt`; rule 6 |
| parameter `Name("l")` | `Expr`; rule 7 |
| builtin `Name("sorted")` in the two exact call shapes | `Expr`; rules 13–14 |
| `BoolOp("or", ...)` | `Expr`; rules 9–10 |
| `Compare(..., CmpOp("==", ...))` | `Expr`/`CmpOp`; rules 11–12 and 25–28 |
| ascending `Call` | `Expr`; rules 13, 15–20 |
| reverse `Call` with `KwArg("reverse", Bool(true))` | `Expr`; rules 14–24 |
| input and result values | `IntList`/`Val`; constructor rules above |

Every constructor in `solution.mpy` is mapped. There is no fabricated
fallback result for an unmodeled used construct.

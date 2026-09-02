# Reviewer rule and declaration inventory

This inventory is reviewer-authored from `/candidate/semantic.k`,
`/candidate/verification.k`, and `/candidate/spec.k`. There are no other
candidate helper `.k` sources.

## Local syntax declarations

`MPY-SYNTAX`:

| Lines | Sort | Production(s) | Used by `solution.mpy` |
|---|---|---|---|
| 6 | `Pgm` | `Module(Stmts)` | yes |
| 8 | `Stmts` | delimiter-free list of `Stmt` | yes |
| 9-11 | `Stmt` | `FuncDef(String,Params,Stmts)`; `Return(Expr)`; `If(Expr,Stmts,Stmts)` | all three |
| 13 | `Params` | `Params(Strings)` | yes |
| 14 | `Strings` | comma-separated list of `String` | yes |
| 16-20 | `Expr` | `Int(Int)`; `Name(String)`; `BinOp(String,Expr,Expr)`; `Compare(Expr,CmpOps)`; `ListExpr(Exprs)` | all five |
| 22 | `CmpOp` | `CmpOp(String,Expr)` | yes |
| 23 | `CmpOps` | comma-separated list of `CmpOp` | yes, singleton |
| 24 | `Exprs` | comma-separated list of `Expr` | yes, pairs |
| 26 | `Args` | `args(Int,Int,Int)` | harness only |
| 27 | `Result` | `result(Int,Int)` | observable result |

`SEMANTIC`:

| Lines | Sort | Production(s) | Attributes |
|---|---|---|---|
| 34-36 | `PyVal` | `intVal(Int)`; `boolVal(Bool)`; `listVal(PyVals)` | constructors |
| 37 | `PyVals` | comma-separated list of `PyVal` | list production |
| 39-40 | `Outcome` | `normal`; `returned(PyVal)` | constructors |
| 42 | `KItem` | `run(Pgm,Args)` | entry computation |
| 45 | `Result` | `carrotContract(Int,Int,Int)` | `function,total` |
| 46 | `Bool` | `validInput(Int,Int,Int)` | `function,total` |
| 47 | `Pgm` | literal `solutionProgram` | `function` |
| 49 | `PyVal` | `lookup(String,Map)` | `function,total` |
| 52 | `PyVal` | `evalExpr(Expr,Map)` | `function,total` |
| 64-66 | `PyVal` | `addVals`; `subVals`; `leVals`, each on `(PyVal,PyVal)` | each `function,total` |
| 74-77 | `Outcome` | `evalStmts(Stmts,Map)`; `evalStmt(Stmt,Map)`; `continueWith(Outcome,Stmts,Map)`; `chooseBranch(PyVal,Stmts,Stmts,Map)` | each `function,total` |
| 90 | `Result` | `resultOf(Outcome)` | `function,total` |

There are no local `[functional]`, `[simplification]`, priority, `owise`,
macro, alias, hook, freshness, or explicit opaque-symbol declarations.
`solutionProgram` is a non-total function declaration; all other local function
declarations carry `[total]`.

## Configuration

Lines 93-96 define exactly `<mpy><k>run($PGM,$ARGS)</k></mpy>`. There are no
store, heap, stack, I/O, allocation, exception, or other state cells. The
read-only local environment needed by this program is an explicit `Map`
argument threaded through evaluator functions.

## `semantic.k` rules

| ID | Lines | Rule | Class and review |
|---|---|---|---|
| S1 | 50 | `lookup(X,(X |-> V) REST) => V` | Environment lookup. True for K maps when the key is present; the entry rule supplies all three names used. |
| S2 | 53 | `evalExpr(Int(I),_) => intVal(I)` | Literal evaluation; exact. |
| S3 | 54 | `evalExpr(Name(X),RHO) => lookup(X,RHO)` | Name evaluation; exact on the supplied environment. |
| S4 | 55-56 | `evalExpr(BinOp("+",L,R),RHO)` delegates to `addVals` | Exact for the used pure integer expression. |
| S5 | 57-58 | `evalExpr(BinOp("-",L,R),RHO)` delegates to `subVals` | Exact for the used pure integer expression. |
| S6 | 59-60 | single `<=` comparison delegates to `leVals` | Exact for the used comparison shape. |
| S7 | 61-62 | two-element `ListExpr` evaluates to two-element `listVal` | Exact content abstraction for the returned list. |
| S8 | 67 | integer `addVals` uses `+Int` | Exact: K and Python integers are unbounded here. |
| S9 | 68 | integer `subVals` uses `-Int` | Exact: K and Python integers are unbounded here. |
| S10 | 69-70 | `leVals(intVal(A),intVal(B)) => true` if `A <= B` | True guard and result. |
| S11 | 71-72 | same comparison returns false if `B < A` | True; guards of S10/S11 are disjoint and exhaustive on integers. |
| S12 | 78 | empty statements evaluate to `normal` | Exact. |
| S13 | 79-80 | nonempty statements evaluate head then pass outcome and tail to `continueWith` | Sequential control. |
| S14 | 81 | `continueWith(normal,REST,RHO)` evaluates the tail | Exact fall-through. |
| S15 | 82 | `continueWith(returned(V),_,_) => returned(V)` | Exact early-return propagation. |
| S16 | 84 | `Return(E)` evaluates and returns `E` | Exact on pure used expressions. |
| S17 | 85-86 | `If` evaluates condition then calls `chooseBranch` | Exact on the used Boolean comparison. |
| S18 | 87 | true chooses `THEN` | Exact. |
| S19 | 88 | false chooses `ELSE` | Exact. |
| S20 | 91 | returned two-int `listVal` becomes `result(A,B)` | Observable-content projection; exact for every actual return. |
| S21 | 98-107 | exact `eat` module invocation binds three integer arguments and evaluates `BODY` | Entry-harness operational rule. It fixes name/signature, preserves body execution, and introduces no task answer. Its abstraction from Python call/list-allocation machinery is adequate for this pure entry point and content-only result. |

The nested evaluator calls do not encode an explicit Python left-to-right
evaluation context. Every actual subexpression is pure, reads an immutable map,
and cannot raise on the documented integer domain, so reordering cannot change
the result or control for this submitted program.

## `verification.k` rules

| ID | Lines | Rule | Class and review |
|---|---|---|---|
| V1 | 7-9 | contract result when `NEED <= REMAINING` | Definitional postcondition summary. The equation is ordinary integer/list-content mathematics and occurs only on the claim destination side. |
| V2 | 10-12 | contract result when `REMAINING < NEED` | Definitional postcondition summary. V1/V2 guards are disjoint and exhaustive for integers. |
| V3 | 14-17 | `validInput` is the conjunction of the three `0..1000` bounds | Exact transcription of the trusted prompt. |
| V4 | 20-35 | `solutionProgram` expands to the full constructor tree | Program-identity definition. Its RHS is structurally the submitted `solution.mpy`; translator byte identity and depth-zero parsing independently pin that tree. |

V1/V2 state the property to be proved; they do not occur in S1-S21 and do not
rewrite or skip program execution. V4 changes only a name for the exact program
term; it is not a result-bearing oracle.

## Claims

`spec.k` has six entry claims and no helper, loop, circularity, or lemma claims:
two symbolic claims partition the entire valid integer domain on
`NEED <= REMAINING` versus `REMAINING < NEED`; four ground claims reproduce the
documented examples.

## Partial coverage behind `[total]`

The following declarations are broader than their equations: `lookup` on an
absent key; `evalExpr` on unsupported operator/cardinality shapes; `addVals`,
`subVals`, and `leVals` on non-integers; `evalStmt` on a nested `FuncDef`;
`chooseBranch` on non-Booleans; and `resultOf` on a non-return or non-two-int
return. These are coverage gaps outside the submitted program, not alternate
rules capable of fabricating a task result. Every reachable use in the two
symbolic claims matches a concrete defining equation. A reviewer build with
all local `total` attributes removed is recorded separately to test that proof
closure does not rely on these over-broad declarations.

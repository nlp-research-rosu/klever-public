# Exhaustive local K inventory

Scope: the submitted `semantic.k`, `verification.k`, and `spec.k`. Imported
builtin modules are recorded as trust boundaries, not re-inventoried here.
There are no generated helper K files other than `verification.k`.

## Local syntax and configuration

`semantic.k`, module `MPY-SYNTAX`:

- `Program`: `Module(Stmts)`.
- `Stmts`: delimiter-free `List{Stmt, ""}`.
- `Stmt`: `FuncDef(String, Params, Stmts)`, `If(Expr, Stmts, Stmts)`,
  and `Return(Expr)`.
- `Strings`: comma-separated `List{String, ","}`; `Params` wraps it.
- `Exprs`: comma-separated `List{Expr, ","}`.
- `CmpOps`: comma-separated `List{CmpOp, ","}`.
- `Expr`: `Int(Int)`, `Name(String)`, `BinOp(String, Expr, Expr)`,
  `Compare(Expr, CmpOps)`, `ListExpr(Exprs)`, and
  `Call(Expr, Exprs)`.
- `CmpOp`: `CmpOp(String, Expr)`.

`semantic.k`, module `TRI-SEMANTIC`:

- `IntSeq`: `nil` or `cons(Int, IntSeq)`.
- `Value`: `IVal(Int)`, `BVal(Bool)`, or `LVal(IntSeq)`.
- `Result`: `returned(Value)` or `fellThrough`.
- Configuration: one `<k>` cell initialized to `run($PGM, $N)`.
- Fifteen `KItem` constructors: `run`, `evalCall`, `findCall`, `exec`,
  `doReturn`, `choose`, `afterBranch`, `evalExpr`, `binLeft`,
  `binRight`, `cmpLeft`, `cmpRight`, `singleton`, `callArg`, and
  `callDone`.
- Two partial K functions, neither declared `total`:
  `bin(String, Value, Value):Value` and
  `append(IntSeq, IntSeq):IntSeq`.

`verification.k`:

- `solutionProgram:Program` is a macro.
- `triValue(Int):Int` and `triPrefix(Int):IntSeq` are partial K
  functions; neither is declared `total`.

There are no local declarations with `total`, `functional`, `simplification`,
`concrete`, `owise`, priority, or opaque attributes. The only attributes are
`function` on `bin`, `append`, `triValue`, and `triPrefix`, and `macro` on
`solutionProgram`.

## Rules in `semantic.k`

| ID | Lines | Rule and complete local role | Static judgment |
|---|---:|---|---|
| S01 | 63 | `run(P,N) => evalCall(P,"tri",N)` in the framed `<k>` continuation. | Exact configured entry binding. |
| S02 | 65–66 | `evalCall(Module(DEFS),F,N) => findCall(DEFS,F,N,Module(DEFS))`. | Exact module lookup setup. Part of the unbounded-call abstraction discussed below. |
| S03 | 68–69 | A head `FuncDef(F,Params(_X),BODY)` executes `BODY` with integer argument `N`. | Exact for the submitted single parameter `Params("n")`; over-broad for other parameter lists, but no false conclusion is enabled for the submitted program. Part of the unbounded-call abstraction. |
| S04 | 70–72 | A differently named function is skipped when `G =/=String F`. | Guard-disjoint from S03 and exact lookup order. |
| S05 | 74 | `exec(.Stmts,...) => fellThrough`. | Correct empty-block result. |
| S06 | 75–76 | A leading `Return(E)` evaluates `E` then schedules `doReturn`, discarding following statements. | Correct evaluation and abrupt-return behavior for the supported subset. |
| S07 | 77 | `Value ~> doReturn => returned(Value)`. | Correct wrapping of a returned value. |
| S08 | 79–80 | A leading `If` evaluates its condition before `choose`, preserving the remaining statements. | Correct left-to-right control setup. |
| S09 | 81–82 | A true condition executes `THEN`, followed by `afterBranch(REST,...)`. | Correct selected-branch control. |
| S10 | 83–84 | A false condition executes `ELSE`, followed by `afterBranch(REST,...)`. | Disjoint from S09 and correct. |
| S11 | 85–86 | A returned branch result passes through `afterBranch` and discards `REST`. | Correct return propagation. |
| S12 | 87–88 | A fall-through branch continues with `REST`. | Correct continuation behavior. |
| S13 | 90 | `evalExpr(Int(I),...) => IVal(I)`. | Exact integer literal evaluation. |
| S14 | 91 | `evalExpr(Name("n"),N,...) => IVal(N)`. | Exact for every name occurrence in the submitted body; intentionally not a general environment semantics. |
| S15 | 92–93 | A `BinOp` evaluates its left operand first and records operator, right operand, argument, and program. | Correct Python operand order for the used pure expressions. |
| S16 | 94–95 | After the left value, evaluate the right operand and retain the left value. | Correct operand order. |
| S17 | 96–97 | After the right value, call partial function `bin(OP,V,W)`. | Correct dispatch; only covered combinations are reachable. |
| S18 | 99–100 | A one-element equality `Compare` evaluates its left operand first. | Exact for every submitted comparison. |
| S19 | 101–102 | After an integer left operand, evaluate the comparator and retain the left integer. | Correct order. |
| S20 | 103–104 | Integer equality produces `BVal(true)` when `A ==Int B`. | Correct guarded result. |
| S21 | 105–106 | Integer equality produces `BVal(false)` when `A =/=Int B`. | Guard-disjoint and exhaustive with S20. |
| S22 | 108–109 | A one-element `ListExpr(E)` evaluates `E` then schedules `singleton`. | Exact for both submitted list literals. |
| S23 | 110 | `IVal(I) ~> singleton => LVal(cons(I,nil))`. | Correct singleton list construction. |
| S24 | 112–113 | A named, single-argument call evaluates its argument before `callArg`. | Correct for both recursive call sites. Part of the unbounded-call abstraction. |
| S25 | 114–115 | The evaluated integer argument invokes `evalCall(P,F,A)` then schedules `callDone`. | Correct call binding for the exact module; part of the unbounded-call abstraction. |
| S26 | 116 | `returned(V) ~> callDone => V`. | Correct normal-call return; part of the model that has no exception/stack-limit path. |
| S27 | 118 | Integer `+` maps to K `+Int`. | Correct on the reachable integer operands. |
| S28 | 119 | Integer `-` maps to K `-Int`. | Correct on the reachable operands, including the recursive `n-1` call after the zero guard. |
| S29 | 120 | Integer `*` maps to K `*Int`. | Correct on the reachable operands. |
| S30 | 121 | Integer `%` maps to K `%Int`. | Correct for non-negative `n` and divisor 2. |
| S31 | 122 | Integer `//` maps to K `/Int`. | Correct for every reachable non-negative numerator and positive divisor 2. Its unguarded declaration is over-broad for other terms, but no contrary witness occurs on the intended submitted-program domain. |
| S32 | 123 | List `+` maps to `append`. | Correct for the immutable list values used here; there is no observable aliasing or mutation. |
| S33 | 125 | `append(nil,YS) => YS`. | Standard true list equation. |
| S34 | 126 | `append(cons(X,XS),YS) => cons(X,append(XS,YS))`. | Standard structurally descending list equation; disjoint from S33. |

The rules are pairwise constructor- or guard-disjoint wherever they share a
head. `bin` and `append` are not declared total, so their intentionally
incomplete off-subset coverage does not assert false totality.

### Concrete soundness failure in the call model

S02, S03, and S24–S26, together with the one-cell configuration, implement
recursive calls with an unbounded mathematical continuation and no CPython
recursion-depth check or `RecursionError` path. This is not merely an unused
language feature: the submitted program calls itself once for every positive
`n`.

False-conclusion witness on the intended domain: `n = 1100` satisfies
`n >= 0`. Fresh LLVM execution of these rules reaches
`returned(LVal(...))`, with a list of length 1101 ending in 551. The actual
submitted `solution.py` under the mounted CPython 3.10.12 runtime terminates
exceptionally with `RecursionError: maximum recursion depth exceeded in
comparison`; the trusted iterative canonical implementation returns the
1101-element result. Thus these locally ordinary call rules collectively
enable the entry claim's normal-return conclusion for a real-program input
where that conclusion is false.

## Rules in `verification.k`

| ID | Lines | Rule | Classification and judgment |
|---|---:|---|---|
| V01 | 7–28 | `solutionProgram` expands to the complete submitted constructor tree. | Syntax macro, not an execution bridge. Fresh `kast --expand-macros` KORE is byte-identical to parsed `solution.mpy`. |
| V02 | 33–34 | For non-negative even `N`, `triValue(N) = 1 + N/2`. | Truthful guarded definitional-summary equation. |
| V03 | 35–36 | For non-negative odd `N`, `triValue(N) = ((N+1)/2)*((N+5)/2)`. | Truthful guarded definitional-summary equation. V02/V03 guards are disjoint and cover all `N >= 0`. |
| V04 | 39 | `triPrefix(0) = cons(1,nil)`. | Truthful base definition. |
| V05 | 40–41 | For `N > 0`, append `triValue(N)` to `triPrefix(N-1)`. | Truthful structurally descending definition, disjoint from V04. |

V02–V05 do not replace an operational `evalCall`, `run`, or program
expression. The exact execution-to-summary connection is the first reachability
claim in `spec.k`, used coinductively at the exact recursive-call configuration.
There is no fresh opaque result, oracle, priority rule, or same-symbol
operational shortcut.

For odd `N = 2k+1`, V03 is `(k+1)(k+3)`. For `k >= 1`, the recurrence right
side is `(k+1) + k(k+2) + (k+2) = (k+1)(k+3)`, justifying the submitted odd
recurrence claim. The even and base equations are immediate.

## Claims in `spec.k`

| ID | Lines | Plain-language statement |
|---|---:|---|
| C01 | 8–10 | For every integer `N >= 0`, interpreting the exact `tri` binding and body returns `triPrefix(N)`. This claim is also the recursive circularity. |
| C02 | 13–15 | The configured `run` entry point for the exact program returns `triPrefix(N)` for every `N >= 0`; it depends on C01. |
| C03 | 18 | `triValue(0) = 1`. |
| C04 | 19 | `triValue(1) = 3`. |
| C05 | 20–21 | Every even `N >= 2` satisfies the prompt's even clause. |
| C06 | 22–25 | Every odd `N >= 3` satisfies the prompt's stated recurrence. |

All six claims closed in the clean reconstruction. C03–C06 were reported by
the backend as trivial after applying truthful function equations. C01 and C02
are result-constraining in the generated semantics; they are not tautologies.
Their limitation is the generated call semantics' false normal-return behavior
for sufficiently deep real CPython recursion.

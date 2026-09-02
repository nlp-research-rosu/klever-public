# Exhaustive local K inventory

Scope: `/candidate/semantic.k`, `/candidate/verification.k`, and `/candidate/spec.k`.
There are no other candidate helper K files. Imports from K's standard library
are part of the toolchain trust boundary, not locally authored extensions.

## Syntax and declarations

| ID | Location | Declaration | Used role and assessment |
|---|---|---|---|
| S1 | semantic.k:5 | `Program ::= Module(Stmts)` | Exact outer constructor emitted by the trusted translator. |
| S2 | semantic.k:7 | `Stmts ::= List{Stmt,""}` | Exact empty/cons statement-list constructor. Both forms execute under R2/R3. |
| S3 | semantic.k:8 | `Stmt ::= FuncDef(...)` | Used by the submitted module; registered by R4. |
| S4 | semantic.k:9 | `Stmt ::= If(...)` | Used by the submitted body; evaluated by R15-R17. |
| S5 | semantic.k:10 | `Stmt ::= Return(Expr)` | Used in both program paths; evaluated by R21-R24. |
| S6 | semantic.k:12 | `Params ::= Params(String)` | Used by the one-argument definition and R4/R20. |
| S7 | semantic.k:14 | `Expr ::= Int(Int)` | Used for constants 1 and 2; R6. |
| S8 | semantic.k:15 | `Expr ::= Name(String)` | Used for `n` and direct `fib`; R7/R18. |
| S9 | semantic.k:16 | `Expr ::= BinOp(String,Expr,Expr)` | Used for `+` and `-`; R8-R11. |
| S10 | semantic.k:17 | `Expr ::= Compare(Expr,CmpOp)` | Used for `n <= 1`; R12-R14. |
| S11 | semantic.k:18 | `Expr ::= Call(Expr,Expr)` | Used for direct recursive calls; R18-R20. |
| S12 | semantic.k:20 | `CmpOp ::= CmpOp(String,Expr)` | Used for `<=`; R12-R14. |
| S13 | semantic.k:29-35 | Four-cell configuration | `<k>` computation, external integer `<arg>`, local `<env>`, and immutable loaded `<functions>`. Every non-`k` cell is read or written. |
| S14 | semantic.k:37 | `Function ::= function(String,Stmts)` | Stored code closure for a one-parameter body. Constructor, not a K `[function]`. |
| S15-S26 | semantic.k:39-50 | `exec`, `topCall`, `eval`, `evalRight`, `applyBin`, `finishCompare`, `applyCompare`, `prepareCall`, `invoke`, `functionEnd`, `makeReturn`, `returned` | Internal control constructors, each consumed by one or more R1-R24 rules. |
| S27 | semantic.k:83 | `finishIf(Stmts,Stmts)` | Internal branch continuation consumed by R15/R16. |
| S28 | verification.k:6 | `fibMath(Int) [function]` | Result-bearing mathematical definition. It is not `total`; E1/E2 cover every `N >= 0` used by the proof and deliberately leave negative arguments undefined. |

No local `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
`[trusted]`, priority, `owise`, or opaque declarations exist.

## Operational rules in `semantic.k`

| ID | Lines | Rule and complete assessment |
|---|---|---|
| R1 | 52 | `Module(SS) => exec(SS) ~> topCall`. Sound task harness: loads the exact one-definition submitted module before calling the required `fib` entry point with `<arg>`. |
| R2 | 54 | `exec(.Stmts) => .K`. Correct termination of an empty translated statement list. |
| R3 | 55 | `exec(S SS) => S ~> exec(SS)`. Preserves source statement order. |
| R4 | 57-59 | Register a previously absent `FuncDef` binding and consume the definition. The guard and initial empty function map make the target's singleton registration deterministic. |
| R5 | 61-62 | `topCall` constructs the required `fib(ARG)` call. It is task-entry harness behavior, not a summary of the body. |
| R6 | 64 | `eval(Int(I)) => I`. Exact integer literal evaluation. |
| R7 | 65-66 | Integer name lookup from `<env>`. Exact for the sole local `n`; failure stays visible if absent or non-integer. |
| R8 | 68-69 | Start binary evaluation with the left operand. |
| R9 | 70-71 | After the left integer, evaluate the right operand. R8/R9 encode CPython's left-to-right order for the used pure operands. |
| R10 | 72 | Apply integer addition as `I +Int J`. K integers are unbounded, matching CPython integers for this program. |
| R11 | 73 | Apply integer subtraction as `I -Int J`. Same representation boundary as R10. |
| R12 | 75-76 | Start comparison with its left operand. |
| R13 | 77-78 | Evaluate the comparison's right operand second. |
| R14 | 79 | Apply `I <=Int J`. Exact for the submitted guard. |
| R15 | 81 | On `true`, execute only `THEN`. |
| R16 | 82 | On `false`, execute only `ELSE`. |
| R17 | 84 | Evaluate the test before choosing a branch. R15-R17 are disjoint and exhaustive for the Boolean result produced by R14. |
| R18 | 86 | For the used direct `Call(Name(F),ARG)`, evaluate `ARG` before invocation. |
| R19 | 87 | Convert the evaluated integer argument to `invoke(F,I)`. |
| R20 | 89-91 | Lookup the exact function binding, save the complete old environment in `functionEnd(RHO)`, replace locals by the singleton parameter binding, and execute the body. The function map and `<arg>` are unchanged. |
| R21 | 93 | Evaluate a return expression before transfer. |
| R22 | 94 | Convert the returned integer to the abrupt `returned(I)` marker. |
| R23 | 95 | Discard pending `exec` statement-list continuations belonging to the current function. A `functionEnd` delimiter inserted by R20 prevents crossing into caller control. |
| R24 | 96-97 | At the matching `functionEnd`, restore the complete saved environment and expose the integer to the preserved caller continuation. |

The only state updates are R4 (function registration), R20 (enter call), and
R24 (restore caller environment). The recursive function has no heap, I/O,
exceptions, mutation, closures, defaults, or multi-argument behavior, so no
omitted cell can affect this submitted execution. Unsupported constructors or
operator strings stay visibly stuck.

## Mathematical equations in `verification.k`

| ID | Lines | Equation and assessment |
|---|---|---|
| E1 | 8-9 | `fibMath(N) = N` for `0 <= N <= 1`. True base cases. |
| E2 | 10-11 | `fibMath(N) = fibMath(N-1)+fibMath(N-2)` for `N > 1`. True Fibonacci recurrence and strictly descends to E1 over integers. |

E1 and E2 have disjoint guards. Together they cover all and only the
nonnegative inputs reachable under both claims. `fibMath` does not rewrite the
program's `invoke` or `Module`; it names the result to which fixed execution is
connected by the separately proven `fib-invoke` claim.

## Reachability claims in `spec.k`

| ID | Lines | Role and assessment |
|---|---|---|
| C1 | 6-20 | `fib-invoke`: for every `N >= 0`, arbitrary caller environment, arbitrary `<arg>`, and arbitrary continuation `REST`, executing the exact registered submitted body produces `fibMath(N)`, restores the environment, preserves the other cells, and leaves `REST` intact. This is the universal fixed-semantics connection theorem and recursive circularity. |
| C2 | 22-47 | `fib-module`: starting with the exact submitted module term, `ARG=N`, empty environment, and empty function map, registration and the entry harness return `fibMath(N)` and leave the exact loaded body in the function map. |

Both are `[all-path]`; neither has `ensures`, a fresh result variable, a
one-way Boolean postcondition, or a trust attribute. C1's exact function body
is the body mechanically extracted from the fresh translator output. C2's
entire left-hand `Module` is mechanically identical to that fresh output.

# Exhaustive local K inventory

Sources inventoried: the fresh copies of `semantic.k`, `verification.k`, and
`spec.k` from `/candidate`. There are no generated helper K files.

## Syntax, configuration, and contexts

`semantic.k` module `MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`.
- `Stmts`: a whitespace-separated `List{Stmt, ""}` with `.Stmts` unit.
- `Params`: exactly two `String` parameters.
- `Stmt`: `FuncDef`, `Assign`, `If`, `While`, and `Return`.
- `Cmp`: `CmpOp(String, Expr)`.
- `Expr`: `Int`, `Str`, `Name`, `TupleExpr`, `Subscript`, `BinOp`, and
  `Compare`.

`semantic.k` module `MPY` declares:

- `Value`: `intVal`, `strVal`, `boolVal`, `tupleVal`, and `unbound`.
- Subsort injections `Value < Expr` and `Value < KResult`.
- `Function`: `function(String, String, Stmts)`.
- `KItem` injections for `Program`, `Stmt`, `Stmts`, and `Expr`.
- Administrative `KItem`s: `runWith`, `saveFirstArg`, `saveSecondArg`,
  `invoke`, `assignTo`, `choose`, `loopGuard`, and `functionReturn`.
- Helper expression `compareValues(String, Expr, Expr)`.
- Configuration `<mpy>` containing `<k>`, `<functions>`, and `<env>`.
- Eight evaluation contexts: two each for `TupleExpr`, `Subscript`, `BinOp`,
  and `compareValues`. Each forces the left operand before the right.

`verification.k` declares four `[function]` symbols:

- `primeResult(Int, Int) : Value`
- `intersectionResult(Int, Int, Int, Int) : Value`
- `lengthResult(Int) : Value`
- `solutionProgram : Program`

There are no local `[total]` declarations, explicit `[functional]`
declarations, opaque symbols, macros, aliases, or `[simplification]` rules.
The sole explicit priority is `[priority(40)]` on P09 below.

## Operational semantics rules

| ID | Source | Rule and review |
|---|---|---|
| S01 | `semantic.k:65` | `Module(S) => S`; exposes the translated statement list. Sound. |
| S02 | `semantic.k:66` | `.Stmts => .K`; list-unit execution. Sound. |
| S03 | `semantic.k:67` | `S SS => S ~> SS`; preserves statement order. Sound. |
| S04 | `semantic.k:69-70` | Loads the sole two-argument function into an initially empty function map. Exact for this one-function module. |
| S05 | `semantic.k:72` | Starts first argument evaluation for `runWith`. Sound. |
| S06 | `semantic.k:73` | After argument 1 is a value, starts argument 2. Sound. |
| S07 | `semantic.k:74` | Invokes the literal `"intersection"` binding with both values. Sound for the fixed entry point. |
| S08 | `semantic.k:76-85` | Looks up the selected function body, binds both parameters, resets the local environment, and installs four unbound locals. Exact for the submitted body. |
| S09 | `semantic.k:88` | Evaluates an assignment RHS before storing. Sound for name targets. |
| S10 | `semantic.k:89-90` | Updates the named environment entry. Sound. |
| S11 | `semantic.k:92` | Evaluates an `If` guard before branch selection. Sound. |
| S12 | `semantic.k:93` | Selects the true branch. Sound. |
| S13 | `semantic.k:94` | Selects the false branch. Sound. |
| S14 | `semantic.k:96` | Evaluates a `While` guard. Sound. |
| S15 | `semantic.k:97` | On true, executes the body and reconstructs the same loop. Sound. |
| S16 | `semantic.k:98` | On false, exits the loop. Sound. |
| S17 | `semantic.k:102` | Evaluates a return expression and discards the remaining current-function continuation. It is broad as reusable language semantics, but all reachable target uses have exactly the current top-level function continuation, so it preserves the target behavior. |
| S18 | `semantic.k:103` | Leaves the evaluated return value in `<k>`. Sound. |
| S19 | `semantic.k:106` | `Int(I) => intVal(I)`. Sound. |
| S20 | `semantic.k:107` | `Str(S) => strVal(S)`. Sound. |
| S21 | `semantic.k:108-109` | Name lookup in `<env>`. Sound on bound target names. |
| S22 | `semantic.k:113` | Constructs a two-value tuple after ordered evaluation. Sound. |
| S23 | `semantic.k:117` | Tuple subscript 0. Sound. |
| S24 | `semantic.k:118` | Tuple subscript 1. Sound. |
| S25 | `semantic.k:122` | Integer addition. Sound against Python unbounded integers. |
| S26 | `semantic.k:123` | Integer subtraction. Sound against Python unbounded integers. |
| S27 | `semantic.k:124` | Integer multiplication. Sound against Python unbounded integers. |
| S28 | `semantic.k:125-126` | Integer modulo guarded by nonzero divisor. The target always has divisor at least 2. Sound. |
| S29 | `semantic.k:128` | Turns a one-link comparison into ordered operand evaluation. Exact for every submitted comparison. |
| S30 | `semantic.k:132` | Integer `<`. Sound. |
| S31 | `semantic.k:133` | Integer `<=`. Sound. |
| S32 | `semantic.k:134` | Integer `>`. Sound. |
| S33 | `semantic.k:135` | Integer `==`. Sound. |

## Verification rules

| ID | Source | Class and review |
|---|---|---|
| P01 | `verification.k:11-12` | Definitional equation: `primeResult(N,D)` is `YES` once `D^2>N`. |
| P02 | `verification.k:13-14` | Definitional equation: returns `NO` when the current divisor divides `N`. |
| P03 | `verification.k:15-16` | Definitional recursion: advances `D` when it is not a divisor. On the used domain `N>=2,D>=2`, P01-P03 are disjoint, exhaustive, and descending toward P01/P02. |
| P04 | `verification.k:20-21` | Definitional `intersectionResult`: lengths below 2 map to `NO`. |
| P05 | `verification.k:22-24` | Definitional `intersectionResult`: other lengths map to trial division from 2. P04/P05 are disjoint and exhaustive. This symbol is not used by an entry claim. |
| P06 | `verification.k:27` | Definitional `lengthResult`: lengths below 2 map to `NO`. |
| P07 | `verification.k:28` | Definitional `lengthResult`: other lengths map to trial division from 2. P06/P07 are disjoint and exhaustive. |
| P08 | `verification.k:34-63` | Definitional alias for the complete submitted constructor tree. The generated pin check closes after only making the four omitted empty statement lists explicit. |
| P09 | `verification.k:71-89` | **Unsound operational bridge.** It replaces the exact loop plus final `YES` return with `primeResult(N,D)`, reads `length` and `divisor`, and preserves all cells, including `divisor`. The bridge-free loop claim proves only an existential final divisor (`?_VD`), not preservation. Concrete false-conclusion witness: at `N=5,D=2`, fixed semantics returns `YES` with divisor 3, so the fixed-state-preservation claim fails; P09 makes the same false claim close with `#Top`. See `stage4.log`, `fixed-state-witness.k`, and `bridge-state-witness.k`. |

P01-P08 have no overlaps with inconsistent right-hand sides. P09 is the only
execution-replacing extension. Its `<k>` continuation is exact and its result
agrees with the bridge-free loop theorem, but its environment footprint is
strictly stronger than that theorem and false on a reachable intended-domain
state. Priority 40 causes it to preempt S14.

## Claims

| ID | Source | Formal role |
|---|---|---|
| C01 | `spec.k:10-27` | Bridge-free loop reachability claim for all `N>=2,D>=2`; result is `primeResult(N,D)`, while final divisor is existential. |
| C02 | `spec.k:37-49` | Valid intervals, `C<=A` and `D>=B`; result is `lengthResult(B-A)`. |
| C03 | `spec.k:51-63` | Valid intervals, `C<=A` and `D<B`; result is `lengthResult(D-A)`. |
| C04 | `spec.k:65-77` | Valid intervals, `C>A` and `D>=B`; result is `lengthResult(B-C)`. |
| C05 | `spec.k:79-91` | Valid intervals, `C>A` and `D<B`; result is `lengthResult(D-C)`. |

C02-C05 are mutually exclusive and exhaustive over `A<=B` and `C<=D`.
Their final function and environment maps are existentially unconstrained.

## Submitted-program construct coverage

Every constructor in `solution.mpy` is covered:

- module/function/list structure: S01-S08;
- `Assign`, `If`, `While`, `Return`: S09-S18;
- `Int`, `Str`, `Name`, runtime `TupleExpr`, and `Subscript`: S19-S24;
- submitted `+`, `-`, `*`, `%`: S25-S28;
- submitted `<`, `<=`, `>`, `==`: S29-S33.

No submitted construct relies on a fabricated default or an unmodeled fallback.

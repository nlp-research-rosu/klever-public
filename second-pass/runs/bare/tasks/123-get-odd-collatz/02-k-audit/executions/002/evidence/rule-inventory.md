# Reviewer rule and declaration inventory

Scope: the only local K sources are scratch copies of `semantic.k` and
`verification.k`. There are no generated helper K files. Imported K builtins
(`INT`, `STRING`, `BOOL`, and `MAP`) are the ordinary toolchain trust boundary,
not local extensions.

## Local syntax declarations

`MPY-SYNTAX` declares:

- `Pgm`: `Module(Stmts)`.
- K list sorts: `Stmts` (zero-delimiter sequence of `Stmt`), `Exprs`
  (comma-separated `Expr`), `Ids` (comma-separated `String`), and `CmpOps`
  (comma-separated `CmpOp`).
- `Stmt`: `FuncDef(String, Params(Ids), Stmts)`, `Assign(Expr, Expr)`,
  `If(Expr, Stmts, Stmts)`, `While(Expr, Stmts)`, and `Return(Expr)`.
- `Expr`: `Int(Int)`, `Name(String)`, `ListExpr(Exprs)`,
  `BinOp(String, Expr, Expr)`, `Compare(Expr, CmpOps)`, and
  `Call(Expr, Exprs)`.
- `CmpOp`: `CmpOp(String, Expr)`.

`SEMANTIC` declares:

- Runtime values: `Ints` (`.Ints` or `Int :: Ints`), `Value` (`vi`, `vb`,
  `vl`), `Function` (`function(String, Stmts)`), and `Result` (`noResult` or
  `result(Value)`).
- K controls: `run`, `load`, `start`, `exec`, `eval`, `assignTo`,
  `singleton`, `binLeft`, `binRight`, `cmpLeft`, `cmpRight`, `whileDecide`,
  `ifDecide`, `sortResult`, and `finish`.
- Functions: `applyBin` and `applyCmp` with `[function]`;
  `appendInts`, `insertInt`, and `sortInts` with `[function, total]`.
- Configuration cells: `<k>`, immutable `<input>`, function-map
  `<functions>`, local-map `<env>`, and `<result>`.

`VERIFICATION` declares:

- AST constants `collatzBranch : Stmt`, `collatzLoop : Stmt`, and
  `solutionProgram : Pgm`, each `[function, total]`.
- Observers `isSorted : Ints -> Bool` and `allOdd : Ints -> Bool`, each
  `[function, total]`.
- Non-functional K controls `checkSorted` and `checkAllOdd`.

There are no local `[functional]` declarations, opaque/fresh symbols, priority
rules, syntax macros, or `[simplification]` rules.

## Every rule in `semantic.k`

All line references are to `/candidate/semantic.k`.

| ID | Line | Rule | Review |
|---|---:|---|---|
| S01 | 71 | `run(Module(S)) => load(S) ~> start` | Sound module-loading sequence for the target. |
| S02 | 73 | Load a one-parameter `FuncDef` into `<functions>` | Sound for the submitted one-function, one-parameter module. |
| S03 | 75 | `load(.Stmts) => .K` | Sound list base case. |
| S04 | 77 | `start` selects `get_odd_collatz`, binds input to its parameter, and executes its body | Sound harness entry-point rule for this task; the initial map and exact binding are pinned by entry claims. |
| S05 | 83 | Decompose assignment into expression evaluation, `assignTo`, and remaining statements | Sound left-to-right sequencing for the used `Name` l-values. |
| S06 | 85 | Store evaluated assignment value in `<env>` | Sound local rebinding. |
| S07 | 88 | Decompose `If` into test and decision continuation | Sound evaluation order. |
| S08 | 90 | True `If` executes THEN then REST | Sound. |
| S09 | 92 | False `If` executes ELSE then REST | Sound. |
| S10 | 95 | Decompose `While` into test and decision continuation | Sound. |
| S11 | 97 | True `While` executes BODY then recreates loop before REST | Sound loop control. |
| S12 | 99 | False `While` executes REST | Sound. |
| S13 | 102 | Top-level `Return` evaluates its expression then `finish`es | Sound on the submitted top-level-return context. It intentionally lacks complete nested-return semantics; no used construct reaches that omitted context. |
| S14 | 103 | `finish` consumes the frame, clears locals/functions, and publishes result | Sound for the sole top-level call; cleared local state is unobservable in this model. |
| S15 | 107 | Empty statement sequence consumes itself | Sound list base case. |
| S16 | 110 | Evaluate integer literal to `vi` | Sound. |
| S17 | 111 | Evaluate name by exact map lookup | Sound and preserves binding. |
| S18 | 114 | Evaluate empty list to `vl(.Ints)` | Sound for an unaliased fresh empty list. |
| S19 | 115 | Evaluate a singleton list's sole expression | Sound for the target's `[n]` and `[1]`. Multi-element literals are deliberately unmodeled but unused. |
| S20 | 116 | Package evaluated singleton integer as `vl(I :: .Ints)` | Sound for integer elements used here. |
| S21 | 118 | Start binary operator with LEFT | Sound left-to-right order. |
| S22 | 120 | After LEFT, evaluate RIGHT | Sound left-to-right order. |
| S23 | 122 | Apply binary operator to two values | Sound dispatch; unsupported pairs remain visibly stuck. |
| S24 | 125 | Start one-comparator comparison with LEFT | Sound for every comparison in the program. Chained comparisons are unmodeled but unused. |
| S25 | 127 | After comparison LEFT, evaluate RIGHT | Sound. |
| S26 | 129 | Apply comparator | Sound dispatch. |
| S27 | 132 | Evaluate the sole argument of the builtin binding `sorted` | Sound for the fixed builtin call in the submitted AST. |
| S28 | 134 | Sort an integer-list value | Sound result rule. |
| S29 | 137 | Integer `+` | Ordinary unbounded integer addition. |
| S30 | 138 | Integer `*` | Ordinary unbounded integer multiplication. |
| S31 | 139 | Integer `%` for nonzero divisor | Agrees with Python on every used state: numerator nonnegative and divisor `2`. The function is partial rather than falsely total. |
| S32 | 140 | Integer `//` as `/Int` for nonnegative dividend and positive divisor | Agrees with Python floor division over the complete reachable domain; unsupported signs stop. |
| S33 | 141 | List `+` as immutable append | Observationally sound because the target has no aliases or mutation. |
| S34 | 144 | Integer `==` true branch | Guard is truthful. |
| S35 | 145 | Integer `==` false branch | Disjoint, exhaustive complement of S34. |
| S36 | 146 | Integer `!=` true branch | Guard is truthful. |
| S37 | 147 | Integer `!=` false branch | Disjoint, exhaustive complement of S36. |
| S38 | 150 | Append empty prefix | Correct base equation. |
| S39 | 151 | Append cons prefix recursively | Correct, structurally descending equation. Together S38/S39 cover all `Ints`. |
| S40 | 155 | Insert into empty list | Correct base equation. |
| S41 | 156 | Insert before head when `I <= J` | Correct. |
| S42 | 157 | Recurse past head when `I > J` | Correct and structurally descending. S41/S42 guards are disjoint and exhaustive. |
| S43 | 160 | Sort empty list | Correct base equation. |
| S44 | 161 | Insertion-sort cons list | Correct and structurally descending. |

The `[total]` declarations S38–S44 have constructor-complete, disjoint
equations. `applyBin` and `applyCmp` correctly remain partial for unused
operator/value combinations. No local rule overlaps another operational rule
on the same control head except through disjoint Boolean or arithmetic guards.

## Every rule in `verification.k`

All line references are to `/candidate/verification.k`.

| ID | Line | Rule | Class and review |
|---|---:|---|---|
| V01 | 10 | Expand `collatzBranch` | Definitional AST constant. Its expansion is exactly the translated `If` body; it does not replace execution. |
| V02 | 19 | Expand `collatzLoop` | Definitional AST constant using V01; exact translated `While`. |
| V03 | 23 | Expand `solutionProgram` | Definitional AST constant using V02; depth-one KORE comparison proves constructor identity with trusted-regenerated `solution.mpy`. |
| V04 | 34 | `isSorted(.Ints) => true` | Truthful observer base equation. |
| V05 | 35 | `isSorted(singleton) => true` | Truthful observer singleton equation. |
| V06 | 36 | Recursive adjacent-order `isSorted` equation | Truthful, structurally descending; list-shape cases V04–V06 are disjoint and exhaustive. |
| V07 | 40 | `allOdd(.Ints) => true` | Truthful observer base equation. |
| V08 | 41 | Recursive remainder-and-tail `allOdd` equation | Truthful over the program's positive integer outputs and structurally descending; disjoint/exhaustive with V07. |
| V09 | 48 | `checkSorted(IS) => isSorted(sortInts(IS))` | Observer-only operational wrapper; it does not occur in program execution or an entry postcondition. |
| V10 | 49 | `checkAllOdd(IS) => allOdd(IS)` | Observer-only operational wrapper; it does not occur in program execution or an entry postcondition. |

V01–V03 are fully defined nullary constants, so their `[total]` annotations
are covered. V04–V08 have exhaustive constructor cases. V09–V10 are not
operational bridges for the submitted program; they define separate validation
commands used only by two ground claims.

## Construct-to-rule coverage for `solution.mpy`

| Submitted construct | Declaration | Execution rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `Pgm`, `Stmt`, `Ids` | S01–S04 |
| `Assign(Name(...), ...)` | `Stmt`, `Expr` | S05–S06, S17 |
| `While` | `Stmt` | S10–S12 |
| `If` | `Stmt` | S07–S09 |
| `Return` | `Stmt` | S13–S15 |
| `Int`, `Name` | `Expr` | S16–S17 |
| Empty/singleton `ListExpr` | `Expr`, `Exprs` | S18–S20 |
| `BinOp` with `+`, `*`, `%`, `//` | `Expr` | S21–S23, S29–S33, S38–S39 |
| `Compare` with `==`, `!=` | `Expr`, `CmpOp`, `CmpOps` | S24–S26, S34–S37 |
| `Call(Name("sorted"), ...)` | `Expr` | S27–S28, S40–S44 |

Every constructor and material operation in the submitted program is modeled.
The generated semantics is deliberately incomplete outside this set, but
unmodeled unused constructs stop rather than fabricate a result. No semantic or
verification rule encodes a Collatz answer, introduces an oracle, or skips the
submitted loop.

# Exhaustive local K inventory

Source hashes are recorded in `01-integrity.log`. There are no other candidate
K/helper files.

## Syntax, attributes, and configuration

`MPY-SYNTAX` declares abstract sorts `Program`, `Params`, `Stmt`, `Expr`, and
`CmpOp`; `Stmts` is `List{Stmt, ""}`. Its constructors are:

- `Module(Stmts)`, `Params(String)`
- `FuncDef(String,Params,Stmts)`, `Assign(Expr,Expr)`,
  `While(Expr,Stmts)`, `If(Expr,Stmts,Stmts)`, `Return(Expr)`
- `Int(Int)`, `Name(String)`, `BinOp(String,Expr,Expr)`,
  `Compare(Expr,CmpOp)`, `CmpOp(String,Expr)`
- `Invoke(Program,String,Int)` as a `KItem`

`MPY-SEMANTICS` adds computation items `exec`, `execStmt`, `eval`, `binLeft`,
`binRight`, `compareLeft`, `compareRight`, `write`, `ifCont`, `loop`,
`loopCont`, and `doReturn`.

The configuration is `<mpy>` containing:

- `<k>`: active computation
- `<n>`: the parameter/local `n`
- `<acc>`: source local `result`
- `<digit>`: source local `digit`
- `<answer>`: returned value

`VERIFICATION` adds `CheckProgram(Program,Program)` and `ProgramsMatch`, plus
seven `[function,total]` declarations: nullary `digitsCond`,
`digitsLoopBody`, and `SolutionProgram`; binary `addOddDigit`,
`oddProductFrom`, and `finalScratchDigit`; and unary `oddProduct`.

There are no `[simplification]`, `[concrete]`, priority, `owise`,
`functional`, or opaque declarations.

Every constructor in `solution.mpy` is declared and used as follows:

| Constructor | Count | Declaration/behavior |
|---|---:|---|
| Module | 1 | invocation rule unwraps the sole matching function |
| FuncDef | 1 | invocation rule checks function name and parameter `"n"` |
| Params | 1 | invocation rule |
| Assign | 5 | S04 plus S23-S25 |
| While | 1 | S06 plus S28-S30 |
| If | 2 | S05 plus S26-S27 |
| Return | 1 | S07 and S31 |
| Int | 7 | S08 |
| Name | 14 | S09-S11 |
| BinOp | 4 | S12-S16 |
| Compare | 3 | S17-S22 |
| CmpOp | 3 | S17-S22 |

## `semantic.k`: all 31 rules

| ID | Rule role | Review |
|---|---|---|
| S01 | `Invoke(Module(FuncDef(F,Params("n"),BODY)),F,N)` initializes cells and executes `BODY` | Exact for this one-function submitted module and direct named call; repeated `F` pins the binding. It is a deliberately narrow call harness. |
| S02 | `exec(.Stmts) => .K` | Correct empty sequence. |
| S03 | `exec(S SS) => execStmt(S) ~> exec(SS)` | Correct left-to-right statement order. |
| S04 | assignment dispatch | Evaluates RHS before write, matching the used Python assignments. |
| S05 | conditional dispatch | Evaluates condition before choosing a branch. |
| S06 | while dispatch | Enters the stable loop term. |
| S07 | return dispatch | Evaluates return expression before abrupt return. |
| S08 | integer literal | Direct K integer value. |
| S09 | lookup `n` | Reads the correct cell. |
| S10 | lookup `result` | Reads `<acc>`. |
| S11 | lookup `digit` | Reads `<digit>`. |
| S12 | binary dispatch | Starts with the left operand. |
| S13 | binary continuation | Evaluates the right operand second and retains the left value. |
| S14 | `%` | Correct for every reached nonnegative dividend and positive divisor; globally differs from Python for negative dividends (documented concern). |
| S15 | `//` | Correct for every reached nonnegative dividend and positive divisor; globally differs from Python floor division for negative dividends (documented concern). |
| S16 | `*` | Exact unbounded integer multiplication. |
| S17 | comparison dispatch | Starts with the left operand. |
| S18 | comparison continuation | Evaluates the right operand second. |
| S19 | `>` true | Produces integer truth value 1 under the exact guard. |
| S20 | `>` false | Produces 0 under the complementary guard. |
| S21 | `==` true | Produces 1 under equality. |
| S22 | `==` false | Produces 0 under disequality. |
| S23 | write `n` | Updates only `<n>`. |
| S24 | write `result` | Updates only `<acc>`. |
| S25 | write `digit` | Updates only `<digit>`. |
| S26 | conditional nonzero | Executes only THEN; correct truthiness for the integer conditions reached here. |
| S27 | conditional zero | Executes only ELSE; guard complements S26. |
| S28 | loop condition dispatch | Reevaluates the condition on every visit. |
| S29 | loop nonzero | Runs body, then returns to the same loop head. |
| S30 | loop zero | Leaves the loop; guard complements S29. |
| S31 | `doReturn` | Stores the value and discards the remaining function-body continuation. All material cells are either updated (`answer`) or deliberately preserved. |

S19/S20, S21/S22, S26/S27, and S29/S30 have disjoint, exhaustive guards.
There are no rule priorities. The only state-writing rules are S01,
S23-S25, and S31; their footprints match the submitted program.

## `verification.k`: all 12 rules

| ID | Rule/function | Class and review |
|---|---|---|
| V01 | `digitsCond` expansion | Definitional syntax summary; single exhaustive nullary equation; exact constructor term. |
| V02 | `digitsLoopBody` expansion | Definitional syntax summary; single exhaustive nullary equation; exact constructor term. |
| V03 | `SolutionProgram` expansion | Definitional syntax summary; exact module/function/body term. Trusted regeneration plus `ProgramsMatch` mechanically establishes constructor identity. |
| V04 | `CheckProgram(P,P) => ProgramsMatch` | Ordinary reflexive structural-equality test helper. It does not occur in either proof claim and cannot rewrite unequal ground programs. |
| V05 | even `addOddDigit` | Definitional mathematical summary; keeps accumulator. |
| V06 | odd digit, zero accumulator | Definitional summary; first odd digit becomes accumulator. |
| V07 | odd digit, nonzero accumulator | Definitional summary; multiplies. |
| V08 | `oddProductFrom` at `N <= 0` | Base equation. |
| V09 | `oddProductFrom` at `N > 0` | Recursive decimal fold; for positive N, `N /Int 10` is nonnegative and strictly smaller. |
| V10 | `oddProduct(N)` | Unguarded exhaustive wrapper equation. |
| V11 | `finalScratchDigit` at `N <= 0` | Base equation preserving incoming scratch value. |
| V12 | `finalScratchDigit` at `N > 0` | Recursive exact characterization of the final assigned decimal digit; descends as in V09. |

V05-V07 are pairwise disjoint and exhaustive for all integer `(A,D)`.
V08/V09 and V11/V12 are pairwise disjoint and exhaustive for all integer N.
Every recursive use relevant to the theorem descends. These summaries do not
replace operational execution: the loop claim connects S28-S30 and the entire
body execution to V05-V12.

## `spec.k`: both reachability claims

- C01, generalized loop claim: for `N >= 0`, executing the exact loop body
  from `<n>N</n>`, accumulator A, and scratch D reaches the continuation with
  n=0, accumulator `oddProductFrom(N,A)`, scratch
  `finalScratchDigit(N,D)`, and unchanged answer. This is the inductive
  operational connection theorem.
- C02, entry claim: for every K integer `N > 0`, direct invocation of the exact
  `SolutionProgram` terminates if execution reaches the destination with
  `<answer>` and `<acc>` both `oddProduct(N)`, n=0, the exact final scratch
  digit, and empty computation. The loop claim is its circularity/invariant.

Both claims mention the complete `<mpy>` configuration. No material cell is
omitted or unconstrained. The result-bearing answer is fixed, not fresh.

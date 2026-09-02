# Reviewer rule inventory

Scope: candidate-authored source only: `semantic.k`, `verification.k`, and the
two reachability claims in `spec.k`. There are no candidate-authored helper K
files. Built-in `domains.md` is recorded as a trusted K primitive boundary, not
reinventoried here.

## Local syntax and configuration

`semantic.k` declares the abstract sorts `Program`, `Params`, `Stmt`, `Stmts`,
`Expr`, and `CmpOp`; `Stmts` is a K list of `Stmt`. Its source constructors are:

- `Program`: `Module(Stmts)`
- `Params`: `Params(String)`
- `Stmt`: `FuncDef(String,Params,Stmts)`, `Assign(Expr,Expr)`,
  `While(Expr,Stmts)`, `If(Expr,Stmts,Stmts)`, and `Return(Expr)`
- `Expr`: `Int(Int)`, `Name(String)`, `BinOp(String,Expr,Expr)`, and
  `Compare(Expr,CmpOp)`
- `CmpOp`: `CmpOp(String,Expr)`
- top-level harness: `Invoke(Program,String,Int)`

The operational helper constructors are `exec`, `execStmt`, `eval`, `binLeft`,
`binRight`, `compareLeft`, `compareRight`, `write`, `ifCont`, `loop`,
`loopCont`, and `doReturn`.

The configuration has `<k>`, `<n>`, `<acc>`, `<digit>`, and `<answer>` cells.
Every non-`<k>` cell is read or written by a candidate rule. There is no heap,
I/O, allocation, exception, or call-stack cell because the submitted program
uses none of those features.

`verification.k` additionally declares `CheckProgram(Program,Program)` and
`ProgramsMatch`, and these total functions:

| Symbol | Arity | Defining rules | Totality/overlap decision |
|---|---:|---:|---|
| `digitsCond` | 0 | V01 | One unconditional equation; total and unique. |
| `digitsLoopBody` | 0 | V02 | One unconditional equation; total and unique. |
| `SolutionProgram` | 0 | V03 | One unconditional equation; total and unique. |
| `addOddDigit` | 2 | V05–V07 | Even/odd and accumulator-zero/nonzero guards are exhaustive and pairwise disjoint. |
| `oddProductFrom` | 2 | V08–V09 | `N <= 0` and `N > 0` are exhaustive/disjoint; positive recursion strictly decreases by division by 10. |
| `oddProduct` | 1 | V10 | One unconditional equation; total via `oddProductFrom`. |
| `finalScratchDigit` | 2 | V11–V12 | `N <= 0` and `N > 0` are exhaustive/disjoint; positive recursion strictly decreases. |

There are no local `[functional]` declarations, opaque or fresh symbols,
priority rules, `[simplification]` rules, `[concrete]` rules, or `owise` rules.
`CheckProgram` is deliberately partial and is not marked `function` or `total`.

## `semantic.k` operational rules

| ID (line) | Rule role | Static decision |
|---|---|---|
| S01 (58–63) | Invoke the sole matching `digits(n)` function and initialize all cells. | Sound for the submitted one-function module. The same `F` occurs in the definition and invocation, so binding is pinned. |
| S02 (65) | Empty statement list terminates. | Sound. |
| S03 (66) | Execute head statement, then tail. | Sound sequential control order. |
| S04 (68) | Assignment evaluates RHS before the named write. | Sound for all submitted assignments. |
| S05 (69–70) | `If` evaluates its condition, then chooses a branch. | Sound. |
| S06 (71) | Turn `While` into a recurring `loop`. | Sound and supplies the stable loop head used by the invariant. |
| S07 (72) | Evaluate return expression before `doReturn`. | Sound. |
| S08 (74) | Integer literal evaluates to its K integer. | Sound. |
| S09 (75) | Read `n`. | Sound; exact cell lookup. |
| S10 (76) | Read source variable `result` from `<acc>`. | Sound renaming, used consistently by writes and claims. |
| S11 (77) | Read `digit`. | Sound; exact cell lookup. |
| S12 (78) | Begin binary operation by evaluating the left operand. | Sound left-to-right order. |
| S13 (79) | After the left value, evaluate the right operand and retain the left. | Sound left-to-right order. |
| S14 (80) | Implement `%` with K `%Int`. | Sound on every reachable theorem state because both operands are nonnegative and divisors are 10 or 2. K remainder differs from Python for negative dividends; that broader language gap is outside `N > 0` and cannot enable a false intended-domain conclusion. |
| S15 (81) | Implement `//` with K `/Int`. | Sound on every reachable theorem state because the dividend is nonnegative and divisor is 10. K division truncates rather than Python-floors for negatives; this is an out-of-domain coverage limitation, not an intended-domain unsoundness. |
| S16 (82) | Implement multiplication with `*Int`. | Sound unbounded-integer multiplication. |
| S17 (84–85) | Begin comparison by evaluating its left operand. | Sound. |
| S18 (86–87) | Evaluate comparison right operand after retaining left. | Sound left-to-right order. |
| S19 (88) | `>` true case yields integer truth value 1. | Sound, and guard is disjoint from S20. |
| S20 (89) | `>` false case yields 0. | Sound, and S19/S20 cover all integers. |
| S21 (90) | `==` true case yields 1. | Sound, and guard is disjoint from S22. |
| S22 (91) | `==` false case yields 0. | Sound, and S21/S22 cover all integers. |
| S23 (93) | Write `n`. | Sound exact cell update; other cells are framed. |
| S24 (94) | Write source `result` to `<acc>`. | Sound consistent renaming. |
| S25 (95) | Write `digit`. | Sound exact cell update. |
| S26 (97–98) | Nonzero condition executes then-branch. | Sound for integer truth values and disjoint from S27. |
| S27 (99–100) | Zero condition executes else-branch. | Sound and exhaustive with S26. |
| S28 (102) | Evaluate loop condition. | Sound. |
| S29 (103–105) | Nonzero condition executes body and returns to same loop head. | Sound; body precedes recurrence, with all cells preserved except through body rules. |
| S30 (106–107) | Zero condition exits loop. | Sound and disjoint/exhaustive with S29. |
| S31 (109–110) | Return discards the remaining function-local continuation and records the value. | Sound for this top-level invocation model. In the real execution the discarded suffix is the empty `exec` tail; no caller frame exists in the modeled language. |

## `verification.k` rules

| ID (line) | Class and role | Static decision |
|---|---|---|
| V01 (12–13) | Definitional macro for exact loop condition. | Sound constructor equality; it expands to the submitted AST. |
| V02 (16–25) | Definitional macro for exact loop body. | Sound constructor equality; statement order and both nested branches match regenerated `solution.mpy`. |
| V03 (30–35) | Definitional macro for the complete program. | Sound constructor equality; independently checked structurally against trusted regeneration. |
| V04 (39) | Partial structural equality witness. | Sound reflexivity only: it rewrites exactly when both constructor trees unify. |
| V05 (44–45) | `addOddDigit`: even digit keeps accumulator. | Sound definition of the requested fold. |
| V06 (46–47) | `addOddDigit`: first odd digit replaces sentinel zero. | Sound; a reachable odd decimal digit is never zero. |
| V07 (48–49) | `addOddDigit`: later odd digit multiplies accumulator. | Sound. |
| V08 (53–54) | Fold base case for nonpositive `N`. | Sound for the claim domain `N >= 0`; only `N=0` is reached. Its negative behavior is outside the theorem. |
| V09 (55–57) | Fold positive `N` by least-significant decimal digit. | Sound; quotient/remainder are the next decimal decomposition and recursion descends. |
| V10 (60) | Name the fold from sentinel zero. | Sound definitional summary; it does not replace operational execution. |
| V11 (65–66) | Scratch-digit base case. | Sound for reachable `N=0`. |
| V12 (67–69) | Track the last processed decimal digit recursively. | Sound and descending for positive `N`. |

V01–V03 are macros that expose the real constructor program to the operational
semantics. V05–V12 occur only in claim destinations and do not rewrite or
bypass the source program. No rule maps `Invoke`, `loop`, or another
property-bearing operational term directly to `oddProduct`.

## Construct coverage

The trusted AST inventory uses exactly `Module`, `FuncDef`, one `Params`,
`Assign`, `While`, `If`, `Return`, `Name`, `Int`, `BinOp` with `%`, `//`, and
`*`, `Compare` with `>` and `==`, and statement sequencing/empty else lists.
Each maps to the declarations and rules above. Every used variable is one of
`n`, `result`, or `digit`, and each has both read and write behavior where
needed. No submitted construct is silently fabricated or left unmodeled.

## Claims

- C01, loop invariant (`spec.k` 8–17): for any `N >= 0`, accumulator `A`,
  scratch digit `D`, answer value, and continuation `CONT`, executing the exact
  real loop consumes it, leaves `CONT`, sets `n` to zero, sets the accumulator
  to `oddProductFrom(N,A)`, sets scratch to `finalScratchDigit(N,D)`, and
  preserves answer. It follows actual loop control and constrains every
  state-changing cell.
- C02, entry contract (`spec.k` 20–28): for any positive `N`, executing the
  exact closed submitted program consumes all computation and returns
  `oddProduct(N)` in `<answer>`, with exact final `n`, accumulator, and scratch
  cells. `oddProduct(N)` is not free and is not used by operational execution,
  so the postcondition is result-constraining and non-circular.

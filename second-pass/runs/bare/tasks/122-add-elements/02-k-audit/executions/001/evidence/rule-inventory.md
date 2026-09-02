# Exhaustive local K inventory

Source hashes are recorded in `02-translation-identity.log`.  This inventory is
rebuilt from the copied source, not from candidate kompiled definitions.

## Syntax, attributes, data, and configuration

`semantic.k`, module `MPY-SYNTAX`:

1. `Program ::= Module(Stmts)`.
2. `Params ::= Params(String,String)`.
3. `Stmts ::= List{Stmt,""}` (juxtaposed statement sequence).
4. `Stmt` has `FuncDef`, `Assign`, `While`, `If`, and `Return`.
5. `Expr` has `Int`, `Name`, `UnaryOp`, `BinOp`, `BoolOp`, `Compare`, and
   `Subscript`.
6. `CmpOp ::= CmpOp(String,Expr)`.

`semantic.k`, module `MPY-SEMANTICS`:

7. `Value ::= Int | Bool | List`; `KResult ::= Value`.
8. `Result ::= noResult | result(Value)`.
9. `intAt(List,Int) : Int [function,total]`.
10. Administrative `KItem`s: `exec`, `setVar`, `ifBranches`, `whileBody`,
    `negate`, `addRight`, `addLeft`, `andRight`, `compareRight`,
    `lessThanLeft`, `subscriptIndex`, `getAt`, and `doReturn`.
11. Configuration `<mpy>` contains `<k>`, mutable `<env>`, immutable input
    `<arr>` and `<n>`, and `<result>`.

`verification.k`, module `MPY-VERIFICATION`:

12. `solutionLoop : Stmt [macro]`.
13. `solutionProgram : Program [macro]`.
14. `smallContribution(Int) : Int [function,total]`.
15. `sumRange(List,Int,Int) : Int [function,total]`.

There are no local `[functional]`, `[simplification]`, `[concrete]`, priority,
or `owise` declarations.  There are no proof-local ordinary operational
bridges.  The data constructors and administrative symbols have no opaque
result-bearing interpretations: each used administrative symbol has an
operational rule below.  The imported K built-ins remain part of the trust
boundary.

## Ordinary semantics rules

| ID | Source | Rule and role | Review |
|---|---|---|---|
| S01 | `semantic.k:41` | `intAt(ListItem(I) REST,0) => I` | Correct head lookup for a nonempty integer list. |
| S02 | `semantic.k:42-43` | Positive-index lookup drops one integer item and decrements the index. | Correct and descending for positive in-bounds indices in integer lists. |
| S03 | `semantic.k:70-74` | Exact `add_elements(arr,k)` module entry becomes `exec(BODY)` and binds input cells into an empty environment. | Correct for the submitted top-level function; no calls or alternate bindings exist. |
| S04 | `semantic.k:76` | Empty statement sequence completes. | Correct. |
| S05 | `semantic.k:77` | Nonempty sequence schedules its head before `exec(tail)`. | Correct source order. |
| S06 | `semantic.k:79` | Assignment evaluates the RHS before `setVar`. | Correct for the only used `Name` targets. |
| S07 | `semantic.k:80-81` | `setVar` updates the environment after obtaining a value. | Correct; map update preserves other bindings. |
| S08 | `semantic.k:83` | `If` evaluates its condition before branch selection. | Correct. |
| S09 | `semantic.k:84` | True selects the then statements. | Correct. |
| S10 | `semantic.k:85` | False selects the else statements. | Correct. |
| S11 | `semantic.k:87` | `While` evaluates its guard. | Correct. |
| S12 | `semantic.k:88` | True executes the body and then reinstalls the exact loop. | Correct recurring loop-head configuration. |
| S13 | `semantic.k:89` | False consumes the loop. | Correct. |
| S14 | `semantic.k:91` | `Return` evaluates its expression before `doReturn`. | Correct. |
| S15 | `semantic.k:92-93` | A value at `doReturn` discards the remaining top-level computation and stores the result when it was `noResult`. | Correct for the single-function, no-call-stack submitted program; broader Python call semantics are intentionally absent. |
| S16 | `semantic.k:95` | `Int(I) => I`. | Correct literal evaluation. |
| S17 | `semantic.k:96-97` | `Name(X)` reads the environment. | Correct lookup for a present binding. |
| S18 | `semantic.k:99` | Unary `-` evaluates its operand. | Correct. |
| S19 | `semantic.k:100` | Negation computes `0 -Int I`. | Correct over unbounded integers. |
| S20 | `semantic.k:102` | Binary `+` evaluates the left operand first. | Correct Python operand order for these pure expressions. |
| S21 | `semantic.k:103` | After the left integer, evaluate the right. | Correct. |
| S22 | `semantic.k:104` | Add the two integers. | Correct. |
| S23 | `semantic.k:106` | `and` evaluates its left operand first. | Correct. |
| S24 | `semantic.k:107` | True evaluates and returns the right operand. | Correct for the used Boolean right operand. |
| S25 | `semantic.k:108` | False short-circuits and returns false. | Correct. |
| S26 | `semantic.k:110` | `<` comparison evaluates its left expression first. | Correct. |
| S27 | `semantic.k:111` | Then evaluate the right expression while retaining the left integer. | Correct. |
| S28 | `semantic.k:112` | Compute `I <Int J`. | Correct. |
| S29 | `semantic.k:114` | Subscript evaluates the container first. | Correct. |
| S30 | `semantic.k:115` | Then evaluate the index while retaining the list. | Correct. |
| S31 | `semantic.k:116` | Apply `intAt` to the evaluated list and integer index. | Correct on in-bounds integer-list inputs; exception behavior is not modeled. |

S01 and S02 are disjoint (`N=0` versus `N>0`) and descend on their recursive
domain, but they do not cover empty lists, negative indices, out-of-bounds
indices, or lists whose traversed item is not an `Int`.  Therefore the
unqualified `[total]` attribute on item 9 is false over its declared
`List × Int` domain.  Fresh LLVM compilation emits a non-exhaustive-match
warning (`06-kompile-semantic-llvm.log`), and concrete
`intAt(ListItem(true),0)` gets stuck (`19-intat-totality-formal-scope-witness.log`).
Removing only `[total]` makes the proof fail on `#Ceil(intAt(A,I))`
(`17-kprove-no-intat-total-expected-failure.log`), showing that the proof uses
the assertion.

All natural-contract inputs have integer elements and every actual access
satisfies `0 <= i < k <= size(A)`, so no false intended-domain output witness
for S01/S02 or local `intAt` totality was found.  The Boolean-list witness is in
the formal K claim's broad `A:List` domain but outside the intended integer-array
domain.  Accordingly, this is recorded as a formal-scope/assumption defect, not
as the intended-domain false-result witness used for the final verdict.

## Verification rules and claims

| ID | Source | Rule and role | Review |
|---|---|---|---|
| V01 | `verification.k:10-19` | Macro-expands `solutionLoop` to the loop AST. | Pure syntactic alias. Fresh expanded-AST comparison is byte-identical (`13-real-program-pinning.log`). |
| V02 | `verification.k:22-28` | Macro-expands `solutionProgram` to the full AST. | Pure syntactic alias, likewise pinned to `solution.mpy`. |
| V03 | `verification.k:34-35` | `smallContribution(I) => I` for `-100 < I < 100`. | True equation and matches the candidate branch. |
| V04 | `verification.k:36-37` | `smallContribution(I) => 0` outside that open interval. | True equation and matches the candidate branch. |
| V05 | `verification.k:40-41` | `sumRange(A,I,K) => 0` for `I >= K`. | True base equation for the chosen summary. |
| V06 | `verification.k:42-44` | For `I < K`, add `smallContribution(intAt(A,I))` and recurse at `I+1`. | Descends by `K-I` on the claim domain and summarizes the candidate loop. It inherits `intAt`'s over-broad totality assumption. |
| C01 | `spec.k:8-21` | Loop circularity from the exact loop head and return continuation to `result(T + sumRange(A,I,K))`. | Matches real control flow; precondition is satisfiable; return is constrained. |
| C02 | `spec.k:24-32` | Entry claim from the exact solution macro to `result(sumRange(A,0,K))`. | Matches the submitted AST and is non-vacuous, but its summary is not the trusted canonical contract for negative two-digit integers. |

V03 and V04 have disjoint, exhaustive guards over mathematical integers.
V05 and V06 are also disjoint and exhaustive over `I,K`; V06 terminates as a
mathematical recursion when used with `I < K`.  None of V03-V06 replaces
program execution.  They are RHS mathematical summaries used after the
ordinary semantic rules execute the actual loop.

The decisive intent witness is `I=-10`: V03 yields `-10`, and the candidate
program does too, but trusted `canonical.py` excludes it because
`len(str(-10)) == 3`, yielding `0`.  This is an adequacy failure of the claimed
"mathematical contract," not a false algebraic equation inside V03.

## Construct-to-rule coverage for `solution.mpy`

| Submitted construct | Declaration | Operational coverage |
|---|---|---|
| `Module`, `FuncDef`, `Params` | syntax items 1, 2, and statement `FuncDef` | S03 |
| juxtaposed statement lists | syntax item 3 | S04-S05 |
| `Assign(Name(...),...)` | statement `Assign`, expressions `Name` | S06-S07 and S17 |
| `Int` | expression `Int` | S16 |
| `While` | statement `While` | S11-S13 |
| `Compare(...,CmpOp("<",...))` | `Compare`, `CmpOp` | S26-S28 |
| `Subscript` | expression `Subscript` | S29-S31 plus S01-S02 |
| `If` | statement `If` | S08-S10 |
| `BoolOp("and",...)` | expression `BoolOp` | S23-S25 |
| `UnaryOp("-",...)` | expression `UnaryOp` | S18-S19 |
| `BinOp("+",...)` | expression `BinOp` | S20-S22 |
| `Return` | statement `Return` | S14-S15 |

Every AST construct in the submitted program has a declaration and an
exercised rule path.  Missing semantics for calls, strings, slicing,
generators, `sum`, `str`, and exceptions is acceptable for execution of this
candidate program, but it means the generated semantics does not directly
execute the trusted canonical implementation.

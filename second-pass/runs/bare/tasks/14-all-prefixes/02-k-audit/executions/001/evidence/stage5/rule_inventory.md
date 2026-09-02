# Local K declaration and rule inventory

This inventory was reconstructed from the source copies in
`/tmp/audit-work/src/candidate`. Built-in modules (`BOOL`, `INT`, `STRING`,
`K-EQUAL`, and syntax imports) are treated as K's primitive trust boundary, not
as candidate-local declarations.

## Syntax and configuration

`semantic.k`, module `MPY-SYNTAX`:

1. `Program`: `Module(Stmts)` and `Run(Program, Expr)`.
2. `Stmts`: separator-free `List{Stmt,""}`.
3. `Exprs`: comma-separated nonempty `NeList{Expr,","}`.
4. `Strings`: comma-separated `List{String,","}`.
5. `Stmt`: `ImportFrom`, `FuncDef`, `Assign`, `While`, expression statement
   `Expr`, and `Return`.
6. `Params`: `Params(Strings)`.
7. `Expr`: `Name`, `Int`, `Str`, empty/nonempty `ListExpr`, `BinOp`,
   `Compare`, `Call`, `Attribute`, and `Subscript`.
8. `CmpOps`: comma-separated `List{CmpOp,","}`.
9. `CmpOp`: operator string plus comparator expression.
10. `Index`: expression or `Slice(Bound,Bound,Bound)`.
11. `Bound`: expression or `NoBound`.

`semantic.k`, module `MPY`:

12. `Value`: integer, string, Boolean, list, and none values.
13. `Values`: `vnil` and `vcons(Value,Values)`.
14. `Env`: `emptyEnv` and linked `bind`.
15. `Function`: one parameter string and statement body.
16. `FEnv`: `emptyFEnv` and linked `fbind`.
17. `KItem`: `exec`, `loop`, `restoreEnv`, `returning`, and `invoke`.
18. Configuration: `<mpy>` contains `<k>`, `<env>`, and `<functions>`; initial
    environment/function environment are empty.

Helper files:

19. `solution-program.k`: `solutionProgram : Program [function]`.
20. `verification.k`: opaque accumulator constructor `pacc(String,Int) :
    Values` and `allPrefixes(String) : Values [function]`.

There are no candidate-local `[total]` or `[functional]` declarations.
Candidate-local `[function]` symbols are `lookup`, `update`, `flookup`, `snoc`,
`eval`, `addVal`, `lenVal`, `lessEqVal`, `prefixVal`, `appendVal`, `truth`,
`solutionProgram`, and `allPrefixes`. The only new opaque/result-bearing
constructor is `pacc`. The only `[simplification]` rule is V2 below. The only
explicit priority is L1 `[priority(30)]`.

## `semantic.k` rules (39)

| ID | Source line | Rule/role | Static assessment |
|---|---:|---|---|
| R1 | 65 | `lookup` matching head | Correct linked-environment lookup. |
| R2 | 66 | guarded `lookup` recursion | Correct; guard is disjoint from R1. Partial at `emptyEnv`, but every target lookup is bound. |
| R3 | 70 | `update` empty environment | Correct insertion. |
| R4 | 71 | `update` matching head | Correct replacement. |
| R5 | 72 | guarded `update` recursion | Correct and structurally descending; guard is disjoint from R4. |
| R6 | 76 | `flookup` matching head | Correct function lookup. |
| R7 | 77 | guarded `flookup` recursion | Correct and descending; partial at `emptyFEnv`, but the target function is registered first. |
| R8 | 81 | `snoc(vnil,V)` | Correct list append base. |
| R9 | 82 | `snoc(vcons(...),V)` | Correct, structurally descending append. |
| R10 | 85 | evaluate integer literal | Correct for Python arbitrary-precision integers. |
| R11 | 86 | evaluate string literal | Syntactically faithful, but the imported K `String` model is byte-oriented; this becomes material through R19/R21. |
| R12 | 87 | evaluate name through `lookup` | Correct on the target's bound locals. |
| R13 | 88 | evaluate empty list | Correct. |
| R14 | 89 | evaluate binary `+` through `addVal` | Correct for the target's integer increment; operands are side-effect-free. |
| R15 | 90 | evaluate `len(E)` through `lenVal` | Correct dispatch for the exact target syntax, but inherits R19's Unicode defect. |
| R16 | 91 | evaluate one `<=` comparison | Correct for target integers. |
| R17 | 93 | evaluate `E[:HI]` through `prefixVal` | Correct dispatch for exact target syntax, but inherits R21's Unicode defect. |
| R18 | 101 | integer addition | Correct and matches Python integers. |
| R19 | 102 | string length via K `lengthString` | **Unsound as Python semantics on intended `str` inputs.** Witness `"🙂x"`: this rule yields 5, while Python `len("🙂x")` is 2. |
| R20 | 103 | integer `<=` | Correct. |
| R21 | 104 | prefix via K `substrString(S,0,I)` | **Unsound as Python semantics on intended `str` inputs.** Witness `S="🙂x", I=1`: this rule yields byte string `"\xf0"`, while Python `S[:1]` is `"🙂"`. |
| R22 | 105 | list append through `snoc` | Correct for target list values and proof accumulator cases covered by V2. |
| R23 | 108 | truth of Boolean value | Correct for target Boolean conditions. |
| R24 | 117 | `Run(Module(SS),E)` schedules module then call | Correct sequencing for the submitted target. |
| R25 | 118 | module schedules statements | Correct. |
| R26 | 120 | empty statement sequence | Correct. |
| R27 | 121 | statement-head scheduling | Correct left-to-right sequencing. |
| R28 | 123 | ignore `ImportFrom` | Sound for the submitted `typing.List` import's result behavior: annotations were transliterated away and `List` is never read. It is intentionally incomplete for imports in general. |
| R29 | 124 | register one-parameter function | Correct for the submitted module; separate `FEnv` is adequate because the body uses no program global. |
| R30 | 126 | name assignment | Correct: RHS is evaluated in the old environment, then the name is updated. |
| R31 | 128 | specialized `result.append(E)` | Correct on the exact submitted path: receiver is a bound list, argument is pure, and no aliases exist. Over-broad as a language rule for arbitrary names/types, but no false conclusion is enabled on the intended target inputs. |
| R32 | 130 | lower `While` to `loop` | Correct. |
| R33 | 131 | true loop branch | Correct; repeats after body. |
| R34 | 134 | false loop branch | Correct; guard complements R33. |
| R35 | 138 | one-argument named call | Correct for the registered target function and pure string argument. |
| R36 | 141 | invoke with fresh local environment and restore frame | Correct for this one-parameter body, which needs no globals/closures. |
| R37 | 144 | evaluate `Return` and mark `returning` | Correct. |
| R38 | 146 | discard remaining `exec` statements after return | Correct for the target's return-at-end context. The semantics is incomplete for return nested in a loop, an unused context. |
| R39 | 147 | restore caller environment and expose return value | Correct for the exact call frame. |

## Generated helper/proof rules

| ID | File:line | Declaration/rule | Classification and assessment |
|---|---|---|---|
| P1 | `solution-program.k:3-16` | `solutionProgram` declaration and expansion rule | `[function]` definition. Independent byte comparison shows the expansion is the exact trusted-regenerated `solution.mpy` term. |
| V1 | `verification.k:10-11` | `pacc(S,0) => vnil` | Definitional summary base. Truthful for “first zero nonempty prefixes.” |
| V2 | `verification.k:12-15` | `snoc(pacc(S,N), prefix(S,I)) => pacc(S,N+1)` when `I=N+1`, `[simplification]` | Definitional summary induction step. Truthful on the loop claim's guarded domain `0 <= N < length(S)`. Its written guard is broader (no nonnegativity/length bounds), so uses outside that domain lack an intended-list interpretation; no false conclusion witness on the intended entry domain was found. It overlaps the concrete `snoc` path at `N=0`, but the two results agree under the stated accumulator interpretation. |
| V3 | `verification.k:17-18` | `allPrefixes(S) => pacc(S,lengthString(S))` | `[function]` definition of the formal summary. It inherits the byte-string defect from `lengthString`. |
| L1 | `verified-lemma.k:7-26` | exact initial-loop configuration rewrites to `listVal(allPrefixes(S))`, restores `OLD`; `[priority(30)]` | Operational bridge. It is the `N=0, I=1` instance of the independently reconstructed `LOOP-SPEC` claim: `pacc(S,0)` reduces to `vnil`, and the remaining guards discharge. It matches the exact loop body, `Return`/restore continuation, bindings, and all observable cells. It is result-bearing but connected by the successful loop reachability proof. Its formal result still inherits R19/R21. |

## Claims

| ID | File | Plain formal content |
|---|---|---|
| C1 | `loop-spec.k` | For any K string `S`, `0 <= N <= lengthString(S)`, and `I=N+1`, the exact submitted loop with accumulator `pacc(S,N)`, followed by the exact return/restore continuation, reaches `listVal(allPrefixes(S))` and restores `OLD`. |
| C2 | `spec.k` | From empty state, `Run(solutionProgram, all_prefixes(Str(S)))` reaches `listVal(allPrefixes(S))`, restores the empty environment, and leaves an unconstrained function environment, for every K string `S`. |

## Used-syntax coverage

The submitted `solution.mpy` uses `Module`, `ImportFrom`, `FuncDef`, `Params`,
`Assign`, `While`, expression statement `Expr`, `Return`, `Name`, `Int`, `Str`
(at call time), empty `ListExpr`, `BinOp("+")`, `Compare` with one
`CmpOp("<=")`, one-argument `Call`, `Attribute("append")`, `Subscript`, `Slice`,
and `NoBound`. These map respectively to R24/R25, R28, R29, R30, R32-R34, R31,
R37-R39, R12, R10, R11, R13, R14/R18, R16/R20/R23, R15/R19 and R35/R36,
R31/R22, R17/R21, and the syntax declarations above. Statement sequencing is
R26-R27. No used construct is silently unmodeled.

The model's material defect is not missing coverage: R19 and R21 deliberately
give used `len` and slice constructs byte semantics that disagree with Python
on valid Unicode strings.

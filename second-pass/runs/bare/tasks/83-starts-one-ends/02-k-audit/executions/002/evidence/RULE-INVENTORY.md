# Reviewer rule and declaration inventory

Sources: scratch copies of `semantic.k`, `verification.k`, and `spec.k`.
Lexical counts are recorded in `11-lexical-inventory.log`: 18 semantic rules,
6 proof-local definitional rules, and 2 entry claims.

## Syntax and configuration declarations

| Source | Declaration | Role and audit result |
|---|---|---|
| `semantic.k:7` | `Pgm ::= Module(Stmts)` `[symbol(Module)]` | Translator-aligned module constructor; used. |
| `semantic.k:9` | `Stmts ::= List{Stmt, ""}` | Empty/concatenated statement sequence; used. |
| `semantic.k:10-13` | `Stmt ::= FuncDef \| Return \| If \| Expr` with constructor symbols | Exactly the statement nodes in `solution.mpy`; all used. |
| `semantic.k:15` | `Params ::= Params(String)` `[symbol(Params)]` | Single-parameter function; used. |
| `semantic.k:17-21` | `Expr ::= Int \| Str \| Name \| BinOp \| Compare` with constructor symbols | Exactly the expression nodes in `solution.mpy`; all used. |
| `semantic.k:23` | `CmpOp ::= CmpOp(String, Expr)` `[symbol(CmpOp)]` | Comparison constructor; `==` used. |
| `semantic.k:32-39` | `FunctionValue`, `Control`, `Result`, and `KItem` (`exec`, `entry`, `endCall`) | Internal one-function/one-call machine vocabulary. |
| `semantic.k:41-48` | `<mpy>` configuration with `<k>`, `<function>`, `<env>`, `<control>`, `<result>` | Every declared cell is read or written. Initial state is explicit. |
| `semantic.k:89` | `evalInt(Expr, Map) : Int` `[function]` | Partial pure evaluator, defined for all integer forms reachable here. No `[total]`. |
| `semantic.k:98` | `evalBool(Expr, Map) : Bool` `[function]` | Partial pure evaluator, defined for the reachable equality comparison. No `[total]`. |
| `verification.k:10-14` | `decimalMiddles`, `startsWithOne`, `endsWithOne`, `startsAndEndsWithOne`, `qualifyingCount` as `[function]` Int symbols | Guarded, nonrecursive mathematical definitions used only to state the postcondition. |

There are no local `total`, `functional`, `simplification`, `opaque`,
`priority`, or `owise` attributes. The constructor declarations use `symbol`;
the evaluator and count declarations use `function`.

## Semantic rules

| ID | Source | Rule | Classification and result |
|---|---|---|---|
| S1 | `semantic.k:52` | `Module(SS) => exec(SS)` | Operational semantics. Starts top-level statement execution; correct here. |
| S2 | `semantic.k:53` | `exec(.Stmts) => .K` | Operational semantics. Empty normal sequence terminates; correct. |
| S3 | `semantic.k:54-55` | `exec(S SS) => S ~> exec(SS)` when control is normal | Operational sequencing. Preserves left-to-right order; correct. |
| S4 | `semantic.k:56-57` | Drop pending `exec(_SS)` when control is returned | Return propagation. Correctly skips remaining function statements. |
| S5 | `semantic.k:59-60` | Register `FuncDef` in the function cell | One-function binding semantics. Correct for the submitted one-definition module. |
| S6 | `semantic.k:62-66` | `entry(F,N)` installs argument binding and executes the matched body | Call setup. The repeated `F` pins the selected binding. Correct for the single call; no general call stack is modeled. |
| S7 | `semantic.k:68-69` | `endCall` resets returned to normal | Call teardown. Correct at the only outer continuation. |
| S8 | `semantic.k:73` | `Expr(_E) => .K` | Operational shortcut. Correct for the reachable `Expr(Str(docstring))`, whose evaluation has no observable effect. It is over-broad globally: `15-expr-rule-overbreadth.log` witnesses Python raising `NameError` for `Expr(Name("missing"))` at positive input 1 while K silently continues and returns 1. That altered program is not the submitted program and the bad instance is unreachable in either target claim, so this is a scope/trust limitation rather than a false target conclusion. |
| S9 | `semantic.k:75-77` | True `If` guard executes THEN | Guarded control rule. Its guard is the program condition; correct. |
| S10 | `semantic.k:78-80` | False `If` guard executes ELSE | Complementary guard; disjoint from S9 and complete for the reachable Boolean. |
| S11 | `semantic.k:82-85` | `Return(E)` stores `evalInt(E,ENV)` and sets returned | Return value/control rule. Correct for the integer expressions and fresh result cell reached here. |
| S12 | `semantic.k:90` | `evalInt(Int(I),ENV) => I` | True literal equation. |
| S13 | `semantic.k:91-92` | Unique map lookup for `Name(X)` | True binding equation; uniqueness guard excludes a duplicate key in the remainder. |
| S14 | `semantic.k:93` | Integer `+` | True pure equation; declared but unused by `solution.mpy`. |
| S15 | `semantic.k:94` | Integer `-` | True pure equation; used for `n - 2`. |
| S16 | `semantic.k:95` | Integer `*` | True pure equation; used. |
| S17 | `semantic.k:96` | Integer `**` via `^Int` | Correct on the reachable nonnegative exponent: `n=1` takes the other branch and `n>1` implies `n-2 >= 0`. |
| S18 | `semantic.k:99-100` | Equality comparison via `==Int` | True pure equation; used. |

The only overlaps are deliberate sequence/control cases: S2 versus S4 at an
empty sequence and S3 versus S4 at a nonempty sequence. Their control guards
are disjoint (`normal` versus `returned`). S9 and S10 are Boolean complements.
Expression equations are constructor/operator-disjoint. Pure operands have no
state or effects, so K's equational reduction order cannot alter an observable
result.

## Proof-local rules

| ID | Source | Rule | Classification and result |
|---|---|---|---|
| V1 | `verification.k:16` | `decimalMiddles(K) = 10^K` for `K >= 0` | Guarded definitional summary. True and terminating. |
| V2 | `verification.k:17-18` | `startsWithOne(N) = 10 * decimalMiddles(N-2)` for `N > 1` | Guarded counting definition. For a leading 1, one following digit plus `N-2` middle digits are free. |
| V3 | `verification.k:19-20` | `endsWithOne(N) = 9 * decimalMiddles(N-2)` for `N > 1` | Guarded counting definition. The leading digit has 9 choices. |
| V4 | `verification.k:21-22` | intersection count `= decimalMiddles(N-2)` for `N > 1` | Guarded counting definition. Both endpoints fixed. |
| V5 | `verification.k:24` | `qualifyingCount(1) = 1` | Disjoint base definition; true. |
| V6 | `verification.k:25-27` | inclusion-exclusion for `qualifyingCount(N)` when `N > 1` | Guarded mathematical definition; expands to `18 * 10^(N-2)`. |

V5 and V6 are disjoint. V1-V4/V6 cover every proof use because the symbolic
claim has `N > 1`; V5 covers the fixed `N=1` claim. There is no recursion,
overlap with conflicting right-hand sides, totality assertion, oracle, opaque
value, or operational rewrite in `verification.k`. These rules do not preempt
program execution.

## Claims and construct coverage

`positive-n-one` has the realizable fixed input `n=1` and postcondition
`result(qualifyingCount(1)) = result(1)`. `positive-n-gt-one` has the realizable
symbolic domain `N>1` (for example `N=2`) and postcondition
`result(qualifyingCount(N)) = result(18 * 10^(N-2))`.

The submitted constructor term uses:

- `Module`, one `FuncDef`, one `Params`, and statement-list sequencing;
- the docstring `Expr(Str(...))`;
- `If(Compare(Name("n"), CmpOp("==", Int(1))), ...)`;
- both `Return` branches;
- `BinOp("*")`, `BinOp("**")`, and `BinOp("-")`.

S1-S18 collectively cover every one of these constructs. Fresh runs at `n=1`
and `n=2` exercise both branch rules; `n=2,3,5,10` exercise subtraction,
nonnegative exponentiation, and multiplication.

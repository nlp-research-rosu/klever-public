# Exhaustive local rule and declaration inventory

The audited source is the immutable `/candidate` tree. Line references below
refer to `/candidate/semantic.k` and `/candidate/verification.k`. Imported K
domain modules are accounted for as trusted primitives, not as local rules.

## Local syntax, attributes, and configuration

`semantic.k` declares:

- `Module ::= Module(Stmts)` (line 8).
- `Stmts ::= List{Stmt, ""}` (line 10).
- Five `Stmt` constructors: `FuncDef`, `Assign`, `If`, `While`, and `Return`
  (lines 11-15).
- `Params(String)` (line 17).
- Six `Expr` constructors: `Int`, `Str`, `Name`, `BinOp`, `Compare`, and
  `Call` (lines 19-24).
- `CmpOp(String, Expr)` (line 25).
- Runtime values `IVal`, `SVal`, and `BVal` (line 36), function closures
  `function(String, Stmts)` (line 37), and call frames `frame(Map, K)`
  (line 38).
- Fifteen local `KItem` constructors (lines 40-54): `init`, `run`, `exec`,
  `eval`, `store`, `binLeft`, `binRight`, `cmpLeft`, `cmpRight`, `ifGuard`,
  `whileGuard`, `call`, `toStr`, `returning`, and `functionEnd`.
- The configuration (lines 56-62) has `<k>`, `<env>`, `<functions>`, and
  `<stack>` cells. Every cell is used. There are no heap, I/O, exception, or
  allocation cells because the submitted program exercises none.

`verification.k` declares eight local `[function]` symbols (lines 6-13):
`sequenceFrom`, `sequence`, `indexAfter`, `loopCondition`, `loopBody`,
`targetBody`, `targetFunction`, and `targetProgram`.

There are no local `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
`[owise]`, `[trusted]`, priority, macro, alias, or opaque declarations. There
are no local priority rules or simplification rules. The only local attributes
are the eight `[function]` attributes above; the attributes affect evaluation
but do not serve as their truth justification.

## Ordinary rules in `semantic.k`

Every one of the 31 local rules is inventoried below.

| ID | Lines | Rule | Static disposition |
|---|---:|---|---|
| S01 | 64-66 | `init(Module(SS),N)` runs the module, then calls `string_sequence(N)` | Sound for the configured one-entry runner. It executes the submitted module before the call and narrows the runner input exactly to the source `int` argument. |
| S02 | 68 | `run(.Stmts) => .K` | Sound empty-sequence base. |
| S03 | 69 | `run(S SS) => exec(S) ~> run(SS)` | Sound left-to-right statement sequencing. |
| S04 | 71-72 | execute `FuncDef` by installing `function(P,BODY)` | Sound for the used one-parameter, no-default, no-closure body. It preserves other functions via map update. |
| S05 | 74 | begin assignment by evaluating the RHS, then storing | Sound evaluation order; the target is the used `Name(X)` form. |
| S06 | 75-76 | store into an existing environment key | Sound update; applicability requires that the map pattern contain `X`. |
| S07 | 77-79 | store a new key when absent | Sound insertion. Its `notBool (X in_keys(ENV))` guard is disjoint from S06. |
| S08 | 81-82 | evaluate a `while` guard before dispatch | Sound guard-first control. |
| S09 | 83-84 | true `while` guard executes the body and repeats | Sound loop control and statement ordering. |
| S10 | 85 | false `while` guard terminates the loop | Sound false branch. |
| S11 | 87-88 | evaluate an `if` guard before dispatch | Sound guard-first control. |
| S12 | 89 | true `if` guard runs the then branch | Sound true branch. |
| S13 | 90 | false `if` guard runs the else branch | Sound false branch; S12/S13 are constructor-disjoint. |
| S14 | 92 | evaluate a return expression, then enter `returning()` | Sound expression-before-control-transfer behavior. |
| S15 | 93-95 | return restores caller environment/continuation and pops one frame | Sound on every reachable target-program return: `_REST` is the remainder of the current function and is correctly discarded, while saved `KREST` is restored. The map of functions is framed and preserved. |
| S16 | 97 | integer literal to `IVal` | Sound constructor injection. |
| S17 | 98 | string literal to `SVal` | Sound constructor injection. |
| S18 | 99-100 | name lookup in `<env>` | Sound for reachable bound local variables. |
| S19 | 102 | begin `BinOp` by evaluating its left operand | Sound left-to-right order. |
| S20 | 103 | retain the left value while evaluating the right operand | Sound left-to-right order. |
| S21 | 104 | integer `+` | Sound use of K mathematical integer addition; value constructors make it disjoint from S22. |
| S22 | 105 | string `+` | Sound use of K string concatenation. |
| S23 | 107-108 | begin comparison by evaluating the left operand | Sound left-to-right order. |
| S24 | 109 | retain left value and evaluate right operand for `<=` | Sound and operator-specific. |
| S25 | 110 | apply integer `<=` | Sound mathematical comparison. |
| S26 | 111 | retain left value and evaluate right operand for `<` | Sound and operator-specific. |
| S27 | 112 | apply integer `<` | Sound mathematical comparison. |
| S28 | 114 | builtin `str` call evaluates its argument before conversion | Sound for the unshadowed builtin used by the submitted body. |
| S29 | 115 | `str(IVal(I))` uses `Int2String(I)` | Sound for the reachable positive loop indices; K concrete runs and Python differential evidence exercise the bridge. |
| S30 | 117-119 | dispatch a non-`str` named call after confirming a function binding | Sound for `string_sequence`; the literal/guard makes it disjoint from S28. |
| S31 | 120-124 | enter a one-argument function, save caller env/continuation, run body | Sound for the used function: the argument was already evaluated, its sole parameter is bound, the caller frame is pushed at the list head, and function bindings are preserved. |

The declared `functionEnd()` continuation has no reduction rule. That means the
generated language intentionally does not model Python's implicit `None` return.
This is not reached by the submitted program: the negative branch executes a
return, and every nonnegative execution reaches the final return. Missing
semantics for this unused behavior is outside the accepted minimal generated
semantics scope.

## Function equations in `verification.k`

Every one of the 11 local equations is inventoried below.

| ID | Lines | Equation | Class and static disposition |
|---|---:|---|---|
| V01 | 15-17 | recursive `sequenceFrom` case for `I <= N` | Definitional summary, not an execution rewrite. Truthfully appends exactly the current index and increments it. |
| V02 | 18-19 | `sequenceFrom` base for `I > N` | Definitional base. V01/V02 guards are exhaustive and disjoint over `Int`; recursion strictly approaches the base for every ground case. |
| V03 | 21 | `sequence(N) => ""` for `N < 0` | Truthful negative-input specification and canonical behavior. |
| V04 | 22 | `sequence(N) => sequenceFrom(1,N,"0")` for `N >= 0` | Truthful nonnegative specification. V03/V04 are exhaustive and disjoint. |
| V05 | 24-25 | recursive `indexAfter` for `I <= N` | Definitional loop-index summary; increments exactly once per modeled iteration. |
| V06 | 26-27 | `indexAfter` base for `I > N` | Truthful base. V05/V06 are exhaustive/disjoint and terminate for every ground case. |
| V07 | 29-30 | `loopCondition()` expands to the submitted comparison | Exact AST abbreviation, not a result oracle. |
| V08 | 32-39 | `loopBody()` expands to the submitted two statements | Exact AST abbreviation preserving evaluation and statement order. |
| V09 | 41-49 | `targetBody()` expands to the submitted function body | Exact AST abbreviation. The trusted translator/KORE/pinning evidence connects it to `solution.mpy`. |
| V10 | 51 | `targetFunction()` expands to the submitted binding | Exact binding abbreviation. |
| V11 | 52-53 | `targetProgram()` expands to the submitted module | Exact module abbreviation. |

There are no guard overlaps with disagreeing right-hand sides, uncovered ground
domains for the mathematical helpers, priority interactions, unconstrained
fresh values, or proof-local operational rules that bypass fixed execution.
The loop reachability claim in `spec.k` is the machine-checked universal
connection between fixed loop execution and `sequenceFrom`/`indexAfter`.

## Used-constructor coverage

| Submitted constructor | Declaration | Execution rules |
|---|---|---|
| `Module`, statement list | lines 8, 10 | S01-S03 |
| `FuncDef`, `Params` | lines 11, 17 | S04, S30-S31 |
| `If` | line 13 | S11-S13 |
| `Assign` | line 12 | S05-S07 |
| `While` | line 14 | S08-S10 |
| `Return` | line 15 | S14-S15 |
| `Int`, `Str`, `Name` | lines 19-21 | S16-S18 |
| `BinOp("+",...)` | line 22 | S19-S22 |
| `Compare`, `CmpOp("<",...)`, `CmpOp("<=",...)` | lines 23, 25 | S23-S27 |
| `Call(Name("str"),...)`, entry call | line 24 | S28-S31 |

Every constructor in the trusted-regenerated `solution.mpy` is declared and
has an applicable rule sequence on every intended input. No used construct is
fabricated or silently left unmodeled.

# Exhaustive local K declaration and rule inventory

The inventory covers every candidate-authored K source file. Imported builtin
domain declarations are outside the local inventory and are listed in the
trust ledger in `REVIEW.md`.

## `semantic.k`: `MPY-SYNTAX`

| ID | Lines | Declaration | Used by submitted term | Assessment |
|---|---:|---|---|---|
| S1 | 9 | sort `Pgm` | yes | Abstract program sort. |
| S2 | 10 | sort `Stmt` | yes | Abstract statement sort. |
| S3 | 11 | sort `Expr` | yes | Abstract expression sort. |
| S4 | 12 | sort `Params` | yes | Abstract parameter-list sort. |
| S5 | 13 | sort `CmpOp` | yes | Abstract comparison-operation sort. |
| S6 | 14 | `Stmts ::= List{Stmt, ""}` | yes | Statement list; submitted module/body each contain one statement. |
| S7 | 15 | `Exprs ::= List{Expr, ","}` | yes | Operand list; contains all 22 comparisons. |
| S8 | 16 | `Strings ::= List{String, ","}` | yes | Parameter list; contains `"a"`. |
| S9 | 17 | `CmpOps ::= List{CmpOp, ","}` | yes | Comparison chain; every submitted comparison has one operation. |
| S10 | 19 | `Pgm ::= Module(Stmts)` | yes | Directly matches translator output. |
| S11 | 20 | `Stmt ::= FuncDef(String, Params, Stmts)` | yes | Directly matches translator output. |
| S12 | 21 | `Stmt ::= Return(Expr)` | yes | Directly matches translator output. |
| S13 | 22 | `Params ::= Params(Strings)` | yes | Directly matches translator output. |
| S14 | 23 | `Expr ::= Name(String)` | yes | All comparisons read `"a"`. |
| S15 | 24 | `Expr ::= Int(Int)` | yes | All comparison constants. |
| S16 | 25 | `Expr ::= Bool(Bool)` | no | Extra but inert syntax; rule R1 gives its sound Boolean-literal behavior. |
| S17 | 26 | `Expr ::= BoolOp(String, Exprs)` | yes | Submitted `"or"` expression. |
| S18 | 27 | `Expr ::= Compare(Expr, CmpOps)` | yes | All equality tests. |
| S19 | 28 | `CmpOp ::= CmpOp(String, Expr)` | yes | Submitted `"=="` operations. |

There are no syntax priorities or associativity declarations; constructor
parentheses and list separators make the submitted term unambiguous.

## `semantic.k`: `MPY`

| ID | Lines | Declaration/rule | Complete match domain and effect | Assessment |
|---|---:|---|---|---|
| S20 | 37 | `Result ::= noResult` | Initial result marker. | Sound and inert. |
| S21 | 37 | `Result ::= Expr` | Returned translated values. | Sound for the modeled subset. |
| S22 | 38 | `KItem ::= execute(Stmts)` | Internal body-execution control item. | Sound internal control. |
| F1 | 42 | `evalBool(Expr, Map) [function]` | Partial Boolean evaluator. No `[total]`/`[functional]` attribute. | Equations R1-R3 cover every form reached by the submitted program. Unsupported forms remain stuck. |
| F2 | 43 | `evalOr(Exprs, Map) [function]` | Partial Boolean-list evaluator. No `[total]`/`[functional]` attribute. | R4-R5 cover every list shape. Operand coverage is delegated to F1. |
| R1 | 45 | `evalBool(Bool(B), _) => B` | Any Boolean literal and any map; returns its Boolean. | True definitional equation. The syntax is unused by the submitted term. |
| R2 | 46-49 | equality of a looked-up integer name and integer literal | Exact singleton map `X |-> Int(A)` and exact one-op `==` chain; returns builtin `A ==Int I`. | Correct Python integer equality for the submitted state. No side effects are skipped. |
| R3 | 50 | `evalBool(BoolOp("or", ES), ENV) => evalOr(ES, ENV)` | Any operand list/map for operator `"or"`; delegates. | Correct on the Boolean-valued operand subset. Unmodeled operands become visibly stuck. |
| R4 | 52 | `evalOr(.Exprs, _) => false` | Empty Boolean operand list. | Correct fold identity; also terminates all-false submitted executions. |
| R5 | 53-54 | head/tail recursion via `orElseBool` | Any nonempty list; evaluates head and short-circuits tail. | Correct order/control for submitted pure comparisons; recursive descent strictly shortens the list. |
| C1 | 56-60 | configuration `<k>`, `<arg>`, `<env>`, `<result>` | Program, integer invocation argument, local map, and result. | Exactly the state required by this unary pure program. |
| O1 | 64-66 | sole-function module launch | Requires exact `<k>` module with exactly one unary function, integer `<arg>`, and empty `<env>`; replaces `<k>` with `execute(BODY)` and binds the formal. Other cells are preserved. | Sound benchmark entry-point harness for the submitted one-function module. It has no continuation wildcard and does not consult task correctness. |
| O2 | 68-70 | execute one `Return(E)` | Requires exact `<k>` body, reads local map, empties it, and sets result to `Bool(evalBool(E, ENV))`; argument is preserved. | Sound big-step return for the submitted Boolean expression; exact control context prevents continuation loss. |

R1-R5 are function equations. O1-O2 are the only ordinary operational rules.
There are no local priority rules, opaque symbols, `[total]` declarations,
`[functional]` declarations, or semantic simplification rules.

## `solution-program.k`

| ID | Lines | Declaration/rule | Classification | Assessment |
|---|---:|---|---|---|
| F3 | 9 | `solutionProgram : Pgm [function]` | Definitional syntax constant. | Its only rule is complete because the function is nullary. |
| R6 | 10-37 | `solutionProgram => Module(FuncDef(...))` | Definitional summary, not an operational bridge. | The RHS has 416 constructor tokens and is mechanically identical to regenerated `solution.mpy`; it expands to, rather than bypasses, the body. |

No simplification, priority, totality, functional, or opaque declarations occur.

## `verification.k`

| ID | Lines | Declaration/rule | Classification | Assessment |
|---|---:|---|---|---|
| F4 | 10 | `isThreePrimeProductBelow100(Int) : Bool [function]` | Definitional mathematical predicate. | Its single unconditional equation covers every K integer. |
| R7 | 11-34 | predicate equals 22 disjuncts `[simplification]` | Proof-local definitional summary and the only local simplification rule. | The symbol is fresh and fully fixed by this equation. Independent enumeration obtains exactly the same 22 nondecreasing prime-triple products below 100, with no duplicates. It does not rewrite program execution. |

There are no ordinary operational, priority, totality, functional, or opaque
declarations in this module.

## `spec.k` and `definition.k`

`spec.k:6-13` contains exactly one reachability claim. `definition.k` contains
only imports and no declaration, rule, simplification, priority, claim, opaque
symbol, or total/functional attribute.

# Exhaustive local rule and declaration inventory

Source basis: the scratch copies whose hashes are recorded in
`scratch_copy.log`. Imported K `INT`, `BOOL`, `MAP`, and collection machinery is
listed later as a trust boundary; this inventory covers every candidate-local
declaration and rule.

## Syntax and attributes

`semantic.k` declarations:

1. `Pgm ::= Module(Stmts)` with symbol `moduleAst`.
2. `Stmts ::= List{Stmt,""}`.
3. `Stmt ::= FuncDef(String,Params,Stmts)` with symbol `funcDefAst`.
4. `Stmt ::= Assign(Expr,Expr)` with symbol `assignAst`.
5. `Stmt ::= While(Expr,Stmts)` with symbol `whileAst`.
6. `Stmt ::= Return(Expr)` with symbol `returnAst`.
7. `Params ::= Params(Strings)` with symbol `paramsAst`.
8. `Strings ::= List{String,","}`.
9. `Expr ::= Name(String)` with symbol `nameAst`.
10. `Expr ::= Int(Int)` with symbol `intAst`.
11. `Expr ::= BinOp(String,Expr,Expr)` with symbol `binOpAst`.
12. `Expr ::= Compare(Expr,CmpOps)` with symbol `compareAst`.
13. `Expr ::= TupleExpr(Exprs)` with symbol `tupleExprAst`.
14. `Exprs ::= List{Expr,","}`.
15. `CmpOp ::= CmpOp(String,Expr)` with symbol `cmpOpAst`.
16. `CmpOps ::= List{CmpOp,","}`.
17. Twelve `KItem` continuation/control constructors: `invoke`, `finish`,
    `assignTo`, `binRhs`, `applyBin`, `compareRhs`, `applyCompare`,
    `tupleSecond`, `tupleThird`, `tupleStore`, `whileDecision`, and
    `returnValue`.
18. `KResult ::= Int | Bool`.
19. Configuration `<fibfib><k> Pgm ~> invoke(N) </k><env>
    .Map</env><result>0</result></fibfib>`.

The `symbol(name)` attributes name AST constructors; they do not declare opaque
or uninterpreted result functions.

`verification.k` declarations:

20. `fibfibMath(Int):Int [function,total]`.
21. `fibfibProgram:Pgm [macro]`.
22. `loopCondition:Expr [macro]`.
23. `loopBody:Stmts [macro]`.

There are no local `functional`, `simplification`, `concrete`, `opaque`,
priority, `owise`, or trusted-rule attributes. There are no local priority
groups and no proof-local operational bridge rules.

## Used-construct coverage

The trusted translator maps the submitted Python AST as follows:

| Python/MPY construct | Local declaration | Operational rules |
|---|---|---|
| module and one function definition | `Module`, `FuncDef`, `Params`, `Stmts` | O1-O3 |
| integer literals and names | `Int`, `Name` | O4-O5 |
| scalar assignments | `Assign(Name,Expr)` | O12-O13 |
| three-target tuple assignment | `Assign(TupleExpr,TupleExpr)` | O14-O17 |
| integer addition | `BinOp("+",...)` | O6-O8 |
| single `<` comparison | `Compare(...,CmpOp("<",...))` | O9-O11 |
| while loop | `While` | O18-O20 |
| terminal return | `Return` | O21-O23 |

Every constructor in `solution.mpy` is covered. Other translator constructs are
deliberately absent and would fail to parse or get stuck; none is silently
fabricated.

## Operational rules in `semantic.k`

1. **O1, lines 59-61 — entry invocation.** For the exact single-function module
   `fibfib(n)`, replaces the module-plus-invocation with its actual body and
   `finish`, while changing the initially empty environment to `n |-> N`.
   This is the entry-call model, not a result summary. It executes `BODY`.
   Sound for the submitted single-function program.
2. **O2, line 63 — statement-list head.** Executes the first `Stmt`, then the
   remaining `Stmts`. Sound sequencing.
3. **O3, line 64 — empty statement list.** Consumes `.Stmts`. Sound identity.
4. **O4, line 66 — integer literal.** `Int(I)` evaluates to mathematical integer
   `I`. Sound for Python integer literals.
5. **O5, lines 67-68 — name lookup.** Reads exactly the mapped integer for `X`.
   All reachable submitted-program bindings are integers and are initialized
   before use.
6. **O6, line 70 — binary-operation start.** Evaluates the left operand first
   and remembers the operator/right expression.
7. **O7, line 71 — binary-operation right operand.** After an integer left
   value, evaluates the right operand and remembers the left value.
8. **O8, line 72 — addition.** Applies K mathematical `+Int`. Together O6-O8
   implements Python left-to-right addition for the only used operator.
   Unsupported operators get stuck.
9. **O9, line 74 — comparison start.** Handles exactly a one-link comparison,
   evaluates the left expression first, and remembers the operator/right
   expression.
10. **O10, line 75 — comparison right operand.** Evaluates the right expression
    after the integer left value.
11. **O11, line 76 — less-than.** Applies K mathematical `<Int`. Together
    O9-O11 implements the only submitted comparison; longer chains and other
    operators are unsupported rather than guessed.
12. **O12, line 78 — scalar assignment evaluation.** Evaluates the RHS before
    storing.
13. **O13, lines 79-80 — scalar assignment store.** Updates/adds the named map
    binding after obtaining an integer. This matches the used name assignment.
14. **O14, lines 82-83 — tuple assignment start.** For exactly three name
    targets and three expressions, begins evaluating RHS expressions from left
    to right, before any store.
15. **O15, lines 84-85 — tuple second expression.** Retains the first value and
    evaluates the second expression.
16. **O16, lines 86-87 — tuple third expression.** Retains the first two values
    and evaluates the third expression.
17. **O17, lines 88-89 — tuple store.** Performs left-to-right target updates
    only after all three RHS values are known. This preserves Python parallel
    tuple assignment, including the submitted alias-sensitive rotation.
18. **O18, line 91 — while condition.** Evaluates the condition and retains both
    condition syntax and body for repetition.
19. **O19, lines 92-93 — true while branch.** Runs the body, then reconstructs
    the same while term. This supplies the real recurring control point used by
    the loop claim.
20. **O20, line 94 — false while branch.** Consumes the loop without executing
    the body.
21. **O21, line 96 — return expression.** Evaluates the expression and records
    return control.
22. **O22, lines 97-98 — terminal return with explicit empty `Stmts`.** In the
    exact submitted continuation, consumes return/empty-list/finish and writes
    the integer result.
23. **O23, lines 99-100 — terminal return after the empty list has already
    reduced.** Consumes return/finish and writes the integer result.

O22 and O23 overlap only as alternative reachable representations of the
terminal empty list; their left sides cannot match the same `<k>` term, and
their effects agree. No return rule accepts an arbitrary continuation, so no
body or observable continuation is discarded.

The configuration contains all state used by the program: computation,
integer-variable environment, and result. The submitted program has no heap,
I/O, allocation, nested calls, exceptions, closures, or other state that needs
modeling. The rules have no competing local left-hand sides on a reachable
front term except the non-overlapping terminal-return forms just described.

## Verification rules

1. **V1, lines 10-11 — `loopCondition` macro.** Expands to the exact submitted
   `i < n` AST.
2. **V2, lines 13-18 — `loopBody` macro.** Expands to the exact submitted tuple
   rotation/tribonacci update followed by `i = i + 1`.
3. **V3, lines 20-28 — `fibfibProgram` macro.** Expands to the full submitted
   MPY AST. `stage4_pinning.log` records byte-identical expanded KORE.
4. **V4, line 30 — base equation.** Defines `fibfibMath(N)=0` for `N<=1`.
5. **V5, line 31 — base equation.** Defines `fibfibMath(2)=1`.
6. **V6, lines 32-35 — recurrence equation.** For `N>=3`, defines the value as
   the sum at `N-1,N-2,N-3`.

V4-V6 partition all mathematical integers into disjoint guards
`N<=1`, `N=2`, and `N>=3`, so the `[total]` declaration is covered and
non-overlapping. V6 strictly descends on its `N>=3` domain. The negative
extension supplied by V4 is never connected to a candidate claim because both
claims require nonnegative indices. On `N>=0`, these equations are exactly the
prompt recurrence; `fibfibMath` is therefore a defined mathematical function,
not an opaque result oracle.

## Claims

1. **P1 `program-correct`.** Executes V3's exact program through O1-O23 from
   empty state for every `N>=0`; constrains final `result` to
   `fibfibMath(N)` and the complete environment to consecutive sequence values.
2. **P2 `loop-invariant`.** From `0<=I<=N` and consecutive sequence values at
   indices `I,I+1,I+2`, executes the real while term plus terminal return. One
   true iteration changes the triple to indices `I+1,I+2,I+3` by V6 and
   increments `i`; the false branch plus `I<=N` yields `I=N`. It constrains both
   result and the complete environment.

No claim introduces a right-only/free result variable, one-way implication, or
oracle. `stage6_nonvacuity.log` records rejection of the false `result+1`
obligation.

## Static decision

All local rules are sound on their complete declared behavior or, for partial
syntax families, stop visibly outside the implemented subset. No rule replaces
the property-bearing loop or tuple computation with a summary. No concrete or
symbolic false-conclusion witness exists for a candidate-local rule on the
formal `N>=0` domain. The trust boundary is limited to standard K parser/list
elaboration and the imported `INT`, `BOOL`, and `MAP` primitives.

# Exhaustive local K declaration and rule review

Sources reviewed: the scratch copies of `semantic.k`, `verification.k`, and
`spec.k` under `/tmp/audit-work/63-fibfib/candidate`. Built-in modules are
listed in the trust ledger rather than re-inventoried here.

## Syntax declarations

`FIBFIB-SYNTAX` declares exactly these source constructors:

1. `Pgm`: `Module(Stmts)`.
2. `Stmts`: an empty-separated `List{Stmt,""}`.
3. `Stmt`: `FuncDef(String,Params,Stmts)`.
4. `Stmt`: `Assign(Expr,Expr)`.
5. `Stmt`: `While(Expr,Stmts)`.
6. `Stmt`: `Return(Expr)`.
7. `Params`: `Params(Strings)`.
8. `Strings`: comma-separated `List{String,","}`.
9. `Expr`: `Name(String)`.
10. `Expr`: `Int(Int)`.
11. `Expr`: `BinOp(String,Expr,Expr)`.
12. `Expr`: `Compare(Expr,CmpOps)`.
13. `Expr`: `TupleExpr(Exprs)`.
14. `Exprs`: comma-separated `List{Expr,","}`.
15. `CmpOp`: `CmpOp(String,Expr)`.
16. `CmpOps`: comma-separated `List{CmpOp,","}`.

The operational module declares exactly twelve continuation/control `KItem`
productions: `invoke`, `finish`, `assignTo`, `binRhs`, `applyBin`,
`compareRhs`, `applyCompare`, `tupleSecond`, `tupleThird`, `tupleStore`,
`whileDecision`, and `returnValue`. It declares `Int` and `Bool` as `KResult`.

The verification module declares exactly:

1. `fibfibMath(Int):Int` with `[function,total]`;
2. `fibfibProgram:Pgm` with `[macro]`;
3. `loopCondition:Expr` with `[macro]`;
4. `loopBody:Stmts` with `[macro]`.

There are no local opaque symbols, priority declarations, `functional`
attributes, simplification rules, or concrete rules. The only `total`
declaration is `fibfibMath`.

## Configuration

The sole configuration is `<fibfib>` with:

- `<k>` initially containing `$PGM:Pgm ~> invoke($N:Int)`;
- `<env>` initially `.Map`;
- `<result>` initially `0`.

Every cell is read or written: `<k>` drives execution, `<env>` stores the
parameter and locals, and `<result>` receives the returned integer. There is no
heap, I/O, exception, or call-stack cell because the submitted straight-line
single-function program needs none under the chosen direct-invocation
representation.

## Operational rules in `semantic.k`

1. Lines 59–61, module invocation: for the exact binding
   `Module(FuncDef("fibfib",Params("n"),BODY))`, bind `n` to `N` in an empty
   environment and execute `BODY ~> finish`. This pins the only submitted
   function and does not summarize its body.
2. Line 63, nonempty statement list: expose the head statement before the tail.
   This is the list's left-to-right sequencing rule.
3. Line 64, empty statement list: consume `.Stmts`.
4. Line 66, integer literal: `Int(I)` evaluates to the K integer `I`.
5. Lines 67–68, name lookup: read the integer bound to `X`; absence or a
   non-integer binding gets stuck visibly.
6. Line 70, binary dispatch: evaluate `E1`, retaining `E2` and the operator.
7. Line 71, binary second operand: after the first integer, evaluate `E2`.
8. Line 72, addition: apply unbounded K integer addition for the only used
   operator, `"+"`; other operator strings get stuck.
9. Line 74, comparison dispatch: evaluate the left operand.
10. Line 75, comparison second operand: evaluate the right operand after the
    left integer.
11. Line 76, less-than: apply K integer `<` for the only used comparator;
    other comparator strings get stuck.
12. Line 78, simple assignment dispatch: evaluate the RHS before storing.
13. Lines 79–80, simple assignment store: update the map binding for `X`.
14. Lines 82–83, three-name tuple assignment dispatch: evaluate `E1` first
    while retaining all target names and remaining RHS expressions.
15. Lines 84–85, tuple second operand: retain `I1`, then evaluate `E2`.
16. Lines 86–87, tuple third operand: retain `I1,I2`, then evaluate `E3`.
17. Lines 88–89, tuple store: after all RHS values are known, perform the three
    map updates in target order. For the submitted distinct targets this is
    exactly Python's simultaneous RHS-before-LHS behavior.
18. Line 91, while dispatch: evaluate the guard and retain the guard/body.
19. Lines 92–93, true while branch: execute the body then recreate the same
    while term, so the guard is re-evaluated.
20. Line 94, false while branch: consume the loop only after the evaluated
    guard is `false`.
21. Line 96, return dispatch: evaluate the return expression.
22. Lines 97–98, return after the submitted final statement: in the exact
    `.Stmts ~> finish` suffix, consume control and store the returned integer.
23. Lines 99–100, return after an already-consumed empty tail: do the same in
    the exact `finish` suffix.

The source has 23 logical operational rules (the multi-line cell rules above
are each one K rule). None is an operational proof bridge: all occur in the
generated language semantics and small-step through the real constructor term.
The two return rules deliberately accept only the two final-statement
continuations reachable in this program; they do not discard an arbitrary
continuation.

## Verification rules

1. Lines 10–11 expand `loopCondition` to the exact
   `Compare(Name("i"),CmpOp("<",Name("n")))` constructor.
2. Lines 13–18 expand `loopBody` to the exact tuple assignment followed by
   `i = i + 1`.
3. Lines 20–28 expand `fibfibProgram` to the complete submitted function term.
   Fresh `kast --expand-macros` output for this term is byte-identical to
   freshly parsed `solution.mpy` JSON (`04-program-pinning.log`).
4. Line 30 defines `fibfibMath(N)=0` for `N<=1`.
5. Line 31 defines `fibfibMath(2)=1`.
6. Lines 32–35 define the sum of the preceding three values for `N>=3`.

Rules 1–3 are parse-time macro definitions, not execution summaries. Rules
4–6 are a definitional mathematical summary and never rewrite a submitted
program operation. Their guards are exhaustive over `Int`, pairwise disjoint,
and their recursive branch strictly decreases until a base case. The negative
part of rule 4 is a harmless total extension of a newly defined symbol; every
claim use is nonnegative. On `N>=0` the equations are exactly the trusted
contract's recurrence.

## Claims

1. `program-correct` starts the macro-expanded real program in an empty
   environment for arbitrary `N>=0`, invokes it, and requires `.K`, the exact
   final local environment, and result `fibfibMath(N)`.
2. `loop-invariant` starts at the real loop with the real final return suffix
   for arbitrary `0<=I<=N`; its environment is the usual three-consecutive-
   values invariant and its destination fixes the exact final environment and
   result.

Neither claim has an `ensures`, free result oracle, existential result, or
one-way implication in place of equality. Both preconditions are satisfiable:
for example, the entry state with `N=5`, and the loop state `I=0,N=5`,
`a=0,b=0,c=1,i=0,n=5` (with any initial result).

## Construct coverage and overlaps

The regenerated program uses exactly `Module`, `FuncDef`, `Params`, statement
lists, `Assign`, `While`, `Return`, `Name`, `Int`, `BinOp("+")`,
`Compare`/`CmpOp("<")`, and three-element `TupleExpr`; every one maps to the
declarations and rules above. Evaluation is deterministic on the used subset.
The simple and tuple assignment rules have disjoint target shapes; the true and
false loop rules are disjoint; the two terminal return rules have distinct
continuation shapes; and the three `fibfibMath` guards are disjoint.

The definition intentionally is not general Python: other operators, other
bindings/modules, early returns with nonempty tails, exceptions, and other AST
constructors are absent or stuck. None occurs in the submitted term, so this is
a scope boundary rather than a fabricated result for a used construct.

No local rule was found unsound, so there is no false-conclusion witness to
report for an alleged unsound rule. The separate body-sensitivity mutation
does produce a concrete false obligation: returning `b` at `I=N=1` requires
`fibfibMath(2)=fibfibMath(1)`, i.e. `1=0`; the prover rejects it in
`04-body-mutation-kprove.log`.

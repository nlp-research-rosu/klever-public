# Exhaustive local K declaration and rule inventory

Sources inventoried: scratch copies of candidate `semantic.k`,
`verification.k`, and `spec.k`. There are no other candidate `.k` helper
files. Line numbers below refer to the immutable candidate source layout.

## Local syntax declarations

| ID | File:line | Declaration (all alternatives included) | Attributes / role |
|---|---|---|---|
| D01 | `semantic.k:6` | `Pgm ::= Module(Stmts)` | Program root constructor. |
| D02 | `semantic.k:8` | `Stmts ::= List{Stmt,""}` | Statement sequence, with generated cons and `.Stmts` identity. |
| D03 | `semantic.k:9-11` | `Stmt ::= FuncDef(String,Params,Stmts) \| Return(Expr) \| If(Expr,Stmts,Stmts)` | All statement constructors admitted by the local grammar. |
| D04 | `semantic.k:13` | `Params ::= Params(Strings)` | Parameter-list wrapper. |
| D05 | `semantic.k:14` | `Strings ::= List{String,","}` | String list. |
| D06 | `semantic.k:16-20` | `Expr ::= Int(Int) \| Name(String) \| BinOp(String,Expr,Expr) \| Compare(Expr,CmpOps) \| ListExpr(Exprs)` | All expression constructors admitted by the local grammar. |
| D07 | `semantic.k:22` | `CmpOp ::= CmpOp(String,Expr)` | One comparison-operation item. |
| D08 | `semantic.k:23` | `CmpOps ::= List{CmpOp,","}` | Comparison-operation list. |
| D09 | `semantic.k:24` | `Exprs ::= List{Expr,","}` | Expression list. |
| D10 | `semantic.k:26` | `Args ::= args(Int,Int,Int)` | Audit entry wrapper for exactly three integer arguments. |
| D11 | `semantic.k:27` | `Result ::= result(Int,Int)` | Observable two-integer result wrapper. |
| D12 | `semantic.k:34-36` | `PyVal ::= intVal(Int) \| boolVal(Bool) \| listVal(PyVals)` | Interpreter values. |
| D13 | `semantic.k:37` | `PyVals ::= List{PyVal,","}` | Interpreter-value list. |
| D14 | `semantic.k:39-40` | `Outcome ::= normal \| returned(PyVal)` | Normal versus abrupt-return control. |
| D15 | `semantic.k:42` | `KItem ::= run(Pgm,Args)` | Top-level execution request. |
| D16 | `semantic.k:45` | `Result ::= carrotContract(Int,Int,Int)` | `[function,total]`; equations supplied in `verification.k`. |
| D17 | `semantic.k:46` | `Bool ::= validInput(Int,Int,Int)` | `[function,total]`; equation supplied in `verification.k`. |
| D18 | `semantic.k:47` | `Pgm ::= solutionProgram` | `[function]`; exact program equation supplied in `verification.k`. |
| D19 | `semantic.k:49` | `PyVal ::= lookup(String,Map)` | `[function,total]`. |
| D20 | `semantic.k:52` | `PyVal ::= evalExpr(Expr,Map)` | `[function,total]`. |
| D21 | `semantic.k:64-66` | `PyVal ::= addVals(PyVal,PyVal) \| subVals(PyVal,PyVal) \| leVals(PyVal,PyVal)` | Each alternative is `[function,total]`. |
| D22 | `semantic.k:74-77` | `Outcome ::= evalStmts(Stmts,Map) \| evalStmt(Stmt,Map) \| continueWith(Outcome,Stmts,Map) \| chooseBranch(PyVal,Stmts,Stmts,Map)` | Each alternative is `[function,total]`. |
| D23 | `semantic.k:90` | `Result ::= resultOf(Outcome)` | `[function,total]`. |

There are 13 local function symbols: `carrotContract`, `validInput`,
`solutionProgram`, `lookup`, `evalExpr`, `addVals`, `subVals`, `leVals`,
`evalStmts`, `evalStmt`, `continueWith`, `chooseBranch`, and `resultOf`.
Twelve are marked `total`; only `solutionProgram` is not. There are no local
`functional`, `opaque`, `simplification`, `concrete`, `owise`, `anywhere`,
or priority attributes and no priority declarations.

## Configuration

`semantic.k:93-96` declares exactly one generated top cell, `<mpy>`, containing
one `<k>` cell initially set to `run($PGM:Pgm,$ARGS:Args)`. There is no mutable
heap, output, exception, allocation, or ambient state cell. That is adequate
for this submitted pure, integer-only function because only its returned
two-element list is observable under the task contract.

## `semantic.k` rules

| ID | File:line | Rule / complete domain | Classification and audit |
|---|---|---|---|
| S01 | 50 | `lookup(X,(X \|-> V:PyVal) REST) => V` | Interpreter equation. Correct for a K map containing `X`; the exact `run` map contains each of the three distinct parameter keys. Not exhaustive over all `(String,Map)` despite `[total]`. |
| S02 | 53 | `evalExpr(Int(I),_) => intVal(I)` | Constructor interpretation; exact. |
| S03 | 54 | `evalExpr(Name(X),RHO) => lookup(X,RHO)` | Name lookup; exact when bound. Every submitted name is bound by S21. |
| S04 | 55-56 | `evalExpr(BinOp("+",L,R),RHO) => addVals(evalExpr(L,RHO),evalExpr(R,RHO))` | Addition interpretation. Both operands are pure in the submitted term, so lack of an explicit side-effect evaluation-order cell is immaterial. |
| S05 | 57-58 | Same for `BinOp("-"... )` and `subVals` | Subtraction interpretation; same purity observation. |
| S06 | 59-60 | `Compare(L,CmpOp("<=",R))` to `leVals(...)` | Exact single `<=` comparison used by the program. |
| S07 | 61-62 | Exactly two-element `ListExpr(FIRST,SECOND)` to `listVal(...)` | Exact submitted return-list arity. Evaluation order cannot affect this pure term. |
| S08 | 67 | `addVals(intVal(A),intVal(B)) => intVal(A +Int B)` | Exact unbounded integer addition. |
| S09 | 68 | `subVals(intVal(A),intVal(B)) => intVal(A -Int B)` | Exact unbounded integer subtraction. |
| S10 | 69-70 | `leVals(intVal(A),intVal(B)) => boolVal(true)` when `A <= B` | True branch of integer comparison. |
| S11 | 71-72 | Same to `false` when `B < A` | False branch. S10/S11 guards are disjoint and exhaustive on integer arguments. |
| S12 | 78 | `evalStmts(.Stmts,_) => normal` | Empty sequence finishes normally. |
| S13 | 79-80 | `evalStmts(S REST,RHO) => continueWith(evalStmt(S,RHO),REST,RHO)` | Head-first statement sequencing. No state update exists in this language subset. |
| S14 | 81 | `continueWith(normal,REST,RHO) => evalStmts(REST,RHO)` | Normal control proceeds to the tail. |
| S15 | 82 | `continueWith(returned(V),_,_) => returned(V)` | Return skips the remaining sequence, correctly modeling the first branch’s early return. |
| S16 | 84 | `evalStmt(Return(E),RHO) => returned(evalExpr(E,RHO))` | Return evaluation. |
| S17 | 85-86 | `evalStmt(If(C,T,E),RHO) => chooseBranch(evalExpr(C,RHO),T,E,RHO)` | Guard evaluation followed by branch selection. |
| S18 | 87 | `chooseBranch(boolVal(true),THEN,_,RHO) => evalStmts(THEN,RHO)` | True branch. |
| S19 | 88 | Same for `false` and `ELSE` | False branch. S18/S19 are constructor-disjoint. |
| S20 | 91 | `resultOf(returned(listVal(intVal(A),intVal(B)))) => result(A,B)` | Observable bridge from the exact returned two-integer list to the audit result wrapper. It preserves both requested list elements. |
| S21 | 98-107 | `run(Module(FuncDef("eat",Params("number","need","remaining"),BODY)),args(N,K,R)) => resultOf(evalStmts(BODY,parameter-map))` | Top-level operational rule. It accepts an arbitrary body but pins function name, arity, parameter order, and bindings. It executes `BODY`; it does not summarize or replace it. The exact candidate module has this shape. |

S21 is the only ordinary top-level operational rewrite. S01-S20 are equations
for declared K functions. No rule changes or omits an observable state cell,
because the generated configuration has no such additional cell.

## `verification.k` rules

| ID | File:line | Rule / complete domain | Classification and audit |
|---|---|---|---|
| V01 | 7-9 | `carrotContract(N,K,R) => result(N+K,R-K)` if `K <= R` | Definitional specification summary, not an operational bridge. The guard is the enough-stock source branch. |
| V02 | 10-12 | `carrotContract(N,K,R) => result(N+R,0)` if `R < K` | Complementary specification equation. V01/V02 guards are disjoint and exhaustive for all K integers. |
| V03 | 14-17 | `validInput(N,K,R)` to the conjunction `0<=N,K,R<=1000` | Unconditional definitional Boolean equation; exact transcription of the prompt. |
| V04 | 20-35 | `solutionProgram => Module(FuncDef("eat",...exact body...))` | Definitional binding, not an execution shortcut. The extracted RHS and trusted-regenerated `solution.mpy` parse to identical constructor JSON after only `.Stmts` list-identity normalization (`04-program-pinning.log`). |

No V-rule rewrites `run`, `evalStmts`, `evalStmt`, `evalExpr`, or any
intermediate program operation to `carrotContract`. The contract symbol occurs
only in the claim destination and reduces independently after the actual body
reduces. Thus there is no result-bearing oracle shared between execution and
postcondition and no operational bridge requiring a separate connection
theorem.

## Reachability claims

`spec.k` contains six positive entry claims and no helper/loop claims:

1. bounded inputs with `need <= remaining`, destination `carrotContract`;
2. bounded inputs with `remaining < need`, destination `carrotContract`;
3. input `(5,6,10)`, destination `result(11,4)`;
4. input `(4,8,9)`, destination `result(12,1)`;
5. input `(1,10,10)`, destination `result(11,0)`;
6. input `(2,11,5)`, destination `result(7,0)`.

Claims 1 and 2 partition the complete documented integer domain. The other four
are redundant example claims. There are no circularities, invariants, helper
claims, framed continuations, existential result variables, or omitted
observable cells.

## Submitted-term coverage and descent

Every constructor in `solution.mpy` is covered:

- `Module`/`FuncDef`/`Params` and argument binding: S21;
- statement-list cons/identity: S12-S13;
- `If`: S17-S19;
- `Return` and return control: S14-S16;
- `Compare`, `CmpOp("<=")`, and `Name`: S03, S06, S10-S11;
- `ListExpr` of arity two: S07;
- `BinOp("+")` and `BinOp("-")`: S04-S05, S08-S09;
- `Int(0)`: S02;
- final returned two-integer list: S20.

Descent is structural: expression rules recurse into strict subexpressions,
statement sequencing consumes a head, branch selection chooses one finite
subsequence, and every submitted leaf closes. The submitted function has no
loop or recursion.

## Totality warning boundary

The fresh LLVM compile reports non-exhaustive matches for ten declarations
marked `[total]` in standalone `semantic.k`: the two proof-layer symbols before
their equations are imported, plus `lookup`, `evalExpr`, `addVals`, `subVals`,
`leVals`, `evalStmt`, `chooseBranch`, and `resultOf` (with related interpreter
symbols covered by the same warning group). Concrete out-of-scope examples
include `lookup("missing",.Map)`, `evalExpr(BinOp("*",...),RHO)`,
`addVals(listVal(...),intVal(1))`, `evalStmt(FuncDef(...),RHO)`,
`chooseBranch(intVal(1),...)`, and `resultOf(normal)`.

Those annotations are therefore globally over-broad and should have been
omitted or the function domains narrowed. This is an evidence/trust-boundary
limitation, not a witnessed false theorem on the intended domain: every
function call reachable from the mechanically pinned submitted term has the
covered constructor and binding shapes listed above, and fresh symbolic and
ground executions close without invoking an uncovered case. Per the benchmark
boundary, unused constructs need not be modeled, and no unsound-rule label is
assigned without an intended-domain false-conclusion witness.

# Exhaustive local K inventory

Scope: submitted `semantic.k`, generated `solution-program.k`,
`verification.k`, and the positive `spec.k`. Imported `DOMAINS` is listed
separately as the K builtin trust boundary.

## Syntax and configuration inventory

The table represents 20 individual syntax productions (counting alternatives)
and one configuration declaration.

| ID | File:line | Declaration | Used construct / assessment |
|---|---|---|---|
| D1 | `semantic.k:4` | `Program ::= Module(Stmts)` | Top-level translated module; used once and consumed by R1. |
| D2 | `semantic.k:6` | `Stmts ::= List{Stmt,""}` | Ordered statement sequence; K's generated list unit/constructor are used by R2/R3. |
| D3 | `semantic.k:7` | `Stmt ::= FuncDef(String,Params,Stmts)` | Exact submitted binding; consumed by R1. |
| D4 | `semantic.k:8` | `Stmt ::= If(Expr,Stmts,Stmts)` | Every source `if`; R4–R7 select branches. |
| D5 | `semantic.k:9` | `Stmt ::= Return(Expr)` | Every source return; R8–R14 terminate execution. |
| D6 | `semantic.k:11` | `Params ::= Params(Names)` | Exact function parameter wrapper; consumed by R1. |
| D7 | `semantic.k:12` | `Names ::= List{String,","}` | Two translated parameter names; structural only. |
| D8 | `semantic.k:14` | `Expr ::= Name(String)` | Only `planet1` and `planet2`; consumed inside R4–R7. |
| D9 | `semantic.k:15` | `Expr ::= Str(String)` | Planet-name literals and tuple elements; consumed inside R4–R14. |
| D10 | `semantic.k:16` | `Expr ::= Compare(Expr,CmpOp)` | All source guards; consumed inside R4–R7. |
| D11 | `semantic.k:17` | `Expr ::= TupleExpr(Exprs)` | All returned tuple literals; consumed by R8–R14. |
| D12 | `semantic.k:18` | `CmpOp ::= CmpOp(String,Expr)` | All used operators are the literal `"=="`; R4–R7 match it exactly. |
| D13 | `semantic.k:19` | `Exprs ::= List{Expr,","}` | Tuple-expression element sequence, arities 0–6. |
| D14 | `semantic.k:25` | `KItem ::= invokeBF(String,String)` | External top-level invocation appended after the submitted module. |
| D15 | `semantic.k:26` | `KItem ::= execStmt(Stmt)` | Internal sequencing marker introduced only by R2. |
| D16 | `semantic.k:27` | `Result ::= noResult` | Initial result sentinel. |
| D17 | `semantic.k:28` | `Result ::= tupleValue(StringValues)` | Observable tuple result. |
| D18 | `semantic.k:29` | `StringValues ::= List{String,","}` | Observable tuple elements, preserving order. |
| D19 | `semantic.k:31-37` | `<bf>` with `<k>`, `<planet1>`, `<planet2>`, `<result>` | Exactly the computation, two immutable argument slots, and one result slot needed by this program. No heap, I/O, allocation, or exceptions are used. |
| D20 | `solution-program.k:6` | `Program ::= solutionProgram` | Proof constant whose sole rewrite is the normalized translator term. |
| D21 | `verification.k:8` | `KItem ::= verifyBF(String,String)` | Proof entry wrapper. |

There are no local declarations with `function`, `total`, `functional`,
`simplification`, `macro`, `anywhere`, `priority`, or `opaque` attributes.
There are no local contexts, aliases, lemmas, helper claims, fresh symbols, or
unconstrained result symbols. `spec.k` contains 73 positive entry claims and no
rules.

## Ordinary rule inventory

| ID | File:line | Rule and matched context | Classification and static assessment |
|---|---|---|---|
| R1 | `semantic.k:39-44` | Exact `Module(FuncDef("bf",Params("planet1","planet2"),BODY)) ~> invokeBF(P1,P2)` in initially empty argument cells rewrites to `BODY` and stores both arguments. | Operational semantics. Correct binding and argument initialization for the exact submitted one-function module. It preserves the framed K suffix and result cell. |
| R2 | `semantic.k:46` | Head `S` of nonempty `Stmts` becomes `execStmt(S) ~> REST`. | Operational semantics. Preserves source order and the framed K continuation. |
| R3 | `semantic.k:47` | Empty `.Stmts` becomes `.K`. | Operational semantics. Correct no-op for an exhausted statement list. |
| R4 | `semantic.k:49-54` | `planet1 == S` source guard with builtin equality true selects `THEN`. | Operational semantics. Guard is exactly the source comparison and reads only `planet1`; no state changes. |
| R5 | `semantic.k:56-61` | Same `planet1` guard with builtin inequality selects `ELSE`. | Operational semantics. Complementary to R4. Builtin String equality/inequality make R4/R5 disjoint and exhaustive. |
| R6 | `semantic.k:63-68` | `planet2 == S` source guard with builtin equality true selects `THEN`. | Operational semantics. Same assessment as R4 for `planet2`. |
| R7 | `semantic.k:70-75` | Same `planet2` guard with builtin inequality selects `ELSE`. | Operational semantics. Same assessment as R5 for `planet2`. |
| R8 | `semantic.k:77-78` | Return empty tuple; discard current function's remaining statement continuation; set empty `tupleValue`. | Operational semantics. Correct top-level Python return and exact empty tuple for a pure literal. |
| R9 | `semantic.k:80-81` | Return one-string tuple. | Operational semantics. Preserves the sole literal and order. |
| R10 | `semantic.k:83-84` | Return two-string tuple. | Operational semantics. Preserves both literals and order. |
| R11 | `semantic.k:86-90` | Return three-string tuple. | Operational semantics. Preserves all literals and order. |
| R12 | `semantic.k:92-97` | Return four-string tuple. | Operational semantics. Preserves all literals and order. |
| R13 | `semantic.k:99-105` | Return five-string tuple. | Operational semantics. Preserves all literals and order. |
| R14 | `semantic.k:107-114` | Return six-string tuple. | Operational semantics. Preserves all literals and order. |
| R15 | `solution-program.k:7-228` | `solutionProgram` rewrites to the complete normalized `Module(FuncDef(...))` translator term. | Definitional constant, not an oracle. The independent pinning check proves byte equality after only explicit empty-list normalization. Body mutation changes this RHS and makes the original target proof fail. |
| R16 | `verification.k:10-12` | `verifyBF(P1,P2)` becomes `solutionProgram ~> invokeBF(P1,P2)`. | Proof entry harness. It forces R15 and then R1; it neither fixes nor fabricates the result. It preserves the framed continuation. |

## Construct-to-rule coverage

Every constructor in `solution.mpy` is covered: `Module` and `FuncDef` by R1;
statement-list structure by R2/R3; all `If`/`Compare`/`Name`/`CmpOp("==")`
forms by R4–R7; and every `Return`/`TupleExpr`/`Str` form (only tuple arities
0–6 occur) by R8–R14. `Params`, `Names`, and the exact binding are matched by
R1. No used constructor is silently fabricated or left without a rule.

## Imported trust boundary and overlap/control review

`DOMAINS` supplies K's `String` token, `==String`, `=/=String`, `andBool`, and
the standard K/list machinery. These are fixed K primitives, not
candidate-defined functions. The proof relies on ordinary mathematical string
equality being total, with equality and inequality complementary.

R4/R5 and R6/R7 are the only same-shape overlaps; their guards are disjoint and
exhaustive. R8–R14 are disjoint by tuple-list arity. R2 does not overlap R3
because one requires a nonempty list. R15 and R16 use distinct symbols.

Evaluation order is source statement order. Guards are pure string comparisons.
The program has no assignments, heap, calls from expressions, allocation, I/O,
exceptions, loops, or mutable effects. A return discards the rest of this
top-level invocation, which is correct for every reachable submitted-program
state. The return rules are not a reusable model of nested calls or arbitrary
post-call continuations; those configurations are outside the submitted
program and its exact entry claims.

No inventoried rule derives a false conclusion on the intended string-input
domain. No task answer is encoded in the semantics: the planet-specific branch
table resides only in the mechanically pinned submitted program term, and the
semantics applies generic equality, sequencing, branch, and literal-return
rules to it.

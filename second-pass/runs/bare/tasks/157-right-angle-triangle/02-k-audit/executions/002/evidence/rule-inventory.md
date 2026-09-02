# Reviewer rule inventory

Sources inventoried: `/candidate/semantic.k`, `/candidate/verification.k`, and
`/candidate/spec.k`. There are no other candidate `.k` or helper K files.

## Local syntax and attributes

- `MPY-SYNTAX` imports `INT-SYNTAX`, `BOOL-SYNTAX`, and `STRING-SYNTAX`.
- `Expr`: `Int(Int)`, `Name(String)`, `BinOp(String,Expr,Expr)`,
  `Compare(Expr,CmpOp)`, and `BoolOp(String,Exprs)`.
- `CmpOp`: `CmpOp(String,Expr)`.
- `Exprs`: comma-separated `List{Expr,","}`.
- `Params`: `Params(Strings)`.
- `Strings`: comma-separated `List{String,","}`.
- `Stmt`: `FuncDef(String,Params,Stmts)` and `Return(Expr)`.
- `Stmts`: juxtaposed `List{Stmt,""}`.
- `Program`: `Module(Stmts)`.
- `Ints`: comma-separated `List{Int,","}`.
- `Arguments`: `Args(Ints)`.
- `Input`: `Program` and `run(Program,String,Arguments)`.
- `MPY` imports `MPY-SYNTAX`, `DOMAINS`, and `MAP`.
- `Value`: `iVal(Int)` and `bVal(Bool)`.
- `Result`: `noResult` and `result(Bool)`.
- `KItem`: `bind`, `eval`, `binRight`, `binApply`, `cmpRight`, `cmpApply`,
  `boolTail`, `boolMerge`, and `publish`.
- Configuration: `<mpy>` contains `<k> $PGM:Input </k>`, `<env> .Map </env>`,
  and `<result> noResult </result>`.
- `rightTriangle(Int,Int,Int):Bool` is `[function,total]`.
- `solutionProgram:Program` is `[function]`.
- There are no local `[simplification]`, `[priority]`, `[owise]`,
  `[functional]`, macro, anywhere, or opaque declarations.

## Operational rules in `semantic.k`

1. `run(Module(FuncDef(F,Params(PS),Return(E))),F,Args(IS))` becomes
   `bind(PS,IS) ~> eval(E) ~> publish`.
2. `bind(.Strings,.Ints)` finishes.
3. `bind((P,PS),(I,IS))` updates the map and recurs.
4. `eval(Int(I))` becomes `iVal(I)`.
5. `eval(Name(X))` looks up an integer and becomes `iVal(I)`.
6. `eval(BinOp(OP,L,R))` starts left-to-right evaluation.
7. A left integer value schedules evaluation of the right operand.
8. `binApply("+",I)` computes `I +Int J`.
9. `binApply("*",I)` computes `I *Int J`.
10. `eval(Compare(L,CmpOp(OP,R)))` starts left-to-right evaluation.
11. A left integer value schedules comparison of the right operand.
12. `cmpApply(">",I)` computes `I >Int J`.
13. `cmpApply("==",I)` computes `I ==Int J`.
14. `eval(BoolOp(OP,E,ES))` evaluates the first element.
15. `boolTail` on an empty expression list returns the accumulated Boolean.
16. `boolTail` on a nonempty list evaluates the next element.
17. `boolMerge("and",B,ES)` computes `B andBool C` and continues.
18. `boolMerge("or",B,ES)` computes `B orBool C` and continues.
19. `publish` clears the local environment and stores `result(B)`.

## Equations and claims outside `semantic.k`

1. `rightTriangle(A,B,C)` expands, without a guard, to positivity of all three
   integers conjoined with the disjunction of the three Pythagorean equations.
2. `solutionProgram` expands, without a guard, to the complete constructor term
   copied from `solution.mpy`.
3. `SPEC` has four reachability claims: one symbolic all-`Int` result claim and
   fixed examples `(3,4,5)`, `(1,2,3)`, and `(5,3,4)`.

## Used-constructor coverage

`solution.mpy` uses exactly `Module`, `FuncDef`, `Params`, `Return`, `BoolOp`
with `"and"`/`"or"`, `Compare`, `CmpOp` with `">"`/`"=="`, `Name`, `Int`,
and `BinOp` with `"+"`/`"*"`; the entry wrapper adds `run` and `Args`.
Each has a declaration and every dynamic use has a rule above.

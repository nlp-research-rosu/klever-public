# Exhaustive local K inventory

Generated helper K files: none. `semantic.k` and `verification.k` are the complete local semantic/proof source set.

## Syntax and configuration declarations

01. semantic.k:6-6 module=MPY-SYNTAX kind=syntax attributes=[] :: `syntax Module ::= "Module" "(" Stmts ")"`
02. semantic.k:8-8 module=MPY-SYNTAX kind=syntax attributes=[] :: `syntax Stmts ::= List{Stmt, ""}`
03. semantic.k:9-12 module=MPY-SYNTAX kind=syntax attributes=[] :: `syntax Stmt ::= "ImportFrom" "(" String "," Strings ")" | "FuncDef" "(" String "," Params "," Stmts ")" | "If" "(" Expr "," Stmts "," Stmts ")" | "Return" "(" Expr ")"`
04. semantic.k:14-14 module=MPY-SYNTAX kind=syntax attributes=[] :: `syntax Params ::= "Params" "(" Strings ")"`
05. semantic.k:15-15 module=MPY-SYNTAX kind=syntax attributes=[] :: `syntax Strings ::= List{String, ","}`
06. semantic.k:17-17 module=MPY-SYNTAX kind=syntax attributes=[] :: `syntax Exprs ::= List{Expr, ","}`
07. semantic.k:18-23 module=MPY-SYNTAX kind=syntax attributes=[] :: `syntax Expr ::= "Int" "(" Int ")" | "Name" "(" String ")" | "BinOp" "(" String "," Expr "," Expr ")" | "Compare" "(" Expr "," CmpOps ")" | "ListExpr" "(" Exprs ")" | "Call" "(" Expr "," Exprs ")"`
08. semantic.k:25-25 module=MPY-SYNTAX kind=syntax attributes=[] :: `syntax CmpOps ::= List{CmpOp, ","}`
09. semantic.k:26-26 module=MPY-SYNTAX kind=syntax attributes=[] :: `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"`
10. semantic.k:37-39 module=SEMANTIC kind=syntax attributes=[] :: `syntax Val ::= IntVal(Int) | BoolVal(Bool) | ListVal(List)`
11. semantic.k:41-41 module=SEMANTIC kind=syntax attributes=[] :: `syntax Closure ::= Closure(Params, Stmts)`
12. semantic.k:43-43 module=SEMANTIC kind=syntax attributes=[] :: `syntax Frame ::= Frame(K, Map)`
13. semantic.k:45-46 module=SEMANTIC kind=syntax attributes=[] :: `syntax Result ::= "noResult" | Val`
14. semantic.k:48-51 module=SEMANTIC kind=configuration attributes=[] :: `configuration <k> $PGM:Module </k> <input> $INPUT:Int </input> <result> noResult </result>`
15. semantic.k:53-54 module=SEMANTIC kind=syntax attributes=['function'] :: `syntax MachineState ::= Machine(K, Map, Map, List, Result) [function] | Halted(Map, Map, List, Val)`
16. semantic.k:55-55 module=SEMANTIC kind=syntax attributes=[] :: `syntax ProofState ::= Run(MachineState)`
17. semantic.k:68-81 module=SEMANTIC kind=syntax attributes=[] :: `syntax KItem ::= Invoke(String, List) | Exec(Stmts) | Eval(Expr) | BinLeft(String, Expr) | BinRight(String, Val) | CompareLeft(String, Expr) | CompareRight(String, Val) | "MakeList" | CallOne(String) | CallTwoLeft(String, Expr) | CallTwoRight(String, Val) | Choose(Stmts, Stmts) | "DoReturn" | "Finish"`
18. semantic.k:168-168 module=SEMANTIC kind=syntax attributes=['function'] :: `syntax Map ::= collect(Stmts) [function]`
19. semantic.k:174-174 module=SEMANTIC kind=syntax attributes=['function'] :: `syntax Map ::= bind(Params, List) [function]`
20. semantic.k:177-177 module=SEMANTIC kind=syntax attributes=['function'] :: `syntax Map ::= bindLists(Strings, List) [function]`
21. semantic.k:182-182 module=SEMANTIC kind=syntax attributes=['function'] :: `syntax Val ::= evalBinOp(String, Val, Val) [function]`
22. semantic.k:191-191 module=SEMANTIC kind=syntax attributes=['function'] :: `syntax Val ::= evalCompare(String, Val, Val) [function]`
23. verification.k:8-8 module=SOLUTION-PROGRAM kind=syntax attributes=['function'] :: `syntax Module ::= SolutionModule() [function]`
24. verification.k:33-33 module=SOLUTION-PROGRAM kind=syntax attributes=['function'] :: `syntax Map ::= SolutionFunctions() [function]`
25. verification.k:36-36 module=SOLUTION-PROGRAM kind=syntax attributes=['function'] :: `syntax MachineState ::= SolutionMachine(Int) [function]`
26. verification.k:41-41 module=SOLUTION-PROGRAM kind=syntax attributes=['function'] :: `syntax Map ::= collectStmts(Module) [function]`
27. verification.k:51-51 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Val ::= FactorFrom(Int, Int) [function]`
28. verification.k:65-65 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Val ::= FactorizeSpec(Int) [function]`
29. verification.k:68-68 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Val ::= PrependFactor(Int, Val) [function]`
30. verification.k:73-73 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Int ::= Product(Val) [function]`
31. verification.k:80-80 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Bool ::= OrderedFrom(Val, Int) [function]`
32. verification.k:85-85 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Val ::= MachineValue(MachineState) [function]`
33. verification.k:88-88 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Bool ::= HasDivisor(Int, Int) [function]`
34. verification.k:96-96 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Bool ::= IsPrime(Int) [function]`
35. verification.k:99-99 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Bool ::= AllPrime(Val) [function]`
36. verification.k:104-104 module=VERIFICATION kind=syntax attributes=['function'] :: `syntax Bool ::= ValidFactorization(Int, Val) [function]`
37. verification.k:110-110 module=VERIFICATION kind=syntax attributes=[] :: `syntax Observation ::= Observe(Bool)`

## Rules

01. semantic.k:57-60 module=SEMANTIC id=5d7921c54d0cc10a attributes=[] :: `rule <k> Module(SS) => Machine(Invoke("factorize", ListItem(IntVal(N))) ~> Finish, .Map, collect(SS), .List, noResult) </k> <input> N:Int </input>`
02. semantic.k:62-63 module=SEMANTIC id=c268d415ed1de0ac attributes=[] :: `rule <k> Halted(_, _, _, V:Val) => .K </k> <result> noResult => V </result>`
03. semantic.k:83-87 module=SEMANTIC id=29a404cd93969558 attributes=[] :: `rule Machine(Invoke(F, VS) ~> KREST, OLD, (F |-> Closure(PS, BODY)) FS, STACK, R) => Machine(Exec(BODY), bind(PS, VS), (F |-> Closure(PS, BODY)) FS, ListItem(Frame(KREST, OLD)) STACK, R)`
04. semantic.k:89-90 module=SEMANTIC id=7bd2bf1ca3bac84e attributes=[] :: `rule Machine(Exec(.Stmts) ~> KREST, ENV, FS, STACK, R) => Machine(KREST, ENV, FS, STACK, R)`
05. semantic.k:91-92 module=SEMANTIC id=a8fb5df0d30e5ca4 attributes=[] :: `rule Machine(Exec(Return(E) _REST) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(E) ~> DoReturn ~> KREST, ENV, FS, STACK, R)`
06. semantic.k:93-96 module=SEMANTIC id=49a80c8a0f1a697b attributes=[] :: `rule Machine(Exec(If(COND, THEN, ELSE) REST) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(COND) ~> Choose(THEN, ELSE) ~> Exec(REST) ~> KREST, ENV, FS, STACK, R)`
07. semantic.k:98-101 module=SEMANTIC id=1a1db19f1043e9e3 attributes=[] :: `rule Machine(BoolVal(B) ~> Choose(THEN, _) ~> KREST, ENV, FS, STACK, R) => Machine(Exec(THEN) ~> KREST, ENV, FS, STACK, R) requires B`
08. semantic.k:102-105 module=SEMANTIC id=12b4f965db2b55bf attributes=[] :: `rule Machine(BoolVal(B) ~> Choose(_, ELSE) ~> KREST, ENV, FS, STACK, R) => Machine(Exec(ELSE) ~> KREST, ENV, FS, STACK, R) requires notBool B`
09. semantic.k:107-109 module=SEMANTIC id=60f081d55528fd04 attributes=[] :: `rule Machine(V:Val ~> DoReturn ~> _CURRENT, _, FS, ListItem(Frame(KREST, OLD)) STACK, R) => Machine(V ~> KREST, OLD, FS, STACK, R)`
10. semantic.k:111-112 module=SEMANTIC id=6055815454928edb attributes=[] :: `rule Machine(V:Val ~> Finish, ENV, FS, STACK, noResult) => Halted(ENV, FS, STACK, V)`
11. semantic.k:114-115 module=SEMANTIC id=2ed5d4d0b59ff999 attributes=[] :: `rule Machine(Eval(Int(I)) ~> KREST, ENV, FS, STACK, R) => Machine(IntVal(I) ~> KREST, ENV, FS, STACK, R)`
12. semantic.k:116-118 module=SEMANTIC id=7a89ab66b0753e8b attributes=[] :: `rule Machine(Eval(Name(X)) ~> KREST, (X |-> V) ENV, FS, STACK, R) => Machine(V ~> KREST, (X |-> V) ENV, FS, STACK, R)`
13. semantic.k:120-121 module=SEMANTIC id=768839afbb33675f attributes=[] :: `rule Machine(Eval(ListExpr(.Exprs)) ~> KREST, ENV, FS, STACK, R) => Machine(ListVal(.List) ~> KREST, ENV, FS, STACK, R)`
14. semantic.k:122-123 module=SEMANTIC id=625e976a33eb5d84 attributes=[] :: `rule Machine(Eval(ListExpr(E)) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(E) ~> MakeList ~> KREST, ENV, FS, STACK, R)`
15. semantic.k:124-125 module=SEMANTIC id=a208912725be5c29 attributes=[] :: `rule Machine(V:Val ~> MakeList ~> KREST, ENV, FS, STACK, R) => Machine(ListVal(ListItem(V)) ~> KREST, ENV, FS, STACK, R)`
16. semantic.k:127-130 module=SEMANTIC id=778c9596111d67be attributes=[] :: `rule Machine(Eval(BinOp(OP, LEFT, RIGHT)) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(LEFT) ~> BinLeft(OP, RIGHT) ~> KREST, ENV, FS, STACK, R)`
17. semantic.k:131-134 module=SEMANTIC id=79aefc8e41f9d5c6 attributes=[] :: `rule Machine(V:Val ~> BinLeft(OP, RIGHT) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(RIGHT) ~> BinRight(OP, V) ~> KREST, ENV, FS, STACK, R)`
18. semantic.k:135-137 module=SEMANTIC id=7f098257933eb589 attributes=[] :: `rule Machine(V2:Val ~> BinRight(OP, V1) ~> KREST, ENV, FS, STACK, R) => Machine(evalBinOp(OP, V1, V2) ~> KREST, ENV, FS, STACK, R)`
19. semantic.k:139-142 module=SEMANTIC id=f95861f0678fa133 attributes=[] :: `rule Machine(Eval(Compare(LEFT, CmpOp(OP, RIGHT))) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(LEFT) ~> CompareLeft(OP, RIGHT) ~> KREST, ENV, FS, STACK, R)`
20. semantic.k:143-146 module=SEMANTIC id=afb5667809fbb799 attributes=[] :: `rule Machine(V:Val ~> CompareLeft(OP, RIGHT) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(RIGHT) ~> CompareRight(OP, V) ~> KREST, ENV, FS, STACK, R)`
21. semantic.k:147-149 module=SEMANTIC id=d73f8103b9d5760f attributes=[] :: `rule Machine(V2:Val ~> CompareRight(OP, V1) ~> KREST, ENV, FS, STACK, R) => Machine(evalCompare(OP, V1, V2) ~> KREST, ENV, FS, STACK, R)`
22. semantic.k:151-152 module=SEMANTIC id=83ee6b772af16c94 attributes=[] :: `rule Machine(Eval(Call(Name(F), E)) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(E) ~> CallOne(F) ~> KREST, ENV, FS, STACK, R)`
23. semantic.k:153-154 module=SEMANTIC id=2b47d02fc4590ce3 attributes=[] :: `rule Machine(V:Val ~> CallOne(F) ~> KREST, ENV, FS, STACK, R) => Machine(Invoke(F, ListItem(V)) ~> KREST, ENV, FS, STACK, R)`
24. semantic.k:155-158 module=SEMANTIC id=a9e36e5886bdfffa attributes=[] :: `rule Machine(Eval(Call(Name(F), E1, E2)) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(E1) ~> CallTwoLeft(F, E2) ~> KREST, ENV, FS, STACK, R)`
25. semantic.k:159-162 module=SEMANTIC id=2101ba5fbf2e0674 attributes=[] :: `rule Machine(V:Val ~> CallTwoLeft(F, E2) ~> KREST, ENV, FS, STACK, R) => Machine(Eval(E2) ~> CallTwoRight(F, V) ~> KREST, ENV, FS, STACK, R)`
26. semantic.k:163-166 module=SEMANTIC id=40f24872eda408b7 attributes=[] :: `rule Machine(V2:Val ~> CallTwoRight(F, V1) ~> KREST, ENV, FS, STACK, R) => Machine(Invoke(F, ListItem(V1) ListItem(V2)) ~> KREST, ENV, FS, STACK, R)`
27. semantic.k:169-169 module=SEMANTIC id=9e77abba594f752e attributes=[] :: `rule collect(.Stmts) => .Map`
28. semantic.k:170-170 module=SEMANTIC id=99e2a7ef731fb2ee attributes=[] :: `rule collect(ImportFrom(_, _) REST) => collect(REST)`
29. semantic.k:171-172 module=SEMANTIC id=545f5fbde3ea02c6 attributes=[] :: `rule collect(FuncDef(F, PS, BODY) REST) => collect(REST)[F <- Closure(PS, BODY)]`
30. semantic.k:175-175 module=SEMANTIC id=d8491a9fa5301081 attributes=[] :: `rule bind(Params(PS), VS) => bindLists(PS, VS)`
31. semantic.k:178-178 module=SEMANTIC id=b185700b92b8e48e attributes=[] :: `rule bindLists(.Strings, .List) => .Map`
32. semantic.k:179-180 module=SEMANTIC id=93359a4a5d59fdd6 attributes=[] :: `rule bindLists(P, PS, ListItem(V) VS) => (P |-> V) bindLists(PS, VS)`
33. semantic.k:183-183 module=SEMANTIC id=5ac5bf57e23e3f8f attributes=[] :: `rule evalBinOp("+", IntVal(A), IntVal(B)) => IntVal(A +Int B)`
34. semantic.k:184-184 module=SEMANTIC id=10cc60089ec7f16f attributes=[] :: `rule evalBinOp("*", IntVal(A), IntVal(B)) => IntVal(A *Int B)`
35. semantic.k:185-185 module=SEMANTIC id=8780d45b016df2b8 attributes=[] :: `rule evalBinOp("+", ListVal(A), ListVal(B)) => ListVal(A B)`
36. semantic.k:186-187 module=SEMANTIC id=ba8aefdbee074eaa attributes=[] :: `rule evalBinOp("%", IntVal(A), IntVal(B)) => IntVal(A %Int B) requires B =/=Int 0`
37. semantic.k:188-189 module=SEMANTIC id=b8e8af809001ec43 attributes=[] :: `rule evalBinOp("//", IntVal(A), IntVal(B)) => IntVal(A /Int B) requires B =/=Int 0`
38. semantic.k:192-192 module=SEMANTIC id=094b149a7fe0e34f attributes=[] :: `rule evalCompare("<", IntVal(A), IntVal(B)) => BoolVal(A <Int B)`
39. semantic.k:193-193 module=SEMANTIC id=4c5d322d454dcd96 attributes=[] :: `rule evalCompare(">", IntVal(A), IntVal(B)) => BoolVal(A >Int B)`
40. semantic.k:194-194 module=SEMANTIC id=6936addf30d6a2b2 attributes=[] :: `rule evalCompare("==", IntVal(A), IntVal(B)) => BoolVal(A ==Int B)`
41. verification.k:9-31 module=SOLUTION-PROGRAM id=3429df84f80dc69e attributes=[] :: `rule SolutionModule() => Module( ImportFrom("typing", "List") FuncDef("factorize_from", Params("n", "divisor"), If(Compare(Name("n"), CmpOp("<", Int(2))), Return(ListExpr(.Exprs)), .Stmts) If(Compare(BinOp("*", Name("divisor"), Name("divisor")), CmpOp(">", Name("n"))), Return(ListExpr(Name("n"))), .Stmts) If(Compare(BinOp("%", Name("n"), Name("divisor")), CmpOp("==", Int(0))), Return(BinOp("+", ListExpr(Name("divisor")), Call(Name("factorize_from"), BinOp("//", Name("n"), Name("divisor")), Name("divisor")))), .Stmts) Return(Call(Name("factorize_from"), Name("n"), BinOp("+", Name("divisor"), Int(1))))) FuncDef("factorize", Params("n"), Return(Call(Name("factorize_from"), Name("n"), Int(2)))))`
42. verification.k:34-34 module=SOLUTION-PROGRAM id=4b4014e2d316b15a attributes=[] :: `rule SolutionFunctions() => collectStmts(SolutionModule())`
43. verification.k:37-39 module=SOLUTION-PROGRAM id=93942d336acb8153 attributes=[] :: `rule SolutionMachine(N) => Machine(Invoke("factorize", ListItem(IntVal(N))) ~> Finish, .Map, SolutionFunctions(), .List, noResult)`
44. verification.k:42-42 module=SOLUTION-PROGRAM id=cc4c24a831c4c212 attributes=[] :: `rule collectStmts(Module(SS)) => collect(SS)`
45. verification.k:52-53 module=VERIFICATION id=ff712f7a795e490f attributes=[] :: `rule FactorFrom(N, _) => ListVal(.List) requires N <Int 2`
46. verification.k:54-55 module=VERIFICATION id=1f0b54ab55e8fb8f attributes=[] :: `rule FactorFrom(N, D) => ListVal(ListItem(IntVal(N))) requires N >=Int 2 andBool D >=Int 2 andBool D *Int D >Int N`
47. verification.k:56-59 module=VERIFICATION id=0dd8ebb16a1cdf89 attributes=[] :: `rule FactorFrom(N, D) => PrependFactor(D, FactorFrom(N /Int D, D)) requires N >=Int 2 andBool D >=Int 2 andBool D *Int D <=Int N andBool N %Int D ==Int 0`
48. verification.k:60-63 module=VERIFICATION id=b79a5a3a99e6f946 attributes=[] :: `rule FactorFrom(N, D) => FactorFrom(N, D +Int 1) requires N >=Int 2 andBool D >=Int 2 andBool D *Int D <=Int N andBool N %Int D =/=Int 0`
49. verification.k:66-66 module=VERIFICATION id=3f76b5a8fc09fde2 attributes=[] :: `rule FactorizeSpec(N) => FactorFrom(N, 2)`
50. verification.k:69-70 module=VERIFICATION id=791bee2fff64b05b attributes=[] :: `rule PrependFactor(D, ListVal(L)) => ListVal(ListItem(IntVal(D)) L)`
51. verification.k:74-74 module=VERIFICATION id=c899d5dead04e980 attributes=[] :: `rule Product(ListVal(.List)) => 1`
52. verification.k:75-76 module=VERIFICATION id=cf30c6f26a7add59 attributes=[] :: `rule Product(ListVal(ListItem(IntVal(X)) REST)) => X *Int Product(ListVal(REST))`
53. verification.k:81-81 module=VERIFICATION id=080b1e36af8987ab attributes=[] :: `rule OrderedFrom(ListVal(.List), _) => true`
54. verification.k:82-83 module=VERIFICATION id=a4e314118a229d46 attributes=[] :: `rule OrderedFrom(ListVal(ListItem(IntVal(X)) REST), L) => (L <=Int X) andBool OrderedFrom(ListVal(REST), X)`
55. verification.k:86-86 module=VERIFICATION id=9996537030c58dca attributes=[] :: `rule MachineValue(Halted(_, _, _, V)) => V`
56. verification.k:89-90 module=VERIFICATION id=54b059bac87022a8 attributes=[] :: `rule HasDivisor(N, D) => false requires D *Int D >Int N`
57. verification.k:91-92 module=VERIFICATION id=95d57c93c65b5d61 attributes=[] :: `rule HasDivisor(N, D) => true requires D *Int D <=Int N andBool N %Int D ==Int 0`
58. verification.k:93-94 module=VERIFICATION id=4f4b9fc387bb617a attributes=[] :: `rule HasDivisor(N, D) => HasDivisor(N, D +Int 1) requires D *Int D <=Int N andBool N %Int D =/=Int 0`
59. verification.k:97-97 module=VERIFICATION id=76a5a59533b8b7ae attributes=[] :: `rule IsPrime(N) => (N >=Int 2) andBool notBool HasDivisor(N, 2)`
60. verification.k:100-100 module=VERIFICATION id=57a41a5e9b725f00 attributes=[] :: `rule AllPrime(ListVal(.List)) => true`
61. verification.k:101-102 module=VERIFICATION id=f735be9285819eda attributes=[] :: `rule AllPrime(ListVal(ListItem(IntVal(X)) REST)) => IsPrime(X) andBool AllPrime(ListVal(REST))`
62. verification.k:105-108 module=VERIFICATION id=16d47c536a3ece60 attributes=[] :: `rule ValidFactorization(N, V) => (Product(V) ==Int N) andBool OrderedFrom(V, 2) andBool AllPrime(V)`

## Inventory totals

syntax/configuration declarations=37
local rules=62
local claims outside spec.k=0
priority attributes=0; simplification attributes=0; total attributes=0; opaque declarations=0

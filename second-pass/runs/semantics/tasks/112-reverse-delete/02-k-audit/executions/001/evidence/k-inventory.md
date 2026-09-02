# Exhaustive K source inventory

Entries: 942

| # | File:line | Class | Attributes | Opaque | Source statement |
|---:|---|---|---|---|---|
| 1 | `/candidate/spec.k:6-40` | reachability-claim | — | no | `claim <k> #loop( str(S:IntSeq), Name("character"), If( Compare(Name("character"), CmpOp("not in", Name("c"))), AugAssign(Name("result"), "+", Name("character")) Assign( Name("reversed_result"), BinOp("+", Name("character"), Name("reversed_result"))), .Stmts)) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> ( scope( ( "s" &#124;-> str(ORIG:IntSeq) "c" &#124;-> str(C:IntSeq) "result" &#124;-> str(A:IntSeq)...` |
| 2 | `/candidate/spec.k:46-93` | reachability-claim | — | no | `claim <k> Call( closureVal( ("s", "c"), Assign(Name("result"), Str("")) Assign(Name("reversed_result"), Str("")) Assign(Name("character"), Str("")) For( Name("character"), Name("s"), If( Compare(Name("character"), CmpOp("not in", Name("c"))), AugAssign(Name("result"), "+", Name("character")) Assign( Name("reversed_result"), BinOp("+", Name("character"), Name("reversed_result"))), .Stmts)) Return( TupleExpr( Name("...` |
| 3 | `/candidate/verification.k:8-8` | syntax-declaration | function, total | no | `syntax IntSeq ::= keptAcc(IntSeq, IntSeq, IntSeq) [function, total]` |
| 4 | `/candidate/verification.k:9-9` | ordinary-rule | — | no | `rule keptAcc(.IntSeq, _:IntSeq, A:IntSeq) => A` |
| 5 | `/candidate/verification.k:10-13` | simplification-rule | simplification | no | `rule keptAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, A:IntSeq) => keptAcc(XS, C, A) requires strContains(iCons(X, .IntSeq), C) [simplification]` |
| 6 | `/candidate/verification.k:14-17` | simplification-rule | simplification | no | `rule keptAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, A:IntSeq) => keptAcc(XS, C, seqConcat(A, iCons(X, .IntSeq))) requires notBool strContains(iCons(X, .IntSeq), C) [simplification]` |
| 7 | `/candidate/verification.k:20-20` | syntax-declaration | function, total | no | `syntax IntSeq ::= reversedKeptAcc(IntSeq, IntSeq, IntSeq) [function, total]` |
| 8 | `/candidate/verification.k:21-21` | ordinary-rule | — | no | `rule reversedKeptAcc(.IntSeq, _:IntSeq, A:IntSeq) => A` |
| 9 | `/candidate/verification.k:22-25` | simplification-rule | simplification | no | `rule reversedKeptAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, A:IntSeq) => reversedKeptAcc(XS, C, A) requires strContains(iCons(X, .IntSeq), C) [simplification]` |
| 10 | `/candidate/verification.k:26-29` | simplification-rule | simplification | no | `rule reversedKeptAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, A:IntSeq) => reversedKeptAcc(XS, C, iCons(X, A)) requires notBool strContains(iCons(X, .IntSeq), C) [simplification]` |
| 11 | `/candidate/verification.k:33-33` | syntax-declaration | function, total | no | `syntax Val ::= lastCharacter(IntSeq, Val) [function, total]` |
| 12 | `/candidate/verification.k:34-34` | ordinary-rule | — | no | `rule lastCharacter(.IntSeq, V:Val) => V` |
| 13 | `/candidate/verification.k:35-36` | ordinary-rule | — | no | `rule lastCharacter(iCons(X:Int, XS:IntSeq), _:Val) => lastCharacter(XS, str(iCons(X, .IntSeq)))` |
| 14 | `/candidate/verification.k:44-79` | priority-rule | priority | no | `rule <k> #loop( str(S:IntSeq), Name("character"), If( Compare(Name("character"), CmpOp("not in", Name("c"))), AugAssign(Name("result"), "+", Name("character")) Assign( Name("reversed_result"), BinOp("+", Name("character"), Name("reversed_result"))), .Stmts)) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> ( scope( ( "s" &#124;-> str(ORIG:IntSeq) "c" &#124;-> str(C:IntSeq) "result" &#124;-> str(A:IntSeq) ...` |
| 15 | `/reference/reference-semantics/semantics/assert.k:6-7` | ordinary-rule | — | no | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| 16 | `/reference/reference-semantics/semantics/assert.k:8-11` | ordinary-rule | — | no | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| 17 | `/reference/reference-semantics/semantics/assert.k:13-15` | priority-rule | priority | no | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 18 | `/reference/reference-semantics/semantics/bool.k:8-8` | ordinary-rule | — | no | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 19 | `/reference/reference-semantics/semantics/bool.k:10-10` | ordinary-rule | — | no | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 20 | `/reference/reference-semantics/semantics/bool.k:11-11` | ordinary-rule | — | no | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| 21 | `/reference/reference-semantics/semantics/bool.k:16-16` | evaluation-context | — | no | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 22 | `/reference/reference-semantics/semantics/bool.k:17-17` | ordinary-rule | — | no | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 23 | `/reference/reference-semantics/semantics/bool.k:18-19` | ordinary-rule | — | no | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| 24 | `/reference/reference-semantics/semantics/bool.k:20-21` | ordinary-rule | — | no | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| 25 | `/reference/reference-semantics/semantics/bool.k:22-23` | ordinary-rule | — | no | `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| 26 | `/reference/reference-semantics/semantics/bool.k:24-25` | ordinary-rule | — | no | `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` |
| 27 | `/reference/reference-semantics/semantics/bool.k:29-30` | priority-rule | priority | no | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| 28 | `/reference/reference-semantics/semantics/bool.k:31-34` | priority-rule | priority | no | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 29 | `/reference/reference-semantics/semantics/bool.k:35-38` | priority-rule | priority | no | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 30 | `/reference/reference-semantics/semantics/bool.k:39-42` | priority-rule | priority | no | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 31 | `/reference/reference-semantics/semantics/bool.k:43-46` | priority-rule | priority | no | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 32 | `/reference/reference-semantics/semantics/builtins.k:17-17` | syntax-declaration | function | no | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| 33 | `/reference/reference-semantics/semantics/builtins.k:20-20` | syntax-declaration | function | no | `syntax Int ::= seqLen(Val) [function]` |
| 34 | `/reference/reference-semantics/semantics/builtins.k:21-21` | ordinary-rule | — | no | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 35 | `/reference/reference-semantics/semantics/builtins.k:22-22` | ordinary-rule | — | no | `rule seqLen(list(VS:ValSeq)) => vsLen(VS)` |
| 36 | `/reference/reference-semantics/semantics/builtins.k:23-23` | ordinary-rule | — | no | `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)` |
| 37 | `/reference/reference-semantics/semantics/builtins.k:24-24` | ordinary-rule | — | no | `rule seqLen(str(IS:IntSeq)) => isLen(IS)` |
| 38 | `/reference/reference-semantics/semantics/builtins.k:25-25` | ordinary-rule | — | no | `rule seqLen(setV(DS:IntSeq)) => isLen(DS)` |
| 39 | `/reference/reference-semantics/semantics/builtins.k:26-26` | ordinary-rule | — | no | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| 40 | `/reference/reference-semantics/semantics/builtins.k:32-32` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 41 | `/reference/reference-semantics/semantics/builtins.k:33-33` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 42 | `/reference/reference-semantics/semantics/builtins.k:34-34` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>` |
| 43 | `/reference/reference-semantics/semantics/builtins.k:35-35` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>` |
| 44 | `/reference/reference-semantics/semantics/builtins.k:36-36` | syntax-declaration | function, total | no | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 45 | `/reference/reference-semantics/semantics/builtins.k:37-37` | ordinary-rule | — | no | `rule charsOf(.IntSeq) => .ValSeq` |
| 46 | `/reference/reference-semantics/semantics/builtins.k:38-38` | ordinary-rule | — | no | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| 47 | `/reference/reference-semantics/semantics/builtins.k:41-41` | ordinary-rule | — | no | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| 48 | `/reference/reference-semantics/semantics/builtins.k:44-44` | ordinary-rule | — | no | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| 49 | `/reference/reference-semantics/semantics/builtins.k:47-47` | syntax-declaration | — | no | `syntax KItem ::= #sumAcc(Iterable, Int) &#124; #sumCont(Int)` |
| 50 | `/reference/reference-semantics/semantics/builtins.k:48-48` | ordinary-rule | — | no | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 51 | `/reference/reference-semantics/semantics/builtins.k:49-49` | ordinary-rule | — | no | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 52 | `/reference/reference-semantics/semantics/builtins.k:50-52` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| 53 | `/reference/reference-semantics/semantics/builtins.k:54-54` | syntax-declaration | function | no | `syntax Int ::= intOf(Val) [function]` |
| 54 | `/reference/reference-semantics/semantics/builtins.k:55-55` | ordinary-rule | — | no | `rule intOf(I:Int) => I` |
| 55 | `/reference/reference-semantics/semantics/builtins.k:56-56` | ordinary-rule | — | no | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| 56 | `/reference/reference-semantics/semantics/builtins.k:59-59` | syntax-declaration | — | no | `syntax KItem ::= #allAcc(Iterable) &#124; "#allCont"` |
| 57 | `/reference/reference-semantics/semantics/builtins.k:60-60` | ordinary-rule | — | no | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 58 | `/reference/reference-semantics/semantics/builtins.k:61-61` | ordinary-rule | — | no | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 59 | `/reference/reference-semantics/semantics/builtins.k:62-63` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| 60 | `/reference/reference-semantics/semantics/builtins.k:64-65` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| 61 | `/reference/reference-semantics/semantics/builtins.k:67-67` | syntax-declaration | — | no | `syntax KItem ::= #anyAcc(Iterable) &#124; "#anyCont"` |
| 62 | `/reference/reference-semantics/semantics/builtins.k:68-68` | ordinary-rule | — | no | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 63 | `/reference/reference-semantics/semantics/builtins.k:69-69` | ordinary-rule | — | no | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 64 | `/reference/reference-semantics/semantics/builtins.k:70-71` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| 65 | `/reference/reference-semantics/semantics/builtins.k:72-73` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` |
| 66 | `/reference/reference-semantics/semantics/builtins.k:76-76` | syntax-declaration | — | no | `syntax KItem ::= #maxAcc0(Iterable) &#124; "#maxCont0" &#124; #maxAcc(Iterable, Int) &#124; #maxCont(Int)` |
| 67 | `/reference/reference-semantics/semantics/builtins.k:77-77` | ordinary-rule | — | no | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 68 | `/reference/reference-semantics/semantics/builtins.k:78-79` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 69 | `/reference/reference-semantics/semantics/builtins.k:80-80` | ordinary-rule | — | no | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 70 | `/reference/reference-semantics/semantics/builtins.k:81-81` | ordinary-rule | — | no | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 71 | `/reference/reference-semantics/semantics/builtins.k:82-84` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 72 | `/reference/reference-semantics/semantics/builtins.k:86-86` | syntax-declaration | — | no | `syntax KItem ::= #minAcc0(Iterable) &#124; "#minCont0" &#124; #minAcc(Iterable, Int) &#124; #minCont(Int)` |
| 73 | `/reference/reference-semantics/semantics/builtins.k:87-87` | ordinary-rule | — | no | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 74 | `/reference/reference-semantics/semantics/builtins.k:88-89` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 75 | `/reference/reference-semantics/semantics/builtins.k:90-90` | ordinary-rule | — | no | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 76 | `/reference/reference-semantics/semantics/builtins.k:91-91` | ordinary-rule | — | no | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 77 | `/reference/reference-semantics/semantics/builtins.k:92-94` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 78 | `/reference/reference-semantics/semantics/builtins.k:97-97` | syntax-declaration | function | no | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 79 | `/reference/reference-semantics/semantics/builtins.k:98-98` | ordinary-rule | — | no | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 80 | `/reference/reference-semantics/semantics/builtins.k:99-99` | ordinary-rule | — | no | `rule maxVals(M:Int, .Vals) => M` |
| 81 | `/reference/reference-semantics/semantics/builtins.k:100-100` | ordinary-rule | — | no | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| 82 | `/reference/reference-semantics/semantics/builtins.k:102-102` | syntax-declaration | function | no | `syntax Int ::= minVals(Int, Vals) [function]` |
| 83 | `/reference/reference-semantics/semantics/builtins.k:103-103` | ordinary-rule | — | no | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 84 | `/reference/reference-semantics/semantics/builtins.k:104-104` | ordinary-rule | — | no | `rule minVals(M:Int, .Vals) => M` |
| 85 | `/reference/reference-semantics/semantics/builtins.k:105-105` | ordinary-rule | — | no | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| 86 | `/reference/reference-semantics/semantics/builtins.k:108-109` | ordinary-rule | — | no | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` |
| 87 | `/reference/reference-semantics/semantics/builtins.k:111-113` | ordinary-rule | — | no | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| 88 | `/reference/reference-semantics/semantics/builtins.k:114-114` | syntax-declaration | function, total | no | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 89 | `/reference/reference-semantics/semantics/builtins.k:115-115` | ordinary-rule | — | no | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 90 | `/reference/reference-semantics/semantics/builtins.k:116-116` | ordinary-rule | — | no | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 91 | `/reference/reference-semantics/semantics/builtins.k:117-117` | syntax-declaration | function, total | no | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 92 | `/reference/reference-semantics/semantics/builtins.k:118-118` | ordinary-rule | — | no | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 93 | `/reference/reference-semantics/semantics/builtins.k:119-121` | ordinary-rule | — | no | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` |
| 94 | `/reference/reference-semantics/semantics/builtins.k:124-125` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| 95 | `/reference/reference-semantics/semantics/builtins.k:126-126` | syntax-declaration | function, total | no | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 96 | `/reference/reference-semantics/semantics/builtins.k:127-127` | ordinary-rule | — | no | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 97 | `/reference/reference-semantics/semantics/builtins.k:128-129` | ordinary-rule | — | no | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` |
| 98 | `/reference/reference-semantics/semantics/builtins.k:132-133` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| 99 | `/reference/reference-semantics/semantics/builtins.k:134-134` | syntax-declaration | function, total | no | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 100 | `/reference/reference-semantics/semantics/builtins.k:135-135` | ordinary-rule | — | no | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 101 | `/reference/reference-semantics/semantics/builtins.k:136-136` | ordinary-rule | — | no | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 102 | `/reference/reference-semantics/semantics/builtins.k:137-137` | ordinary-rule | — | no | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| 103 | `/reference/reference-semantics/semantics/builtins.k:140-140` | ordinary-rule | — | no | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| 104 | `/reference/reference-semantics/semantics/builtins.k:143-143` | ordinary-rule | — | no | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 105 | `/reference/reference-semantics/semantics/builtins.k:144-145` | ordinary-rule | — | no | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` |
| 106 | `/reference/reference-semantics/semantics/builtins.k:148-148` | ordinary-rule | — | no | `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))` |
| 107 | `/reference/reference-semantics/semantics/builtins.k:149-149` | ordinary-rule | — | no | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| 108 | `/reference/reference-semantics/semantics/builtins.k:152-153` | ordinary-rule | — | no | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` |
| 109 | `/reference/reference-semantics/semantics/builtins.k:156-157` | ordinary-rule | — | no | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| 110 | `/reference/reference-semantics/semantics/builtins.k:158-158` | syntax-declaration | function, total | no | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 111 | `/reference/reference-semantics/semantics/builtins.k:159-159` | ordinary-rule | — | no | `rule intDigAcc(.IntSeq, ACC:Int) => ACC` |
| 112 | `/reference/reference-semantics/semantics/builtins.k:160-160` | ordinary-rule | — | no | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| 113 | `/reference/reference-semantics/semantics/builtins.k:163-163` | ordinary-rule | — | no | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 114 | `/reference/reference-semantics/semantics/builtins.k:164-164` | ordinary-rule | — | no | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B)` |
| 115 | `/reference/reference-semantics/semantics/builtins.k:167-168` | ordinary-rule | — | no | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| 116 | `/reference/reference-semantics/semantics/builtins.k:169-169` | ordinary-rule | — | no | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>` |
| 117 | `/reference/reference-semantics/semantics/builtins.k:170-170` | ordinary-rule | — | no | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 118 | `/reference/reference-semantics/semantics/builtins.k:171-172` | ordinary-rule | — | no | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| 119 | `/reference/reference-semantics/semantics/builtins.k:173-173` | ordinary-rule | — | no | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>` |
| 120 | `/reference/reference-semantics/semantics/builtins.k:174-174` | ordinary-rule | — | no | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| 121 | `/reference/reference-semantics/semantics/builtins.k:177-177` | ordinary-rule | — | no | `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)` |
| 122 | `/reference/reference-semantics/semantics/builtins.k:178-178` | ordinary-rule | — | no | `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)` |
| 123 | `/reference/reference-semantics/semantics/builtins.k:179-180` | ordinary-rule | — | no | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` |
| 124 | `/reference/reference-semantics/semantics/builtins.k:187-187` | ordinary-rule | — | no | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 125 | `/reference/reference-semantics/semantics/builtins.k:188-188` | syntax-declaration | function | no | `syntax Int ::= evalArith(IntSeq) [function]` |
| 126 | `/reference/reference-semantics/semantics/builtins.k:189-190` | ordinary-rule | — | no | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| 127 | `/reference/reference-semantics/semantics/builtins.k:192-192` | syntax-declaration | — | no | `syntax OpSeq ::= ".OpSeq" &#124; oCons(String, OpSeq)` |
| 128 | `/reference/reference-semantics/semantics/builtins.k:194-194` | syntax-declaration | function, total | no | `syntax Bool ::= evDigit(Int) [function, total]` |
| 129 | `/reference/reference-semantics/semantics/builtins.k:195-195` | ordinary-rule | — | no | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 130 | `/reference/reference-semantics/semantics/builtins.k:196-196` | syntax-declaration | function, total | no | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 131 | `/reference/reference-semantics/semantics/builtins.k:197-197` | ordinary-rule | — | no | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 132 | `/reference/reference-semantics/semantics/builtins.k:198-198` | ordinary-rule | owise | no | `rule evHead42(_:IntSeq) => false [owise]` |
| 133 | `/reference/reference-semantics/semantics/builtins.k:199-199` | syntax-declaration | function, total | no | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 134 | `/reference/reference-semantics/semantics/builtins.k:200-200` | ordinary-rule | — | no | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 135 | `/reference/reference-semantics/semantics/builtins.k:201-201` | ordinary-rule | owise | no | `rule evHead47(_:IntSeq) => false [owise]` |
| 136 | `/reference/reference-semantics/semantics/builtins.k:203-203` | syntax-declaration | function, total | no | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 137 | `/reference/reference-semantics/semantics/builtins.k:204-204` | ordinary-rule | — | no | `rule tokOps(.IntSeq) => .OpSeq` |
| 138 | `/reference/reference-semantics/semantics/builtins.k:205-205` | ordinary-rule | — | no | `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)` |
| 139 | `/reference/reference-semantics/semantics/builtins.k:206-206` | ordinary-rule | — | no | `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)` |
| 140 | `/reference/reference-semantics/semantics/builtins.k:207-207` | ordinary-rule | — | no | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 141 | `/reference/reference-semantics/semantics/builtins.k:208-208` | ordinary-rule | — | no | `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 142 | `/reference/reference-semantics/semantics/builtins.k:209-209` | ordinary-rule | — | no | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 143 | `/reference/reference-semantics/semantics/builtins.k:210-210` | ordinary-rule | — | no | `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 144 | `/reference/reference-semantics/semantics/builtins.k:211-211` | ordinary-rule | — | no | `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))` |
| 145 | `/reference/reference-semantics/semantics/builtins.k:212-212` | ordinary-rule | — | no | `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))` |
| 146 | `/reference/reference-semantics/semantics/builtins.k:214-215` | syntax-declaration | function, total | no | `syntax IntSeq ::= tokNds(IntSeq) [function, total] &#124; tokNdAcc(Int, IntSeq) [function, total]` |
| 147 | `/reference/reference-semantics/semantics/builtins.k:216-216` | ordinary-rule | — | no | `rule tokNds(.IntSeq) => .IntSeq` |
| 148 | `/reference/reference-semantics/semantics/builtins.k:217-217` | ordinary-rule | — | no | `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)` |
| 149 | `/reference/reference-semantics/semantics/builtins.k:218-218` | ordinary-rule | — | no | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 150 | `/reference/reference-semantics/semantics/builtins.k:219-220` | ordinary-rule | — | no | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| 151 | `/reference/reference-semantics/semantics/builtins.k:221-222` | ordinary-rule | — | no | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| 152 | `/reference/reference-semantics/semantics/builtins.k:223-223` | ordinary-rule | owise | no | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 153 | `/reference/reference-semantics/semantics/builtins.k:225-225` | syntax-declaration | — | no | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 154 | `/reference/reference-semantics/semantics/builtins.k:226-226` | syntax-declaration | function, total | no | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 155 | `/reference/reference-semantics/semantics/builtins.k:227-227` | ordinary-rule | — | no | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 156 | `/reference/reference-semantics/semantics/builtins.k:228-228` | ordinary-rule | owise | no | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 157 | `/reference/reference-semantics/semantics/builtins.k:230-230` | syntax-declaration | function, total | no | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 158 | `/reference/reference-semantics/semantics/builtins.k:231-231` | ordinary-rule | — | no | `rule applyOpE("+", A:Int, B:Int) => A +Int B` |
| 159 | `/reference/reference-semantics/semantics/builtins.k:232-232` | ordinary-rule | — | no | `rule applyOpE("-", A:Int, B:Int) => A -Int B` |
| 160 | `/reference/reference-semantics/semantics/builtins.k:233-233` | ordinary-rule | — | no | `rule applyOpE("*", A:Int, B:Int) => A *Int B` |
| 161 | `/reference/reference-semantics/semantics/builtins.k:234-234` | ordinary-rule | — | no | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 162 | `/reference/reference-semantics/semantics/builtins.k:235-235` | ordinary-rule | — | no | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 163 | `/reference/reference-semantics/semantics/builtins.k:236-236` | ordinary-rule | owise | no | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 164 | `/reference/reference-semantics/semantics/builtins.k:238-238` | syntax-declaration | function, total | no | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 165 | `/reference/reference-semantics/semantics/builtins.k:239-239` | ordinary-rule | — | no | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 166 | `/reference/reference-semantics/semantics/builtins.k:240-240` | ordinary-rule | — | no | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 167 | `/reference/reference-semantics/semantics/builtins.k:241-242` | ordinary-rule | — | no | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| 168 | `/reference/reference-semantics/semantics/builtins.k:243-243` | ordinary-rule | owise | no | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 169 | `/reference/reference-semantics/semantics/builtins.k:244-244` | syntax-declaration | function, total | no | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 170 | `/reference/reference-semantics/semantics/builtins.k:245-245` | ordinary-rule | — | no | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 171 | `/reference/reference-semantics/semantics/builtins.k:246-246` | ordinary-rule | — | no | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 172 | `/reference/reference-semantics/semantics/builtins.k:247-247` | syntax-declaration | function, total | no | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 173 | `/reference/reference-semantics/semantics/builtins.k:248-248` | ordinary-rule | — | no | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 174 | `/reference/reference-semantics/semantics/builtins.k:250-250` | syntax-declaration | function, total | no | `syntax EvPair ::= passMulE(EvPair) [function, total] &#124; passAddE(EvPair) [function, total]` |
| 175 | `/reference/reference-semantics/semantics/builtins.k:251-251` | ordinary-rule | — | no | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 176 | `/reference/reference-semantics/semantics/builtins.k:252-252` | ordinary-rule | — | no | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 177 | `/reference/reference-semantics/semantics/builtins.k:253-253` | ordinary-rule | — | no | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 178 | `/reference/reference-semantics/semantics/builtins.k:254-254` | ordinary-rule | — | no | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 179 | `/reference/reference-semantics/semantics/builtins.k:255-255` | syntax-declaration | function, total | no | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 180 | `/reference/reference-semantics/semantics/builtins.k:256-256` | ordinary-rule | — | no | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 181 | `/reference/reference-semantics/semantics/builtins.k:257-259` | ordinary-rule | — | no | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| 182 | `/reference/reference-semantics/semantics/builtins.k:260-262` | ordinary-rule | — | no | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| 183 | `/reference/reference-semantics/semantics/builtins.k:263-264` | ordinary-rule | owise | no | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| 184 | `/reference/reference-semantics/semantics/builtins.k:265-265` | syntax-declaration | function, total | no | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 185 | `/reference/reference-semantics/semantics/builtins.k:266-266` | ordinary-rule | — | no | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 186 | `/reference/reference-semantics/semantics/builtins.k:267-267` | ordinary-rule | — | no | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 187 | `/reference/reference-semantics/semantics/builtins.k:268-268` | ordinary-rule | owise | no | `rule inLevelE(_:String, _:String) => false [owise]` |
| 188 | `/reference/reference-semantics/semantics/builtins.k:269-269` | syntax-declaration | function, total | no | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 189 | `/reference/reference-semantics/semantics/builtins.k:270-270` | ordinary-rule | — | no | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 190 | `/reference/reference-semantics/semantics/builtins.k:271-271` | ordinary-rule | — | no | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 191 | `/reference/reference-semantics/semantics/builtins.k:272-272` | syntax-declaration | function, total | no | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 192 | `/reference/reference-semantics/semantics/builtins.k:273-273` | ordinary-rule | — | no | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 193 | `/reference/reference-semantics/semantics/builtins.k:274-274` | ordinary-rule | — | no | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| 194 | `/reference/reference-semantics/semantics/builtins.k:279-279` | syntax-declaration | — | no | `syntax KItem ::= "#md5"` |
| 195 | `/reference/reference-semantics/semantics/builtins.k:280-281` | priority-rule | priority | no | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| 196 | `/reference/reference-semantics/semantics/builtins.k:282-282` | ordinary-rule | — | no | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 197 | `/reference/reference-semantics/semantics/builtins.k:283-283` | syntax-declaration | — | no | `syntax Val ::= md5Obj(IntSeq)` |
| 198 | `/reference/reference-semantics/semantics/builtins.k:284-284` | ordinary-rule | — | no | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 199 | `/reference/reference-semantics/semantics/builtins.k:285-285` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| 200 | `/reference/reference-semantics/semantics/builtins.k:291-291` | ordinary-rule | — | no | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 201 | `/reference/reference-semantics/semantics/builtins.k:292-292` | ordinary-rule | — | no | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 202 | `/reference/reference-semantics/semantics/builtins.k:293-293` | syntax-declaration | function | no | `syntax Bool ::= isIntV(Val) [function] &#124; isStrV(Val) [function]` |
| 203 | `/reference/reference-semantics/semantics/builtins.k:294-294` | ordinary-rule | — | no | `rule isIntV(_:Int) => true` |
| 204 | `/reference/reference-semantics/semantics/builtins.k:295-295` | ordinary-rule | owise | no | `rule isIntV(_:Val) => false [owise]` |
| 205 | `/reference/reference-semantics/semantics/builtins.k:296-296` | ordinary-rule | — | no | `rule isStrV(str(_:IntSeq)) => true` |
| 206 | `/reference/reference-semantics/semantics/builtins.k:297-297` | ordinary-rule | owise | no | `rule isStrV(_:Val) => false [owise]` |
| 207 | `/reference/reference-semantics/semantics/call.k:16-16` | ordinary-rule | — | no | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| 208 | `/reference/reference-semantics/semantics/call.k:19-19` | syntax-declaration | — | no | `syntax KItem ::= #callee(Exprs)` |
| 209 | `/reference/reference-semantics/semantics/call.k:20-20` | ordinary-rule | owise | no | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 210 | `/reference/reference-semantics/semantics/call.k:21-21` | ordinary-rule | — | no | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| 211 | `/reference/reference-semantics/semantics/call.k:24-24` | ordinary-rule | — | no | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 212 | `/reference/reference-semantics/semantics/call.k:26-26` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 213 | `/reference/reference-semantics/semantics/call.k:27-27` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>` |
| 214 | `/reference/reference-semantics/semantics/call.k:28-28` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>` |
| 215 | `/reference/reference-semantics/semantics/call.k:29-29` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>` |
| 216 | `/reference/reference-semantics/semantics/call.k:30-30` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>` |
| 217 | `/reference/reference-semantics/semantics/call.k:31-31` | ordinary-rule | owise | no | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 218 | `/reference/reference-semantics/semantics/call.k:32-32` | ordinary-rule | — | no | `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k>` |
| 219 | `/reference/reference-semantics/semantics/call.k:38-41` | priority-rule | priority | no | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 220 | `/reference/reference-semantics/semantics/call.k:42-46` | priority-rule | priority | no | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| 221 | `/reference/reference-semantics/semantics/call.k:47-50` | priority-rule | priority | no | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 222 | `/reference/reference-semantics/semantics/call.k:52-52` | syntax-declaration | function, total | no | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 223 | `/reference/reference-semantics/semantics/call.k:53-55` | ordinary-rule | — | no | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| 224 | `/reference/reference-semantics/semantics/call.k:56-60` | priority-rule | priority | no | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` |
| 225 | `/reference/reference-semantics/semantics/call.k:63-67` | priority-rule | priority | no | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| 226 | `/reference/reference-semantics/semantics/call.k:69-74` | ordinary-rule | — | no | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| 227 | `/reference/reference-semantics/semantics/call.k:80-85` | ordinary-rule | — | no | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </st...` |
| 228 | `/reference/reference-semantics/semantics/call.k:87-87` | syntax-declaration | — | no | `syntax KItem ::= #allocCells(ParamNames)` |
| 229 | `/reference/reference-semantics/semantics/call.k:88-88` | ordinary-rule | — | no | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 230 | `/reference/reference-semantics/semantics/call.k:89-94` | ordinary-rule | — | no | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N &#124;-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 231 | `/reference/reference-semantics/semantics/comprehension.k:11-11` | ordinary-rule | — | no | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 232 | `/reference/reference-semantics/semantics/comprehension.k:12-12` | ordinary-rule | — | no | `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 233 | `/reference/reference-semantics/semantics/comprehension.k:14-14` | syntax-declaration | macro | no | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 234 | `/reference/reference-semantics/semantics/comprehension.k:15-16` | ordinary-rule | — | no | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| 235 | `/reference/reference-semantics/semantics/comprehension.k:18-18` | syntax-declaration | macro, macro-rec | no | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 236 | `/reference/reference-semantics/semantics/comprehension.k:19-20` | ordinary-rule | — | no | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| 237 | `/reference/reference-semantics/semantics/comprehension.k:21-22` | ordinary-rule | — | no | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| 238 | `/reference/reference-semantics/semantics/comprehension.k:24-24` | syntax-declaration | macro | no | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 239 | `/reference/reference-semantics/semantics/comprehension.k:25-25` | ordinary-rule | — | no | `rule compGuard(.Exprs) => Bool(true)` |
| 240 | `/reference/reference-semantics/semantics/comprehension.k:26-26` | ordinary-rule | — | no | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| 241 | `/reference/reference-semantics/semantics/concrete.k:13-15` | ordinary-rule | — | no | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 242 | `/reference/reference-semantics/semantics/concrete.k:16-18` | ordinary-rule | — | no | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 243 | `/reference/reference-semantics/semantics/concrete.k:25-25` | syntax-declaration | — | no | `syntax Val ::= kvP(Val, Val)` |
| 244 | `/reference/reference-semantics/semantics/concrete.k:26-27` | syntax-declaration | — | no | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) &#124; #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| 245 | `/reference/reference-semantics/semantics/concrete.k:28-30` | priority-rule | priority | no | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| 246 | `/reference/reference-semantics/semantics/concrete.k:31-33` | priority-rule | priority | no | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| 247 | `/reference/reference-semantics/semantics/concrete.k:34-35` | ordinary-rule | — | no | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| 248 | `/reference/reference-semantics/semantics/concrete.k:36-37` | ordinary-rule | — | no | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| 249 | `/reference/reference-semantics/semantics/concrete.k:38-40` | ordinary-rule | — | no | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| 250 | `/reference/reference-semantics/semantics/concrete.k:42-42` | syntax-declaration | function | no | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 251 | `/reference/reference-semantics/semantics/concrete.k:43-43` | ordinary-rule | — | no | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 252 | `/reference/reference-semantics/semantics/concrete.k:44-46` | ordinary-rule | — | no | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| 253 | `/reference/reference-semantics/semantics/concrete.k:47-49` | ordinary-rule | — | no | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| 254 | `/reference/reference-semantics/semantics/concrete.k:51-51` | syntax-declaration | function | no | `syntax Bool ::= kLt(Val, Val) [function]` |
| 255 | `/reference/reference-semantics/semantics/concrete.k:52-52` | ordinary-rule | — | no | `rule kLt(I1:Int, I2:Int) => I1 <Int I2` |
| 256 | `/reference/reference-semantics/semantics/concrete.k:53-53` | ordinary-rule | — | no | `rule kLt(F1:Float, F2:Float) => F1 <Float F2` |
| 257 | `/reference/reference-semantics/semantics/concrete.k:54-54` | ordinary-rule | — | no | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 258 | `/reference/reference-semantics/semantics/concrete.k:56-56` | syntax-declaration | function, total | no | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 259 | `/reference/reference-semantics/semantics/concrete.k:57-57` | ordinary-rule | — | no | `rule unpairVS(.ValSeq) => .ValSeq` |
| 260 | `/reference/reference-semantics/semantics/concrete.k:58-58` | ordinary-rule | — | no | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 261 | `/reference/reference-semantics/semantics/concrete.k:59-59` | ordinary-rule | owise | no | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| 262 | `/reference/reference-semantics/semantics/controls.k:9-11` | ordinary-rule | — | no | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 263 | `/reference/reference-semantics/semantics/controls.k:12-18` | priority-rule | priority | no | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 264 | `/reference/reference-semantics/semantics/controls.k:20-23` | ordinary-rule | — | no | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` |
| 265 | `/reference/reference-semantics/semantics/controls.k:27-31` | priority-rule | priority | no | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]` |
| 266 | `/reference/reference-semantics/semantics/controls.k:35-35` | ordinary-rule | — | no | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 267 | `/reference/reference-semantics/semantics/controls.k:36-36` | ordinary-rule | owise | no | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 268 | `/reference/reference-semantics/semantics/controls.k:37-37` | syntax-declaration | — | no | `syntax KItem ::= #bindImports(ParamNames)` |
| 269 | `/reference/reference-semantics/semantics/controls.k:38-38` | ordinary-rule | — | no | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 270 | `/reference/reference-semantics/semantics/controls.k:39-42` | ordinary-rule | — | no | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| 271 | `/reference/reference-semantics/semantics/controls.k:43-44` | ordinary-rule | — | no | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` |
| 272 | `/reference/reference-semantics/semantics/controls.k:48-48` | ordinary-rule | — | no | `rule <k> Expr(_:Val) => .K ... </k>` |
| 273 | `/reference/reference-semantics/semantics/controls.k:51-51` | syntax-declaration | — | no | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 274 | `/reference/reference-semantics/semantics/controls.k:52-52` | ordinary-rule | — | no | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 275 | `/reference/reference-semantics/semantics/controls.k:53-53` | ordinary-rule | — | no | `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>` |
| 276 | `/reference/reference-semantics/semantics/controls.k:54-54` | ordinary-rule | — | no | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| 277 | `/reference/reference-semantics/semantics/controls.k:57-58` | ordinary-rule | — | no | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| 278 | `/reference/reference-semantics/semantics/controls.k:59-60` | ordinary-rule | — | no | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` |
| 279 | `/reference/reference-semantics/semantics/controls.k:65-67` | syntax-declaration | — | no | `syntax KItem ::= #loop(Val, Expr, Stmts) &#124; #loopStep(Expr, Stmts) &#124; #while(Expr, Stmts) &#124; #whileCond(Expr, Stmts) &#124; #loopLbl(K) &#124; "#cont" &#124; "#brk"` |
| 280 | `/reference/reference-semantics/semantics/controls.k:69-69` | ordinary-rule | — | no | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 281 | `/reference/reference-semantics/semantics/controls.k:71-71` | ordinary-rule | — | no | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 282 | `/reference/reference-semantics/semantics/controls.k:72-72` | ordinary-rule | — | no | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 283 | `/reference/reference-semantics/semantics/controls.k:73-74` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` |
| 284 | `/reference/reference-semantics/semantics/controls.k:77-77` | ordinary-rule | — | no | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 285 | `/reference/reference-semantics/semantics/controls.k:78-78` | ordinary-rule | — | no | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 286 | `/reference/reference-semantics/semantics/controls.k:79-80` | ordinary-rule | — | no | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| 287 | `/reference/reference-semantics/semantics/controls.k:81-82` | ordinary-rule | — | no | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` |
| 288 | `/reference/reference-semantics/semantics/controls.k:85-85` | ordinary-rule | — | no | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 289 | `/reference/reference-semantics/semantics/controls.k:86-86` | ordinary-rule | — | no | `rule <k> Continue => #cont ... </k>` |
| 290 | `/reference/reference-semantics/semantics/controls.k:87-87` | ordinary-rule | — | no | `rule <k> Break => #brk ... </k>` |
| 291 | `/reference/reference-semantics/semantics/controls.k:88-88` | ordinary-rule | — | no | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 292 | `/reference/reference-semantics/semantics/controls.k:89-89` | ordinary-rule | owise | no | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 293 | `/reference/reference-semantics/semantics/controls.k:90-90` | ordinary-rule | — | no | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 294 | `/reference/reference-semantics/semantics/controls.k:91-91` | ordinary-rule | owise | no | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| 295 | `/reference/reference-semantics/semantics/controls.k:95-97` | priority-rule | priority | no | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 296 | `/reference/reference-semantics/semantics/controls.k:98-100` | priority-rule | priority | no | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 297 | `/reference/reference-semantics/semantics/controls.k:101-103` | priority-rule | priority | no | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 298 | `/reference/reference-semantics/semantics/controls.k:106-108` | priority-rule | priority | no | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 299 | `/reference/reference-semantics/semantics/core.k:13-13` | syntax-declaration | — | no | `syntax IntSeq ::= ".IntSeq" &#124; iCons(Int, IntSeq)` |
| 300 | `/reference/reference-semantics/semantics/core.k:14-14` | syntax-declaration | — | no | `syntax ValSeq ::= ".ValSeq" &#124; vCons(Val, ValSeq)` |
| 301 | `/reference/reference-semantics/semantics/core.k:15-15` | syntax-declaration | — | no | `syntax Str ::= str(IntSeq)` |
| 302 | `/reference/reference-semantics/semantics/core.k:18-23` | syntax-declaration | — | no | `syntax Iterable ::= list(ValSeq) &#124; tuple(ValSeq) &#124; Str &#124; rangeObj(Int, Int, Int) &#124; zipObj(ValSeq, ValSeq) &#124; zipObjS(IntSeq, IntSeq)` |
| 303 | `/reference/reference-semantics/semantics/core.k:25-34` | syntax-declaration | function | no | `syntax Val ::= Int &#124; Bool &#124; "noneV" &#124; Iterable &#124; ref(Int) // a heap object: <heap> holds its list(VS) &#124; cellRef(Int) // a closure cell: <heap> holds cellV(V) &#124; closureVal(ParamNames, Stmts, Int) &#124; typeV(String) // a type object (int/str), resolved from the builtins frame &#124; builtinV(String) // a builtin function, resolved like any name (LEGB fallthrough) &#124; boundMethodV(V...` |
| 304 | `/reference/reference-semantics/semantics/core.k:36-36` | syntax-declaration | — | no | `syntax Parent ::= "root" &#124; parent(Int)` |
| 305 | `/reference/reference-semantics/semantics/core.k:37-37` | syntax-declaration | — | no | `syntax Scope ::= scope(Map, Parent)` |
| 306 | `/reference/reference-semantics/semantics/core.k:38-38` | syntax-declaration | — | no | `syntax KResult ::= Val` |
| 307 | `/reference/reference-semantics/semantics/core.k:39-39` | syntax-declaration | — | no | `syntax Expr ::= Val // cooling puts results back into expression holes` |
| 308 | `/reference/reference-semantics/semantics/core.k:40-40` | syntax-declaration | — | no | `syntax Vals ::= List{Val, ","}` |
| 309 | `/reference/reference-semantics/semantics/core.k:41-41` | syntax-declaration | — | no | `syntax Exc ::= "NoExc" &#124; "AssertionError"` |
| 310 | `/reference/reference-semantics/semantics/core.k:42-42` | syntax-declaration | — | no | `syntax RetState ::= "noRet" &#124; retV(Val)` |
| 311 | `/reference/reference-semantics/semantics/core.k:49-60` | configuration | — | no | `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 &#124;-> scope(.Map, parent(-1)) -1 &#124;-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code>` |
| 312 | `/reference/reference-semantics/semantics/core.k:68-68` | syntax-declaration | function, total | no | `syntax Bool ::= isRefV(Val) [function, total]` |
| 313 | `/reference/reference-semantics/semantics/core.k:69-69` | ordinary-rule | — | no | `rule isRefV(ref(_:Int)) => true` |
| 314 | `/reference/reference-semantics/semantics/core.k:70-70` | ordinary-rule | owise | no | `rule isRefV(_:Val) => false [owise]` |
| 315 | `/reference/reference-semantics/semantics/core.k:75-75` | syntax-declaration | — | no | `syntax HeapVal ::= cellV(Val)` |
| 316 | `/reference/reference-semantics/semantics/core.k:76-76` | syntax-declaration | function, total | no | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 317 | `/reference/reference-semantics/semantics/core.k:77-77` | ordinary-rule | — | no | `rule isCellRef(cellRef(_:Int)) => true` |
| 318 | `/reference/reference-semantics/semantics/core.k:78-78` | ordinary-rule | owise | no | `rule isCellRef(_:Val) => false [owise]` |
| 319 | `/reference/reference-semantics/semantics/core.k:85-90` | priority-rule | priority | no | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> <heap> ... H &#124;-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` |
| 320 | `/reference/reference-semantics/semantics/core.k:95-95` | syntax-declaration | — | no | `syntax Val ::= kwV(String, Val)` |
| 321 | `/reference/reference-semantics/semantics/core.k:96-96` | syntax-declaration | — | no | `syntax KItem ::= #kwTag(String)` |
| 322 | `/reference/reference-semantics/semantics/core.k:97-97` | ordinary-rule | — | no | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 323 | `/reference/reference-semantics/semantics/core.k:98-99` | ordinary-rule | — | no | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| 324 | `/reference/reference-semantics/semantics/core.k:100-100` | syntax-declaration | function, total | no | `syntax Bool ::= isKwV(Val) [function, total]` |
| 325 | `/reference/reference-semantics/semantics/core.k:101-101` | ordinary-rule | — | no | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 326 | `/reference/reference-semantics/semantics/core.k:102-102` | ordinary-rule | owise | no | `rule isKwV(_:Val) => false [owise]` |
| 327 | `/reference/reference-semantics/semantics/core.k:106-106` | syntax-declaration | — | no | `syntax Val ::= cellsMark(ParamNames)` |
| 328 | `/reference/reference-semantics/semantics/core.k:107-107` | syntax-declaration | function | no | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 329 | `/reference/reference-semantics/semantics/core.k:108-108` | ordinary-rule | — | no | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 330 | `/reference/reference-semantics/semantics/core.k:109-109` | syntax-declaration | function, total | no | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 331 | `/reference/reference-semantics/semantics/core.k:110-110` | ordinary-rule | — | no | `rule pnMember(_:String, .ParamNames) => false` |
| 332 | `/reference/reference-semantics/semantics/core.k:111-111` | ordinary-rule | — | no | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 333 | `/reference/reference-semantics/semantics/core.k:113-113` | syntax-declaration | — | no | `syntax KItem ::= #cellW(Val, Val)` |
| 334 | `/reference/reference-semantics/semantics/core.k:114-115` | ordinary-rule | — | no | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H &#124;-> cellV(_:Val => V) ... </heap>` |
| 335 | `/reference/reference-semantics/semantics/core.k:117-117` | syntax-declaration | — | no | `syntax KItem ::= #alloc(Val)` |
| 336 | `/reference/reference-semantics/semantics/core.k:118-121` | ordinary-rule | — | no | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N &#124;-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 337 | `/reference/reference-semantics/semantics/core.k:124-124` | syntax-declaration | — | no | `syntax KItem ::= #loadAll(Module)` |
| 338 | `/reference/reference-semantics/semantics/core.k:125-125` | ordinary-rule | — | no | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 339 | `/reference/reference-semantics/semantics/core.k:126-126` | ordinary-rule | — | no | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 340 | `/reference/reference-semantics/semantics/core.k:127-127` | ordinary-rule | — | no | `rule <k> .Stmts => .K ... </k>` |
| 341 | `/reference/reference-semantics/semantics/core.k:130-130` | syntax-declaration | — | no | `syntax KItem ::= #look(String, Int)` |
| 342 | `/reference/reference-semantics/semantics/core.k:131-131` | ordinary-rule | — | no | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 343 | `/reference/reference-semantics/semantics/core.k:132-134` | ordinary-rule | — | no | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L &#124;-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` |
| 344 | `/reference/reference-semantics/semantics/core.k:145-151` | priority-rule | priority | no | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L &#124;-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H &#124;-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| 345 | `/reference/reference-semantics/semantics/core.k:152-154` | ordinary-rule | — | no | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L &#124;-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` |
| 346 | `/reference/reference-semantics/semantics/core.k:157-157` | syntax-declaration | function, total | no | `syntax Scope ::= "builtinsScope" [function, total]` |
| 347 | `/reference/reference-semantics/semantics/core.k:158-181` | ordinary-rule | — | no | `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isin...` |
| 348 | `/reference/reference-semantics/semantics/core.k:185-185` | syntax-declaration | — | no | `syntax ApplyK ::= toCall(Val)` |
| 349 | `/reference/reference-semantics/semantics/core.k:186-188` | syntax-declaration | — | no | `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) &#124; #evalArgCont(Exprs, Vals, ApplyK) &#124; #applyK(ApplyK, Vals)` |
| 350 | `/reference/reference-semantics/semantics/core.k:189-189` | ordinary-rule | — | no | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 351 | `/reference/reference-semantics/semantics/core.k:190-190` | ordinary-rule | — | no | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 352 | `/reference/reference-semantics/semantics/core.k:191-191` | ordinary-rule | — | no | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| 353 | `/reference/reference-semantics/semantics/core.k:194-194` | ordinary-rule | — | no | `rule <k> Int(I:Int) => I ... </k>` |
| 354 | `/reference/reference-semantics/semantics/core.k:195-195` | ordinary-rule | — | no | `rule <k> Bool(B:Bool) => B ... </k>` |
| 355 | `/reference/reference-semantics/semantics/core.k:196-196` | ordinary-rule | — | no | `rule <k> NoneVal => noneV ... </k>` |
| 356 | `/reference/reference-semantics/semantics/core.k:199-199` | syntax-declaration | function | no | `syntax Bool ::= truthy(Val) [function]` |
| 357 | `/reference/reference-semantics/semantics/core.k:200-200` | ordinary-rule | — | no | `rule truthy(B:Bool) => B` |
| 358 | `/reference/reference-semantics/semantics/core.k:201-201` | ordinary-rule | — | no | `rule truthy(noneV) => false` |
| 359 | `/reference/reference-semantics/semantics/core.k:202-202` | ordinary-rule | — | no | `rule truthy(I:Int) => I =/=Int 0` |
| 360 | `/reference/reference-semantics/semantics/core.k:203-203` | ordinary-rule | — | no | `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)` |
| 361 | `/reference/reference-semantics/semantics/core.k:204-204` | ordinary-rule | — | no | `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 362 | `/reference/reference-semantics/semantics/core.k:205-205` | ordinary-rule | — | no | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 363 | `/reference/reference-semantics/semantics/core.k:208-208` | syntax-declaration | function | no | `syntax Val ::= applyUn(String, Val) [function]` |
| 364 | `/reference/reference-semantics/semantics/core.k:209-209` | syntax-declaration | function | no | `syntax Val ::= applyBin(String, Val, Val) [function]` |
| 365 | `/reference/reference-semantics/semantics/core.k:210-210` | syntax-declaration | function | no | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| 366 | `/reference/reference-semantics/semantics/core.k:213-213` | syntax-declaration | function, total | no | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 367 | `/reference/reference-semantics/semantics/core.k:214-214` | ordinary-rule | — | no | `rule appendVal(.Vals, V:Val) => V , .Vals` |
| 368 | `/reference/reference-semantics/semantics/core.k:215-215` | ordinary-rule | — | no | `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)` |
| 369 | `/reference/reference-semantics/semantics/core.k:217-217` | syntax-declaration | function, total | no | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 370 | `/reference/reference-semantics/semantics/core.k:218-218` | ordinary-rule | — | no | `rule vals2valSeq(.Vals) => .ValSeq` |
| 371 | `/reference/reference-semantics/semantics/core.k:219-219` | ordinary-rule | — | no | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| 372 | `/reference/reference-semantics/semantics/core.k:223-223` | syntax-declaration | function, total | no | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 373 | `/reference/reference-semantics/semantics/core.k:224-224` | ordinary-rule | — | no | `rule vsLen(.ValSeq) => 0` |
| 374 | `/reference/reference-semantics/semantics/core.k:225-225` | ordinary-rule | — | no | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 375 | `/reference/reference-semantics/semantics/core.k:227-227` | syntax-declaration | function, total | no | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 376 | `/reference/reference-semantics/semantics/core.k:228-228` | ordinary-rule | — | no | `rule isLen(.IntSeq) => 0` |
| 377 | `/reference/reference-semantics/semantics/core.k:229-229` | ordinary-rule | — | no | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| 378 | `/reference/reference-semantics/semantics/core.k:233-233` | syntax-declaration | function, total | no | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 379 | `/reference/reference-semantics/semantics/core.k:234-234` | ordinary-rule | — | no | `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq` |
| 380 | `/reference/reference-semantics/semantics/core.k:235-235` | ordinary-rule | — | no | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)` |
| 381 | `/reference/reference-semantics/semantics/core.k:236-237` | ordinary-rule | — | no | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| 382 | `/reference/reference-semantics/semantics/core.k:238-239` | ordinary-rule | — | no | `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0` |
| 383 | `/reference/reference-semantics/semantics/dict.k:20-20` | syntax-declaration | — | no | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| 384 | `/reference/reference-semantics/semantics/dict.k:23-25` | syntax-declaration | — | no | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) &#124; #dictKey(Expr, Entries, ValSeq, ValSeq) &#124; #dictVal(Val, Entries, ValSeq, ValSeq)` |
| 385 | `/reference/reference-semantics/semantics/dict.k:26-26` | ordinary-rule | — | no | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 386 | `/reference/reference-semantics/semantics/dict.k:27-27` | ordinary-rule | — | no | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 387 | `/reference/reference-semantics/semantics/dict.k:28-29` | ordinary-rule | — | no | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| 388 | `/reference/reference-semantics/semantics/dict.k:30-31` | ordinary-rule | — | no | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| 389 | `/reference/reference-semantics/semantics/dict.k:32-33` | ordinary-rule | — | no | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` |
| 390 | `/reference/reference-semantics/semantics/dict.k:37-37` | syntax-declaration | function, total | no | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 391 | `/reference/reference-semantics/semantics/dict.k:38-38` | ordinary-rule | — | no | `rule dHasKey(.ValSeq, _:Val) => false` |
| 392 | `/reference/reference-semantics/semantics/dict.k:39-39` | ordinary-rule | — | no | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K` |
| 393 | `/reference/reference-semantics/semantics/dict.k:40-40` | ordinary-rule | — | no | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| 394 | `/reference/reference-semantics/semantics/dict.k:43-43` | syntax-declaration | function, total | no | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 395 | `/reference/reference-semantics/semantics/dict.k:44-44` | ordinary-rule | — | no | `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)` |
| 396 | `/reference/reference-semantics/semantics/dict.k:45-45` | ordinary-rule | — | no | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| 397 | `/reference/reference-semantics/semantics/dict.k:49-49` | syntax-declaration | function, total | no | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 398 | `/reference/reference-semantics/semantics/dict.k:50-51` | ordinary-rule | — | no | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K` |
| 399 | `/reference/reference-semantics/semantics/dict.k:52-53` | ordinary-rule | — | no | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| 400 | `/reference/reference-semantics/semantics/dict.k:54-54` | ordinary-rule | owise | no | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| 401 | `/reference/reference-semantics/semantics/dict.k:58-60` | priority-rule | priority | no | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` |
| 402 | `/reference/reference-semantics/semantics/dict.k:63-63` | ordinary-rule | — | no | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 403 | `/reference/reference-semantics/semantics/dict.k:64-64` | syntax-declaration | function | no | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 404 | `/reference/reference-semantics/semantics/dict.k:65-66` | priority-rule | priority | no | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` |
| 405 | `/reference/reference-semantics/semantics/dict.k:70-70` | syntax-declaration | function | no | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 406 | `/reference/reference-semantics/semantics/dict.k:71-71` | ordinary-rule | — | no | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| 407 | `/reference/reference-semantics/semantics/dict.k:76-76` | syntax-declaration | — | no | `syntax KItem ::= #dsetK(String, Val)` |
| 408 | `/reference/reference-semantics/semantics/dict.k:77-77` | ordinary-rule | — | no | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 409 | `/reference/reference-semantics/semantics/dict.k:78-81` | ordinary-rule | — | no | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| 410 | `/reference/reference-semantics/semantics/dict.k:82-85` | ordinary-rule | — | no | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| 411 | `/reference/reference-semantics/semantics/dict.k:86-86` | syntax-declaration | — | no | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 412 | `/reference/reference-semantics/semantics/dict.k:87-88` | ordinary-rule | — | no | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H &#124;-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` |
| 413 | `/reference/reference-semantics/semantics/dict.k:90-90` | syntax-declaration | function, total | no | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 414 | `/reference/reference-semantics/semantics/dict.k:91-91` | ordinary-rule | — | no | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 415 | `/reference/reference-semantics/semantics/dict.k:92-92` | ordinary-rule | — | no | `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0` |
| 416 | `/reference/reference-semantics/semantics/dict.k:95-96` | ordinary-rule | — | no | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| 417 | `/reference/reference-semantics/semantics/dict.k:97-97` | syntax-declaration | function | no | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 418 | `/reference/reference-semantics/semantics/dict.k:98-98` | ordinary-rule | — | no | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 419 | `/reference/reference-semantics/semantics/dict.k:99-100` | ordinary-rule | — | no | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| 420 | `/reference/reference-semantics/semantics/dict.k:101-101` | syntax-declaration | function | no | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 421 | `/reference/reference-semantics/semantics/dict.k:102-102` | ordinary-rule | — | no | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K` |
| 422 | `/reference/reference-semantics/semantics/dict.k:103-103` | ordinary-rule | — | no | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| 423 | `/reference/reference-semantics/semantics/float.k:20-20` | syntax-declaration | — | no | `syntax Val ::= Float` |
| 424 | `/reference/reference-semantics/semantics/float.k:21-21` | ordinary-rule | — | no | `rule <k> Float(F:Float) => F ... </k>` |
| 425 | `/reference/reference-semantics/semantics/float.k:24-24` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 426 | `/reference/reference-semantics/semantics/float.k:25-25` | ordinary-rule | concrete | no | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 427 | `/reference/reference-semantics/semantics/float.k:27-27` | ordinary-rule | — | no | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| 428 | `/reference/reference-semantics/semantics/float.k:30-30` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 429 | `/reference/reference-semantics/semantics/float.k:31-31` | ordinary-rule | concrete | no | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 430 | `/reference/reference-semantics/semantics/float.k:32-32` | ordinary-rule | — | no | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| 431 | `/reference/reference-semantics/semantics/float.k:37-37` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 432 | `/reference/reference-semantics/semantics/float.k:38-38` | ordinary-rule | concrete | no | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 433 | `/reference/reference-semantics/semantics/float.k:39-39` | ordinary-rule | — | no | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| 434 | `/reference/reference-semantics/semantics/float.k:43-43` | ordinary-rule | — | no | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 435 | `/reference/reference-semantics/semantics/float.k:44-44` | ordinary-rule | — | no | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| 436 | `/reference/reference-semantics/semantics/float.k:50-50` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 437 | `/reference/reference-semantics/semantics/float.k:51-51` | ordinary-rule | concrete | no | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 438 | `/reference/reference-semantics/semantics/float.k:52-52` | ordinary-rule | — | no | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 439 | `/reference/reference-semantics/semantics/float.k:54-54` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 440 | `/reference/reference-semantics/semantics/float.k:55-55` | ordinary-rule | concrete | no | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 441 | `/reference/reference-semantics/semantics/float.k:56-56` | ordinary-rule | — | no | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| 442 | `/reference/reference-semantics/semantics/float.k:61-61` | ordinary-rule | — | no | `rule <k> Import(_:String) => .K ... </k>` |
| 443 | `/reference/reference-semantics/semantics/float.k:65-65` | syntax-declaration | — | no | `syntax KItem ::= "#mathCeil"` |
| 444 | `/reference/reference-semantics/semantics/float.k:66-66` | priority-rule | priority | no | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 445 | `/reference/reference-semantics/semantics/float.k:67-67` | ordinary-rule | — | no | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| 446 | `/reference/reference-semantics/semantics/float.k:70-70` | syntax-declaration | — | no | `syntax KItem ::= "#mathFloor"` |
| 447 | `/reference/reference-semantics/semantics/float.k:71-71` | priority-rule | priority | no | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 448 | `/reference/reference-semantics/semantics/float.k:72-72` | ordinary-rule | — | no | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 449 | `/reference/reference-semantics/semantics/float.k:73-73` | syntax-declaration | function, symbol, total | no | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 450 | `/reference/reference-semantics/semantics/float.k:74-74` | ordinary-rule | concrete | no | `rule floorFI(I:Int) => I [concrete]` |
| 451 | `/reference/reference-semantics/semantics/float.k:75-75` | ordinary-rule | concrete | no | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| 452 | `/reference/reference-semantics/semantics/float.k:78-78` | ordinary-rule | — | no | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 453 | `/reference/reference-semantics/semantics/float.k:79-79` | ordinary-rule | — | no | `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V)` |
| 454 | `/reference/reference-semantics/semantics/float.k:82-82` | syntax-declaration | — | no | `syntax KItem ::= #mathPow1(Expr) &#124; #mathPow2(Val)` |
| 455 | `/reference/reference-semantics/semantics/float.k:83-83` | priority-rule | priority | no | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 456 | `/reference/reference-semantics/semantics/float.k:84-84` | ordinary-rule | — | no | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 457 | `/reference/reference-semantics/semantics/float.k:85-85` | ordinary-rule | — | no | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 458 | `/reference/reference-semantics/semantics/float.k:86-86` | syntax-declaration | function, symbol, total | no | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 459 | `/reference/reference-semantics/semantics/float.k:87-87` | ordinary-rule | concrete | no | `rule toF(F:Float) => F [concrete]` |
| 460 | `/reference/reference-semantics/semantics/float.k:88-88` | ordinary-rule | concrete | no | `rule toF(I:Int) => intToF(I) [concrete]` |
| 461 | `/reference/reference-semantics/semantics/float.k:93-93` | syntax-declaration | function, symbol, total | no | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 462 | `/reference/reference-semantics/semantics/float.k:94-94` | ordinary-rule | concrete | no | `rule ceilF(I:Int) => I [concrete]` |
| 463 | `/reference/reference-semantics/semantics/float.k:95-95` | ordinary-rule | concrete | no | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| 464 | `/reference/reference-semantics/semantics/float.k:99-99` | ordinary-rule | — | no | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| 465 | `/reference/reference-semantics/semantics/float.k:103-103` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 466 | `/reference/reference-semantics/semantics/float.k:104-104` | ordinary-rule | concrete | no | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 467 | `/reference/reference-semantics/semantics/float.k:105-105` | ordinary-rule | — | no | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 468 | `/reference/reference-semantics/semantics/float.k:107-107` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 469 | `/reference/reference-semantics/semantics/float.k:108-108` | ordinary-rule | concrete | no | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 470 | `/reference/reference-semantics/semantics/float.k:109-109` | ordinary-rule | — | no | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 471 | `/reference/reference-semantics/semantics/float.k:111-111` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 472 | `/reference/reference-semantics/semantics/float.k:112-112` | ordinary-rule | concrete | no | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 473 | `/reference/reference-semantics/semantics/float.k:113-113` | ordinary-rule | — | no | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 474 | `/reference/reference-semantics/semantics/float.k:115-115` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 475 | `/reference/reference-semantics/semantics/float.k:116-116` | ordinary-rule | concrete | no | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 476 | `/reference/reference-semantics/semantics/float.k:117-117` | ordinary-rule | — | no | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 477 | `/reference/reference-semantics/semantics/float.k:119-119` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 478 | `/reference/reference-semantics/semantics/float.k:120-120` | ordinary-rule | concrete | no | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 479 | `/reference/reference-semantics/semantics/float.k:121-121` | ordinary-rule | — | no | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| 480 | `/reference/reference-semantics/semantics/float.k:125-125` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 481 | `/reference/reference-semantics/semantics/float.k:126-126` | ordinary-rule | concrete | no | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 482 | `/reference/reference-semantics/semantics/float.k:127-127` | ordinary-rule | — | no | `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)` |
| 483 | `/reference/reference-semantics/semantics/float.k:128-128` | ordinary-rule | — | no | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 484 | `/reference/reference-semantics/semantics/float.k:129-129` | ordinary-rule | — | no | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| 485 | `/reference/reference-semantics/semantics/float.k:132-132` | ordinary-rule | — | no | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 486 | `/reference/reference-semantics/semantics/float.k:133-133` | ordinary-rule | — | no | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 487 | `/reference/reference-semantics/semantics/float.k:134-134` | ordinary-rule | — | no | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 488 | `/reference/reference-semantics/semantics/float.k:135-135` | ordinary-rule | — | no | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 489 | `/reference/reference-semantics/semantics/float.k:136-136` | ordinary-rule | — | no | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 490 | `/reference/reference-semantics/semantics/float.k:137-137` | ordinary-rule | — | no | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 491 | `/reference/reference-semantics/semantics/float.k:138-138` | ordinary-rule | — | no | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 492 | `/reference/reference-semantics/semantics/float.k:139-139` | ordinary-rule | — | no | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 493 | `/reference/reference-semantics/semantics/float.k:142-142` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 494 | `/reference/reference-semantics/semantics/float.k:143-143` | ordinary-rule | concrete | no | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 495 | `/reference/reference-semantics/semantics/float.k:144-144` | ordinary-rule | — | no | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 496 | `/reference/reference-semantics/semantics/float.k:145-145` | ordinary-rule | — | no | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 497 | `/reference/reference-semantics/semantics/float.k:146-146` | ordinary-rule | — | no | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 498 | `/reference/reference-semantics/semantics/float.k:147-147` | ordinary-rule | — | no | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 499 | `/reference/reference-semantics/semantics/float.k:148-148` | ordinary-rule | — | no | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 500 | `/reference/reference-semantics/semantics/float.k:149-149` | ordinary-rule | — | no | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 501 | `/reference/reference-semantics/semantics/float.k:150-150` | ordinary-rule | — | no | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 502 | `/reference/reference-semantics/semantics/float.k:151-151` | ordinary-rule | — | no | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| 503 | `/reference/reference-semantics/semantics/float.k:154-154` | ordinary-rule | — | no | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 504 | `/reference/reference-semantics/semantics/float.k:155-155` | ordinary-rule | — | no | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| 505 | `/reference/reference-semantics/semantics/float.k:160-160` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 506 | `/reference/reference-semantics/semantics/float.k:161-161` | ordinary-rule | concrete | no | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 507 | `/reference/reference-semantics/semantics/float.k:162-164` | ordinary-rule | concrete | no | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| 508 | `/reference/reference-semantics/semantics/float.k:165-165` | syntax-declaration | function | no | `syntax Int ::= headIS(IntSeq) [function]` |
| 509 | `/reference/reference-semantics/semantics/float.k:166-166` | ordinary-rule | — | no | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 510 | `/reference/reference-semantics/semantics/float.k:167-167` | syntax-declaration | function, total | no | `syntax Int ::= intPart(IntSeq) [function, total] &#124; intPartAcc(IntSeq, Int) [function, total]` |
| 511 | `/reference/reference-semantics/semantics/float.k:168-168` | ordinary-rule | — | no | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 512 | `/reference/reference-semantics/semantics/float.k:169-169` | ordinary-rule | — | no | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 513 | `/reference/reference-semantics/semantics/float.k:170-170` | ordinary-rule | — | no | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 514 | `/reference/reference-semantics/semantics/float.k:171-172` | ordinary-rule | — | no | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| 515 | `/reference/reference-semantics/semantics/float.k:173-173` | syntax-declaration | function, total | no | `syntax Int ::= fracPart(IntSeq) [function, total] &#124; fracAcc(IntSeq, Int) [function, total]` |
| 516 | `/reference/reference-semantics/semantics/float.k:174-174` | ordinary-rule | — | no | `rule fracPart(.IntSeq) => 0` |
| 517 | `/reference/reference-semantics/semantics/float.k:175-175` | ordinary-rule | — | no | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 518 | `/reference/reference-semantics/semantics/float.k:176-176` | ordinary-rule | — | no | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 519 | `/reference/reference-semantics/semantics/float.k:177-177` | ordinary-rule | — | no | `rule fracAcc(.IntSeq, A:Int) => A` |
| 520 | `/reference/reference-semantics/semantics/float.k:178-178` | ordinary-rule | — | no | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 521 | `/reference/reference-semantics/semantics/float.k:179-179` | syntax-declaration | function, total | no | `syntax Int ::= fracScale(IntSeq) [function, total] &#124; fscAcc(IntSeq, Int) [function, total]` |
| 522 | `/reference/reference-semantics/semantics/float.k:180-180` | ordinary-rule | — | no | `rule fracScale(.IntSeq) => 1` |
| 523 | `/reference/reference-semantics/semantics/float.k:181-181` | ordinary-rule | — | no | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 524 | `/reference/reference-semantics/semantics/float.k:182-182` | ordinary-rule | — | no | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 525 | `/reference/reference-semantics/semantics/float.k:183-183` | ordinary-rule | — | no | `rule fscAcc(.IntSeq, A:Int) => A` |
| 526 | `/reference/reference-semantics/semantics/float.k:184-184` | ordinary-rule | — | no | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 527 | `/reference/reference-semantics/semantics/float.k:185-185` | ordinary-rule | — | no | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 528 | `/reference/reference-semantics/semantics/float.k:186-186` | ordinary-rule | — | no | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 529 | `/reference/reference-semantics/semantics/float.k:187-187` | ordinary-rule | — | no | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| 530 | `/reference/reference-semantics/semantics/float.k:190-190` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 531 | `/reference/reference-semantics/semantics/float.k:191-191` | ordinary-rule | concrete | no | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 532 | `/reference/reference-semantics/semantics/float.k:192-192` | ordinary-rule | — | no | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| 533 | `/reference/reference-semantics/semantics/float.k:195-195` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 534 | `/reference/reference-semantics/semantics/float.k:196-196` | ordinary-rule | concrete | no | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 535 | `/reference/reference-semantics/semantics/float.k:197-197` | ordinary-rule | — | no | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 536 | `/reference/reference-semantics/semantics/float.k:198-198` | ordinary-rule | — | no | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 537 | `/reference/reference-semantics/semantics/float.k:199-199` | ordinary-rule | — | no | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 538 | `/reference/reference-semantics/semantics/float.k:200-200` | ordinary-rule | — | no | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 539 | `/reference/reference-semantics/semantics/float.k:201-201` | ordinary-rule | — | no | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 540 | `/reference/reference-semantics/semantics/float.k:202-202` | ordinary-rule | — | no | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 541 | `/reference/reference-semantics/semantics/float.k:203-203` | ordinary-rule | — | no | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 542 | `/reference/reference-semantics/semantics/float.k:204-204` | ordinary-rule | — | no | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 543 | `/reference/reference-semantics/semantics/float.k:205-205` | ordinary-rule | — | no | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 544 | `/reference/reference-semantics/semantics/float.k:206-206` | ordinary-rule | — | no | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| 545 | `/reference/reference-semantics/semantics/float.k:209-209` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 546 | `/reference/reference-semantics/semantics/float.k:210-210` | ordinary-rule | concrete | no | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 547 | `/reference/reference-semantics/semantics/float.k:211-211` | ordinary-rule | — | no | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 548 | `/reference/reference-semantics/semantics/float.k:213-213` | ordinary-rule | — | no | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 549 | `/reference/reference-semantics/semantics/float.k:214-214` | ordinary-rule | — | no | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| 550 | `/reference/reference-semantics/semantics/float.k:217-217` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 551 | `/reference/reference-semantics/semantics/float.k:218-222` | ordinary-rule | concrete | no | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| 552 | `/reference/reference-semantics/semantics/float.k:223-223` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 553 | `/reference/reference-semantics/semantics/float.k:224-226` | ordinary-rule | concrete | no | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| 554 | `/reference/reference-semantics/semantics/float.k:227-227` | ordinary-rule | — | no | `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)` |
| 555 | `/reference/reference-semantics/semantics/float.k:228-228` | ordinary-rule | — | no | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 556 | `/reference/reference-semantics/semantics/float.k:230-230` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 557 | `/reference/reference-semantics/semantics/float.k:231-231` | ordinary-rule | concrete | no | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 558 | `/reference/reference-semantics/semantics/float.k:232-232` | syntax-declaration | — | no | `syntax KItem ::= "#mathSqrt"` |
| 559 | `/reference/reference-semantics/semantics/float.k:233-233` | priority-rule | priority | no | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 560 | `/reference/reference-semantics/semantics/float.k:234-234` | ordinary-rule | — | no | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 561 | `/reference/reference-semantics/semantics/float.k:235-235` | ordinary-rule | — | no | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| 562 | `/reference/reference-semantics/semantics/float.k:243-243` | syntax-declaration | — | no | `syntax KItem ::= #maxAccF(Iterable, Float) &#124; #maxContF(Float)` |
| 563 | `/reference/reference-semantics/semantics/float.k:244-244` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 564 | `/reference/reference-semantics/semantics/float.k:245-245` | ordinary-rule | — | no | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 565 | `/reference/reference-semantics/semantics/float.k:246-246` | ordinary-rule | — | no | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 566 | `/reference/reference-semantics/semantics/float.k:247-248` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 567 | `/reference/reference-semantics/semantics/float.k:250-250` | syntax-declaration | — | no | `syntax KItem ::= #minAccF(Iterable, Float) &#124; #minContF(Float)` |
| 568 | `/reference/reference-semantics/semantics/float.k:251-251` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 569 | `/reference/reference-semantics/semantics/float.k:252-252` | ordinary-rule | — | no | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 570 | `/reference/reference-semantics/semantics/float.k:253-253` | ordinary-rule | — | no | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 571 | `/reference/reference-semantics/semantics/float.k:254-255` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 572 | `/reference/reference-semantics/semantics/float.k:261-261` | syntax-declaration | — | no | `syntax KItem ::= #sumAccF(Iterable, Float) &#124; #sumContF(Float)` |
| 573 | `/reference/reference-semantics/semantics/float.k:262-264` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| 574 | `/reference/reference-semantics/semantics/float.k:265-265` | ordinary-rule | — | no | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 575 | `/reference/reference-semantics/semantics/float.k:266-266` | ordinary-rule | — | no | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 576 | `/reference/reference-semantics/semantics/float.k:267-269` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| 577 | `/reference/reference-semantics/semantics/float.k:270-272` | ordinary-rule | — | no | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| 578 | `/reference/reference-semantics/semantics/functions.k:8-11` | syntax-declaration | — | no | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) &#124; #bindP(ParamNames, Vals) &#124; "#pop" &#124; "#endcall"` |
| 579 | `/reference/reference-semantics/semantics/functions.k:14-16` | ordinary-rule | — | no | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| 580 | `/reference/reference-semantics/semantics/functions.k:18-18` | syntax-declaration | — | no | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 581 | `/reference/reference-semantics/semantics/functions.k:19-20` | ordinary-rule | — | no | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` |
| 582 | `/reference/reference-semantics/semantics/functions.k:27-27` | syntax-declaration | — | no | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| 583 | `/reference/reference-semantics/semantics/functions.k:31-32` | syntax-declaration | — | no | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) &#124; #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 584 | `/reference/reference-semantics/semantics/functions.k:33-35` | ordinary-rule | — | no | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| 585 | `/reference/reference-semantics/semantics/functions.k:36-41` | ordinary-rule | — | no | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 586 | `/reference/reference-semantics/semantics/functions.k:42-45` | ordinary-rule | — | no | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| 587 | `/reference/reference-semantics/semantics/functions.k:47-49` | ordinary-rule | — | no | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| 588 | `/reference/reference-semantics/semantics/functions.k:50-52` | ordinary-rule | — | no | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| 589 | `/reference/reference-semantics/semantics/functions.k:53-58` | ordinary-rule | — | no | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 590 | `/reference/reference-semantics/semantics/functions.k:59-60` | ordinary-rule | — | no | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` |
| 591 | `/reference/reference-semantics/semantics/functions.k:63-63` | ordinary-rule | — | no | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 592 | `/reference/reference-semantics/semantics/functions.k:64-66` | ordinary-rule | — | no | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ P <- V ], _) ... </scopes>` |
| 593 | `/reference/reference-semantics/semantics/functions.k:68-75` | priority-rule | priority | no | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]` |
| 594 | `/reference/reference-semantics/semantics/functions.k:78-79` | ordinary-rule | — | no | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| 595 | `/reference/reference-semantics/semantics/functions.k:80-81` | ordinary-rule | — | no | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` |
| 596 | `/reference/reference-semantics/semantics/functions.k:85-90` | ordinary-rule | — | no | `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |
| 597 | `/reference/reference-semantics/semantics/int.k:7-7` | ordinary-rule | — | no | `rule applyUn("-", I:Int) => 0 -Int I` |
| 598 | `/reference/reference-semantics/semantics/int.k:9-9` | ordinary-rule | — | no | `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2` |
| 599 | `/reference/reference-semantics/semantics/int.k:11-11` | ordinary-rule | — | no | `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 600 | `/reference/reference-semantics/semantics/int.k:12-12` | ordinary-rule | — | no | `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 601 | `/reference/reference-semantics/semantics/int.k:13-13` | ordinary-rule | — | no | `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2` |
| 602 | `/reference/reference-semantics/semantics/int.k:14-14` | ordinary-rule | — | no | `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2` |
| 603 | `/reference/reference-semantics/semantics/int.k:15-15` | ordinary-rule | — | no | `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)` |
| 604 | `/reference/reference-semantics/semantics/int.k:16-16` | ordinary-rule | — | no | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 605 | `/reference/reference-semantics/semantics/int.k:17-17` | ordinary-rule | — | no | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 606 | `/reference/reference-semantics/semantics/int.k:19-19` | syntax-declaration | function | no | `syntax Int ::= pyMod(Int, Int) [function]` |
| 607 | `/reference/reference-semantics/semantics/int.k:20-20` | ordinary-rule | — | no | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 608 | `/reference/reference-semantics/semantics/int.k:22-22` | ordinary-rule | — | no | `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` |
| 609 | `/reference/reference-semantics/semantics/int.k:23-23` | ordinary-rule | — | no | `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2` |
| 610 | `/reference/reference-semantics/semantics/int.k:24-24` | ordinary-rule | — | no | `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` |
| 611 | `/reference/reference-semantics/semantics/int.k:25-25` | ordinary-rule | — | no | `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2` |
| 612 | `/reference/reference-semantics/semantics/int.k:26-26` | ordinary-rule | — | no | `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2` |
| 613 | `/reference/reference-semantics/semantics/int.k:27-27` | ordinary-rule | — | no | `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2` |
| 614 | `/reference/reference-semantics/semantics/iter.k:8-8` | syntax-declaration | — | no | `syntax KItem ::= #iterNext(Iterable) &#124; "#iterDone" &#124; #iterYield(Val, Iterable)` |
| 615 | `/reference/reference-semantics/semantics/list.k:9-9` | ordinary-rule | — | no | `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>` |
| 616 | `/reference/reference-semantics/semantics/list.k:10-10` | ordinary-rule | — | no | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| 617 | `/reference/reference-semantics/semantics/list.k:13-13` | syntax-declaration | — | no | `syntax ApplyK ::= "toList"` |
| 618 | `/reference/reference-semantics/semantics/list.k:14-14` | ordinary-rule | — | no | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 619 | `/reference/reference-semantics/semantics/list.k:15-15` | ordinary-rule | — | no | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| 620 | `/reference/reference-semantics/semantics/list.k:18-18` | syntax-declaration | function, total | no | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 621 | `/reference/reference-semantics/semantics/list.k:19-19` | ordinary-rule | — | no | `rule valSeqConcat(.ValSeq, T:ValSeq) => T` |
| 622 | `/reference/reference-semantics/semantics/list.k:20-20` | ordinary-rule | — | no | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| 623 | `/reference/reference-semantics/semantics/list.k:24-25` | priority-rule | priority | no | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| 624 | `/reference/reference-semantics/semantics/list.k:27-27` | ordinary-rule | — | no | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 625 | `/reference/reference-semantics/semantics/list.k:28-28` | ordinary-rule | — | no | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| 626 | `/reference/reference-semantics/semantics/list.k:33-33` | syntax-declaration | function, total | no | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 627 | `/reference/reference-semantics/semantics/list.k:34-34` | ordinary-rule | — | no | `rule hasRefVS(.ValSeq) => false` |
| 628 | `/reference/reference-semantics/semantics/list.k:35-35` | ordinary-rule | — | no | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 629 | `/reference/reference-semantics/semantics/list.k:37-38` | syntax-declaration | function | no | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] &#124; deepEqV(Val, Val, Map) [function]` |
| 630 | `/reference/reference-semantics/semantics/list.k:39-39` | ordinary-rule | — | no | `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true` |
| 631 | `/reference/reference-semantics/semantics/list.k:40-40` | ordinary-rule | — | no | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false` |
| 632 | `/reference/reference-semantics/semantics/list.k:41-41` | ordinary-rule | — | no | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false` |
| 633 | `/reference/reference-semantics/semantics/list.k:42-43` | ordinary-rule | — | no | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| 634 | `/reference/reference-semantics/semantics/list.k:45-46` | ordinary-rule | — | no | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| 635 | `/reference/reference-semantics/semantics/list.k:47-48` | ordinary-rule | — | no | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| 636 | `/reference/reference-semantics/semantics/list.k:49-49` | ordinary-rule | — | no | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 637 | `/reference/reference-semantics/semantics/list.k:50-50` | ordinary-rule | owise | no | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| 638 | `/reference/reference-semantics/semantics/list.k:53-55` | priority-rule | priority | no | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H &#124;-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` |
| 639 | `/reference/reference-semantics/semantics/list.k:58-58` | syntax-declaration | — | no | `syntax KItem ::= #memberAcc(Val, Iterable) &#124; #memberCont(Val) &#124; "#notB"` |
| 640 | `/reference/reference-semantics/semantics/list.k:59-59` | ordinary-rule | — | no | `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 641 | `/reference/reference-semantics/semantics/list.k:60-60` | ordinary-rule | — | no | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 642 | `/reference/reference-semantics/semantics/list.k:61-61` | ordinary-rule | — | no | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 643 | `/reference/reference-semantics/semantics/list.k:62-62` | ordinary-rule | — | no | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 644 | `/reference/reference-semantics/semantics/list.k:63-64` | ordinary-rule | — | no | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| 645 | `/reference/reference-semantics/semantics/list.k:65-66` | ordinary-rule | — | no | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| 646 | `/reference/reference-semantics/semantics/list.k:67-67` | ordinary-rule | — | no | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| 647 | `/reference/reference-semantics/semantics/methods.k:10-10` | syntax-declaration | function | no | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| 648 | `/reference/reference-semantics/semantics/methods.k:13-13` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 649 | `/reference/reference-semantics/semantics/methods.k:14-14` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 650 | `/reference/reference-semantics/semantics/methods.k:15-15` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 651 | `/reference/reference-semantics/semantics/methods.k:16-16` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| 652 | `/reference/reference-semantics/semantics/methods.k:19-19` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))` |
| 653 | `/reference/reference-semantics/semantics/methods.k:20-20` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))` |
| 654 | `/reference/reference-semantics/semantics/methods.k:21-21` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| 655 | `/reference/reference-semantics/semantics/methods.k:26-26` | ordinary-rule | — | no | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 656 | `/reference/reference-semantics/semantics/methods.k:27-27` | syntax-declaration | function, total | no | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 657 | `/reference/reference-semantics/semantics/methods.k:28-28` | ordinary-rule | — | no | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 658 | `/reference/reference-semantics/semantics/methods.k:29-29` | ordinary-rule | — | no | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 659 | `/reference/reference-semantics/semantics/methods.k:30-31` | ordinary-rule | — | no | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` |
| 660 | `/reference/reference-semantics/semantics/methods.k:34-34` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 661 | `/reference/reference-semantics/semantics/methods.k:35-35` | syntax-declaration | function | no | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 662 | `/reference/reference-semantics/semantics/methods.k:36-36` | ordinary-rule | — | no | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 663 | `/reference/reference-semantics/semantics/methods.k:37-38` | ordinary-rule | — | no | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| 664 | `/reference/reference-semantics/semantics/methods.k:39-40` | ordinary-rule | — | no | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| 665 | `/reference/reference-semantics/semantics/methods.k:41-41` | syntax-declaration | function, total | no | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 666 | `/reference/reference-semantics/semantics/methods.k:42-42` | ordinary-rule | — | no | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 667 | `/reference/reference-semantics/semantics/methods.k:43-43` | ordinary-rule | owise | no | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 668 | `/reference/reference-semantics/semantics/methods.k:44-44` | ordinary-rule | — | no | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| 669 | `/reference/reference-semantics/semantics/methods.k:47-47` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 670 | `/reference/reference-semantics/semantics/methods.k:48-48` | syntax-declaration | function, total | no | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 671 | `/reference/reference-semantics/semantics/methods.k:49-49` | ordinary-rule | — | no | `rule trimWS(.IntSeq) => .IntSeq` |
| 672 | `/reference/reference-semantics/semantics/methods.k:50-50` | ordinary-rule | — | no | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 673 | `/reference/reference-semantics/semantics/methods.k:51-51` | ordinary-rule | — | no | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 674 | `/reference/reference-semantics/semantics/methods.k:52-52` | syntax-declaration | function, total | no | `syntax IntSeq ::= revIS(IntSeq) [function, total] &#124; revISAcc(IntSeq, IntSeq) [function, total]` |
| 675 | `/reference/reference-semantics/semantics/methods.k:53-53` | ordinary-rule | — | no | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 676 | `/reference/reference-semantics/semantics/methods.k:54-54` | ordinary-rule | — | no | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 677 | `/reference/reference-semantics/semantics/methods.k:55-55` | ordinary-rule | — | no | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| 678 | `/reference/reference-semantics/semantics/methods.k:58-58` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| 679 | `/reference/reference-semantics/semantics/methods.k:61-61` | ordinary-rule | — | no | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| 680 | `/reference/reference-semantics/semantics/methods.k:64-64` | ordinary-rule | — | no | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 681 | `/reference/reference-semantics/semantics/methods.k:65-65` | syntax-declaration | function, total | no | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 682 | `/reference/reference-semantics/semantics/methods.k:66-66` | ordinary-rule | — | no | `rule cntOccVS(.ValSeq, _:Val) => 0` |
| 683 | `/reference/reference-semantics/semantics/methods.k:67-67` | ordinary-rule | — | no | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 684 | `/reference/reference-semantics/semantics/methods.k:68-68` | ordinary-rule | — | no | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V)` |
| 685 | `/reference/reference-semantics/semantics/methods.k:72-74` | priority-rule | priority | no | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| 686 | `/reference/reference-semantics/semantics/methods.k:75-75` | syntax-declaration | function | no | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result` |
| 687 | `/reference/reference-semantics/semantics/methods.k:76-76` | ordinary-rule | — | no | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 688 | `/reference/reference-semantics/semantics/methods.k:77-78` | ordinary-rule | — | no | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| 689 | `/reference/reference-semantics/semantics/methods.k:79-80` | ordinary-rule | — | no | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` |
| 690 | `/reference/reference-semantics/semantics/methods.k:82-82` | syntax-declaration | function | no | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 691 | `/reference/reference-semantics/semantics/methods.k:83-83` | ordinary-rule | — | no | `rule flushTok(ACC:ValSeq, .IntSeq) => ACC` |
| 692 | `/reference/reference-semantics/semantics/methods.k:84-84` | ordinary-rule | — | no | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 693 | `/reference/reference-semantics/semantics/methods.k:85-85` | syntax-declaration | function, total | no | `syntax Bool ::= isWSC(Int) [function, total]` |
| 694 | `/reference/reference-semantics/semantics/methods.k:86-86` | ordinary-rule | — | no | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| 695 | `/reference/reference-semantics/semantics/methods.k:89-91` | priority-rule | priority | no | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` |
| 696 | `/reference/reference-semantics/semantics/methods.k:94-96` | priority-rule | priority | no | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| 697 | `/reference/reference-semantics/semantics/methods.k:97-97` | syntax-declaration | function | no | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token` |
| 698 | `/reference/reference-semantics/semantics/methods.k:98-98` | ordinary-rule | — | no | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)` |
| 699 | `/reference/reference-semantics/semantics/methods.k:99-100` | ordinary-rule | — | no | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| 700 | `/reference/reference-semantics/semantics/methods.k:101-102` | ordinary-rule | — | no | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| 701 | `/reference/reference-semantics/semantics/methods.k:104-105` | ordinary-rule | — | no | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| 702 | `/reference/reference-semantics/semantics/methods.k:106-106` | syntax-declaration | function, total | no | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 703 | `/reference/reference-semantics/semantics/methods.k:107-107` | ordinary-rule | — | no | `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq` |
| 704 | `/reference/reference-semantics/semantics/methods.k:108-108` | ordinary-rule | — | no | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 705 | `/reference/reference-semantics/semantics/methods.k:109-109` | ordinary-rule | — | no | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| 706 | `/reference/reference-semantics/semantics/methods.k:112-112` | syntax-declaration | function, total | no | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 707 | `/reference/reference-semantics/semantics/methods.k:113-113` | ordinary-rule | — | no | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 708 | `/reference/reference-semantics/semantics/methods.k:115-115` | syntax-declaration | function, total | no | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 709 | `/reference/reference-semantics/semantics/methods.k:116-116` | ordinary-rule | — | no | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 710 | `/reference/reference-semantics/semantics/methods.k:118-118` | syntax-declaration | function, total | no | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 711 | `/reference/reference-semantics/semantics/methods.k:119-119` | ordinary-rule | — | no | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 712 | `/reference/reference-semantics/semantics/methods.k:121-121` | syntax-declaration | function, total | no | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 713 | `/reference/reference-semantics/semantics/methods.k:122-122` | ordinary-rule | — | no | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 714 | `/reference/reference-semantics/semantics/methods.k:124-124` | syntax-declaration | function, total | no | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 715 | `/reference/reference-semantics/semantics/methods.k:125-125` | ordinary-rule | — | no | `rule hasUpper(.IntSeq) => false` |
| 716 | `/reference/reference-semantics/semantics/methods.k:126-126` | ordinary-rule | — | no | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 717 | `/reference/reference-semantics/semantics/methods.k:128-128` | syntax-declaration | function, total | no | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 718 | `/reference/reference-semantics/semantics/methods.k:129-129` | ordinary-rule | — | no | `rule hasLower(.IntSeq) => false` |
| 719 | `/reference/reference-semantics/semantics/methods.k:130-130` | ordinary-rule | — | no | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 720 | `/reference/reference-semantics/semantics/methods.k:132-132` | syntax-declaration | function, total | no | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 721 | `/reference/reference-semantics/semantics/methods.k:133-133` | ordinary-rule | — | no | `rule allAlpha(.IntSeq) => true` |
| 722 | `/reference/reference-semantics/semantics/methods.k:134-134` | ordinary-rule | — | no | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 723 | `/reference/reference-semantics/semantics/methods.k:136-136` | syntax-declaration | function, total | no | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 724 | `/reference/reference-semantics/semantics/methods.k:137-137` | ordinary-rule | — | no | `rule allDigit(.IntSeq) => true` |
| 725 | `/reference/reference-semantics/semantics/methods.k:138-138` | ordinary-rule | — | no | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 726 | `/reference/reference-semantics/semantics/methods.k:140-140` | syntax-declaration | function, total | no | `syntax Int ::= lowerC(Int) [function, total]` |
| 727 | `/reference/reference-semantics/semantics/methods.k:142-142` | ordinary-rule | — | no | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 728 | `/reference/reference-semantics/semantics/methods.k:143-143` | ordinary-rule | owise | no | `rule lowerC(C:Int) => C [owise]` |
| 729 | `/reference/reference-semantics/semantics/methods.k:145-145` | syntax-declaration | function, total | no | `syntax Int ::= upperC(Int) [function, total]` |
| 730 | `/reference/reference-semantics/semantics/methods.k:146-146` | ordinary-rule | — | no | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 731 | `/reference/reference-semantics/semantics/methods.k:147-147` | ordinary-rule | owise | no | `rule upperC(C:Int) => C [owise]` |
| 732 | `/reference/reference-semantics/semantics/methods.k:149-149` | syntax-declaration | function, total | no | `syntax Int ::= swapC(Int) [function, total]` |
| 733 | `/reference/reference-semantics/semantics/methods.k:150-150` | ordinary-rule | — | no | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 734 | `/reference/reference-semantics/semantics/methods.k:151-151` | ordinary-rule | — | no | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 735 | `/reference/reference-semantics/semantics/methods.k:152-152` | ordinary-rule | owise | no | `rule swapC(C:Int) => C [owise]` |
| 736 | `/reference/reference-semantics/semantics/methods.k:154-154` | syntax-declaration | function, total | no | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 737 | `/reference/reference-semantics/semantics/methods.k:155-155` | ordinary-rule | — | no | `rule mapLower(.IntSeq) => .IntSeq` |
| 738 | `/reference/reference-semantics/semantics/methods.k:156-156` | ordinary-rule | — | no | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 739 | `/reference/reference-semantics/semantics/methods.k:158-158` | syntax-declaration | function, total | no | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 740 | `/reference/reference-semantics/semantics/methods.k:159-159` | ordinary-rule | — | no | `rule mapUpper(.IntSeq) => .IntSeq` |
| 741 | `/reference/reference-semantics/semantics/methods.k:160-160` | ordinary-rule | — | no | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 742 | `/reference/reference-semantics/semantics/methods.k:162-162` | syntax-declaration | function, total | no | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 743 | `/reference/reference-semantics/semantics/methods.k:163-163` | ordinary-rule | — | no | `rule mapSwap(.IntSeq) => .IntSeq` |
| 744 | `/reference/reference-semantics/semantics/methods.k:164-164` | ordinary-rule | — | no | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 745 | `/reference/reference-semantics/semantics/methods.k:166-166` | syntax-declaration | function, total | no | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 746 | `/reference/reference-semantics/semantics/methods.k:167-167` | ordinary-rule | — | no | `rule startsWith(.IntSeq, _:IntSeq) => true` |
| 747 | `/reference/reference-semantics/semantics/methods.k:168-168` | ordinary-rule | — | no | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 748 | `/reference/reference-semantics/semantics/methods.k:169-169` | ordinary-rule | — | no | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| 749 | `/reference/reference-semantics/semantics/operators.k:10-10` | ordinary-rule | — | no | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 750 | `/reference/reference-semantics/semantics/operators.k:12-12` | ordinary-rule | — | no | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| 751 | `/reference/reference-semantics/semantics/operators.k:15-15` | evaluation-context | — | no | `context Compare(HOLE, _)` |
| 752 | `/reference/reference-semantics/semantics/operators.k:16-16` | evaluation-context | — | no | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 753 | `/reference/reference-semantics/semantics/operators.k:17-17` | ordinary-rule | owise | no | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 754 | `/reference/reference-semantics/semantics/operators.k:19-19` | ordinary-rule | — | no | `rule applyCmp("is", V:Val, noneV) => V ==K noneV` |
| 755 | `/reference/reference-semantics/semantics/operators.k:20-20` | ordinary-rule | — | no | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| 756 | `/reference/reference-semantics/semantics/operators.k:25-27` | priority-rule | priority | no | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 757 | `/reference/reference-semantics/semantics/operators.k:28-31` | priority-rule | priority | no | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` |
| 758 | `/reference/reference-semantics/semantics/operators.k:34-37` | priority-rule | priority | no | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| 759 | `/reference/reference-semantics/semantics/operators.k:38-42` | priority-rule | priority | no | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| 760 | `/reference/reference-semantics/semantics/operators.k:44-46` | priority-rule | priority | no | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 761 | `/reference/reference-semantics/semantics/range.k:9-9` | syntax-declaration | function, total | no | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 762 | `/reference/reference-semantics/semantics/range.k:10-10` | ordinary-rule | — | no | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 763 | `/reference/reference-semantics/semantics/range.k:12-12` | syntax-declaration | function | no | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 764 | `/reference/reference-semantics/semantics/range.k:13-14` | ordinary-rule | — | no | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| 765 | `/reference/reference-semantics/semantics/range.k:15-16` | ordinary-rule | — | no | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| 766 | `/reference/reference-semantics/semantics/range.k:17-18` | ordinary-rule | — | no | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| 767 | `/reference/reference-semantics/semantics/range.k:20-22` | ordinary-rule | — | no | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| 768 | `/reference/reference-semantics/semantics/range.k:23-24` | ordinary-rule | — | no | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| 769 | `/reference/reference-semantics/semantics/set.k:8-8` | syntax-declaration | — | no | `syntax Val ::= setV(IntSeq)` |
| 770 | `/reference/reference-semantics/semantics/set.k:11-11` | syntax-declaration | function, total | no | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 771 | `/reference/reference-semantics/semantics/set.k:12-12` | ordinary-rule | — | no | `rule codeIn(_:Int, .IntSeq) => false` |
| 772 | `/reference/reference-semantics/semantics/set.k:13-13` | ordinary-rule | — | no | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| 773 | `/reference/reference-semantics/semantics/set.k:16-17` | syntax-declaration | function, total | no | `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] &#124; dedupFrom(IntSeq, IntSeq) [function, total]` |
| 774 | `/reference/reference-semantics/semantics/set.k:18-18` | ordinary-rule | — | no | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 775 | `/reference/reference-semantics/semantics/set.k:19-19` | ordinary-rule | — | no | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 776 | `/reference/reference-semantics/semantics/set.k:20-21` | ordinary-rule | — | no | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| 777 | `/reference/reference-semantics/semantics/set.k:22-23` | ordinary-rule | — | no | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| 778 | `/reference/reference-semantics/semantics/set.k:25-25` | syntax-declaration | function, total | no | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 779 | `/reference/reference-semantics/semantics/set.k:26-26` | ordinary-rule | — | no | `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)` |
| 780 | `/reference/reference-semantics/semantics/set.k:27-27` | ordinary-rule | — | no | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| 781 | `/reference/reference-semantics/semantics/set.k:31-31` | syntax-declaration | function, total | no | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 782 | `/reference/reference-semantics/semantics/set.k:32-32` | ordinary-rule | — | no | `rule subsetCodes(.IntSeq, _:IntSeq) => true` |
| 783 | `/reference/reference-semantics/semantics/set.k:33-33` | ordinary-rule | — | no | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 784 | `/reference/reference-semantics/semantics/set.k:35-35` | syntax-declaration | function, total | no | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 785 | `/reference/reference-semantics/semantics/set.k:36-36` | ordinary-rule | — | no | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| 786 | `/reference/reference-semantics/semantics/set.k:39-39` | ordinary-rule | — | no | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| 787 | `/reference/reference-semantics/semantics/sort.k:18-18` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 788 | `/reference/reference-semantics/semantics/sort.k:19-19` | syntax-declaration | function | no | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 789 | `/reference/reference-semantics/semantics/sort.k:20-20` | ordinary-rule | concrete | no | `rule sortVS(.ValSeq) => .ValSeq [concrete]` |
| 790 | `/reference/reference-semantics/semantics/sort.k:21-21` | ordinary-rule | concrete | no | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 791 | `/reference/reference-semantics/semantics/sort.k:22-22` | ordinary-rule | concrete | no | `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]` |
| 792 | `/reference/reference-semantics/semantics/sort.k:23-23` | ordinary-rule | concrete | no | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 793 | `/reference/reference-semantics/semantics/sort.k:24-24` | ordinary-rule | concrete | no | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete]` |
| 794 | `/reference/reference-semantics/semantics/sort.k:26-26` | syntax-declaration | function | no | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 795 | `/reference/reference-semantics/semantics/sort.k:27-27` | ordinary-rule | concrete | no | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 796 | `/reference/reference-semantics/semantics/sort.k:28-28` | ordinary-rule | concrete | no | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 797 | `/reference/reference-semantics/semantics/sort.k:29-30` | ordinary-rule | concrete | no | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| 798 | `/reference/reference-semantics/semantics/sort.k:31-32` | ordinary-rule | concrete | no | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` |
| 799 | `/reference/reference-semantics/semantics/sort.k:36-37` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` |
| 800 | `/reference/reference-semantics/semantics/sort.k:40-42` | priority-rule | priority | no | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H &#124;-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` |
| 801 | `/reference/reference-semantics/semantics/sort.k:49-49` | syntax-declaration | function, no-evaluators, symbol, total | yes | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 802 | `/reference/reference-semantics/semantics/sort.k:51-52` | syntax-declaration | function, total | no | `syntax ValSeq ::= revVS(ValSeq) [function, total] &#124; revVSAcc(ValSeq, ValSeq) [function, total]` |
| 803 | `/reference/reference-semantics/semantics/sort.k:53-53` | ordinary-rule | — | no | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 804 | `/reference/reference-semantics/semantics/sort.k:54-54` | ordinary-rule | — | no | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 805 | `/reference/reference-semantics/semantics/sort.k:55-55` | ordinary-rule | — | no | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 806 | `/reference/reference-semantics/semantics/sort.k:57-57` | syntax-declaration | function, total | no | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 807 | `/reference/reference-semantics/semantics/sort.k:58-58` | ordinary-rule | — | no | `rule condRev(S:ValSeq, false) => S` |
| 808 | `/reference/reference-semantics/semantics/sort.k:59-59` | ordinary-rule | — | no | `rule condRev(S:ValSeq, true) => revVS(S)` |
| 809 | `/reference/reference-semantics/semantics/sort.k:61-62` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| 810 | `/reference/reference-semantics/semantics/sort.k:63-64` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| 811 | `/reference/reference-semantics/semantics/sort.k:65-66` | ordinary-rule | — | no | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` |
| 812 | `/reference/reference-semantics/semantics/str.k:8-8` | ordinary-rule | — | no | `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>` |
| 813 | `/reference/reference-semantics/semantics/str.k:9-10` | ordinary-rule | — | no | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` |
| 814 | `/reference/reference-semantics/semantics/str.k:13-13` | syntax-declaration | function | no | `syntax IntSeq ::= strToCodes(String) [function]` |
| 815 | `/reference/reference-semantics/semantics/str.k:14-14` | ordinary-rule | — | no | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 816 | `/reference/reference-semantics/semantics/str.k:15-15` | ordinary-rule | — | no | `rule strToCodes("") => .IntSeq` |
| 817 | `/reference/reference-semantics/semantics/str.k:16-17` | ordinary-rule | — | no | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` |
| 818 | `/reference/reference-semantics/semantics/str.k:20-20` | syntax-declaration | function, total | no | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 819 | `/reference/reference-semantics/semantics/str.k:21-21` | ordinary-rule | — | no | `rule seqConcat(.IntSeq, T:IntSeq) => T` |
| 820 | `/reference/reference-semantics/semantics/str.k:22-22` | ordinary-rule | — | no | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 821 | `/reference/reference-semantics/semantics/str.k:24-24` | ordinary-rule | — | no | `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 822 | `/reference/reference-semantics/semantics/str.k:25-25` | ordinary-rule | — | no | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 823 | `/reference/reference-semantics/semantics/str.k:26-26` | ordinary-rule | — | no | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| 824 | `/reference/reference-semantics/semantics/str.k:29-29` | ordinary-rule | — | no | `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 825 | `/reference/reference-semantics/semantics/str.k:30-30` | ordinary-rule | — | no | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 826 | `/reference/reference-semantics/semantics/str.k:32-32` | syntax-declaration | function, total | no | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 827 | `/reference/reference-semantics/semantics/str.k:33-33` | ordinary-rule | — | no | `rule strPrefix(.IntSeq, _:IntSeq) => true` |
| 828 | `/reference/reference-semantics/semantics/str.k:34-34` | ordinary-rule | — | no | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 829 | `/reference/reference-semantics/semantics/str.k:35-35` | ordinary-rule | — | no | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 830 | `/reference/reference-semantics/semantics/str.k:37-37` | syntax-declaration | function, total | no | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 831 | `/reference/reference-semantics/semantics/str.k:38-38` | ordinary-rule | — | no | `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)` |
| 832 | `/reference/reference-semantics/semantics/str.k:39-39` | ordinary-rule | — | no | `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)` |
| 833 | `/reference/reference-semantics/semantics/str.k:40-41` | ordinary-rule | — | no | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` |
| 834 | `/reference/reference-semantics/semantics/str.k:48-48` | syntax-declaration | function, total | no | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 835 | `/reference/reference-semantics/semantics/str.k:49-49` | ordinary-rule | — | no | `rule strLt(.IntSeq, .IntSeq) => false` |
| 836 | `/reference/reference-semantics/semantics/str.k:50-50` | ordinary-rule | — | no | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 837 | `/reference/reference-semantics/semantics/str.k:51-51` | ordinary-rule | — | no | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 838 | `/reference/reference-semantics/semantics/str.k:52-52` | ordinary-rule | — | no | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B` |
| 839 | `/reference/reference-semantics/semantics/str.k:53-53` | ordinary-rule | — | no | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B` |
| 840 | `/reference/reference-semantics/semantics/str.k:54-54` | ordinary-rule | — | no | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 841 | `/reference/reference-semantics/semantics/str.k:56-56` | ordinary-rule | — | no | `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 842 | `/reference/reference-semantics/semantics/str.k:57-57` | ordinary-rule | — | no | `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 843 | `/reference/reference-semantics/semantics/str.k:58-58` | ordinary-rule | — | no | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 844 | `/reference/reference-semantics/semantics/str.k:59-59` | ordinary-rule | — | no | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| 845 | `/reference/reference-semantics/semantics/subscript.k:11-11` | syntax-declaration | function, total | no | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 846 | `/reference/reference-semantics/semantics/subscript.k:12-12` | ordinary-rule | — | no | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V` |
| 847 | `/reference/reference-semantics/semantics/subscript.k:13-14` | ordinary-rule | — | no | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| 848 | `/reference/reference-semantics/semantics/subscript.k:16-16` | syntax-declaration | function | no | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 849 | `/reference/reference-semantics/semantics/subscript.k:17-17` | ordinary-rule | — | no | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C` |
| 850 | `/reference/reference-semantics/semantics/subscript.k:18-19` | ordinary-rule | — | no | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| 851 | `/reference/reference-semantics/semantics/subscript.k:21-21` | syntax-declaration | function, total | no | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 852 | `/reference/reference-semantics/semantics/subscript.k:22-22` | ordinary-rule | — | no | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 853 | `/reference/reference-semantics/semantics/subscript.k:23-23` | ordinary-rule | — | no | `rule normIdx(I:Int, _:Int) => I requires I >=Int 0` |
| 854 | `/reference/reference-semantics/semantics/subscript.k:27-27` | evaluation-context | — | no | `context Subscript(HOLE, _)` |
| 855 | `/reference/reference-semantics/semantics/subscript.k:28-28` | evaluation-context | — | no | `context Subscript(_:Val, HOLE:Expr)` |
| 856 | `/reference/reference-semantics/semantics/subscript.k:31-33` | priority-rule | priority | no | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 857 | `/reference/reference-semantics/semantics/subscript.k:35-35` | ordinary-rule | — | no | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 858 | `/reference/reference-semantics/semantics/subscript.k:37-37` | syntax-declaration | function | no | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 859 | `/reference/reference-semantics/semantics/subscript.k:38-38` | ordinary-rule | — | no | `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 860 | `/reference/reference-semantics/semantics/subscript.k:39-39` | ordinary-rule | — | no | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 861 | `/reference/reference-semantics/semantics/subscript.k:40-41` | ordinary-rule | — | no | `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` |
| 862 | `/reference/reference-semantics/semantics/subscript.k:44-47` | syntax-declaration | — | no | `syntax KItem ::= #evalB(Bound) &#124; "#toSome" &#124; #slLo(Val, Bound, Bound) &#124; #slHi(Val, OptInt, Bound) &#124; #slStep(Val, OptInt, OptInt)` |
| 863 | `/reference/reference-semantics/semantics/subscript.k:49-49` | syntax-declaration | — | no | `syntax OptInt ::= "noB" &#124; someB(Int)` |
| 864 | `/reference/reference-semantics/semantics/subscript.k:50-50` | ordinary-rule | — | no | `rule <k> #evalB(NoBound) => noB ... </k>` |
| 865 | `/reference/reference-semantics/semantics/subscript.k:51-51` | ordinary-rule | — | no | `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>` |
| 866 | `/reference/reference-semantics/semantics/subscript.k:52-52` | ordinary-rule | — | no | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 867 | `/reference/reference-semantics/semantics/subscript.k:54-54` | ordinary-rule | — | no | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 868 | `/reference/reference-semantics/semantics/subscript.k:55-55` | ordinary-rule | — | no | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 869 | `/reference/reference-semantics/semantics/subscript.k:56-56` | ordinary-rule | — | no | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| 870 | `/reference/reference-semantics/semantics/subscript.k:58-60` | priority-rule | priority | no | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| 871 | `/reference/reference-semantics/semantics/subscript.k:61-61` | ordinary-rule | — | no | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 872 | `/reference/reference-semantics/semantics/subscript.k:63-63` | syntax-declaration | function | no | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 873 | `/reference/reference-semantics/semantics/subscript.k:64-65` | ordinary-rule | — | no | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 874 | `/reference/reference-semantics/semantics/subscript.k:66-67` | ordinary-rule | — | no | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 875 | `/reference/reference-semantics/semantics/subscript.k:68-69` | ordinary-rule | — | no | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` |
| 876 | `/reference/reference-semantics/semantics/subscript.k:72-72` | syntax-declaration | function, total | no | `syntax Int ::= slStep(OptInt) [function, total]` |
| 877 | `/reference/reference-semantics/semantics/subscript.k:73-73` | ordinary-rule | — | no | `rule slStep(noB) => 1` |
| 878 | `/reference/reference-semantics/semantics/subscript.k:74-74` | ordinary-rule | — | no | `rule slStep(someB(S:Int)) => S` |
| 879 | `/reference/reference-semantics/semantics/subscript.k:76-76` | syntax-declaration | function | no | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 880 | `/reference/reference-semantics/semantics/subscript.k:77-78` | ordinary-rule | — | no | `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| 881 | `/reference/reference-semantics/semantics/subscript.k:79-80` | ordinary-rule | — | no | `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0` |
| 882 | `/reference/reference-semantics/semantics/subscript.k:81-81` | ordinary-rule | — | no | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 883 | `/reference/reference-semantics/semantics/subscript.k:83-83` | syntax-declaration | function | no | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 884 | `/reference/reference-semantics/semantics/subscript.k:84-85` | ordinary-rule | — | no | `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0` |
| 885 | `/reference/reference-semantics/semantics/subscript.k:86-87` | ordinary-rule | — | no | `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| 886 | `/reference/reference-semantics/semantics/subscript.k:88-88` | ordinary-rule | — | no | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 887 | `/reference/reference-semantics/semantics/subscript.k:90-90` | syntax-declaration | function, total | no | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 888 | `/reference/reference-semantics/semantics/subscript.k:91-92` | ordinary-rule | — | no | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0` |
| 889 | `/reference/reference-semantics/semantics/subscript.k:93-94` | ordinary-rule | — | no | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| 890 | `/reference/reference-semantics/semantics/subscript.k:96-96` | syntax-declaration | function, total | no | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 891 | `/reference/reference-semantics/semantics/subscript.k:97-98` | ordinary-rule | — | no | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| 892 | `/reference/reference-semantics/semantics/subscript.k:99-100` | ordinary-rule | — | no | `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| 893 | `/reference/reference-semantics/semantics/subscript.k:102-102` | syntax-declaration | function, total | no | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 894 | `/reference/reference-semantics/semantics/subscript.k:103-104` | ordinary-rule | — | no | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN` |
| 895 | `/reference/reference-semantics/semantics/subscript.k:105-106` | ordinary-rule | — | no | `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` |
| 896 | `/reference/reference-semantics/semantics/subscript.k:109-109` | syntax-declaration | function | no | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 897 | `/reference/reference-semantics/semantics/subscript.k:110-112` | ordinary-rule | — | no | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 898 | `/reference/reference-semantics/semantics/subscript.k:113-114` | ordinary-rule | — | no | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 899 | `/reference/reference-semantics/semantics/subscript.k:116-116` | syntax-declaration | function | no | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 900 | `/reference/reference-semantics/semantics/subscript.k:117-119` | ordinary-rule | — | no | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 901 | `/reference/reference-semantics/semantics/subscript.k:120-121` | ordinary-rule | — | no | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 902 | `/reference/reference-semantics/semantics/syntax.k:9-30` | syntax-declaration | macro, seqstrict, strict | no | `syntax Expr ::= "Int" "(" Int ")" &#124; "Float" "(" Float ")" &#124; "Bool" "(" Bool ")" &#124; "Name" "(" String ")" &#124; "Str" "(" String ")" &#124; "UnaryOp" "(" String "," Expr ")" [strict(2)] &#124; "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] &#124; "BoolOp" "(" String "," Exprs ")" &#124; "ListExpr" "(" Exprs ")" &#124; "DictExpr" "(" Entries ")" &#124; "ListComp" "(" Expr "," CompFors ")" ...` |
| 903 | `/reference/reference-semantics/semantics/syntax.k:32-32` | syntax-declaration | — | no | `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"` |
| 904 | `/reference/reference-semantics/semantics/syntax.k:33-33` | syntax-declaration | — | no | `syntax Entry ::= "Entry" "(" Expr "," Expr ")"` |
| 905 | `/reference/reference-semantics/semantics/syntax.k:34-34` | syntax-declaration | — | no | `syntax Entries ::= List{Entry, ","}` |
| 906 | `/reference/reference-semantics/semantics/syntax.k:35-35` | syntax-declaration | — | no | `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 907 | `/reference/reference-semantics/semantics/syntax.k:36-36` | syntax-declaration | — | no | `syntax CompFors ::= List{CompFor, ""}` |
| 908 | `/reference/reference-semantics/semantics/syntax.k:37-37` | syntax-declaration | — | no | `syntax Exprs ::= List{Expr, ","}` |
| 909 | `/reference/reference-semantics/semantics/syntax.k:38-38` | syntax-declaration | — | no | `syntax Index ::= Expr &#124; "Slice" "(" Bound "," Bound "," Bound ")"` |
| 910 | `/reference/reference-semantics/semantics/syntax.k:39-39` | syntax-declaration | — | no | `syntax Bound ::= Expr &#124; "NoBound"` |
| 911 | `/reference/reference-semantics/semantics/syntax.k:41-54` | syntax-declaration | strict | no | `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] &#124; "Import" "(" String ")" &#124; "ImportFrom" "(" String "," ParamNames ")" &#124; "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] &#124; "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] &#124; "While" "(" Expr "," Stmts ")" &#124; "Break" &#124; "Continue" &#124; "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] &#124; "Return" "(" Expr ")"...` |
| 912 | `/reference/reference-semantics/semantics/syntax.k:56-56` | syntax-declaration | — | no | `syntax Stmts ::= List{Stmt, ""}` |
| 913 | `/reference/reference-semantics/semantics/syntax.k:57-57` | syntax-declaration | — | no | `syntax Params ::= "Params" "(" ParamNames ")"` |
| 914 | `/reference/reference-semantics/semantics/syntax.k:58-58` | syntax-declaration | — | no | `syntax CellVars ::= "CellVars" "(" ParamNames ")"` |
| 915 | `/reference/reference-semantics/semantics/syntax.k:59-59` | syntax-declaration | — | no | `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"` |
| 916 | `/reference/reference-semantics/semantics/syntax.k:60-60` | syntax-declaration | — | no | `syntax ParamNames ::= List{String, ","}` |
| 917 | `/reference/reference-semantics/semantics/syntax.k:61-61` | syntax-declaration | — | no | `syntax Module ::= "Module" "(" Stmts ")"` |
| 918 | `/reference/reference-semantics/semantics/tuple.k:10-10` | ordinary-rule | — | no | `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>` |
| 919 | `/reference/reference-semantics/semantics/tuple.k:11-11` | ordinary-rule | — | no | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| 920 | `/reference/reference-semantics/semantics/tuple.k:14-14` | syntax-declaration | — | no | `syntax ApplyK ::= "toTuple"` |
| 921 | `/reference/reference-semantics/semantics/tuple.k:15-15` | ordinary-rule | — | no | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 922 | `/reference/reference-semantics/semantics/tuple.k:16-16` | ordinary-rule | — | no | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 923 | `/reference/reference-semantics/semantics/tuple.k:18-18` | ordinary-rule | — | no | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| 924 | `/reference/reference-semantics/semantics/tuple.k:20-20` | ordinary-rule | — | no | `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 925 | `/reference/reference-semantics/semantics/tuple.k:21-21` | ordinary-rule | — | no | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| 926 | `/reference/reference-semantics/semantics/tuple.k:23-23` | ordinary-rule | — | no | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 927 | `/reference/reference-semantics/semantics/tuple.k:24-24` | syntax-declaration | function | no | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 928 | `/reference/reference-semantics/semantics/tuple.k:25-25` | ordinary-rule | — | no | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 929 | `/reference/reference-semantics/semantics/tuple.k:26-27` | ordinary-rule | — | no | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| 930 | `/reference/reference-semantics/semantics/tuple.k:28-28` | ordinary-rule | — | no | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| 931 | `/reference/reference-semantics/semantics/tuple.k:31-31` | syntax-declaration | — | no | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 932 | `/reference/reference-semantics/semantics/tuple.k:32-34` | ordinary-rule | — | no | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 933 | `/reference/reference-semantics/semantics/tuple.k:35-41` | priority-rule | priority | no | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 934 | `/reference/reference-semantics/semantics/tuple.k:42-42` | ordinary-rule | — | no | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 935 | `/reference/reference-semantics/semantics/tuple.k:43-43` | ordinary-rule | — | no | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 936 | `/reference/reference-semantics/semantics/tuple.k:44-46` | priority-rule | priority | no | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 937 | `/reference/reference-semantics/semantics/tuple.k:49-49` | syntax-declaration | — | no | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 938 | `/reference/reference-semantics/semantics/tuple.k:50-50` | ordinary-rule | — | no | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 939 | `/reference/reference-semantics/semantics/tuple.k:51-51` | ordinary-rule | — | no | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 940 | `/reference/reference-semantics/semantics/tuple.k:52-54` | priority-rule | priority | no | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)]` |
| 941 | `/reference/reference-semantics/semantics/tuple.k:55-56` | ordinary-rule | — | no | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| 942 | `/reference/reference-semantics/semantics/tuple.k:57-57` | ordinary-rule | — | no | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |

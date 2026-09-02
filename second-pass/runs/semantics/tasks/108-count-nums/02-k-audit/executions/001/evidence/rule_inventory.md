# Exhaustive K declaration and rule inventory

Generated from the fresh scratch copy. Each row is one K declaration, configuration, context, rule, or claim start; multiline bodies retain their source location and are available in the byte-checked source tree.

Total records: 1004.

Kinds: claim=9, configuration=1, context=5, rule=737, syntax=252.

Review classes: integrity-checked supplied-semantics baseline=928, proof-local definition or exact-syntax macro=59, proof-local operational bridge=8, target reachability claim=9.

| # | Location | Kind | Attributes | Audit class | Declaration start |
|---:|---|---|---|---|---|
| 1 | `reference-semantics/semantics/assert.k:6` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Assert(V:Val) => .K ... </k>` |
| 2 | `reference-semantics/semantics/assert.k:8` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Assert(V:Val) ~> _ => .K </k>` |
| 3 | `reference-semantics/semantics/assert.k:13` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>` |
| 4 | `reference-semantics/semantics/bool.k:8` | rule | — | integrity-checked supplied-semantics baseline | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 5 | `reference-semantics/semantics/bool.k:10` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 6 | `reference-semantics/semantics/bool.k:11` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| 7 | `reference-semantics/semantics/bool.k:16` | context | — | integrity-checked supplied-semantics baseline | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 8 | `reference-semantics/semantics/bool.k:17` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 9 | `reference-semantics/semantics/bool.k:18` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>` |
| 10 | `reference-semantics/semantics/bool.k:20` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>` |
| 11 | `reference-semantics/semantics/bool.k:22` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k>` |
| 12 | `reference-semantics/semantics/bool.k:24` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>` |
| 13 | `reference-semantics/semantics/bool.k:29` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>` |
| 14 | `reference-semantics/semantics/bool.k:31` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>` |
| 15 | `reference-semantics/semantics/bool.k:35` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>` |
| 16 | `reference-semantics/semantics/bool.k:39` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>` |
| 17 | `reference-semantics/semantics/bool.k:43` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>` |
| 18 | `reference-semantics/semantics/builtins.k:17` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| 19 | `reference-semantics/semantics/builtins.k:20` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= seqLen(Val) [function]` |
| 20 | `reference-semantics/semantics/builtins.k:21` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 21 | `reference-semantics/semantics/builtins.k:22` | rule | — | integrity-checked supplied-semantics baseline | `rule seqLen(list(VS:ValSeq)) => vsLen(VS)` |
| 22 | `reference-semantics/semantics/builtins.k:23` | rule | — | integrity-checked supplied-semantics baseline | `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)` |
| 23 | `reference-semantics/semantics/builtins.k:24` | rule | — | integrity-checked supplied-semantics baseline | `rule seqLen(str(IS:IntSeq)) => isLen(IS)` |
| 24 | `reference-semantics/semantics/builtins.k:25` | rule | — | integrity-checked supplied-semantics baseline | `rule seqLen(setV(DS:IntSeq)) => isLen(DS)` |
| 25 | `reference-semantics/semantics/builtins.k:26` | rule | — | integrity-checked supplied-semantics baseline | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| 26 | `reference-semantics/semantics/builtins.k:32` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 27 | `reference-semantics/semantics/builtins.k:33` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 28 | `reference-semantics/semantics/builtins.k:34` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>` |
| 29 | `reference-semantics/semantics/builtins.k:35` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>` |
| 30 | `reference-semantics/semantics/builtins.k:36` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 31 | `reference-semantics/semantics/builtins.k:37` | rule | — | integrity-checked supplied-semantics baseline | `rule charsOf(.IntSeq) => .ValSeq` |
| 32 | `reference-semantics/semantics/builtins.k:38` | rule | — | integrity-checked supplied-semantics baseline | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| 33 | `reference-semantics/semantics/builtins.k:41` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| 34 | `reference-semantics/semantics/builtins.k:44` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| 35 | `reference-semantics/semantics/builtins.k:47` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 36 | `reference-semantics/semantics/builtins.k:48` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 37 | `reference-semantics/semantics/builtins.k:49` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 38 | `reference-semantics/semantics/builtins.k:50` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)` |
| 39 | `reference-semantics/semantics/builtins.k:54` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= intOf(Val) [function]` |
| 40 | `reference-semantics/semantics/builtins.k:55` | rule | — | integrity-checked supplied-semantics baseline | `rule intOf(I:Int) => I` |
| 41 | `reference-semantics/semantics/builtins.k:56` | rule | — | integrity-checked supplied-semantics baseline | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| 42 | `reference-semantics/semantics/builtins.k:59` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 43 | `reference-semantics/semantics/builtins.k:60` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 44 | `reference-semantics/semantics/builtins.k:61` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 45 | `reference-semantics/semantics/builtins.k:62` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>` |
| 46 | `reference-semantics/semantics/builtins.k:64` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>` |
| 47 | `reference-semantics/semantics/builtins.k:67` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 48 | `reference-semantics/semantics/builtins.k:68` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 49 | `reference-semantics/semantics/builtins.k:69` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 50 | `reference-semantics/semantics/builtins.k:70` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>` |
| 51 | `reference-semantics/semantics/builtins.k:72` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>` |
| 52 | `reference-semantics/semantics/builtins.k:76` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 53 | `reference-semantics/semantics/builtins.k:77` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 54 | `reference-semantics/semantics/builtins.k:78` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>` |
| 55 | `reference-semantics/semantics/builtins.k:80` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 56 | `reference-semantics/semantics/builtins.k:81` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 57 | `reference-semantics/semantics/builtins.k:82` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)` |
| 58 | `reference-semantics/semantics/builtins.k:86` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 59 | `reference-semantics/semantics/builtins.k:87` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 60 | `reference-semantics/semantics/builtins.k:88` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>` |
| 61 | `reference-semantics/semantics/builtins.k:90` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 62 | `reference-semantics/semantics/builtins.k:91` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 63 | `reference-semantics/semantics/builtins.k:92` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)` |
| 64 | `reference-semantics/semantics/builtins.k:97` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 65 | `reference-semantics/semantics/builtins.k:98` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 66 | `reference-semantics/semantics/builtins.k:99` | rule | — | integrity-checked supplied-semantics baseline | `rule maxVals(M:Int, .Vals) => M` |
| 67 | `reference-semantics/semantics/builtins.k:100` | rule | — | integrity-checked supplied-semantics baseline | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| 68 | `reference-semantics/semantics/builtins.k:102` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= minVals(Int, Vals) [function]` |
| 69 | `reference-semantics/semantics/builtins.k:103` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 70 | `reference-semantics/semantics/builtins.k:104` | rule | — | integrity-checked supplied-semantics baseline | `rule minVals(M:Int, .Vals) => M` |
| 71 | `reference-semantics/semantics/builtins.k:105` | rule | — | integrity-checked supplied-semantics baseline | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| 72 | `reference-semantics/semantics/builtins.k:108` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))` |
| 73 | `reference-semantics/semantics/builtins.k:111` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("bin", N:Int, .Vals)` |
| 74 | `reference-semantics/semantics/builtins.k:114` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 75 | `reference-semantics/semantics/builtins.k:115` | rule | — | integrity-checked supplied-semantics baseline | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 76 | `reference-semantics/semantics/builtins.k:116` | rule | — | integrity-checked supplied-semantics baseline | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 77 | `reference-semantics/semantics/builtins.k:117` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 78 | `reference-semantics/semantics/builtins.k:118` | rule | — | integrity-checked supplied-semantics baseline | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 79 | `reference-semantics/semantics/builtins.k:119` | rule | — | integrity-checked supplied-semantics baseline | `rule binAcc(N:Int, ACC:IntSeq)` |
| 80 | `reference-semantics/semantics/builtins.k:124` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))` |
| 81 | `reference-semantics/semantics/builtins.k:126` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 82 | `reference-semantics/semantics/builtins.k:127` | rule | — | integrity-checked supplied-semantics baseline | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 83 | `reference-semantics/semantics/builtins.k:128` | rule | — | integrity-checked supplied-semantics baseline | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int)` |
| 84 | `reference-semantics/semantics/builtins.k:132` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))` |
| 85 | `reference-semantics/semantics/builtins.k:134` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 86 | `reference-semantics/semantics/builtins.k:135` | rule | — | integrity-checked supplied-semantics baseline | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 87 | `reference-semantics/semantics/builtins.k:136` | rule | — | integrity-checked supplied-semantics baseline | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 88 | `reference-semantics/semantics/builtins.k:137` | rule | — | integrity-checked supplied-semantics baseline | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| 89 | `reference-semantics/semantics/builtins.k:140` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| 90 | `reference-semantics/semantics/builtins.k:143` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 91 | `reference-semantics/semantics/builtins.k:144` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))` |
| 92 | `reference-semantics/semantics/builtins.k:148` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))` |
| 93 | `reference-semantics/semantics/builtins.k:149` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| 94 | `reference-semantics/semantics/builtins.k:152` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48` |
| 95 | `reference-semantics/semantics/builtins.k:156` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)` |
| 96 | `reference-semantics/semantics/builtins.k:158` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 97 | `reference-semantics/semantics/builtins.k:159` | rule | — | integrity-checked supplied-semantics baseline | `rule intDigAcc(.IntSeq, ACC:Int) => ACC` |
| 98 | `reference-semantics/semantics/builtins.k:160` | rule | — | integrity-checked supplied-semantics baseline | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| 99 | `reference-semantics/semantics/builtins.k:163` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 100 | `reference-semantics/semantics/builtins.k:164` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B)` |
| 101 | `reference-semantics/semantics/builtins.k:167` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))` |
| 102 | `reference-semantics/semantics/builtins.k:169` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>` |
| 103 | `reference-semantics/semantics/builtins.k:170` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 104 | `reference-semantics/semantics/builtins.k:171` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))` |
| 105 | `reference-semantics/semantics/builtins.k:173` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>` |
| 106 | `reference-semantics/semantics/builtins.k:174` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| 107 | `reference-semantics/semantics/builtins.k:177` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)` |
| 108 | `reference-semantics/semantics/builtins.k:178` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)` |
| 109 | `reference-semantics/semantics/builtins.k:179` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)` |
| 110 | `reference-semantics/semantics/builtins.k:187` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 111 | `reference-semantics/semantics/builtins.k:188` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= evalArith(IntSeq) [function]` |
| 112 | `reference-semantics/semantics/builtins.k:189` | rule | — | integrity-checked supplied-semantics baseline | `rule evalArith(CS:IntSeq)` |
| 113 | `reference-semantics/semantics/builtins.k:192` | syntax | — | integrity-checked supplied-semantics baseline | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| 114 | `reference-semantics/semantics/builtins.k:194` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= evDigit(Int) [function, total]` |
| 115 | `reference-semantics/semantics/builtins.k:195` | rule | — | integrity-checked supplied-semantics baseline | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 116 | `reference-semantics/semantics/builtins.k:196` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 117 | `reference-semantics/semantics/builtins.k:197` | rule | — | integrity-checked supplied-semantics baseline | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 118 | `reference-semantics/semantics/builtins.k:198` | rule | owise | integrity-checked supplied-semantics baseline | `rule evHead42(_:IntSeq) => false [owise]` |
| 119 | `reference-semantics/semantics/builtins.k:199` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 120 | `reference-semantics/semantics/builtins.k:200` | rule | — | integrity-checked supplied-semantics baseline | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 121 | `reference-semantics/semantics/builtins.k:201` | rule | owise | integrity-checked supplied-semantics baseline | `rule evHead47(_:IntSeq) => false [owise]` |
| 122 | `reference-semantics/semantics/builtins.k:203` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 123 | `reference-semantics/semantics/builtins.k:204` | rule | — | integrity-checked supplied-semantics baseline | `rule tokOps(.IntSeq) => .OpSeq` |
| 124 | `reference-semantics/semantics/builtins.k:205` | rule | — | integrity-checked supplied-semantics baseline | `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)` |
| 125 | `reference-semantics/semantics/builtins.k:206` | rule | — | integrity-checked supplied-semantics baseline | `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)` |
| 126 | `reference-semantics/semantics/builtins.k:207` | rule | — | integrity-checked supplied-semantics baseline | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 127 | `reference-semantics/semantics/builtins.k:208` | rule | — | integrity-checked supplied-semantics baseline | `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 128 | `reference-semantics/semantics/builtins.k:209` | rule | — | integrity-checked supplied-semantics baseline | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 129 | `reference-semantics/semantics/builtins.k:210` | rule | — | integrity-checked supplied-semantics baseline | `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 130 | `reference-semantics/semantics/builtins.k:211` | rule | — | integrity-checked supplied-semantics baseline | `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))` |
| 131 | `reference-semantics/semantics/builtins.k:212` | rule | — | integrity-checked supplied-semantics baseline | `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))` |
| 132 | `reference-semantics/semantics/builtins.k:214` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= tokNds(IntSeq) [function, total]` |
| 133 | `reference-semantics/semantics/builtins.k:216` | rule | — | integrity-checked supplied-semantics baseline | `rule tokNds(.IntSeq) => .IntSeq` |
| 134 | `reference-semantics/semantics/builtins.k:217` | rule | — | integrity-checked supplied-semantics baseline | `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)` |
| 135 | `reference-semantics/semantics/builtins.k:218` | rule | — | integrity-checked supplied-semantics baseline | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 136 | `reference-semantics/semantics/builtins.k:219` | rule | — | integrity-checked supplied-semantics baseline | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)` |
| 137 | `reference-semantics/semantics/builtins.k:221` | rule | — | integrity-checked supplied-semantics baseline | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)` |
| 138 | `reference-semantics/semantics/builtins.k:223` | rule | owise | integrity-checked supplied-semantics baseline | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 139 | `reference-semantics/semantics/builtins.k:225` | syntax | — | integrity-checked supplied-semantics baseline | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 140 | `reference-semantics/semantics/builtins.k:226` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 141 | `reference-semantics/semantics/builtins.k:227` | rule | — | integrity-checked supplied-semantics baseline | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 142 | `reference-semantics/semantics/builtins.k:228` | rule | owise | integrity-checked supplied-semantics baseline | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 143 | `reference-semantics/semantics/builtins.k:230` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 144 | `reference-semantics/semantics/builtins.k:231` | rule | — | integrity-checked supplied-semantics baseline | `rule applyOpE("+", A:Int, B:Int) => A +Int B` |
| 145 | `reference-semantics/semantics/builtins.k:232` | rule | — | integrity-checked supplied-semantics baseline | `rule applyOpE("-", A:Int, B:Int) => A -Int B` |
| 146 | `reference-semantics/semantics/builtins.k:233` | rule | — | integrity-checked supplied-semantics baseline | `rule applyOpE("*", A:Int, B:Int) => A *Int B` |
| 147 | `reference-semantics/semantics/builtins.k:234` | rule | — | integrity-checked supplied-semantics baseline | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 148 | `reference-semantics/semantics/builtins.k:235` | rule | — | integrity-checked supplied-semantics baseline | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 149 | `reference-semantics/semantics/builtins.k:236` | rule | owise | integrity-checked supplied-semantics baseline | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 150 | `reference-semantics/semantics/builtins.k:238` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 151 | `reference-semantics/semantics/builtins.k:239` | rule | — | integrity-checked supplied-semantics baseline | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 152 | `reference-semantics/semantics/builtins.k:240` | rule | — | integrity-checked supplied-semantics baseline | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 153 | `reference-semantics/semantics/builtins.k:241` | rule | — | integrity-checked supplied-semantics baseline | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))` |
| 154 | `reference-semantics/semantics/builtins.k:243` | rule | owise | integrity-checked supplied-semantics baseline | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 155 | `reference-semantics/semantics/builtins.k:244` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 156 | `reference-semantics/semantics/builtins.k:245` | rule | — | integrity-checked supplied-semantics baseline | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 157 | `reference-semantics/semantics/builtins.k:246` | rule | — | integrity-checked supplied-semantics baseline | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 158 | `reference-semantics/semantics/builtins.k:247` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 159 | `reference-semantics/semantics/builtins.k:248` | rule | — | integrity-checked supplied-semantics baseline | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 160 | `reference-semantics/semantics/builtins.k:250` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 161 | `reference-semantics/semantics/builtins.k:251` | rule | — | integrity-checked supplied-semantics baseline | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 162 | `reference-semantics/semantics/builtins.k:252` | rule | — | integrity-checked supplied-semantics baseline | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 163 | `reference-semantics/semantics/builtins.k:253` | rule | — | integrity-checked supplied-semantics baseline | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 164 | `reference-semantics/semantics/builtins.k:254` | rule | — | integrity-checked supplied-semantics baseline | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 165 | `reference-semantics/semantics/builtins.k:255` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 166 | `reference-semantics/semantics/builtins.k:256` | rule | — | integrity-checked supplied-semantics baseline | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 167 | `reference-semantics/semantics/builtins.k:257` | rule | — | integrity-checked supplied-semantics baseline | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)` |
| 168 | `reference-semantics/semantics/builtins.k:260` | rule | — | integrity-checked supplied-semantics baseline | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)` |
| 169 | `reference-semantics/semantics/builtins.k:263` | rule | owise | integrity-checked supplied-semantics baseline | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)` |
| 170 | `reference-semantics/semantics/builtins.k:265` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 171 | `reference-semantics/semantics/builtins.k:266` | rule | — | integrity-checked supplied-semantics baseline | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 172 | `reference-semantics/semantics/builtins.k:267` | rule | — | integrity-checked supplied-semantics baseline | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 173 | `reference-semantics/semantics/builtins.k:268` | rule | owise | integrity-checked supplied-semantics baseline | `rule inLevelE(_:String, _:String) => false [owise]` |
| 174 | `reference-semantics/semantics/builtins.k:269` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 175 | `reference-semantics/semantics/builtins.k:270` | rule | — | integrity-checked supplied-semantics baseline | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 176 | `reference-semantics/semantics/builtins.k:271` | rule | — | integrity-checked supplied-semantics baseline | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 177 | `reference-semantics/semantics/builtins.k:272` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 178 | `reference-semantics/semantics/builtins.k:273` | rule | — | integrity-checked supplied-semantics baseline | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 179 | `reference-semantics/semantics/builtins.k:274` | rule | — | integrity-checked supplied-semantics baseline | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| 180 | `reference-semantics/semantics/builtins.k:279` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= "#md5"` |
| 181 | `reference-semantics/semantics/builtins.k:280` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>` |
| 182 | `reference-semantics/semantics/builtins.k:282` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 183 | `reference-semantics/semantics/builtins.k:283` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Val ::= md5Obj(IntSeq)` |
| 184 | `reference-semantics/semantics/builtins.k:284` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 185 | `reference-semantics/semantics/builtins.k:285` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| 186 | `reference-semantics/semantics/builtins.k:291` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 187 | `reference-semantics/semantics/builtins.k:292` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 188 | `reference-semantics/semantics/builtins.k:293` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 189 | `reference-semantics/semantics/builtins.k:294` | rule | — | integrity-checked supplied-semantics baseline | `rule isIntV(_:Int) => true` |
| 190 | `reference-semantics/semantics/builtins.k:295` | rule | owise | integrity-checked supplied-semantics baseline | `rule isIntV(_:Val) => false [owise]` |
| 191 | `reference-semantics/semantics/builtins.k:296` | rule | — | integrity-checked supplied-semantics baseline | `rule isStrV(str(_:IntSeq)) => true` |
| 192 | `reference-semantics/semantics/builtins.k:297` | rule | owise | integrity-checked supplied-semantics baseline | `rule isStrV(_:Val) => false [owise]` |
| 193 | `reference-semantics/semantics/call.k:16` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| 194 | `reference-semantics/semantics/call.k:19` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #callee(Exprs)` |
| 195 | `reference-semantics/semantics/call.k:20` | rule | owise | integrity-checked supplied-semantics baseline | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 196 | `reference-semantics/semantics/call.k:21` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| 197 | `reference-semantics/semantics/call.k:24` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 198 | `reference-semantics/semantics/call.k:26` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 199 | `reference-semantics/semantics/call.k:27` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>` |
| 200 | `reference-semantics/semantics/call.k:28` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>` |
| 201 | `reference-semantics/semantics/call.k:29` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>` |
| 202 | `reference-semantics/semantics/call.k:30` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>` |
| 203 | `reference-semantics/semantics/call.k:31` | rule | owise | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 204 | `reference-semantics/semantics/call.k:32` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k>` |
| 205 | `reference-semantics/semantics/call.k:38` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))` |
| 206 | `reference-semantics/semantics/call.k:42` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))` |
| 207 | `reference-semantics/semantics/call.k:47` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))` |
| 208 | `reference-semantics/semantics/call.k:52` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 209 | `reference-semantics/semantics/call.k:53` | rule | — | integrity-checked supplied-semantics baseline | `rule isMutMethod(M:String)` |
| 210 | `reference-semantics/semantics/call.k:56` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)` |
| 211 | `reference-semantics/semantics/call.k:63` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))` |
| 212 | `reference-semantics/semantics/call.k:69` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT` |
| 213 | `reference-semantics/semantics/call.k:80` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT` |
| 214 | `reference-semantics/semantics/call.k:87` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #allocCells(ParamNames)` |
| 215 | `reference-semantics/semantics/call.k:88` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 216 | `reference-semantics/semantics/call.k:89` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>` |
| 217 | `reference-semantics/semantics/comprehension.k:11` | rule | — | integrity-checked supplied-semantics baseline | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 218 | `reference-semantics/semantics/comprehension.k:12` | rule | — | integrity-checked supplied-semantics baseline | `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 219 | `reference-semantics/semantics/comprehension.k:14` | syntax | macro | integrity-checked supplied-semantics baseline | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 220 | `reference-semantics/semantics/comprehension.k:15` | rule | — | integrity-checked supplied-semantics baseline | `rule compBody(Gs:CompFors, ELT:Expr)` |
| 221 | `reference-semantics/semantics/comprehension.k:18` | syntax | macro, macro-rec | integrity-checked supplied-semantics baseline | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 222 | `reference-semantics/semantics/comprehension.k:19` | rule | — | integrity-checked supplied-semantics baseline | `rule compNest(.CompFors, ELT:Expr)` |
| 223 | `reference-semantics/semantics/comprehension.k:21` | rule | — | integrity-checked supplied-semantics baseline | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)` |
| 224 | `reference-semantics/semantics/comprehension.k:24` | syntax | macro | integrity-checked supplied-semantics baseline | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 225 | `reference-semantics/semantics/comprehension.k:25` | rule | — | integrity-checked supplied-semantics baseline | `rule compGuard(.Exprs) => Bool(true)` |
| 226 | `reference-semantics/semantics/comprehension.k:26` | rule | — | integrity-checked supplied-semantics baseline | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| 227 | `reference-semantics/semantics/concrete.k:13` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>` |
| 228 | `reference-semantics/semantics/concrete.k:16` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>` |
| 229 | `reference-semantics/semantics/concrete.k:25` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Val ::= kvP(Val, Val)` |
| 230 | `reference-semantics/semantics/concrete.k:26` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)` |
| 231 | `reference-semantics/semantics/concrete.k:28` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))` |
| 232 | `reference-semantics/semantics/concrete.k:31` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))` |
| 233 | `reference-semantics/semantics/concrete.k:34` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)` |
| 234 | `reference-semantics/semantics/concrete.k:36` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)` |
| 235 | `reference-semantics/semantics/concrete.k:38` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)` |
| 236 | `reference-semantics/semantics/concrete.k:42` | syntax | function | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 237 | `reference-semantics/semantics/concrete.k:43` | rule | — | integrity-checked supplied-semantics baseline | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 238 | `reference-semantics/semantics/concrete.k:44` | rule | — | integrity-checked supplied-semantics baseline | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)` |
| 239 | `reference-semantics/semantics/concrete.k:47` | rule | — | integrity-checked supplied-semantics baseline | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)` |
| 240 | `reference-semantics/semantics/concrete.k:51` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Bool ::= kLt(Val, Val) [function]` |
| 241 | `reference-semantics/semantics/concrete.k:52` | rule | — | integrity-checked supplied-semantics baseline | `rule kLt(I1:Int, I2:Int) => I1 <Int I2` |
| 242 | `reference-semantics/semantics/concrete.k:53` | rule | — | integrity-checked supplied-semantics baseline | `rule kLt(F1:Float, F2:Float) => F1 <Float F2` |
| 243 | `reference-semantics/semantics/concrete.k:54` | rule | — | integrity-checked supplied-semantics baseline | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 244 | `reference-semantics/semantics/concrete.k:56` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 245 | `reference-semantics/semantics/concrete.k:57` | rule | — | integrity-checked supplied-semantics baseline | `rule unpairVS(.ValSeq) => .ValSeq` |
| 246 | `reference-semantics/semantics/concrete.k:58` | rule | — | integrity-checked supplied-semantics baseline | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 247 | `reference-semantics/semantics/concrete.k:59` | rule | owise | integrity-checked supplied-semantics baseline | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| 248 | `reference-semantics/semantics/controls.k:9` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k>` |
| 249 | `reference-semantics/semantics/controls.k:12` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>` |
| 250 | `reference-semantics/semantics/controls.k:20` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>` |
| 251 | `reference-semantics/semantics/controls.k:27` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>` |
| 252 | `reference-semantics/semantics/controls.k:35` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 253 | `reference-semantics/semantics/controls.k:36` | rule | owise | integrity-checked supplied-semantics baseline | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 254 | `reference-semantics/semantics/controls.k:37` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #bindImports(ParamNames)` |
| 255 | `reference-semantics/semantics/controls.k:38` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 256 | `reference-semantics/semantics/controls.k:39` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>` |
| 257 | `reference-semantics/semantics/controls.k:43` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>` |
| 258 | `reference-semantics/semantics/controls.k:48` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Expr(_:Val) => .K ... </k>` |
| 259 | `reference-semantics/semantics/controls.k:51` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 260 | `reference-semantics/semantics/controls.k:52` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 261 | `reference-semantics/semantics/controls.k:53` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>` |
| 262 | `reference-semantics/semantics/controls.k:54` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| 263 | `reference-semantics/semantics/controls.k:57` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>` |
| 264 | `reference-semantics/semantics/controls.k:59` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>` |
| 265 | `reference-semantics/semantics/controls.k:65` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts)` |
| 266 | `reference-semantics/semantics/controls.k:69` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 267 | `reference-semantics/semantics/controls.k:71` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 268 | `reference-semantics/semantics/controls.k:72` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 269 | `reference-semantics/semantics/controls.k:73` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)` |
| 270 | `reference-semantics/semantics/controls.k:77` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 271 | `reference-semantics/semantics/controls.k:78` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 272 | `reference-semantics/semantics/controls.k:79` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>` |
| 273 | `reference-semantics/semantics/controls.k:81` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>` |
| 274 | `reference-semantics/semantics/controls.k:85` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 275 | `reference-semantics/semantics/controls.k:86` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Continue => #cont ... </k>` |
| 276 | `reference-semantics/semantics/controls.k:87` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Break => #brk ... </k>` |
| 277 | `reference-semantics/semantics/controls.k:88` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 278 | `reference-semantics/semantics/controls.k:89` | rule | owise | integrity-checked supplied-semantics baseline | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 279 | `reference-semantics/semantics/controls.k:90` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 280 | `reference-semantics/semantics/controls.k:91` | rule | owise | integrity-checked supplied-semantics baseline | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| 281 | `reference-semantics/semantics/controls.k:95` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>` |
| 282 | `reference-semantics/semantics/controls.k:98` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>` |
| 283 | `reference-semantics/semantics/controls.k:101` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>` |
| 284 | `reference-semantics/semantics/controls.k:106` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>` |
| 285 | `reference-semantics/semantics/core.k:13` | syntax | — | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 286 | `reference-semantics/semantics/core.k:14` | syntax | — | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 287 | `reference-semantics/semantics/core.k:15` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Str ::= str(IntSeq)` |
| 288 | `reference-semantics/semantics/core.k:18` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Iterable ::= list(ValSeq)` |
| 289 | `reference-semantics/semantics/core.k:25` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Val ::= Int` |
| 290 | `reference-semantics/semantics/core.k:36` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Parent ::= "root" \| parent(Int)` |
| 291 | `reference-semantics/semantics/core.k:37` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Scope ::= scope(Map, Parent)` |
| 292 | `reference-semantics/semantics/core.k:38` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KResult ::= Val` |
| 293 | `reference-semantics/semantics/core.k:39` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Expr ::= Val // cooling puts results back into expression holes` |
| 294 | `reference-semantics/semantics/core.k:40` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Vals ::= List{Val, ","}` |
| 295 | `reference-semantics/semantics/core.k:41` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Exc ::= "NoExc" \| "AssertionError"` |
| 296 | `reference-semantics/semantics/core.k:42` | syntax | — | integrity-checked supplied-semantics baseline | `syntax RetState ::= "noRet" \| retV(Val)` |
| 297 | `reference-semantics/semantics/core.k:49` | configuration | — | integrity-checked supplied-semantics baseline | `configuration` |
| 298 | `reference-semantics/semantics/core.k:68` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= isRefV(Val) [function, total]` |
| 299 | `reference-semantics/semantics/core.k:69` | rule | — | integrity-checked supplied-semantics baseline | `rule isRefV(ref(_:Int)) => true` |
| 300 | `reference-semantics/semantics/core.k:70` | rule | owise | integrity-checked supplied-semantics baseline | `rule isRefV(_:Val) => false [owise]` |
| 301 | `reference-semantics/semantics/core.k:75` | syntax | — | integrity-checked supplied-semantics baseline | `syntax HeapVal ::= cellV(Val)` |
| 302 | `reference-semantics/semantics/core.k:76` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 303 | `reference-semantics/semantics/core.k:77` | rule | — | integrity-checked supplied-semantics baseline | `rule isCellRef(cellRef(_:Int)) => true` |
| 304 | `reference-semantics/semantics/core.k:78` | rule | owise | integrity-checked supplied-semantics baseline | `rule isCellRef(_:Val) => false [owise]` |
| 305 | `reference-semantics/semantics/core.k:85` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> cellRef(H:Int) => V ... </k>` |
| 306 | `reference-semantics/semantics/core.k:95` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Val ::= kwV(String, Val)` |
| 307 | `reference-semantics/semantics/core.k:96` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #kwTag(String)` |
| 308 | `reference-semantics/semantics/core.k:97` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 309 | `reference-semantics/semantics/core.k:98` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>` |
| 310 | `reference-semantics/semantics/core.k:100` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= isKwV(Val) [function, total]` |
| 311 | `reference-semantics/semantics/core.k:101` | rule | — | integrity-checked supplied-semantics baseline | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 312 | `reference-semantics/semantics/core.k:102` | rule | owise | integrity-checked supplied-semantics baseline | `rule isKwV(_:Val) => false [owise]` |
| 313 | `reference-semantics/semantics/core.k:106` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Val ::= cellsMark(ParamNames)` |
| 314 | `reference-semantics/semantics/core.k:107` | syntax | function | integrity-checked supplied-semantics baseline | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 315 | `reference-semantics/semantics/core.k:108` | rule | — | integrity-checked supplied-semantics baseline | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 316 | `reference-semantics/semantics/core.k:109` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 317 | `reference-semantics/semantics/core.k:110` | rule | — | integrity-checked supplied-semantics baseline | `rule pnMember(_:String, .ParamNames) => false` |
| 318 | `reference-semantics/semantics/core.k:111` | rule | — | integrity-checked supplied-semantics baseline | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 319 | `reference-semantics/semantics/core.k:113` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #cellW(Val, Val)` |
| 320 | `reference-semantics/semantics/core.k:114` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>` |
| 321 | `reference-semantics/semantics/core.k:117` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #alloc(Val)` |
| 322 | `reference-semantics/semantics/core.k:118` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #alloc(V:Val) => ref(N) ... </k>` |
| 323 | `reference-semantics/semantics/core.k:124` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #loadAll(Module)` |
| 324 | `reference-semantics/semantics/core.k:125` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 325 | `reference-semantics/semantics/core.k:126` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 326 | `reference-semantics/semantics/core.k:127` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> .Stmts => .K ... </k>` |
| 327 | `reference-semantics/semantics/core.k:130` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #look(String, Int)` |
| 328 | `reference-semantics/semantics/core.k:131` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 329 | `reference-semantics/semantics/core.k:132` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>` |
| 330 | `reference-semantics/semantics/core.k:145` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #look(X:String, L:Int) => V ... </k>` |
| 331 | `reference-semantics/semantics/core.k:152` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>` |
| 332 | `reference-semantics/semantics/core.k:157` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Scope ::= "builtinsScope" [function, total]` |
| 333 | `reference-semantics/semantics/core.k:158` | rule | — | integrity-checked supplied-semantics baseline | `rule builtinsScope` |
| 334 | `reference-semantics/semantics/core.k:185` | syntax | — | integrity-checked supplied-semantics baseline | `syntax ApplyK ::= toCall(Val)` |
| 335 | `reference-semantics/semantics/core.k:186` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK)` |
| 336 | `reference-semantics/semantics/core.k:189` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 337 | `reference-semantics/semantics/core.k:190` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 338 | `reference-semantics/semantics/core.k:191` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| 339 | `reference-semantics/semantics/core.k:194` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Int(I:Int) => I ... </k>` |
| 340 | `reference-semantics/semantics/core.k:195` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Bool(B:Bool) => B ... </k>` |
| 341 | `reference-semantics/semantics/core.k:196` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> NoneVal => noneV ... </k>` |
| 342 | `reference-semantics/semantics/core.k:199` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Bool ::= truthy(Val) [function]` |
| 343 | `reference-semantics/semantics/core.k:200` | rule | — | integrity-checked supplied-semantics baseline | `rule truthy(B:Bool) => B` |
| 344 | `reference-semantics/semantics/core.k:201` | rule | — | integrity-checked supplied-semantics baseline | `rule truthy(noneV) => false` |
| 345 | `reference-semantics/semantics/core.k:202` | rule | — | integrity-checked supplied-semantics baseline | `rule truthy(I:Int) => I =/=Int 0` |
| 346 | `reference-semantics/semantics/core.k:203` | rule | — | integrity-checked supplied-semantics baseline | `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)` |
| 347 | `reference-semantics/semantics/core.k:204` | rule | — | integrity-checked supplied-semantics baseline | `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 348 | `reference-semantics/semantics/core.k:205` | rule | — | integrity-checked supplied-semantics baseline | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 349 | `reference-semantics/semantics/core.k:208` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Val ::= applyUn(String, Val) [function]` |
| 350 | `reference-semantics/semantics/core.k:209` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Val ::= applyBin(String, Val, Val) [function]` |
| 351 | `reference-semantics/semantics/core.k:210` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| 352 | `reference-semantics/semantics/core.k:213` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 353 | `reference-semantics/semantics/core.k:214` | rule | — | integrity-checked supplied-semantics baseline | `rule appendVal(.Vals, V:Val) => V , .Vals` |
| 354 | `reference-semantics/semantics/core.k:215` | rule | — | integrity-checked supplied-semantics baseline | `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)` |
| 355 | `reference-semantics/semantics/core.k:217` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 356 | `reference-semantics/semantics/core.k:218` | rule | — | integrity-checked supplied-semantics baseline | `rule vals2valSeq(.Vals) => .ValSeq` |
| 357 | `reference-semantics/semantics/core.k:219` | rule | — | integrity-checked supplied-semantics baseline | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| 358 | `reference-semantics/semantics/core.k:223` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 359 | `reference-semantics/semantics/core.k:224` | rule | — | integrity-checked supplied-semantics baseline | `rule vsLen(.ValSeq) => 0` |
| 360 | `reference-semantics/semantics/core.k:225` | rule | — | integrity-checked supplied-semantics baseline | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 361 | `reference-semantics/semantics/core.k:227` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 362 | `reference-semantics/semantics/core.k:228` | rule | — | integrity-checked supplied-semantics baseline | `rule isLen(.IntSeq) => 0` |
| 363 | `reference-semantics/semantics/core.k:229` | rule | — | integrity-checked supplied-semantics baseline | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| 364 | `reference-semantics/semantics/core.k:233` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 365 | `reference-semantics/semantics/core.k:234` | rule | — | integrity-checked supplied-semantics baseline | `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq` |
| 366 | `reference-semantics/semantics/core.k:235` | rule | — | integrity-checked supplied-semantics baseline | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)` |
| 367 | `reference-semantics/semantics/core.k:236` | rule | — | integrity-checked supplied-semantics baseline | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))` |
| 368 | `reference-semantics/semantics/core.k:238` | rule | — | integrity-checked supplied-semantics baseline | `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS` |
| 369 | `reference-semantics/semantics/dict.k:20` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| 370 | `reference-semantics/semantics/dict.k:23` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)` |
| 371 | `reference-semantics/semantics/dict.k:26` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 372 | `reference-semantics/semantics/dict.k:27` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 373 | `reference-semantics/semantics/dict.k:28` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)` |
| 374 | `reference-semantics/semantics/dict.k:30` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)` |
| 375 | `reference-semantics/semantics/dict.k:32` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)` |
| 376 | `reference-semantics/semantics/dict.k:37` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 377 | `reference-semantics/semantics/dict.k:38` | rule | — | integrity-checked supplied-semantics baseline | `rule dHasKey(.ValSeq, _:Val) => false` |
| 378 | `reference-semantics/semantics/dict.k:39` | rule | — | integrity-checked supplied-semantics baseline | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K` |
| 379 | `reference-semantics/semantics/dict.k:40` | rule | — | integrity-checked supplied-semantics baseline | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| 380 | `reference-semantics/semantics/dict.k:43` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 381 | `reference-semantics/semantics/dict.k:44` | rule | — | integrity-checked supplied-semantics baseline | `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)` |
| 382 | `reference-semantics/semantics/dict.k:45` | rule | — | integrity-checked supplied-semantics baseline | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| 383 | `reference-semantics/semantics/dict.k:49` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 384 | `reference-semantics/semantics/dict.k:50` | rule | — | integrity-checked supplied-semantics baseline | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR)` |
| 385 | `reference-semantics/semantics/dict.k:52` | rule | — | integrity-checked supplied-semantics baseline | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))` |
| 386 | `reference-semantics/semantics/dict.k:54` | rule | owise | integrity-checked supplied-semantics baseline | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| 387 | `reference-semantics/semantics/dict.k:58` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)` |
| 388 | `reference-semantics/semantics/dict.k:63` | rule | — | integrity-checked supplied-semantics baseline | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 389 | `reference-semantics/semantics/dict.k:64` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 390 | `reference-semantics/semantics/dict.k:65` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>` |
| 391 | `reference-semantics/semantics/dict.k:70` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 392 | `reference-semantics/semantics/dict.k:71` | rule | — | integrity-checked supplied-semantics baseline | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| 393 | `reference-semantics/semantics/dict.k:76` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #dsetK(String, Val)` |
| 394 | `reference-semantics/semantics/dict.k:77` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 395 | `reference-semantics/semantics/dict.k:78` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>` |
| 396 | `reference-semantics/semantics/dict.k:82` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>` |
| 397 | `reference-semantics/semantics/dict.k:86` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 398 | `reference-semantics/semantics/dict.k:87` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>` |
| 399 | `reference-semantics/semantics/dict.k:90` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 400 | `reference-semantics/semantics/dict.k:91` | rule | — | integrity-checked supplied-semantics baseline | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 401 | `reference-semantics/semantics/dict.k:92` | rule | — | integrity-checked supplied-semantics baseline | `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0` |
| 402 | `reference-semantics/semantics/dict.k:95` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))` |
| 403 | `reference-semantics/semantics/dict.k:97` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 404 | `reference-semantics/semantics/dict.k:98` | rule | — | integrity-checked supplied-semantics baseline | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 405 | `reference-semantics/semantics/dict.k:99` | rule | — | integrity-checked supplied-semantics baseline | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)` |
| 406 | `reference-semantics/semantics/dict.k:101` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 407 | `reference-semantics/semantics/dict.k:102` | rule | — | integrity-checked supplied-semantics baseline | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K` |
| 408 | `reference-semantics/semantics/dict.k:103` | rule | — | integrity-checked supplied-semantics baseline | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| 409 | `reference-semantics/semantics/float.k:20` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Val ::= Float` |
| 410 | `reference-semantics/semantics/float.k:21` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Float(F:Float) => F ... </k>` |
| 411 | `reference-semantics/semantics/float.k:24` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 412 | `reference-semantics/semantics/float.k:25` | rule | concrete | integrity-checked supplied-semantics baseline | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 413 | `reference-semantics/semantics/float.k:27` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| 414 | `reference-semantics/semantics/float.k:30` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 415 | `reference-semantics/semantics/float.k:31` | rule | concrete | integrity-checked supplied-semantics baseline | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 416 | `reference-semantics/semantics/float.k:32` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| 417 | `reference-semantics/semantics/float.k:37` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 418 | `reference-semantics/semantics/float.k:38` | rule | concrete | integrity-checked supplied-semantics baseline | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 419 | `reference-semantics/semantics/float.k:39` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| 420 | `reference-semantics/semantics/float.k:43` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 421 | `reference-semantics/semantics/float.k:44` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| 422 | `reference-semantics/semantics/float.k:50` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 423 | `reference-semantics/semantics/float.k:51` | rule | concrete | integrity-checked supplied-semantics baseline | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 424 | `reference-semantics/semantics/float.k:52` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 425 | `reference-semantics/semantics/float.k:54` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 426 | `reference-semantics/semantics/float.k:55` | rule | concrete | integrity-checked supplied-semantics baseline | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 427 | `reference-semantics/semantics/float.k:56` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| 428 | `reference-semantics/semantics/float.k:61` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Import(_:String) => .K ... </k>` |
| 429 | `reference-semantics/semantics/float.k:65` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= "#mathCeil"` |
| 430 | `reference-semantics/semantics/float.k:66` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 431 | `reference-semantics/semantics/float.k:67` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| 432 | `reference-semantics/semantics/float.k:70` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= "#mathFloor"` |
| 433 | `reference-semantics/semantics/float.k:71` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 434 | `reference-semantics/semantics/float.k:72` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 435 | `reference-semantics/semantics/float.k:73` | syntax | function, total, symbol | integrity-checked supplied-semantics baseline | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 436 | `reference-semantics/semantics/float.k:74` | rule | concrete | integrity-checked supplied-semantics baseline | `rule floorFI(I:Int) => I [concrete]` |
| 437 | `reference-semantics/semantics/float.k:75` | rule | concrete | integrity-checked supplied-semantics baseline | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| 438 | `reference-semantics/semantics/float.k:78` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 439 | `reference-semantics/semantics/float.k:79` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V)` |
| 440 | `reference-semantics/semantics/float.k:82` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 441 | `reference-semantics/semantics/float.k:83` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 442 | `reference-semantics/semantics/float.k:84` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 443 | `reference-semantics/semantics/float.k:85` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 444 | `reference-semantics/semantics/float.k:86` | syntax | function, total, symbol | integrity-checked supplied-semantics baseline | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 445 | `reference-semantics/semantics/float.k:87` | rule | concrete | integrity-checked supplied-semantics baseline | `rule toF(F:Float) => F [concrete]` |
| 446 | `reference-semantics/semantics/float.k:88` | rule | concrete | integrity-checked supplied-semantics baseline | `rule toF(I:Int) => intToF(I) [concrete]` |
| 447 | `reference-semantics/semantics/float.k:93` | syntax | function, total, symbol | integrity-checked supplied-semantics baseline | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 448 | `reference-semantics/semantics/float.k:94` | rule | concrete | integrity-checked supplied-semantics baseline | `rule ceilF(I:Int) => I [concrete]` |
| 449 | `reference-semantics/semantics/float.k:95` | rule | concrete | integrity-checked supplied-semantics baseline | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| 450 | `reference-semantics/semantics/float.k:99` | rule | — | integrity-checked supplied-semantics baseline | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| 451 | `reference-semantics/semantics/float.k:103` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 452 | `reference-semantics/semantics/float.k:104` | rule | concrete | integrity-checked supplied-semantics baseline | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 453 | `reference-semantics/semantics/float.k:105` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 454 | `reference-semantics/semantics/float.k:107` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 455 | `reference-semantics/semantics/float.k:108` | rule | concrete | integrity-checked supplied-semantics baseline | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 456 | `reference-semantics/semantics/float.k:109` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 457 | `reference-semantics/semantics/float.k:111` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 458 | `reference-semantics/semantics/float.k:112` | rule | concrete | integrity-checked supplied-semantics baseline | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 459 | `reference-semantics/semantics/float.k:113` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 460 | `reference-semantics/semantics/float.k:115` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 461 | `reference-semantics/semantics/float.k:116` | rule | concrete | integrity-checked supplied-semantics baseline | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 462 | `reference-semantics/semantics/float.k:117` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 463 | `reference-semantics/semantics/float.k:119` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 464 | `reference-semantics/semantics/float.k:120` | rule | concrete | integrity-checked supplied-semantics baseline | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 465 | `reference-semantics/semantics/float.k:121` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| 466 | `reference-semantics/semantics/float.k:125` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 467 | `reference-semantics/semantics/float.k:126` | rule | concrete | integrity-checked supplied-semantics baseline | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 468 | `reference-semantics/semantics/float.k:127` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)` |
| 469 | `reference-semantics/semantics/float.k:128` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 470 | `reference-semantics/semantics/float.k:129` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| 471 | `reference-semantics/semantics/float.k:132` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 472 | `reference-semantics/semantics/float.k:133` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 473 | `reference-semantics/semantics/float.k:134` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 474 | `reference-semantics/semantics/float.k:135` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 475 | `reference-semantics/semantics/float.k:136` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 476 | `reference-semantics/semantics/float.k:137` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 477 | `reference-semantics/semantics/float.k:138` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 478 | `reference-semantics/semantics/float.k:139` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 479 | `reference-semantics/semantics/float.k:142` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 480 | `reference-semantics/semantics/float.k:143` | rule | concrete | integrity-checked supplied-semantics baseline | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 481 | `reference-semantics/semantics/float.k:144` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 482 | `reference-semantics/semantics/float.k:145` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 483 | `reference-semantics/semantics/float.k:146` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 484 | `reference-semantics/semantics/float.k:147` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 485 | `reference-semantics/semantics/float.k:148` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 486 | `reference-semantics/semantics/float.k:149` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 487 | `reference-semantics/semantics/float.k:150` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 488 | `reference-semantics/semantics/float.k:151` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| 489 | `reference-semantics/semantics/float.k:154` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 490 | `reference-semantics/semantics/float.k:155` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| 491 | `reference-semantics/semantics/float.k:160` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 492 | `reference-semantics/semantics/float.k:161` | rule | concrete | integrity-checked supplied-semantics baseline | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 493 | `reference-semantics/semantics/float.k:162` | rule | concrete | integrity-checked supplied-semantics baseline | `rule decStrToF(CS:IntSeq)` |
| 494 | `reference-semantics/semantics/float.k:165` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= headIS(IntSeq) [function]` |
| 495 | `reference-semantics/semantics/float.k:166` | rule | — | integrity-checked supplied-semantics baseline | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 496 | `reference-semantics/semantics/float.k:167` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 497 | `reference-semantics/semantics/float.k:168` | rule | — | integrity-checked supplied-semantics baseline | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 498 | `reference-semantics/semantics/float.k:169` | rule | — | integrity-checked supplied-semantics baseline | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 499 | `reference-semantics/semantics/float.k:170` | rule | — | integrity-checked supplied-semantics baseline | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 500 | `reference-semantics/semantics/float.k:171` | rule | — | integrity-checked supplied-semantics baseline | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))` |
| 501 | `reference-semantics/semantics/float.k:173` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 502 | `reference-semantics/semantics/float.k:174` | rule | — | integrity-checked supplied-semantics baseline | `rule fracPart(.IntSeq) => 0` |
| 503 | `reference-semantics/semantics/float.k:175` | rule | — | integrity-checked supplied-semantics baseline | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 504 | `reference-semantics/semantics/float.k:176` | rule | — | integrity-checked supplied-semantics baseline | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 505 | `reference-semantics/semantics/float.k:177` | rule | — | integrity-checked supplied-semantics baseline | `rule fracAcc(.IntSeq, A:Int) => A` |
| 506 | `reference-semantics/semantics/float.k:178` | rule | — | integrity-checked supplied-semantics baseline | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 507 | `reference-semantics/semantics/float.k:179` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 508 | `reference-semantics/semantics/float.k:180` | rule | — | integrity-checked supplied-semantics baseline | `rule fracScale(.IntSeq) => 1` |
| 509 | `reference-semantics/semantics/float.k:181` | rule | — | integrity-checked supplied-semantics baseline | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 510 | `reference-semantics/semantics/float.k:182` | rule | — | integrity-checked supplied-semantics baseline | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 511 | `reference-semantics/semantics/float.k:183` | rule | — | integrity-checked supplied-semantics baseline | `rule fscAcc(.IntSeq, A:Int) => A` |
| 512 | `reference-semantics/semantics/float.k:184` | rule | — | integrity-checked supplied-semantics baseline | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 513 | `reference-semantics/semantics/float.k:185` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 514 | `reference-semantics/semantics/float.k:186` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 515 | `reference-semantics/semantics/float.k:187` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| 516 | `reference-semantics/semantics/float.k:190` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 517 | `reference-semantics/semantics/float.k:191` | rule | concrete | integrity-checked supplied-semantics baseline | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 518 | `reference-semantics/semantics/float.k:192` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| 519 | `reference-semantics/semantics/float.k:195` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 520 | `reference-semantics/semantics/float.k:196` | rule | concrete | integrity-checked supplied-semantics baseline | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 521 | `reference-semantics/semantics/float.k:197` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 522 | `reference-semantics/semantics/float.k:198` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 523 | `reference-semantics/semantics/float.k:199` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 524 | `reference-semantics/semantics/float.k:200` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 525 | `reference-semantics/semantics/float.k:201` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 526 | `reference-semantics/semantics/float.k:202` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 527 | `reference-semantics/semantics/float.k:203` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 528 | `reference-semantics/semantics/float.k:204` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 529 | `reference-semantics/semantics/float.k:205` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 530 | `reference-semantics/semantics/float.k:206` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| 531 | `reference-semantics/semantics/float.k:209` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 532 | `reference-semantics/semantics/float.k:210` | rule | concrete | integrity-checked supplied-semantics baseline | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 533 | `reference-semantics/semantics/float.k:211` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 534 | `reference-semantics/semantics/float.k:213` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 535 | `reference-semantics/semantics/float.k:214` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| 536 | `reference-semantics/semantics/float.k:217` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 537 | `reference-semantics/semantics/float.k:218` | rule | concrete | integrity-checked supplied-semantics baseline | `rule roundF(F:Float)` |
| 538 | `reference-semantics/semantics/float.k:223` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 539 | `reference-semantics/semantics/float.k:224` | rule | concrete | integrity-checked supplied-semantics baseline | `rule roundFN(F:Float, N:Int)` |
| 540 | `reference-semantics/semantics/float.k:227` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)` |
| 541 | `reference-semantics/semantics/float.k:228` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 542 | `reference-semantics/semantics/float.k:230` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 543 | `reference-semantics/semantics/float.k:231` | rule | concrete | integrity-checked supplied-semantics baseline | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 544 | `reference-semantics/semantics/float.k:232` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= "#mathSqrt"` |
| 545 | `reference-semantics/semantics/float.k:233` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 546 | `reference-semantics/semantics/float.k:234` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 547 | `reference-semantics/semantics/float.k:235` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| 548 | `reference-semantics/semantics/float.k:243` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 549 | `reference-semantics/semantics/float.k:244` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 550 | `reference-semantics/semantics/float.k:245` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 551 | `reference-semantics/semantics/float.k:246` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 552 | `reference-semantics/semantics/float.k:247` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>` |
| 553 | `reference-semantics/semantics/float.k:250` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 554 | `reference-semantics/semantics/float.k:251` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 555 | `reference-semantics/semantics/float.k:252` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 556 | `reference-semantics/semantics/float.k:253` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 557 | `reference-semantics/semantics/float.k:254` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>` |
| 558 | `reference-semantics/semantics/float.k:261` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 559 | `reference-semantics/semantics/float.k:262` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)` |
| 560 | `reference-semantics/semantics/float.k:265` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 561 | `reference-semantics/semantics/float.k:266` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 562 | `reference-semantics/semantics/float.k:267` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)` |
| 563 | `reference-semantics/semantics/float.k:270` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)` |
| 564 | `reference-semantics/semantics/functions.k:8` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)` |
| 565 | `reference-semantics/semantics/functions.k:14` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>` |
| 566 | `reference-semantics/semantics/functions.k:18` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 567 | `reference-semantics/semantics/functions.k:19` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>` |
| 568 | `reference-semantics/semantics/functions.k:27` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| 569 | `reference-semantics/semantics/functions.k:31` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 570 | `reference-semantics/semantics/functions.k:33` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),` |
| 571 | `reference-semantics/semantics/functions.k:36` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,` |
| 572 | `reference-semantics/semantics/functions.k:42` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,` |
| 573 | `reference-semantics/semantics/functions.k:47` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr)` |
| 574 | `reference-semantics/semantics/functions.k:50` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),` |
| 575 | `reference-semantics/semantics/functions.k:53` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,` |
| 576 | `reference-semantics/semantics/functions.k:59` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)` |
| 577 | `reference-semantics/semantics/functions.k:63` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 578 | `reference-semantics/semantics/functions.k:64` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>` |
| 579 | `reference-semantics/semantics/functions.k:68` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))` |
| 580 | `reference-semantics/semantics/functions.k:78` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Return(V:Val) ~> _ => #pop </k>` |
| 581 | `reference-semantics/semantics/functions.k:80` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #endcall => #pop ... </k>` |
| 582 | `reference-semantics/semantics/functions.k:85` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #pop => V ~> CONT </k>` |
| 583 | `reference-semantics/semantics/int.k:7` | rule | — | integrity-checked supplied-semantics baseline | `rule applyUn("-", I:Int) => 0 -Int I` |
| 584 | `reference-semantics/semantics/int.k:9` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2` |
| 585 | `reference-semantics/semantics/int.k:11` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 586 | `reference-semantics/semantics/int.k:12` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 587 | `reference-semantics/semantics/int.k:13` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2` |
| 588 | `reference-semantics/semantics/int.k:14` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2` |
| 589 | `reference-semantics/semantics/int.k:15` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)` |
| 590 | `reference-semantics/semantics/int.k:16` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 591 | `reference-semantics/semantics/int.k:17` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 592 | `reference-semantics/semantics/int.k:19` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= pyMod(Int, Int) [function]` |
| 593 | `reference-semantics/semantics/int.k:20` | rule | — | integrity-checked supplied-semantics baseline | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 594 | `reference-semantics/semantics/int.k:22` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` |
| 595 | `reference-semantics/semantics/int.k:23` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2` |
| 596 | `reference-semantics/semantics/int.k:24` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` |
| 597 | `reference-semantics/semantics/int.k:25` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2` |
| 598 | `reference-semantics/semantics/int.k:26` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2` |
| 599 | `reference-semantics/semantics/int.k:27` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2` |
| 600 | `reference-semantics/semantics/iter.k:8` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| 601 | `reference-semantics/semantics/list.k:9` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>` |
| 602 | `reference-semantics/semantics/list.k:10` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| 603 | `reference-semantics/semantics/list.k:13` | syntax | — | integrity-checked supplied-semantics baseline | `syntax ApplyK ::= "toList"` |
| 604 | `reference-semantics/semantics/list.k:14` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 605 | `reference-semantics/semantics/list.k:15` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| 606 | `reference-semantics/semantics/list.k:18` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 607 | `reference-semantics/semantics/list.k:19` | rule | — | integrity-checked supplied-semantics baseline | `rule valSeqConcat(.ValSeq, T:ValSeq) => T` |
| 608 | `reference-semantics/semantics/list.k:20` | rule | — | integrity-checked supplied-semantics baseline | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| 609 | `reference-semantics/semantics/list.k:24` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>` |
| 610 | `reference-semantics/semantics/list.k:27` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 611 | `reference-semantics/semantics/list.k:28` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| 612 | `reference-semantics/semantics/list.k:33` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 613 | `reference-semantics/semantics/list.k:34` | rule | — | integrity-checked supplied-semantics baseline | `rule hasRefVS(.ValSeq) => false` |
| 614 | `reference-semantics/semantics/list.k:35` | rule | — | integrity-checked supplied-semantics baseline | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 615 | `reference-semantics/semantics/list.k:37` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]` |
| 616 | `reference-semantics/semantics/list.k:39` | rule | — | integrity-checked supplied-semantics baseline | `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true` |
| 617 | `reference-semantics/semantics/list.k:40` | rule | — | integrity-checked supplied-semantics baseline | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false` |
| 618 | `reference-semantics/semantics/list.k:41` | rule | — | integrity-checked supplied-semantics baseline | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false` |
| 619 | `reference-semantics/semantics/list.k:42` | rule | — | integrity-checked supplied-semantics baseline | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)` |
| 620 | `reference-semantics/semantics/list.k:45` | rule | — | integrity-checked supplied-semantics baseline | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)` |
| 621 | `reference-semantics/semantics/list.k:47` | rule | — | integrity-checked supplied-semantics baseline | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)` |
| 622 | `reference-semantics/semantics/list.k:49` | rule | — | integrity-checked supplied-semantics baseline | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 623 | `reference-semantics/semantics/list.k:50` | rule | owise | integrity-checked supplied-semantics baseline | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| 624 | `reference-semantics/semantics/list.k:53` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>` |
| 625 | `reference-semantics/semantics/list.k:58` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 626 | `reference-semantics/semantics/list.k:59` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 627 | `reference-semantics/semantics/list.k:60` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 628 | `reference-semantics/semantics/list.k:61` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 629 | `reference-semantics/semantics/list.k:62` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 630 | `reference-semantics/semantics/list.k:63` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>` |
| 631 | `reference-semantics/semantics/list.k:65` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>` |
| 632 | `reference-semantics/semantics/list.k:67` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| 633 | `reference-semantics/semantics/methods.k:10` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| 634 | `reference-semantics/semantics/methods.k:13` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 635 | `reference-semantics/semantics/methods.k:14` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 636 | `reference-semantics/semantics/methods.k:15` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 637 | `reference-semantics/semantics/methods.k:16` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| 638 | `reference-semantics/semantics/methods.k:19` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))` |
| 639 | `reference-semantics/semantics/methods.k:20` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))` |
| 640 | `reference-semantics/semantics/methods.k:21` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| 641 | `reference-semantics/semantics/methods.k:26` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 642 | `reference-semantics/semantics/methods.k:27` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 643 | `reference-semantics/semantics/methods.k:28` | rule | — | integrity-checked supplied-semantics baseline | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 644 | `reference-semantics/semantics/methods.k:29` | rule | — | integrity-checked supplied-semantics baseline | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 645 | `reference-semantics/semantics/methods.k:30` | rule | — | integrity-checked supplied-semantics baseline | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))` |
| 646 | `reference-semantics/semantics/methods.k:34` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 647 | `reference-semantics/semantics/methods.k:35` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 648 | `reference-semantics/semantics/methods.k:36` | rule | — | integrity-checked supplied-semantics baseline | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 649 | `reference-semantics/semantics/methods.k:37` | rule | — | integrity-checked supplied-semantics baseline | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)` |
| 650 | `reference-semantics/semantics/methods.k:39` | rule | — | integrity-checked supplied-semantics baseline | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)` |
| 651 | `reference-semantics/semantics/methods.k:41` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 652 | `reference-semantics/semantics/methods.k:42` | rule | — | integrity-checked supplied-semantics baseline | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 653 | `reference-semantics/semantics/methods.k:43` | rule | owise | integrity-checked supplied-semantics baseline | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 654 | `reference-semantics/semantics/methods.k:44` | rule | — | integrity-checked supplied-semantics baseline | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| 655 | `reference-semantics/semantics/methods.k:47` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 656 | `reference-semantics/semantics/methods.k:48` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 657 | `reference-semantics/semantics/methods.k:49` | rule | — | integrity-checked supplied-semantics baseline | `rule trimWS(.IntSeq) => .IntSeq` |
| 658 | `reference-semantics/semantics/methods.k:50` | rule | — | integrity-checked supplied-semantics baseline | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 659 | `reference-semantics/semantics/methods.k:51` | rule | — | integrity-checked supplied-semantics baseline | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 660 | `reference-semantics/semantics/methods.k:52` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 661 | `reference-semantics/semantics/methods.k:53` | rule | — | integrity-checked supplied-semantics baseline | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 662 | `reference-semantics/semantics/methods.k:54` | rule | — | integrity-checked supplied-semantics baseline | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 663 | `reference-semantics/semantics/methods.k:55` | rule | — | integrity-checked supplied-semantics baseline | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| 664 | `reference-semantics/semantics/methods.k:58` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| 665 | `reference-semantics/semantics/methods.k:61` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| 666 | `reference-semantics/semantics/methods.k:64` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 667 | `reference-semantics/semantics/methods.k:65` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 668 | `reference-semantics/semantics/methods.k:66` | rule | — | integrity-checked supplied-semantics baseline | `rule cntOccVS(.ValSeq, _:Val) => 0` |
| 669 | `reference-semantics/semantics/methods.k:67` | rule | — | integrity-checked supplied-semantics baseline | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 670 | `reference-semantics/semantics/methods.k:68` | rule | — | integrity-checked supplied-semantics baseline | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V)` |
| 671 | `reference-semantics/semantics/methods.k:72` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)` |
| 672 | `reference-semantics/semantics/methods.k:75` | syntax | function | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result` |
| 673 | `reference-semantics/semantics/methods.k:76` | rule | — | integrity-checked supplied-semantics baseline | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 674 | `reference-semantics/semantics/methods.k:77` | rule | — | integrity-checked supplied-semantics baseline | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))` |
| 675 | `reference-semantics/semantics/methods.k:79` | rule | — | integrity-checked supplied-semantics baseline | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)` |
| 676 | `reference-semantics/semantics/methods.k:82` | syntax | function | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 677 | `reference-semantics/semantics/methods.k:83` | rule | — | integrity-checked supplied-semantics baseline | `rule flushTok(ACC:ValSeq, .IntSeq) => ACC` |
| 678 | `reference-semantics/semantics/methods.k:84` | rule | — | integrity-checked supplied-semantics baseline | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 679 | `reference-semantics/semantics/methods.k:85` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= isWSC(Int) [function, total]` |
| 680 | `reference-semantics/semantics/methods.k:86` | rule | — | integrity-checked supplied-semantics baseline | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| 681 | `reference-semantics/semantics/methods.k:89` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))` |
| 682 | `reference-semantics/semantics/methods.k:94` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))` |
| 683 | `reference-semantics/semantics/methods.k:97` | syntax | function | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token` |
| 684 | `reference-semantics/semantics/methods.k:98` | rule | — | integrity-checked supplied-semantics baseline | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)` |
| 685 | `reference-semantics/semantics/methods.k:99` | rule | — | integrity-checked supplied-semantics baseline | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))` |
| 686 | `reference-semantics/semantics/methods.k:101` | rule | — | integrity-checked supplied-semantics baseline | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))` |
| 687 | `reference-semantics/semantics/methods.k:104` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)` |
| 688 | `reference-semantics/semantics/methods.k:106` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 689 | `reference-semantics/semantics/methods.k:107` | rule | — | integrity-checked supplied-semantics baseline | `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq` |
| 690 | `reference-semantics/semantics/methods.k:108` | rule | — | integrity-checked supplied-semantics baseline | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 691 | `reference-semantics/semantics/methods.k:109` | rule | — | integrity-checked supplied-semantics baseline | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| 692 | `reference-semantics/semantics/methods.k:112` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 693 | `reference-semantics/semantics/methods.k:113` | rule | — | integrity-checked supplied-semantics baseline | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 694 | `reference-semantics/semantics/methods.k:115` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 695 | `reference-semantics/semantics/methods.k:116` | rule | — | integrity-checked supplied-semantics baseline | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 696 | `reference-semantics/semantics/methods.k:118` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 697 | `reference-semantics/semantics/methods.k:119` | rule | — | integrity-checked supplied-semantics baseline | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 698 | `reference-semantics/semantics/methods.k:121` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 699 | `reference-semantics/semantics/methods.k:122` | rule | — | integrity-checked supplied-semantics baseline | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 700 | `reference-semantics/semantics/methods.k:124` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 701 | `reference-semantics/semantics/methods.k:125` | rule | — | integrity-checked supplied-semantics baseline | `rule hasUpper(.IntSeq) => false` |
| 702 | `reference-semantics/semantics/methods.k:126` | rule | — | integrity-checked supplied-semantics baseline | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 703 | `reference-semantics/semantics/methods.k:128` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 704 | `reference-semantics/semantics/methods.k:129` | rule | — | integrity-checked supplied-semantics baseline | `rule hasLower(.IntSeq) => false` |
| 705 | `reference-semantics/semantics/methods.k:130` | rule | — | integrity-checked supplied-semantics baseline | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 706 | `reference-semantics/semantics/methods.k:132` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 707 | `reference-semantics/semantics/methods.k:133` | rule | — | integrity-checked supplied-semantics baseline | `rule allAlpha(.IntSeq) => true` |
| 708 | `reference-semantics/semantics/methods.k:134` | rule | — | integrity-checked supplied-semantics baseline | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 709 | `reference-semantics/semantics/methods.k:136` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 710 | `reference-semantics/semantics/methods.k:137` | rule | — | integrity-checked supplied-semantics baseline | `rule allDigit(.IntSeq) => true` |
| 711 | `reference-semantics/semantics/methods.k:138` | rule | — | integrity-checked supplied-semantics baseline | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 712 | `reference-semantics/semantics/methods.k:140` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= lowerC(Int) [function, total]` |
| 713 | `reference-semantics/semantics/methods.k:142` | rule | — | integrity-checked supplied-semantics baseline | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 714 | `reference-semantics/semantics/methods.k:143` | rule | owise | integrity-checked supplied-semantics baseline | `rule lowerC(C:Int) => C [owise]` |
| 715 | `reference-semantics/semantics/methods.k:145` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= upperC(Int) [function, total]` |
| 716 | `reference-semantics/semantics/methods.k:146` | rule | — | integrity-checked supplied-semantics baseline | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 717 | `reference-semantics/semantics/methods.k:147` | rule | owise | integrity-checked supplied-semantics baseline | `rule upperC(C:Int) => C [owise]` |
| 718 | `reference-semantics/semantics/methods.k:149` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= swapC(Int) [function, total]` |
| 719 | `reference-semantics/semantics/methods.k:150` | rule | — | integrity-checked supplied-semantics baseline | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 720 | `reference-semantics/semantics/methods.k:151` | rule | — | integrity-checked supplied-semantics baseline | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 721 | `reference-semantics/semantics/methods.k:152` | rule | owise | integrity-checked supplied-semantics baseline | `rule swapC(C:Int) => C [owise]` |
| 722 | `reference-semantics/semantics/methods.k:154` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 723 | `reference-semantics/semantics/methods.k:155` | rule | — | integrity-checked supplied-semantics baseline | `rule mapLower(.IntSeq) => .IntSeq` |
| 724 | `reference-semantics/semantics/methods.k:156` | rule | — | integrity-checked supplied-semantics baseline | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 725 | `reference-semantics/semantics/methods.k:158` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 726 | `reference-semantics/semantics/methods.k:159` | rule | — | integrity-checked supplied-semantics baseline | `rule mapUpper(.IntSeq) => .IntSeq` |
| 727 | `reference-semantics/semantics/methods.k:160` | rule | — | integrity-checked supplied-semantics baseline | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 728 | `reference-semantics/semantics/methods.k:162` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 729 | `reference-semantics/semantics/methods.k:163` | rule | — | integrity-checked supplied-semantics baseline | `rule mapSwap(.IntSeq) => .IntSeq` |
| 730 | `reference-semantics/semantics/methods.k:164` | rule | — | integrity-checked supplied-semantics baseline | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 731 | `reference-semantics/semantics/methods.k:166` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 732 | `reference-semantics/semantics/methods.k:167` | rule | — | integrity-checked supplied-semantics baseline | `rule startsWith(.IntSeq, _:IntSeq) => true` |
| 733 | `reference-semantics/semantics/methods.k:168` | rule | — | integrity-checked supplied-semantics baseline | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 734 | `reference-semantics/semantics/methods.k:169` | rule | — | integrity-checked supplied-semantics baseline | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| 735 | `reference-semantics/semantics/operators.k:10` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 736 | `reference-semantics/semantics/operators.k:12` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| 737 | `reference-semantics/semantics/operators.k:15` | context | — | integrity-checked supplied-semantics baseline | `context Compare(HOLE, _)` |
| 738 | `reference-semantics/semantics/operators.k:16` | context | — | integrity-checked supplied-semantics baseline | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 739 | `reference-semantics/semantics/operators.k:17` | rule | owise | integrity-checked supplied-semantics baseline | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 740 | `reference-semantics/semantics/operators.k:19` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("is", V:Val, noneV) => V ==K noneV` |
| 741 | `reference-semantics/semantics/operators.k:20` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| 742 | `reference-semantics/semantics/operators.k:25` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>` |
| 743 | `reference-semantics/semantics/operators.k:28` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>` |
| 744 | `reference-semantics/semantics/operators.k:34` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>` |
| 745 | `reference-semantics/semantics/operators.k:38` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>` |
| 746 | `reference-semantics/semantics/operators.k:44` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>` |
| 747 | `reference-semantics/semantics/range.k:9` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 748 | `reference-semantics/semantics/range.k:10` | rule | — | integrity-checked supplied-semantics baseline | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 749 | `reference-semantics/semantics/range.k:12` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 750 | `reference-semantics/semantics/range.k:13` | rule | — | integrity-checked supplied-semantics baseline | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST` |
| 751 | `reference-semantics/semantics/range.k:15` | rule | — | integrity-checked supplied-semantics baseline | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)` |
| 752 | `reference-semantics/semantics/range.k:17` | rule | — | integrity-checked supplied-semantics baseline | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0` |
| 753 | `reference-semantics/semantics/range.k:20` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))` |
| 754 | `reference-semantics/semantics/range.k:23` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>` |
| 755 | `reference-semantics/semantics/set.k:8` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Val ::= setV(IntSeq)` |
| 756 | `reference-semantics/semantics/set.k:11` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 757 | `reference-semantics/semantics/set.k:12` | rule | — | integrity-checked supplied-semantics baseline | `rule codeIn(_:Int, .IntSeq) => false` |
| 758 | `reference-semantics/semantics/set.k:13` | rule | — | integrity-checked supplied-semantics baseline | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| 759 | `reference-semantics/semantics/set.k:16` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= dedupCodes(IntSeq) [function, total]` |
| 760 | `reference-semantics/semantics/set.k:18` | rule | — | integrity-checked supplied-semantics baseline | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 761 | `reference-semantics/semantics/set.k:19` | rule | — | integrity-checked supplied-semantics baseline | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 762 | `reference-semantics/semantics/set.k:20` | rule | — | integrity-checked supplied-semantics baseline | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)` |
| 763 | `reference-semantics/semantics/set.k:22` | rule | — | integrity-checked supplied-semantics baseline | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))` |
| 764 | `reference-semantics/semantics/set.k:25` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 765 | `reference-semantics/semantics/set.k:26` | rule | — | integrity-checked supplied-semantics baseline | `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)` |
| 766 | `reference-semantics/semantics/set.k:27` | rule | — | integrity-checked supplied-semantics baseline | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| 767 | `reference-semantics/semantics/set.k:31` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 768 | `reference-semantics/semantics/set.k:32` | rule | — | integrity-checked supplied-semantics baseline | `rule subsetCodes(.IntSeq, _:IntSeq) => true` |
| 769 | `reference-semantics/semantics/set.k:33` | rule | — | integrity-checked supplied-semantics baseline | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 770 | `reference-semantics/semantics/set.k:35` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 771 | `reference-semantics/semantics/set.k:36` | rule | — | integrity-checked supplied-semantics baseline | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| 772 | `reference-semantics/semantics/set.k:39` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| 773 | `reference-semantics/semantics/sort.k:18` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 774 | `reference-semantics/semantics/sort.k:19` | syntax | function | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 775 | `reference-semantics/semantics/sort.k:20` | rule | concrete | integrity-checked supplied-semantics baseline | `rule sortVS(.ValSeq) => .ValSeq [concrete]` |
| 776 | `reference-semantics/semantics/sort.k:21` | rule | concrete | integrity-checked supplied-semantics baseline | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 777 | `reference-semantics/semantics/sort.k:22` | rule | concrete | integrity-checked supplied-semantics baseline | `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]` |
| 778 | `reference-semantics/semantics/sort.k:23` | rule | concrete | integrity-checked supplied-semantics baseline | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 779 | `reference-semantics/semantics/sort.k:24` | rule | concrete | integrity-checked supplied-semantics baseline | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete]` |
| 780 | `reference-semantics/semantics/sort.k:26` | syntax | function | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 781 | `reference-semantics/semantics/sort.k:27` | rule | concrete | integrity-checked supplied-semantics baseline | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 782 | `reference-semantics/semantics/sort.k:28` | rule | concrete | integrity-checked supplied-semantics baseline | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 783 | `reference-semantics/semantics/sort.k:29` | rule | concrete | integrity-checked supplied-semantics baseline | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))` |
| 784 | `reference-semantics/semantics/sort.k:31` | rule | concrete | integrity-checked supplied-semantics baseline | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))` |
| 785 | `reference-semantics/semantics/sort.k:36` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))` |
| 786 | `reference-semantics/semantics/sort.k:40` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>` |
| 787 | `reference-semantics/semantics/sort.k:49` | syntax | function, total, symbol, no-evaluators | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 788 | `reference-semantics/semantics/sort.k:51` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= revVS(ValSeq) [function, total]` |
| 789 | `reference-semantics/semantics/sort.k:53` | rule | — | integrity-checked supplied-semantics baseline | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 790 | `reference-semantics/semantics/sort.k:54` | rule | — | integrity-checked supplied-semantics baseline | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 791 | `reference-semantics/semantics/sort.k:55` | rule | — | integrity-checked supplied-semantics baseline | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 792 | `reference-semantics/semantics/sort.k:57` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 793 | `reference-semantics/semantics/sort.k:58` | rule | — | integrity-checked supplied-semantics baseline | `rule condRev(S:ValSeq, false) => S` |
| 794 | `reference-semantics/semantics/sort.k:59` | rule | — | integrity-checked supplied-semantics baseline | `rule condRev(S:ValSeq, true) => revVS(S)` |
| 795 | `reference-semantics/semantics/sort.k:61` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))` |
| 796 | `reference-semantics/semantics/sort.k:63` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))` |
| 797 | `reference-semantics/semantics/sort.k:65` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))` |
| 798 | `reference-semantics/semantics/str.k:8` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>` |
| 799 | `reference-semantics/semantics/str.k:9` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))` |
| 800 | `reference-semantics/semantics/str.k:13` | syntax | function | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= strToCodes(String) [function]` |
| 801 | `reference-semantics/semantics/str.k:14` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 802 | `reference-semantics/semantics/str.k:15` | rule | — | integrity-checked supplied-semantics baseline | `rule strToCodes("") => .IntSeq` |
| 803 | `reference-semantics/semantics/str.k:16` | rule | — | integrity-checked supplied-semantics baseline | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))` |
| 804 | `reference-semantics/semantics/str.k:20` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 805 | `reference-semantics/semantics/str.k:21` | rule | — | integrity-checked supplied-semantics baseline | `rule seqConcat(.IntSeq, T:IntSeq) => T` |
| 806 | `reference-semantics/semantics/str.k:22` | rule | — | integrity-checked supplied-semantics baseline | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 807 | `reference-semantics/semantics/str.k:24` | rule | — | integrity-checked supplied-semantics baseline | `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 808 | `reference-semantics/semantics/str.k:25` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 809 | `reference-semantics/semantics/str.k:26` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| 810 | `reference-semantics/semantics/str.k:29` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 811 | `reference-semantics/semantics/str.k:30` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 812 | `reference-semantics/semantics/str.k:32` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 813 | `reference-semantics/semantics/str.k:33` | rule | — | integrity-checked supplied-semantics baseline | `rule strPrefix(.IntSeq, _:IntSeq) => true` |
| 814 | `reference-semantics/semantics/str.k:34` | rule | — | integrity-checked supplied-semantics baseline | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 815 | `reference-semantics/semantics/str.k:35` | rule | — | integrity-checked supplied-semantics baseline | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 816 | `reference-semantics/semantics/str.k:37` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 817 | `reference-semantics/semantics/str.k:38` | rule | — | integrity-checked supplied-semantics baseline | `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)` |
| 818 | `reference-semantics/semantics/str.k:39` | rule | — | integrity-checked supplied-semantics baseline | `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)` |
| 819 | `reference-semantics/semantics/str.k:40` | rule | — | integrity-checked supplied-semantics baseline | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)` |
| 820 | `reference-semantics/semantics/str.k:48` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 821 | `reference-semantics/semantics/str.k:49` | rule | — | integrity-checked supplied-semantics baseline | `rule strLt(.IntSeq, .IntSeq) => false` |
| 822 | `reference-semantics/semantics/str.k:50` | rule | — | integrity-checked supplied-semantics baseline | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 823 | `reference-semantics/semantics/str.k:51` | rule | — | integrity-checked supplied-semantics baseline | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 824 | `reference-semantics/semantics/str.k:52` | rule | — | integrity-checked supplied-semantics baseline | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B` |
| 825 | `reference-semantics/semantics/str.k:53` | rule | — | integrity-checked supplied-semantics baseline | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B` |
| 826 | `reference-semantics/semantics/str.k:54` | rule | — | integrity-checked supplied-semantics baseline | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 827 | `reference-semantics/semantics/str.k:56` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 828 | `reference-semantics/semantics/str.k:57` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 829 | `reference-semantics/semantics/str.k:58` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 830 | `reference-semantics/semantics/str.k:59` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| 831 | `reference-semantics/semantics/subscript.k:11` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 832 | `reference-semantics/semantics/subscript.k:12` | rule | — | integrity-checked supplied-semantics baseline | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V` |
| 833 | `reference-semantics/semantics/subscript.k:13` | rule | — | integrity-checked supplied-semantics baseline | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)` |
| 834 | `reference-semantics/semantics/subscript.k:16` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 835 | `reference-semantics/semantics/subscript.k:17` | rule | — | integrity-checked supplied-semantics baseline | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C` |
| 836 | `reference-semantics/semantics/subscript.k:18` | rule | — | integrity-checked supplied-semantics baseline | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)` |
| 837 | `reference-semantics/semantics/subscript.k:21` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 838 | `reference-semantics/semantics/subscript.k:22` | rule | — | integrity-checked supplied-semantics baseline | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 839 | `reference-semantics/semantics/subscript.k:23` | rule | — | integrity-checked supplied-semantics baseline | `rule normIdx(I:Int, _:Int) => I requires I >=Int 0` |
| 840 | `reference-semantics/semantics/subscript.k:27` | context | — | integrity-checked supplied-semantics baseline | `context Subscript(HOLE, _)` |
| 841 | `reference-semantics/semantics/subscript.k:28` | context | — | integrity-checked supplied-semantics baseline | `context Subscript(_:Val, HOLE:Expr)` |
| 842 | `reference-semantics/semantics/subscript.k:31` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>` |
| 843 | `reference-semantics/semantics/subscript.k:35` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 844 | `reference-semantics/semantics/subscript.k:37` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 845 | `reference-semantics/semantics/subscript.k:38` | rule | — | integrity-checked supplied-semantics baseline | `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 846 | `reference-semantics/semantics/subscript.k:39` | rule | — | integrity-checked supplied-semantics baseline | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 847 | `reference-semantics/semantics/subscript.k:40` | rule | — | integrity-checked supplied-semantics baseline | `rule applyIndex(str(IS:IntSeq), I:Int)` |
| 848 | `reference-semantics/semantics/subscript.k:44` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #evalB(Bound) \| "#toSome"` |
| 849 | `reference-semantics/semantics/subscript.k:49` | syntax | — | integrity-checked supplied-semantics baseline | `syntax OptInt ::= "noB" \| someB(Int)` |
| 850 | `reference-semantics/semantics/subscript.k:50` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #evalB(NoBound) => noB ... </k>` |
| 851 | `reference-semantics/semantics/subscript.k:51` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>` |
| 852 | `reference-semantics/semantics/subscript.k:52` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 853 | `reference-semantics/semantics/subscript.k:54` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 854 | `reference-semantics/semantics/subscript.k:55` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 855 | `reference-semantics/semantics/subscript.k:56` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| 856 | `reference-semantics/semantics/subscript.k:58` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)` |
| 857 | `reference-semantics/semantics/subscript.k:61` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 858 | `reference-semantics/semantics/subscript.k:63` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 859 | `reference-semantics/semantics/subscript.k:64` | rule | — | integrity-checked supplied-semantics baseline | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)` |
| 860 | `reference-semantics/semantics/subscript.k:66` | rule | — | integrity-checked supplied-semantics baseline | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)` |
| 861 | `reference-semantics/semantics/subscript.k:68` | rule | — | integrity-checked supplied-semantics baseline | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)` |
| 862 | `reference-semantics/semantics/subscript.k:72` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= slStep(OptInt) [function, total]` |
| 863 | `reference-semantics/semantics/subscript.k:73` | rule | — | integrity-checked supplied-semantics baseline | `rule slStep(noB) => 1` |
| 864 | `reference-semantics/semantics/subscript.k:74` | rule | — | integrity-checked supplied-semantics baseline | `rule slStep(someB(S:Int)) => S` |
| 865 | `reference-semantics/semantics/subscript.k:76` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 866 | `reference-semantics/semantics/subscript.k:77` | rule | — | integrity-checked supplied-semantics baseline | `rule slStart(noB, ST:OptInt, _LEN:Int) => 0` |
| 867 | `reference-semantics/semantics/subscript.k:79` | rule | — | integrity-checked supplied-semantics baseline | `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1` |
| 868 | `reference-semantics/semantics/subscript.k:81` | rule | — | integrity-checked supplied-semantics baseline | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 869 | `reference-semantics/semantics/subscript.k:83` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 870 | `reference-semantics/semantics/subscript.k:84` | rule | — | integrity-checked supplied-semantics baseline | `rule slStop(noB, ST:OptInt, LEN:Int) => LEN` |
| 871 | `reference-semantics/semantics/subscript.k:86` | rule | — | integrity-checked supplied-semantics baseline | `rule slStop(noB, ST:OptInt, _LEN:Int) => -1` |
| 872 | `reference-semantics/semantics/subscript.k:88` | rule | — | integrity-checked supplied-semantics baseline | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 873 | `reference-semantics/semantics/subscript.k:90` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 874 | `reference-semantics/semantics/subscript.k:91` | rule | — | integrity-checked supplied-semantics baseline | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)` |
| 875 | `reference-semantics/semantics/subscript.k:93` | rule | — | integrity-checked supplied-semantics baseline | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)` |
| 876 | `reference-semantics/semantics/subscript.k:96` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 877 | `reference-semantics/semantics/subscript.k:97` | rule | — | integrity-checked supplied-semantics baseline | `rule clampLo(J:Int, _STEP:Int) => J` |
| 878 | `reference-semantics/semantics/subscript.k:99` | rule | — | integrity-checked supplied-semantics baseline | `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi` |
| 879 | `reference-semantics/semantics/subscript.k:102` | syntax | function, total | integrity-checked supplied-semantics baseline | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 880 | `reference-semantics/semantics/subscript.k:103` | rule | — | integrity-checked supplied-semantics baseline | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I` |
| 881 | `reference-semantics/semantics/subscript.k:105` | rule | — | integrity-checked supplied-semantics baseline | `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi` |
| 882 | `reference-semantics/semantics/subscript.k:109` | syntax | function | integrity-checked supplied-semantics baseline | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 883 | `reference-semantics/semantics/subscript.k:110` | rule | — | integrity-checked supplied-semantics baseline | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)` |
| 884 | `reference-semantics/semantics/subscript.k:113` | rule | — | integrity-checked supplied-semantics baseline | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq` |
| 885 | `reference-semantics/semantics/subscript.k:116` | syntax | function | integrity-checked supplied-semantics baseline | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 886 | `reference-semantics/semantics/subscript.k:117` | rule | — | integrity-checked supplied-semantics baseline | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)` |
| 887 | `reference-semantics/semantics/subscript.k:120` | rule | — | integrity-checked supplied-semantics baseline | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq` |
| 888 | `reference-semantics/semantics/syntax.k:9` | syntax | macro, strict, seqstrict | integrity-checked supplied-semantics baseline | `syntax Expr ::= "Int" "(" Int ")"` |
| 889 | `reference-semantics/semantics/syntax.k:32` | syntax | — | integrity-checked supplied-semantics baseline | `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"` |
| 890 | `reference-semantics/semantics/syntax.k:33` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Entry ::= "Entry" "(" Expr "," Expr ")"` |
| 891 | `reference-semantics/semantics/syntax.k:34` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Entries ::= List{Entry, ","}` |
| 892 | `reference-semantics/semantics/syntax.k:35` | syntax | — | integrity-checked supplied-semantics baseline | `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 893 | `reference-semantics/semantics/syntax.k:36` | syntax | — | integrity-checked supplied-semantics baseline | `syntax CompFors ::= List{CompFor, ""}` |
| 894 | `reference-semantics/semantics/syntax.k:37` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Exprs ::= List{Expr, ","}` |
| 895 | `reference-semantics/semantics/syntax.k:38` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 896 | `reference-semantics/semantics/syntax.k:39` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Bound ::= Expr \| "NoBound"` |
| 897 | `reference-semantics/semantics/syntax.k:41` | syntax | strict | integrity-checked supplied-semantics baseline | `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)]` |
| 898 | `reference-semantics/semantics/syntax.k:56` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Stmts ::= List{Stmt, ""}` |
| 899 | `reference-semantics/semantics/syntax.k:57` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Params ::= "Params" "(" ParamNames ")"` |
| 900 | `reference-semantics/semantics/syntax.k:58` | syntax | — | integrity-checked supplied-semantics baseline | `syntax CellVars ::= "CellVars" "(" ParamNames ")"` |
| 901 | `reference-semantics/semantics/syntax.k:59` | syntax | — | integrity-checked supplied-semantics baseline | `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"` |
| 902 | `reference-semantics/semantics/syntax.k:60` | syntax | — | integrity-checked supplied-semantics baseline | `syntax ParamNames ::= List{String, ","}` |
| 903 | `reference-semantics/semantics/syntax.k:61` | syntax | — | integrity-checked supplied-semantics baseline | `syntax Module ::= "Module" "(" Stmts ")"` |
| 904 | `reference-semantics/semantics/tuple.k:10` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>` |
| 905 | `reference-semantics/semantics/tuple.k:11` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| 906 | `reference-semantics/semantics/tuple.k:14` | syntax | — | integrity-checked supplied-semantics baseline | `syntax ApplyK ::= "toTuple"` |
| 907 | `reference-semantics/semantics/tuple.k:15` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 908 | `reference-semantics/semantics/tuple.k:16` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 909 | `reference-semantics/semantics/tuple.k:18` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| 910 | `reference-semantics/semantics/tuple.k:20` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 911 | `reference-semantics/semantics/tuple.k:21` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| 912 | `reference-semantics/semantics/tuple.k:23` | rule | — | integrity-checked supplied-semantics baseline | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 913 | `reference-semantics/semantics/tuple.k:24` | syntax | function | integrity-checked supplied-semantics baseline | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 914 | `reference-semantics/semantics/tuple.k:25` | rule | — | integrity-checked supplied-semantics baseline | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 915 | `reference-semantics/semantics/tuple.k:26` | rule | — | integrity-checked supplied-semantics baseline | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)` |
| 916 | `reference-semantics/semantics/tuple.k:28` | rule | — | integrity-checked supplied-semantics baseline | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| 917 | `reference-semantics/semantics/tuple.k:31` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 918 | `reference-semantics/semantics/tuple.k:32` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>` |
| 919 | `reference-semantics/semantics/tuple.k:35` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>` |
| 920 | `reference-semantics/semantics/tuple.k:42` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 921 | `reference-semantics/semantics/tuple.k:43` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 922 | `reference-semantics/semantics/tuple.k:44` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>` |
| 923 | `reference-semantics/semantics/tuple.k:49` | syntax | — | integrity-checked supplied-semantics baseline | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 924 | `reference-semantics/semantics/tuple.k:50` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 925 | `reference-semantics/semantics/tuple.k:51` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 926 | `reference-semantics/semantics/tuple.k:52` | rule | priority | integrity-checked supplied-semantics baseline | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>` |
| 927 | `reference-semantics/semantics/tuple.k:55` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))` |
| 928 | `reference-semantics/semantics/tuple.k:57` | rule | — | integrity-checked supplied-semantics baseline | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| 929 | `verification.k:7` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= digitQuot(Int) [function, total]` |
| 930 | `verification.k:8` | rule | — | proof-local definition or exact-syntax macro | `rule digitQuot(N:Int) => (N -Int pyMod(N, 10)) /Int 10` |
| 931 | `verification.k:10` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= positiveFold(Int, Int) [function, total]` |
| 932 | `verification.k:11` | rule | — | proof-local definition or exact-syntax macro | `rule positiveFold(N:Int, A:Int) => A requires N <=Int 0` |
| 933 | `verification.k:12` | rule | — | proof-local definition or exact-syntax macro | `rule positiveFold(N:Int, A:Int)` |
| 934 | `verification.k:16` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= positiveDigitSum(Int) [function, total]` |
| 935 | `verification.k:17` | rule | — | proof-local definition or exact-syntax macro | `rule positiveDigitSum(N:Int) => positiveFold(N, 0)` |
| 936 | `verification.k:20` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= leadingDigit(Int) [function, total]` |
| 937 | `verification.k:21` | rule | — | proof-local definition or exact-syntax macro | `rule leadingDigit(N:Int) => N` |
| 938 | `verification.k:23` | rule | — | proof-local definition or exact-syntax macro | `rule leadingDigit(N:Int) => leadingDigit(digitQuot(N))` |
| 939 | `verification.k:26` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= negativeTotal(Int, Int) [function, total]` |
| 940 | `verification.k:27` | rule | — | proof-local definition or exact-syntax macro | `rule negativeTotal(N:Int, A:Int) => A` |
| 941 | `verification.k:29` | rule | — | proof-local definition or exact-syntax macro | `rule negativeTotal(N:Int, A:Int)` |
| 942 | `verification.k:33` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= negativeDigitSum(Int) [function, total]` |
| 943 | `verification.k:34` | rule | — | proof-local definition or exact-syntax macro | `rule negativeDigitSum(N:Int)` |
| 944 | `verification.k:37` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= signedDigitSum(Int) [function, total]` |
| 945 | `verification.k:38` | rule | — | proof-local definition or exact-syntax macro | `rule signedDigitSum(N:Int) => negativeDigitSum(0 -Int N)` |
| 946 | `verification.k:40` | rule | — | proof-local definition or exact-syntax macro | `rule signedDigitSum(N:Int) => positiveDigitSum(N)` |
| 947 | `verification.k:44` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= intValue(Val) [function, total]` |
| 948 | `verification.k:45` | rule | — | proof-local definition or exact-syntax macro | `rule intValue(N:Int) => N` |
| 949 | `verification.k:46` | rule | owise | proof-local definition or exact-syntax macro | `rule intValue(_:Val) => 0 [owise]` |
| 950 | `verification.k:48` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= positiveBit(Int) [function, total]` |
| 951 | `verification.k:49` | rule | — | proof-local definition or exact-syntax macro | `rule positiveBit(N:Int) => 1 requires N >Int 0` |
| 952 | `verification.k:50` | rule | — | proof-local definition or exact-syntax macro | `rule positiveBit(N:Int) => 0 requires N <=Int 0` |
| 953 | `verification.k:52` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= countFold(ValSeq, Int) [function, total]` |
| 954 | `verification.k:53` | rule | — | proof-local definition or exact-syntax macro | `rule countFold(.ValSeq, C:Int) => C` |
| 955 | `verification.k:54` | rule | — | proof-local definition or exact-syntax macro | `rule countFold(vCons(V:Val, REST:ValSeq), C:Int)` |
| 956 | `verification.k:59` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Int ::= countPositive(ValSeq) [function, total]` |
| 957 | `verification.k:60` | rule | — | proof-local definition or exact-syntax macro | `rule countPositive(VS:ValSeq) => countFold(VS, 0)` |
| 958 | `verification.k:62` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Bool ::= allInts(ValSeq) [function, total]` |
| 959 | `verification.k:63` | rule | — | proof-local definition or exact-syntax macro | `rule allInts(.ValSeq) => true` |
| 960 | `verification.k:64` | rule | — | proof-local definition or exact-syntax macro | `rule allInts(vCons(V:Val, REST:ValSeq))` |
| 961 | `verification.k:68` | syntax | function, total | proof-local definition or exact-syntax macro | `syntax Val ::= lastOr(ValSeq, Val) [function, total]` |
| 962 | `verification.k:69` | rule | — | proof-local definition or exact-syntax macro | `rule lastOr(.ValSeq, OLD:Val) => OLD` |
| 963 | `verification.k:70` | rule | — | proof-local definition or exact-syntax macro | `rule lastOr(vCons(V:Val, REST:ValSeq), _OLD:Val)` |
| 964 | `verification.k:74` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Stmts ::= "positiveLoopBody" [macro]` |
| 965 | `verification.k:75` | rule | — | proof-local definition or exact-syntax macro | `rule positiveLoopBody` |
| 966 | `verification.k:79` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Stmts ::= "negativeLoopBody" [macro]` |
| 967 | `verification.k:80` | rule | — | proof-local definition or exact-syntax macro | `rule negativeLoopBody` |
| 968 | `verification.k:84` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Stmts ::= "positiveFunctionBody" [macro]` |
| 969 | `verification.k:85` | rule | — | proof-local definition or exact-syntax macro | `rule positiveFunctionBody` |
| 970 | `verification.k:90` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Stmts ::= "negativeFunctionBody" [macro]` |
| 971 | `verification.k:91` | rule | — | proof-local definition or exact-syntax macro | `rule negativeFunctionBody` |
| 972 | `verification.k:96` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Stmts ::= "signedFunctionBody" [macro]` |
| 973 | `verification.k:97` | rule | — | proof-local definition or exact-syntax macro | `rule signedFunctionBody` |
| 974 | `verification.k:104` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Stmts ::= "countLoopBody" [macro]` |
| 975 | `verification.k:105` | rule | — | proof-local definition or exact-syntax macro | `rule countLoopBody` |
| 976 | `verification.k:111` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Stmts ::= "countFunctionBody" [macro]` |
| 977 | `verification.k:112` | rule | — | proof-local definition or exact-syntax macro | `rule countFunctionBody` |
| 978 | `verification.k:117` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Val ::= "positiveDigitClosure" [macro]` |
| 979 | `verification.k:118` | rule | — | proof-local definition or exact-syntax macro | `rule positiveDigitClosure` |
| 980 | `verification.k:121` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Val ::= "negativeDigitClosure" [macro]` |
| 981 | `verification.k:122` | rule | — | proof-local definition or exact-syntax macro | `rule negativeDigitClosure` |
| 982 | `verification.k:125` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Val ::= "signedDigitClosure" [macro]` |
| 983 | `verification.k:126` | rule | — | proof-local definition or exact-syntax macro | `rule signedDigitClosure` |
| 984 | `verification.k:129` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Val ::= "countNumsClosure" [macro]` |
| 985 | `verification.k:130` | rule | — | proof-local definition or exact-syntax macro | `rule countNumsClosure` |
| 986 | `verification.k:133` | syntax | macro | proof-local definition or exact-syntax macro | `syntax Map ::= "digitFunctionBindings" [macro]` |
| 987 | `verification.k:134` | rule | — | proof-local definition or exact-syntax macro | `rule digitFunctionBindings` |
| 988 | `verification.k:145` | rule | priority | proof-local operational bridge | `rule <k> #while(Compare(Name("n"), CmpOp(">", Int(0))),` |
| 989 | `verification.k:159` | rule | priority | proof-local operational bridge | `rule <k> #while(Compare(Name("n"), CmpOp(">=", Int(10))),` |
| 990 | `verification.k:177` | rule | priority | proof-local operational bridge | `rule <k> #applyK(toCall(positiveDigitClosure), (N:Int, .Vals))` |
| 991 | `verification.k:182` | rule | priority | proof-local operational bridge | `rule <k> #applyK(toCall(negativeDigitClosure), (N:Int, .Vals))` |
| 992 | `verification.k:191` | rule | priority | proof-local operational bridge | `rule <k> #applyK(toCall(signedDigitClosure), (V:Val, .Vals))` |
| 993 | `verification.k:200` | rule | priority | proof-local operational bridge | `rule <k> #loop(list(VS:ValSeq), Name("n"), countLoopBody) => .K ... </k>` |
| 994 | `verification.k:220` | rule | priority | proof-local operational bridge | `rule <k> #loop(list(.ValSeq), Name("n"), countLoopBody) => .K ... </k>` |
| 995 | `verification.k:230` | rule | priority | proof-local operational bridge | `rule <k> #loop(list(vCons(H:Val, REST:ValSeq)),` |
| 996 | `spec.k:6` | claim | — | target reachability claim | `claim <k> #while(Compare(Name("n"), CmpOp(">", Int(0))),` |
| 997 | `spec.k:23` | claim | — | target reachability claim | `claim <k> #while(Compare(Name("n"), CmpOp(">=", Int(10))),` |
| 998 | `spec.k:40` | claim | — | target reachability claim | `claim` |
| 999 | `spec.k:61` | claim | — | target reachability claim | `claim` |
| 1000 | `spec.k:82` | claim | — | target reachability claim | `claim` |
| 1001 | `spec.k:102` | claim | — | target reachability claim | `claim <k> #loop(list(VS:ValSeq), Name("n"), countLoopBody)` |
| 1002 | `spec.k:123` | claim | — | target reachability claim | `claim <k> #loop(list(.ValSeq), Name("n"), countLoopBody)` |
| 1003 | `spec.k:135` | claim | — | target reachability claim | `claim <k> #loop(list(vCons(H:Val, REST:ValSeq)),` |
| 1004 | `spec.k:156` | claim | — | target reachability claim | `claim` |

## Opaque/symbol declarations

- `reference-semantics/semantics/builtins.k:285`: `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`
- `reference-semantics/semantics/float.k:24`: `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`
- `reference-semantics/semantics/float.k:30`: `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`
- `reference-semantics/semantics/float.k:37`: `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`
- `reference-semantics/semantics/float.k:50`: `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`
- `reference-semantics/semantics/float.k:54`: `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`
- `reference-semantics/semantics/float.k:73`: `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`
- `reference-semantics/semantics/float.k:86`: `syntax Float ::= toF(Val) [function, total, symbol(toF)]`
- `reference-semantics/semantics/float.k:93`: `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`
- `reference-semantics/semantics/float.k:103`: `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`
- `reference-semantics/semantics/float.k:107`: `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`
- `reference-semantics/semantics/float.k:111`: `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`
- `reference-semantics/semantics/float.k:115`: `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`
- `reference-semantics/semantics/float.k:119`: `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`
- `reference-semantics/semantics/float.k:125`: `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`
- `reference-semantics/semantics/float.k:142`: `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`
- `reference-semantics/semantics/float.k:160`: `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`
- `reference-semantics/semantics/float.k:190`: `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`
- `reference-semantics/semantics/float.k:195`: `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`
- `reference-semantics/semantics/float.k:209`: `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`
- `reference-semantics/semantics/float.k:217`: `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`
- `reference-semantics/semantics/float.k:223`: `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`
- `reference-semantics/semantics/float.k:230`: `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`
- `reference-semantics/semantics/sort.k:18`: `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`
- `reference-semantics/semantics/sort.k:49`: `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`

## Simplification declarations/rules

None.

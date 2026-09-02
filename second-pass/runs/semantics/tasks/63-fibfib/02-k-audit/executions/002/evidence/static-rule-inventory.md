# Exhaustive local K inventory

Generated from the fresh scratch sources. `SUPPLIED-FIXED` means the entry belongs byte-for-byte to the selected trusted semantics; the used slice was additionally checked against this program's execution. Entries outside the directly mapped slice were screened for overlap, task-specific content, and dependency through opaque results.

Total entries: 937. Kinds: {'rule': 698, 'context': 5, 'syntax': 228, 'configuration': 1, 'claim': 5}.

Attribute markers: {'priority(40)': 41, 'function': 147, 'total': 107, 'owise': 26, 'no-evaluators': 22, 'symbol(md5hexCodes)': 1, 'macro': 4, 'priority(45)': 3, 'symbol(intFloatDiv)': 1, 'concrete': 35, 'symbol(divII)': 1, 'symbol(floatMod)': 1, 'symbol(floatLt)': 1, 'symbol(absF)': 1, 'symbol(floorFI)': 1, 'symbol(toF)': 1, 'symbol(ceilF)': 1, 'symbol(subF)': 1, 'symbol(divF)': 1, 'symbol(addF)': 1, 'symbol(mulF)': 1, 'symbol(powF)': 1, 'symbol(gtF)': 1, 'symbol(eqF)': 1, 'symbol(decStrToF)': 1, 'symbol(divFloatIntV)': 1, 'symbol(intToF)': 1, 'symbol(truncF)': 1, 'symbol(roundF)': 1, 'symbol(roundFN)': 1, 'symbol(sqrtF)': 1, 'priority(39)': 1, 'symbol(sortVS)': 1, 'symbol(sortKeyVS)': 1, 'seqstrict': 1, 'strict': 2, 'simplification': 1}.

| ID | Location | Kind | Attributes | Used | Decision | Source statement |
|---:|---|---|---|:---:|---|---|
| 1 | `semantics/assert.k:6` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| 2 | `semantics/assert.k:8` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| 3 | `semantics/assert.k:13` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 4 | `semantics/bool.k:8` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 5 | `semantics/bool.k:10` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 6 | `semantics/bool.k:11` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| 7 | `semantics/bool.k:16` | context | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 8 | `semantics/bool.k:17` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 9 | `semantics/bool.k:18` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| 10 | `semantics/bool.k:20` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| 11 | `semantics/bool.k:22` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| 12 | `semantics/bool.k:24` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` |
| 13 | `semantics/bool.k:29` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| 14 | `semantics/bool.k:31` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 15 | `semantics/bool.k:35` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 16 | `semantics/bool.k:39` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 17 | `semantics/bool.k:43` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 18 | `semantics/builtins.k:17` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| 19 | `semantics/builtins.k:20` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= seqLen(Val) [function]` |
| 20 | `semantics/builtins.k:21` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 21 | `semantics/builtins.k:22` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)` |
| 22 | `semantics/builtins.k:23` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)` |
| 23 | `semantics/builtins.k:24` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule seqLen(str(IS:IntSeq))                   => isLen(IS)` |
| 24 | `semantics/builtins.k:25` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)` |
| 25 | `semantics/builtins.k:26` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| 26 | `semantics/builtins.k:32` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>` |
| 27 | `semantics/builtins.k:33` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 28 | `semantics/builtins.k:34` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>` |
| 29 | `semantics/builtins.k:35` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>` |
| 30 | `semantics/builtins.k:36` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 31 | `semantics/builtins.k:37` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule charsOf(.IntSeq)                => .ValSeq` |
| 32 | `semantics/builtins.k:38` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| 33 | `semantics/builtins.k:41` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| 34 | `semantics/builtins.k:44` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| 35 | `semantics/builtins.k:47` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 36 | `semantics/builtins.k:48` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 37 | `semantics/builtins.k:49` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 38 | `semantics/builtins.k:50` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| 39 | `semantics/builtins.k:54` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= intOf(Val) [function]` |
| 40 | `semantics/builtins.k:55` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intOf(I:Int)  => I` |
| 41 | `semantics/builtins.k:56` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| 42 | `semantics/builtins.k:59` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 43 | `semantics/builtins.k:60` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 44 | `semantics/builtins.k:61` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 45 | `semantics/builtins.k:62` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| 46 | `semantics/builtins.k:64` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| 47 | `semantics/builtins.k:67` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 48 | `semantics/builtins.k:68` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 49 | `semantics/builtins.k:69` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 50 | `semantics/builtins.k:70` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| 51 | `semantics/builtins.k:72` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` |
| 52 | `semantics/builtins.k:76` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 53 | `semantics/builtins.k:77` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 54 | `semantics/builtins.k:78` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 55 | `semantics/builtins.k:80` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 56 | `semantics/builtins.k:81` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 57 | `semantics/builtins.k:82` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 58 | `semantics/builtins.k:86` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 59 | `semantics/builtins.k:87` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 60 | `semantics/builtins.k:88` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 61 | `semantics/builtins.k:90` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 62 | `semantics/builtins.k:91` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 63 | `semantics/builtins.k:92` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 64 | `semantics/builtins.k:97` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 65 | `semantics/builtins.k:98` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 66 | `semantics/builtins.k:99` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule maxVals(M:Int, .Vals)           => M` |
| 67 | `semantics/builtins.k:100` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| 68 | `semantics/builtins.k:102` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= minVals(Int, Vals) [function]` |
| 69 | `semantics/builtins.k:103` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 70 | `semantics/builtins.k:104` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule minVals(M:Int, .Vals)           => M` |
| 71 | `semantics/builtins.k:105` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| 72 | `semantics/builtins.k:108` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` |
| 73 | `semantics/builtins.k:111` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| 74 | `semantics/builtins.k:114` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 75 | `semantics/builtins.k:115` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 76 | `semantics/builtins.k:116` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 77 | `semantics/builtins.k:117` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 78 | `semantics/builtins.k:118` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 79 | `semantics/builtins.k:119` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` |
| 80 | `semantics/builtins.k:124` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| 81 | `semantics/builtins.k:126` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 82 | `semantics/builtins.k:127` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 83 | `semantics/builtins.k:128` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` |
| 84 | `semantics/builtins.k:132` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| 85 | `semantics/builtins.k:134` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 86 | `semantics/builtins.k:135` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 87 | `semantics/builtins.k:136` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 88 | `semantics/builtins.k:137` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| 89 | `semantics/builtins.k:140` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| 90 | `semantics/builtins.k:143` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 91 | `semantics/builtins.k:144` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` |
| 92 | `semantics/builtins.k:148` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))` |
| 93 | `semantics/builtins.k:149` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| 94 | `semantics/builtins.k:152` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` |
| 95 | `semantics/builtins.k:156` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| 96 | `semantics/builtins.k:158` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 97 | `semantics/builtins.k:159` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intDigAcc(.IntSeq, ACC:Int)             => ACC` |
| 98 | `semantics/builtins.k:160` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| 99 | `semantics/builtins.k:163` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 100 | `semantics/builtins.k:164` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)` |
| 101 | `semantics/builtins.k:167` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| 102 | `semantics/builtins.k:169` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>` |
| 103 | `semantics/builtins.k:170` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 104 | `semantics/builtins.k:171` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| 105 | `semantics/builtins.k:173` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>` |
| 106 | `semantics/builtins.k:174` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| 107 | `semantics/builtins.k:177` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)` |
| 108 | `semantics/builtins.k:178` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)` |
| 109 | `semantics/builtins.k:179` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` |
| 110 | `semantics/builtins.k:187` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 111 | `semantics/builtins.k:188` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= evalArith(IntSeq) [function]` |
| 112 | `semantics/builtins.k:189` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| 113 | `semantics/builtins.k:192` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| 114 | `semantics/builtins.k:194` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= evDigit(Int) [function, total]` |
| 115 | `semantics/builtins.k:195` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 116 | `semantics/builtins.k:196` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 117 | `semantics/builtins.k:197` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 118 | `semantics/builtins.k:198` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule evHead42(_:IntSeq)            => false [owise]` |
| 119 | `semantics/builtins.k:199` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 120 | `semantics/builtins.k:200` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 121 | `semantics/builtins.k:201` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule evHead47(_:IntSeq)            => false [owise]` |
| 122 | `semantics/builtins.k:203` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 123 | `semantics/builtins.k:204` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokOps(.IntSeq)                 => .OpSeq` |
| 124 | `semantics/builtins.k:205` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)` |
| 125 | `semantics/builtins.k:206` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)` |
| 126 | `semantics/builtins.k:207` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 127 | `semantics/builtins.k:208` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 128 | `semantics/builtins.k:209` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 129 | `semantics/builtins.k:210` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 130 | `semantics/builtins.k:211` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))` |
| 131 | `semantics/builtins.k:212` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))` |
| 132 | `semantics/builtins.k:214` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| 133 | `semantics/builtins.k:216` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokNds(.IntSeq)                => .IntSeq` |
| 134 | `semantics/builtins.k:217` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)` |
| 135 | `semantics/builtins.k:218` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 136 | `semantics/builtins.k:219` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| 137 | `semantics/builtins.k:221` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| 138 | `semantics/builtins.k:223` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 139 | `semantics/builtins.k:225` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 140 | `semantics/builtins.k:226` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 141 | `semantics/builtins.k:227` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 142 | `semantics/builtins.k:228` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 143 | `semantics/builtins.k:230` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 144 | `semantics/builtins.k:231` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyOpE("+",  A:Int, B:Int) => A +Int B` |
| 145 | `semantics/builtins.k:232` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyOpE("-",  A:Int, B:Int) => A -Int B` |
| 146 | `semantics/builtins.k:233` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyOpE("*",  A:Int, B:Int) => A *Int B` |
| 147 | `semantics/builtins.k:234` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 148 | `semantics/builtins.k:235` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 149 | `semantics/builtins.k:236` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 150 | `semantics/builtins.k:238` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 151 | `semantics/builtins.k:239` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 152 | `semantics/builtins.k:240` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 153 | `semantics/builtins.k:241` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| 154 | `semantics/builtins.k:243` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 155 | `semantics/builtins.k:244` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 156 | `semantics/builtins.k:245` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 157 | `semantics/builtins.k:246` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 158 | `semantics/builtins.k:247` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 159 | `semantics/builtins.k:248` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 160 | `semantics/builtins.k:250` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 161 | `semantics/builtins.k:251` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 162 | `semantics/builtins.k:252` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 163 | `semantics/builtins.k:253` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 164 | `semantics/builtins.k:254` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 165 | `semantics/builtins.k:255` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 166 | `semantics/builtins.k:256` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 167 | `semantics/builtins.k:257` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| 168 | `semantics/builtins.k:260` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| 169 | `semantics/builtins.k:263` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| 170 | `semantics/builtins.k:265` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 171 | `semantics/builtins.k:266` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 172 | `semantics/builtins.k:267` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 173 | `semantics/builtins.k:268` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule inLevelE(_:String, _:String) => false [owise]` |
| 174 | `semantics/builtins.k:269` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 175 | `semantics/builtins.k:270` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 176 | `semantics/builtins.k:271` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 177 | `semantics/builtins.k:272` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 178 | `semantics/builtins.k:273` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 179 | `semantics/builtins.k:274` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| 180 | `semantics/builtins.k:279` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= "#md5"` |
| 181 | `semantics/builtins.k:280` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| 182 | `semantics/builtins.k:282` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 183 | `semantics/builtins.k:283` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= md5Obj(IntSeq)` |
| 184 | `semantics/builtins.k:284` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 185 | `semantics/builtins.k:285` | syntax | function, no-evaluators, symbol(md5hexCodes), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| 186 | `semantics/builtins.k:291` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 187 | `semantics/builtins.k:292` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 188 | `semantics/builtins.k:293` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 189 | `semantics/builtins.k:294` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isIntV(_:Int)         => true` |
| 190 | `semantics/builtins.k:295` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isIntV(_:Val)         => false [owise]` |
| 191 | `semantics/builtins.k:296` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isStrV(str(_:IntSeq)) => true` |
| 192 | `semantics/builtins.k:297` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isStrV(_:Val)         => false [owise]` |
| 193 | `semantics/call.k:16` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| 194 | `semantics/call.k:19` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax KItem ::= #callee(Exprs)` |
| 195 | `semantics/call.k:20` | rule | owise | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 196 | `semantics/call.k:21` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| 197 | `semantics/call.k:24` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 198 | `semantics/call.k:26` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 199 | `semantics/call.k:27` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>` |
| 200 | `semantics/call.k:28` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>` |
| 201 | `semantics/call.k:29` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>` |
| 202 | `semantics/call.k:30` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>` |
| 203 | `semantics/call.k:31` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 204 | `semantics/call.k:32` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>` |
| 205 | `semantics/call.k:38` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 206 | `semantics/call.k:42` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| 207 | `semantics/call.k:47` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 208 | `semantics/call.k:52` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 209 | `semantics/call.k:53` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| 210 | `semantics/call.k:56` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` |
| 211 | `semantics/call.k:63` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| 212 | `semantics/call.k:69` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| 213 | `semantics/call.k:80` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| 214 | `semantics/call.k:87` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #allocCells(ParamNames)` |
| 215 | `semantics/call.k:88` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 216 | `semantics/call.k:89` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 217 | `semantics/comprehension.k:11` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 218 | `semantics/comprehension.k:12` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 219 | `semantics/comprehension.k:14` | syntax | macro | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 220 | `semantics/comprehension.k:15` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| 221 | `semantics/comprehension.k:18` | syntax | macro | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 222 | `semantics/comprehension.k:19` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| 223 | `semantics/comprehension.k:21` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| 224 | `semantics/comprehension.k:24` | syntax | macro | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 225 | `semantics/comprehension.k:25` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule compGuard(.Exprs)             => Bool(true)` |
| 226 | `semantics/comprehension.k:26` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| 227 | `semantics/concrete.k:13` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 228 | `semantics/concrete.k:16` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 229 | `semantics/concrete.k:25` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= kvP(Val, Val)` |
| 230 | `semantics/concrete.k:26` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| 231 | `semantics/concrete.k:28` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| 232 | `semantics/concrete.k:31` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| 233 | `semantics/concrete.k:34` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| 234 | `semantics/concrete.k:36` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| 235 | `semantics/concrete.k:38` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| 236 | `semantics/concrete.k:42` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 237 | `semantics/concrete.k:43` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 238 | `semantics/concrete.k:44` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| 239 | `semantics/concrete.k:47` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| 240 | `semantics/concrete.k:51` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= kLt(Val, Val) [function]` |
| 241 | `semantics/concrete.k:52` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule kLt(I1:Int, I2:Int)             => I1 <Int I2` |
| 242 | `semantics/concrete.k:53` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule kLt(F1:Float, F2:Float)         => F1 <Float F2` |
| 243 | `semantics/concrete.k:54` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 244 | `semantics/concrete.k:56` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 245 | `semantics/concrete.k:57` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule unpairVS(.ValSeq) => .ValSeq` |
| 246 | `semantics/concrete.k:58` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 247 | `semantics/concrete.k:59` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| 248 | `semantics/controls.k:9` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 249 | `semantics/controls.k:12` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 250 | `semantics/controls.k:20` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` |
| 251 | `semantics/controls.k:27` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]` |
| 252 | `semantics/controls.k:35` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 253 | `semantics/controls.k:36` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 254 | `semantics/controls.k:37` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #bindImports(ParamNames)` |
| 255 | `semantics/controls.k:38` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 256 | `semantics/controls.k:39` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| 257 | `semantics/controls.k:43` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` |
| 258 | `semantics/controls.k:48` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Expr(_:Val) => .K ... </k>` |
| 259 | `semantics/controls.k:51` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 260 | `semantics/controls.k:52` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 261 | `semantics/controls.k:53` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>` |
| 262 | `semantics/controls.k:54` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| 263 | `semantics/controls.k:57` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| 264 | `semantics/controls.k:59` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` |
| 265 | `semantics/controls.k:65` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| 266 | `semantics/controls.k:69` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 267 | `semantics/controls.k:71` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 268 | `semantics/controls.k:72` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 269 | `semantics/controls.k:73` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` |
| 270 | `semantics/controls.k:77` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 271 | `semantics/controls.k:78` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 272 | `semantics/controls.k:79` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| 273 | `semantics/controls.k:81` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` |
| 274 | `semantics/controls.k:85` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 275 | `semantics/controls.k:86` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Continue => #cont ... </k>` |
| 276 | `semantics/controls.k:87` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Break => #brk ... </k>` |
| 277 | `semantics/controls.k:88` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 278 | `semantics/controls.k:89` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 279 | `semantics/controls.k:90` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 280 | `semantics/controls.k:91` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| 281 | `semantics/controls.k:95` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 282 | `semantics/controls.k:98` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 283 | `semantics/controls.k:101` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 284 | `semantics/controls.k:106` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 285 | `semantics/core.k:13` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 286 | `semantics/core.k:14` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 287 | `semantics/core.k:15` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Str    ::= str(IntSeq)` |
| 288 | `semantics/core.k:18` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| 289 | `semantics/core.k:25` | syntax | function | yes | SUPPLIED-FIXED / EXERCISED | `syntax Val      ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int)          // a heap object: <heap> holds its list(VS) \| cellRef(Int)      // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String)     // a type object (int/str), resolved from the builtins frame \| builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String)   // a cooled Attribute: obj.method` |
| 290 | `semantics/core.k:36` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax Parent   ::= "root" \| parent(Int)` |
| 291 | `semantics/core.k:37` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax Scope    ::= scope(Map, Parent)` |
| 292 | `semantics/core.k:38` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax KResult  ::= Val` |
| 293 | `semantics/core.k:39` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax Expr     ::= Val   // cooling puts results back into expression holes` |
| 294 | `semantics/core.k:40` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax Vals     ::= List{Val, ","}` |
| 295 | `semantics/core.k:41` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Exc      ::= "NoExc" \| "AssertionError"` |
| 296 | `semantics/core.k:42` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax RetState ::= "noRet" \| retV(Val)` |
| 297 | `semantics/core.k:49` | configuration | none | yes | SUPPLIED-FIXED / EXERCISED | `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     \|-> scope(.Map, parent(-1)) -1    \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code>` |
| 298 | `semantics/core.k:68` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isRefV(Val) [function, total]` |
| 299 | `semantics/core.k:69` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isRefV(ref(_:Int)) => true` |
| 300 | `semantics/core.k:70` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isRefV(_:Val)      => false [owise]` |
| 301 | `semantics/core.k:75` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax HeapVal ::= cellV(Val)` |
| 302 | `semantics/core.k:76` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 303 | `semantics/core.k:77` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isCellRef(cellRef(_:Int)) => true` |
| 304 | `semantics/core.k:78` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isCellRef(_:Val)          => false [owise]` |
| 305 | `semantics/core.k:85` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` |
| 306 | `semantics/core.k:95` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= kwV(String, Val)` |
| 307 | `semantics/core.k:96` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #kwTag(String)` |
| 308 | `semantics/core.k:97` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 309 | `semantics/core.k:98` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| 310 | `semantics/core.k:100` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isKwV(Val) [function, total]` |
| 311 | `semantics/core.k:101` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 312 | `semantics/core.k:102` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isKwV(_:Val)                => false [owise]` |
| 313 | `semantics/core.k:106` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= cellsMark(ParamNames)` |
| 314 | `semantics/core.k:107` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 315 | `semantics/core.k:108` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 316 | `semantics/core.k:109` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 317 | `semantics/core.k:110` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule pnMember(_:String, .ParamNames) => false` |
| 318 | `semantics/core.k:111` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 319 | `semantics/core.k:113` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #cellW(Val, Val)` |
| 320 | `semantics/core.k:114` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| 321 | `semantics/core.k:117` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #alloc(Val)` |
| 322 | `semantics/core.k:118` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 323 | `semantics/core.k:124` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #loadAll(Module)` |
| 324 | `semantics/core.k:125` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 325 | `semantics/core.k:126` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 326 | `semantics/core.k:127` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> .Stmts => .K ... </k>` |
| 327 | `semantics/core.k:130` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #look(String, Int)` |
| 328 | `semantics/core.k:131` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 329 | `semantics/core.k:132` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` |
| 330 | `semantics/core.k:145` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| 331 | `semantics/core.k:152` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` |
| 332 | `semantics/core.k:157` | syntax | function, total | yes | SUPPLIED-FIXED / EXERCISED | `syntax Scope ::= "builtinsScope" [function, total]` |
| 333 | `semantics/core.k:158` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root)` |
| 334 | `semantics/core.k:185` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax ApplyK ::= toCall(Val)` |
| 335 | `semantics/core.k:186` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| 336 | `semantics/core.k:189` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 337 | `semantics/core.k:190` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 338 | `semantics/core.k:191` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| 339 | `semantics/core.k:194` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> Int(I:Int)   => I ... </k>` |
| 340 | `semantics/core.k:195` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Bool(B:Bool) => B ... </k>` |
| 341 | `semantics/core.k:196` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> NoneVal      => noneV ... </k>` |
| 342 | `semantics/core.k:199` | syntax | function | yes | SUPPLIED-FIXED / EXERCISED | `syntax Bool ::= truthy(Val) [function]` |
| 343 | `semantics/core.k:200` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule truthy(B:Bool)          => B` |
| 344 | `semantics/core.k:201` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule truthy(noneV)           => false` |
| 345 | `semantics/core.k:202` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule truthy(I:Int)           => I =/=Int 0` |
| 346 | `semantics/core.k:203` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)` |
| 347 | `semantics/core.k:204` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)` |
| 348 | `semantics/core.k:205` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 349 | `semantics/core.k:208` | syntax | function | yes | SUPPLIED-FIXED / EXERCISED | `syntax Val  ::= applyUn(String, Val) [function]` |
| 350 | `semantics/core.k:209` | syntax | function | yes | SUPPLIED-FIXED / EXERCISED | `syntax Val  ::= applyBin(String, Val, Val) [function]` |
| 351 | `semantics/core.k:210` | syntax | function | yes | SUPPLIED-FIXED / EXERCISED | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| 352 | `semantics/core.k:213` | syntax | function, total | yes | SUPPLIED-FIXED / EXERCISED | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 353 | `semantics/core.k:214` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule appendVal(.Vals, V:Val)              => V , .Vals` |
| 354 | `semantics/core.k:215` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)` |
| 355 | `semantics/core.k:217` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 356 | `semantics/core.k:218` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule vals2valSeq(.Vals)            => .ValSeq` |
| 357 | `semantics/core.k:219` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| 358 | `semantics/core.k:223` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 359 | `semantics/core.k:224` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule vsLen(.ValSeq)                => 0` |
| 360 | `semantics/core.k:225` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 361 | `semantics/core.k:227` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 362 | `semantics/core.k:228` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isLen(.IntSeq)                => 0` |
| 363 | `semantics/core.k:229` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| 364 | `semantics/core.k:233` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 365 | `semantics/core.k:234` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq` |
| 366 | `semantics/core.k:235` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)` |
| 367 | `semantics/core.k:236` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| 368 | `semantics/core.k:238` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0` |
| 369 | `semantics/dict.k:20` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| 370 | `semantics/dict.k:23` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| 371 | `semantics/dict.k:26` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 372 | `semantics/dict.k:27` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 373 | `semantics/dict.k:28` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| 374 | `semantics/dict.k:30` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| 375 | `semantics/dict.k:32` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` |
| 376 | `semantics/dict.k:37` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 377 | `semantics/dict.k:38` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dHasKey(.ValSeq, _:Val)                => false` |
| 378 | `semantics/dict.k:39` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K` |
| 379 | `semantics/dict.k:40` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| 380 | `semantics/dict.k:43` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 381 | `semantics/dict.k:44` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)` |
| 382 | `semantics/dict.k:45` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| 383 | `semantics/dict.k:49` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 384 | `semantics/dict.k:50` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K` |
| 385 | `semantics/dict.k:52` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| 386 | `semantics/dict.k:54` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| 387 | `semantics/dict.k:58` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` |
| 388 | `semantics/dict.k:63` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 389 | `semantics/dict.k:64` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 390 | `semantics/dict.k:65` | rule | priority(45) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` |
| 391 | `semantics/dict.k:70` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 392 | `semantics/dict.k:71` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| 393 | `semantics/dict.k:76` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #dsetK(String, Val)` |
| 394 | `semantics/dict.k:77` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 395 | `semantics/dict.k:78` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| 396 | `semantics/dict.k:82` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| 397 | `semantics/dict.k:86` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 398 | `semantics/dict.k:87` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` |
| 399 | `semantics/dict.k:90` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 400 | `semantics/dict.k:91` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 401 | `semantics/dict.k:92` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0` |
| 402 | `semantics/dict.k:95` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| 403 | `semantics/dict.k:97` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 404 | `semantics/dict.k:98` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 405 | `semantics/dict.k:99` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| 406 | `semantics/dict.k:101` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 407 | `semantics/dict.k:102` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K` |
| 408 | `semantics/dict.k:103` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| 409 | `semantics/float.k:20` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= Float` |
| 410 | `semantics/float.k:21` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Float(F:Float) => F ... </k>` |
| 411 | `semantics/float.k:24` | syntax | function, no-evaluators, symbol(intFloatDiv), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 412 | `semantics/float.k:25` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 413 | `semantics/float.k:27` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| 414 | `semantics/float.k:30` | syntax | function, no-evaluators, symbol(divII), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 415 | `semantics/float.k:31` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 416 | `semantics/float.k:32` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| 417 | `semantics/float.k:37` | syntax | function, no-evaluators, symbol(floatMod), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 418 | `semantics/float.k:38` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 419 | `semantics/float.k:39` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| 420 | `semantics/float.k:43` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 421 | `semantics/float.k:44` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| 422 | `semantics/float.k:50` | syntax | function, no-evaluators, symbol(floatLt), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 423 | `semantics/float.k:51` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 424 | `semantics/float.k:52` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 425 | `semantics/float.k:54` | syntax | function, no-evaluators, symbol(absF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 426 | `semantics/float.k:55` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 427 | `semantics/float.k:56` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| 428 | `semantics/float.k:61` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Import(_:String) => .K ... </k>` |
| 429 | `semantics/float.k:65` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= "#mathCeil"` |
| 430 | `semantics/float.k:66` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 431 | `semantics/float.k:67` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| 432 | `semantics/float.k:70` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= "#mathFloor"` |
| 433 | `semantics/float.k:71` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 434 | `semantics/float.k:72` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 435 | `semantics/float.k:73` | syntax | function, symbol(floorFI), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 436 | `semantics/float.k:74` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule floorFI(I:Int)   => I                        [concrete]` |
| 437 | `semantics/float.k:75` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| 438 | `semantics/float.k:78` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 439 | `semantics/float.k:79` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)` |
| 440 | `semantics/float.k:82` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 441 | `semantics/float.k:83` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 442 | `semantics/float.k:84` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 443 | `semantics/float.k:85` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 444 | `semantics/float.k:86` | syntax | function, symbol(toF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 445 | `semantics/float.k:87` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule toF(F:Float) => F        [concrete]` |
| 446 | `semantics/float.k:88` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule toF(I:Int)   => intToF(I) [concrete]` |
| 447 | `semantics/float.k:93` | syntax | function, symbol(ceilF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 448 | `semantics/float.k:94` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule ceilF(I:Int)   => I                       [concrete]` |
| 449 | `semantics/float.k:95` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| 450 | `semantics/float.k:99` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| 451 | `semantics/float.k:103` | syntax | function, no-evaluators, symbol(subF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 452 | `semantics/float.k:104` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 453 | `semantics/float.k:105` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 454 | `semantics/float.k:107` | syntax | function, no-evaluators, symbol(divF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 455 | `semantics/float.k:108` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 456 | `semantics/float.k:109` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 457 | `semantics/float.k:111` | syntax | function, no-evaluators, symbol(addF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 458 | `semantics/float.k:112` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 459 | `semantics/float.k:113` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 460 | `semantics/float.k:115` | syntax | function, no-evaluators, symbol(mulF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 461 | `semantics/float.k:116` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 462 | `semantics/float.k:117` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 463 | `semantics/float.k:119` | syntax | function, no-evaluators, symbol(powF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 464 | `semantics/float.k:120` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 465 | `semantics/float.k:121` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| 466 | `semantics/float.k:125` | syntax | function, no-evaluators, symbol(gtF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 467 | `semantics/float.k:126` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 468 | `semantics/float.k:127` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)` |
| 469 | `semantics/float.k:128` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 470 | `semantics/float.k:129` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| 471 | `semantics/float.k:132` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 472 | `semantics/float.k:133` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 473 | `semantics/float.k:134` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)` |
| 474 | `semantics/float.k:135` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))` |
| 475 | `semantics/float.k:136` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)` |
| 476 | `semantics/float.k:137` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))` |
| 477 | `semantics/float.k:138` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)` |
| 478 | `semantics/float.k:139` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))` |
| 479 | `semantics/float.k:142` | syntax | function, no-evaluators, symbol(eqF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 480 | `semantics/float.k:143` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 481 | `semantics/float.k:144` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 482 | `semantics/float.k:145` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 483 | `semantics/float.k:146` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 484 | `semantics/float.k:147` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 485 | `semantics/float.k:148` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)` |
| 486 | `semantics/float.k:149` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))` |
| 487 | `semantics/float.k:150` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)` |
| 488 | `semantics/float.k:151` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))` |
| 489 | `semantics/float.k:154` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 490 | `semantics/float.k:155` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| 491 | `semantics/float.k:160` | syntax | function, no-evaluators, symbol(decStrToF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 492 | `semantics/float.k:161` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 493 | `semantics/float.k:162` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| 494 | `semantics/float.k:165` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= headIS(IntSeq) [function]` |
| 495 | `semantics/float.k:166` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 496 | `semantics/float.k:167` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 497 | `semantics/float.k:168` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 498 | `semantics/float.k:169` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 499 | `semantics/float.k:170` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 500 | `semantics/float.k:171` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| 501 | `semantics/float.k:173` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 502 | `semantics/float.k:174` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fracPart(.IntSeq) => 0` |
| 503 | `semantics/float.k:175` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 504 | `semantics/float.k:176` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 505 | `semantics/float.k:177` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fracAcc(.IntSeq, A:Int) => A` |
| 506 | `semantics/float.k:178` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 507 | `semantics/float.k:179` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 508 | `semantics/float.k:180` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fracScale(.IntSeq) => 1` |
| 509 | `semantics/float.k:181` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 510 | `semantics/float.k:182` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 511 | `semantics/float.k:183` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fscAcc(.IntSeq, A:Int) => A` |
| 512 | `semantics/float.k:184` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 513 | `semantics/float.k:185` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 514 | `semantics/float.k:186` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)` |
| 515 | `semantics/float.k:187` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("float", F:Float, .Vals)        => F` |
| 516 | `semantics/float.k:190` | syntax | function, no-evaluators, symbol(divFloatIntV), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 517 | `semantics/float.k:191` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 518 | `semantics/float.k:192` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| 519 | `semantics/float.k:195` | syntax | function, no-evaluators, symbol(intToF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 520 | `semantics/float.k:196` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 521 | `semantics/float.k:197` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 522 | `semantics/float.k:198` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 523 | `semantics/float.k:199` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 524 | `semantics/float.k:200` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 525 | `semantics/float.k:201` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 526 | `semantics/float.k:202` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 527 | `semantics/float.k:203` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 528 | `semantics/float.k:204` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 529 | `semantics/float.k:205` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 530 | `semantics/float.k:206` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| 531 | `semantics/float.k:209` | syntax | function, no-evaluators, symbol(truncF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 532 | `semantics/float.k:210` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 533 | `semantics/float.k:211` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 534 | `semantics/float.k:213` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)` |
| 535 | `semantics/float.k:214` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| 536 | `semantics/float.k:217` | syntax | function, no-evaluators, symbol(roundF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 537 | `semantics/float.k:218` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| 538 | `semantics/float.k:223` | syntax | function, no-evaluators, symbol(roundFN), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 539 | `semantics/float.k:224` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| 540 | `semantics/float.k:227` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)` |
| 541 | `semantics/float.k:228` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 542 | `semantics/float.k:230` | syntax | function, no-evaluators, symbol(sqrtF), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 543 | `semantics/float.k:231` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 544 | `semantics/float.k:232` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= "#mathSqrt"` |
| 545 | `semantics/float.k:233` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 546 | `semantics/float.k:234` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 547 | `semantics/float.k:235` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| 548 | `semantics/float.k:243` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 549 | `semantics/float.k:244` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 550 | `semantics/float.k:245` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 551 | `semantics/float.k:246` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 552 | `semantics/float.k:247` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 553 | `semantics/float.k:250` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 554 | `semantics/float.k:251` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 555 | `semantics/float.k:252` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 556 | `semantics/float.k:253` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 557 | `semantics/float.k:254` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 558 | `semantics/float.k:261` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 559 | `semantics/float.k:262` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| 560 | `semantics/float.k:265` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 561 | `semantics/float.k:266` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 562 | `semantics/float.k:267` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| 563 | `semantics/float.k:270` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| 564 | `semantics/functions.k:8` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall"` |
| 565 | `semantics/functions.k:14` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| 566 | `semantics/functions.k:18` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 567 | `semantics/functions.k:19` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` |
| 568 | `semantics/functions.k:27` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| 569 | `semantics/functions.k:31` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 570 | `semantics/functions.k:33` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| 571 | `semantics/functions.k:36` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 572 | `semantics/functions.k:42` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| 573 | `semantics/functions.k:47` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| 574 | `semantics/functions.k:50` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| 575 | `semantics/functions.k:53` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 576 | `semantics/functions.k:59` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` |
| 577 | `semantics/functions.k:63` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 578 | `semantics/functions.k:64` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes>` |
| 579 | `semantics/functions.k:68` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]` |
| 580 | `semantics/functions.k:78` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| 581 | `semantics/functions.k:80` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` |
| 582 | `semantics/functions.k:85` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |
| 583 | `semantics/int.k:7` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyUn("-", I:Int) => 0 -Int I` |
| 584 | `semantics/int.k:9` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2` |
| 585 | `semantics/int.k:11` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 586 | `semantics/int.k:12` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 587 | `semantics/int.k:13` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2` |
| 588 | `semantics/int.k:14` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2` |
| 589 | `semantics/int.k:15` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)` |
| 590 | `semantics/int.k:16` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 591 | `semantics/int.k:17` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 592 | `semantics/int.k:19` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= pyMod(Int, Int) [function]` |
| 593 | `semantics/int.k:20` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 594 | `semantics/int.k:22` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2` |
| 595 | `semantics/int.k:23` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2` |
| 596 | `semantics/int.k:24` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2` |
| 597 | `semantics/int.k:25` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2` |
| 598 | `semantics/int.k:26` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2` |
| 599 | `semantics/int.k:27` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2` |
| 600 | `semantics/iter.k:8` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| 601 | `semantics/list.k:9` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>` |
| 602 | `semantics/list.k:10` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| 603 | `semantics/list.k:13` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ApplyK ::= "toList"` |
| 604 | `semantics/list.k:14` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 605 | `semantics/list.k:15` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| 606 | `semantics/list.k:18` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 607 | `semantics/list.k:19` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule valSeqConcat(.ValSeq, T:ValSeq)                => T` |
| 608 | `semantics/list.k:20` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| 609 | `semantics/list.k:24` | rule | priority(45) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| 610 | `semantics/list.k:27` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 611 | `semantics/list.k:28` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| 612 | `semantics/list.k:33` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 613 | `semantics/list.k:34` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule hasRefVS(.ValSeq)                => false` |
| 614 | `semantics/list.k:35` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 615 | `semantics/list.k:37` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map)        [function]` |
| 616 | `semantics/list.k:39` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true` |
| 617 | `semantics/list.k:40` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false` |
| 618 | `semantics/list.k:41` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false` |
| 619 | `semantics/list.k:42` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| 620 | `semantics/list.k:45` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| 621 | `semantics/list.k:47` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| 622 | `semantics/list.k:49` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 623 | `semantics/list.k:50` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| 624 | `semantics/list.k:53` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` |
| 625 | `semantics/list.k:58` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 626 | `semantics/list.k:59` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 627 | `semantics/list.k:60` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 628 | `semantics/list.k:61` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 629 | `semantics/list.k:62` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 630 | `semantics/list.k:63` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| 631 | `semantics/list.k:65` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| 632 | `semantics/list.k:67` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| 633 | `semantics/methods.k:10` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| 634 | `semantics/methods.k:13` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 635 | `semantics/methods.k:14` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 636 | `semantics/methods.k:15` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 637 | `semantics/methods.k:16` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| 638 | `semantics/methods.k:19` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))` |
| 639 | `semantics/methods.k:20` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))` |
| 640 | `semantics/methods.k:21` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| 641 | `semantics/methods.k:26` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 642 | `semantics/methods.k:27` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 643 | `semantics/methods.k:28` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 644 | `semantics/methods.k:29` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 645 | `semantics/methods.k:30` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` |
| 646 | `semantics/methods.k:34` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 647 | `semantics/methods.k:35` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 648 | `semantics/methods.k:36` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 649 | `semantics/methods.k:37` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| 650 | `semantics/methods.k:39` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| 651 | `semantics/methods.k:41` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 652 | `semantics/methods.k:42` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 653 | `semantics/methods.k:43` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 654 | `semantics/methods.k:44` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| 655 | `semantics/methods.k:47` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 656 | `semantics/methods.k:48` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 657 | `semantics/methods.k:49` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule trimWS(.IntSeq) => .IntSeq` |
| 658 | `semantics/methods.k:50` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 659 | `semantics/methods.k:51` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 660 | `semantics/methods.k:52` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 661 | `semantics/methods.k:53` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 662 | `semantics/methods.k:54` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 663 | `semantics/methods.k:55` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| 664 | `semantics/methods.k:58` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| 665 | `semantics/methods.k:61` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| 666 | `semantics/methods.k:64` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 667 | `semantics/methods.k:65` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 668 | `semantics/methods.k:66` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule cntOccVS(.ValSeq, _:Val)                => 0` |
| 669 | `semantics/methods.k:67` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 670 | `semantics/methods.k:68` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)` |
| 671 | `semantics/methods.k:72` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| 672 | `semantics/methods.k:75` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result` |
| 673 | `semantics/methods.k:76` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 674 | `semantics/methods.k:77` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| 675 | `semantics/methods.k:79` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` |
| 676 | `semantics/methods.k:82` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 677 | `semantics/methods.k:83` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC` |
| 678 | `semantics/methods.k:84` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 679 | `semantics/methods.k:85` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isWSC(Int) [function, total]` |
| 680 | `semantics/methods.k:86` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| 681 | `semantics/methods.k:89` | rule | priority(39) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` |
| 682 | `semantics/methods.k:94` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| 683 | `semantics/methods.k:97` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token` |
| 684 | `semantics/methods.k:98` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)` |
| 685 | `semantics/methods.k:99` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| 686 | `semantics/methods.k:101` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| 687 | `semantics/methods.k:104` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| 688 | `semantics/methods.k:106` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 689 | `semantics/methods.k:107` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq` |
| 690 | `semantics/methods.k:108` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 691 | `semantics/methods.k:109` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| 692 | `semantics/methods.k:112` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 693 | `semantics/methods.k:113` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 694 | `semantics/methods.k:115` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 695 | `semantics/methods.k:116` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 696 | `semantics/methods.k:118` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 697 | `semantics/methods.k:119` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 698 | `semantics/methods.k:121` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 699 | `semantics/methods.k:122` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 700 | `semantics/methods.k:124` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 701 | `semantics/methods.k:125` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule hasUpper(.IntSeq) => false` |
| 702 | `semantics/methods.k:126` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 703 | `semantics/methods.k:128` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 704 | `semantics/methods.k:129` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule hasLower(.IntSeq) => false` |
| 705 | `semantics/methods.k:130` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 706 | `semantics/methods.k:132` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 707 | `semantics/methods.k:133` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule allAlpha(.IntSeq) => true` |
| 708 | `semantics/methods.k:134` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 709 | `semantics/methods.k:136` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 710 | `semantics/methods.k:137` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule allDigit(.IntSeq) => true` |
| 711 | `semantics/methods.k:138` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 712 | `semantics/methods.k:140` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= lowerC(Int) [function, total]` |
| 713 | `semantics/methods.k:142` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 714 | `semantics/methods.k:143` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule lowerC(C:Int) => C         [owise]` |
| 715 | `semantics/methods.k:145` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= upperC(Int) [function, total]` |
| 716 | `semantics/methods.k:146` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 717 | `semantics/methods.k:147` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule upperC(C:Int) => C         [owise]` |
| 718 | `semantics/methods.k:149` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= swapC(Int) [function, total]` |
| 719 | `semantics/methods.k:150` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 720 | `semantics/methods.k:151` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 721 | `semantics/methods.k:152` | rule | owise | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule swapC(C:Int) => C         [owise]` |
| 722 | `semantics/methods.k:154` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 723 | `semantics/methods.k:155` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mapLower(.IntSeq) => .IntSeq` |
| 724 | `semantics/methods.k:156` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 725 | `semantics/methods.k:158` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 726 | `semantics/methods.k:159` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mapUpper(.IntSeq) => .IntSeq` |
| 727 | `semantics/methods.k:160` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 728 | `semantics/methods.k:162` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 729 | `semantics/methods.k:163` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mapSwap(.IntSeq) => .IntSeq` |
| 730 | `semantics/methods.k:164` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 731 | `semantics/methods.k:166` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 732 | `semantics/methods.k:167` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule startsWith(.IntSeq, _:IntSeq)               => true` |
| 733 | `semantics/methods.k:168` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 734 | `semantics/methods.k:169` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| 735 | `semantics/operators.k:10` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 736 | `semantics/operators.k:12` | rule | none | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| 737 | `semantics/operators.k:15` | context | none | yes | SUPPLIED-FIXED / EXERCISED | `context Compare(HOLE, _)` |
| 738 | `semantics/operators.k:16` | context | none | yes | SUPPLIED-FIXED / EXERCISED | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 739 | `semantics/operators.k:17` | rule | owise | yes | SUPPLIED-FIXED / EXERCISED | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 740 | `semantics/operators.k:19` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("is",     V:Val, noneV) => V ==K noneV` |
| 741 | `semantics/operators.k:20` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| 742 | `semantics/operators.k:25` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 743 | `semantics/operators.k:28` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` |
| 744 | `semantics/operators.k:34` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| 745 | `semantics/operators.k:38` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| 746 | `semantics/operators.k:44` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 747 | `semantics/range.k:9` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 748 | `semantics/range.k:10` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 749 | `semantics/range.k:12` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 750 | `semantics/range.k:13` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| 751 | `semantics/range.k:15` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| 752 | `semantics/range.k:17` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| 753 | `semantics/range.k:20` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| 754 | `semantics/range.k:23` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| 755 | `semantics/set.k:8` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= setV(IntSeq)` |
| 756 | `semantics/set.k:11` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 757 | `semantics/set.k:12` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule codeIn(_:Int, .IntSeq)                => false` |
| 758 | `semantics/set.k:13` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| 759 | `semantics/set.k:16` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] \| dedupFrom(IntSeq, IntSeq)  [function, total]` |
| 760 | `semantics/set.k:18` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 761 | `semantics/set.k:19` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 762 | `semantics/set.k:20` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| 763 | `semantics/set.k:22` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| 764 | `semantics/set.k:25` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 765 | `semantics/set.k:26` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)` |
| 766 | `semantics/set.k:27` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| 767 | `semantics/set.k:31` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 768 | `semantics/set.k:32` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule subsetCodes(.IntSeq, _:IntSeq)                => true` |
| 769 | `semantics/set.k:33` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 770 | `semantics/set.k:35` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 771 | `semantics/set.k:36` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| 772 | `semantics/set.k:39` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| 773 | `semantics/sort.k:18` | syntax | function, no-evaluators, symbol(sortVS), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 774 | `semantics/sort.k:19` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 775 | `semantics/sort.k:20` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule sortVS(.ValSeq)                => .ValSeq          [concrete]` |
| 776 | `semantics/sort.k:21` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 777 | `semantics/sort.k:22` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]` |
| 778 | `semantics/sort.k:23` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 779 | `semantics/sort.k:24` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]` |
| 780 | `semantics/sort.k:26` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 781 | `semantics/sort.k:27` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 782 | `semantics/sort.k:28` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 783 | `semantics/sort.k:29` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| 784 | `semantics/sort.k:31` | rule | concrete | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` |
| 785 | `semantics/sort.k:36` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` |
| 786 | `semantics/sort.k:40` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` |
| 787 | `semantics/sort.k:49` | syntax | function, no-evaluators, symbol(sortKeyVS), total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 788 | `semantics/sort.k:51` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| 789 | `semantics/sort.k:53` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 790 | `semantics/sort.k:54` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 791 | `semantics/sort.k:55` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 792 | `semantics/sort.k:57` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 793 | `semantics/sort.k:58` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule condRev(S:ValSeq, false) => S` |
| 794 | `semantics/sort.k:59` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule condRev(S:ValSeq, true)  => revVS(S)` |
| 795 | `semantics/sort.k:61` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| 796 | `semantics/sort.k:63` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| 797 | `semantics/sort.k:65` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` |
| 798 | `semantics/str.k:8` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>` |
| 799 | `semantics/str.k:9` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` |
| 800 | `semantics/str.k:13` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= strToCodes(String) [function]` |
| 801 | `semantics/str.k:14` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 802 | `semantics/str.k:15` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strToCodes("") => .IntSeq` |
| 803 | `semantics/str.k:16` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` |
| 804 | `semantics/str.k:20` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 805 | `semantics/str.k:21` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule seqConcat(.IntSeq, T:IntSeq)                => T` |
| 806 | `semantics/str.k:22` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 807 | `semantics/str.k:24` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 808 | `semantics/str.k:25` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 809 | `semantics/str.k:26` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| 810 | `semantics/str.k:29` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 811 | `semantics/str.k:30` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 812 | `semantics/str.k:32` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 813 | `semantics/str.k:33` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strPrefix(.IntSeq, _:IntSeq)               => true` |
| 814 | `semantics/str.k:34` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 815 | `semantics/str.k:35` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 816 | `semantics/str.k:37` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 817 | `semantics/str.k:38` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)` |
| 818 | `semantics/str.k:39` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)` |
| 819 | `semantics/str.k:40` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` |
| 820 | `semantics/str.k:48` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 821 | `semantics/str.k:49` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strLt(.IntSeq, .IntSeq)                => false` |
| 822 | `semantics/str.k:50` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 823 | `semantics/str.k:51` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 824 | `semantics/str.k:52` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B` |
| 825 | `semantics/str.k:53` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B` |
| 826 | `semantics/str.k:54` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 827 | `semantics/str.k:56` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 828 | `semantics/str.k:57` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 829 | `semantics/str.k:58` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 830 | `semantics/str.k:59` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| 831 | `semantics/subscript.k:11` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 832 | `semantics/subscript.k:12` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V` |
| 833 | `semantics/subscript.k:13` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| 834 | `semantics/subscript.k:16` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 835 | `semantics/subscript.k:17` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C` |
| 836 | `semantics/subscript.k:18` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| 837 | `semantics/subscript.k:21` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 838 | `semantics/subscript.k:22` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 839 | `semantics/subscript.k:23` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0` |
| 840 | `semantics/subscript.k:27` | context | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `context Subscript(HOLE, _)` |
| 841 | `semantics/subscript.k:28` | context | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `context Subscript(_:Val, HOLE:Expr)` |
| 842 | `semantics/subscript.k:31` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 843 | `semantics/subscript.k:35` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 844 | `semantics/subscript.k:37` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 845 | `semantics/subscript.k:38` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 846 | `semantics/subscript.k:39` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 847 | `semantics/subscript.k:40` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` |
| 848 | `semantics/subscript.k:44` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| 849 | `semantics/subscript.k:49` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax OptInt ::= "noB" \| someB(Int)` |
| 850 | `semantics/subscript.k:50` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #evalB(NoBound)  => noB ... </k>` |
| 851 | `semantics/subscript.k:51` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>` |
| 852 | `semantics/subscript.k:52` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 853 | `semantics/subscript.k:54` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 854 | `semantics/subscript.k:55` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 855 | `semantics/subscript.k:56` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| 856 | `semantics/subscript.k:58` | rule | priority(45) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| 857 | `semantics/subscript.k:61` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 858 | `semantics/subscript.k:63` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 859 | `semantics/subscript.k:64` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 860 | `semantics/subscript.k:66` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 861 | `semantics/subscript.k:68` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` |
| 862 | `semantics/subscript.k:72` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= slStep(OptInt) [function, total]` |
| 863 | `semantics/subscript.k:73` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slStep(noB)          => 1` |
| 864 | `semantics/subscript.k:74` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slStep(someB(S:Int)) => S` |
| 865 | `semantics/subscript.k:76` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 866 | `semantics/subscript.k:77` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| 867 | `semantics/subscript.k:79` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0` |
| 868 | `semantics/subscript.k:81` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 869 | `semantics/subscript.k:83` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 870 | `semantics/subscript.k:84` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0` |
| 871 | `semantics/subscript.k:86` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| 872 | `semantics/subscript.k:88` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 873 | `semantics/subscript.k:90` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 874 | `semantics/subscript.k:91` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0` |
| 875 | `semantics/subscript.k:93` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| 876 | `semantics/subscript.k:96` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 877 | `semantics/subscript.k:97` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| 878 | `semantics/subscript.k:99` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| 879 | `semantics/subscript.k:102` | syntax | function, total | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 880 | `semantics/subscript.k:103` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN` |
| 881 | `semantics/subscript.k:105` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` |
| 882 | `semantics/subscript.k:109` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 883 | `semantics/subscript.k:110` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 884 | `semantics/subscript.k:113` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 885 | `semantics/subscript.k:116` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 886 | `semantics/subscript.k:117` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 887 | `semantics/subscript.k:120` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 888 | `semantics/syntax.k:9` | syntax | macro, seqstrict, strict | yes | SUPPLIED-FIXED / EXERCISED | `syntax Expr ::= "Int"      "(" Int ")" \| "Float"    "(" Float ")" \| "Bool"     "(" Bool ")" \| "Name"     "(" String ")" \| "Str"      "(" String ")" \| "UnaryOp"  "(" String "," Expr ")" [strict(2)] \| "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp"    "(" String "," Exprs ")" \| "ListExpr"  "(" Exprs ")" \| "DictExpr"  "(" Entries ")" \| "ListComp"  "(" Expr "," CompFors ")" [macro] \| "GenExp"    "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda"    "(" Params "," Expr ")" \| "KwArg"     "(" String "," Expr ")" \| "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call"      "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare"   "(" Expr "," CmpOp ")"` |
| 889 | `semantics/syntax.k:32` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"` |
| 890 | `semantics/syntax.k:33` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"` |
| 891 | `semantics/syntax.k:34` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Entries  ::= List{Entry, ","}` |
| 892 | `semantics/syntax.k:35` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 893 | `semantics/syntax.k:36` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax CompFors ::= List{CompFor, ""}` |
| 894 | `semantics/syntax.k:37` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax Exprs    ::= List{Expr, ","}` |
| 895 | `semantics/syntax.k:38` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 896 | `semantics/syntax.k:39` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Bound    ::= Expr \| "NoBound"` |
| 897 | `semantics/syntax.k:41` | syntax | strict | yes | SUPPLIED-FIXED / EXERCISED | `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] \| "Import"    "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While"     "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return"    "(" Expr ")" [strict] \| "Assert"    "(" Expr ")" [strict] \| "Expr"      "(" Expr ")" [strict] \| "FuncDef"   "(" String "," Params "," Stmts ")" \| "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` |
| 898 | `semantics/syntax.k:56` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax Stmts      ::= List{Stmt, ""}` |
| 899 | `semantics/syntax.k:57` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax Params     ::= "Params" "(" ParamNames ")"` |
| 900 | `semantics/syntax.k:58` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax CellVars   ::= "CellVars" "(" ParamNames ")"` |
| 901 | `semantics/syntax.k:59` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"` |
| 902 | `semantics/syntax.k:60` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax ParamNames ::= List{String, ","}` |
| 903 | `semantics/syntax.k:61` | syntax | none | yes | SUPPLIED-FIXED / EXERCISED | `syntax Module     ::= "Module" "(" Stmts ")"` |
| 904 | `semantics/tuple.k:10` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>` |
| 905 | `semantics/tuple.k:11` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| 906 | `semantics/tuple.k:14` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax ApplyK ::= "toTuple"` |
| 907 | `semantics/tuple.k:15` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 908 | `semantics/tuple.k:16` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 909 | `semantics/tuple.k:18` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| 910 | `semantics/tuple.k:20` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 911 | `semantics/tuple.k:21` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| 912 | `semantics/tuple.k:23` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 913 | `semantics/tuple.k:24` | syntax | function | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 914 | `semantics/tuple.k:25` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 915 | `semantics/tuple.k:26` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| 916 | `semantics/tuple.k:28` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| 917 | `semantics/tuple.k:31` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 918 | `semantics/tuple.k:32` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 919 | `semantics/tuple.k:35` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 920 | `semantics/tuple.k:42` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 921 | `semantics/tuple.k:43` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 922 | `semantics/tuple.k:44` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 923 | `semantics/tuple.k:49` | syntax | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 924 | `semantics/tuple.k:50` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 925 | `semantics/tuple.k:51` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 926 | `semantics/tuple.k:52` | rule | priority(40) | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 927 | `semantics/tuple.k:55` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| 928 | `semantics/tuple.k:57` | rule | none | no | SUPPLIED-FIXED / OUTSIDE DIRECTLY MAPPED SLICE | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| 929 | `verification.k:8` | syntax | function | no | PROOF-LOCAL DEFINITIONAL SUMMARY / REVIEWED SOUND | `syntax Int ::= fibFrom(Int, Int, Int, Int) [function]` |
| 930 | `verification.k:9` | rule | none | no | PROOF-LOCAL fibFrom EQUATION / REVIEWED SOUND | `rule fibFrom(A:Int, _B:Int, _C:Int, N:Int) => A requires N <=Int 0` |
| 931 | `verification.k:11` | rule | none | no | PROOF-LOCAL fibFrom EQUATION / REVIEWED SOUND | `rule fibFrom(A:Int, B:Int, C:Int, N:Int) => fibFrom(B, C, A +Int B +Int C, N -Int 1) requires N >Int 0` |
| 932 | `verification.k:17` | rule | simplification | no | PROOF-LOCAL ARITHMETIC SIMPLIFICATION / REVIEWED SOUND | `rule N:Int -Int (I:Int +Int 1) => N -Int I +Int -1 [simplification]` |
| 933 | `spec.k:6` | claim | none | no | AUXILIARY LOOP CIRCULARITY / MACHINE-CHECKED | `claim [fibfib-loop]: <k> #while(Compare(Name("i"), CmpOp("<", Name("n"))), Assign(Name("d"), BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("c")) Assign(Name("c"), Name("d")) Assign(Name("i"), BinOp("+", Name("i"), Int(1)))) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope( "a" \|-> (A:Int => fibFrom(A, B, C, N -Int I)) "b" \|-> (B:Int => ?_B:Int) "c" \|-> (C:Int => ?_C:Int) "d" \|-> (_D:Int => ?_D:Int) "i" \|-> (I:Int => N:Int) "n" \|-> N, _P:Parent) ... </scopes> requires 0 <=Int I andBool I <=Int N` |
| 934 | `spec.k:31` | claim | none | no | ENTRY TARGET / MACHINE-CHECKED | `claim [fibfib-correct]: <k> Call(Name("fibfib"), Int(N:Int)) => fibFrom(0, 0, 1, N) </k> <env> 0 </env> <scopes> 0 \|-> scope( "fibfib" \|-> closureVal( "n", .ParamNames, Assign(Name("a"), Int(0)) Assign(Name("b"), Int(0)) Assign(Name("c"), Int(1)) Assign(Name("i"), Int(0)) Assign(Name("d"), Int(0)) While(Compare(Name("i"), CmpOp("<", Name("n"))), Assign(Name("d"), BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("c")) Assign(Name("c"), Name("d")) Assign(Name("i"), BinOp("+", Name("i"), Int(1)))) Return(Name("a")), 0), parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> requires N >=Int 0` |
| 935 | `spec.k:66` | claim | none | no | GROUND SANITY CLAIM / MACHINE-CHECKED | `claim [example-1]: <k> fibFrom(0, 0, 1, 1) => 0 </k>` |
| 936 | `spec.k:69` | claim | none | no | GROUND SANITY CLAIM / MACHINE-CHECKED | `claim [example-5]: <k> fibFrom(0, 0, 1, 5) => 4 </k>` |
| 937 | `spec.k:72` | claim | none | no | GROUND SANITY CLAIM / MACHINE-CHECKED | `claim [example-8]: <k> fibFrom(0, 0, 1, 8) => 24 </k>` |

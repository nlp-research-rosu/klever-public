# Exhaustive K declaration and rule inventory

Scope: all `.k` files in the byte-identical supplied semantics tree, plus candidate `verification.k` and `spec.k`. Each entry identifies the complete source block by inclusive line range; `head` is only a compact preview.

Files: 26; declarations: 954; claim=1; configuration=1; context=5; rule=710; syntax=237

| # | source lines | kind | detected attributes | compact head | audit disposition |
|---:|---|---|---|---|---|
| 1 | `reference-semantics/semantics/assert.k:6-7` | rule | — | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 2 | `reference-semantics/semantics/assert.k:8-11` | rule | — | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 3 | `reference-semantics/semantics/assert.k:13-15` | rule | priority | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 4 | `reference-semantics/semantics/bool.k:8-8` | rule | — | `rule applyUn("not", V:Val) => notBool truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 5 | `reference-semantics/semantics/bool.k:10-10` | rule | — | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 6 | `reference-semantics/semantics/bool.k:11-11` | rule | — | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 7 | `reference-semantics/semantics/bool.k:16-16` | context | — | `context BoolOp(_, (HOLE:Expr, _:Exprs))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 8 | `reference-semantics/semantics/bool.k:17-17` | rule | — | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 9 | `reference-semantics/semantics/bool.k:18-19` | rule | — | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 10 | `reference-semantics/semantics/bool.k:20-21` | rule | — | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 11 | `reference-semantics/semantics/bool.k:22-23` | rule | — | `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 12 | `reference-semantics/semantics/bool.k:24-25` | rule | — | `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 13 | `reference-semantics/semantics/bool.k:29-30` | rule | priority | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 14 | `reference-semantics/semantics/bool.k:31-34` | rule | priority | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 15 | `reference-semantics/semantics/bool.k:35-38` | rule | priority | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 16 | `reference-semantics/semantics/bool.k:39-42` | rule | priority | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 17 | `reference-semantics/semantics/bool.k:43-46` | rule | priority | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 18 | `reference-semantics/semantics/builtins.k:17-17` | syntax | function | `syntax Val ::= applyBuiltin(String, Vals) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 19 | `reference-semantics/semantics/builtins.k:20-20` | syntax | function | `syntax Int ::= seqLen(Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 20 | `reference-semantics/semantics/builtins.k:21-21` | rule | — | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 21 | `reference-semantics/semantics/builtins.k:22-22` | rule | — | `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 22 | `reference-semantics/semantics/builtins.k:23-23` | rule | — | `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 23 | `reference-semantics/semantics/builtins.k:24-24` | rule | — | `rule seqLen(str(IS:IntSeq))                   => isLen(IS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 24 | `reference-semantics/semantics/builtins.k:25-25` | rule | — | `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 25 | `reference-semantics/semantics/builtins.k:26-26` | rule | — | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 26 | `reference-semantics/semantics/builtins.k:32-32` | rule | — | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 27 | `reference-semantics/semantics/builtins.k:33-33` | rule | — | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 28 | `reference-semantics/semantics/builtins.k:34-34` | rule | — | `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 29 | `reference-semantics/semantics/builtins.k:35-35` | rule | — | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 30 | `reference-semantics/semantics/builtins.k:36-36` | syntax | function,total | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 31 | `reference-semantics/semantics/builtins.k:37-37` | rule | — | `rule charsOf(.IntSeq)                => .ValSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 32 | `reference-semantics/semantics/builtins.k:38-38` | rule | — | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 33 | `reference-semantics/semantics/builtins.k:41-41` | rule | — | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 34 | `reference-semantics/semantics/builtins.k:44-44` | rule | — | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 35 | `reference-semantics/semantics/builtins.k:47-47` | syntax | — | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 36 | `reference-semantics/semantics/builtins.k:48-48` | rule | — | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 37 | `reference-semantics/semantics/builtins.k:49-49` | rule | — | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 38 | `reference-semantics/semantics/builtins.k:50-52` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 39 | `reference-semantics/semantics/builtins.k:54-54` | syntax | function | `syntax Int ::= intOf(Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 40 | `reference-semantics/semantics/builtins.k:55-55` | rule | — | `rule intOf(I:Int)  => I` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 41 | `reference-semantics/semantics/builtins.k:56-56` | rule | — | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 42 | `reference-semantics/semantics/builtins.k:59-59` | syntax | — | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 43 | `reference-semantics/semantics/builtins.k:60-60` | rule | — | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 44 | `reference-semantics/semantics/builtins.k:61-61` | rule | — | `rule <k> #iterDone ~> #allCont => true ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 45 | `reference-semantics/semantics/builtins.k:62-63` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 46 | `reference-semantics/semantics/builtins.k:64-65` | rule | — | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 47 | `reference-semantics/semantics/builtins.k:67-67` | syntax | — | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 48 | `reference-semantics/semantics/builtins.k:68-68` | rule | — | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 49 | `reference-semantics/semantics/builtins.k:69-69` | rule | — | `rule <k> #iterDone ~> #anyCont => false ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 50 | `reference-semantics/semantics/builtins.k:70-71` | rule | — | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 51 | `reference-semantics/semantics/builtins.k:72-73` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 52 | `reference-semantics/semantics/builtins.k:76-76` | syntax | — | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 53 | `reference-semantics/semantics/builtins.k:77-77` | rule | — | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 54 | `reference-semantics/semantics/builtins.k:78-79` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 55 | `reference-semantics/semantics/builtins.k:80-80` | rule | — | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 56 | `reference-semantics/semantics/builtins.k:81-81` | rule | — | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 57 | `reference-semantics/semantics/builtins.k:82-84` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 58 | `reference-semantics/semantics/builtins.k:86-86` | syntax | — | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 59 | `reference-semantics/semantics/builtins.k:87-87` | rule | — | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 60 | `reference-semantics/semantics/builtins.k:88-89` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 61 | `reference-semantics/semantics/builtins.k:90-90` | rule | — | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 62 | `reference-semantics/semantics/builtins.k:91-91` | rule | — | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 63 | `reference-semantics/semantics/builtins.k:92-94` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 64 | `reference-semantics/semantics/builtins.k:97-97` | syntax | function | `syntax Int ::= maxVals(Int, Vals) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 65 | `reference-semantics/semantics/builtins.k:98-98` | rule | — | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 66 | `reference-semantics/semantics/builtins.k:99-99` | rule | — | `rule maxVals(M:Int, .Vals)           => M` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 67 | `reference-semantics/semantics/builtins.k:100-100` | rule | — | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 68 | `reference-semantics/semantics/builtins.k:102-102` | syntax | function | `syntax Int ::= minVals(Int, Vals) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 69 | `reference-semantics/semantics/builtins.k:103-103` | rule | — | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 70 | `reference-semantics/semantics/builtins.k:104-104` | rule | — | `rule minVals(M:Int, .Vals)           => M` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 71 | `reference-semantics/semantics/builtins.k:105-105` | rule | — | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 72 | `reference-semantics/semantics/builtins.k:108-109` | rule | — | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 73 | `reference-semantics/semantics/builtins.k:111-113` | rule | — | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 74 | `reference-semantics/semantics/builtins.k:114-114` | syntax | function,total | `syntax IntSeq ::= binCodes(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 75 | `reference-semantics/semantics/builtins.k:115-115` | rule | — | `rule binCodes(0) => iCons(48, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 76 | `reference-semantics/semantics/builtins.k:116-116` | rule | — | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 77 | `reference-semantics/semantics/builtins.k:117-117` | syntax | function,total | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 78 | `reference-semantics/semantics/builtins.k:118-118` | rule | — | `rule binAcc(0, ACC:IntSeq) => ACC` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 79 | `reference-semantics/semantics/builtins.k:119-121` | rule | — | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 80 | `reference-semantics/semantics/builtins.k:124-125` | rule | — | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 81 | `reference-semantics/semantics/builtins.k:126-126` | syntax | function,total | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 82 | `reference-semantics/semantics/builtins.k:127-127` | rule | — | `rule enumVS(.ValSeq, _:Int) => .ValSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 83 | `reference-semantics/semantics/builtins.k:128-129` | rule | — | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 84 | `reference-semantics/semantics/builtins.k:132-133` | rule | — | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 85 | `reference-semantics/semantics/builtins.k:134-134` | syntax | function,total | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 86 | `reference-semantics/semantics/builtins.k:135-135` | rule | — | `rule mapStrVS(.ValSeq) => .ValSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 87 | `reference-semantics/semantics/builtins.k:136-136` | rule | — | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 88 | `reference-semantics/semantics/builtins.k:137-137` | rule | — | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 89 | `reference-semantics/semantics/builtins.k:140-140` | rule | — | `rule applyBuiltin("int", I:Int, .Vals) => I` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 90 | `reference-semantics/semantics/builtins.k:143-143` | rule | — | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 91 | `reference-semantics/semantics/builtins.k:144-145` | rule | — | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 92 | `reference-semantics/semantics/builtins.k:148-148` | rule | — | `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 93 | `reference-semantics/semantics/builtins.k:149-149` | rule | — | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 94 | `reference-semantics/semantics/builtins.k:152-153` | rule | — | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 95 | `reference-semantics/semantics/builtins.k:156-157` | rule | — | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 96 | `reference-semantics/semantics/builtins.k:158-158` | syntax | function,total | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 97 | `reference-semantics/semantics/builtins.k:159-159` | rule | — | `rule intDigAcc(.IntSeq, ACC:Int)             => ACC` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 98 | `reference-semantics/semantics/builtins.k:160-160` | rule | — | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 99 | `reference-semantics/semantics/builtins.k:163-163` | rule | — | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 100 | `reference-semantics/semantics/builtins.k:164-164` | rule | — | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 101 | `reference-semantics/semantics/builtins.k:167-168` | rule | — | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 102 | `reference-semantics/semantics/builtins.k:169-169` | rule | — | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 103 | `reference-semantics/semantics/builtins.k:170-170` | rule | — | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 104 | `reference-semantics/semantics/builtins.k:171-172` | rule | — | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 105 | `reference-semantics/semantics/builtins.k:173-173` | rule | — | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 106 | `reference-semantics/semantics/builtins.k:174-174` | rule | — | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 107 | `reference-semantics/semantics/builtins.k:177-177` | rule | — | `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 108 | `reference-semantics/semantics/builtins.k:178-178` | rule | — | `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 109 | `reference-semantics/semantics/builtins.k:179-180` | rule | — | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 110 | `reference-semantics/semantics/builtins.k:187-187` | rule | — | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 111 | `reference-semantics/semantics/builtins.k:188-188` | syntax | function | `syntax Int ::= evalArith(IntSeq) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 112 | `reference-semantics/semantics/builtins.k:189-190` | rule | — | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 113 | `reference-semantics/semantics/builtins.k:192-192` | syntax | — | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 114 | `reference-semantics/semantics/builtins.k:194-194` | syntax | function,total | `syntax Bool ::= evDigit(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 115 | `reference-semantics/semantics/builtins.k:195-195` | rule | — | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 116 | `reference-semantics/semantics/builtins.k:196-196` | syntax | function,total | `syntax Bool ::= evHead42(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 117 | `reference-semantics/semantics/builtins.k:197-197` | rule | — | `rule evHead42(iCons(42, _:IntSeq)) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 118 | `reference-semantics/semantics/builtins.k:198-198` | rule | owise | `rule evHead42(_:IntSeq)            => false [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 119 | `reference-semantics/semantics/builtins.k:199-199` | syntax | function,total | `syntax Bool ::= evHead47(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 120 | `reference-semantics/semantics/builtins.k:200-200` | rule | — | `rule evHead47(iCons(47, _:IntSeq)) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 121 | `reference-semantics/semantics/builtins.k:201-201` | rule | owise | `rule evHead47(_:IntSeq)            => false [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 122 | `reference-semantics/semantics/builtins.k:203-203` | syntax | function,total | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 123 | `reference-semantics/semantics/builtins.k:204-204` | rule | — | `rule tokOps(.IntSeq)                 => .OpSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 124 | `reference-semantics/semantics/builtins.k:205-205` | rule | — | `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 125 | `reference-semantics/semantics/builtins.k:206-206` | rule | — | `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 126 | `reference-semantics/semantics/builtins.k:207-207` | rule | — | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 127 | `reference-semantics/semantics/builtins.k:208-208` | rule | — | `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 128 | `reference-semantics/semantics/builtins.k:209-209` | rule | — | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 129 | `reference-semantics/semantics/builtins.k:210-210` | rule | — | `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 130 | `reference-semantics/semantics/builtins.k:211-211` | rule | — | `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 131 | `reference-semantics/semantics/builtins.k:212-212` | rule | — | `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 132 | `reference-semantics/semantics/builtins.k:214-215` | syntax | function,total | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 133 | `reference-semantics/semantics/builtins.k:216-216` | rule | — | `rule tokNds(.IntSeq)                => .IntSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 134 | `reference-semantics/semantics/builtins.k:217-217` | rule | — | `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 135 | `reference-semantics/semantics/builtins.k:218-218` | rule | — | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 136 | `reference-semantics/semantics/builtins.k:219-220` | rule | — | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 137 | `reference-semantics/semantics/builtins.k:221-222` | rule | — | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 138 | `reference-semantics/semantics/builtins.k:223-223` | rule | owise | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 139 | `reference-semantics/semantics/builtins.k:225-225` | syntax | — | `syntax EvPair ::= evp(OpSeq, IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 140 | `reference-semantics/semantics/builtins.k:226-226` | syntax | function,total | `syntax Int ::= firstNdE(EvPair) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 141 | `reference-semantics/semantics/builtins.k:227-227` | rule | — | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 142 | `reference-semantics/semantics/builtins.k:228-228` | rule | owise | `rule firstNdE(_:EvPair) => 0 [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 143 | `reference-semantics/semantics/builtins.k:230-230` | syntax | function,total | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 144 | `reference-semantics/semantics/builtins.k:231-231` | rule | — | `rule applyOpE("+",  A:Int, B:Int) => A +Int B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 145 | `reference-semantics/semantics/builtins.k:232-232` | rule | — | `rule applyOpE("-",  A:Int, B:Int) => A -Int B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 146 | `reference-semantics/semantics/builtins.k:233-233` | rule | — | `rule applyOpE("*",  A:Int, B:Int) => A *Int B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 147 | `reference-semantics/semantics/builtins.k:234-234` | rule | — | `rule applyOpE("//", A:Int, B:Int) => A divInt B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 148 | `reference-semantics/semantics/builtins.k:235-235` | rule | — | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 149 | `reference-semantics/semantics/builtins.k:236-236` | rule | owise | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 150 | `reference-semantics/semantics/builtins.k:238-238` | syntax | function,total | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 151 | `reference-semantics/semantics/builtins.k:239-239` | rule | — | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 152 | `reference-semantics/semantics/builtins.k:240-240` | rule | — | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 153 | `reference-semantics/semantics/builtins.k:241-242` | rule | — | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 154 | `reference-semantics/semantics/builtins.k:243-243` | rule | owise | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 155 | `reference-semantics/semantics/builtins.k:244-244` | syntax | function,total | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 156 | `reference-semantics/semantics/builtins.k:245-245` | rule | — | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 157 | `reference-semantics/semantics/builtins.k:246-246` | rule | — | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 158 | `reference-semantics/semantics/builtins.k:247-247` | syntax | function,total | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 159 | `reference-semantics/semantics/builtins.k:248-248` | rule | — | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 160 | `reference-semantics/semantics/builtins.k:250-250` | syntax | function,total | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 161 | `reference-semantics/semantics/builtins.k:251-251` | rule | — | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 162 | `reference-semantics/semantics/builtins.k:252-252` | rule | — | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 163 | `reference-semantics/semantics/builtins.k:253-253` | rule | — | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 164 | `reference-semantics/semantics/builtins.k:254-254` | rule | — | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 165 | `reference-semantics/semantics/builtins.k:255-255` | syntax | function,total | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 166 | `reference-semantics/semantics/builtins.k:256-256` | rule | — | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 167 | `reference-semantics/semantics/builtins.k:257-259` | rule | — | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 168 | `reference-semantics/semantics/builtins.k:260-262` | rule | — | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 169 | `reference-semantics/semantics/builtins.k:263-264` | rule | owise | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 170 | `reference-semantics/semantics/builtins.k:265-265` | syntax | function,total | `syntax Bool ::= inLevelE(String, String) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 171 | `reference-semantics/semantics/builtins.k:266-266` | rule | — | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 172 | `reference-semantics/semantics/builtins.k:267-267` | rule | — | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 173 | `reference-semantics/semantics/builtins.k:268-268` | rule | owise | `rule inLevelE(_:String, _:String) => false [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 174 | `reference-semantics/semantics/builtins.k:269-269` | syntax | function,total | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 175 | `reference-semantics/semantics/builtins.k:270-270` | rule | — | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 176 | `reference-semantics/semantics/builtins.k:271-271` | rule | — | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 177 | `reference-semantics/semantics/builtins.k:272-272` | syntax | function,total | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 178 | `reference-semantics/semantics/builtins.k:273-273` | rule | — | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 179 | `reference-semantics/semantics/builtins.k:274-274` | rule | — | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 180 | `reference-semantics/semantics/builtins.k:279-279` | syntax | — | `syntax KItem ::= "#md5"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 181 | `reference-semantics/semantics/builtins.k:280-281` | rule | priority | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 182 | `reference-semantics/semantics/builtins.k:282-282` | rule | — | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 183 | `reference-semantics/semantics/builtins.k:283-283` | syntax | — | `syntax Val ::= md5Obj(IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 184 | `reference-semantics/semantics/builtins.k:284-284` | rule | — | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 185 | `reference-semantics/semantics/builtins.k:285-285` | syntax | function,total,symbol | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 186 | `reference-semantics/semantics/builtins.k:291-291` | rule | — | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 187 | `reference-semantics/semantics/builtins.k:292-292` | rule | — | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 188 | `reference-semantics/semantics/builtins.k:293-293` | syntax | function | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 189 | `reference-semantics/semantics/builtins.k:294-294` | rule | — | `rule isIntV(_:Int)         => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 190 | `reference-semantics/semantics/builtins.k:295-295` | rule | owise | `rule isIntV(_:Val)         => false [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 191 | `reference-semantics/semantics/builtins.k:296-296` | rule | — | `rule isStrV(str(_:IntSeq)) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 192 | `reference-semantics/semantics/builtins.k:297-297` | rule | owise | `rule isStrV(_:Val)         => false [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 193 | `reference-semantics/semantics/call.k:16-16` | rule | — | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 194 | `reference-semantics/semantics/call.k:19-19` | syntax | — | `syntax KItem ::= #callee(Exprs)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 195 | `reference-semantics/semantics/call.k:20-20` | rule | owise | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 196 | `reference-semantics/semantics/call.k:21-21` | rule | — | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 197 | `reference-semantics/semantics/call.k:24-24` | rule | — | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 198 | `reference-semantics/semantics/call.k:26-26` | rule | — | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 199 | `reference-semantics/semantics/call.k:27-27` | rule | — | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 200 | `reference-semantics/semantics/call.k:28-28` | rule | — | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 201 | `reference-semantics/semantics/call.k:29-29` | rule | — | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 202 | `reference-semantics/semantics/call.k:30-30` | rule | — | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 203 | `reference-semantics/semantics/call.k:31-31` | rule | owise | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 204 | `reference-semantics/semantics/call.k:32-32` | rule | — | `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 205 | `reference-semantics/semantics/call.k:38-41` | rule | priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 206 | `reference-semantics/semantics/call.k:42-46` | rule | priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 207 | `reference-semantics/semantics/call.k:47-50` | rule | priority | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 208 | `reference-semantics/semantics/call.k:52-52` | syntax | function,total | `syntax Bool ::= isMutMethod(String) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 209 | `reference-semantics/semantics/call.k:53-55` | rule | — | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 210 | `reference-semantics/semantics/call.k:56-60` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 211 | `reference-semantics/semantics/call.k:63-67` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 212 | `reference-semantics/semantics/call.k:69-74` | rule | — | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 213 | `reference-semantics/semantics/call.k:80-85` | rule | — | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE ` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 214 | `reference-semantics/semantics/call.k:87-87` | syntax | — | `syntax KItem ::= #allocCells(ParamNames)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 215 | `reference-semantics/semantics/call.k:88-88` | rule | — | `rule <k> #allocCells(.ParamNames) => .K ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 216 | `reference-semantics/semantics/call.k:89-94` | rule | — | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N ` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 217 | `reference-semantics/semantics/comprehension.k:11-11` | rule | — | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 218 | `reference-semantics/semantics/comprehension.k:12-12` | rule | — | `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 219 | `reference-semantics/semantics/comprehension.k:14-14` | syntax | macro | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 220 | `reference-semantics/semantics/comprehension.k:15-16` | rule | — | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 221 | `reference-semantics/semantics/comprehension.k:18-18` | syntax | macro | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 222 | `reference-semantics/semantics/comprehension.k:19-20` | rule | — | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 223 | `reference-semantics/semantics/comprehension.k:21-22` | rule | — | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 224 | `reference-semantics/semantics/comprehension.k:24-24` | syntax | macro | `syntax Expr ::= compGuard(Exprs) [macro]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 225 | `reference-semantics/semantics/comprehension.k:25-25` | rule | — | `rule compGuard(.Exprs)             => Bool(true)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 226 | `reference-semantics/semantics/comprehension.k:26-26` | rule | — | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 227 | `reference-semantics/semantics/concrete.k:13-15` | rule | — | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 228 | `reference-semantics/semantics/concrete.k:16-18` | rule | — | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 229 | `reference-semantics/semantics/concrete.k:25-25` | syntax | — | `syntax Val ::= kvP(Val, Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 230 | `reference-semantics/semantics/concrete.k:26-27` | syntax | — | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 231 | `reference-semantics/semantics/concrete.k:28-30` | rule | priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 232 | `reference-semantics/semantics/concrete.k:31-33` | rule | priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 233 | `reference-semantics/semantics/concrete.k:34-35` | rule | — | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 234 | `reference-semantics/semantics/concrete.k:36-37` | rule | — | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 235 | `reference-semantics/semantics/concrete.k:38-40` | rule | — | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 236 | `reference-semantics/semantics/concrete.k:42-42` | syntax | function | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 237 | `reference-semantics/semantics/concrete.k:43-43` | rule | — | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 238 | `reference-semantics/semantics/concrete.k:44-46` | rule | — | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 239 | `reference-semantics/semantics/concrete.k:47-49` | rule | — | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 240 | `reference-semantics/semantics/concrete.k:51-51` | syntax | function | `syntax Bool ::= kLt(Val, Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 241 | `reference-semantics/semantics/concrete.k:52-52` | rule | — | `rule kLt(I1:Int, I2:Int)             => I1 <Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 242 | `reference-semantics/semantics/concrete.k:53-53` | rule | — | `rule kLt(F1:Float, F2:Float)         => F1 <Float F2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 243 | `reference-semantics/semantics/concrete.k:54-54` | rule | — | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 244 | `reference-semantics/semantics/concrete.k:56-56` | syntax | function,total | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 245 | `reference-semantics/semantics/concrete.k:57-57` | rule | — | `rule unpairVS(.ValSeq) => .ValSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 246 | `reference-semantics/semantics/concrete.k:58-58` | rule | — | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 247 | `reference-semantics/semantics/concrete.k:59-59` | rule | owise | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 248 | `reference-semantics/semantics/controls.k:9-11` | rule | — | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 249 | `reference-semantics/semantics/controls.k:12-18` | rule | priority | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 250 | `reference-semantics/semantics/controls.k:20-23` | rule | — | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 251 | `reference-semantics/semantics/controls.k:27-31` | rule | priority | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 252 | `reference-semantics/semantics/controls.k:35-35` | rule | — | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 253 | `reference-semantics/semantics/controls.k:36-36` | rule | owise | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 254 | `reference-semantics/semantics/controls.k:37-37` | syntax | — | `syntax KItem ::= #bindImports(ParamNames)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 255 | `reference-semantics/semantics/controls.k:38-38` | rule | — | `rule <k> #bindImports(.ParamNames) => .K ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 256 | `reference-semantics/semantics/controls.k:39-42` | rule | — | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 257 | `reference-semantics/semantics/controls.k:43-44` | rule | — | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 258 | `reference-semantics/semantics/controls.k:48-48` | rule | — | `rule <k> Expr(_:Val) => .K ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 259 | `reference-semantics/semantics/controls.k:51-51` | syntax | — | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 260 | `reference-semantics/semantics/controls.k:52-52` | rule | — | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 261 | `reference-semantics/semantics/controls.k:53-53` | rule | — | `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 262 | `reference-semantics/semantics/controls.k:54-54` | rule | — | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 263 | `reference-semantics/semantics/controls.k:57-58` | rule | — | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 264 | `reference-semantics/semantics/controls.k:59-60` | rule | — | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 265 | `reference-semantics/semantics/controls.k:65-67` | syntax | — | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 266 | `reference-semantics/semantics/controls.k:69-69` | rule | — | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 267 | `reference-semantics/semantics/controls.k:71-71` | rule | — | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 268 | `reference-semantics/semantics/controls.k:72-72` | rule | — | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 269 | `reference-semantics/semantics/controls.k:73-74` | rule | — | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 270 | `reference-semantics/semantics/controls.k:77-77` | rule | — | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 271 | `reference-semantics/semantics/controls.k:78-78` | rule | — | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 272 | `reference-semantics/semantics/controls.k:79-80` | rule | — | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 273 | `reference-semantics/semantics/controls.k:81-82` | rule | — | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 274 | `reference-semantics/semantics/controls.k:85-85` | rule | — | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 275 | `reference-semantics/semantics/controls.k:86-86` | rule | — | `rule <k> Continue => #cont ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 276 | `reference-semantics/semantics/controls.k:87-87` | rule | — | `rule <k> Break => #brk ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 277 | `reference-semantics/semantics/controls.k:88-88` | rule | — | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 278 | `reference-semantics/semantics/controls.k:89-89` | rule | owise | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 279 | `reference-semantics/semantics/controls.k:90-90` | rule | — | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 280 | `reference-semantics/semantics/controls.k:91-91` | rule | owise | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 281 | `reference-semantics/semantics/controls.k:95-97` | rule | priority | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 282 | `reference-semantics/semantics/controls.k:98-100` | rule | priority | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 283 | `reference-semantics/semantics/controls.k:101-103` | rule | priority | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 284 | `reference-semantics/semantics/controls.k:106-108` | rule | priority | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 285 | `reference-semantics/semantics/core.k:13-13` | syntax | — | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 286 | `reference-semantics/semantics/core.k:14-14` | syntax | — | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 287 | `reference-semantics/semantics/core.k:15-15` | syntax | — | `syntax Str    ::= str(IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 288 | `reference-semantics/semantics/core.k:18-23` | syntax | — | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 289 | `reference-semantics/semantics/core.k:25-34` | syntax | function | `syntax Val      ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int)          // a heap object: <heap> holds its list(VS) \| cellRef(Int)      // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String)     // a t` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 290 | `reference-semantics/semantics/core.k:36-36` | syntax | — | `syntax Parent   ::= "root" \| parent(Int)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 291 | `reference-semantics/semantics/core.k:37-37` | syntax | — | `syntax Scope    ::= scope(Map, Parent)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 292 | `reference-semantics/semantics/core.k:38-38` | syntax | — | `syntax KResult  ::= Val` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 293 | `reference-semantics/semantics/core.k:39-39` | syntax | — | `syntax Expr     ::= Val   // cooling puts results back into expression holes` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 294 | `reference-semantics/semantics/core.k:40-40` | syntax | — | `syntax Vals     ::= List{Val, ","}` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 295 | `reference-semantics/semantics/core.k:41-41` | syntax | — | `syntax Exc      ::= "NoExc" \| "AssertionError"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 296 | `reference-semantics/semantics/core.k:42-42` | syntax | — | `syntax RetState ::= "noRet" \| retV(Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 297 | `reference-semantics/semantics/core.k:49-60` | configuration | — | `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     \|-> scope(.Map, parent(-1)) -1    \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </st` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 298 | `reference-semantics/semantics/core.k:68-68` | syntax | function,total | `syntax Bool ::= isRefV(Val) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 299 | `reference-semantics/semantics/core.k:69-69` | rule | — | `rule isRefV(ref(_:Int)) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 300 | `reference-semantics/semantics/core.k:70-70` | rule | owise | `rule isRefV(_:Val)      => false [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 301 | `reference-semantics/semantics/core.k:75-75` | syntax | — | `syntax HeapVal ::= cellV(Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 302 | `reference-semantics/semantics/core.k:76-76` | syntax | function,total | `syntax Bool ::= isCellRef(Val) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 303 | `reference-semantics/semantics/core.k:77-77` | rule | — | `rule isCellRef(cellRef(_:Int)) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 304 | `reference-semantics/semantics/core.k:78-78` | rule | owise | `rule isCellRef(_:Val)          => false [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 305 | `reference-semantics/semantics/core.k:85-90` | rule | priority | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 306 | `reference-semantics/semantics/core.k:95-95` | syntax | — | `syntax Val ::= kwV(String, Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 307 | `reference-semantics/semantics/core.k:96-96` | syntax | — | `syntax KItem ::= #kwTag(String)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 308 | `reference-semantics/semantics/core.k:97-97` | rule | — | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 309 | `reference-semantics/semantics/core.k:98-99` | rule | — | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 310 | `reference-semantics/semantics/core.k:100-100` | syntax | function,total | `syntax Bool ::= isKwV(Val) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 311 | `reference-semantics/semantics/core.k:101-101` | rule | — | `rule isKwV(kwV(_:String, _:Val)) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 312 | `reference-semantics/semantics/core.k:102-102` | rule | owise | `rule isKwV(_:Val)                => false [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 313 | `reference-semantics/semantics/core.k:106-106` | syntax | — | `syntax Val ::= cellsMark(ParamNames)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 314 | `reference-semantics/semantics/core.k:107-107` | syntax | function | `syntax ParamNames ::= cellsOf(Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 315 | `reference-semantics/semantics/core.k:108-108` | rule | — | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 316 | `reference-semantics/semantics/core.k:109-109` | syntax | function,total | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 317 | `reference-semantics/semantics/core.k:110-110` | rule | — | `rule pnMember(_:String, .ParamNames) => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 318 | `reference-semantics/semantics/core.k:111-111` | rule | — | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 319 | `reference-semantics/semantics/core.k:113-113` | syntax | — | `syntax KItem ::= #cellW(Val, Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 320 | `reference-semantics/semantics/core.k:114-115` | rule | — | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 321 | `reference-semantics/semantics/core.k:117-117` | syntax | — | `syntax KItem ::= #alloc(Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 322 | `reference-semantics/semantics/core.k:118-121` | rule | — | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 323 | `reference-semantics/semantics/core.k:124-124` | syntax | — | `syntax KItem ::= #loadAll(Module)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 324 | `reference-semantics/semantics/core.k:125-125` | rule | — | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 325 | `reference-semantics/semantics/core.k:126-126` | rule | — | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 326 | `reference-semantics/semantics/core.k:127-127` | rule | — | `rule <k> .Stmts => .K ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 327 | `reference-semantics/semantics/core.k:130-130` | syntax | — | `syntax KItem ::= #look(String, Int)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 328 | `reference-semantics/semantics/core.k:131-131` | rule | — | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 329 | `reference-semantics/semantics/core.k:132-134` | rule | — | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 330 | `reference-semantics/semantics/core.k:145-151` | rule | priority | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 331 | `reference-semantics/semantics/core.k:152-154` | rule | — | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 332 | `reference-semantics/semantics/core.k:157-157` | syntax | function,total | `syntax Scope ::= "builtinsScope" [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 333 | `reference-semantics/semantics/core.k:158-181` | rule | — | `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")   ` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 334 | `reference-semantics/semantics/core.k:185-185` | syntax | — | `syntax ApplyK ::= toCall(Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 335 | `reference-semantics/semantics/core.k:186-188` | syntax | — | `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 336 | `reference-semantics/semantics/core.k:189-189` | rule | — | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 337 | `reference-semantics/semantics/core.k:190-190` | rule | — | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 338 | `reference-semantics/semantics/core.k:191-191` | rule | — | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 339 | `reference-semantics/semantics/core.k:194-194` | rule | — | `rule <k> Int(I:Int)   => I ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 340 | `reference-semantics/semantics/core.k:195-195` | rule | — | `rule <k> Bool(B:Bool) => B ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 341 | `reference-semantics/semantics/core.k:196-196` | rule | — | `rule <k> NoneVal      => noneV ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 342 | `reference-semantics/semantics/core.k:199-199` | syntax | function | `syntax Bool ::= truthy(Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 343 | `reference-semantics/semantics/core.k:200-200` | rule | — | `rule truthy(B:Bool)          => B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 344 | `reference-semantics/semantics/core.k:201-201` | rule | — | `rule truthy(noneV)           => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 345 | `reference-semantics/semantics/core.k:202-202` | rule | — | `rule truthy(I:Int)           => I =/=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 346 | `reference-semantics/semantics/core.k:203-203` | rule | — | `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 347 | `reference-semantics/semantics/core.k:204-204` | rule | — | `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 348 | `reference-semantics/semantics/core.k:205-205` | rule | — | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 349 | `reference-semantics/semantics/core.k:208-208` | syntax | function | `syntax Val  ::= applyUn(String, Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 350 | `reference-semantics/semantics/core.k:209-209` | syntax | function | `syntax Val  ::= applyBin(String, Val, Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 351 | `reference-semantics/semantics/core.k:210-210` | syntax | function | `syntax Bool ::= applyCmp(String, Val, Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 352 | `reference-semantics/semantics/core.k:213-213` | syntax | function,total | `syntax Vals ::= appendVal(Vals, Val) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 353 | `reference-semantics/semantics/core.k:214-214` | rule | — | `rule appendVal(.Vals, V:Val)              => V , .Vals` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 354 | `reference-semantics/semantics/core.k:215-215` | rule | — | `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 355 | `reference-semantics/semantics/core.k:217-217` | syntax | function,total | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 356 | `reference-semantics/semantics/core.k:218-218` | rule | — | `rule vals2valSeq(.Vals)            => .ValSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 357 | `reference-semantics/semantics/core.k:219-219` | rule | — | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 358 | `reference-semantics/semantics/core.k:223-223` | syntax | function,total | `syntax Int ::= vsLen(ValSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 359 | `reference-semantics/semantics/core.k:224-224` | rule | — | `rule vsLen(.ValSeq)                => 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 360 | `reference-semantics/semantics/core.k:225-225` | rule | — | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 361 | `reference-semantics/semantics/core.k:227-227` | syntax | function,total | `syntax Int ::= isLen(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 362 | `reference-semantics/semantics/core.k:228-228` | rule | — | `rule isLen(.IntSeq)                => 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 363 | `reference-semantics/semantics/core.k:229-229` | rule | — | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 364 | `reference-semantics/semantics/core.k:233-233` | syntax | function,total | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 365 | `reference-semantics/semantics/core.k:234-234` | rule | — | `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 366 | `reference-semantics/semantics/core.k:235-235` | rule | — | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 367 | `reference-semantics/semantics/core.k:236-237` | rule | — | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 368 | `reference-semantics/semantics/core.k:238-239` | rule | — | `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 369 | `reference-semantics/semantics/dict.k:20-20` | syntax | — | `syntax Val ::= dictV(ValSeq, ValSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 370 | `reference-semantics/semantics/dict.k:23-25` | syntax | — | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 371 | `reference-semantics/semantics/dict.k:26-26` | rule | — | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 372 | `reference-semantics/semantics/dict.k:27-27` | rule | — | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 373 | `reference-semantics/semantics/dict.k:28-29` | rule | — | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 374 | `reference-semantics/semantics/dict.k:30-31` | rule | — | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 375 | `reference-semantics/semantics/dict.k:32-33` | rule | — | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 376 | `reference-semantics/semantics/dict.k:37-37` | syntax | function,total | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 377 | `reference-semantics/semantics/dict.k:38-38` | rule | — | `rule dHasKey(.ValSeq, _:Val)                => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 378 | `reference-semantics/semantics/dict.k:39-39` | rule | — | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 379 | `reference-semantics/semantics/dict.k:40-40` | rule | — | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 380 | `reference-semantics/semantics/dict.k:43-43` | syntax | function,total | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 381 | `reference-semantics/semantics/dict.k:44-44` | rule | — | `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 382 | `reference-semantics/semantics/dict.k:45-45` | rule | — | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 383 | `reference-semantics/semantics/dict.k:49-49` | syntax | function,total | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 384 | `reference-semantics/semantics/dict.k:50-51` | rule | — | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 385 | `reference-semantics/semantics/dict.k:52-53` | rule | — | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 386 | `reference-semantics/semantics/dict.k:54-54` | rule | owise | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 387 | `reference-semantics/semantics/dict.k:58-60` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 388 | `reference-semantics/semantics/dict.k:63-63` | rule | — | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 389 | `reference-semantics/semantics/dict.k:64-64` | syntax | function | `syntax Val ::= applyIndexD(Val, Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 390 | `reference-semantics/semantics/dict.k:65-66` | rule | priority | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 391 | `reference-semantics/semantics/dict.k:70-70` | syntax | function | `syntax Val ::= dictSet(Val, Val, Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 392 | `reference-semantics/semantics/dict.k:71-71` | rule | — | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 393 | `reference-semantics/semantics/dict.k:76-76` | syntax | — | `syntax KItem ::= #dsetK(String, Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 394 | `reference-semantics/semantics/dict.k:77-77` | rule | — | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 395 | `reference-semantics/semantics/dict.k:78-81` | rule | — | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 396 | `reference-semantics/semantics/dict.k:82-85` | rule | — | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 397 | `reference-semantics/semantics/dict.k:86-86` | syntax | — | `syntax KItem ::= #dsetV(Val, Val, Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 398 | `reference-semantics/semantics/dict.k:87-88` | rule | — | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 399 | `reference-semantics/semantics/dict.k:90-90` | syntax | function,total | `syntax Int ::= normIdxD(Int, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 400 | `reference-semantics/semantics/dict.k:91-91` | rule | — | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 401 | `reference-semantics/semantics/dict.k:92-92` | rule | — | `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 402 | `reference-semantics/semantics/dict.k:95-96` | rule | — | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 403 | `reference-semantics/semantics/dict.k:97-97` | syntax | function | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 404 | `reference-semantics/semantics/dict.k:98-98` | rule | — | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 405 | `reference-semantics/semantics/dict.k:99-100` | rule | — | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 406 | `reference-semantics/semantics/dict.k:101-101` | syntax | function | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 407 | `reference-semantics/semantics/dict.k:102-102` | rule | — | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 408 | `reference-semantics/semantics/dict.k:103-103` | rule | — | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 409 | `reference-semantics/semantics/float.k:20-20` | syntax | — | `syntax Val ::= Float` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 410 | `reference-semantics/semantics/float.k:21-21` | rule | — | `rule <k> Float(F:Float) => F ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 411 | `reference-semantics/semantics/float.k:24-24` | syntax | function,total,symbol | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 412 | `reference-semantics/semantics/float.k:25-25` | rule | concrete | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 413 | `reference-semantics/semantics/float.k:27-27` | rule | — | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 414 | `reference-semantics/semantics/float.k:30-30` | syntax | function,total,symbol | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 415 | `reference-semantics/semantics/float.k:31-31` | rule | concrete | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 416 | `reference-semantics/semantics/float.k:32-32` | rule | — | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 417 | `reference-semantics/semantics/float.k:37-37` | syntax | function,total,symbol | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 418 | `reference-semantics/semantics/float.k:38-38` | rule | concrete | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 419 | `reference-semantics/semantics/float.k:39-39` | rule | — | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 420 | `reference-semantics/semantics/float.k:43-43` | rule | — | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 421 | `reference-semantics/semantics/float.k:44-44` | rule | — | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 422 | `reference-semantics/semantics/float.k:50-50` | syntax | function,total,symbol | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 423 | `reference-semantics/semantics/float.k:51-51` | rule | concrete | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 424 | `reference-semantics/semantics/float.k:52-52` | rule | — | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 425 | `reference-semantics/semantics/float.k:54-54` | syntax | function,total,symbol | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 426 | `reference-semantics/semantics/float.k:55-55` | rule | concrete | `rule absF(F:Float) => absFloat(F) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 427 | `reference-semantics/semantics/float.k:56-56` | rule | — | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 428 | `reference-semantics/semantics/float.k:61-61` | rule | — | `rule <k> Import(_:String) => .K ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 429 | `reference-semantics/semantics/float.k:65-65` | syntax | — | `syntax KItem ::= "#mathCeil"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 430 | `reference-semantics/semantics/float.k:66-66` | rule | priority | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 431 | `reference-semantics/semantics/float.k:67-67` | rule | — | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 432 | `reference-semantics/semantics/float.k:70-70` | syntax | — | `syntax KItem ::= "#mathFloor"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 433 | `reference-semantics/semantics/float.k:71-71` | rule | priority | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 434 | `reference-semantics/semantics/float.k:72-72` | rule | — | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 435 | `reference-semantics/semantics/float.k:73-73` | syntax | function,total,symbol | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 436 | `reference-semantics/semantics/float.k:74-74` | rule | concrete | `rule floorFI(I:Int)   => I                        [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 437 | `reference-semantics/semantics/float.k:75-75` | rule | concrete | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 438 | `reference-semantics/semantics/float.k:78-78` | rule | — | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 439 | `reference-semantics/semantics/float.k:79-79` | rule | — | `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 440 | `reference-semantics/semantics/float.k:82-82` | syntax | — | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 441 | `reference-semantics/semantics/float.k:83-83` | rule | priority | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 442 | `reference-semantics/semantics/float.k:84-84` | rule | — | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 443 | `reference-semantics/semantics/float.k:85-85` | rule | — | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 444 | `reference-semantics/semantics/float.k:86-86` | syntax | function,total,symbol | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 445 | `reference-semantics/semantics/float.k:87-87` | rule | concrete | `rule toF(F:Float) => F        [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 446 | `reference-semantics/semantics/float.k:88-88` | rule | concrete | `rule toF(I:Int)   => intToF(I) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 447 | `reference-semantics/semantics/float.k:93-93` | syntax | function,total,symbol | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 448 | `reference-semantics/semantics/float.k:94-94` | rule | concrete | `rule ceilF(I:Int)   => I                       [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 449 | `reference-semantics/semantics/float.k:95-95` | rule | concrete | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 450 | `reference-semantics/semantics/float.k:99-99` | rule | — | `rule applyUn("-", F:Float) => 0.0 -Float F` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 451 | `reference-semantics/semantics/float.k:103-103` | syntax | function,total,symbol | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 452 | `reference-semantics/semantics/float.k:104-104` | rule | concrete | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 453 | `reference-semantics/semantics/float.k:105-105` | rule | — | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 454 | `reference-semantics/semantics/float.k:107-107` | syntax | function,total,symbol | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 455 | `reference-semantics/semantics/float.k:108-108` | rule | concrete | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 456 | `reference-semantics/semantics/float.k:109-109` | rule | — | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 457 | `reference-semantics/semantics/float.k:111-111` | syntax | function,total,symbol | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 458 | `reference-semantics/semantics/float.k:112-112` | rule | concrete | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 459 | `reference-semantics/semantics/float.k:113-113` | rule | — | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 460 | `reference-semantics/semantics/float.k:115-115` | syntax | function,total,symbol | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 461 | `reference-semantics/semantics/float.k:116-116` | rule | concrete | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 462 | `reference-semantics/semantics/float.k:117-117` | rule | — | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 463 | `reference-semantics/semantics/float.k:119-119` | syntax | function,total,symbol | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 464 | `reference-semantics/semantics/float.k:120-120` | rule | concrete | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 465 | `reference-semantics/semantics/float.k:121-121` | rule | — | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 466 | `reference-semantics/semantics/float.k:125-125` | syntax | function,total,symbol | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 467 | `reference-semantics/semantics/float.k:126-126` | rule | concrete | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 468 | `reference-semantics/semantics/float.k:127-127` | rule | — | `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 469 | `reference-semantics/semantics/float.k:128-128` | rule | — | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 470 | `reference-semantics/semantics/float.k:129-129` | rule | — | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 471 | `reference-semantics/semantics/float.k:132-132` | rule | — | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 472 | `reference-semantics/semantics/float.k:133-133` | rule | — | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 473 | `reference-semantics/semantics/float.k:134-134` | rule | — | `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 474 | `reference-semantics/semantics/float.k:135-135` | rule | — | `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 475 | `reference-semantics/semantics/float.k:136-136` | rule | — | `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 476 | `reference-semantics/semantics/float.k:137-137` | rule | — | `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 477 | `reference-semantics/semantics/float.k:138-138` | rule | — | `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 478 | `reference-semantics/semantics/float.k:139-139` | rule | — | `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 479 | `reference-semantics/semantics/float.k:142-142` | syntax | function,total,symbol | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 480 | `reference-semantics/semantics/float.k:143-143` | rule | concrete | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 481 | `reference-semantics/semantics/float.k:144-144` | rule | — | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 482 | `reference-semantics/semantics/float.k:145-145` | rule | — | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 483 | `reference-semantics/semantics/float.k:146-146` | rule | — | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 484 | `reference-semantics/semantics/float.k:147-147` | rule | — | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 485 | `reference-semantics/semantics/float.k:148-148` | rule | — | `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 486 | `reference-semantics/semantics/float.k:149-149` | rule | — | `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 487 | `reference-semantics/semantics/float.k:150-150` | rule | — | `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 488 | `reference-semantics/semantics/float.k:151-151` | rule | — | `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 489 | `reference-semantics/semantics/float.k:154-154` | rule | — | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 490 | `reference-semantics/semantics/float.k:155-155` | rule | — | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 491 | `reference-semantics/semantics/float.k:160-160` | syntax | function,total,symbol | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 492 | `reference-semantics/semantics/float.k:161-161` | rule | concrete | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 493 | `reference-semantics/semantics/float.k:162-164` | rule | concrete | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 494 | `reference-semantics/semantics/float.k:165-165` | syntax | function | `syntax Int ::= headIS(IntSeq) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 495 | `reference-semantics/semantics/float.k:166-166` | rule | — | `rule headIS(iCons(C:Int, _:IntSeq)) => C` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 496 | `reference-semantics/semantics/float.k:167-167` | syntax | function,total | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 497 | `reference-semantics/semantics/float.k:168-168` | rule | — | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 498 | `reference-semantics/semantics/float.k:169-169` | rule | — | `rule intPartAcc(.IntSeq, A:Int) => A` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 499 | `reference-semantics/semantics/float.k:170-170` | rule | — | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 500 | `reference-semantics/semantics/float.k:171-172` | rule | — | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 501 | `reference-semantics/semantics/float.k:173-173` | syntax | function,total | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 502 | `reference-semantics/semantics/float.k:174-174` | rule | — | `rule fracPart(.IntSeq) => 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 503 | `reference-semantics/semantics/float.k:175-175` | rule | — | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 504 | `reference-semantics/semantics/float.k:176-176` | rule | — | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 505 | `reference-semantics/semantics/float.k:177-177` | rule | — | `rule fracAcc(.IntSeq, A:Int) => A` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 506 | `reference-semantics/semantics/float.k:178-178` | rule | — | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 507 | `reference-semantics/semantics/float.k:179-179` | syntax | function,total | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 508 | `reference-semantics/semantics/float.k:180-180` | rule | — | `rule fracScale(.IntSeq) => 1` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 509 | `reference-semantics/semantics/float.k:181-181` | rule | — | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 510 | `reference-semantics/semantics/float.k:182-182` | rule | — | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 511 | `reference-semantics/semantics/float.k:183-183` | rule | — | `rule fscAcc(.IntSeq, A:Int) => A` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 512 | `reference-semantics/semantics/float.k:184-184` | rule | — | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 513 | `reference-semantics/semantics/float.k:185-185` | rule | — | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 514 | `reference-semantics/semantics/float.k:186-186` | rule | — | `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 515 | `reference-semantics/semantics/float.k:187-187` | rule | — | `rule applyBuiltin("float", F:Float, .Vals)        => F` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 516 | `reference-semantics/semantics/float.k:190-190` | syntax | function,total,symbol | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 517 | `reference-semantics/semantics/float.k:191-191` | rule | concrete | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 518 | `reference-semantics/semantics/float.k:192-192` | rule | — | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 519 | `reference-semantics/semantics/float.k:195-195` | syntax | function,total,symbol | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 520 | `reference-semantics/semantics/float.k:196-196` | rule | concrete | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 521 | `reference-semantics/semantics/float.k:197-197` | rule | — | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 522 | `reference-semantics/semantics/float.k:198-198` | rule | — | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 523 | `reference-semantics/semantics/float.k:199-199` | rule | — | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 524 | `reference-semantics/semantics/float.k:200-200` | rule | — | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 525 | `reference-semantics/semantics/float.k:201-201` | rule | — | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 526 | `reference-semantics/semantics/float.k:202-202` | rule | — | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 527 | `reference-semantics/semantics/float.k:203-203` | rule | — | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 528 | `reference-semantics/semantics/float.k:204-204` | rule | — | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 529 | `reference-semantics/semantics/float.k:205-205` | rule | — | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 530 | `reference-semantics/semantics/float.k:206-206` | rule | — | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 531 | `reference-semantics/semantics/float.k:209-209` | syntax | function,total,symbol | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 532 | `reference-semantics/semantics/float.k:210-210` | rule | concrete | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 533 | `reference-semantics/semantics/float.k:211-211` | rule | — | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 534 | `reference-semantics/semantics/float.k:213-213` | rule | — | `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 535 | `reference-semantics/semantics/float.k:214-214` | rule | — | `rule applyBuiltin("float", F:Float, .Vals) => F` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 536 | `reference-semantics/semantics/float.k:217-217` | syntax | function,total,symbol | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 537 | `reference-semantics/semantics/float.k:218-222` | rule | concrete | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 538 | `reference-semantics/semantics/float.k:223-223` | syntax | function,total,symbol | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 539 | `reference-semantics/semantics/float.k:224-226` | rule | concrete | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 540 | `reference-semantics/semantics/float.k:227-227` | rule | — | `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 541 | `reference-semantics/semantics/float.k:228-228` | rule | — | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 542 | `reference-semantics/semantics/float.k:230-230` | syntax | function,total,symbol | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 543 | `reference-semantics/semantics/float.k:231-231` | rule | concrete | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 544 | `reference-semantics/semantics/float.k:232-232` | syntax | — | `syntax KItem ::= "#mathSqrt"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 545 | `reference-semantics/semantics/float.k:233-233` | rule | priority | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 546 | `reference-semantics/semantics/float.k:234-234` | rule | — | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 547 | `reference-semantics/semantics/float.k:235-235` | rule | — | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 548 | `reference-semantics/semantics/float.k:243-243` | syntax | — | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 549 | `reference-semantics/semantics/float.k:244-244` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 550 | `reference-semantics/semantics/float.k:245-245` | rule | — | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 551 | `reference-semantics/semantics/float.k:246-246` | rule | — | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 552 | `reference-semantics/semantics/float.k:247-248` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 553 | `reference-semantics/semantics/float.k:250-250` | syntax | — | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 554 | `reference-semantics/semantics/float.k:251-251` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 555 | `reference-semantics/semantics/float.k:252-252` | rule | — | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 556 | `reference-semantics/semantics/float.k:253-253` | rule | — | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 557 | `reference-semantics/semantics/float.k:254-255` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 558 | `reference-semantics/semantics/float.k:261-261` | syntax | — | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 559 | `reference-semantics/semantics/float.k:262-264` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 560 | `reference-semantics/semantics/float.k:265-265` | rule | — | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 561 | `reference-semantics/semantics/float.k:266-266` | rule | — | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 562 | `reference-semantics/semantics/float.k:267-269` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 563 | `reference-semantics/semantics/float.k:270-272` | rule | — | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 564 | `reference-semantics/semantics/functions.k:8-11` | syntax | — | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 565 | `reference-semantics/semantics/functions.k:14-16` | rule | — | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 566 | `reference-semantics/semantics/functions.k:18-18` | syntax | — | `syntax Expr ::= closureExpr(ParamNames, Stmts)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 567 | `reference-semantics/semantics/functions.k:19-20` | rule | — | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 568 | `reference-semantics/semantics/functions.k:27-27` | syntax | — | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 569 | `reference-semantics/semantics/functions.k:31-32` | syntax | — | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 570 | `reference-semantics/semantics/functions.k:33-35` | rule | — | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 571 | `reference-semantics/semantics/functions.k:36-41` | rule | — | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) .` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 572 | `reference-semantics/semantics/functions.k:42-45` | rule | — | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 573 | `reference-semantics/semantics/functions.k:47-49` | rule | — | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 574 | `reference-semantics/semantics/functions.k:50-52` | rule | — | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 575 | `reference-semantics/semantics/functions.k:53-58` | rule | — | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> re` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 576 | `reference-semantics/semantics/functions.k:59-60` | rule | — | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 577 | `reference-semantics/semantics/functions.k:63-63` | rule | — | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 578 | `reference-semantics/semantics/functions.k:64-66` | rule | — | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 579 | `reference-semantics/semantics/functions.k:68-75` | rule | priority | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 580 | `reference-semantics/semantics/functions.k:78-79` | rule | — | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 581 | `reference-semantics/semantics/functions.k:80-81` | rule | — | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 582 | `reference-semantics/semantics/functions.k:85-90` | rule | — | `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SA` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 583 | `reference-semantics/semantics/int.k:7-7` | rule | — | `rule applyUn("-", I:Int) => 0 -Int I` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 584 | `reference-semantics/semantics/int.k:9-9` | rule | — | `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 585 | `reference-semantics/semantics/int.k:11-11` | rule | — | `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 586 | `reference-semantics/semantics/int.k:12-12` | rule | — | `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 587 | `reference-semantics/semantics/int.k:13-13` | rule | — | `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 588 | `reference-semantics/semantics/int.k:14-14` | rule | — | `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 589 | `reference-semantics/semantics/int.k:15-15` | rule | — | `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 590 | `reference-semantics/semantics/int.k:16-16` | rule | — | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 591 | `reference-semantics/semantics/int.k:17-17` | rule | — | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 592 | `reference-semantics/semantics/int.k:19-19` | syntax | function | `syntax Int ::= pyMod(Int, Int) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 593 | `reference-semantics/semantics/int.k:20-20` | rule | — | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 594 | `reference-semantics/semantics/int.k:22-22` | rule | — | `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 595 | `reference-semantics/semantics/int.k:23-23` | rule | — | `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 596 | `reference-semantics/semantics/int.k:24-24` | rule | — | `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 597 | `reference-semantics/semantics/int.k:25-25` | rule | — | `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 598 | `reference-semantics/semantics/int.k:26-26` | rule | — | `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 599 | `reference-semantics/semantics/int.k:27-27` | rule | — | `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 600 | `reference-semantics/semantics/iter.k:8-8` | syntax | — | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 601 | `reference-semantics/semantics/list.k:9-9` | rule | — | `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 602 | `reference-semantics/semantics/list.k:10-10` | rule | — | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 603 | `reference-semantics/semantics/list.k:13-13` | syntax | — | `syntax ApplyK ::= "toList"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 604 | `reference-semantics/semantics/list.k:14-14` | rule | — | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 605 | `reference-semantics/semantics/list.k:15-15` | rule | — | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 606 | `reference-semantics/semantics/list.k:18-18` | syntax | function,total | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 607 | `reference-semantics/semantics/list.k:19-19` | rule | — | `rule valSeqConcat(.ValSeq, T:ValSeq)                => T` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 608 | `reference-semantics/semantics/list.k:20-20` | rule | — | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 609 | `reference-semantics/semantics/list.k:24-25` | rule | priority | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 610 | `reference-semantics/semantics/list.k:27-27` | rule | — | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 611 | `reference-semantics/semantics/list.k:28-28` | rule | — | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 612 | `reference-semantics/semantics/list.k:33-33` | syntax | function,total | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 613 | `reference-semantics/semantics/list.k:34-34` | rule | — | `rule hasRefVS(.ValSeq)                => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 614 | `reference-semantics/semantics/list.k:35-35` | rule | — | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 615 | `reference-semantics/semantics/list.k:37-38` | syntax | function | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map)        [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 616 | `reference-semantics/semantics/list.k:39-39` | rule | — | `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 617 | `reference-semantics/semantics/list.k:40-40` | rule | — | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 618 | `reference-semantics/semantics/list.k:41-41` | rule | — | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 619 | `reference-semantics/semantics/list.k:42-43` | rule | — | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 620 | `reference-semantics/semantics/list.k:45-46` | rule | — | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 621 | `reference-semantics/semantics/list.k:47-48` | rule | — | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 622 | `reference-semantics/semantics/list.k:49-49` | rule | — | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 623 | `reference-semantics/semantics/list.k:50-50` | rule | owise | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 624 | `reference-semantics/semantics/list.k:53-55` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 625 | `reference-semantics/semantics/list.k:58-58` | syntax | — | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 626 | `reference-semantics/semantics/list.k:59-59` | rule | — | `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 627 | `reference-semantics/semantics/list.k:60-60` | rule | — | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 628 | `reference-semantics/semantics/list.k:61-61` | rule | — | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 629 | `reference-semantics/semantics/list.k:62-62` | rule | — | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 630 | `reference-semantics/semantics/list.k:63-64` | rule | — | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 631 | `reference-semantics/semantics/list.k:65-66` | rule | — | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 632 | `reference-semantics/semantics/list.k:67-67` | rule | — | `rule <k> B:Bool ~> #notB => notBool B ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 633 | `reference-semantics/semantics/methods.k:10-10` | syntax | function | `syntax Val ::= applyMethod(Val, String, Vals) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 634 | `reference-semantics/semantics/methods.k:13-13` | rule | — | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 635 | `reference-semantics/semantics/methods.k:14-14` | rule | — | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 636 | `reference-semantics/semantics/methods.k:15-15` | rule | — | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 637 | `reference-semantics/semantics/methods.k:16-16` | rule | — | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 638 | `reference-semantics/semantics/methods.k:19-19` | rule | — | `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 639 | `reference-semantics/semantics/methods.k:20-20` | rule | — | `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 640 | `reference-semantics/semantics/methods.k:21-21` | rule | — | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 641 | `reference-semantics/semantics/methods.k:26-26` | rule | — | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 642 | `reference-semantics/semantics/methods.k:27-27` | syntax | function,total | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 643 | `reference-semantics/semantics/methods.k:28-28` | rule | — | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 644 | `reference-semantics/semantics/methods.k:29-29` | rule | — | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 645 | `reference-semantics/semantics/methods.k:30-31` | rule | — | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 646 | `reference-semantics/semantics/methods.k:34-34` | rule | — | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 647 | `reference-semantics/semantics/methods.k:35-35` | syntax | function | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 648 | `reference-semantics/semantics/methods.k:36-36` | rule | — | `rule cntSub(.IntSeq, _:IntSeq) => 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 649 | `reference-semantics/semantics/methods.k:37-38` | rule | — | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 650 | `reference-semantics/semantics/methods.k:39-40` | rule | — | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 651 | `reference-semantics/semantics/methods.k:41-41` | syntax | function,total | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 652 | `reference-semantics/semantics/methods.k:42-42` | rule | — | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 653 | `reference-semantics/semantics/methods.k:43-43` | rule | owise | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 654 | `reference-semantics/semantics/methods.k:44-44` | rule | — | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 655 | `reference-semantics/semantics/methods.k:47-47` | rule | — | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 656 | `reference-semantics/semantics/methods.k:48-48` | syntax | function,total | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 657 | `reference-semantics/semantics/methods.k:49-49` | rule | — | `rule trimWS(.IntSeq) => .IntSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 658 | `reference-semantics/semantics/methods.k:50-50` | rule | — | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 659 | `reference-semantics/semantics/methods.k:51-51` | rule | — | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 660 | `reference-semantics/semantics/methods.k:52-52` | syntax | function,total | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 661 | `reference-semantics/semantics/methods.k:53-53` | rule | — | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 662 | `reference-semantics/semantics/methods.k:54-54` | rule | — | `rule revISAcc(.IntSeq, A:IntSeq) => A` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 663 | `reference-semantics/semantics/methods.k:55-55` | rule | — | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 664 | `reference-semantics/semantics/methods.k:58-58` | rule | — | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 665 | `reference-semantics/semantics/methods.k:61-61` | rule | — | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 666 | `reference-semantics/semantics/methods.k:64-64` | rule | — | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 667 | `reference-semantics/semantics/methods.k:65-65` | syntax | function,total | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 668 | `reference-semantics/semantics/methods.k:66-66` | rule | — | `rule cntOccVS(.ValSeq, _:Val)                => 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 669 | `reference-semantics/semantics/methods.k:67-67` | rule | — | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 670 | `reference-semantics/semantics/methods.k:68-68` | rule | — | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 671 | `reference-semantics/semantics/methods.k:72-74` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 672 | `reference-semantics/semantics/methods.k:75-75` | syntax | function,token | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 673 | `reference-semantics/semantics/methods.k:76-76` | rule | — | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 674 | `reference-semantics/semantics/methods.k:77-78` | rule | — | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 675 | `reference-semantics/semantics/methods.k:79-80` | rule | — | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 676 | `reference-semantics/semantics/methods.k:82-82` | syntax | function | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 677 | `reference-semantics/semantics/methods.k:83-83` | rule | — | `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 678 | `reference-semantics/semantics/methods.k:84-84` | rule | — | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 679 | `reference-semantics/semantics/methods.k:85-85` | syntax | function,total | `syntax Bool ::= isWSC(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 680 | `reference-semantics/semantics/methods.k:86-86` | rule | — | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 681 | `reference-semantics/semantics/methods.k:89-91` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 682 | `reference-semantics/semantics/methods.k:94-96` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 683 | `reference-semantics/semantics/methods.k:97-97` | syntax | function,token | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 684 | `reference-semantics/semantics/methods.k:98-98` | rule | — | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 685 | `reference-semantics/semantics/methods.k:99-100` | rule | — | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 686 | `reference-semantics/semantics/methods.k:101-102` | rule | — | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 687 | `reference-semantics/semantics/methods.k:104-105` | rule | — | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 688 | `reference-semantics/semantics/methods.k:106-106` | syntax | function,total | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 689 | `reference-semantics/semantics/methods.k:107-107` | rule | — | `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 690 | `reference-semantics/semantics/methods.k:108-108` | rule | — | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 691 | `reference-semantics/semantics/methods.k:109-109` | rule | — | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 692 | `reference-semantics/semantics/methods.k:112-112` | syntax | function,total | `syntax Bool ::= isUpperC(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 693 | `reference-semantics/semantics/methods.k:113-113` | rule | — | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 694 | `reference-semantics/semantics/methods.k:115-115` | syntax | function,total | `syntax Bool ::= isLowerC(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 695 | `reference-semantics/semantics/methods.k:116-116` | rule | — | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 696 | `reference-semantics/semantics/methods.k:118-118` | syntax | function,total | `syntax Bool ::= isAlphaC(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 697 | `reference-semantics/semantics/methods.k:119-119` | rule | — | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 698 | `reference-semantics/semantics/methods.k:121-121` | syntax | function,total | `syntax Bool ::= isDigitC(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 699 | `reference-semantics/semantics/methods.k:122-122` | rule | — | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 700 | `reference-semantics/semantics/methods.k:124-124` | syntax | function,total | `syntax Bool ::= hasUpper(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 701 | `reference-semantics/semantics/methods.k:125-125` | rule | — | `rule hasUpper(.IntSeq) => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 702 | `reference-semantics/semantics/methods.k:126-126` | rule | — | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 703 | `reference-semantics/semantics/methods.k:128-128` | syntax | function,total | `syntax Bool ::= hasLower(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 704 | `reference-semantics/semantics/methods.k:129-129` | rule | — | `rule hasLower(.IntSeq) => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 705 | `reference-semantics/semantics/methods.k:130-130` | rule | — | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 706 | `reference-semantics/semantics/methods.k:132-132` | syntax | function,total | `syntax Bool ::= allAlpha(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 707 | `reference-semantics/semantics/methods.k:133-133` | rule | — | `rule allAlpha(.IntSeq) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 708 | `reference-semantics/semantics/methods.k:134-134` | rule | — | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 709 | `reference-semantics/semantics/methods.k:136-136` | syntax | function,total | `syntax Bool ::= allDigit(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 710 | `reference-semantics/semantics/methods.k:137-137` | rule | — | `rule allDigit(.IntSeq) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 711 | `reference-semantics/semantics/methods.k:138-138` | rule | — | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 712 | `reference-semantics/semantics/methods.k:140-140` | syntax | function,total | `syntax Int ::= lowerC(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 713 | `reference-semantics/semantics/methods.k:142-142` | rule | — | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 714 | `reference-semantics/semantics/methods.k:143-143` | rule | owise | `rule lowerC(C:Int) => C         [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 715 | `reference-semantics/semantics/methods.k:145-145` | syntax | function,total | `syntax Int ::= upperC(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 716 | `reference-semantics/semantics/methods.k:146-146` | rule | — | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 717 | `reference-semantics/semantics/methods.k:147-147` | rule | owise | `rule upperC(C:Int) => C         [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 718 | `reference-semantics/semantics/methods.k:149-149` | syntax | function,total | `syntax Int ::= swapC(Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 719 | `reference-semantics/semantics/methods.k:150-150` | rule | — | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 720 | `reference-semantics/semantics/methods.k:151-151` | rule | — | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 721 | `reference-semantics/semantics/methods.k:152-152` | rule | owise | `rule swapC(C:Int) => C         [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 722 | `reference-semantics/semantics/methods.k:154-154` | syntax | function,total | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 723 | `reference-semantics/semantics/methods.k:155-155` | rule | — | `rule mapLower(.IntSeq) => .IntSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 724 | `reference-semantics/semantics/methods.k:156-156` | rule | — | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 725 | `reference-semantics/semantics/methods.k:158-158` | syntax | function,total | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 726 | `reference-semantics/semantics/methods.k:159-159` | rule | — | `rule mapUpper(.IntSeq) => .IntSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 727 | `reference-semantics/semantics/methods.k:160-160` | rule | — | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 728 | `reference-semantics/semantics/methods.k:162-162` | syntax | function,total | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 729 | `reference-semantics/semantics/methods.k:163-163` | rule | — | `rule mapSwap(.IntSeq) => .IntSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 730 | `reference-semantics/semantics/methods.k:164-164` | rule | — | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 731 | `reference-semantics/semantics/methods.k:166-166` | syntax | function,total | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 732 | `reference-semantics/semantics/methods.k:167-167` | rule | — | `rule startsWith(.IntSeq, _:IntSeq)               => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 733 | `reference-semantics/semantics/methods.k:168-168` | rule | — | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 734 | `reference-semantics/semantics/methods.k:169-169` | rule | — | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 735 | `reference-semantics/semantics/operators.k:10-10` | rule | — | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 736 | `reference-semantics/semantics/operators.k:12-12` | rule | — | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 737 | `reference-semantics/semantics/operators.k:15-15` | context | — | `context Compare(HOLE, _)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 738 | `reference-semantics/semantics/operators.k:16-16` | context | — | `context Compare(_:Val, CmpOp(_, HOLE))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 739 | `reference-semantics/semantics/operators.k:17-17` | rule | owise | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 740 | `reference-semantics/semantics/operators.k:19-19` | rule | — | `rule applyCmp("is",     V:Val, noneV) => V ==K noneV` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 741 | `reference-semantics/semantics/operators.k:20-20` | rule | — | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 742 | `reference-semantics/semantics/operators.k:25-27` | rule | priority | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 743 | `reference-semantics/semantics/operators.k:28-31` | rule | priority | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 744 | `reference-semantics/semantics/operators.k:34-37` | rule | priority | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 745 | `reference-semantics/semantics/operators.k:38-42` | rule | priority | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 746 | `reference-semantics/semantics/operators.k:44-46` | rule | priority | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 747 | `reference-semantics/semantics/range.k:9-9` | syntax | function,total | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 748 | `reference-semantics/semantics/range.k:10-10` | rule | — | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 749 | `reference-semantics/semantics/range.k:12-12` | syntax | function | `syntax Int ::= rangeLen(Int, Int, Int) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 750 | `reference-semantics/semantics/range.k:13-14` | rule | — | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 751 | `reference-semantics/semantics/range.k:15-16` | rule | — | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 752 | `reference-semantics/semantics/range.k:17-18` | rule | — | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 753 | `reference-semantics/semantics/range.k:20-22` | rule | — | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 754 | `reference-semantics/semantics/range.k:23-24` | rule | — | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 755 | `reference-semantics/semantics/set.k:8-8` | syntax | — | `syntax Val ::= setV(IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 756 | `reference-semantics/semantics/set.k:11-11` | syntax | function,total | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 757 | `reference-semantics/semantics/set.k:12-12` | rule | — | `rule codeIn(_:Int, .IntSeq)                => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 758 | `reference-semantics/semantics/set.k:13-13` | rule | — | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 759 | `reference-semantics/semantics/set.k:16-17` | syntax | function,total | `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] \| dedupFrom(IntSeq, IntSeq)  [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 760 | `reference-semantics/semantics/set.k:18-18` | rule | — | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 761 | `reference-semantics/semantics/set.k:19-19` | rule | — | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 762 | `reference-semantics/semantics/set.k:20-21` | rule | — | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 763 | `reference-semantics/semantics/set.k:22-23` | rule | — | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 764 | `reference-semantics/semantics/set.k:25-25` | syntax | function,total | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 765 | `reference-semantics/semantics/set.k:26-26` | rule | — | `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 766 | `reference-semantics/semantics/set.k:27-27` | rule | — | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 767 | `reference-semantics/semantics/set.k:31-31` | syntax | function,total | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 768 | `reference-semantics/semantics/set.k:32-32` | rule | — | `rule subsetCodes(.IntSeq, _:IntSeq)                => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 769 | `reference-semantics/semantics/set.k:33-33` | rule | — | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 770 | `reference-semantics/semantics/set.k:35-35` | syntax | function,total | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 771 | `reference-semantics/semantics/set.k:36-36` | rule | — | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 772 | `reference-semantics/semantics/set.k:39-39` | rule | — | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 773 | `reference-semantics/semantics/sort.k:18-18` | syntax | function,total,symbol | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 774 | `reference-semantics/semantics/sort.k:19-19` | syntax | function | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 775 | `reference-semantics/semantics/sort.k:20-20` | rule | concrete | `rule sortVS(.ValSeq)                => .ValSeq          [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 776 | `reference-semantics/semantics/sort.k:21-21` | rule | concrete | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 777 | `reference-semantics/semantics/sort.k:22-22` | rule | concrete | `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 778 | `reference-semantics/semantics/sort.k:23-23` | rule | concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 779 | `reference-semantics/semantics/sort.k:24-24` | rule | concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 780 | `reference-semantics/semantics/sort.k:26-26` | syntax | function | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 781 | `reference-semantics/semantics/sort.k:27-27` | rule | concrete | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 782 | `reference-semantics/semantics/sort.k:28-28` | rule | concrete | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 783 | `reference-semantics/semantics/sort.k:29-30` | rule | concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 784 | `reference-semantics/semantics/sort.k:31-32` | rule | concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 785 | `reference-semantics/semantics/sort.k:36-37` | rule | — | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 786 | `reference-semantics/semantics/sort.k:40-42` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 787 | `reference-semantics/semantics/sort.k:49-49` | syntax | function,total,symbol | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 788 | `reference-semantics/semantics/sort.k:51-52` | syntax | function,total | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 789 | `reference-semantics/semantics/sort.k:53-53` | rule | — | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 790 | `reference-semantics/semantics/sort.k:54-54` | rule | — | `rule revVSAcc(.ValSeq, A:ValSeq) => A` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 791 | `reference-semantics/semantics/sort.k:55-55` | rule | — | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 792 | `reference-semantics/semantics/sort.k:57-57` | syntax | function,total | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 793 | `reference-semantics/semantics/sort.k:58-58` | rule | — | `rule condRev(S:ValSeq, false) => S` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 794 | `reference-semantics/semantics/sort.k:59-59` | rule | — | `rule condRev(S:ValSeq, true)  => revVS(S)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 795 | `reference-semantics/semantics/sort.k:61-62` | rule | — | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 796 | `reference-semantics/semantics/sort.k:63-64` | rule | — | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 797 | `reference-semantics/semantics/sort.k:65-66` | rule | — | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 798 | `reference-semantics/semantics/str.k:8-8` | rule | — | `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 799 | `reference-semantics/semantics/str.k:9-10` | rule | — | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 800 | `reference-semantics/semantics/str.k:13-13` | syntax | function | `syntax IntSeq ::= strToCodes(String) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 801 | `reference-semantics/semantics/str.k:14-14` | rule | — | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 802 | `reference-semantics/semantics/str.k:15-15` | rule | — | `rule strToCodes("") => .IntSeq` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 803 | `reference-semantics/semantics/str.k:16-17` | rule | — | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 804 | `reference-semantics/semantics/str.k:20-20` | syntax | function,total | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 805 | `reference-semantics/semantics/str.k:21-21` | rule | — | `rule seqConcat(.IntSeq, T:IntSeq)                => T` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 806 | `reference-semantics/semantics/str.k:22-22` | rule | — | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 807 | `reference-semantics/semantics/str.k:24-24` | rule | — | `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 808 | `reference-semantics/semantics/str.k:25-25` | rule | — | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 809 | `reference-semantics/semantics/str.k:26-26` | rule | — | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 810 | `reference-semantics/semantics/str.k:29-29` | rule | — | `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 811 | `reference-semantics/semantics/str.k:30-30` | rule | — | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 812 | `reference-semantics/semantics/str.k:32-32` | syntax | function,total | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 813 | `reference-semantics/semantics/str.k:33-33` | rule | — | `rule strPrefix(.IntSeq, _:IntSeq)               => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 814 | `reference-semantics/semantics/str.k:34-34` | rule | — | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 815 | `reference-semantics/semantics/str.k:35-35` | rule | — | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 816 | `reference-semantics/semantics/str.k:37-37` | syntax | function,total | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 817 | `reference-semantics/semantics/str.k:38-38` | rule | — | `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 818 | `reference-semantics/semantics/str.k:39-39` | rule | — | `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 819 | `reference-semantics/semantics/str.k:40-41` | rule | — | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 820 | `reference-semantics/semantics/str.k:48-48` | syntax | function,total | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 821 | `reference-semantics/semantics/str.k:49-49` | rule | — | `rule strLt(.IntSeq, .IntSeq)                => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 822 | `reference-semantics/semantics/str.k:50-50` | rule | — | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 823 | `reference-semantics/semantics/str.k:51-51` | rule | — | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 824 | `reference-semantics/semantics/str.k:52-52` | rule | — | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 825 | `reference-semantics/semantics/str.k:53-53` | rule | — | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 826 | `reference-semantics/semantics/str.k:54-54` | rule | — | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 827 | `reference-semantics/semantics/str.k:56-56` | rule | — | `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 828 | `reference-semantics/semantics/str.k:57-57` | rule | — | `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 829 | `reference-semantics/semantics/str.k:58-58` | rule | — | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 830 | `reference-semantics/semantics/str.k:59-59` | rule | — | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 831 | `reference-semantics/semantics/subscript.k:11-11` | syntax | function,total | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 832 | `reference-semantics/semantics/subscript.k:12-12` | rule | — | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 833 | `reference-semantics/semantics/subscript.k:13-14` | rule | — | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 834 | `reference-semantics/semantics/subscript.k:16-16` | syntax | function | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 835 | `reference-semantics/semantics/subscript.k:17-17` | rule | — | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 836 | `reference-semantics/semantics/subscript.k:18-19` | rule | — | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 837 | `reference-semantics/semantics/subscript.k:21-21` | syntax | function,total | `syntax Int ::= normIdx(Int, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 838 | `reference-semantics/semantics/subscript.k:22-22` | rule | — | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 839 | `reference-semantics/semantics/subscript.k:23-23` | rule | — | `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 840 | `reference-semantics/semantics/subscript.k:27-27` | context | — | `context Subscript(HOLE, _)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 841 | `reference-semantics/semantics/subscript.k:28-28` | context | — | `context Subscript(_:Val, HOLE:Expr)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 842 | `reference-semantics/semantics/subscript.k:31-33` | rule | priority | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 843 | `reference-semantics/semantics/subscript.k:35-35` | rule | — | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 844 | `reference-semantics/semantics/subscript.k:37-37` | syntax | function | `syntax Val ::= applyIndex(Val, Int) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 845 | `reference-semantics/semantics/subscript.k:38-38` | rule | — | `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 846 | `reference-semantics/semantics/subscript.k:39-39` | rule | — | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 847 | `reference-semantics/semantics/subscript.k:40-41` | rule | — | `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 848 | `reference-semantics/semantics/subscript.k:44-47` | syntax | — | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 849 | `reference-semantics/semantics/subscript.k:49-49` | syntax | — | `syntax OptInt ::= "noB" \| someB(Int)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 850 | `reference-semantics/semantics/subscript.k:50-50` | rule | — | `rule <k> #evalB(NoBound)  => noB ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 851 | `reference-semantics/semantics/subscript.k:51-51` | rule | — | `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 852 | `reference-semantics/semantics/subscript.k:52-52` | rule | — | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 853 | `reference-semantics/semantics/subscript.k:54-54` | rule | — | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 854 | `reference-semantics/semantics/subscript.k:55-55` | rule | — | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 855 | `reference-semantics/semantics/subscript.k:56-56` | rule | — | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 856 | `reference-semantics/semantics/subscript.k:58-60` | rule | priority | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 857 | `reference-semantics/semantics/subscript.k:61-61` | rule | — | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 858 | `reference-semantics/semantics/subscript.k:63-63` | syntax | function | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 859 | `reference-semantics/semantics/subscript.k:64-65` | rule | — | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 860 | `reference-semantics/semantics/subscript.k:66-67` | rule | — | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 861 | `reference-semantics/semantics/subscript.k:68-69` | rule | — | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 862 | `reference-semantics/semantics/subscript.k:72-72` | syntax | function,total | `syntax Int ::= slStep(OptInt) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 863 | `reference-semantics/semantics/subscript.k:73-73` | rule | — | `rule slStep(noB)          => 1` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 864 | `reference-semantics/semantics/subscript.k:74-74` | rule | — | `rule slStep(someB(S:Int)) => S` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 865 | `reference-semantics/semantics/subscript.k:76-76` | syntax | function | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 866 | `reference-semantics/semantics/subscript.k:77-78` | rule | — | `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 867 | `reference-semantics/semantics/subscript.k:79-80` | rule | — | `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 868 | `reference-semantics/semantics/subscript.k:81-81` | rule | — | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 869 | `reference-semantics/semantics/subscript.k:83-83` | syntax | function | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 870 | `reference-semantics/semantics/subscript.k:84-85` | rule | — | `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 871 | `reference-semantics/semantics/subscript.k:86-87` | rule | — | `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 872 | `reference-semantics/semantics/subscript.k:88-88` | rule | — | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 873 | `reference-semantics/semantics/subscript.k:90-90` | syntax | function,total | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 874 | `reference-semantics/semantics/subscript.k:91-92` | rule | — | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 875 | `reference-semantics/semantics/subscript.k:93-94` | rule | — | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 876 | `reference-semantics/semantics/subscript.k:96-96` | syntax | function,total | `syntax Int ::= clampLo(Int, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 877 | `reference-semantics/semantics/subscript.k:97-98` | rule | — | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 878 | `reference-semantics/semantics/subscript.k:99-100` | rule | — | `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 879 | `reference-semantics/semantics/subscript.k:102-102` | syntax | function,total | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 880 | `reference-semantics/semantics/subscript.k:103-104` | rule | — | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 881 | `reference-semantics/semantics/subscript.k:105-106` | rule | — | `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 882 | `reference-semantics/semantics/subscript.k:109-109` | syntax | function | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 883 | `reference-semantics/semantics/subscript.k:110-112` | rule | — | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 884 | `reference-semantics/semantics/subscript.k:113-114` | rule | — | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 885 | `reference-semantics/semantics/subscript.k:116-116` | syntax | function | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 886 | `reference-semantics/semantics/subscript.k:117-119` | rule | — | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 887 | `reference-semantics/semantics/subscript.k:120-121` | rule | — | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 888 | `reference-semantics/semantics/syntax.k:9-30` | syntax | macro,strict,seqstrict | `syntax Expr ::= "Int"      "(" Int ")" \| "Float"    "(" Float ")" \| "Bool"     "(" Bool ")" \| "Name"     "(" String ")" \| "Str"      "(" String ")" \| "UnaryOp"  "(" String "," Expr ")" [strict(2)] \| "BinOp"    "(" String "," Expr "," Expr "` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 889 | `reference-semantics/semantics/syntax.k:32-32` | syntax | — | `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 890 | `reference-semantics/semantics/syntax.k:33-33` | syntax | — | `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 891 | `reference-semantics/semantics/syntax.k:34-34` | syntax | — | `syntax Entries  ::= List{Entry, ","}` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 892 | `reference-semantics/semantics/syntax.k:35-35` | syntax | — | `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 893 | `reference-semantics/semantics/syntax.k:36-36` | syntax | — | `syntax CompFors ::= List{CompFor, ""}` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 894 | `reference-semantics/semantics/syntax.k:37-37` | syntax | — | `syntax Exprs    ::= List{Expr, ","}` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 895 | `reference-semantics/semantics/syntax.k:38-38` | syntax | — | `syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 896 | `reference-semantics/semantics/syntax.k:39-39` | syntax | — | `syntax Bound    ::= Expr \| "NoBound"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 897 | `reference-semantics/semantics/syntax.k:41-54` | syntax | strict | `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] \| "Import"    "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For"       "(" Expr "," Expr "," Stmts ")"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 898 | `reference-semantics/semantics/syntax.k:56-56` | syntax | — | `syntax Stmts      ::= List{Stmt, ""}` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 899 | `reference-semantics/semantics/syntax.k:57-57` | syntax | — | `syntax Params     ::= "Params" "(" ParamNames ")"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 900 | `reference-semantics/semantics/syntax.k:58-58` | syntax | — | `syntax CellVars   ::= "CellVars" "(" ParamNames ")"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 901 | `reference-semantics/semantics/syntax.k:59-59` | syntax | — | `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 902 | `reference-semantics/semantics/syntax.k:60-60` | syntax | — | `syntax ParamNames ::= List{String, ","}` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 903 | `reference-semantics/semantics/syntax.k:61-61` | syntax | — | `syntax Module     ::= "Module" "(" Stmts ")"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 904 | `reference-semantics/semantics/tuple.k:10-10` | rule | — | `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 905 | `reference-semantics/semantics/tuple.k:11-11` | rule | — | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 906 | `reference-semantics/semantics/tuple.k:14-14` | syntax | — | `syntax ApplyK ::= "toTuple"` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 907 | `reference-semantics/semantics/tuple.k:15-15` | rule | — | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 908 | `reference-semantics/semantics/tuple.k:16-16` | rule | — | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 909 | `reference-semantics/semantics/tuple.k:18-18` | rule | — | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 910 | `reference-semantics/semantics/tuple.k:20-20` | rule | — | `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 911 | `reference-semantics/semantics/tuple.k:21-21` | rule | — | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 912 | `reference-semantics/semantics/tuple.k:23-23` | rule | — | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 913 | `reference-semantics/semantics/tuple.k:24-24` | syntax | function | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 914 | `reference-semantics/semantics/tuple.k:25-25` | rule | — | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 915 | `reference-semantics/semantics/tuple.k:26-27` | rule | — | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 916 | `reference-semantics/semantics/tuple.k:28-28` | rule | — | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 917 | `reference-semantics/semantics/tuple.k:31-31` | syntax | — | `syntax KItem ::= #bindTgt(Expr, Val)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 918 | `reference-semantics/semantics/tuple.k:32-34` | rule | — | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 919 | `reference-semantics/semantics/tuple.k:35-41` | rule | priority | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 920 | `reference-semantics/semantics/tuple.k:42-42` | rule | — | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 921 | `reference-semantics/semantics/tuple.k:43-43` | rule | — | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 922 | `reference-semantics/semantics/tuple.k:44-46` | rule | priority | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 923 | `reference-semantics/semantics/tuple.k:49-49` | syntax | — | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 924 | `reference-semantics/semantics/tuple.k:50-50` | rule | — | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 925 | `reference-semantics/semantics/tuple.k:51-51` | rule | — | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 926 | `reference-semantics/semantics/tuple.k:52-54` | rule | priority | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 927 | `reference-semantics/semantics/tuple.k:55-56` | rule | — | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 928 | `reference-semantics/semantics/tuple.k:57-57` | rule | — | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` | TRUSTED-SUPPLIED baseline (byte-identical) |
| 929 | `verification.k:8-8` | syntax | macro | `syntax Stmts ::= "#innerBody" [macro]` | PROOF-LOCAL—individual decision in REVIEW.md |
| 930 | `verification.k:9-12` | rule | — | `rule #innerBody => If(Compare(Name("item"), CmpOp("==", Name("value"))), AugAssign(Name("count"), "+", Int(1)) .Stmts, .Stmts) .Stmts` | PROOF-LOCAL—individual decision in REVIEW.md |
| 931 | `verification.k:14-14` | syntax | macro | `syntax Stmts ::= "#outerBody" [macro]` | PROOF-LOCAL—individual decision in REVIEW.md |
| 932 | `verification.k:15-22` | rule | — | `rule #outerBody => Assign(Name("count"), Int(0)) For(Name("item"), Name("lst"), #innerBody) If(Compare(Name("count"), CmpOp(">=", Name("value"))), If(Compare(Name("value"), CmpOp(">", Name("result"))), Assign(Name("result"), Name("value")) ` | PROOF-LOCAL—individual decision in REVIEW.md |
| 933 | `verification.k:24-24` | syntax | macro | `syntax Stmts ::= "#searchBody" [macro]` | PROOF-LOCAL—individual decision in REVIEW.md |
| 934 | `verification.k:25-28` | rule | — | `rule #searchBody => Assign(Name("result"), UnaryOp("-", Int(1))) For(Name("value"), Name("lst"), #outerBody) Return(Name("result")) .Stmts` | PROOF-LOCAL—individual decision in REVIEW.md |
| 935 | `verification.k:33-33` | syntax | — | `syntax IntValSeq ::= ".ValSeq" \| vCons(Int, IntValSeq)` | PROOF-LOCAL—individual decision in REVIEW.md |
| 936 | `verification.k:34-34` | syntax | — | `syntax ValSeq ::= IntValSeq` | PROOF-LOCAL—individual decision in REVIEW.md |
| 937 | `verification.k:36-36` | syntax | function,total | `syntax Bool ::= allPositive(IntValSeq) [function, total]` | PROOF-LOCAL—individual decision in REVIEW.md |
| 938 | `verification.k:37-37` | rule | — | `rule allPositive(.ValSeq) => true` | PROOF-LOCAL—individual decision in REVIEW.md |
| 939 | `verification.k:38-39` | rule | — | `rule allPositive(vCons(X:Int, XS:IntValSeq)) => X >Int 0 andBool allPositive(XS)` | PROOF-LOCAL—individual decision in REVIEW.md |
| 940 | `verification.k:41-41` | syntax | function,total | `syntax Bool ::= nonEmpty(IntValSeq) [function, total]` | PROOF-LOCAL—individual decision in REVIEW.md |
| 941 | `verification.k:42-42` | rule | — | `rule nonEmpty(.ValSeq) => false` | PROOF-LOCAL—individual decision in REVIEW.md |
| 942 | `verification.k:43-43` | rule | — | `rule nonEmpty(vCons(_:Int, _:IntValSeq)) => true` | PROOF-LOCAL—individual decision in REVIEW.md |
| 943 | `verification.k:48-48` | syntax | function,total | `syntax Int ::= frequency(Int, IntValSeq) [function, total]` | PROOF-LOCAL—individual decision in REVIEW.md |
| 944 | `verification.k:49-49` | rule | — | `rule frequency(_:Int, .ValSeq) => 0` | PROOF-LOCAL—individual decision in REVIEW.md |
| 945 | `verification.k:50-51` | rule | — | `rule frequency(X:Int, vCons(Y:Int, YS:IntValSeq)) => (#if X ==Int Y #then 1 #else 0 #fi) +Int frequency(X, YS)` | PROOF-LOCAL—individual decision in REVIEW.md |
| 946 | `verification.k:53-53` | syntax | function,total | `syntax Int ::= chooseFreq(Int, IntValSeq, Int) [function, total]` | PROOF-LOCAL—individual decision in REVIEW.md |
| 947 | `verification.k:54-57` | rule | — | `rule chooseFreq(X:Int, ALL:IntValSeq, BEST:Int) => X requires X >Int 0 andBool frequency(X, ALL) >=Int X andBool X >Int BEST` | PROOF-LOCAL—individual decision in REVIEW.md |
| 948 | `verification.k:58-61` | rule | — | `rule chooseFreq(X:Int, ALL:IntValSeq, BEST:Int) => BEST requires notBool (X >Int 0 andBool frequency(X, ALL) >=Int X andBool X >Int BEST)` | PROOF-LOCAL—individual decision in REVIEW.md |
| 949 | `verification.k:63-64` | syntax | function,total | `syntax Int ::= greatestFreq(IntValSeq) [function, total] \| greatestFreqFrom(IntValSeq, IntValSeq, Int) [function, total]` | PROOF-LOCAL—individual decision in REVIEW.md |
| 950 | `verification.k:65-66` | rule | — | `rule greatestFreq(ALL:IntValSeq) => greatestFreqFrom(ALL, ALL, -1)` | PROOF-LOCAL—individual decision in REVIEW.md |
| 951 | `verification.k:67-67` | rule | — | `rule greatestFreqFrom(.ValSeq, _:IntValSeq, BEST:Int) => BEST` | PROOF-LOCAL—individual decision in REVIEW.md |
| 952 | `verification.k:68-69` | rule | — | `rule greatestFreqFrom(vCons(X:Int, XS:IntValSeq), ALL:IntValSeq, BEST:Int) => greatestFreqFrom(XS, ALL, chooseFreq(X, ALL, BEST))` | PROOF-LOCAL—individual decision in REVIEW.md |
| 953 | `verification.k:77-86` | rule | priority | `rule <k> For(Name("value"), list(ALL:IntValSeq), #outerBody) => Assign(Name("result"), Int(greatestFreq(ALL))) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "lst" in_keys(M) andBool "result" in_keys(M` | PROOF-LOCAL—individual decision in REVIEW.md |
| 954 | `spec.k:8-30` | claim | — | `claim <k> Call(Name("search"), list(ALL:IntValSeq), .Exprs) => greatestFreq(ALL) </k> <env> 0 </env> <scopes> 0 \|-> scope( "search" \|-> closureVal( "lst" , .ParamNames, #searchBody, 0), parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> ` | ENTRY CLAIM—adequacy decision in REVIEW.md |

## Attribute searches

- `function`: 151 declaration block(s)
  - `reference-semantics/semantics/builtins.k:17-17`
  - `reference-semantics/semantics/builtins.k:20-20`
  - `reference-semantics/semantics/builtins.k:36-36`
  - `reference-semantics/semantics/builtins.k:54-54`
  - `reference-semantics/semantics/builtins.k:97-97`
  - `reference-semantics/semantics/builtins.k:102-102`
  - `reference-semantics/semantics/builtins.k:114-114`
  - `reference-semantics/semantics/builtins.k:117-117`
  - `reference-semantics/semantics/builtins.k:126-126`
  - `reference-semantics/semantics/builtins.k:134-134`
  - `reference-semantics/semantics/builtins.k:158-158`
  - `reference-semantics/semantics/builtins.k:188-188`
  - `reference-semantics/semantics/builtins.k:194-194`
  - `reference-semantics/semantics/builtins.k:196-196`
  - `reference-semantics/semantics/builtins.k:199-199`
  - `reference-semantics/semantics/builtins.k:203-203`
  - `reference-semantics/semantics/builtins.k:214-215`
  - `reference-semantics/semantics/builtins.k:226-226`
  - `reference-semantics/semantics/builtins.k:230-230`
  - `reference-semantics/semantics/builtins.k:238-238`
  - `reference-semantics/semantics/builtins.k:244-244`
  - `reference-semantics/semantics/builtins.k:247-247`
  - `reference-semantics/semantics/builtins.k:250-250`
  - `reference-semantics/semantics/builtins.k:255-255`
  - `reference-semantics/semantics/builtins.k:265-265`
  - `reference-semantics/semantics/builtins.k:269-269`
  - `reference-semantics/semantics/builtins.k:272-272`
  - `reference-semantics/semantics/builtins.k:285-285`
  - `reference-semantics/semantics/builtins.k:293-293`
  - `reference-semantics/semantics/call.k:52-52`
  - `reference-semantics/semantics/concrete.k:42-42`
  - `reference-semantics/semantics/concrete.k:51-51`
  - `reference-semantics/semantics/concrete.k:56-56`
  - `reference-semantics/semantics/core.k:25-34`
  - `reference-semantics/semantics/core.k:68-68`
  - `reference-semantics/semantics/core.k:76-76`
  - `reference-semantics/semantics/core.k:100-100`
  - `reference-semantics/semantics/core.k:107-107`
  - `reference-semantics/semantics/core.k:109-109`
  - `reference-semantics/semantics/core.k:157-157`
  - `reference-semantics/semantics/core.k:199-199`
  - `reference-semantics/semantics/core.k:208-208`
  - `reference-semantics/semantics/core.k:209-209`
  - `reference-semantics/semantics/core.k:210-210`
  - `reference-semantics/semantics/core.k:213-213`
  - `reference-semantics/semantics/core.k:217-217`
  - `reference-semantics/semantics/core.k:223-223`
  - `reference-semantics/semantics/core.k:227-227`
  - `reference-semantics/semantics/core.k:233-233`
  - `reference-semantics/semantics/dict.k:37-37`
  - `reference-semantics/semantics/dict.k:43-43`
  - `reference-semantics/semantics/dict.k:49-49`
  - `reference-semantics/semantics/dict.k:64-64`
  - `reference-semantics/semantics/dict.k:70-70`
  - `reference-semantics/semantics/dict.k:90-90`
  - `reference-semantics/semantics/dict.k:97-97`
  - `reference-semantics/semantics/dict.k:101-101`
  - `reference-semantics/semantics/float.k:24-24`
  - `reference-semantics/semantics/float.k:30-30`
  - `reference-semantics/semantics/float.k:37-37`
  - `reference-semantics/semantics/float.k:50-50`
  - `reference-semantics/semantics/float.k:54-54`
  - `reference-semantics/semantics/float.k:73-73`
  - `reference-semantics/semantics/float.k:86-86`
  - `reference-semantics/semantics/float.k:93-93`
  - `reference-semantics/semantics/float.k:103-103`
  - `reference-semantics/semantics/float.k:107-107`
  - `reference-semantics/semantics/float.k:111-111`
  - `reference-semantics/semantics/float.k:115-115`
  - `reference-semantics/semantics/float.k:119-119`
  - `reference-semantics/semantics/float.k:125-125`
  - `reference-semantics/semantics/float.k:142-142`
  - `reference-semantics/semantics/float.k:160-160`
  - `reference-semantics/semantics/float.k:165-165`
  - `reference-semantics/semantics/float.k:167-167`
  - `reference-semantics/semantics/float.k:173-173`
  - `reference-semantics/semantics/float.k:179-179`
  - `reference-semantics/semantics/float.k:190-190`
  - `reference-semantics/semantics/float.k:195-195`
  - `reference-semantics/semantics/float.k:209-209`
  - `reference-semantics/semantics/float.k:217-217`
  - `reference-semantics/semantics/float.k:223-223`
  - `reference-semantics/semantics/float.k:230-230`
  - `reference-semantics/semantics/int.k:19-19`
  - `reference-semantics/semantics/list.k:18-18`
  - `reference-semantics/semantics/list.k:33-33`
  - `reference-semantics/semantics/list.k:37-38`
  - `reference-semantics/semantics/methods.k:10-10`
  - `reference-semantics/semantics/methods.k:27-27`
  - `reference-semantics/semantics/methods.k:35-35`
  - `reference-semantics/semantics/methods.k:41-41`
  - `reference-semantics/semantics/methods.k:48-48`
  - `reference-semantics/semantics/methods.k:52-52`
  - `reference-semantics/semantics/methods.k:65-65`
  - `reference-semantics/semantics/methods.k:75-75`
  - `reference-semantics/semantics/methods.k:82-82`
  - `reference-semantics/semantics/methods.k:85-85`
  - `reference-semantics/semantics/methods.k:97-97`
  - `reference-semantics/semantics/methods.k:106-106`
  - `reference-semantics/semantics/methods.k:112-112`
  - `reference-semantics/semantics/methods.k:115-115`
  - `reference-semantics/semantics/methods.k:118-118`
  - `reference-semantics/semantics/methods.k:121-121`
  - `reference-semantics/semantics/methods.k:124-124`
  - `reference-semantics/semantics/methods.k:128-128`
  - `reference-semantics/semantics/methods.k:132-132`
  - `reference-semantics/semantics/methods.k:136-136`
  - `reference-semantics/semantics/methods.k:140-140`
  - `reference-semantics/semantics/methods.k:145-145`
  - `reference-semantics/semantics/methods.k:149-149`
  - `reference-semantics/semantics/methods.k:154-154`
  - `reference-semantics/semantics/methods.k:158-158`
  - `reference-semantics/semantics/methods.k:162-162`
  - `reference-semantics/semantics/methods.k:166-166`
  - `reference-semantics/semantics/range.k:9-9`
  - `reference-semantics/semantics/range.k:12-12`
  - `reference-semantics/semantics/set.k:11-11`
  - `reference-semantics/semantics/set.k:16-17`
  - `reference-semantics/semantics/set.k:25-25`
  - `reference-semantics/semantics/set.k:31-31`
  - `reference-semantics/semantics/set.k:35-35`
  - `reference-semantics/semantics/sort.k:18-18`
  - `reference-semantics/semantics/sort.k:19-19`
  - `reference-semantics/semantics/sort.k:26-26`
  - `reference-semantics/semantics/sort.k:49-49`
  - `reference-semantics/semantics/sort.k:51-52`
  - `reference-semantics/semantics/sort.k:57-57`
  - `reference-semantics/semantics/str.k:13-13`
  - `reference-semantics/semantics/str.k:20-20`
  - `reference-semantics/semantics/str.k:32-32`
  - `reference-semantics/semantics/str.k:37-37`
  - `reference-semantics/semantics/str.k:48-48`
  - `reference-semantics/semantics/subscript.k:11-11`
  - `reference-semantics/semantics/subscript.k:16-16`
  - `reference-semantics/semantics/subscript.k:21-21`
  - `reference-semantics/semantics/subscript.k:37-37`
  - `reference-semantics/semantics/subscript.k:63-63`
  - `reference-semantics/semantics/subscript.k:72-72`
  - `reference-semantics/semantics/subscript.k:76-76`
  - `reference-semantics/semantics/subscript.k:83-83`
  - `reference-semantics/semantics/subscript.k:90-90`
  - `reference-semantics/semantics/subscript.k:96-96`
  - `reference-semantics/semantics/subscript.k:102-102`
  - `reference-semantics/semantics/subscript.k:109-109`
  - `reference-semantics/semantics/subscript.k:116-116`
  - `reference-semantics/semantics/tuple.k:24-24`
  - `verification.k:36-36`
  - `verification.k:41-41`
  - `verification.k:48-48`
  - `verification.k:53-53`
  - `verification.k:63-64`
- `functional`: 0 declaration block(s)
- `total`: 112 declaration block(s)
  - `reference-semantics/semantics/builtins.k:36-36`
  - `reference-semantics/semantics/builtins.k:114-114`
  - `reference-semantics/semantics/builtins.k:117-117`
  - `reference-semantics/semantics/builtins.k:126-126`
  - `reference-semantics/semantics/builtins.k:134-134`
  - `reference-semantics/semantics/builtins.k:158-158`
  - `reference-semantics/semantics/builtins.k:194-194`
  - `reference-semantics/semantics/builtins.k:196-196`
  - `reference-semantics/semantics/builtins.k:199-199`
  - `reference-semantics/semantics/builtins.k:203-203`
  - `reference-semantics/semantics/builtins.k:214-215`
  - `reference-semantics/semantics/builtins.k:226-226`
  - `reference-semantics/semantics/builtins.k:230-230`
  - `reference-semantics/semantics/builtins.k:238-238`
  - `reference-semantics/semantics/builtins.k:244-244`
  - `reference-semantics/semantics/builtins.k:247-247`
  - `reference-semantics/semantics/builtins.k:250-250`
  - `reference-semantics/semantics/builtins.k:255-255`
  - `reference-semantics/semantics/builtins.k:265-265`
  - `reference-semantics/semantics/builtins.k:269-269`
  - `reference-semantics/semantics/builtins.k:272-272`
  - `reference-semantics/semantics/builtins.k:285-285`
  - `reference-semantics/semantics/call.k:52-52`
  - `reference-semantics/semantics/concrete.k:56-56`
  - `reference-semantics/semantics/core.k:68-68`
  - `reference-semantics/semantics/core.k:76-76`
  - `reference-semantics/semantics/core.k:100-100`
  - `reference-semantics/semantics/core.k:109-109`
  - `reference-semantics/semantics/core.k:157-157`
  - `reference-semantics/semantics/core.k:213-213`
  - `reference-semantics/semantics/core.k:217-217`
  - `reference-semantics/semantics/core.k:223-223`
  - `reference-semantics/semantics/core.k:227-227`
  - `reference-semantics/semantics/core.k:233-233`
  - `reference-semantics/semantics/dict.k:37-37`
  - `reference-semantics/semantics/dict.k:43-43`
  - `reference-semantics/semantics/dict.k:49-49`
  - `reference-semantics/semantics/dict.k:90-90`
  - `reference-semantics/semantics/float.k:24-24`
  - `reference-semantics/semantics/float.k:30-30`
  - `reference-semantics/semantics/float.k:37-37`
  - `reference-semantics/semantics/float.k:50-50`
  - `reference-semantics/semantics/float.k:54-54`
  - `reference-semantics/semantics/float.k:73-73`
  - `reference-semantics/semantics/float.k:86-86`
  - `reference-semantics/semantics/float.k:93-93`
  - `reference-semantics/semantics/float.k:103-103`
  - `reference-semantics/semantics/float.k:107-107`
  - `reference-semantics/semantics/float.k:111-111`
  - `reference-semantics/semantics/float.k:115-115`
  - `reference-semantics/semantics/float.k:119-119`
  - `reference-semantics/semantics/float.k:125-125`
  - `reference-semantics/semantics/float.k:142-142`
  - `reference-semantics/semantics/float.k:160-160`
  - `reference-semantics/semantics/float.k:167-167`
  - `reference-semantics/semantics/float.k:173-173`
  - `reference-semantics/semantics/float.k:179-179`
  - `reference-semantics/semantics/float.k:190-190`
  - `reference-semantics/semantics/float.k:195-195`
  - `reference-semantics/semantics/float.k:209-209`
  - `reference-semantics/semantics/float.k:217-217`
  - `reference-semantics/semantics/float.k:223-223`
  - `reference-semantics/semantics/float.k:230-230`
  - `reference-semantics/semantics/list.k:18-18`
  - `reference-semantics/semantics/list.k:33-33`
  - `reference-semantics/semantics/methods.k:27-27`
  - `reference-semantics/semantics/methods.k:41-41`
  - `reference-semantics/semantics/methods.k:48-48`
  - `reference-semantics/semantics/methods.k:52-52`
  - `reference-semantics/semantics/methods.k:65-65`
  - `reference-semantics/semantics/methods.k:85-85`
  - `reference-semantics/semantics/methods.k:106-106`
  - `reference-semantics/semantics/methods.k:112-112`
  - `reference-semantics/semantics/methods.k:115-115`
  - `reference-semantics/semantics/methods.k:118-118`
  - `reference-semantics/semantics/methods.k:121-121`
  - `reference-semantics/semantics/methods.k:124-124`
  - `reference-semantics/semantics/methods.k:128-128`
  - `reference-semantics/semantics/methods.k:132-132`
  - `reference-semantics/semantics/methods.k:136-136`
  - `reference-semantics/semantics/methods.k:140-140`
  - `reference-semantics/semantics/methods.k:145-145`
  - `reference-semantics/semantics/methods.k:149-149`
  - `reference-semantics/semantics/methods.k:154-154`
  - `reference-semantics/semantics/methods.k:158-158`
  - `reference-semantics/semantics/methods.k:162-162`
  - `reference-semantics/semantics/methods.k:166-166`
  - `reference-semantics/semantics/range.k:9-9`
  - `reference-semantics/semantics/set.k:11-11`
  - `reference-semantics/semantics/set.k:16-17`
  - `reference-semantics/semantics/set.k:25-25`
  - `reference-semantics/semantics/set.k:31-31`
  - `reference-semantics/semantics/set.k:35-35`
  - `reference-semantics/semantics/sort.k:18-18`
  - `reference-semantics/semantics/sort.k:49-49`
  - `reference-semantics/semantics/sort.k:51-52`
  - `reference-semantics/semantics/sort.k:57-57`
  - `reference-semantics/semantics/str.k:20-20`
  - `reference-semantics/semantics/str.k:32-32`
  - `reference-semantics/semantics/str.k:37-37`
  - `reference-semantics/semantics/str.k:48-48`
  - `reference-semantics/semantics/subscript.k:11-11`
  - `reference-semantics/semantics/subscript.k:21-21`
  - `reference-semantics/semantics/subscript.k:72-72`
  - `reference-semantics/semantics/subscript.k:90-90`
  - `reference-semantics/semantics/subscript.k:96-96`
  - `reference-semantics/semantics/subscript.k:102-102`
  - `verification.k:36-36`
  - `verification.k:41-41`
  - `verification.k:48-48`
  - `verification.k:53-53`
  - `verification.k:63-64`
- `macro`: 7 declaration block(s)
  - `reference-semantics/semantics/comprehension.k:14-14`
  - `reference-semantics/semantics/comprehension.k:18-18`
  - `reference-semantics/semantics/comprehension.k:24-24`
  - `reference-semantics/semantics/syntax.k:9-30`
  - `verification.k:8-8`
  - `verification.k:14-14`
  - `verification.k:24-24`
- `simplification`: 0 declaration block(s)
- `concrete`: 35 declaration block(s)
  - `reference-semantics/semantics/float.k:25-25`
  - `reference-semantics/semantics/float.k:31-31`
  - `reference-semantics/semantics/float.k:38-38`
  - `reference-semantics/semantics/float.k:51-51`
  - `reference-semantics/semantics/float.k:55-55`
  - `reference-semantics/semantics/float.k:74-74`
  - `reference-semantics/semantics/float.k:75-75`
  - `reference-semantics/semantics/float.k:87-87`
  - `reference-semantics/semantics/float.k:88-88`
  - `reference-semantics/semantics/float.k:94-94`
  - `reference-semantics/semantics/float.k:95-95`
  - `reference-semantics/semantics/float.k:104-104`
  - `reference-semantics/semantics/float.k:108-108`
  - `reference-semantics/semantics/float.k:112-112`
  - `reference-semantics/semantics/float.k:116-116`
  - `reference-semantics/semantics/float.k:120-120`
  - `reference-semantics/semantics/float.k:126-126`
  - `reference-semantics/semantics/float.k:143-143`
  - `reference-semantics/semantics/float.k:161-161`
  - `reference-semantics/semantics/float.k:162-164`
  - `reference-semantics/semantics/float.k:191-191`
  - `reference-semantics/semantics/float.k:196-196`
  - `reference-semantics/semantics/float.k:210-210`
  - `reference-semantics/semantics/float.k:218-222`
  - `reference-semantics/semantics/float.k:224-226`
  - `reference-semantics/semantics/float.k:231-231`
  - `reference-semantics/semantics/sort.k:20-20`
  - `reference-semantics/semantics/sort.k:21-21`
  - `reference-semantics/semantics/sort.k:22-22`
  - `reference-semantics/semantics/sort.k:23-23`
  - `reference-semantics/semantics/sort.k:24-24`
  - `reference-semantics/semantics/sort.k:27-27`
  - `reference-semantics/semantics/sort.k:28-28`
  - `reference-semantics/semantics/sort.k:29-30`
  - `reference-semantics/semantics/sort.k:31-32`
- `owise`: 26 declaration block(s)
  - `reference-semantics/semantics/builtins.k:198-198`
  - `reference-semantics/semantics/builtins.k:201-201`
  - `reference-semantics/semantics/builtins.k:223-223`
  - `reference-semantics/semantics/builtins.k:228-228`
  - `reference-semantics/semantics/builtins.k:236-236`
  - `reference-semantics/semantics/builtins.k:243-243`
  - `reference-semantics/semantics/builtins.k:263-264`
  - `reference-semantics/semantics/builtins.k:268-268`
  - `reference-semantics/semantics/builtins.k:295-295`
  - `reference-semantics/semantics/builtins.k:297-297`
  - `reference-semantics/semantics/call.k:20-20`
  - `reference-semantics/semantics/call.k:31-31`
  - `reference-semantics/semantics/concrete.k:59-59`
  - `reference-semantics/semantics/controls.k:36-36`
  - `reference-semantics/semantics/controls.k:89-89`
  - `reference-semantics/semantics/controls.k:91-91`
  - `reference-semantics/semantics/core.k:70-70`
  - `reference-semantics/semantics/core.k:78-78`
  - `reference-semantics/semantics/core.k:102-102`
  - `reference-semantics/semantics/dict.k:54-54`
  - `reference-semantics/semantics/list.k:50-50`
  - `reference-semantics/semantics/methods.k:43-43`
  - `reference-semantics/semantics/methods.k:143-143`
  - `reference-semantics/semantics/methods.k:147-147`
  - `reference-semantics/semantics/methods.k:152-152`
  - `reference-semantics/semantics/operators.k:17-17`
- `priority`: 46 declaration block(s)
  - `reference-semantics/semantics/assert.k:13-15`
  - `reference-semantics/semantics/bool.k:29-30`
  - `reference-semantics/semantics/bool.k:31-34`
  - `reference-semantics/semantics/bool.k:35-38`
  - `reference-semantics/semantics/bool.k:39-42`
  - `reference-semantics/semantics/bool.k:43-46`
  - `reference-semantics/semantics/builtins.k:280-281`
  - `reference-semantics/semantics/call.k:38-41`
  - `reference-semantics/semantics/call.k:42-46`
  - `reference-semantics/semantics/call.k:47-50`
  - `reference-semantics/semantics/call.k:56-60`
  - `reference-semantics/semantics/call.k:63-67`
  - `reference-semantics/semantics/concrete.k:28-30`
  - `reference-semantics/semantics/concrete.k:31-33`
  - `reference-semantics/semantics/controls.k:12-18`
  - `reference-semantics/semantics/controls.k:27-31`
  - `reference-semantics/semantics/controls.k:95-97`
  - `reference-semantics/semantics/controls.k:98-100`
  - `reference-semantics/semantics/controls.k:101-103`
  - `reference-semantics/semantics/controls.k:106-108`
  - `reference-semantics/semantics/core.k:85-90`
  - `reference-semantics/semantics/core.k:145-151`
  - `reference-semantics/semantics/dict.k:58-60`
  - `reference-semantics/semantics/dict.k:65-66`
  - `reference-semantics/semantics/float.k:66-66`
  - `reference-semantics/semantics/float.k:71-71`
  - `reference-semantics/semantics/float.k:83-83`
  - `reference-semantics/semantics/float.k:233-233`
  - `reference-semantics/semantics/functions.k:68-75`
  - `reference-semantics/semantics/list.k:24-25`
  - `reference-semantics/semantics/list.k:53-55`
  - `reference-semantics/semantics/methods.k:72-74`
  - `reference-semantics/semantics/methods.k:89-91`
  - `reference-semantics/semantics/methods.k:94-96`
  - `reference-semantics/semantics/operators.k:25-27`
  - `reference-semantics/semantics/operators.k:28-31`
  - `reference-semantics/semantics/operators.k:34-37`
  - `reference-semantics/semantics/operators.k:38-42`
  - `reference-semantics/semantics/operators.k:44-46`
  - `reference-semantics/semantics/sort.k:40-42`
  - `reference-semantics/semantics/subscript.k:31-33`
  - `reference-semantics/semantics/subscript.k:58-60`
  - `reference-semantics/semantics/tuple.k:35-41`
  - `reference-semantics/semantics/tuple.k:44-46`
  - `reference-semantics/semantics/tuple.k:52-54`
  - `verification.k:77-86`
- `strict`: 2 declaration block(s)
  - `reference-semantics/semantics/syntax.k:9-30`
  - `reference-semantics/semantics/syntax.k:41-54`
- `seqstrict`: 1 declaration block(s)
  - `reference-semantics/semantics/syntax.k:9-30`
- `symbol`: 25 declaration block(s)
  - `reference-semantics/semantics/builtins.k:285-285`
  - `reference-semantics/semantics/float.k:24-24`
  - `reference-semantics/semantics/float.k:30-30`
  - `reference-semantics/semantics/float.k:37-37`
  - `reference-semantics/semantics/float.k:50-50`
  - `reference-semantics/semantics/float.k:54-54`
  - `reference-semantics/semantics/float.k:73-73`
  - `reference-semantics/semantics/float.k:86-86`
  - `reference-semantics/semantics/float.k:93-93`
  - `reference-semantics/semantics/float.k:103-103`
  - `reference-semantics/semantics/float.k:107-107`
  - `reference-semantics/semantics/float.k:111-111`
  - `reference-semantics/semantics/float.k:115-115`
  - `reference-semantics/semantics/float.k:119-119`
  - `reference-semantics/semantics/float.k:125-125`
  - `reference-semantics/semantics/float.k:142-142`
  - `reference-semantics/semantics/float.k:160-160`
  - `reference-semantics/semantics/float.k:190-190`
  - `reference-semantics/semantics/float.k:195-195`
  - `reference-semantics/semantics/float.k:209-209`
  - `reference-semantics/semantics/float.k:217-217`
  - `reference-semantics/semantics/float.k:223-223`
  - `reference-semantics/semantics/float.k:230-230`
  - `reference-semantics/semantics/sort.k:18-18`
  - `reference-semantics/semantics/sort.k:49-49`
- `hook`: 0 declaration block(s)
- `token`: 2 declaration block(s)
  - `reference-semantics/semantics/methods.k:75-75`
  - `reference-semantics/semantics/methods.k:97-97`

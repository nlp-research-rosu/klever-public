# Stage 5 exhaustive K source inventory

Every source-level `syntax`, `rule`, `context`, `configuration`, `claim`, and `alias` declaration in the fresh trusted semantics plus candidate `verification.k` is listed below. `USED-*` marks the dependency slice of the submitted program; unused fixed-model entries were checked for overlap with used terms and have none.

Total inventory entries: **1021**.

| # | Location | Kind | Attributes/class | Review decision | Source excerpt |
|---:|---|---|---|---|---|
| 1 | `semantics/assert.k:6` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| 2 | `semantics/assert.k:8` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| 3 | `semantics/assert.k:13` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 4 | `semantics/bool.k:8` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 5 | `semantics/bool.k:10` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 6 | `semantics/bool.k:11` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| 7 | `semantics/bool.k:17` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(OP:String, B:Bool, I:Int) => applyCmp(OP, boolAsInt(B), I) requires isEqOrdOp(OP)` |
| 8 | `semantics/bool.k:19` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(OP:String, I:Int, B:Bool) => applyCmp(OP, I, boolAsInt(B)) requires isEqOrdOp(OP)` |
| 9 | `semantics/bool.k:21` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(OP:String, B1:Bool, B2:Bool) => applyCmp(OP, boolAsInt(B1), boolAsInt(B2)) requires isOrdOp(OP)` |
| 10 | `semantics/bool.k:27` | context | — | USED-PATH-SOUND | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 11 | `semantics/bool.k:28` | rule | — | USED-PATH-SOUND | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 12 | `semantics/bool.k:29` | rule | — | USED-PATH-SOUND | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| 13 | `semantics/bool.k:31` | rule | — | USED-PATH-SOUND | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| 14 | `semantics/bool.k:33` | rule | — | USED-PATH-SOUND | `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| 15 | `semantics/bool.k:35` | rule | — | USED-PATH-SOUND | `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` |
| 16 | `semantics/bool.k:40` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| 17 | `semantics/bool.k:42` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 18 | `semantics/bool.k:46` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 19 | `semantics/bool.k:50` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 20 | `semantics/bool.k:54` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 21 | `semantics/builtins.k:17` | syntax | function | USED-PATH-SOUND | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| 22 | `semantics/builtins.k:20` | syntax | function | USED-PATH-SOUND | `syntax Int ::= seqLen(Val) [function]` |
| 23 | `semantics/builtins.k:21` | rule | — | USED-PATH-SOUND | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 24 | `semantics/builtins.k:22` | rule | — | USED-PATH-SOUND | `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)` |
| 25 | `semantics/builtins.k:23` | rule | — | USED-PATH-SOUND | `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)` |
| 26 | `semantics/builtins.k:24` | rule | — | USED-PATH-SOUND | `rule seqLen(str(IS:IntSeq))                   => isLen(IS)` |
| 27 | `semantics/builtins.k:25` | rule | — | USED-PATH-SOUND | `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)` |
| 28 | `semantics/builtins.k:26` | rule | — | USED-PATH-SOUND | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| 29 | `semantics/builtins.k:32` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>` |
| 30 | `semantics/builtins.k:33` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 31 | `semantics/builtins.k:34` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>` |
| 32 | `semantics/builtins.k:35` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>` |
| 33 | `semantics/builtins.k:36` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 34 | `semantics/builtins.k:37` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule charsOf(.IntSeq)                => .ValSeq` |
| 35 | `semantics/builtins.k:38` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| 36 | `semantics/builtins.k:41` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| 37 | `semantics/builtins.k:44` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| 38 | `semantics/builtins.k:47` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 39 | `semantics/builtins.k:48` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 40 | `semantics/builtins.k:49` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 41 | `semantics/builtins.k:50` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| 42 | `semantics/builtins.k:54` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= intOf(Val) [function]` |
| 43 | `semantics/builtins.k:55` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule intOf(I:Int)  => I` |
| 44 | `semantics/builtins.k:56` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| 45 | `semantics/builtins.k:59` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 46 | `semantics/builtins.k:60` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 47 | `semantics/builtins.k:61` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 48 | `semantics/builtins.k:62` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| 49 | `semantics/builtins.k:64` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| 50 | `semantics/builtins.k:67` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 51 | `semantics/builtins.k:68` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 52 | `semantics/builtins.k:69` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 53 | `semantics/builtins.k:70` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| 54 | `semantics/builtins.k:72` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` |
| 55 | `semantics/builtins.k:76` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 56 | `semantics/builtins.k:77` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 57 | `semantics/builtins.k:78` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 58 | `semantics/builtins.k:80` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 59 | `semantics/builtins.k:81` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 60 | `semantics/builtins.k:82` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 61 | `semantics/builtins.k:86` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 62 | `semantics/builtins.k:87` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 63 | `semantics/builtins.k:88` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 64 | `semantics/builtins.k:90` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 65 | `semantics/builtins.k:91` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 66 | `semantics/builtins.k:92` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 67 | `semantics/builtins.k:105` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #maxAccV(Iterable, Val) \| #maxContV(Val)` |
| 68 | `semantics/builtins.k:106` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccV(R, V) ... </k> requires isBool(V) orBool isStr(V)` |
| 69 | `semantics/builtins.k:108` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #iterYield(V, R) ~> #maxContV(M) ... </k> requires isFloat(V) orBool isBool(V)` |
| 70 | `semantics/builtins.k:111` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #maxAccV(IT:Iterable, M:Val) => #iterNext(IT) ~> #maxContV(M) ... </k>` |
| 71 | `semantics/builtins.k:112` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #maxContV(M:Val) => M ... </k>` |
| 72 | `semantics/builtins.k:113` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContV(M:Val) => #maxAccV(R, V) ... </k> requires applyCmp(">", V, M)` |
| 73 | `semantics/builtins.k:115` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContV(M:Val) => #maxAccV(R, M) ... </k> requires notBool applyCmp(">", V, M)` |
| 74 | `semantics/builtins.k:118` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #minAccV(Iterable, Val) \| #minContV(Val)` |
| 75 | `semantics/builtins.k:119` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccV(R, V) ... </k> requires isBool(V) orBool isStr(V)` |
| 76 | `semantics/builtins.k:121` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #iterYield(V, R) ~> #minContV(M) ... </k> requires isFloat(V) orBool isBool(V)` |
| 77 | `semantics/builtins.k:124` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #minAccV(IT:Iterable, M:Val) => #iterNext(IT) ~> #minContV(M) ... </k>` |
| 78 | `semantics/builtins.k:125` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #minContV(M:Val) => M ... </k>` |
| 79 | `semantics/builtins.k:126` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContV(M:Val) => #minAccV(R, V) ... </k> requires applyCmp("<", V, M)` |
| 80 | `semantics/builtins.k:128` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContV(M:Val) => #minAccV(R, M) ... </k> requires notBool applyCmp("<", V, M)` |
| 81 | `semantics/builtins.k:135` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= maxVals(Val, Vals) [function]` |
| 82 | `semantics/builtins.k:136` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 83 | `semantics/builtins.k:137` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("max", V:Val, (V2:Val, REST:Vals)) => maxVals(V, (V2, REST)) requires isFloat(V) orBool isBool(V) orBool isStr(V)` |
| 84 | `semantics/builtins.k:139` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule maxVals(M:Val, .Vals)           => M` |
| 85 | `semantics/builtins.k:140` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule maxVals(M:Val, (V:Val, R:Vals)) => maxVals(V, R) requires applyCmp(">", V, M)` |
| 86 | `semantics/builtins.k:141` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule maxVals(M:Val, (V:Val, R:Vals)) => maxVals(M, R) requires notBool applyCmp(">", V, M)` |
| 87 | `semantics/builtins.k:143` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= minVals(Val, Vals) [function]` |
| 88 | `semantics/builtins.k:144` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 89 | `semantics/builtins.k:145` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("min", V:Val, (V2:Val, REST:Vals)) => minVals(V, (V2, REST)) requires isFloat(V) orBool isBool(V) orBool isStr(V)` |
| 90 | `semantics/builtins.k:147` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule minVals(M:Val, .Vals)           => M` |
| 91 | `semantics/builtins.k:148` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule minVals(M:Val, (V:Val, R:Vals)) => minVals(V, R) requires applyCmp("<", V, M)` |
| 92 | `semantics/builtins.k:149` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule minVals(M:Val, (V:Val, R:Vals)) => minVals(M, R) requires notBool applyCmp("<", V, M)` |
| 93 | `semantics/builtins.k:152` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` |
| 94 | `semantics/builtins.k:155` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| 95 | `semantics/builtins.k:158` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 96 | `semantics/builtins.k:159` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 97 | `semantics/builtins.k:160` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 98 | `semantics/builtins.k:161` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 99 | `semantics/builtins.k:162` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 100 | `semantics/builtins.k:163` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` |
| 101 | `semantics/builtins.k:168` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| 102 | `semantics/builtins.k:170` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 103 | `semantics/builtins.k:171` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 104 | `semantics/builtins.k:172` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` |
| 105 | `semantics/builtins.k:176` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| 106 | `semantics/builtins.k:178` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 107 | `semantics/builtins.k:179` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 108 | `semantics/builtins.k:180` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 109 | `semantics/builtins.k:181` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| 110 | `semantics/builtins.k:184` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| 111 | `semantics/builtins.k:187` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 112 | `semantics/builtins.k:188` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` |
| 113 | `semantics/builtins.k:192` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))` |
| 114 | `semantics/builtins.k:193` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| 115 | `semantics/builtins.k:196` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` |
| 116 | `semantics/builtins.k:200` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| 117 | `semantics/builtins.k:202` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 118 | `semantics/builtins.k:203` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule intDigAcc(.IntSeq, ACC:Int)             => ACC` |
| 119 | `semantics/builtins.k:204` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| 120 | `semantics/builtins.k:207` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 121 | `semantics/builtins.k:208` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)` |
| 122 | `semantics/builtins.k:211` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| 123 | `semantics/builtins.k:213` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>` |
| 124 | `semantics/builtins.k:214` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 125 | `semantics/builtins.k:215` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| 126 | `semantics/builtins.k:217` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>` |
| 127 | `semantics/builtins.k:218` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| 128 | `semantics/builtins.k:221` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)` |
| 129 | `semantics/builtins.k:222` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)` |
| 130 | `semantics/builtins.k:223` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` |
| 131 | `semantics/builtins.k:231` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 132 | `semantics/builtins.k:232` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= evalArith(IntSeq) [function]` |
| 133 | `semantics/builtins.k:233` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| 134 | `semantics/builtins.k:236` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| 135 | `semantics/builtins.k:238` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= evDigit(Int) [function, total]` |
| 136 | `semantics/builtins.k:239` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 137 | `semantics/builtins.k:240` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 138 | `semantics/builtins.k:241` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 139 | `semantics/builtins.k:242` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule evHead42(_:IntSeq)            => false [owise]` |
| 140 | `semantics/builtins.k:243` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 141 | `semantics/builtins.k:244` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 142 | `semantics/builtins.k:245` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule evHead47(_:IntSeq)            => false [owise]` |
| 143 | `semantics/builtins.k:247` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 144 | `semantics/builtins.k:248` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokOps(.IntSeq)                 => .OpSeq` |
| 145 | `semantics/builtins.k:249` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)` |
| 146 | `semantics/builtins.k:250` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)` |
| 147 | `semantics/builtins.k:251` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 148 | `semantics/builtins.k:252` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 149 | `semantics/builtins.k:253` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 150 | `semantics/builtins.k:254` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 151 | `semantics/builtins.k:255` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))` |
| 152 | `semantics/builtins.k:256` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))` |
| 153 | `semantics/builtins.k:258` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| 154 | `semantics/builtins.k:260` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokNds(.IntSeq)                => .IntSeq` |
| 155 | `semantics/builtins.k:261` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)` |
| 156 | `semantics/builtins.k:262` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 157 | `semantics/builtins.k:263` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| 158 | `semantics/builtins.k:265` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| 159 | `semantics/builtins.k:267` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 160 | `semantics/builtins.k:269` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 161 | `semantics/builtins.k:270` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 162 | `semantics/builtins.k:271` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 163 | `semantics/builtins.k:272` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 164 | `semantics/builtins.k:274` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 165 | `semantics/builtins.k:275` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyOpE("+",  A:Int, B:Int) => A +Int B` |
| 166 | `semantics/builtins.k:276` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyOpE("-",  A:Int, B:Int) => A -Int B` |
| 167 | `semantics/builtins.k:277` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyOpE("*",  A:Int, B:Int) => A *Int B` |
| 168 | `semantics/builtins.k:278` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 169 | `semantics/builtins.k:279` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 170 | `semantics/builtins.k:280` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 171 | `semantics/builtins.k:282` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 172 | `semantics/builtins.k:283` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 173 | `semantics/builtins.k:284` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 174 | `semantics/builtins.k:285` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| 175 | `semantics/builtins.k:287` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 176 | `semantics/builtins.k:288` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 177 | `semantics/builtins.k:289` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 178 | `semantics/builtins.k:290` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 179 | `semantics/builtins.k:291` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 180 | `semantics/builtins.k:292` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 181 | `semantics/builtins.k:294` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 182 | `semantics/builtins.k:295` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 183 | `semantics/builtins.k:296` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 184 | `semantics/builtins.k:297` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 185 | `semantics/builtins.k:298` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 186 | `semantics/builtins.k:299` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 187 | `semantics/builtins.k:300` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 188 | `semantics/builtins.k:301` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| 189 | `semantics/builtins.k:304` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| 190 | `semantics/builtins.k:307` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| 191 | `semantics/builtins.k:309` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 192 | `semantics/builtins.k:310` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 193 | `semantics/builtins.k:311` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 194 | `semantics/builtins.k:312` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule inLevelE(_:String, _:String) => false [owise]` |
| 195 | `semantics/builtins.k:313` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 196 | `semantics/builtins.k:314` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 197 | `semantics/builtins.k:315` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 198 | `semantics/builtins.k:316` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 199 | `semantics/builtins.k:317` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 200 | `semantics/builtins.k:318` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| 201 | `semantics/builtins.k:323` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= "#md5"` |
| 202 | `semantics/builtins.k:324` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| 203 | `semantics/builtins.k:326` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 204 | `semantics/builtins.k:327` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= md5Obj(IntSeq)` |
| 205 | `semantics/builtins.k:328` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 206 | `semantics/builtins.k:329` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| 207 | `semantics/builtins.k:335` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 208 | `semantics/builtins.k:336` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 209 | `semantics/builtins.k:337` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 210 | `semantics/builtins.k:338` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule isIntV(_:Int)         => true` |
| 211 | `semantics/builtins.k:340` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule isIntV(_:Bool)        => true` |
| 212 | `semantics/builtins.k:341` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule isIntV(_:Val)         => false [owise]` |
| 213 | `semantics/builtins.k:342` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule isStrV(str(_:IntSeq)) => true` |
| 214 | `semantics/builtins.k:343` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule isStrV(_:Val)         => false [owise]` |
| 215 | `semantics/call.k:16` | rule | — | USED-PATH-SOUND | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| 216 | `semantics/call.k:19` | syntax | — | USED-PATH-SOUND | `syntax KItem ::= #callee(Exprs)` |
| 217 | `semantics/call.k:20` | rule | owise | USED-PATH-SOUND | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 218 | `semantics/call.k:21` | rule | — | USED-PATH-SOUND | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| 219 | `semantics/call.k:24` | rule | — | USED-PATH-SOUND | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 220 | `semantics/call.k:26` | rule | — | USED-PATH-SOUND | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 221 | `semantics/call.k:27` | rule | — | USED-PATH-SOUND | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>` |
| 222 | `semantics/call.k:28` | rule | — | USED-PATH-SOUND | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>` |
| 223 | `semantics/call.k:29` | rule | — | USED-PATH-SOUND | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>` |
| 224 | `semantics/call.k:30` | rule | — | USED-PATH-SOUND | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>` |
| 225 | `semantics/call.k:31` | rule | owise | USED-PATH-SOUND | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 226 | `semantics/call.k:32` | rule | — | USED-PATH-SOUND | `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>` |
| 227 | `semantics/call.k:38` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 228 | `semantics/call.k:42` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)…` |
| 229 | `semantics/call.k:47` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 230 | `semantics/call.k:52` | syntax | function, total | USED-PATH-SOUND | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 231 | `semantics/call.k:53` | rule | — | USED-PATH-SOUND | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| 232 | `semantics/call.k:56` | rule | priority | USED-PATH-SOUND | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` |
| 233 | `semantics/call.k:63` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M…` |
| 234 | `semantics/call.k:69` | rule | — | USED-PATH-SOUND | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEW…` |
| 235 | `semantics/call.k:80` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> …` |
| 236 | `semantics/call.k:87` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #allocCells(ParamNames)` |
| 237 | `semantics/call.k:88` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 238 | `semantics/call.k:89` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N \|-> cellV(noneV))…` |
| 239 | `semantics/comprehension.k:11` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 240 | `semantics/comprehension.k:12` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 241 | `semantics/comprehension.k:14` | syntax | macro | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 242 | `semantics/comprehension.k:15` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| 243 | `semantics/comprehension.k:18` | syntax | macro-rec, macro | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 244 | `semantics/comprehension.k:19` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| 245 | `semantics/comprehension.k:21` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| 246 | `semantics/comprehension.k:24` | syntax | macro | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 247 | `semantics/comprehension.k:25` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule compGuard(.Exprs)             => Bool(true)` |
| 248 | `semantics/comprehension.k:26` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| 249 | `semantics/concrete.k:13` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 250 | `semantics/concrete.k:16` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 251 | `semantics/concrete.k:25` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= kvP(Val, Val)` |
| 252 | `semantics/concrete.k:26` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| 253 | `semantics/concrete.k:28` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| 254 | `semantics/concrete.k:31` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| 255 | `semantics/concrete.k:34` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| 256 | `semantics/concrete.k:36` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| 257 | `semantics/concrete.k:38` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| 258 | `semantics/concrete.k:42` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 259 | `semantics/concrete.k:43` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 260 | `semantics/concrete.k:44` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| 261 | `semantics/concrete.k:47` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| 262 | `semantics/concrete.k:51` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= kLt(Val, Val) [function]` |
| 263 | `semantics/concrete.k:52` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule kLt(I1:Int, I2:Int)             => I1 <Int I2` |
| 264 | `semantics/concrete.k:53` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule kLt(F1:Float, F2:Float)         => F1 <Float F2` |
| 265 | `semantics/concrete.k:54` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 266 | `semantics/concrete.k:58` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule kLt(I:Int, F:Float)   => ltIF(I, F)` |
| 267 | `semantics/concrete.k:59` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule kLt(F:Float, I:Int)   => ltFI(F, I)` |
| 268 | `semantics/concrete.k:60` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule kLt(B:Bool, V:Val)    => kLt(boolAsInt(B), V) requires isInt(V) orBool isFloat(V)` |
| 269 | `semantics/concrete.k:61` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule kLt(V:Val, B:Bool)    => kLt(V, boolAsInt(B)) requires isInt(V) orBool isFloat(V)` |
| 270 | `semantics/concrete.k:62` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule kLt(B1:Bool, B2:Bool) => boolAsInt(B1) <Int boolAsInt(B2)` |
| 271 | `semantics/concrete.k:64` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 272 | `semantics/concrete.k:65` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule unpairVS(.ValSeq) => .ValSeq` |
| 273 | `semantics/concrete.k:66` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 274 | `semantics/concrete.k:67` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| 275 | `semantics/concrete.k:77` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", true), .Vals)) => #alloc(list(revVS(sortVS(revVS(VS))))) ... </k> [priority(40)]` |
| 276 | `semantics/concrete.k:90` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= numOrKEq(Val, Val) [function]` |
| 277 | `semantics/concrete.k:91` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule numOrKEq(A:Val, B:Val) => applyCmp("==", A, B) requires (isInt(A) orBool isBool(A) orBool isFloat(A)) andBool (isInt(B) orBool isBool(B) orBool isFloat(B))` |
| 278 | `semantics/concrete.k:94` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule numOrKEq(A:Val, B:Val) => A ==K B [owise]` |
| 279 | `semantics/concrete.k:96` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires numOrKEq(E, V) [priority(40)]` |
| 280 | `semantics/concrete.k:98` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool numOrKEq(E, V) [priority(40)]` |
| 281 | `semantics/controls.k:9` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 282 | `semantics/controls.k:12` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells…` |
| 283 | `semantics/controls.k:20` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` |
| 284 | `semantics/controls.k:27` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV(…` |
| 285 | `semantics/controls.k:35` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 286 | `semantics/controls.k:36` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 287 | `semantics/controls.k:37` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #bindImports(ParamNames)` |
| 288 | `semantics/controls.k:38` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 289 | `semantics/controls.k:39` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N …` |
| 290 | `semantics/controls.k:43` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` |
| 291 | `semantics/controls.k:48` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Expr(_:Val) => .K ... </k>` |
| 292 | `semantics/controls.k:51` | syntax | — | USED-PATH-SOUND | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 293 | `semantics/controls.k:52` | rule | — | USED-PATH-SOUND | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 294 | `semantics/controls.k:53` | rule | — | USED-PATH-SOUND | `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>` |
| 295 | `semantics/controls.k:54` | rule | — | USED-PATH-SOUND | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| 296 | `semantics/controls.k:57` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| 297 | `semantics/controls.k:59` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` |
| 298 | `semantics/controls.k:65` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| 299 | `semantics/controls.k:69` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 300 | `semantics/controls.k:71` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 301 | `semantics/controls.k:72` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 302 | `semantics/controls.k:73` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` |
| 303 | `semantics/controls.k:77` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 304 | `semantics/controls.k:78` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 305 | `semantics/controls.k:79` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| 306 | `semantics/controls.k:81` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` |
| 307 | `semantics/controls.k:85` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 308 | `semantics/controls.k:86` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Continue => #cont ... </k>` |
| 309 | `semantics/controls.k:87` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Break => #brk ... </k>` |
| 310 | `semantics/controls.k:88` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 311 | `semantics/controls.k:89` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 312 | `semantics/controls.k:90` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 313 | `semantics/controls.k:91` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| 314 | `semantics/controls.k:95` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 315 | `semantics/controls.k:98` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 316 | `semantics/controls.k:101` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 317 | `semantics/controls.k:106` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 318 | `semantics/core.k:13` | syntax | — | USED-PATH-SOUND | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 319 | `semantics/core.k:14` | syntax | — | USED-PATH-SOUND | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 320 | `semantics/core.k:15` | syntax | — | USED-PATH-SOUND | `syntax Str    ::= str(IntSeq)` |
| 321 | `semantics/core.k:18` | syntax | — | USED-PATH-SOUND | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| 322 | `semantics/core.k:25` | syntax | function | USED-PATH-SOUND | `syntax Val      ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int)          // a heap object: <heap> holds its list(VS) \| cellRef(Int)      // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, St…` |
| 323 | `semantics/core.k:36` | syntax | — | USED-PATH-SOUND | `syntax Parent   ::= "root" \| parent(Int)` |
| 324 | `semantics/core.k:37` | syntax | — | USED-PATH-SOUND | `syntax Scope    ::= scope(Map, Parent)` |
| 325 | `semantics/core.k:38` | syntax | — | USED-PATH-SOUND | `syntax KResult  ::= Val` |
| 326 | `semantics/core.k:39` | syntax | — | USED-PATH-SOUND | `syntax Expr     ::= Val   // cooling puts results back into expression holes` |
| 327 | `semantics/core.k:40` | syntax | — | USED-PATH-SOUND | `syntax Vals     ::= List{Val, ","}` |
| 328 | `semantics/core.k:41` | syntax | — | USED-PATH-SOUND | `syntax Exc      ::= "NoExc" \| "AssertionError"` |
| 329 | `semantics/core.k:42` | syntax | — | USED-PATH-SOUND | `syntax RetState ::= "noRet" \| retV(Val)` |
| 330 | `semantics/core.k:49` | configuration | — | USED-PATH-SOUND | `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     \|-> scope(.Map, parent(-1)) -1    \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0…` |
| 331 | `semantics/core.k:68` | syntax | function, total | USED-PATH-SOUND | `syntax Bool ::= isRefV(Val) [function, total]` |
| 332 | `semantics/core.k:69` | rule | — | USED-PATH-SOUND | `rule isRefV(ref(_:Int)) => true` |
| 333 | `semantics/core.k:70` | rule | owise | USED-PATH-SOUND | `rule isRefV(_:Val)      => false [owise]` |
| 334 | `semantics/core.k:75` | syntax | — | USED-PATH-SOUND | `syntax HeapVal ::= cellV(Val)` |
| 335 | `semantics/core.k:76` | syntax | function, total | USED-PATH-SOUND | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 336 | `semantics/core.k:77` | rule | — | USED-PATH-SOUND | `rule isCellRef(cellRef(_:Int)) => true` |
| 337 | `semantics/core.k:78` | rule | owise | USED-PATH-SOUND | `rule isCellRef(_:Val)          => false [owise]` |
| 338 | `semantics/core.k:85` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` |
| 339 | `semantics/core.k:95` | syntax | — | USED-PATH-SOUND | `syntax Val ::= kwV(String, Val)` |
| 340 | `semantics/core.k:96` | syntax | — | USED-PATH-SOUND | `syntax KItem ::= #kwTag(String)` |
| 341 | `semantics/core.k:97` | rule | — | USED-PATH-SOUND | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 342 | `semantics/core.k:98` | rule | — | USED-PATH-SOUND | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| 343 | `semantics/core.k:100` | syntax | function, total | USED-PATH-SOUND | `syntax Bool ::= isKwV(Val) [function, total]` |
| 344 | `semantics/core.k:101` | rule | — | USED-PATH-SOUND | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 345 | `semantics/core.k:102` | rule | owise | USED-PATH-SOUND | `rule isKwV(_:Val)                => false [owise]` |
| 346 | `semantics/core.k:106` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= cellsMark(ParamNames)` |
| 347 | `semantics/core.k:107` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 348 | `semantics/core.k:108` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 349 | `semantics/core.k:109` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 350 | `semantics/core.k:110` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule pnMember(_:String, .ParamNames) => false` |
| 351 | `semantics/core.k:111` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 352 | `semantics/core.k:113` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #cellW(Val, Val)` |
| 353 | `semantics/core.k:114` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| 354 | `semantics/core.k:117` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #alloc(Val)` |
| 355 | `semantics/core.k:118` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 356 | `semantics/core.k:124` | syntax | — | USED-PATH-SOUND | `syntax KItem ::= #loadAll(Module)` |
| 357 | `semantics/core.k:125` | rule | — | USED-PATH-SOUND | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 358 | `semantics/core.k:126` | rule | — | USED-PATH-SOUND | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 359 | `semantics/core.k:127` | rule | — | USED-PATH-SOUND | `rule <k> .Stmts => .K ... </k>` |
| 360 | `semantics/core.k:130` | syntax | — | USED-PATH-SOUND | `syntax KItem ::= #look(String, Int)` |
| 361 | `semantics/core.k:131` | rule | — | USED-PATH-SOUND | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 362 | `semantics/core.k:132` | rule | — | USED-PATH-SOUND | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` |
| 363 | `semantics/core.k:145` | rule | priority | USED-PATH-SOUND | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMemb…` |
| 364 | `semantics/core.k:152` | rule | — | USED-PATH-SOUND | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` |
| 365 | `semantics/core.k:157` | syntax | function, total | USED-PATH-SOUND | `syntax Scope ::= "builtinsScope" [function, total]` |
| 366 | `semantics/core.k:158` | rule | — | USED-PATH-SOUND | `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ …` |
| 367 | `semantics/core.k:185` | syntax | — | USED-PATH-SOUND | `syntax ApplyK ::= toCall(Val)` |
| 368 | `semantics/core.k:186` | syntax | — | USED-PATH-SOUND | `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| 369 | `semantics/core.k:189` | rule | — | USED-PATH-SOUND | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 370 | `semantics/core.k:190` | rule | — | USED-PATH-SOUND | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 371 | `semantics/core.k:191` | rule | — | USED-PATH-SOUND | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| 372 | `semantics/core.k:194` | rule | — | USED-PATH-SOUND | `rule <k> Int(I:Int)   => I ... </k>` |
| 373 | `semantics/core.k:195` | rule | — | USED-PATH-SOUND | `rule <k> Bool(B:Bool) => B ... </k>` |
| 374 | `semantics/core.k:196` | rule | — | USED-PATH-SOUND | `rule <k> NoneVal      => noneV ... </k>` |
| 375 | `semantics/core.k:199` | syntax | function | USED-PATH-SOUND | `syntax Bool ::= truthy(Val) [function]` |
| 376 | `semantics/core.k:200` | rule | — | USED-PATH-SOUND | `rule truthy(B:Bool)          => B` |
| 377 | `semantics/core.k:201` | rule | — | USED-PATH-SOUND | `rule truthy(noneV)           => false` |
| 378 | `semantics/core.k:202` | rule | — | USED-PATH-SOUND | `rule truthy(I:Int)           => I =/=Int 0` |
| 379 | `semantics/core.k:203` | rule | — | USED-PATH-SOUND | `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)` |
| 380 | `semantics/core.k:204` | rule | — | USED-PATH-SOUND | `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)` |
| 381 | `semantics/core.k:205` | rule | — | USED-PATH-SOUND | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 382 | `semantics/core.k:208` | syntax | function | USED-PATH-SOUND | `syntax Val  ::= applyUn(String, Val) [function]` |
| 383 | `semantics/core.k:209` | syntax | function | USED-PATH-SOUND | `syntax Val  ::= applyBin(String, Val, Val) [function]` |
| 384 | `semantics/core.k:210` | syntax | function | USED-PATH-SOUND | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| 385 | `semantics/core.k:218` | syntax | function, total | USED-PATH-SOUND | `syntax Int ::= boolAsInt(Bool) [function, total]` |
| 386 | `semantics/core.k:219` | rule | — | USED-PATH-SOUND | `rule boolAsInt(true)  => 1` |
| 387 | `semantics/core.k:220` | rule | — | USED-PATH-SOUND | `rule boolAsInt(false) => 0` |
| 388 | `semantics/core.k:222` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= isArithOp(String) [function, total]` |
| 389 | `semantics/core.k:223` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule isArithOp(OP:String) => OP ==String "+"  orBool OP ==String "-"  orBool OP ==String "*" orBool OP ==String "/" orBool OP ==String "//" orBool OP ==String "%" orBool OP ==String "**"` |
| 390 | `semantics/core.k:228` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= isEqOrdOp(String) [function, total]` |
| 391 | `semantics/core.k:229` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule isEqOrdOp(OP:String) => OP ==String "==" orBool OP ==String "!=" orBool OP ==String "<" orBool OP ==String "<=" orBool OP ==String ">" orBool OP ==String ">="` |
| 392 | `semantics/core.k:233` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= isOrdOp(String) [function, total]` |
| 393 | `semantics/core.k:234` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule isOrdOp(OP:String) => OP ==String "<" orBool OP ==String "<=" orBool OP ==String ">" orBool OP ==String ">="` |
| 394 | `semantics/core.k:238` | syntax | function, total | USED-PATH-SOUND | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 395 | `semantics/core.k:239` | rule | — | USED-PATH-SOUND | `rule appendVal(.Vals, V:Val)              => V , .Vals` |
| 396 | `semantics/core.k:240` | rule | — | USED-PATH-SOUND | `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)` |
| 397 | `semantics/core.k:242` | syntax | function, total | USED-PATH-SOUND | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 398 | `semantics/core.k:243` | rule | — | USED-PATH-SOUND | `rule vals2valSeq(.Vals)            => .ValSeq` |
| 399 | `semantics/core.k:244` | rule | — | USED-PATH-SOUND | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| 400 | `semantics/core.k:248` | syntax | function, total | USED-PATH-SOUND | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 401 | `semantics/core.k:249` | rule | — | USED-PATH-SOUND | `rule vsLen(.ValSeq)                => 0` |
| 402 | `semantics/core.k:250` | rule | — | USED-PATH-SOUND | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 403 | `semantics/core.k:252` | syntax | function, total | USED-PATH-SOUND | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 404 | `semantics/core.k:253` | rule | — | USED-PATH-SOUND | `rule isLen(.IntSeq)                => 0` |
| 405 | `semantics/core.k:254` | rule | — | USED-PATH-SOUND | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| 406 | `semantics/core.k:258` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 407 | `semantics/core.k:259` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq` |
| 408 | `semantics/core.k:260` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)` |
| 409 | `semantics/core.k:261` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| 410 | `semantics/core.k:263` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0` |
| 411 | `semantics/dict.k:20` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| 412 | `semantics/dict.k:23` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| 413 | `semantics/dict.k:26` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 414 | `semantics/dict.k:27` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 415 | `semantics/dict.k:28` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| 416 | `semantics/dict.k:30` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| 417 | `semantics/dict.k:32` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` |
| 418 | `semantics/dict.k:37` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 419 | `semantics/dict.k:38` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dHasKey(.ValSeq, _:Val)                => false` |
| 420 | `semantics/dict.k:39` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K` |
| 421 | `semantics/dict.k:40` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| 422 | `semantics/dict.k:43` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 423 | `semantics/dict.k:44` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)` |
| 424 | `semantics/dict.k:45` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| 425 | `semantics/dict.k:49` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 426 | `semantics/dict.k:50` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K` |
| 427 | `semantics/dict.k:52` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| 428 | `semantics/dict.k:54` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| 429 | `semantics/dict.k:58` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` |
| 430 | `semantics/dict.k:63` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 431 | `semantics/dict.k:64` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 432 | `semantics/dict.k:65` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` |
| 433 | `semantics/dict.k:70` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 434 | `semantics/dict.k:71` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| 435 | `semantics/dict.k:76` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #dsetK(String, Val)` |
| 436 | `semantics/dict.k:77` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 437 | `semantics/dict.k:78` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool i…` |
| 438 | `semantics/dict.k:82` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| 439 | `semantics/dict.k:86` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 440 | `semantics/dict.k:87` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` |
| 441 | `semantics/dict.k:90` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 442 | `semantics/dict.k:91` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 443 | `semantics/dict.k:92` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0` |
| 444 | `semantics/dict.k:95` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| 445 | `semantics/dict.k:97` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 446 | `semantics/dict.k:98` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 447 | `semantics/dict.k:99` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| 448 | `semantics/dict.k:101` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 449 | `semantics/dict.k:102` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K` |
| 450 | `semantics/dict.k:103` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| 451 | `semantics/float.k:20` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= Float` |
| 452 | `semantics/float.k:21` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Float(F:Float) => F ... </k>` |
| 453 | `semantics/float.k:24` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 454 | `semantics/float.k:25` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 455 | `semantics/float.k:27` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| 456 | `semantics/float.k:30` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 457 | `semantics/float.k:31` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 458 | `semantics/float.k:32` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| 459 | `semantics/float.k:37` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 460 | `semantics/float.k:38` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 461 | `semantics/float.k:39` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| 462 | `semantics/float.k:43` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 463 | `semantics/float.k:44` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| 464 | `semantics/float.k:50` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 465 | `semantics/float.k:51` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 466 | `semantics/float.k:52` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 467 | `semantics/float.k:54` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 468 | `semantics/float.k:55` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 469 | `semantics/float.k:56` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| 470 | `semantics/float.k:61` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Import(_:String) => .K ... </k>` |
| 471 | `semantics/float.k:65` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= "#mathCeil"` |
| 472 | `semantics/float.k:66` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 473 | `semantics/float.k:67` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| 474 | `semantics/float.k:70` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= "#mathFloor"` |
| 475 | `semantics/float.k:71` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 476 | `semantics/float.k:72` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 477 | `semantics/float.k:73` | syntax | function, total, symbol | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 478 | `semantics/float.k:74` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule floorFI(I:Int)   => I                        [concrete]` |
| 479 | `semantics/float.k:75` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| 480 | `semantics/float.k:78` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 481 | `semantics/float.k:79` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)` |
| 482 | `semantics/float.k:82` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 483 | `semantics/float.k:83` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 484 | `semantics/float.k:84` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 485 | `semantics/float.k:85` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 486 | `semantics/float.k:86` | syntax | function, total, symbol | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 487 | `semantics/float.k:87` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule toF(F:Float) => F        [concrete]` |
| 488 | `semantics/float.k:88` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule toF(I:Int)   => intToF(I) [concrete]` |
| 489 | `semantics/float.k:93` | syntax | function, total, symbol | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 490 | `semantics/float.k:94` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule ceilF(I:Int)   => I                       [concrete]` |
| 491 | `semantics/float.k:95` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| 492 | `semantics/float.k:99` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| 493 | `semantics/float.k:103` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 494 | `semantics/float.k:104` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 495 | `semantics/float.k:105` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 496 | `semantics/float.k:107` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 497 | `semantics/float.k:108` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 498 | `semantics/float.k:109` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 499 | `semantics/float.k:111` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 500 | `semantics/float.k:112` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 501 | `semantics/float.k:113` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 502 | `semantics/float.k:115` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 503 | `semantics/float.k:116` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 504 | `semantics/float.k:117` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 505 | `semantics/float.k:119` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 506 | `semantics/float.k:120` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 507 | `semantics/float.k:121` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| 508 | `semantics/float.k:125` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 509 | `semantics/float.k:126` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 510 | `semantics/float.k:127` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)` |
| 511 | `semantics/float.k:128` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 512 | `semantics/float.k:129` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| 513 | `semantics/float.k:132` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 514 | `semantics/float.k:133` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 515 | `semantics/float.k:134` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)` |
| 516 | `semantics/float.k:135` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))` |
| 517 | `semantics/float.k:136` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)` |
| 518 | `semantics/float.k:137` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))` |
| 519 | `semantics/float.k:138` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)` |
| 520 | `semantics/float.k:139` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))` |
| 521 | `semantics/float.k:152` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 522 | `semantics/float.k:153` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 523 | `semantics/float.k:155` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Bool ::= floatFinite(Float) [function, total, symbol(floatFinite), no-evaluators]` |
| 524 | `semantics/float.k:156` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule floatFinite(F:Float) => notBool isNaN(F) andBool notBool isInfinite(F) [concrete]` |
| 525 | `semantics/float.k:158` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Bool ::= ltFI(Float, Int) [function, total, symbol(ltFI), no-evaluators]   // F <  I \| ltIF(Int, Float) [function, total, symbol(ltIF), no-evaluators]   // I <  F \| eqIF(Int, Float) [function, total, s…` |
| 526 | `semantics/float.k:161` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule ltFI(F:Float, I:Int) => Float2Int(floorFloat(F)) <Int I  requires floatFinite(F)          [concrete]` |
| 527 | `semantics/float.k:162` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule ltFI(F:Float, I:Int) => floatLt(F, intToF(I))            requires notBool floatFinite(F)   [concrete]` |
| 528 | `semantics/float.k:163` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule ltIF(I:Int, F:Float) => Float2Int(ceilFloat(F))  >Int I  requires floatFinite(F)          [concrete]` |
| 529 | `semantics/float.k:164` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule ltIF(I:Int, F:Float) => floatLt(intToF(I), F)            requires notBool floatFinite(F)   [concrete]` |
| 530 | `semantics/float.k:165` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule eqIF(I:Int, F:Float) => (floorFloat(F) ==Float ceilFloat(F)) andBool (Float2Int(floorFloat(F)) ==Int I) requires floatFinite(F) [concrete]` |
| 531 | `semantics/float.k:168` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule eqIF(I:Int, F:Float) => eqF(intToF(I), F) requires notBool floatFinite(F) [concrete]` |
| 532 | `semantics/float.k:170` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("==", I:Int, F:Float) => eqIF(I, F)` |
| 533 | `semantics/float.k:171` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("==", F:Float, I:Int) => eqIF(I, F)` |
| 534 | `semantics/float.k:172` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("!=", I:Int, F:Float) => notBool eqIF(I, F)` |
| 535 | `semantics/float.k:173` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("!=", F:Float, I:Int) => notBool eqIF(I, F)` |
| 536 | `semantics/float.k:174` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("<",  I:Int, F:Float) => ltIF(I, F)` |
| 537 | `semantics/float.k:175` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("<",  F:Float, I:Int) => ltFI(F, I)` |
| 538 | `semantics/float.k:176` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(">",  I:Int, F:Float) => ltFI(F, I)          // I >  F  <=>  F <  I` |
| 539 | `semantics/float.k:177` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(">",  F:Float, I:Int) => ltIF(I, F)          // F >  I  <=>  I <  F` |
| 540 | `semantics/float.k:178` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("<=", I:Int, F:Float) => notBool ltFI(F, I)  // I <= F  <=>  not (F < I)` |
| 541 | `semantics/float.k:179` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("<=", F:Float, I:Int) => notBool ltIF(I, F)  // F <= I  <=>  not (I < F)` |
| 542 | `semantics/float.k:180` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(">=", I:Int, F:Float) => notBool ltIF(I, F)  // I >= F  <=>  not (I < F)` |
| 543 | `semantics/float.k:181` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(">=", F:Float, I:Int) => notBool ltFI(F, I)  // F >= I  <=>  not (F < I)` |
| 544 | `semantics/float.k:184` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin(OP:String, B:Bool, F:Float) => applyBin(OP, boolAsInt(B), F) requires isArithOp(OP)` |
| 545 | `semantics/float.k:185` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin(OP:String, F:Float, B:Bool) => applyBin(OP, F, boolAsInt(B)) requires isArithOp(OP)` |
| 546 | `semantics/float.k:186` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(OP:String, B:Bool, F:Float) => applyCmp(OP, boolAsInt(B), F) requires isEqOrdOp(OP)` |
| 547 | `semantics/float.k:187` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(OP:String, F:Float, B:Bool) => applyCmp(OP, F, boolAsInt(B)) requires isEqOrdOp(OP)` |
| 548 | `semantics/float.k:190` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 549 | `semantics/float.k:191` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| 550 | `semantics/float.k:196` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 551 | `semantics/float.k:197` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 552 | `semantics/float.k:198` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| 553 | `semantics/float.k:201` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= headIS(IntSeq) [function]` |
| 554 | `semantics/float.k:202` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 555 | `semantics/float.k:203` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 556 | `semantics/float.k:204` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 557 | `semantics/float.k:205` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 558 | `semantics/float.k:206` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 559 | `semantics/float.k:207` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| 560 | `semantics/float.k:209` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 561 | `semantics/float.k:210` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fracPart(.IntSeq) => 0` |
| 562 | `semantics/float.k:211` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 563 | `semantics/float.k:212` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 564 | `semantics/float.k:213` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fracAcc(.IntSeq, A:Int) => A` |
| 565 | `semantics/float.k:214` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 566 | `semantics/float.k:215` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 567 | `semantics/float.k:216` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fracScale(.IntSeq) => 1` |
| 568 | `semantics/float.k:217` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 569 | `semantics/float.k:218` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 570 | `semantics/float.k:219` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fscAcc(.IntSeq, A:Int) => A` |
| 571 | `semantics/float.k:220` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 572 | `semantics/float.k:221` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 573 | `semantics/float.k:222` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)` |
| 574 | `semantics/float.k:223` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("float", F:Float, .Vals)        => F` |
| 575 | `semantics/float.k:226` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 576 | `semantics/float.k:227` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 577 | `semantics/float.k:228` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| 578 | `semantics/float.k:231` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 579 | `semantics/float.k:232` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 580 | `semantics/float.k:233` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 581 | `semantics/float.k:234` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 582 | `semantics/float.k:235` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 583 | `semantics/float.k:236` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 584 | `semantics/float.k:237` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 585 | `semantics/float.k:238` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 586 | `semantics/float.k:243` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 587 | `semantics/float.k:244` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 588 | `semantics/float.k:245` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 589 | `semantics/float.k:247` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)` |
| 590 | `semantics/float.k:248` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| 591 | `semantics/float.k:251` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 592 | `semantics/float.k:252` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F…` |
| 593 | `semantics/float.k:271` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 594 | `semantics/float.k:272` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule roundFN(F:Float, N:Int) => roundExactFN(F, N) requires notBool isNaN(F) andBool notBool isInfinite(F) andBool N >=Int 0 andBool absFloat(F) <Float 1000000000000.0 andBool (absFloat(F) *Float Int2Float(10 ^…` |
| 595 | `semantics/float.k:277` | rule | concrete, owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [owise, concrete]` |
| 596 | `semantics/float.k:281` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Float ::= roundExactFN(Float, Int) [function]` |
| 597 | `semantics/float.k:282` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule roundExactFN(F:Float, N:Int) => rheToFloat(rndHalfEven(rExNumer(F) *Int (10 ^Int N), rExDenom(F)), 10 ^Int N, F) [concrete]` |
| 598 | `semantics/float.k:287` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= rExK(Float) [function]` |
| 599 | `semantics/float.k:288` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rExK(F:Float) => 52 -Int exponentFloat(F) [concrete]` |
| 600 | `semantics/float.k:289` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= rExNumer(Float) [function]` |
| 601 | `semantics/float.k:290` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rExNumer(F:Float) => Float2Int(F *Float Int2Float(2 ^Int rExK(F), 53, 11)) [concrete]` |
| 602 | `semantics/float.k:291` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= rExDenom(Float) [function]` |
| 603 | `semantics/float.k:292` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rExDenom(F:Float) => 2 ^Int rExK(F) [concrete]` |
| 604 | `semantics/float.k:296` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= rndHalfEven(Int, Int) [function]` |
| 605 | `semantics/float.k:297` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rndHalfEven(A:Int, B:Int) => rndHE(A divInt B, A modInt B, B) [concrete]` |
| 606 | `semantics/float.k:298` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= rndHE(Int, Int, Int) [function]` |
| 607 | `semantics/float.k:299` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rndHE(Q:Int, R:Int, B:Int) => Q        requires 2 *Int R <Int B [concrete]` |
| 608 | `semantics/float.k:300` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rndHE(Q:Int, R:Int, B:Int) => Q +Int 1 requires 2 *Int R >Int B [concrete]` |
| 609 | `semantics/float.k:301` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rndHE(Q:Int, R:Int, B:Int) => Q        requires 2 *Int R ==Int B andBool Q modInt 2 ==Int 0 [concrete]` |
| 610 | `semantics/float.k:302` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rndHE(Q:Int, R:Int, B:Int) => Q +Int 1 requires 2 *Int R ==Int B andBool Q modInt 2 =/=Int 0 [concrete]` |
| 611 | `semantics/float.k:305` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Float ::= rheToFloat(Int, Int, Float) [function]` |
| 612 | `semantics/float.k:306` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rheToFloat(0, _:Int, F:Float) => #if signFloat(F) #then --Float 0.0 #else 0.0 #fi [concrete]` |
| 613 | `semantics/float.k:307` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule rheToFloat(Q:Int, SCALE:Int, _:Float) => Int2Float(Q, 53, 11) /Float Int2Float(SCALE, 53, 11) requires Q =/=Int 0 [concrete]` |
| 614 | `semantics/float.k:310` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)` |
| 615 | `semantics/float.k:311` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 616 | `semantics/float.k:313` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 617 | `semantics/float.k:314` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 618 | `semantics/float.k:315` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= "#mathSqrt"` |
| 619 | `semantics/float.k:316` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 620 | `semantics/float.k:317` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 621 | `semantics/float.k:318` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| 622 | `semantics/float.k:326` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 623 | `semantics/float.k:327` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 624 | `semantics/float.k:328` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 625 | `semantics/float.k:329` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 626 | `semantics/float.k:330` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 627 | `semantics/float.k:333` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 628 | `semantics/float.k:334` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 629 | `semantics/float.k:335` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 630 | `semantics/float.k:336` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 631 | `semantics/float.k:337` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 632 | `semantics/float.k:344` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #iterYield(V, R) ~> #maxContV(M) ... </k> requires isInt(V) orBool isBool(V)` |
| 633 | `semantics/float.k:347` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #iterYield(V, R) ~> #minContV(M) ... </k> requires isInt(V) orBool isBool(V)` |
| 634 | `semantics/float.k:355` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 635 | `semantics/float.k:356` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| 636 | `semantics/float.k:359` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 637 | `semantics/float.k:360` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 638 | `semantics/float.k:361` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| 639 | `semantics/float.k:364` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| 640 | `semantics/functions.k:8` | syntax | — | USED-PATH-SOUND | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall"` |
| 641 | `semantics/functions.k:14` | rule | — | USED-PATH-SOUND | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| 642 | `semantics/functions.k:18` | syntax | — | USED-PATH-SOUND | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 643 | `semantics/functions.k:19` | rule | — | USED-PATH-SOUND | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` |
| 644 | `semantics/functions.k:27` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| 645 | `semantics/functions.k:31` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 646 | `semantics/functions.k:33` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| 647 | `semantics/functions.k:36` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scope…` |
| 648 | `semantics/functions.k:42` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _)…` |
| 649 | `semantics/functions.k:47` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| 650 | `semantics/functions.k:50` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| 651 | `semantics/functions.k:53` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> s…` |
| 652 | `semantics/functions.k:59` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` |
| 653 | `semantics/functions.k:63` | rule | — | USED-PATH-SOUND | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 654 | `semantics/functions.k:64` | rule | — | USED-PATH-SOUND | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes>` |
| 655 | `semantics/functions.k:68` | rule | priority | USED-PATH-SOUND | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M…` |
| 656 | `semantics/functions.k:78` | rule | — | USED-PATH-SOUND | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| 657 | `semantics/functions.k:80` | rule | — | USED-PATH-SOUND | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` |
| 658 | `semantics/functions.k:85` | rule | — | USED-PATH-SOUND | `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef …` |
| 659 | `semantics/int.k:7` | rule | — | USED-PATH-SOUND | `rule applyUn("-", I:Int) => 0 -Int I` |
| 660 | `semantics/int.k:9` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2` |
| 661 | `semantics/int.k:11` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 662 | `semantics/int.k:12` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 663 | `semantics/int.k:16` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin(OP:String, B1:Bool, B2:Bool) => applyBin(OP, boolAsInt(B1), boolAsInt(B2)) requires isArithOp(OP)` |
| 664 | `semantics/int.k:18` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin(OP:String, B:Bool, I:Int)    => applyBin(OP, boolAsInt(B), I) requires isArithOp(OP) andBool OP =/=String "+"` |
| 665 | `semantics/int.k:20` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin(OP:String, I:Int, B:Bool)    => applyBin(OP, I, boolAsInt(B)) requires isArithOp(OP) andBool OP =/=String "+"` |
| 666 | `semantics/int.k:22` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2` |
| 667 | `semantics/int.k:23` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2` |
| 668 | `semantics/int.k:24` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)` |
| 669 | `semantics/int.k:25` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 670 | `semantics/int.k:26` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 671 | `semantics/int.k:28` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= pyMod(Int, Int) [function]` |
| 672 | `semantics/int.k:29` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 673 | `semantics/int.k:31` | rule | — | USED-PATH-SOUND | `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2` |
| 674 | `semantics/int.k:32` | rule | — | USED-PATH-SOUND | `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2` |
| 675 | `semantics/int.k:33` | rule | — | USED-PATH-SOUND | `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2` |
| 676 | `semantics/int.k:34` | rule | — | USED-PATH-SOUND | `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2` |
| 677 | `semantics/int.k:35` | rule | — | USED-PATH-SOUND | `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2` |
| 678 | `semantics/int.k:36` | rule | — | USED-PATH-SOUND | `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2` |
| 679 | `semantics/iter.k:8` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| 680 | `semantics/list.k:9` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>` |
| 681 | `semantics/list.k:10` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| 682 | `semantics/list.k:13` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ApplyK ::= "toList"` |
| 683 | `semantics/list.k:14` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 684 | `semantics/list.k:15` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| 685 | `semantics/list.k:18` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 686 | `semantics/list.k:19` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule valSeqConcat(.ValSeq, T:ValSeq)                => T` |
| 687 | `semantics/list.k:20` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| 688 | `semantics/list.k:24` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| 689 | `semantics/list.k:27` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 690 | `semantics/list.k:28` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| 691 | `semantics/list.k:33` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 692 | `semantics/list.k:34` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule hasRefVS(.ValSeq)                => false` |
| 693 | `semantics/list.k:35` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 694 | `semantics/list.k:37` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map)        [function]` |
| 695 | `semantics/list.k:39` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true` |
| 696 | `semantics/list.k:40` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false` |
| 697 | `semantics/list.k:41` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false` |
| 698 | `semantics/list.k:42` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| 699 | `semantics/list.k:45` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| 700 | `semantics/list.k:47` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| 701 | `semantics/list.k:49` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 702 | `semantics/list.k:50` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| 703 | `semantics/list.k:53` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` |
| 704 | `semantics/list.k:58` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 705 | `semantics/list.k:59` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 706 | `semantics/list.k:60` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 707 | `semantics/list.k:61` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 708 | `semantics/list.k:62` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 709 | `semantics/list.k:63` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| 710 | `semantics/list.k:65` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| 711 | `semantics/list.k:67` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| 712 | `semantics/methods.k:10` | syntax | function | USED-PATH-SOUND | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| 713 | `semantics/methods.k:13` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 714 | `semantics/methods.k:14` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 715 | `semantics/methods.k:15` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 716 | `semantics/methods.k:16` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| 717 | `semantics/methods.k:19` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))` |
| 718 | `semantics/methods.k:20` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))` |
| 719 | `semantics/methods.k:21` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| 720 | `semantics/methods.k:26` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 721 | `semantics/methods.k:27` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 722 | `semantics/methods.k:28` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 723 | `semantics/methods.k:29` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 724 | `semantics/methods.k:30` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` |
| 725 | `semantics/methods.k:34` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 726 | `semantics/methods.k:35` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 727 | `semantics/methods.k:36` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 728 | `semantics/methods.k:37` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| 729 | `semantics/methods.k:39` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| 730 | `semantics/methods.k:41` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 731 | `semantics/methods.k:42` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 732 | `semantics/methods.k:43` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 733 | `semantics/methods.k:44` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| 734 | `semantics/methods.k:47` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 735 | `semantics/methods.k:48` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 736 | `semantics/methods.k:49` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule trimWS(.IntSeq) => .IntSeq` |
| 737 | `semantics/methods.k:50` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 738 | `semantics/methods.k:51` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 739 | `semantics/methods.k:52` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 740 | `semantics/methods.k:53` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 741 | `semantics/methods.k:54` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 742 | `semantics/methods.k:55` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| 743 | `semantics/methods.k:58` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| 744 | `semantics/methods.k:61` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| 745 | `semantics/methods.k:64` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 746 | `semantics/methods.k:65` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 747 | `semantics/methods.k:66` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule cntOccVS(.ValSeq, _:Val)                => 0` |
| 748 | `semantics/methods.k:67` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 749 | `semantics/methods.k:68` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)` |
| 750 | `semantics/methods.k:72` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| 751 | `semantics/methods.k:75` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result` |
| 752 | `semantics/methods.k:76` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 753 | `semantics/methods.k:77` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| 754 | `semantics/methods.k:79` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` |
| 755 | `semantics/methods.k:82` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 756 | `semantics/methods.k:83` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC` |
| 757 | `semantics/methods.k:84` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 758 | `semantics/methods.k:85` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= isWSC(Int) [function, total]` |
| 759 | `semantics/methods.k:86` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| 760 | `semantics/methods.k:89` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` |
| 761 | `semantics/methods.k:94` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| 762 | `semantics/methods.k:97` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token` |
| 763 | `semantics/methods.k:98` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)` |
| 764 | `semantics/methods.k:99` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| 765 | `semantics/methods.k:101` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| 766 | `semantics/methods.k:104` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| 767 | `semantics/methods.k:106` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 768 | `semantics/methods.k:107` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq` |
| 769 | `semantics/methods.k:108` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 770 | `semantics/methods.k:109` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| 771 | `semantics/methods.k:112` | syntax | function, total | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 772 | `semantics/methods.k:113` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 773 | `semantics/methods.k:115` | syntax | function, total | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 774 | `semantics/methods.k:116` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 775 | `semantics/methods.k:118` | syntax | function, total | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 776 | `semantics/methods.k:119` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 777 | `semantics/methods.k:121` | syntax | function, total | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 778 | `semantics/methods.k:122` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 779 | `semantics/methods.k:124` | syntax | function, total | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 780 | `semantics/methods.k:125` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule hasUpper(.IntSeq) => false` |
| 781 | `semantics/methods.k:126` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 782 | `semantics/methods.k:128` | syntax | function, total | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 783 | `semantics/methods.k:129` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule hasLower(.IntSeq) => false` |
| 784 | `semantics/methods.k:130` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 785 | `semantics/methods.k:132` | syntax | function, total | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 786 | `semantics/methods.k:133` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule allAlpha(.IntSeq) => true` |
| 787 | `semantics/methods.k:134` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 788 | `semantics/methods.k:136` | syntax | function, total | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 789 | `semantics/methods.k:137` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule allDigit(.IntSeq) => true` |
| 790 | `semantics/methods.k:138` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 791 | `semantics/methods.k:140` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= lowerC(Int) [function, total]` |
| 792 | `semantics/methods.k:142` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 793 | `semantics/methods.k:143` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule lowerC(C:Int) => C         [owise]` |
| 794 | `semantics/methods.k:145` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= upperC(Int) [function, total]` |
| 795 | `semantics/methods.k:146` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 796 | `semantics/methods.k:147` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule upperC(C:Int) => C         [owise]` |
| 797 | `semantics/methods.k:149` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= swapC(Int) [function, total]` |
| 798 | `semantics/methods.k:150` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 799 | `semantics/methods.k:151` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 800 | `semantics/methods.k:152` | rule | owise | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule swapC(C:Int) => C         [owise]` |
| 801 | `semantics/methods.k:154` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 802 | `semantics/methods.k:155` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule mapLower(.IntSeq) => .IntSeq` |
| 803 | `semantics/methods.k:156` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 804 | `semantics/methods.k:158` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 805 | `semantics/methods.k:159` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule mapUpper(.IntSeq) => .IntSeq` |
| 806 | `semantics/methods.k:160` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 807 | `semantics/methods.k:162` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 808 | `semantics/methods.k:163` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule mapSwap(.IntSeq) => .IntSeq` |
| 809 | `semantics/methods.k:164` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 810 | `semantics/methods.k:166` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 811 | `semantics/methods.k:167` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule startsWith(.IntSeq, _:IntSeq)               => true` |
| 812 | `semantics/methods.k:168` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 813 | `semantics/methods.k:169` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| 814 | `semantics/operators.k:10` | rule | — | USED-PATH-SOUND | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 815 | `semantics/operators.k:12` | rule | — | USED-PATH-SOUND | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| 816 | `semantics/operators.k:15` | context | — | USED-PATH-SOUND | `context Compare(HOLE, _)` |
| 817 | `semantics/operators.k:16` | context | — | USED-PATH-SOUND | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 818 | `semantics/operators.k:17` | rule | owise | USED-PATH-SOUND | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 819 | `semantics/operators.k:19` | rule | — | USED-PATH-SOUND | `rule applyCmp("is",     V:Val, noneV) => V ==K noneV` |
| 820 | `semantics/operators.k:20` | rule | — | USED-PATH-SOUND | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| 821 | `semantics/operators.k:25` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 822 | `semantics/operators.k:28` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` |
| 823 | `semantics/operators.k:34` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| 824 | `semantics/operators.k:38` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [pri…` |
| 825 | `semantics/operators.k:44` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 826 | `semantics/range.k:9` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 827 | `semantics/range.k:10` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 828 | `semantics/range.k:12` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 829 | `semantics/range.k:13` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| 830 | `semantics/range.k:15` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| 831 | `semantics/range.k:17` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| 832 | `semantics/range.k:20` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| 833 | `semantics/range.k:23` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| 834 | `semantics/set.k:8` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= setV(IntSeq)` |
| 835 | `semantics/set.k:11` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 836 | `semantics/set.k:12` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule codeIn(_:Int, .IntSeq)                => false` |
| 837 | `semantics/set.k:13` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| 838 | `semantics/set.k:16` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] \| dedupFrom(IntSeq, IntSeq)  [function, total]` |
| 839 | `semantics/set.k:18` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 840 | `semantics/set.k:19` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 841 | `semantics/set.k:20` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| 842 | `semantics/set.k:22` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| 843 | `semantics/set.k:25` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 844 | `semantics/set.k:26` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)` |
| 845 | `semantics/set.k:27` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| 846 | `semantics/set.k:31` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 847 | `semantics/set.k:32` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule subsetCodes(.IntSeq, _:IntSeq)                => true` |
| 848 | `semantics/set.k:33` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 849 | `semantics/set.k:35` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 850 | `semantics/set.k:36` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| 851 | `semantics/set.k:39` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| 852 | `semantics/sort.k:18` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 853 | `semantics/sort.k:19` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 854 | `semantics/sort.k:20` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule sortVS(.ValSeq)                => .ValSeq          [concrete]` |
| 855 | `semantics/sort.k:21` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 856 | `semantics/sort.k:22` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]` |
| 857 | `semantics/sort.k:23` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 858 | `semantics/sort.k:24` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]` |
| 859 | `semantics/sort.k:32` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= insVSn(Val, ValSeq) [function]` |
| 860 | `semantics/sort.k:33` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule sortVS(vCons(X:Val, R:ValSeq)) => insVSn(X, sortVS(R)) requires isFloat(X) orBool isBool(X) [concrete]` |
| 861 | `semantics/sort.k:35` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVS(X:Int, vCons(Y:Val, R:ValSeq)) => vCons(X, vCons(Y, R)) requires (isFloat(Y) orBool isBool(Y)) andBool notBool applyCmp("<", Y, X) [concrete]` |
| 862 | `semantics/sort.k:37` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVS(X:Int, vCons(Y:Val, R:ValSeq)) => vCons(Y, insVS(X, R)) requires (isFloat(Y) orBool isBool(Y)) andBool applyCmp("<", Y, X) [concrete]` |
| 863 | `semantics/sort.k:39` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVSn(X:Val, .ValSeq) => vCons(X, .ValSeq) [concrete]` |
| 864 | `semantics/sort.k:40` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVSn(X:Val, vCons(Y:Val, R:ValSeq)) => vCons(X, vCons(Y, R)) requires notBool applyCmp("<", Y, X) [concrete]` |
| 865 | `semantics/sort.k:42` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVSn(X:Val, vCons(Y:Val, R:ValSeq)) => vCons(Y, insVSn(X, R)) requires applyCmp("<", Y, X) [concrete]` |
| 866 | `semantics/sort.k:45` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 867 | `semantics/sort.k:46` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 868 | `semantics/sort.k:47` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 869 | `semantics/sort.k:48` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| 870 | `semantics/sort.k:50` | rule | concrete | ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` |
| 871 | `semantics/sort.k:55` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` |
| 872 | `semantics/sort.k:59` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` |
| 873 | `semantics/sort.k:68` | syntax | function, total, opaque/no-evaluators, symbol | ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 874 | `semantics/sort.k:70` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| 875 | `semantics/sort.k:72` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 876 | `semantics/sort.k:73` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 877 | `semantics/sort.k:74` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 878 | `semantics/sort.k:76` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 879 | `semantics/sort.k:77` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule condRev(S:ValSeq, false) => S` |
| 880 | `semantics/sort.k:78` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule condRev(S:ValSeq, true)  => revVS(S)` |
| 881 | `semantics/sort.k:80` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| 882 | `semantics/sort.k:82` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| 883 | `semantics/sort.k:84` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` |
| 884 | `semantics/str.k:8` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>` |
| 885 | `semantics/str.k:9` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` |
| 886 | `semantics/str.k:13` | syntax | function | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `syntax IntSeq ::= strToCodes(String) [function]` |
| 887 | `semantics/str.k:14` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 888 | `semantics/str.k:15` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule strToCodes("") => .IntSeq` |
| 889 | `semantics/str.k:16` | rule | — | USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` |
| 890 | `semantics/str.k:20` | syntax | function, total | USED-PATH-SOUND | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 891 | `semantics/str.k:21` | rule | — | USED-PATH-SOUND | `rule seqConcat(.IntSeq, T:IntSeq)                => T` |
| 892 | `semantics/str.k:22` | rule | — | USED-PATH-SOUND | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 893 | `semantics/str.k:24` | rule | — | USED-PATH-SOUND | `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 894 | `semantics/str.k:25` | rule | — | USED-PATH-SOUND | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 895 | `semantics/str.k:26` | rule | — | USED-PATH-SOUND | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| 896 | `semantics/str.k:29` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 897 | `semantics/str.k:30` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 898 | `semantics/str.k:32` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 899 | `semantics/str.k:33` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strPrefix(.IntSeq, _:IntSeq)               => true` |
| 900 | `semantics/str.k:34` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 901 | `semantics/str.k:35` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 902 | `semantics/str.k:37` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 903 | `semantics/str.k:38` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)` |
| 904 | `semantics/str.k:39` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)` |
| 905 | `semantics/str.k:40` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` |
| 906 | `semantics/str.k:48` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 907 | `semantics/str.k:49` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strLt(.IntSeq, .IntSeq)                => false` |
| 908 | `semantics/str.k:50` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 909 | `semantics/str.k:51` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 910 | `semantics/str.k:52` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B` |
| 911 | `semantics/str.k:53` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B` |
| 912 | `semantics/str.k:54` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 913 | `semantics/str.k:56` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 914 | `semantics/str.k:57` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 915 | `semantics/str.k:58` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 916 | `semantics/str.k:59` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| 917 | `semantics/subscript.k:11` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 918 | `semantics/subscript.k:12` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V` |
| 919 | `semantics/subscript.k:13` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| 920 | `semantics/subscript.k:16` | syntax | function | USED-PATH-SOUND | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 921 | `semantics/subscript.k:17` | rule | — | USED-PATH-SOUND | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C` |
| 922 | `semantics/subscript.k:18` | rule | — | USED-PATH-SOUND | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| 923 | `semantics/subscript.k:21` | syntax | function, total | USED-PATH-SOUND | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 924 | `semantics/subscript.k:22` | rule | — | USED-PATH-SOUND | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 925 | `semantics/subscript.k:23` | rule | — | USED-PATH-SOUND | `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0` |
| 926 | `semantics/subscript.k:27` | context | — | USED-PATH-SOUND | `context Subscript(HOLE, _)` |
| 927 | `semantics/subscript.k:28` | context | — | USED-PATH-SOUND | `context Subscript(_:Val, HOLE:Expr)` |
| 928 | `semantics/subscript.k:31` | rule | priority | USED-PATH-SOUND | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 929 | `semantics/subscript.k:35` | rule | — | USED-PATH-SOUND | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 930 | `semantics/subscript.k:37` | syntax | function | USED-PATH-SOUND | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 931 | `semantics/subscript.k:38` | rule | — | USED-PATH-SOUND | `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 932 | `semantics/subscript.k:39` | rule | — | USED-PATH-SOUND | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 933 | `semantics/subscript.k:40` | rule | — | USED-PATH-SOUND | `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` |
| 934 | `semantics/subscript.k:44` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| 935 | `semantics/subscript.k:49` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax OptInt ::= "noB" \| someB(Int)` |
| 936 | `semantics/subscript.k:50` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #evalB(NoBound)  => noB ... </k>` |
| 937 | `semantics/subscript.k:51` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>` |
| 938 | `semantics/subscript.k:52` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 939 | `semantics/subscript.k:54` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 940 | `semantics/subscript.k:55` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 941 | `semantics/subscript.k:56` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| 942 | `semantics/subscript.k:58` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| 943 | `semantics/subscript.k:61` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 944 | `semantics/subscript.k:63` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 945 | `semantics/subscript.k:64` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 946 | `semantics/subscript.k:66` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 947 | `semantics/subscript.k:68` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` |
| 948 | `semantics/subscript.k:72` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= slStep(OptInt) [function, total]` |
| 949 | `semantics/subscript.k:73` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slStep(noB)          => 1` |
| 950 | `semantics/subscript.k:74` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slStep(someB(S:Int)) => S` |
| 951 | `semantics/subscript.k:76` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 952 | `semantics/subscript.k:77` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| 953 | `semantics/subscript.k:79` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0` |
| 954 | `semantics/subscript.k:81` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 955 | `semantics/subscript.k:83` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 956 | `semantics/subscript.k:84` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0` |
| 957 | `semantics/subscript.k:86` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| 958 | `semantics/subscript.k:88` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 959 | `semantics/subscript.k:90` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 960 | `semantics/subscript.k:91` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0` |
| 961 | `semantics/subscript.k:93` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| 962 | `semantics/subscript.k:96` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 963 | `semantics/subscript.k:97` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| 964 | `semantics/subscript.k:99` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| 965 | `semantics/subscript.k:102` | syntax | function, total | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 966 | `semantics/subscript.k:103` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN` |
| 967 | `semantics/subscript.k:105` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` |
| 968 | `semantics/subscript.k:109` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 969 | `semantics/subscript.k:110` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 970 | `semantics/subscript.k:113` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 971 | `semantics/subscript.k:116` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 972 | `semantics/subscript.k:117` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 973 | `semantics/subscript.k:120` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 974 | `semantics/syntax.k:9` | syntax | macro, strict, seqstrict | USED-PATH-SOUND | `syntax Expr ::= "Int"      "(" Int ")" \| "Float"    "(" Float ")" \| "Bool"     "(" Bool ")" \| "Name"     "(" String ")" \| "Str"      "(" String ")" \| "UnaryOp"  "(" String "," Expr ")" [strict(2)] \| "BinO…` |
| 975 | `semantics/syntax.k:32` | syntax | — | USED-PATH-SOUND | `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"` |
| 976 | `semantics/syntax.k:33` | syntax | — | USED-PATH-SOUND | `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"` |
| 977 | `semantics/syntax.k:34` | syntax | — | USED-PATH-SOUND | `syntax Entries  ::= List{Entry, ","}` |
| 978 | `semantics/syntax.k:35` | syntax | — | USED-PATH-SOUND | `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 979 | `semantics/syntax.k:36` | syntax | — | USED-PATH-SOUND | `syntax CompFors ::= List{CompFor, ""}` |
| 980 | `semantics/syntax.k:37` | syntax | — | USED-PATH-SOUND | `syntax Exprs    ::= List{Expr, ","}` |
| 981 | `semantics/syntax.k:38` | syntax | — | USED-PATH-SOUND | `syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 982 | `semantics/syntax.k:39` | syntax | — | USED-PATH-SOUND | `syntax Bound    ::= Expr \| "NoBound"` |
| 983 | `semantics/syntax.k:41` | syntax | strict | USED-PATH-SOUND | `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] \| "Import"    "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For"    …` |
| 984 | `semantics/syntax.k:56` | syntax | — | USED-PATH-SOUND | `syntax Stmts      ::= List{Stmt, ""}` |
| 985 | `semantics/syntax.k:57` | syntax | — | USED-PATH-SOUND | `syntax Params     ::= "Params" "(" ParamNames ")"` |
| 986 | `semantics/syntax.k:58` | syntax | — | USED-PATH-SOUND | `syntax CellVars   ::= "CellVars" "(" ParamNames ")"` |
| 987 | `semantics/syntax.k:59` | syntax | — | USED-PATH-SOUND | `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"` |
| 988 | `semantics/syntax.k:60` | syntax | — | USED-PATH-SOUND | `syntax ParamNames ::= List{String, ","}` |
| 989 | `semantics/syntax.k:61` | syntax | — | USED-PATH-SOUND | `syntax Module     ::= "Module" "(" Stmts ")"` |
| 990 | `semantics/tuple.k:10` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>` |
| 991 | `semantics/tuple.k:11` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| 992 | `semantics/tuple.k:14` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax ApplyK ::= "toTuple"` |
| 993 | `semantics/tuple.k:15` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 994 | `semantics/tuple.k:16` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 995 | `semantics/tuple.k:18` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| 996 | `semantics/tuple.k:20` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 997 | `semantics/tuple.k:21` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| 998 | `semantics/tuple.k:23` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 999 | `semantics/tuple.k:24` | syntax | function | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 1000 | `semantics/tuple.k:25` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 1001 | `semantics/tuple.k:26` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| 1002 | `semantics/tuple.k:28` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| 1003 | `semantics/tuple.k:31` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 1004 | `semantics/tuple.k:32` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 1005 | `semantics/tuple.k:35` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cel…` |
| 1006 | `semantics/tuple.k:42` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 1007 | `semantics/tuple.k:43` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 1008 | `semantics/tuple.k:44` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 1009 | `semantics/tuple.k:49` | syntax | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 1010 | `semantics/tuple.k:50` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 1011 | `semantics/tuple.k:51` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 1012 | `semantics/tuple.k:52` | rule | priority | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 1013 | `semantics/tuple.k:55` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| 1014 | `semantics/tuple.k:57` | rule | — | ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| 1015 | `verification.k:8` | syntax | function, total | PROOF-LOCAL-SOUND | `syntax Bool ::= standaloneLastLetter(IntSeq) [function, total]` |
| 1016 | `verification.k:10` | rule | — | PROOF-LOCAL-SOUND | `rule standaloneLastLetter(IS:IntSeq) => false requires isLen(IS) ==Int 0` |
| 1017 | `verification.k:13` | rule | — | PROOF-LOCAL-SOUND | `rule standaloneLastLetter(IS:IntSeq) => false requires isLen(IS) >Int 0 andBool notBool isAlphaC(intSeqAt(IS, isLen(IS) -Int 1))` |
| 1018 | `verification.k:17` | rule | — | PROOF-LOCAL-SOUND | `rule standaloneLastLetter(IS:IntSeq) => true requires isLen(IS) ==Int 1 andBool isAlphaC(intSeqAt(IS, 0))` |
| 1019 | `verification.k:21` | rule | — | PROOF-LOCAL-SOUND | `rule standaloneLastLetter(IS:IntSeq) => intSeqAt(IS, isLen(IS) -Int 2) ==Int 32 requires isLen(IS) >Int 1 andBool isAlphaC(intSeqAt(IS, isLen(IS) -Int 1))` |
| 1020 | `verification.k:28` | rule | simplification | PROOF-LOCAL-SOUND | `rule iCons(_C:Int, _REST:IntSeq) ==K .IntSeq => false [simplification]` |
| 1021 | `verification.k:33` | rule | simplification | PROOF-LOCAL-SOUND | `rule iCons(C:Int, .IntSeq) ==K iCons(D:Int, .IntSeq) => C ==Int D [simplification]` |

## Counts

- kind `configuration`: 1
- kind `context`: 5
- kind `rule`: 770
- kind `syntax`: 245
- decision `ACCEPTED-FIXED-CONCRETE-MODEL; UNUSED`: 59
- decision `ACCEPTED-FIXED-OPAQUE-BOUNDARY; UNUSED`: 24
- decision `ACCEPTED-FIXED-SUBSET; UNUSED/NO USED-TERM MATCH`: 737
- decision `PROOF-LOCAL-SOUND`: 7
- decision `USED-PATH-SOUND`: 166
- decision `USED-SOUND-FOR-ASCII-MODEL; UNICODE-GAP`: 28

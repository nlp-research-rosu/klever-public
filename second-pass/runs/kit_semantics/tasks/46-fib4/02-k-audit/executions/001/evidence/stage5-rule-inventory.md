# Stage 5 exhaustive local K inventory

Files inventoried: 26
Items inventoried: 936
By kind: {'claim': 2, 'configuration': 1, 'context': 5, 'rule': 700, 'syntax': 228}
By decision: {'CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF': 21, 'DERIVED_CIRCULARITY_REVIEWED_SOUND': 1, 'PROOF_LOCAL_REVIEWED_SOUND': 6, 'REACHED_FIXED_ITEM_REVIEWED_SOUND': 114, 'TARGET_CLAIM_REVIEWED_SOUND': 1, 'UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS': 793}
Attribute-bearing item counts: {'concrete': 35, 'function': 147, 'macro': 4, 'macro-rec': 1, 'no-evaluators': 22, 'owise': 26, 'priority': 45, 'seqstrict': 1, 'strict': 2, 'symbol': 25, 'total': 108}
Interpretation: `UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS` means the item was inspected but no constructor/operator in the submitted program or proof path can match it. It is not a proof-local assumption.

| ID | Kind | Attributes | Reachability/soundness decision | Declaration or rule |
|---|---|---|---|---|
| `reference-semantics/semantics/assert.k:6` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| `reference-semantics/semantics/assert.k:8` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| `reference-semantics/semantics/assert.k:13` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/bool.k:8` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| `reference-semantics/semantics/bool.k:10` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| `reference-semantics/semantics/bool.k:11` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| `reference-semantics/semantics/bool.k:16` | context | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| `reference-semantics/semantics/bool.k:17` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| `reference-semantics/semantics/bool.k:18` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| `reference-semantics/semantics/bool.k:20` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| `reference-semantics/semantics/bool.k:22` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| `reference-semantics/semantics/bool.k:24` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` |
| `reference-semantics/semantics/bool.k:29` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| `reference-semantics/semantics/bool.k:31` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| `reference-semantics/semantics/bool.k:35` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| `reference-semantics/semantics/bool.k:39` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| `reference-semantics/semantics/bool.k:43` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| `reference-semantics/semantics/builtins.k:17` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| `reference-semantics/semantics/builtins.k:20` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= seqLen(Val) [function]` |
| `reference-semantics/semantics/builtins.k:21` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| `reference-semantics/semantics/builtins.k:22` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)` |
| `reference-semantics/semantics/builtins.k:23` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)` |
| `reference-semantics/semantics/builtins.k:24` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule seqLen(str(IS:IntSeq))                   => isLen(IS)` |
| `reference-semantics/semantics/builtins.k:25` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)` |
| `reference-semantics/semantics/builtins.k:26` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| `reference-semantics/semantics/builtins.k:32` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>` |
| `reference-semantics/semantics/builtins.k:33` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| `reference-semantics/semantics/builtins.k:34` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>` |
| `reference-semantics/semantics/builtins.k:35` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>` |
| `reference-semantics/semantics/builtins.k:36` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| `reference-semantics/semantics/builtins.k:37` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule charsOf(.IntSeq)                => .ValSeq` |
| `reference-semantics/semantics/builtins.k:38` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| `reference-semantics/semantics/builtins.k:41` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| `reference-semantics/semantics/builtins.k:44` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| `reference-semantics/semantics/builtins.k:47` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| `reference-semantics/semantics/builtins.k:48` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| `reference-semantics/semantics/builtins.k:49` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| `reference-semantics/semantics/builtins.k:50` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| `reference-semantics/semantics/builtins.k:54` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= intOf(Val) [function]` |
| `reference-semantics/semantics/builtins.k:55` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intOf(I:Int)  => I` |
| `reference-semantics/semantics/builtins.k:56` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| `reference-semantics/semantics/builtins.k:59` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| `reference-semantics/semantics/builtins.k:60` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| `reference-semantics/semantics/builtins.k:61` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| `reference-semantics/semantics/builtins.k:62` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| `reference-semantics/semantics/builtins.k:64` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| `reference-semantics/semantics/builtins.k:67` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| `reference-semantics/semantics/builtins.k:68` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| `reference-semantics/semantics/builtins.k:69` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| `reference-semantics/semantics/builtins.k:70` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| `reference-semantics/semantics/builtins.k:72` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` |
| `reference-semantics/semantics/builtins.k:76` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| `reference-semantics/semantics/builtins.k:77` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| `reference-semantics/semantics/builtins.k:78` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| `reference-semantics/semantics/builtins.k:80` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| `reference-semantics/semantics/builtins.k:81` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| `reference-semantics/semantics/builtins.k:82` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| `reference-semantics/semantics/builtins.k:86` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| `reference-semantics/semantics/builtins.k:87` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| `reference-semantics/semantics/builtins.k:88` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| `reference-semantics/semantics/builtins.k:90` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| `reference-semantics/semantics/builtins.k:91` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| `reference-semantics/semantics/builtins.k:92` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| `reference-semantics/semantics/builtins.k:97` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= maxVals(Int, Vals) [function]` |
| `reference-semantics/semantics/builtins.k:98` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| `reference-semantics/semantics/builtins.k:99` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule maxVals(M:Int, .Vals)           => M` |
| `reference-semantics/semantics/builtins.k:100` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| `reference-semantics/semantics/builtins.k:102` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= minVals(Int, Vals) [function]` |
| `reference-semantics/semantics/builtins.k:103` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| `reference-semantics/semantics/builtins.k:104` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule minVals(M:Int, .Vals)           => M` |
| `reference-semantics/semantics/builtins.k:105` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| `reference-semantics/semantics/builtins.k:108` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` |
| `reference-semantics/semantics/builtins.k:111` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| `reference-semantics/semantics/builtins.k:114` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| `reference-semantics/semantics/builtins.k:115` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule binCodes(0) => iCons(48, .IntSeq)` |
| `reference-semantics/semantics/builtins.k:116` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| `reference-semantics/semantics/builtins.k:117` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| `reference-semantics/semantics/builtins.k:118` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule binAcc(0, ACC:IntSeq) => ACC` |
| `reference-semantics/semantics/builtins.k:119` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` |
| `reference-semantics/semantics/builtins.k:124` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| `reference-semantics/semantics/builtins.k:126` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| `reference-semantics/semantics/builtins.k:127` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| `reference-semantics/semantics/builtins.k:128` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` |
| `reference-semantics/semantics/builtins.k:132` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| `reference-semantics/semantics/builtins.k:134` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| `reference-semantics/semantics/builtins.k:135` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mapStrVS(.ValSeq) => .ValSeq` |
| `reference-semantics/semantics/builtins.k:136` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| `reference-semantics/semantics/builtins.k:137` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| `reference-semantics/semantics/builtins.k:140` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| `reference-semantics/semantics/builtins.k:143` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| `reference-semantics/semantics/builtins.k:144` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` |
| `reference-semantics/semantics/builtins.k:148` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))` |
| `reference-semantics/semantics/builtins.k:149` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| `reference-semantics/semantics/builtins.k:152` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` |
| `reference-semantics/semantics/builtins.k:156` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| `reference-semantics/semantics/builtins.k:158` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| `reference-semantics/semantics/builtins.k:159` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intDigAcc(.IntSeq, ACC:Int)             => ACC` |
| `reference-semantics/semantics/builtins.k:160` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| `reference-semantics/semantics/builtins.k:163` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| `reference-semantics/semantics/builtins.k:164` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)` |
| `reference-semantics/semantics/builtins.k:167` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| `reference-semantics/semantics/builtins.k:169` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>` |
| `reference-semantics/semantics/builtins.k:170` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| `reference-semantics/semantics/builtins.k:171` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| `reference-semantics/semantics/builtins.k:173` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>` |
| `reference-semantics/semantics/builtins.k:174` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| `reference-semantics/semantics/builtins.k:177` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)` |
| `reference-semantics/semantics/builtins.k:178` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)` |
| `reference-semantics/semantics/builtins.k:179` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` |
| `reference-semantics/semantics/builtins.k:187` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| `reference-semantics/semantics/builtins.k:188` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= evalArith(IntSeq) [function]` |
| `reference-semantics/semantics/builtins.k:189` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| `reference-semantics/semantics/builtins.k:192` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| `reference-semantics/semantics/builtins.k:194` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= evDigit(Int) [function, total]` |
| `reference-semantics/semantics/builtins.k:195` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `reference-semantics/semantics/builtins.k:196` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| `reference-semantics/semantics/builtins.k:197` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| `reference-semantics/semantics/builtins.k:198` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule evHead42(_:IntSeq)            => false [owise]` |
| `reference-semantics/semantics/builtins.k:199` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| `reference-semantics/semantics/builtins.k:200` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| `reference-semantics/semantics/builtins.k:201` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule evHead47(_:IntSeq)            => false [owise]` |
| `reference-semantics/semantics/builtins.k:203` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| `reference-semantics/semantics/builtins.k:204` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokOps(.IntSeq)                 => .OpSeq` |
| `reference-semantics/semantics/builtins.k:205` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)` |
| `reference-semantics/semantics/builtins.k:206` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)` |
| `reference-semantics/semantics/builtins.k:207` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| `reference-semantics/semantics/builtins.k:208` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| `reference-semantics/semantics/builtins.k:209` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| `reference-semantics/semantics/builtins.k:210` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| `reference-semantics/semantics/builtins.k:211` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))` |
| `reference-semantics/semantics/builtins.k:212` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))` |
| `reference-semantics/semantics/builtins.k:214` | syntax | `function, total;function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| `reference-semantics/semantics/builtins.k:216` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokNds(.IntSeq)                => .IntSeq` |
| `reference-semantics/semantics/builtins.k:217` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)` |
| `reference-semantics/semantics/builtins.k:218` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| `reference-semantics/semantics/builtins.k:219` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| `reference-semantics/semantics/builtins.k:221` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| `reference-semantics/semantics/builtins.k:223` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| `reference-semantics/semantics/builtins.k:225` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| `reference-semantics/semantics/builtins.k:226` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| `reference-semantics/semantics/builtins.k:227` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| `reference-semantics/semantics/builtins.k:228` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule firstNdE(_:EvPair) => 0 [owise]` |
| `reference-semantics/semantics/builtins.k:230` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| `reference-semantics/semantics/builtins.k:231` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyOpE("+",  A:Int, B:Int) => A +Int B` |
| `reference-semantics/semantics/builtins.k:232` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyOpE("-",  A:Int, B:Int) => A -Int B` |
| `reference-semantics/semantics/builtins.k:233` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyOpE("*",  A:Int, B:Int) => A *Int B` |
| `reference-semantics/semantics/builtins.k:234` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| `reference-semantics/semantics/builtins.k:235` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| `reference-semantics/semantics/builtins.k:236` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| `reference-semantics/semantics/builtins.k:238` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/builtins.k:239` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| `reference-semantics/semantics/builtins.k:240` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| `reference-semantics/semantics/builtins.k:241` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| `reference-semantics/semantics/builtins.k:243` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| `reference-semantics/semantics/builtins.k:244` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| `reference-semantics/semantics/builtins.k:245` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| `reference-semantics/semantics/builtins.k:246` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| `reference-semantics/semantics/builtins.k:247` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| `reference-semantics/semantics/builtins.k:248` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| `reference-semantics/semantics/builtins.k:250` | syntax | `function, total;function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| `reference-semantics/semantics/builtins.k:251` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `reference-semantics/semantics/builtins.k:252` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `reference-semantics/semantics/builtins.k:253` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `reference-semantics/semantics/builtins.k:254` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `reference-semantics/semantics/builtins.k:255` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/builtins.k:256` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| `reference-semantics/semantics/builtins.k:257` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| `reference-semantics/semantics/builtins.k:260` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| `reference-semantics/semantics/builtins.k:263` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| `reference-semantics/semantics/builtins.k:265` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| `reference-semantics/semantics/builtins.k:266` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| `reference-semantics/semantics/builtins.k:267` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| `reference-semantics/semantics/builtins.k:268` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule inLevelE(_:String, _:String) => false [owise]` |
| `reference-semantics/semantics/builtins.k:269` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| `reference-semantics/semantics/builtins.k:270` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| `reference-semantics/semantics/builtins.k:271` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| `reference-semantics/semantics/builtins.k:272` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| `reference-semantics/semantics/builtins.k:273` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| `reference-semantics/semantics/builtins.k:274` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| `reference-semantics/semantics/builtins.k:279` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= "#md5"` |
| `reference-semantics/semantics/builtins.k:280` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| `reference-semantics/semantics/builtins.k:282` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| `reference-semantics/semantics/builtins.k:283` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= md5Obj(IntSeq)` |
| `reference-semantics/semantics/builtins.k:284` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| `reference-semantics/semantics/builtins.k:285` | syntax | `function, total, symbol(md5hexCodes), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| `reference-semantics/semantics/builtins.k:291` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| `reference-semantics/semantics/builtins.k:292` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| `reference-semantics/semantics/builtins.k:293` | syntax | `function;function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| `reference-semantics/semantics/builtins.k:294` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isIntV(_:Int)         => true` |
| `reference-semantics/semantics/builtins.k:295` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isIntV(_:Val)         => false [owise]` |
| `reference-semantics/semantics/builtins.k:296` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isStrV(str(_:IntSeq)) => true` |
| `reference-semantics/semantics/builtins.k:297` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isStrV(_:Val)         => false [owise]` |
| `reference-semantics/semantics/call.k:16` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| `reference-semantics/semantics/call.k:19` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax KItem ::= #callee(Exprs)` |
| `reference-semantics/semantics/call.k:20` | rule | `owise` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| `reference-semantics/semantics/call.k:21` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| `reference-semantics/semantics/call.k:24` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| `reference-semantics/semantics/call.k:26` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| `reference-semantics/semantics/call.k:27` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>` |
| `reference-semantics/semantics/call.k:28` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>` |
| `reference-semantics/semantics/call.k:29` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>` |
| `reference-semantics/semantics/call.k:30` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>` |
| `reference-semantics/semantics/call.k:31` | rule | `owise` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| `reference-semantics/semantics/call.k:32` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>` |
| `reference-semantics/semantics/call.k:38` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/call.k:42` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| `reference-semantics/semantics/call.k:47` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/call.k:52` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isMutMethod(String) [function, total]` |
| `reference-semantics/semantics/call.k:53` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| `reference-semantics/semantics/call.k:56` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` |
| `reference-semantics/semantics/call.k:63` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| `reference-semantics/semantics/call.k:69` | rule | ` NEWL <- scope(.Map, parent(DEFL)) ` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| `reference-semantics/semantics/call.k:80` | rule | ` NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| `reference-semantics/semantics/call.k:87` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #allocCells(ParamNames)` |
| `reference-semantics/semantics/call.k:88` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| `reference-semantics/semantics/call.k:89` | rule | ` CV <- cellRef(N) ` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| `reference-semantics/semantics/comprehension.k:11` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `reference-semantics/semantics/comprehension.k:12` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `reference-semantics/semantics/comprehension.k:14` | syntax | `macro` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| `reference-semantics/semantics/comprehension.k:15` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| `reference-semantics/semantics/comprehension.k:18` | syntax | `macro-rec` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| `reference-semantics/semantics/comprehension.k:19` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| `reference-semantics/semantics/comprehension.k:21` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| `reference-semantics/semantics/comprehension.k:24` | syntax | `macro` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Expr ::= compGuard(Exprs) [macro]` |
| `reference-semantics/semantics/comprehension.k:25` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule compGuard(.Exprs)             => Bool(true)` |
| `reference-semantics/semantics/comprehension.k:26` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| `reference-semantics/semantics/concrete.k:13` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| `reference-semantics/semantics/concrete.k:16` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| `reference-semantics/semantics/concrete.k:25` | syntax | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `syntax Val ::= kvP(Val, Val)` |
| `reference-semantics/semantics/concrete.k:26` | syntax | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| `reference-semantics/semantics/concrete.k:28` | rule | `priority(40)` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| `reference-semantics/semantics/concrete.k:31` | rule | `priority(40)` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| `reference-semantics/semantics/concrete.k:34` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| `reference-semantics/semantics/concrete.k:36` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| `reference-semantics/semantics/concrete.k:38` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| `reference-semantics/semantics/concrete.k:42` | syntax | `function` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| `reference-semantics/semantics/concrete.k:43` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| `reference-semantics/semantics/concrete.k:44` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| `reference-semantics/semantics/concrete.k:47` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| `reference-semantics/semantics/concrete.k:51` | syntax | `function` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `syntax Bool ::= kLt(Val, Val) [function]` |
| `reference-semantics/semantics/concrete.k:52` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule kLt(I1:Int, I2:Int)             => I1 <Int I2` |
| `reference-semantics/semantics/concrete.k:53` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule kLt(F1:Float, F2:Float)         => F1 <Float F2` |
| `reference-semantics/semantics/concrete.k:54` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `reference-semantics/semantics/concrete.k:56` | syntax | `function, total` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| `reference-semantics/semantics/concrete.k:57` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule unpairVS(.ValSeq) => .ValSeq` |
| `reference-semantics/semantics/concrete.k:58` | rule | `-` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| `reference-semantics/semantics/concrete.k:59` | rule | `owise` | CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| `reference-semantics/semantics/controls.k:9` | rule | ` X <- V ` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| `reference-semantics/semantics/controls.k:12` | rule | `X;"$cells";X;priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| `reference-semantics/semantics/controls.k:20` | rule | ` X <- applyBin(OP, {M[X` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` |
| `reference-semantics/semantics/controls.k:27` | rule | `X;priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]` |
| `reference-semantics/semantics/controls.k:35` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| `reference-semantics/semantics/controls.k:36` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| `reference-semantics/semantics/controls.k:37` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #bindImports(ParamNames)` |
| `reference-semantics/semantics/controls.k:38` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| `reference-semantics/semantics/controls.k:39` | rule | ` N <- builtinV(N) ` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| `reference-semantics/semantics/controls.k:43` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` |
| `reference-semantics/semantics/controls.k:48` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Expr(_:Val) => .K ... </k>` |
| `reference-semantics/semantics/controls.k:51` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| `reference-semantics/semantics/controls.k:52` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| `reference-semantics/semantics/controls.k:53` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>` |
| `reference-semantics/semantics/controls.k:54` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| `reference-semantics/semantics/controls.k:57` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| `reference-semantics/semantics/controls.k:59` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` |
| `reference-semantics/semantics/controls.k:65` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| `reference-semantics/semantics/controls.k:69` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| `reference-semantics/semantics/controls.k:71` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| `reference-semantics/semantics/controls.k:72` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| `reference-semantics/semantics/controls.k:73` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` |
| `reference-semantics/semantics/controls.k:77` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| `reference-semantics/semantics/controls.k:78` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| `reference-semantics/semantics/controls.k:79` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| `reference-semantics/semantics/controls.k:81` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` |
| `reference-semantics/semantics/controls.k:85` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `reference-semantics/semantics/controls.k:86` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Continue => #cont ... </k>` |
| `reference-semantics/semantics/controls.k:87` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Break => #brk ... </k>` |
| `reference-semantics/semantics/controls.k:88` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `reference-semantics/semantics/controls.k:89` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| `reference-semantics/semantics/controls.k:90` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| `reference-semantics/semantics/controls.k:91` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| `reference-semantics/semantics/controls.k:95` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/controls.k:98` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/controls.k:101` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/controls.k:106` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/core.k:13` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| `reference-semantics/semantics/core.k:14` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| `reference-semantics/semantics/core.k:15` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Str    ::= str(IntSeq)` |
| `reference-semantics/semantics/core.k:18` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| `reference-semantics/semantics/core.k:25` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Val      ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int)          // a heap object: <heap> holds its list(VS) \| cellRef(Int)      // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String)     // a type object (int/str), resolved from the builtins frame \| builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String)   // a cooled Attribute: obj.method` |
| `reference-semantics/semantics/core.k:36` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Parent   ::= "root" \| parent(Int)` |
| `reference-semantics/semantics/core.k:37` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Scope    ::= scope(Map, Parent)` |
| `reference-semantics/semantics/core.k:38` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax KResult  ::= Val` |
| `reference-semantics/semantics/core.k:39` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Expr     ::= Val   // cooling puts results back into expression holes` |
| `reference-semantics/semantics/core.k:40` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Vals     ::= List{Val, ","}` |
| `reference-semantics/semantics/core.k:41` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Exc      ::= "NoExc" \| "AssertionError"` |
| `reference-semantics/semantics/core.k:42` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax RetState ::= "noRet" \| retV(Val)` |
| `reference-semantics/semantics/core.k:49` | configuration | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     \|-> scope(.Map, parent(-1)) -1    \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code>` |
| `reference-semantics/semantics/core.k:68` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isRefV(Val) [function, total]` |
| `reference-semantics/semantics/core.k:69` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isRefV(ref(_:Int)) => true` |
| `reference-semantics/semantics/core.k:70` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isRefV(_:Val)      => false [owise]` |
| `reference-semantics/semantics/core.k:75` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax HeapVal ::= cellV(Val)` |
| `reference-semantics/semantics/core.k:76` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isCellRef(Val) [function, total]` |
| `reference-semantics/semantics/core.k:77` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isCellRef(cellRef(_:Int)) => true` |
| `reference-semantics/semantics/core.k:78` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isCellRef(_:Val)          => false [owise]` |
| `reference-semantics/semantics/core.k:85` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` |
| `reference-semantics/semantics/core.k:95` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= kwV(String, Val)` |
| `reference-semantics/semantics/core.k:96` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #kwTag(String)` |
| `reference-semantics/semantics/core.k:97` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| `reference-semantics/semantics/core.k:98` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| `reference-semantics/semantics/core.k:100` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isKwV(Val) [function, total]` |
| `reference-semantics/semantics/core.k:101` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isKwV(kwV(_:String, _:Val)) => true` |
| `reference-semantics/semantics/core.k:102` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isKwV(_:Val)                => false [owise]` |
| `reference-semantics/semantics/core.k:106` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= cellsMark(ParamNames)` |
| `reference-semantics/semantics/core.k:107` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ParamNames ::= cellsOf(Val) [function]` |
| `reference-semantics/semantics/core.k:108` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| `reference-semantics/semantics/core.k:109` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| `reference-semantics/semantics/core.k:110` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule pnMember(_:String, .ParamNames) => false` |
| `reference-semantics/semantics/core.k:111` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| `reference-semantics/semantics/core.k:113` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #cellW(Val, Val)` |
| `reference-semantics/semantics/core.k:114` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| `reference-semantics/semantics/core.k:117` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #alloc(Val)` |
| `reference-semantics/semantics/core.k:118` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| `reference-semantics/semantics/core.k:124` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax KItem ::= #loadAll(Module)` |
| `reference-semantics/semantics/core.k:125` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| `reference-semantics/semantics/core.k:126` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| `reference-semantics/semantics/core.k:127` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> .Stmts => .K ... </k>` |
| `reference-semantics/semantics/core.k:130` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax KItem ::= #look(String, Int)` |
| `reference-semantics/semantics/core.k:131` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| `reference-semantics/semantics/core.k:132` | rule | `X` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` |
| `reference-semantics/semantics/core.k:145` | rule | `"$cells";X;priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| `reference-semantics/semantics/core.k:152` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` |
| `reference-semantics/semantics/core.k:157` | syntax | `function, total` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Scope ::= "builtinsScope" [function, total]` |
| `reference-semantics/semantics/core.k:158` | rule | ` "len"    <- builtinV("len")    ; "set"    <- builtinV("set")    ; "sum"    <- builtinV("sum")    ; "abs"    <- builtinV("abs")    ; "min"    <- builtinV("min")    ; "max"    <- builtinV("max")    ; "ord"    <- builtinV("ord")    ; "chr"    <- builtinV("chr")    ; "range"  <- builtinV("range")  ; "all"    <- builtinV("all")    ; "any"    <- builtinV("any")    ; "zip"    <- builtinV("zip")    ; "isinstance" <- builtinV("isinstance") ; "sorted" <- builtinV("sorted") ; "list"   <- builtinV("list")   ; "round"  <- builtinV("round")  ; "bin"    <- builtinV("bin")    ; "enumerate" <- builtinV("enumerate") ; "map"    <- builtinV("map")    ; "eval"   <- builtinV("eval")   ; "int"    <- typeV("int")       ; "str"    <- typeV("str")       ; "float"  <- typeV("float")     ` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root)` |
| `reference-semantics/semantics/core.k:185` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ApplyK ::= toCall(Val)` |
| `reference-semantics/semantics/core.k:186` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| `reference-semantics/semantics/core.k:189` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| `reference-semantics/semantics/core.k:190` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| `reference-semantics/semantics/core.k:191` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| `reference-semantics/semantics/core.k:194` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Int(I:Int)   => I ... </k>` |
| `reference-semantics/semantics/core.k:195` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Bool(B:Bool) => B ... </k>` |
| `reference-semantics/semantics/core.k:196` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> NoneVal      => noneV ... </k>` |
| `reference-semantics/semantics/core.k:199` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= truthy(Val) [function]` |
| `reference-semantics/semantics/core.k:200` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule truthy(B:Bool)          => B` |
| `reference-semantics/semantics/core.k:201` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule truthy(noneV)           => false` |
| `reference-semantics/semantics/core.k:202` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule truthy(I:Int)           => I =/=Int 0` |
| `reference-semantics/semantics/core.k:203` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)` |
| `reference-semantics/semantics/core.k:204` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)` |
| `reference-semantics/semantics/core.k:205` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| `reference-semantics/semantics/core.k:208` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val  ::= applyUn(String, Val) [function]` |
| `reference-semantics/semantics/core.k:209` | syntax | `function` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Val  ::= applyBin(String, Val, Val) [function]` |
| `reference-semantics/semantics/core.k:210` | syntax | `function` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| `reference-semantics/semantics/core.k:213` | syntax | `function, total` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| `reference-semantics/semantics/core.k:214` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule appendVal(.Vals, V:Val)              => V , .Vals` |
| `reference-semantics/semantics/core.k:215` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)` |
| `reference-semantics/semantics/core.k:217` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| `reference-semantics/semantics/core.k:218` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule vals2valSeq(.Vals)            => .ValSeq` |
| `reference-semantics/semantics/core.k:219` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| `reference-semantics/semantics/core.k:223` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| `reference-semantics/semantics/core.k:224` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule vsLen(.ValSeq)                => 0` |
| `reference-semantics/semantics/core.k:225` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| `reference-semantics/semantics/core.k:227` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= isLen(IntSeq) [function, total]` |
| `reference-semantics/semantics/core.k:228` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isLen(.IntSeq)                => 0` |
| `reference-semantics/semantics/core.k:229` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| `reference-semantics/semantics/core.k:233` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| `reference-semantics/semantics/core.k:234` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq` |
| `reference-semantics/semantics/core.k:235` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)` |
| `reference-semantics/semantics/core.k:236` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| `reference-semantics/semantics/core.k:238` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0` |
| `reference-semantics/semantics/dict.k:20` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| `reference-semantics/semantics/dict.k:23` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| `reference-semantics/semantics/dict.k:26` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| `reference-semantics/semantics/dict.k:27` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| `reference-semantics/semantics/dict.k:28` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| `reference-semantics/semantics/dict.k:30` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| `reference-semantics/semantics/dict.k:32` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` |
| `reference-semantics/semantics/dict.k:37` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| `reference-semantics/semantics/dict.k:38` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dHasKey(.ValSeq, _:Val)                => false` |
| `reference-semantics/semantics/dict.k:39` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K` |
| `reference-semantics/semantics/dict.k:40` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| `reference-semantics/semantics/dict.k:43` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| `reference-semantics/semantics/dict.k:44` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)` |
| `reference-semantics/semantics/dict.k:45` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| `reference-semantics/semantics/dict.k:49` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| `reference-semantics/semantics/dict.k:50` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K` |
| `reference-semantics/semantics/dict.k:52` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| `reference-semantics/semantics/dict.k:54` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| `reference-semantics/semantics/dict.k:58` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` |
| `reference-semantics/semantics/dict.k:63` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| `reference-semantics/semantics/dict.k:64` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| `reference-semantics/semantics/dict.k:65` | rule | `priority(45)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` |
| `reference-semantics/semantics/dict.k:70` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| `reference-semantics/semantics/dict.k:71` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| `reference-semantics/semantics/dict.k:76` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #dsetK(String, Val)` |
| `reference-semantics/semantics/dict.k:77` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| `reference-semantics/semantics/dict.k:78` | rule | ` X <- dictSet({M[X;X` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| `reference-semantics/semantics/dict.k:82` | rule | `X;X` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| `reference-semantics/semantics/dict.k:86` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| `reference-semantics/semantics/dict.k:87` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` |
| `reference-semantics/semantics/dict.k:90` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| `reference-semantics/semantics/dict.k:91` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| `reference-semantics/semantics/dict.k:92` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0` |
| `reference-semantics/semantics/dict.k:95` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| `reference-semantics/semantics/dict.k:97` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| `reference-semantics/semantics/dict.k:98` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| `reference-semantics/semantics/dict.k:99` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| `reference-semantics/semantics/dict.k:101` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| `reference-semantics/semantics/dict.k:102` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K` |
| `reference-semantics/semantics/dict.k:103` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| `reference-semantics/semantics/float.k:20` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= Float` |
| `reference-semantics/semantics/float.k:21` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Float(F:Float) => F ... </k>` |
| `reference-semantics/semantics/float.k:24` | syntax | `function, total, symbol(intFloatDiv), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| `reference-semantics/semantics/float.k:25` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| `reference-semantics/semantics/float.k:27` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| `reference-semantics/semantics/float.k:30` | syntax | `function, total, symbol(divII), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| `reference-semantics/semantics/float.k:31` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| `reference-semantics/semantics/float.k:32` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| `reference-semantics/semantics/float.k:37` | syntax | `function, total, symbol(floatMod), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| `reference-semantics/semantics/float.k:38` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| `reference-semantics/semantics/float.k:39` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| `reference-semantics/semantics/float.k:43` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| `reference-semantics/semantics/float.k:44` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| `reference-semantics/semantics/float.k:50` | syntax | `function, total, symbol(floatLt), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| `reference-semantics/semantics/float.k:51` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| `reference-semantics/semantics/float.k:52` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| `reference-semantics/semantics/float.k:54` | syntax | `function, total, symbol(absF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| `reference-semantics/semantics/float.k:55` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule absF(F:Float) => absFloat(F) [concrete]` |
| `reference-semantics/semantics/float.k:56` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| `reference-semantics/semantics/float.k:61` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Import(_:String) => .K ... </k>` |
| `reference-semantics/semantics/float.k:65` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= "#mathCeil"` |
| `reference-semantics/semantics/float.k:66` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| `reference-semantics/semantics/float.k:67` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| `reference-semantics/semantics/float.k:70` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= "#mathFloor"` |
| `reference-semantics/semantics/float.k:71` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| `reference-semantics/semantics/float.k:72` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| `reference-semantics/semantics/float.k:73` | syntax | `function, total, symbol(floorFI)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| `reference-semantics/semantics/float.k:74` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule floorFI(I:Int)   => I                        [concrete]` |
| `reference-semantics/semantics/float.k:75` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| `reference-semantics/semantics/float.k:78` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| `reference-semantics/semantics/float.k:79` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)` |
| `reference-semantics/semantics/float.k:82` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| `reference-semantics/semantics/float.k:83` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| `reference-semantics/semantics/float.k:84` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| `reference-semantics/semantics/float.k:85` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| `reference-semantics/semantics/float.k:86` | syntax | `function, total, symbol(toF)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| `reference-semantics/semantics/float.k:87` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule toF(F:Float) => F        [concrete]` |
| `reference-semantics/semantics/float.k:88` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule toF(I:Int)   => intToF(I) [concrete]` |
| `reference-semantics/semantics/float.k:93` | syntax | `function, total, symbol(ceilF)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| `reference-semantics/semantics/float.k:94` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule ceilF(I:Int)   => I                       [concrete]` |
| `reference-semantics/semantics/float.k:95` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| `reference-semantics/semantics/float.k:99` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| `reference-semantics/semantics/float.k:103` | syntax | `function, total, symbol(subF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| `reference-semantics/semantics/float.k:104` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| `reference-semantics/semantics/float.k:105` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| `reference-semantics/semantics/float.k:107` | syntax | `function, total, symbol(divF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| `reference-semantics/semantics/float.k:108` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| `reference-semantics/semantics/float.k:109` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| `reference-semantics/semantics/float.k:111` | syntax | `function, total, symbol(addF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| `reference-semantics/semantics/float.k:112` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| `reference-semantics/semantics/float.k:113` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| `reference-semantics/semantics/float.k:115` | syntax | `function, total, symbol(mulF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| `reference-semantics/semantics/float.k:116` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| `reference-semantics/semantics/float.k:117` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| `reference-semantics/semantics/float.k:119` | syntax | `function, total, symbol(powF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| `reference-semantics/semantics/float.k:120` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| `reference-semantics/semantics/float.k:121` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| `reference-semantics/semantics/float.k:125` | syntax | `function, total, symbol(gtF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| `reference-semantics/semantics/float.k:126` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| `reference-semantics/semantics/float.k:127` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)` |
| `reference-semantics/semantics/float.k:128` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| `reference-semantics/semantics/float.k:129` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| `reference-semantics/semantics/float.k:132` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:133` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:134` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:135` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:136` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:137` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:138` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:139` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:142` | syntax | `function, total, symbol(eqF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| `reference-semantics/semantics/float.k:143` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| `reference-semantics/semantics/float.k:144` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:145` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:146` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:147` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:148` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)` |
| `reference-semantics/semantics/float.k:149` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))` |
| `reference-semantics/semantics/float.k:150` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:151` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:154` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| `reference-semantics/semantics/float.k:155` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| `reference-semantics/semantics/float.k:160` | syntax | `function, total, symbol(decStrToF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| `reference-semantics/semantics/float.k:161` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| `reference-semantics/semantics/float.k:162` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| `reference-semantics/semantics/float.k:165` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= headIS(IntSeq) [function]` |
| `reference-semantics/semantics/float.k:166` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| `reference-semantics/semantics/float.k:167` | syntax | `function, total;function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| `reference-semantics/semantics/float.k:168` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| `reference-semantics/semantics/float.k:169` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intPartAcc(.IntSeq, A:Int) => A` |
| `reference-semantics/semantics/float.k:170` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| `reference-semantics/semantics/float.k:171` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| `reference-semantics/semantics/float.k:173` | syntax | `function, total;function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| `reference-semantics/semantics/float.k:174` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fracPart(.IntSeq) => 0` |
| `reference-semantics/semantics/float.k:175` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| `reference-semantics/semantics/float.k:176` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| `reference-semantics/semantics/float.k:177` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fracAcc(.IntSeq, A:Int) => A` |
| `reference-semantics/semantics/float.k:178` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| `reference-semantics/semantics/float.k:179` | syntax | `function, total;function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| `reference-semantics/semantics/float.k:180` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fracScale(.IntSeq) => 1` |
| `reference-semantics/semantics/float.k:181` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| `reference-semantics/semantics/float.k:182` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| `reference-semantics/semantics/float.k:183` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fscAcc(.IntSeq, A:Int) => A` |
| `reference-semantics/semantics/float.k:184` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| `reference-semantics/semantics/float.k:185` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| `reference-semantics/semantics/float.k:186` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)` |
| `reference-semantics/semantics/float.k:187` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("float", F:Float, .Vals)        => F` |
| `reference-semantics/semantics/float.k:190` | syntax | `function, total, symbol(divFloatIntV), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| `reference-semantics/semantics/float.k:191` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| `reference-semantics/semantics/float.k:192` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| `reference-semantics/semantics/float.k:195` | syntax | `function, total, symbol(intToF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| `reference-semantics/semantics/float.k:196` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| `reference-semantics/semantics/float.k:197` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:198` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:199` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:200` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:201` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:202` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:203` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| `reference-semantics/semantics/float.k:204` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| `reference-semantics/semantics/float.k:205` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| `reference-semantics/semantics/float.k:206` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| `reference-semantics/semantics/float.k:209` | syntax | `function, total, symbol(truncF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| `reference-semantics/semantics/float.k:210` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| `reference-semantics/semantics/float.k:211` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| `reference-semantics/semantics/float.k:213` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)` |
| `reference-semantics/semantics/float.k:214` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| `reference-semantics/semantics/float.k:217` | syntax | `function, total, symbol(roundF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| `reference-semantics/semantics/float.k:218` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| `reference-semantics/semantics/float.k:223` | syntax | `function, total, symbol(roundFN), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| `reference-semantics/semantics/float.k:224` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| `reference-semantics/semantics/float.k:227` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)` |
| `reference-semantics/semantics/float.k:228` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| `reference-semantics/semantics/float.k:230` | syntax | `function, total, symbol(sqrtF), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| `reference-semantics/semantics/float.k:231` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| `reference-semantics/semantics/float.k:232` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= "#mathSqrt"` |
| `reference-semantics/semantics/float.k:233` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| `reference-semantics/semantics/float.k:234` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| `reference-semantics/semantics/float.k:235` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| `reference-semantics/semantics/float.k:243` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| `reference-semantics/semantics/float.k:244` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `reference-semantics/semantics/float.k:245` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| `reference-semantics/semantics/float.k:246` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| `reference-semantics/semantics/float.k:247` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| `reference-semantics/semantics/float.k:250` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| `reference-semantics/semantics/float.k:251` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `reference-semantics/semantics/float.k:252` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| `reference-semantics/semantics/float.k:253` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| `reference-semantics/semantics/float.k:254` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| `reference-semantics/semantics/float.k:261` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| `reference-semantics/semantics/float.k:262` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| `reference-semantics/semantics/float.k:265` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| `reference-semantics/semantics/float.k:266` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| `reference-semantics/semantics/float.k:267` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| `reference-semantics/semantics/float.k:270` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| `reference-semantics/semantics/functions.k:8` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall"` |
| `reference-semantics/semantics/functions.k:14` | rule | ` F <- closureVal(PNS, BODY, L) ` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| `reference-semantics/semantics/functions.k:18` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| `reference-semantics/semantics/functions.k:19` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` |
| `reference-semantics/semantics/functions.k:27` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| `reference-semantics/semantics/functions.k:31` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| `reference-semantics/semantics/functions.k:33` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| `reference-semantics/semantics/functions.k:36` | rule | ` FV <- {M[FV` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| `reference-semantics/semantics/functions.k:42` | rule | ` F <- closureValC(PNS, CVS, BODY, CM) ` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| `reference-semantics/semantics/functions.k:47` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| `reference-semantics/semantics/functions.k:50` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| `reference-semantics/semantics/functions.k:53` | rule | ` FV <- {M[FV` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| `reference-semantics/semantics/functions.k:59` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` |
| `reference-semantics/semantics/functions.k:63` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| `reference-semantics/semantics/functions.k:64` | rule | ` P <- V ` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes>` |
| `reference-semantics/semantics/functions.k:68` | rule | `P;"$cells";P;priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]` |
| `reference-semantics/semantics/functions.k:78` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| `reference-semantics/semantics/functions.k:80` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` |
| `reference-semantics/semantics/functions.k:85` | rule | ` L <- undef ` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |
| `reference-semantics/semantics/int.k:7` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyUn("-", I:Int) => 0 -Int I` |
| `reference-semantics/semantics/int.k:9` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2` |
| `reference-semantics/semantics/int.k:11` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| `reference-semantics/semantics/int.k:12` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| `reference-semantics/semantics/int.k:13` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2` |
| `reference-semantics/semantics/int.k:14` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2` |
| `reference-semantics/semantics/int.k:15` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)` |
| `reference-semantics/semantics/int.k:16` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| `reference-semantics/semantics/int.k:17` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| `reference-semantics/semantics/int.k:19` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= pyMod(Int, Int) [function]` |
| `reference-semantics/semantics/int.k:20` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| `reference-semantics/semantics/int.k:22` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2` |
| `reference-semantics/semantics/int.k:23` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2` |
| `reference-semantics/semantics/int.k:24` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2` |
| `reference-semantics/semantics/int.k:25` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2` |
| `reference-semantics/semantics/int.k:26` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2` |
| `reference-semantics/semantics/int.k:27` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2` |
| `reference-semantics/semantics/iter.k:8` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| `reference-semantics/semantics/list.k:9` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>` |
| `reference-semantics/semantics/list.k:10` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| `reference-semantics/semantics/list.k:13` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ApplyK ::= "toList"` |
| `reference-semantics/semantics/list.k:14` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| `reference-semantics/semantics/list.k:15` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| `reference-semantics/semantics/list.k:18` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| `reference-semantics/semantics/list.k:19` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule valSeqConcat(.ValSeq, T:ValSeq)                => T` |
| `reference-semantics/semantics/list.k:20` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| `reference-semantics/semantics/list.k:24` | rule | `priority(45)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| `reference-semantics/semantics/list.k:27` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| `reference-semantics/semantics/list.k:28` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| `reference-semantics/semantics/list.k:33` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| `reference-semantics/semantics/list.k:34` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule hasRefVS(.ValSeq)                => false` |
| `reference-semantics/semantics/list.k:35` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| `reference-semantics/semantics/list.k:37` | syntax | `function;function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map)        [function]` |
| `reference-semantics/semantics/list.k:39` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true` |
| `reference-semantics/semantics/list.k:40` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false` |
| `reference-semantics/semantics/list.k:41` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false` |
| `reference-semantics/semantics/list.k:42` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| `reference-semantics/semantics/list.k:45` | rule | `H` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| `reference-semantics/semantics/list.k:47` | rule | `H` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| `reference-semantics/semantics/list.k:49` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| `reference-semantics/semantics/list.k:50` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| `reference-semantics/semantics/list.k:53` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` |
| `reference-semantics/semantics/list.k:58` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| `reference-semantics/semantics/list.k:59` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| `reference-semantics/semantics/list.k:60` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| `reference-semantics/semantics/list.k:61` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| `reference-semantics/semantics/list.k:62` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| `reference-semantics/semantics/list.k:63` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| `reference-semantics/semantics/list.k:65` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| `reference-semantics/semantics/list.k:67` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| `reference-semantics/semantics/methods.k:10` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| `reference-semantics/semantics/methods.k:13` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| `reference-semantics/semantics/methods.k:14` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| `reference-semantics/semantics/methods.k:15` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| `reference-semantics/semantics/methods.k:16` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| `reference-semantics/semantics/methods.k:19` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))` |
| `reference-semantics/semantics/methods.k:20` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))` |
| `reference-semantics/semantics/methods.k:21` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| `reference-semantics/semantics/methods.k:26` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| `reference-semantics/semantics/methods.k:27` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:28` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| `reference-semantics/semantics/methods.k:29` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| `reference-semantics/semantics/methods.k:30` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` |
| `reference-semantics/semantics/methods.k:34` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| `reference-semantics/semantics/methods.k:35` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| `reference-semantics/semantics/methods.k:36` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| `reference-semantics/semantics/methods.k:37` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| `reference-semantics/semantics/methods.k:39` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| `reference-semantics/semantics/methods.k:41` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| `reference-semantics/semantics/methods.k:42` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| `reference-semantics/semantics/methods.k:43` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| `reference-semantics/semantics/methods.k:44` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| `reference-semantics/semantics/methods.k:47` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| `reference-semantics/semantics/methods.k:48` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:49` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule trimWS(.IntSeq) => .IntSeq` |
| `reference-semantics/semantics/methods.k:50` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| `reference-semantics/semantics/methods.k:51` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| `reference-semantics/semantics/methods.k:52` | syntax | `function, total;function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:53` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| `reference-semantics/semantics/methods.k:54` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| `reference-semantics/semantics/methods.k:55` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| `reference-semantics/semantics/methods.k:58` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| `reference-semantics/semantics/methods.k:61` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| `reference-semantics/semantics/methods.k:64` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| `reference-semantics/semantics/methods.k:65` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| `reference-semantics/semantics/methods.k:66` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule cntOccVS(.ValSeq, _:Val)                => 0` |
| `reference-semantics/semantics/methods.k:67` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| `reference-semantics/semantics/methods.k:68` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)` |
| `reference-semantics/semantics/methods.k:72` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| `reference-semantics/semantics/methods.k:75` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result` |
| `reference-semantics/semantics/methods.k:76` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| `reference-semantics/semantics/methods.k:77` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| `reference-semantics/semantics/methods.k:79` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` |
| `reference-semantics/semantics/methods.k:82` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| `reference-semantics/semantics/methods.k:83` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC` |
| `reference-semantics/semantics/methods.k:84` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| `reference-semantics/semantics/methods.k:85` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isWSC(Int) [function, total]` |
| `reference-semantics/semantics/methods.k:86` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| `reference-semantics/semantics/methods.k:89` | rule | `priority(39)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` |
| `reference-semantics/semantics/methods.k:94` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| `reference-semantics/semantics/methods.k:97` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token` |
| `reference-semantics/semantics/methods.k:98` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)` |
| `reference-semantics/semantics/methods.k:99` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| `reference-semantics/semantics/methods.k:101` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| `reference-semantics/semantics/methods.k:104` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| `reference-semantics/semantics/methods.k:106` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| `reference-semantics/semantics/methods.k:107` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq` |
| `reference-semantics/semantics/methods.k:108` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| `reference-semantics/semantics/methods.k:109` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| `reference-semantics/semantics/methods.k:112` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isUpperC(Int) [function, total]` |
| `reference-semantics/semantics/methods.k:113` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| `reference-semantics/semantics/methods.k:115` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isLowerC(Int) [function, total]` |
| `reference-semantics/semantics/methods.k:116` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| `reference-semantics/semantics/methods.k:118` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| `reference-semantics/semantics/methods.k:119` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| `reference-semantics/semantics/methods.k:121` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= isDigitC(Int) [function, total]` |
| `reference-semantics/semantics/methods.k:122` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `reference-semantics/semantics/methods.k:124` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:125` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule hasUpper(.IntSeq) => false` |
| `reference-semantics/semantics/methods.k:126` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| `reference-semantics/semantics/methods.k:128` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:129` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule hasLower(.IntSeq) => false` |
| `reference-semantics/semantics/methods.k:130` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| `reference-semantics/semantics/methods.k:132` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:133` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule allAlpha(.IntSeq) => true` |
| `reference-semantics/semantics/methods.k:134` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| `reference-semantics/semantics/methods.k:136` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:137` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule allDigit(.IntSeq) => true` |
| `reference-semantics/semantics/methods.k:138` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| `reference-semantics/semantics/methods.k:140` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= lowerC(Int) [function, total]` |
| `reference-semantics/semantics/methods.k:142` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `reference-semantics/semantics/methods.k:143` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule lowerC(C:Int) => C         [owise]` |
| `reference-semantics/semantics/methods.k:145` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= upperC(Int) [function, total]` |
| `reference-semantics/semantics/methods.k:146` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `reference-semantics/semantics/methods.k:147` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule upperC(C:Int) => C         [owise]` |
| `reference-semantics/semantics/methods.k:149` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= swapC(Int) [function, total]` |
| `reference-semantics/semantics/methods.k:150` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `reference-semantics/semantics/methods.k:151` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `reference-semantics/semantics/methods.k:152` | rule | `owise` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule swapC(C:Int) => C         [owise]` |
| `reference-semantics/semantics/methods.k:154` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:155` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mapLower(.IntSeq) => .IntSeq` |
| `reference-semantics/semantics/methods.k:156` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| `reference-semantics/semantics/methods.k:158` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:159` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mapUpper(.IntSeq) => .IntSeq` |
| `reference-semantics/semantics/methods.k:160` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| `reference-semantics/semantics/methods.k:162` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:163` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mapSwap(.IntSeq) => .IntSeq` |
| `reference-semantics/semantics/methods.k:164` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| `reference-semantics/semantics/methods.k:166` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/methods.k:167` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule startsWith(.IntSeq, _:IntSeq)               => true` |
| `reference-semantics/semantics/methods.k:168` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `reference-semantics/semantics/methods.k:169` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| `reference-semantics/semantics/operators.k:10` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| `reference-semantics/semantics/operators.k:12` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| `reference-semantics/semantics/operators.k:15` | context | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `context Compare(HOLE, _)` |
| `reference-semantics/semantics/operators.k:16` | context | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `context Compare(_:Val, CmpOp(_, HOLE))` |
| `reference-semantics/semantics/operators.k:17` | rule | `owise` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| `reference-semantics/semantics/operators.k:19` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("is",     V:Val, noneV) => V ==K noneV` |
| `reference-semantics/semantics/operators.k:20` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| `reference-semantics/semantics/operators.k:25` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/operators.k:28` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` |
| `reference-semantics/semantics/operators.k:34` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| `reference-semantics/semantics/operators.k:38` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| `reference-semantics/semantics/operators.k:44` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/range.k:9` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| `reference-semantics/semantics/range.k:10` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| `reference-semantics/semantics/range.k:12` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| `reference-semantics/semantics/range.k:13` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| `reference-semantics/semantics/range.k:15` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| `reference-semantics/semantics/range.k:17` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| `reference-semantics/semantics/range.k:20` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| `reference-semantics/semantics/range.k:23` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| `reference-semantics/semantics/set.k:8` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= setV(IntSeq)` |
| `reference-semantics/semantics/set.k:11` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| `reference-semantics/semantics/set.k:12` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule codeIn(_:Int, .IntSeq)                => false` |
| `reference-semantics/semantics/set.k:13` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| `reference-semantics/semantics/set.k:16` | syntax | `function, total;function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] \| dedupFrom(IntSeq, IntSeq)  [function, total]` |
| `reference-semantics/semantics/set.k:18` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| `reference-semantics/semantics/set.k:19` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| `reference-semantics/semantics/set.k:20` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| `reference-semantics/semantics/set.k:22` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| `reference-semantics/semantics/set.k:25` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| `reference-semantics/semantics/set.k:26` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)` |
| `reference-semantics/semantics/set.k:27` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| `reference-semantics/semantics/set.k:31` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/set.k:32` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule subsetCodes(.IntSeq, _:IntSeq)                => true` |
| `reference-semantics/semantics/set.k:33` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| `reference-semantics/semantics/set.k:35` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/set.k:36` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| `reference-semantics/semantics/set.k:39` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| `reference-semantics/semantics/sort.k:18` | syntax | `function, total, symbol(sortVS), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| `reference-semantics/semantics/sort.k:19` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| `reference-semantics/semantics/sort.k:20` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule sortVS(.ValSeq)                => .ValSeq          [concrete]` |
| `reference-semantics/semantics/sort.k:21` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| `reference-semantics/semantics/sort.k:22` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]` |
| `reference-semantics/semantics/sort.k:23` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| `reference-semantics/semantics/sort.k:24` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]` |
| `reference-semantics/semantics/sort.k:26` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| `reference-semantics/semantics/sort.k:27` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| `reference-semantics/semantics/sort.k:28` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| `reference-semantics/semantics/sort.k:29` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| `reference-semantics/semantics/sort.k:31` | rule | `concrete` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` |
| `reference-semantics/semantics/sort.k:36` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` |
| `reference-semantics/semantics/sort.k:40` | rule | `priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` |
| `reference-semantics/semantics/sort.k:49` | syntax | `function, total, symbol(sortKeyVS), no-evaluators` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| `reference-semantics/semantics/sort.k:51` | syntax | `function, total;function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| `reference-semantics/semantics/sort.k:53` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| `reference-semantics/semantics/sort.k:54` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| `reference-semantics/semantics/sort.k:55` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| `reference-semantics/semantics/sort.k:57` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| `reference-semantics/semantics/sort.k:58` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule condRev(S:ValSeq, false) => S` |
| `reference-semantics/semantics/sort.k:59` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule condRev(S:ValSeq, true)  => revVS(S)` |
| `reference-semantics/semantics/sort.k:61` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| `reference-semantics/semantics/sort.k:63` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| `reference-semantics/semantics/sort.k:65` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` |
| `reference-semantics/semantics/str.k:8` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>` |
| `reference-semantics/semantics/str.k:9` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` |
| `reference-semantics/semantics/str.k:13` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= strToCodes(String) [function]` |
| `reference-semantics/semantics/str.k:14` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| `reference-semantics/semantics/str.k:15` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strToCodes("") => .IntSeq` |
| `reference-semantics/semantics/str.k:16` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` |
| `reference-semantics/semantics/str.k:20` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/str.k:21` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule seqConcat(.IntSeq, T:IntSeq)                => T` |
| `reference-semantics/semantics/str.k:22` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| `reference-semantics/semantics/str.k:24` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| `reference-semantics/semantics/str.k:25` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| `reference-semantics/semantics/str.k:26` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| `reference-semantics/semantics/str.k:29` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| `reference-semantics/semantics/str.k:30` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| `reference-semantics/semantics/str.k:32` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/str.k:33` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strPrefix(.IntSeq, _:IntSeq)               => true` |
| `reference-semantics/semantics/str.k:34` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `reference-semantics/semantics/str.k:35` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| `reference-semantics/semantics/str.k:37` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/str.k:38` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)` |
| `reference-semantics/semantics/str.k:39` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)` |
| `reference-semantics/semantics/str.k:40` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` |
| `reference-semantics/semantics/str.k:48` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| `reference-semantics/semantics/str.k:49` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strLt(.IntSeq, .IntSeq)                => false` |
| `reference-semantics/semantics/str.k:50` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| `reference-semantics/semantics/str.k:51` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `reference-semantics/semantics/str.k:52` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B` |
| `reference-semantics/semantics/str.k:53` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B` |
| `reference-semantics/semantics/str.k:54` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| `reference-semantics/semantics/str.k:56` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `reference-semantics/semantics/str.k:57` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| `reference-semantics/semantics/str.k:58` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| `reference-semantics/semantics/str.k:59` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| `reference-semantics/semantics/subscript.k:11` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| `reference-semantics/semantics/subscript.k:12` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V` |
| `reference-semantics/semantics/subscript.k:13` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| `reference-semantics/semantics/subscript.k:16` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| `reference-semantics/semantics/subscript.k:17` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C` |
| `reference-semantics/semantics/subscript.k:18` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| `reference-semantics/semantics/subscript.k:21` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| `reference-semantics/semantics/subscript.k:22` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| `reference-semantics/semantics/subscript.k:23` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0` |
| `reference-semantics/semantics/subscript.k:27` | context | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `context Subscript(HOLE, _)` |
| `reference-semantics/semantics/subscript.k:28` | context | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `context Subscript(_:Val, HOLE:Expr)` |
| `reference-semantics/semantics/subscript.k:31` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/subscript.k:35` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| `reference-semantics/semantics/subscript.k:37` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= applyIndex(Val, Int) [function]` |
| `reference-semantics/semantics/subscript.k:38` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `reference-semantics/semantics/subscript.k:39` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `reference-semantics/semantics/subscript.k:40` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` |
| `reference-semantics/semantics/subscript.k:44` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| `reference-semantics/semantics/subscript.k:49` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax OptInt ::= "noB" \| someB(Int)` |
| `reference-semantics/semantics/subscript.k:50` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #evalB(NoBound)  => noB ... </k>` |
| `reference-semantics/semantics/subscript.k:51` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>` |
| `reference-semantics/semantics/subscript.k:52` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| `reference-semantics/semantics/subscript.k:54` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| `reference-semantics/semantics/subscript.k:55` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| `reference-semantics/semantics/subscript.k:56` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| `reference-semantics/semantics/subscript.k:58` | rule | `priority(45)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| `reference-semantics/semantics/subscript.k:61` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| `reference-semantics/semantics/subscript.k:63` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| `reference-semantics/semantics/subscript.k:64` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| `reference-semantics/semantics/subscript.k:66` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| `reference-semantics/semantics/subscript.k:68` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` |
| `reference-semantics/semantics/subscript.k:72` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= slStep(OptInt) [function, total]` |
| `reference-semantics/semantics/subscript.k:73` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slStep(noB)          => 1` |
| `reference-semantics/semantics/subscript.k:74` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slStep(someB(S:Int)) => S` |
| `reference-semantics/semantics/subscript.k:76` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| `reference-semantics/semantics/subscript.k:77` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| `reference-semantics/semantics/subscript.k:79` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0` |
| `reference-semantics/semantics/subscript.k:81` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| `reference-semantics/semantics/subscript.k:83` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| `reference-semantics/semantics/subscript.k:84` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0` |
| `reference-semantics/semantics/subscript.k:86` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| `reference-semantics/semantics/subscript.k:88` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| `reference-semantics/semantics/subscript.k:90` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| `reference-semantics/semantics/subscript.k:91` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0` |
| `reference-semantics/semantics/subscript.k:93` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| `reference-semantics/semantics/subscript.k:96` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| `reference-semantics/semantics/subscript.k:97` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| `reference-semantics/semantics/subscript.k:99` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| `reference-semantics/semantics/subscript.k:102` | syntax | `function, total` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| `reference-semantics/semantics/subscript.k:103` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN` |
| `reference-semantics/semantics/subscript.k:105` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` |
| `reference-semantics/semantics/subscript.k:109` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| `reference-semantics/semantics/subscript.k:110` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| `reference-semantics/semantics/subscript.k:113` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| `reference-semantics/semantics/subscript.k:116` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| `reference-semantics/semantics/subscript.k:117` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| `reference-semantics/semantics/subscript.k:120` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| `reference-semantics/semantics/syntax.k:9` | syntax | `strict(2);seqstrict(2, 3);macro;macro;strict(1);strict(1)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Expr ::= "Int"      "(" Int ")" \| "Float"    "(" Float ")" \| "Bool"     "(" Bool ")" \| "Name"     "(" String ")" \| "Str"      "(" String ")" \| "UnaryOp"  "(" String "," Expr ")" [strict(2)] \| "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp"    "(" String "," Exprs ")" \| "ListExpr"  "(" Exprs ")" \| "DictExpr"  "(" Entries ")" \| "ListComp"  "(" Expr "," CompFors ")" [macro] \| "GenExp"    "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda"    "(" Params "," Expr ")" \| "KwArg"     "(" String "," Expr ")" \| "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call"      "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare"   "(" Expr "," CmpOp ")"` |
| `reference-semantics/semantics/syntax.k:32` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"` |
| `reference-semantics/semantics/syntax.k:33` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"` |
| `reference-semantics/semantics/syntax.k:34` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Entries  ::= List{Entry, ","}` |
| `reference-semantics/semantics/syntax.k:35` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| `reference-semantics/semantics/syntax.k:36` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax CompFors ::= List{CompFor, ""}` |
| `reference-semantics/semantics/syntax.k:37` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Exprs    ::= List{Expr, ","}` |
| `reference-semantics/semantics/syntax.k:38` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| `reference-semantics/semantics/syntax.k:39` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Bound    ::= Expr \| "NoBound"` |
| `reference-semantics/semantics/syntax.k:41` | syntax | `strict(2);strict(3);strict(2);strict(1);strict;strict;strict` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] \| "Import"    "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While"     "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return"    "(" Expr ")" [strict] \| "Assert"    "(" Expr ")" [strict] \| "Expr"      "(" Expr ")" [strict] \| "FuncDef"   "(" String "," Params "," Stmts ")" \| "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` |
| `reference-semantics/semantics/syntax.k:56` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Stmts      ::= List{Stmt, ""}` |
| `reference-semantics/semantics/syntax.k:57` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Params     ::= "Params" "(" ParamNames ")"` |
| `reference-semantics/semantics/syntax.k:58` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax CellVars   ::= "CellVars" "(" ParamNames ")"` |
| `reference-semantics/semantics/syntax.k:59` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"` |
| `reference-semantics/semantics/syntax.k:60` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ParamNames ::= List{String, ","}` |
| `reference-semantics/semantics/syntax.k:61` | syntax | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `syntax Module     ::= "Module" "(" Stmts ")"` |
| `reference-semantics/semantics/tuple.k:10` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>` |
| `reference-semantics/semantics/tuple.k:11` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| `reference-semantics/semantics/tuple.k:14` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax ApplyK ::= "toTuple"` |
| `reference-semantics/semantics/tuple.k:15` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| `reference-semantics/semantics/tuple.k:16` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| `reference-semantics/semantics/tuple.k:18` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| `reference-semantics/semantics/tuple.k:20` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| `reference-semantics/semantics/tuple.k:21` | rule | `-` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| `reference-semantics/semantics/tuple.k:23` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| `reference-semantics/semantics/tuple.k:24` | syntax | `function` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| `reference-semantics/semantics/tuple.k:25` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| `reference-semantics/semantics/tuple.k:26` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| `reference-semantics/semantics/tuple.k:28` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| `reference-semantics/semantics/tuple.k:31` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #bindTgt(Expr, Val)` |
| `reference-semantics/semantics/tuple.k:32` | rule | ` X <- V ` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| `reference-semantics/semantics/tuple.k:35` | rule | `X;"$cells";X;priority(40)` | REACHED_FIXED_ITEM_REVIEWED_SOUND | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| `reference-semantics/semantics/tuple.k:42` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `reference-semantics/semantics/tuple.k:43` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| `reference-semantics/semantics/tuple.k:44` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/tuple.k:49` | syntax | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| `reference-semantics/semantics/tuple.k:50` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `reference-semantics/semantics/tuple.k:51` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| `reference-semantics/semantics/tuple.k:52` | rule | `priority(40)` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `reference-semantics/semantics/tuple.k:55` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| `reference-semantics/semantics/tuple.k:57` | rule | `-` | UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| `verification.k:8` | syntax | `function, total` | PROOF_LOCAL_REVIEWED_SOUND | `syntax Int ::= fib4Spec(Int) [function, total] endmodule module VERIFICATION imports MPY imports VERIFICATION-SYNTAX` |
| `verification.k:15` | rule | `-` | PROOF_LOCAL_REVIEWED_SOUND | `rule fib4Spec(N) => 0 requires N <=Int 0` |
| `verification.k:17` | rule | `-` | PROOF_LOCAL_REVIEWED_SOUND | `rule fib4Spec(1) => 0` |
| `verification.k:18` | rule | `-` | PROOF_LOCAL_REVIEWED_SOUND | `rule fib4Spec(2) => 2` |
| `verification.k:19` | rule | `-` | PROOF_LOCAL_REVIEWED_SOUND | `rule fib4Spec(3) => 0` |
| `verification.k:20` | rule | `-` | PROOF_LOCAL_REVIEWED_SOUND | `rule fib4Spec(N) => fib4Spec(N -Int 1) +Int fib4Spec(N -Int 2) +Int fib4Spec(N -Int 3) +Int fib4Spec(N -Int 4) requires N >=Int 4` |
| `spec.k:8` | claim | `loop-invariant` | DERIVED_CIRCULARITY_REVIEWED_SOUND | `claim [loop-invariant]: <k> #while( Compare(Name("i"), CmpOp("<", Name("n"))), Assign( Name("e"), BinOp( "+", BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")), Name("d"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("c")) Assign(Name("c"), Name("d")) Assign(Name("d"), Name("e")) Assign(Name("i"), BinOp("+", Name("i"), Int(1))) ) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope( ("n" \|-> N:Int) ("i" \|-> (I:Int => N)) ("a" \|-> (fib4Spec(I) => fib4Spec(N))) ("b" \|-> (fib4Spec(I +Int 1) => ?BFinal:Int)) ("c" \|-> (fib4Spec(I +Int 2) => ?CFinal:Int)) ("d" \|-> (fib4Spec(I +Int 3) => ?DFinal:Int)) ("e" \|-> (E:Int => ?EFinal:Int)), P:Parent) ... </scopes> requires I >=Int 0 andBool I <=Int N` |
| `spec.k:44` | claim | `fib4-correct` | TARGET_CLAIM_REVIEWED_SOUND | `claim [fib4-correct]: <k> Call(Name("fib4"), Int(N:Int)) => fib4Spec(N) </k> <env> 0 </env> <scopes> 0 \|-> scope( "fib4" \|-> closureVal( "n", Assign(Name("a"), Int(0)) Assign(Name("b"), Int(0)) Assign(Name("c"), Int(2)) Assign(Name("d"), Int(0)) Assign(Name("e"), Int(0)) Assign(Name("i"), Int(0)) While( Compare(Name("i"), CmpOp("<", Name("n"))), Assign( Name("e"), BinOp( "+", BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")), Name("d"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("c")) Assign(Name("c"), Name("d")) Assign(Name("d"), Name("e")) Assign(Name("i"), BinOp("+", Name("i"), Int(1)))) Return(Name("a")), 0), parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires N >=Int 0` |

## Per-file raw-start cross-check

- `reference-semantics/semantics.k`: PASS; raw={} parsed={}
- `reference-semantics/semantics/assert.k`: PASS; raw={'rule': 3} parsed={'rule': 3}
- `reference-semantics/semantics/bool.k`: PASS; raw={'rule': 13, 'context': 1} parsed={'rule': 13, 'context': 1}
- `reference-semantics/semantics/builtins.k`: PASS; raw={'syntax': 38, 'rule': 137} parsed={'syntax': 38, 'rule': 137}
- `reference-semantics/semantics/call.k`: PASS; raw={'rule': 21, 'syntax': 3} parsed={'rule': 21, 'syntax': 3}
- `reference-semantics/semantics/comprehension.k`: PASS; raw={'rule': 7, 'syntax': 3} parsed={'rule': 7, 'syntax': 3}
- `reference-semantics/semantics/concrete.k`: PASS; raw={'rule': 16, 'syntax': 5} parsed={'rule': 16, 'syntax': 5}
- `reference-semantics/semantics/controls.k`: PASS; raw={'rule': 34, 'syntax': 3} parsed={'rule': 34, 'syntax': 3}
- `reference-semantics/semantics/core.k`: PASS; raw={'syntax': 37, 'configuration': 1, 'rule': 46} parsed={'syntax': 37, 'configuration': 1, 'rule': 46}
- `reference-semantics/semantics/dict.k`: PASS; raw={'syntax': 12, 'rule': 28} parsed={'syntax': 12, 'rule': 28}
- `reference-semantics/semantics/float.k`: PASS; raw={'syntax': 34, 'rule': 121} parsed={'syntax': 34, 'rule': 121}
- `reference-semantics/semantics/functions.k`: PASS; raw={'syntax': 4, 'rule': 15} parsed={'syntax': 4, 'rule': 15}
- `reference-semantics/semantics/int.k`: PASS; raw={'rule': 16, 'syntax': 1} parsed={'rule': 16, 'syntax': 1}
- `reference-semantics/semantics/iter.k`: PASS; raw={'syntax': 1} parsed={'syntax': 1}
- `reference-semantics/semantics/list.k`: PASS; raw={'rule': 27, 'syntax': 5} parsed={'rule': 27, 'syntax': 5}
- `reference-semantics/semantics/methods.k`: PASS; raw={'syntax': 27, 'rule': 75} parsed={'syntax': 27, 'rule': 75}
- `reference-semantics/semantics/operators.k`: PASS; raw={'rule': 10, 'context': 2} parsed={'rule': 10, 'context': 2}
- `reference-semantics/semantics/range.k`: PASS; raw={'syntax': 2, 'rule': 6} parsed={'syntax': 2, 'rule': 6}
- `reference-semantics/semantics/set.k`: PASS; raw={'syntax': 6, 'rule': 12} parsed={'syntax': 6, 'rule': 12}
- `reference-semantics/semantics/sort.k`: PASS; raw={'syntax': 6, 'rule': 19} parsed={'syntax': 6, 'rule': 19}
- `reference-semantics/semantics/str.k`: PASS; raw={'rule': 28, 'syntax': 5} parsed={'rule': 28, 'syntax': 5}
- `reference-semantics/semantics/subscript.k`: PASS; raw={'syntax': 15, 'rule': 40, 'context': 2} parsed={'syntax': 15, 'rule': 40, 'context': 2}
- `reference-semantics/semantics/syntax.k`: PASS; raw={'syntax': 16} parsed={'syntax': 16}
- `reference-semantics/semantics/tuple.k`: PASS; raw={'rule': 21, 'syntax': 4} parsed={'rule': 21, 'syntax': 4}
- `verification.k`: PASS; raw={'syntax': 1, 'rule': 5} parsed={'syntax': 1, 'rule': 5}
- `spec.k`: PASS; raw={'claim': 2} parsed={'claim': 2}

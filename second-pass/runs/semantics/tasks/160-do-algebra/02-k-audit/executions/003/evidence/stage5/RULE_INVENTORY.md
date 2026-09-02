# Exhaustive K source inventory

Generated from the clean scratch copies. Each row is keyed by source line and a digest of the full declaration/sentence; displayed text is bounded.

- Files: 26
- Total inventory records: 950
- Kinds: `{'claim': 10, 'configuration': 1, 'context': 5, 'rule': 703, 'syntax': 231}`
- Classes: `{'claim': 10, 'concrete rule': 35, 'configuration': 1, 'context': 5, 'ordinary rule': 597, 'owise rule': 26, 'priority rule': 45, 'syntax': 79, 'syntax (function)': 38, 'syntax (function, total)': 86, 'syntax (function, total, no-evaluators)': 22, 'syntax (macro)': 5, 'syntax (macro-rec)': 1}`

## Per-file counts

| File | configuration | syntax | context | rule | claim | alias |
|---|---:|---:|---:|---:|---:|---:|
| `reference-semantics/semantics/assert.k` | 0 | 0 | 0 | 3 | 0 | 0 |
| `reference-semantics/semantics/bool.k` | 0 | 0 | 1 | 13 | 0 | 0 |
| `reference-semantics/semantics/builtins.k` | 0 | 38 | 0 | 137 | 0 | 0 |
| `reference-semantics/semantics/call.k` | 0 | 3 | 0 | 21 | 0 | 0 |
| `reference-semantics/semantics/comprehension.k` | 0 | 3 | 0 | 7 | 0 | 0 |
| `reference-semantics/semantics/concrete.k` | 0 | 5 | 0 | 16 | 0 | 0 |
| `reference-semantics/semantics/controls.k` | 0 | 3 | 0 | 34 | 0 | 0 |
| `reference-semantics/semantics/core.k` | 1 | 37 | 0 | 46 | 0 | 0 |
| `reference-semantics/semantics/dict.k` | 0 | 12 | 0 | 28 | 0 | 0 |
| `reference-semantics/semantics/float.k` | 0 | 34 | 0 | 121 | 0 | 0 |
| `reference-semantics/semantics/functions.k` | 0 | 4 | 0 | 15 | 0 | 0 |
| `reference-semantics/semantics/int.k` | 0 | 1 | 0 | 16 | 0 | 0 |
| `reference-semantics/semantics/iter.k` | 0 | 1 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/list.k` | 0 | 5 | 0 | 27 | 0 | 0 |
| `reference-semantics/semantics/methods.k` | 0 | 27 | 0 | 75 | 0 | 0 |
| `reference-semantics/semantics/operators.k` | 0 | 0 | 2 | 10 | 0 | 0 |
| `reference-semantics/semantics/range.k` | 0 | 2 | 0 | 6 | 0 | 0 |
| `reference-semantics/semantics/set.k` | 0 | 6 | 0 | 12 | 0 | 0 |
| `reference-semantics/semantics/sort.k` | 0 | 6 | 0 | 19 | 0 | 0 |
| `reference-semantics/semantics/str.k` | 0 | 5 | 0 | 28 | 0 | 0 |
| `reference-semantics/semantics/subscript.k` | 0 | 15 | 2 | 40 | 0 | 0 |
| `reference-semantics/semantics/syntax.k` | 0 | 16 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/tuple.k` | 0 | 4 | 0 | 21 | 0 | 0 |
| `spec.k` | 0 | 0 | 0 | 0 | 10 | 0 |
| `verification.k` | 0 | 4 | 0 | 8 | 0 | 0 |

## Source-addressed inventory

| Location | Kind/class | Attributes | Digest | Full-sentence prefix |
|---|---|---|---|---|
| `reference-semantics/semantics/assert.k:6` | ordinary rule | — | `682cca2e3a04` | rule <k> Assert(V:Val) => .K ... </k> requires truthy(V) |
| `reference-semantics/semantics/assert.k:8` | ordinary rule | — | `8e836f6b30c1` | rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V) |
| `reference-semantics/semantics/assert.k:13` | priority rule | priority(40) | `5ee0a6a35fcd` | rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/bool.k:8` | ordinary rule | — | `f6a9f817afd5` | rule applyUn("not", V:Val) => notBool truthy(V) |
| `reference-semantics/semantics/bool.k:10` | ordinary rule | — | `27c7ab073847` | rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2 |
| `reference-semantics/semantics/bool.k:11` | ordinary rule | — | `f0788e13f0ab` | rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 |
| `reference-semantics/semantics/bool.k:16` | context | — | `4bad2e2ff81c` | context BoolOp(_, (HOLE:Expr, _:Exprs)) |
| `reference-semantics/semantics/bool.k:17` | ordinary rule | — | `dd652a87b566` | rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k> |
| `reference-semantics/semantics/bool.k:18` | ordinary rule | — | `b81701969e23` | rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V) |
| `reference-semantics/semantics/bool.k:20` | ordinary rule | — | `1952c4203132` | rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V) |
| `reference-semantics/semantics/bool.k:22` | ordinary rule | — | `e2c0667e86f3` | rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V) |
| `reference-semantics/semantics/bool.k:24` | ordinary rule | — | `8370ea466dbf` | rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) |
| `reference-semantics/semantics/bool.k:29` | priority rule | priority(40) | `7680e70ab6b9` | rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)] |
| `reference-semantics/semantics/bool.k:31` | priority rule | priority(40) | `653b3d2be1cc` | rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)] |
| `reference-semantics/semantics/bool.k:35` | priority rule | priority(40) | `c7fb0eae3ef3` | rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)] |
| `reference-semantics/semantics/bool.k:39` | priority rule | priority(40) | `80995c2d026a` | rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)] |
| `reference-semantics/semantics/bool.k:43` | priority rule | priority(40) | `308edf67354a` | rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)] |
| `reference-semantics/semantics/builtins.k:17` | syntax (function) | function | `8eb9b94daf32` | syntax Val ::= applyBuiltin(String, Vals) [function] |
| `reference-semantics/semantics/builtins.k:20` | syntax (function) | function | `f6cf3d1713c1` | syntax Int ::= seqLen(Val) [function] |
| `reference-semantics/semantics/builtins.k:21` | ordinary rule | — | `4c33466e09a7` | rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ) |
| `reference-semantics/semantics/builtins.k:22` | ordinary rule | — | `4304dc6e0531` | rule seqLen(list(VS:ValSeq)) => vsLen(VS) |
| `reference-semantics/semantics/builtins.k:23` | ordinary rule | — | `60d5ac1453fb` | rule seqLen(tuple(VS:ValSeq)) => vsLen(VS) |
| `reference-semantics/semantics/builtins.k:24` | ordinary rule | — | `daf5d65cb8f2` | rule seqLen(str(IS:IntSeq)) => isLen(IS) |
| `reference-semantics/semantics/builtins.k:25` | ordinary rule | — | `423d538bf265` | rule seqLen(setV(DS:IntSeq)) => isLen(DS) |
| `reference-semantics/semantics/builtins.k:26` | ordinary rule | — | `b762a4c2dc2a` | rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) |
| `reference-semantics/semantics/builtins.k:32` | ordinary rule | — | `ca8be208f8fa` | rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k> |
| `reference-semantics/semantics/builtins.k:33` | ordinary rule | — | `d4c8072f0224` | rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k> |
| `reference-semantics/semantics/builtins.k:34` | ordinary rule | — | `3dd9d5c101b8` | rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k> |
| `reference-semantics/semantics/builtins.k:35` | ordinary rule | — | `d19a2af0b576` | rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k> |
| `reference-semantics/semantics/builtins.k:36` | syntax (function, total) | function, total | `01aff6eecdd4` | syntax ValSeq ::= charsOf(IntSeq) [function, total] |
| `reference-semantics/semantics/builtins.k:37` | ordinary rule | — | `18e5f857c943` | rule charsOf(.IntSeq) => .ValSeq |
| `reference-semantics/semantics/builtins.k:38` | ordinary rule | — | `a2c1d74e5b75` | rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) |
| `reference-semantics/semantics/builtins.k:41` | ordinary rule | — | `9f9f03920225` | rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) |
| `reference-semantics/semantics/builtins.k:44` | ordinary rule | — | `d43957f0423a` | rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) |
| `reference-semantics/semantics/builtins.k:47` | syntax | — | `8faa5250ed2b` | syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int) |
| `reference-semantics/semantics/builtins.k:48` | ordinary rule | — | `cd531bdb9afa` | rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k> |
| `reference-semantics/semantics/builtins.k:49` | ordinary rule | — | `74ff8e8be842` | rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k> |
| `reference-semantics/semantics/builtins.k:50` | ordinary rule | — | `3216ead685aa` | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V) |
| `reference-semantics/semantics/builtins.k:54` | syntax (function) | function | `0355f95a50a6` | syntax Int ::= intOf(Val) [function] |
| `reference-semantics/semantics/builtins.k:55` | ordinary rule | — | `ec6a1865ddec` | rule intOf(I:Int) => I |
| `reference-semantics/semantics/builtins.k:56` | ordinary rule | — | `39b97d83aa9d` | rule intOf(B:Bool) => #if B #then 1 #else 0 #fi |
| `reference-semantics/semantics/builtins.k:59` | syntax | — | `ed695fa0c4db` | syntax KItem ::= #allAcc(Iterable) \| "#allCont" |
| `reference-semantics/semantics/builtins.k:60` | ordinary rule | — | `e7fc3b9b3a84` | rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k> |
| `reference-semantics/semantics/builtins.k:61` | ordinary rule | — | `b74e515d3e67` | rule <k> #iterDone ~> #allCont => true ... </k> |
| `reference-semantics/semantics/builtins.k:62` | ordinary rule | — | `c7480ce5c2eb` | rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V) |
| `reference-semantics/semantics/builtins.k:64` | ordinary rule | — | `d10dbb51af32` | rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V) |
| `reference-semantics/semantics/builtins.k:67` | syntax | — | `fbd45cd7894a` | syntax KItem ::= #anyAcc(Iterable) \| "#anyCont" |
| `reference-semantics/semantics/builtins.k:68` | ordinary rule | — | `ca3f3bc3212a` | rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k> |
| `reference-semantics/semantics/builtins.k:69` | ordinary rule | — | `c0ee3d29de0f` | rule <k> #iterDone ~> #anyCont => false ... </k> |
| `reference-semantics/semantics/builtins.k:70` | ordinary rule | — | `3bc1ac77dc8a` | rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V) |
| `reference-semantics/semantics/builtins.k:72` | ordinary rule | — | `8af4aae9516c` | rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) |
| `reference-semantics/semantics/builtins.k:76` | syntax | — | `e3461106d962` | syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int) |
| `reference-semantics/semantics/builtins.k:77` | ordinary rule | — | `59848da8989b` | rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k> |
| `reference-semantics/semantics/builtins.k:78` | ordinary rule | — | `692729d25920` | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V) |
| `reference-semantics/semantics/builtins.k:80` | ordinary rule | — | `66b9fabf71fa` | rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k> |
| `reference-semantics/semantics/builtins.k:81` | ordinary rule | — | `45675f8137ef` | rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k> |
| `reference-semantics/semantics/builtins.k:82` | ordinary rule | — | `87e28ee6f8a2` | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V) |
| `reference-semantics/semantics/builtins.k:86` | syntax | — | `612c7bdfd2d3` | syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int) |
| `reference-semantics/semantics/builtins.k:87` | ordinary rule | — | `eb6389d2a176` | rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k> |
| `reference-semantics/semantics/builtins.k:88` | ordinary rule | — | `1905dec42a2a` | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V) |
| `reference-semantics/semantics/builtins.k:90` | ordinary rule | — | `20c0d7b936a1` | rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k> |
| `reference-semantics/semantics/builtins.k:91` | ordinary rule | — | `3f472924a83d` | rule <k> #iterDone ~> #minCont(M:Int) => M ... </k> |
| `reference-semantics/semantics/builtins.k:92` | ordinary rule | — | `71050e22f698` | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) |
| `reference-semantics/semantics/builtins.k:97` | syntax (function) | function | `4282c4747876` | syntax Int ::= maxVals(Int, Vals) [function] |
| `reference-semantics/semantics/builtins.k:98` | ordinary rule | — | `16f482b70cca` | rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST) |
| `reference-semantics/semantics/builtins.k:99` | ordinary rule | — | `fb21a7851f56` | rule maxVals(M:Int, .Vals) => M |
| `reference-semantics/semantics/builtins.k:100` | ordinary rule | — | `f1bf63869c2f` | rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R) |
| `reference-semantics/semantics/builtins.k:102` | syntax (function) | function | `8b1e9d6e3b83` | syntax Int ::= minVals(Int, Vals) [function] |
| `reference-semantics/semantics/builtins.k:103` | ordinary rule | — | `92b52ecacf4f` | rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST) |
| `reference-semantics/semantics/builtins.k:104` | ordinary rule | — | `4daf802c8ea1` | rule minVals(M:Int, .Vals) => M |
| `reference-semantics/semantics/builtins.k:105` | ordinary rule | — | `e2ec20f0d229` | rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) |
| `reference-semantics/semantics/builtins.k:108` | ordinary rule | — | `c62f22bf7149` | rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 // negative operand: the '-' sign prefixes the magnitude's digits |
| `reference-semantics/semantics/builtins.k:111` | ordinary rule | — | `1979f4a341ad` | rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0 |
| `reference-semantics/semantics/builtins.k:114` | syntax (function, total) | function, total | `c616aba4766f` | syntax IntSeq ::= binCodes(Int) [function, total] |
| `reference-semantics/semantics/builtins.k:115` | ordinary rule | — | `4e15dfee6cc6` | rule binCodes(0) => iCons(48, .IntSeq) |
| `reference-semantics/semantics/builtins.k:116` | ordinary rule | — | `7e1227c3ef64` | rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0 |
| `reference-semantics/semantics/builtins.k:117` | syntax (function, total) | function, total | `939453dbc7b8` | syntax IntSeq ::= binAcc(Int, IntSeq) [function, total] |
| `reference-semantics/semantics/builtins.k:118` | ordinary rule | — | `7503c649eb67` | rule binAcc(0, ACC:IntSeq) => ACC |
| `reference-semantics/semantics/builtins.k:119` | ordinary rule | — | `a678c3550525` | rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 |
| `reference-semantics/semantics/builtins.k:124` | ordinary rule | — | `84309128fd26` | rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k> |
| `reference-semantics/semantics/builtins.k:126` | syntax (function, total) | function, total | `aeb5f1496dff` | syntax ValSeq ::= enumVS(ValSeq, Int) [function, total] |
| `reference-semantics/semantics/builtins.k:127` | ordinary rule | — | `4833a908272d` | rule enumVS(.ValSeq, _:Int) => .ValSeq |
| `reference-semantics/semantics/builtins.k:128` | ordinary rule | — | `8e7ccd3c1e3b` | rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) |
| `reference-semantics/semantics/builtins.k:132` | ordinary rule | — | `1ee11e41d66b` | rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k> |
| `reference-semantics/semantics/builtins.k:134` | syntax (function, total) | function, total | `0513f86f41d9` | syntax ValSeq ::= mapStrVS(ValSeq) [function, total] |
| `reference-semantics/semantics/builtins.k:135` | ordinary rule | — | `289c1f881385` | rule mapStrVS(.ValSeq) => .ValSeq |
| `reference-semantics/semantics/builtins.k:136` | ordinary rule | — | `74f471f298ee` | rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R)) |
| `reference-semantics/semantics/builtins.k:137` | ordinary rule | — | `8b0d47ce433f` | rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) |
| `reference-semantics/semantics/builtins.k:140` | ordinary rule | — | `b502e27ccb7e` | rule applyBuiltin("int", I:Int, .Vals) => I |
| `reference-semantics/semantics/builtins.k:143` | ordinary rule | — | `c4bb6edca951` | rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C |
| `reference-semantics/semantics/builtins.k:144` | ordinary rule | — | `a270fa319e95` | rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 |
| `reference-semantics/semantics/builtins.k:148` | ordinary rule | — | `8e899362692d` | rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I))) |
| `reference-semantics/semantics/builtins.k:149` | ordinary rule | — | `948b6cbe0695` | rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) |
| `reference-semantics/semantics/builtins.k:152` | ordinary rule | — | `88e015826cea` | rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 |
| `reference-semantics/semantics/builtins.k:156` | ordinary rule | — | `685720c87ab9` | rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2 |
| `reference-semantics/semantics/builtins.k:158` | syntax (function, total) | function, total | `5400597dd0d2` | syntax Int ::= intDigAcc(IntSeq, Int) [function, total] |
| `reference-semantics/semantics/builtins.k:159` | ordinary rule | — | `0d7d7afcdff4` | rule intDigAcc(.IntSeq, ACC:Int) => ACC |
| `reference-semantics/semantics/builtins.k:160` | ordinary rule | — | `dedabaa457bf` | rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) |
| `reference-semantics/semantics/builtins.k:163` | ordinary rule | — | `d3b8ae0c04fe` | rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B) |
| `reference-semantics/semantics/builtins.k:164` | ordinary rule | — | `278ac52bcbfc` | rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B) |
| `reference-semantics/semantics/builtins.k:167` | ordinary rule | — | `ee54105504d3` | rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k> |
| `reference-semantics/semantics/builtins.k:169` | ordinary rule | — | `db7593d35aaf` | rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k> |
| `reference-semantics/semantics/builtins.k:170` | ordinary rule | — | `84cabfd28956` | rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k> |
| `reference-semantics/semantics/builtins.k:171` | ordinary rule | — | `3123ec683490` | rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k> |
| `reference-semantics/semantics/builtins.k:173` | ordinary rule | — | `221848fbddba` | rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k> |
| `reference-semantics/semantics/builtins.k:174` | ordinary rule | — | `2c19868ffadb` | rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> |
| `reference-semantics/semantics/builtins.k:177` | ordinary rule | — | `4ff496b44fe1` | rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1) |
| `reference-semantics/semantics/builtins.k:178` | ordinary rule | — | `906c5a513bd4` | rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1) |
| `reference-semantics/semantics/builtins.k:179` | ordinary rule | — | `e77f814bf496` | rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 |
| `reference-semantics/semantics/builtins.k:187` | ordinary rule | — | `3115789003f5` | rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS) |
| `reference-semantics/semantics/builtins.k:188` | syntax (function) | function | `ac5c7747453b` | syntax Int ::= evalArith(IntSeq) [function] |
| `reference-semantics/semantics/builtins.k:189` | ordinary rule | — | `51c0c83fdb40` | rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS))))) |
| `reference-semantics/semantics/builtins.k:192` | syntax | — | `82f289aff157` | syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq) |
| `reference-semantics/semantics/builtins.k:194` | syntax (function, total) | function, total | `b174a010e1cc` | syntax Bool ::= evDigit(Int) [function, total] |
| `reference-semantics/semantics/builtins.k:195` | ordinary rule | — | `3e38e9b3918a` | rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57 |
| `reference-semantics/semantics/builtins.k:196` | syntax (function, total) | function, total | `7322fabc33c9` | syntax Bool ::= evHead42(IntSeq) [function, total] |
| `reference-semantics/semantics/builtins.k:197` | ordinary rule | — | `8943c2a4d630` | rule evHead42(iCons(42, _:IntSeq)) => true |
| `reference-semantics/semantics/builtins.k:198` | owise rule | owise | `91cad1617995` | rule evHead42(_:IntSeq) => false [owise] |
| `reference-semantics/semantics/builtins.k:199` | syntax (function, total) | function, total | `0c7954767f99` | syntax Bool ::= evHead47(IntSeq) [function, total] |
| `reference-semantics/semantics/builtins.k:200` | ordinary rule | — | `238e1f40d90a` | rule evHead47(iCons(47, _:IntSeq)) => true |
| `reference-semantics/semantics/builtins.k:201` | owise rule | owise | `fb275676fb19` | rule evHead47(_:IntSeq) => false [owise] |
| `reference-semantics/semantics/builtins.k:203` | syntax (function, total) | function, total | `d6d582239dd5` | syntax OpSeq ::= tokOps(IntSeq) [function, total] |
| `reference-semantics/semantics/builtins.k:204` | ordinary rule | — | `e04fbacffc89` | rule tokOps(.IntSeq) => .OpSeq |
| `reference-semantics/semantics/builtins.k:205` | ordinary rule | — | `9e10fd4dda11` | rule tokOps(iCons(32, R:IntSeq)) => tokOps(R) |
| `reference-semantics/semantics/builtins.k:206` | ordinary rule | — | `584bf3fa5f59` | rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C) |
| `reference-semantics/semantics/builtins.k:207` | ordinary rule | — | `011c9edcd2e8` | rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R)) |
| `reference-semantics/semantics/builtins.k:208` | ordinary rule | — | `d5628edd807e` | rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R) |
| `reference-semantics/semantics/builtins.k:209` | ordinary rule | — | `005eaf8a7dd6` | rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R)) |
| `reference-semantics/semantics/builtins.k:210` | ordinary rule | — | `8111317537ff` | rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R) |
| `reference-semantics/semantics/builtins.k:211` | ordinary rule | — | `85d2d15517e2` | rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R)) |
| `reference-semantics/semantics/builtins.k:212` | ordinary rule | — | `a6a3d20dada5` | rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R)) |
| `reference-semantics/semantics/builtins.k:214` | syntax (function, total) | function, total | `d508522621a8` | syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total] |
| `reference-semantics/semantics/builtins.k:216` | ordinary rule | — | `8c6548026431` | rule tokNds(.IntSeq) => .IntSeq |
| `reference-semantics/semantics/builtins.k:217` | ordinary rule | — | `a6ad609ffead` | rule tokNds(iCons(32, R:IntSeq)) => tokNds(R) |
| `reference-semantics/semantics/builtins.k:218` | ordinary rule | — | `2378510f6563` | rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C) |
| `reference-semantics/semantics/builtins.k:219` | ordinary rule | — | `05eb9aff9741` | rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32 |
| `reference-semantics/semantics/builtins.k:221` | ordinary rule | — | `86cd82351ee8` | rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C) |
| `reference-semantics/semantics/builtins.k:223` | owise rule | owise | `a5f697b9adb7` | rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise] |
| `reference-semantics/semantics/builtins.k:225` | syntax | — | `906d0c17f2fb` | syntax EvPair ::= evp(OpSeq, IntSeq) |
| `reference-semantics/semantics/builtins.k:226` | syntax (function, total) | function, total | `cdf7f8b500cf` | syntax Int ::= firstNdE(EvPair) [function, total] |
| `reference-semantics/semantics/builtins.k:227` | ordinary rule | — | `493a0efa8ace` | rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N |
| `reference-semantics/semantics/builtins.k:228` | owise rule | owise | `99460cf0fcab` | rule firstNdE(_:EvPair) => 0 [owise] |
| `reference-semantics/semantics/builtins.k:230` | syntax (function, total) | function, total | `f15a46d2a884` | syntax Int ::= applyOpE(String, Int, Int) [function, total] |
| `reference-semantics/semantics/builtins.k:231` | ordinary rule | — | `e87c23f5d28b` | rule applyOpE("+", A:Int, B:Int) => A +Int B |
| `reference-semantics/semantics/builtins.k:232` | ordinary rule | — | `d26a9d3a522a` | rule applyOpE("-", A:Int, B:Int) => A -Int B |
| `reference-semantics/semantics/builtins.k:233` | ordinary rule | — | `d27c36510a59` | rule applyOpE("*", A:Int, B:Int) => A *Int B |
| `reference-semantics/semantics/builtins.k:234` | ordinary rule | — | `fe469f129f99` | rule applyOpE("//", A:Int, B:Int) => A divInt B |
| `reference-semantics/semantics/builtins.k:235` | ordinary rule | — | `45890407b049` | rule applyOpE("**", A:Int, B:Int) => A ^Int B |
| `reference-semantics/semantics/builtins.k:236` | owise rule | owise | `77542379cedb` | rule applyOpE(_:String, A:Int, _:Int) => A [owise] |
| `reference-semantics/semantics/builtins.k:238` | syntax (function, total) | function, total | `7039540535a2` | syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/builtins.k:239` | ordinary rule | — | `337779ec3207` | rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS) |
| `reference-semantics/semantics/builtins.k:240` | ordinary rule | — | `cfc7aaf38685` | rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS)) |
| `reference-semantics/semantics/builtins.k:241` | ordinary rule | — | `2ba5f008db68` | rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**" |
| `reference-semantics/semantics/builtins.k:243` | owise rule | owise | `25a4663fe177` | rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise] |
| `reference-semantics/semantics/builtins.k:244` | syntax (function, total) | function, total | `6a975303e128` | syntax EvPair ::= powCombE(Int, EvPair) [function, total] |
| `reference-semantics/semantics/builtins.k:245` | ordinary rule | — | `b0fe3350706d` | rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST)) |
| `reference-semantics/semantics/builtins.k:246` | ordinary rule | — | `2474e1e106b7` | rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq)) |
| `reference-semantics/semantics/builtins.k:247` | syntax (function, total) | function, total | `ccb2ec4ebb2f` | syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total] |
| `reference-semantics/semantics/builtins.k:248` | ordinary rule | — | `1b1d231b33e5` | rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS)) |
| `reference-semantics/semantics/builtins.k:250` | syntax (function, total) | function, total | `b236e49f85be` | syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total] |
| `reference-semantics/semantics/builtins.k:251` | ordinary rule | — | `e5919eeb7c7e` | rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq) |
| `reference-semantics/semantics/builtins.k:252` | ordinary rule | — | `6b1d3c71e798` | rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq) |
| `reference-semantics/semantics/builtins.k:253` | ordinary rule | — | `c3f2a5ab71fe` | rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq) |
| `reference-semantics/semantics/builtins.k:254` | ordinary rule | — | `8842e532de29` | rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq) |
| `reference-semantics/semantics/builtins.k:255` | syntax (function, total) | function, total | `3b8c247c3782` | syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/builtins.k:256` | ordinary rule | — | `1232a86fdb86` | rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) |
| `reference-semantics/semantics/builtins.k:257` | ordinary rule | — | `b050e168b90f` | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O) |
| `reference-semantics/semantics/builtins.k:260` | ordinary rule | — | `453fc29790b1` | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O) |
| `reference-semantics/semantics/builtins.k:263` | owise rule | owise | `bd2ed20b94e7` | rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise] |
| `reference-semantics/semantics/builtins.k:265` | syntax (function, total) | function, total | `241368398e21` | syntax Bool ::= inLevelE(String, String) [function, total] |
| `reference-semantics/semantics/builtins.k:266` | ordinary rule | — | `55734e1ee045` | rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/" |
| `reference-semantics/semantics/builtins.k:267` | ordinary rule | — | `d4ca4934e9e1` | rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-" |
| `reference-semantics/semantics/builtins.k:268` | owise rule | owise | `7c8e03ff739b` | rule inLevelE(_:String, _:String) => false [owise] |
| `reference-semantics/semantics/builtins.k:269` | syntax (function, total) | function, total | `b9870a621ad1` | syntax OpSeq ::= appendOpE(OpSeq, String) [function, total] |
| `reference-semantics/semantics/builtins.k:270` | ordinary rule | — | `7a7e56f73880` | rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq) |
| `reference-semantics/semantics/builtins.k:271` | ordinary rule | — | `d0623558f5e8` | rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O)) |
| `reference-semantics/semantics/builtins.k:272` | syntax (function, total) | function, total | `5895024c900e` | syntax IntSeq ::= appendIE(IntSeq, Int) [function, total] |
| `reference-semantics/semantics/builtins.k:273` | ordinary rule | — | `0a8e13361178` | rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq) |
| `reference-semantics/semantics/builtins.k:274` | ordinary rule | — | `2c035f9af86e` | rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) |
| `reference-semantics/semantics/builtins.k:279` | syntax | — | `daf634ba2a45` | syntax KItem ::= "#md5" |
| `reference-semantics/semantics/builtins.k:280` | priority rule | priority(40) | `1651b5d13893` | rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)] |
| `reference-semantics/semantics/builtins.k:282` | ordinary rule | — | `3dea3e5b7893` | rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k> |
| `reference-semantics/semantics/builtins.k:283` | syntax | — | `697d07fdfb43` | syntax Val ::= md5Obj(IntSeq) |
| `reference-semantics/semantics/builtins.k:284` | ordinary rule | — | `314edc78f759` | rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS)) |
| `reference-semantics/semantics/builtins.k:285` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(md5hexCodes), total | `a3cdf84d6e5d` | syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] |
| `reference-semantics/semantics/builtins.k:291` | ordinary rule | — | `89ae05ae7446` | rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V) |
| `reference-semantics/semantics/builtins.k:292` | ordinary rule | — | `42f642e09611` | rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V) |
| `reference-semantics/semantics/builtins.k:293` | syntax (function) | function | `09de746af4b8` | syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function] |
| `reference-semantics/semantics/builtins.k:294` | ordinary rule | — | `999a8165286d` | rule isIntV(_:Int) => true |
| `reference-semantics/semantics/builtins.k:295` | owise rule | owise | `fa24b2641774` | rule isIntV(_:Val) => false [owise] |
| `reference-semantics/semantics/builtins.k:296` | ordinary rule | — | `d3c0ce1552b2` | rule isStrV(str(_:IntSeq)) => true |
| `reference-semantics/semantics/builtins.k:297` | owise rule | owise | `c79400091783` | rule isStrV(_:Val) => false [owise] |
| `reference-semantics/semantics/call.k:16` | ordinary rule | — | `d87ce6dbcf15` | rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> |
| `reference-semantics/semantics/call.k:19` | syntax | — | `2e4b9931b31d` | syntax KItem ::= #callee(Exprs) |
| `reference-semantics/semantics/call.k:20` | owise rule | owise | `1e7cf6c3f022` | rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise] |
| `reference-semantics/semantics/call.k:21` | ordinary rule | — | `d344c79af57e` | rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> |
| `reference-semantics/semantics/call.k:24` | ordinary rule | — | `ba0da2a7daa0` | rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k> |
| `reference-semantics/semantics/call.k:26` | ordinary rule | — | `9355577d2cbe` | rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k> |
| `reference-semantics/semantics/call.k:27` | ordinary rule | — | `c61154d49e9b` | rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k> |
| `reference-semantics/semantics/call.k:28` | ordinary rule | — | `c6499b637357` | rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k> |
| `reference-semantics/semantics/call.k:29` | ordinary rule | — | `c477beb1100e` | rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k> |
| `reference-semantics/semantics/call.k:30` | ordinary rule | — | `c299129ec675` | rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k> |
| `reference-semantics/semantics/call.k:31` | owise rule | owise | `6240ee6cdac4` | rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise] |
| `reference-semantics/semantics/call.k:32` | ordinary rule | — | `785722624d9c` | rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k> |
| `reference-semantics/semantics/call.k:38` | priority rule | priority(40) | `ee3d87d37701` | rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/call.k:42` | priority rule | priority(40) | `5cfcef8958d3` | rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)] |
| `reference-semantics/semantics/call.k:47` | priority rule | priority(40) | `fd42ded76cba` | rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/call.k:52` | syntax (function, total) | function, total | `d5c2626ac8a7` | syntax Bool ::= isMutMethod(String) [function, total] |
| `reference-semantics/semantics/call.k:53` | ordinary rule | — | `1d9f03fc012d` | rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove" |
| `reference-semantics/semantics/call.k:56` | priority rule | priority(40) | `3c518e910de9` | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] // non-mutating methods READ their heap-object arguments too (join's list); // mutators keep refs (append of a list into a list-of-lists stays aliased) |
| `reference-semantics/semantics/call.k:63` | priority rule | priority(40) | `187b119fad38` | rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)] |
| `reference-semantics/semantics/call.k:69` | ordinary rule | — | `d13afd9793ea` | rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> |
| `reference-semantics/semantics/call.k:80` | ordinary rule | — | `dfda7a0ca530` | rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> |
| `reference-semantics/semantics/call.k:87` | syntax | — | `66b816d7dbbc` | syntax KItem ::= #allocCells(ParamNames) |
| `reference-semantics/semantics/call.k:88` | ordinary rule | — | `ab5f4beee335` | rule <k> #allocCells(.ParamNames) => .K ... </k> |
| `reference-semantics/semantics/call.k:89` | ordinary rule | — | `fafea1ce5a10` | rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) |
| `reference-semantics/semantics/comprehension.k:11` | ordinary rule | — | `4645372e277c` | rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| `reference-semantics/semantics/comprehension.k:12` | ordinary rule | — | `a3878283cbe8` | rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| `reference-semantics/semantics/comprehension.k:14` | syntax (macro) | macro | `824d607beedb` | syntax Stmts ::= compBody(CompFors, Expr) [macro] |
| `reference-semantics/semantics/comprehension.k:15` | ordinary rule | — | `5c4c897cdd72` | rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc")) |
| `reference-semantics/semantics/comprehension.k:18` | syntax (macro-rec) | macro-rec | `7d588d134f4b` | syntax Stmt ::= compNest(CompFors, Expr) [macro-rec] |
| `reference-semantics/semantics/comprehension.k:19` | ordinary rule | — | `57c2e26708be` | rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT))) |
| `reference-semantics/semantics/comprehension.k:21` | ordinary rule | — | `6e48579ec017` | rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts)) |
| `reference-semantics/semantics/comprehension.k:24` | syntax (macro) | macro | `2ecdbee509dd` | syntax Expr ::= compGuard(Exprs) [macro] |
| `reference-semantics/semantics/comprehension.k:25` | ordinary rule | — | `17ed18454df9` | rule compGuard(.Exprs) => Bool(true) |
| `reference-semantics/semantics/comprehension.k:26` | ordinary rule | — | `93505f664b89` | rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs)) |
| `reference-semantics/semantics/concrete.k:13` | ordinary rule | — | `5b920898a921` | rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) |
| `reference-semantics/semantics/concrete.k:16` | ordinary rule | — | `8c37deda0f97` | rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) |
| `reference-semantics/semantics/concrete.k:25` | syntax | — | `2a9016918418` | syntax Val ::= kvP(Val, Val) |
| `reference-semantics/semantics/concrete.k:26` | syntax | — | `c81660cf2ded` | syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool) |
| `reference-semantics/semantics/concrete.k:28` | priority rule | priority(40) | `69542fb8e543` | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)] |
| `reference-semantics/semantics/concrete.k:31` | priority rule | priority(40) | `00feff65cbca` | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)] |
| `reference-semantics/semantics/concrete.k:34` | ordinary rule | — | `14b845c8db97` | rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k> |
| `reference-semantics/semantics/concrete.k:36` | ordinary rule | — | `fb87dc6e2e9f` | rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k> |
| `reference-semantics/semantics/concrete.k:38` | ordinary rule | — | `110222299ad8` | rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K) |
| `reference-semantics/semantics/concrete.k:42` | syntax (function) | function | `55dc07274299` | syntax ValSeq ::= insPair(ValSeq, Val, Val) [function] |
| `reference-semantics/semantics/concrete.k:43` | ordinary rule | — | `1b9c47e83939` | rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq) |
| `reference-semantics/semantics/concrete.k:44` | ordinary rule | — | `041af2698561` | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2) |
| `reference-semantics/semantics/concrete.k:47` | ordinary rule | — | `0be272f2ab85` | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2) |
| `reference-semantics/semantics/concrete.k:51` | syntax (function) | function | `a74ccb7aaf4f` | syntax Bool ::= kLt(Val, Val) [function] |
| `reference-semantics/semantics/concrete.k:52` | ordinary rule | — | `fbdc0f5eaf8a` | rule kLt(I1:Int, I2:Int) => I1 <Int I2 |
| `reference-semantics/semantics/concrete.k:53` | ordinary rule | — | `b5c575a5cf71` | rule kLt(F1:Float, F2:Float) => F1 <Float F2 |
| `reference-semantics/semantics/concrete.k:54` | ordinary rule | — | `608ffd1665ed` | rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B) |
| `reference-semantics/semantics/concrete.k:56` | syntax (function, total) | function, total | `4f9bc29fa28a` | syntax ValSeq ::= unpairVS(ValSeq) [function, total] |
| `reference-semantics/semantics/concrete.k:57` | ordinary rule | — | `a2e6dd066c67` | rule unpairVS(.ValSeq) => .ValSeq |
| `reference-semantics/semantics/concrete.k:58` | ordinary rule | — | `84d1ae0473a1` | rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R)) |
| `reference-semantics/semantics/concrete.k:59` | owise rule | owise | `7ae54fdad398` | rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise] |
| `reference-semantics/semantics/controls.k:9` | ordinary rule | — | `727336c6ee2c` | rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes> |
| `reference-semantics/semantics/controls.k:12` | priority rule | priority(40) | `86f7726c7fa4` | rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)] |
| `reference-semantics/semantics/controls.k:20` | ordinary rule | — | `f7b414275b72` | rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route // the ref case through BinOp so the deref + list-concat +... |
| `reference-semantics/semantics/controls.k:27` | priority rule | priority(40) | `2136b0846a30` | rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] |
| `reference-semantics/semantics/controls.k:35` | ordinary rule | — | `f402a7269397` | rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k> |
| `reference-semantics/semantics/controls.k:36` | owise rule | owise | `52700f6597b2` | rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise] |
| `reference-semantics/semantics/controls.k:37` | syntax | — | `88b5590c6cf0` | syntax KItem ::= #bindImports(ParamNames) |
| `reference-semantics/semantics/controls.k:38` | ordinary rule | — | `775670eae46f` | rule <k> #bindImports(.ParamNames) => .K ... </k> |
| `reference-semantics/semantics/controls.k:39` | ordinary rule | — | `72a0209aaedb` | rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil" |
| `reference-semantics/semantics/controls.k:43` | ordinary rule | — | `7c9973fe6a17` | rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") |
| `reference-semantics/semantics/controls.k:48` | ordinary rule | — | `eb3ba2f76867` | rule <k> Expr(_:Val) => .K ... </k> |
| `reference-semantics/semantics/controls.k:51` | syntax | — | `7b0fe50a6219` | syntax KItem ::= #branch(Bool, Stmts, Stmts) |
| `reference-semantics/semantics/controls.k:52` | ordinary rule | — | `cbe0a65ca8b4` | rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k> |
| `reference-semantics/semantics/controls.k:53` | ordinary rule | — | `5e1b96eb480c` | rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k> |
| `reference-semantics/semantics/controls.k:54` | ordinary rule | — | `ff7557d947a0` | rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> |
| `reference-semantics/semantics/controls.k:57` | ordinary rule | — | `ac20784b5ae4` | rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V) |
| `reference-semantics/semantics/controls.k:59` | ordinary rule | — | `5d0d142ae8ef` | rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) |
| `reference-semantics/semantics/controls.k:65` | syntax | — | `d3eeb935e6cc` | syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk" |
| `reference-semantics/semantics/controls.k:69` | ordinary rule | — | `54e2c3c93eb9` | rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k> |
| `reference-semantics/semantics/controls.k:71` | ordinary rule | — | `f6431203e70c` | rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k> |
| `reference-semantics/semantics/controls.k:72` | ordinary rule | — | `e22f89d510cf` | rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k> |
| `reference-semantics/semantics/controls.k:73` | ordinary rule | — | `b48dd2a1b470` | rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> |
| `reference-semantics/semantics/controls.k:77` | ordinary rule | — | `cc778d0a7dee` | rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k> |
| `reference-semantics/semantics/controls.k:78` | ordinary rule | — | `6b4a239ea016` | rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k> |
| `reference-semantics/semantics/controls.k:79` | ordinary rule | — | `4d0735d2af74` | rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V) |
| `reference-semantics/semantics/controls.k:81` | ordinary rule | — | `1fd277da3d41` | rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) |
| `reference-semantics/semantics/controls.k:85` | ordinary rule | — | `bb87d59b209a` | rule <k> #loopLbl(NEXT:K) => NEXT ... </k> |
| `reference-semantics/semantics/controls.k:86` | ordinary rule | — | `7987cb734506` | rule <k> Continue => #cont ... </k> |
| `reference-semantics/semantics/controls.k:87` | ordinary rule | — | `0c6690a88f1d` | rule <k> Break => #brk ... </k> |
| `reference-semantics/semantics/controls.k:88` | ordinary rule | — | `8617466b0146` | rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k> |
| `reference-semantics/semantics/controls.k:89` | owise rule | owise | `5cabf37fa715` | rule <k> #cont ~> (_:KItem => .K) ... </k> [owise] |
| `reference-semantics/semantics/controls.k:90` | ordinary rule | — | `5b9a5f06df03` | rule <k> #brk ~> #loopLbl(_:K) => .K ... </k> |
| `reference-semantics/semantics/controls.k:91` | owise rule | owise | `0b85dbffe432` | rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] |
| `reference-semantics/semantics/controls.k:95` | priority rule | priority(40) | `aebf4530a7ab` | rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/controls.k:98` | priority rule | priority(40) | `c18a31f5ea1d` | rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/controls.k:101` | priority rule | priority(40) | `a6ee60705325` | rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // For derefs its iterable ONCE at loop start (iteration is over the snapshot; // mutating the iterated list inside its own loop is outside the subset) |
| `reference-semantics/semantics/controls.k:106` | priority rule | priority(40) | `f3e64e39e89e` | rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/core.k:13` | syntax | — | `2768b2d6c3a1` | syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq) |
| `reference-semantics/semantics/core.k:14` | syntax | — | `3571b0fa24f6` | syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq) |
| `reference-semantics/semantics/core.k:15` | syntax | — | `7992f5935fe5` | syntax Str ::= str(IntSeq) |
| `reference-semantics/semantics/core.k:18` | syntax | — | `95c276903d0f` | syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq) |
| `reference-semantics/semantics/core.k:25` | syntax | — | `5093ac288834` | syntax Val ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) // a heap object: <heap> holds its list(VS) \| cellRef(Int) // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) // a type object (int/str), resolved from the builtins frame \| builtinV(String) // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String) // a cooled Attribute: obj.method |
| `reference-semantics/semantics/core.k:36` | syntax | — | `c883cd56f6e6` | syntax Parent ::= "root" \| parent(Int) |
| `reference-semantics/semantics/core.k:37` | syntax | — | `364e84e4303e` | syntax Scope ::= scope(Map, Parent) |
| `reference-semantics/semantics/core.k:38` | syntax | — | `48fc3fcf1882` | syntax KResult ::= Val |
| `reference-semantics/semantics/core.k:39` | syntax | — | `af287dc638f3` | syntax Expr ::= Val // cooling puts results back into expression holes |
| `reference-semantics/semantics/core.k:40` | syntax | — | `2db74932694d` | syntax Vals ::= List{Val, ","} |
| `reference-semantics/semantics/core.k:41` | syntax | — | `f742989919fe` | syntax Exc ::= "NoExc" \| "AssertionError" |
| `reference-semantics/semantics/core.k:42` | syntax | — | `de0c80b21d8e` | syntax RetState ::= "noRet" \| retV(Val) |
| `reference-semantics/semantics/core.k:49` | configuration | — | `c36112c4d400` | configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code> |
| `reference-semantics/semantics/core.k:68` | syntax (function, total) | function, total | `3338ad77ca00` | syntax Bool ::= isRefV(Val) [function, total] |
| `reference-semantics/semantics/core.k:69` | ordinary rule | — | `d1ee5822bc20` | rule isRefV(ref(_:Int)) => true |
| `reference-semantics/semantics/core.k:70` | owise rule | owise | `509a5d07077c` | rule isRefV(_:Val) => false [owise] |
| `reference-semantics/semantics/core.k:75` | syntax | — | `21cd98225d72` | syntax HeapVal ::= cellV(Val) |
| `reference-semantics/semantics/core.k:76` | syntax (function, total) | function, total | `a9d42f86eb00` | syntax Bool ::= isCellRef(Val) [function, total] |
| `reference-semantics/semantics/core.k:77` | ordinary rule | — | `d10f04444db1` | rule isCellRef(cellRef(_:Int)) => true |
| `reference-semantics/semantics/core.k:78` | owise rule | owise | `a851114a10aa` | rule isCellRef(_:Val) => false [owise] // k-top deref for cell-bound reads surfacing INSIDE the annotated frame // (AugAssign's in-place read and friends). The "$cells" guard keeps this // DECIDABLY inapplicable in plain frames — an unguarded rule lets the // prover narrow abstract k-top values into cellRef junk (probed on // 26-remove-duplicates). Cross-frame reads (a comprehension closure // reading the enclosing function's cellvar) deref inside #look... |
| `reference-semantics/semantics/core.k:85` | priority rule | priority(40) | `bb55d5bd659f` | rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] |
| `reference-semantics/semantics/core.k:95` | syntax | — | `746e63785a2a` | syntax Val ::= kwV(String, Val) |
| `reference-semantics/semantics/core.k:96` | syntax | — | `7135e0a28684` | syntax KItem ::= #kwTag(String) |
| `reference-semantics/semantics/core.k:97` | ordinary rule | — | `28d46dc1bd55` | rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k> |
| `reference-semantics/semantics/core.k:98` | ordinary rule | — | `13f6503b1865` | rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V) |
| `reference-semantics/semantics/core.k:100` | syntax (function, total) | function, total | `50eabe9c99f3` | syntax Bool ::= isKwV(Val) [function, total] |
| `reference-semantics/semantics/core.k:101` | ordinary rule | — | `a1fa116710bd` | rule isKwV(kwV(_:String, _:Val)) => true |
| `reference-semantics/semantics/core.k:102` | owise rule | owise | `08aa624873dd` | rule isKwV(_:Val) => false [owise] |
| `reference-semantics/semantics/core.k:106` | syntax | — | `2285105441dc` | syntax Val ::= cellsMark(ParamNames) |
| `reference-semantics/semantics/core.k:107` | syntax (function) | function | `ad2441054e7f` | syntax ParamNames ::= cellsOf(Val) [function] |
| `reference-semantics/semantics/core.k:108` | ordinary rule | — | `dadd75df5321` | rule cellsOf(cellsMark(CVS:ParamNames)) => CVS |
| `reference-semantics/semantics/core.k:109` | syntax (function, total) | function, total | `009b993788c2` | syntax Bool ::= pnMember(String, ParamNames) [function, total] |
| `reference-semantics/semantics/core.k:110` | ordinary rule | — | `09cb69784187` | rule pnMember(_:String, .ParamNames) => false |
| `reference-semantics/semantics/core.k:111` | ordinary rule | — | `40d3ebcbac2e` | rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R) |
| `reference-semantics/semantics/core.k:113` | syntax | — | `16af91ae2538` | syntax KItem ::= #cellW(Val, Val) |
| `reference-semantics/semantics/core.k:114` | ordinary rule | — | `23d2c2b6c8f3` | rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap> |
| `reference-semantics/semantics/core.k:117` | syntax | — | `584583182d33` | syntax KItem ::= #alloc(Val) |
| `reference-semantics/semantics/core.k:118` | ordinary rule | — | `956c073b6b4a` | rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) |
| `reference-semantics/semantics/core.k:124` | syntax | — | `40d32b5e1ad1` | syntax KItem ::= #loadAll(Module) |
| `reference-semantics/semantics/core.k:125` | ordinary rule | — | `831765b43e68` | rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k> |
| `reference-semantics/semantics/core.k:126` | ordinary rule | — | `622f8afd4910` | rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k> |
| `reference-semantics/semantics/core.k:127` | ordinary rule | — | `913b04bec3e9` | rule <k> .Stmts => .K ... </k> |
| `reference-semantics/semantics/core.k:130` | syntax | — | `68e17b99a979` | syntax KItem ::= #look(String, Int) |
| `reference-semantics/semantics/core.k:131` | ordinary rule | — | `4dffd7efda70` | rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env> |
| `reference-semantics/semantics/core.k:132` | ordinary rule | — | `e184a5f152d0` | rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE // LOOKUP (higher priority beats the plain return above on concrete cell // bindings; abstract claim values take the plain rule unchanged) — this // covers cross-frame cell reads (a comprehension closure reading the // enclosing function's cellvar) wit... |
| `reference-semantics/semantics/core.k:145` | priority rule | priority(40) | `d28eff3f5eef` | rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)] |
| `reference-semantics/semantics/core.k:152` | ordinary rule | — | `64d6895b653b` | rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) |
| `reference-semantics/semantics/core.k:157` | syntax (function, total) | function, total | `9b3d6c932d97` | syntax Scope ::= "builtinsScope" [function, total] |
| `reference-semantics/semantics/core.k:158` | ordinary rule | — | `c19d041e322e` | rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorte... |
| `reference-semantics/semantics/core.k:185` | syntax | — | `0cd464bb92d6` | syntax ApplyK ::= toCall(Val) |
| `reference-semantics/semantics/core.k:186` | syntax | — | `c232da225c21` | syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals) |
| `reference-semantics/semantics/core.k:189` | ordinary rule | — | `e7135690e726` | rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k> |
| `reference-semantics/semantics/core.k:190` | ordinary rule | — | `aee090561fe2` | rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k> |
| `reference-semantics/semantics/core.k:191` | ordinary rule | — | `970d561c7f9c` | rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> |
| `reference-semantics/semantics/core.k:194` | ordinary rule | — | `818c9ba8a73e` | rule <k> Int(I:Int) => I ... </k> |
| `reference-semantics/semantics/core.k:195` | ordinary rule | — | `28c8aac589eb` | rule <k> Bool(B:Bool) => B ... </k> |
| `reference-semantics/semantics/core.k:196` | ordinary rule | — | `95e9086b296e` | rule <k> NoneVal => noneV ... </k> |
| `reference-semantics/semantics/core.k:199` | syntax (function) | function | `c70b8b2eac36` | syntax Bool ::= truthy(Val) [function] |
| `reference-semantics/semantics/core.k:200` | ordinary rule | — | `7df2db27abe2` | rule truthy(B:Bool) => B |
| `reference-semantics/semantics/core.k:201` | ordinary rule | — | `2154ca8be6a6` | rule truthy(noneV) => false |
| `reference-semantics/semantics/core.k:202` | ordinary rule | — | `1b473f752373` | rule truthy(I:Int) => I =/=Int 0 |
| `reference-semantics/semantics/core.k:203` | ordinary rule | — | `a91f771de331` | rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq) |
| `reference-semantics/semantics/core.k:204` | ordinary rule | — | `3f5155710300` | rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq) |
| `reference-semantics/semantics/core.k:205` | ordinary rule | — | `1660cb202632` | rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) |
| `reference-semantics/semantics/core.k:208` | syntax (function) | function | `033e06a0df36` | syntax Val ::= applyUn(String, Val) [function] |
| `reference-semantics/semantics/core.k:209` | syntax (function) | function | `c8b918102a85` | syntax Val ::= applyBin(String, Val, Val) [function] |
| `reference-semantics/semantics/core.k:210` | syntax (function) | function | `da44e152afa8` | syntax Bool ::= applyCmp(String, Val, Val) [function] |
| `reference-semantics/semantics/core.k:213` | syntax (function, total) | function, total | `763cc5fd6e1a` | syntax Vals ::= appendVal(Vals, Val) [function, total] |
| `reference-semantics/semantics/core.k:214` | ordinary rule | — | `4114893ecb98` | rule appendVal(.Vals, V:Val) => V , .Vals |
| `reference-semantics/semantics/core.k:215` | ordinary rule | — | `32c06da8db7c` | rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V) |
| `reference-semantics/semantics/core.k:217` | syntax (function, total) | function, total | `7a97605e841a` | syntax ValSeq ::= vals2valSeq(Vals) [function, total] |
| `reference-semantics/semantics/core.k:218` | ordinary rule | — | `24991725fdf9` | rule vals2valSeq(.Vals) => .ValSeq |
| `reference-semantics/semantics/core.k:219` | ordinary rule | — | `e9fb82f13f27` | rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) |
| `reference-semantics/semantics/core.k:223` | syntax (function, total) | function, total | `dd74bc995871` | syntax Int ::= vsLen(ValSeq) [function, total] |
| `reference-semantics/semantics/core.k:224` | ordinary rule | — | `c4769d54f3a0` | rule vsLen(.ValSeq) => 0 |
| `reference-semantics/semantics/core.k:225` | ordinary rule | — | `c1a7ece33229` | rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S) |
| `reference-semantics/semantics/core.k:227` | syntax (function, total) | function, total | `cefb7744efac` | syntax Int ::= isLen(IntSeq) [function, total] |
| `reference-semantics/semantics/core.k:228` | ordinary rule | — | `4447a9050e81` | rule isLen(.IntSeq) => 0 |
| `reference-semantics/semantics/core.k:229` | ordinary rule | — | `71e04135edd8` | rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) |
| `reference-semantics/semantics/core.k:233` | syntax (function, total) | function, total | `912ccb9ff6dc` | syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total] |
| `reference-semantics/semantics/core.k:234` | ordinary rule | — | `1e6118f46d4f` | rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq |
| `reference-semantics/semantics/core.k:235` | ordinary rule | — | `41d35046504f` | rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S) |
| `reference-semantics/semantics/core.k:236` | ordinary rule | — | `915d44202de0` | rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0 |
| `reference-semantics/semantics/core.k:238` | ordinary rule | — | `8935316ee314` | rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0 |
| `reference-semantics/semantics/dict.k:20` | syntax | — | `6df725675f7a` | syntax Val ::= dictV(ValSeq, ValSeq) |
| `reference-semantics/semantics/dict.k:23` | syntax | — | `64f4d467c14c` | syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq) |
| `reference-semantics/semantics/dict.k:26` | ordinary rule | — | `338fc50af3ec` | rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k> |
| `reference-semantics/semantics/dict.k:27` | ordinary rule | — | `f86750e273ef` | rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k> |
| `reference-semantics/semantics/dict.k:28` | ordinary rule | — | `9f430a15316b` | rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k> |
| `reference-semantics/semantics/dict.k:30` | ordinary rule | — | `a93b464aec89` | rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k> |
| `reference-semantics/semantics/dict.k:32` | ordinary rule | — | `3dfb5e8b9a85` | rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> |
| `reference-semantics/semantics/dict.k:37` | syntax (function, total) | function, total | `b1e4066d0d4a` | syntax Bool ::= dHasKey(ValSeq, Val) [function, total] |
| `reference-semantics/semantics/dict.k:38` | ordinary rule | — | `f3d38f90b6d2` | rule dHasKey(.ValSeq, _:Val) => false |
| `reference-semantics/semantics/dict.k:39` | ordinary rule | — | `eabe6c23e459` | rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K |
| `reference-semantics/semantics/dict.k:40` | ordinary rule | — | `d5e79e57f442` | rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) |
| `reference-semantics/semantics/dict.k:43` | syntax (function, total) | function, total | `97a166c788d6` | syntax ValSeq ::= dPutK(ValSeq, Val) [function, total] |
| `reference-semantics/semantics/dict.k:44` | ordinary rule | — | `f36012828a09` | rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K) |
| `reference-semantics/semantics/dict.k:45` | ordinary rule | — | `e529b1885d79` | rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) |
| `reference-semantics/semantics/dict.k:49` | syntax (function, total) | function, total | `a03444397cd8` | syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total] |
| `reference-semantics/semantics/dict.k:50` | ordinary rule | — | `d9941fcd2342` | rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K |
| `reference-semantics/semantics/dict.k:52` | ordinary rule | — | `a4c617d1ea5d` | rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K) |
| `reference-semantics/semantics/dict.k:54` | owise rule | owise | `23c2d76a5bb2` | rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] |
| `reference-semantics/semantics/dict.k:58` | priority rule | priority(40) | `52ba35e3f3e1` | rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] |
| `reference-semantics/semantics/dict.k:63` | ordinary rule | — | `2e626ca3a0e5` | rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K) |
| `reference-semantics/semantics/dict.k:64` | syntax (function) | function | `391e4efc5555` | syntax Val ::= applyIndexD(Val, Val) [function] |
| `reference-semantics/semantics/dict.k:65` | priority rule | priority(45) | `cb2b7811a295` | rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] |
| `reference-semantics/semantics/dict.k:70` | syntax (function) | function | `31f3f6e36c10` | syntax Val ::= dictSet(Val, Val, Val) [function] |
| `reference-semantics/semantics/dict.k:71` | ordinary rule | — | `fe76006a41db` | rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) |
| `reference-semantics/semantics/dict.k:76` | syntax | — | `882d796d0a94` | syntax KItem ::= #dsetK(String, Val) |
| `reference-semantics/semantics/dict.k:77` | ordinary rule | — | `4bbcefc7ea06` | rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k> |
| `reference-semantics/semantics/dict.k:78` | ordinary rule | — | `883ae84d25cd` | rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val) |
| `reference-semantics/semantics/dict.k:82` | ordinary rule | — | `1174d6494b10` | rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) |
| `reference-semantics/semantics/dict.k:86` | syntax | — | `cfa9005e176e` | syntax KItem ::= #dsetV(Val, Val, Val) |
| `reference-semantics/semantics/dict.k:87` | ordinary rule | — | `0585a796d9ac` | rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> // negative-index normalization local to the write (subscript.k's is not imported here) |
| `reference-semantics/semantics/dict.k:90` | syntax (function, total) | function, total | `1c5323bfd95c` | syntax Int ::= normIdxD(Int, Int) [function, total] |
| `reference-semantics/semantics/dict.k:91` | ordinary rule | — | `0abef29e8f8d` | rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0 |
| `reference-semantics/semantics/dict.k:92` | ordinary rule | — | `91d01ee2adec` | rule normIdxD(I:Int, _:Int) => I requires I >=Int 0 |
| `reference-semantics/semantics/dict.k:95` | ordinary rule | — | `79a01618ecfd` | rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2) |
| `reference-semantics/semantics/dict.k:97` | syntax (function) | function | `24fc648b5bc5` | syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function] |
| `reference-semantics/semantics/dict.k:98` | ordinary rule | — | `38e9c64805ad` | rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true |
| `reference-semantics/semantics/dict.k:99` | ordinary rule | — | `673f8778545f` | rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2) |
| `reference-semantics/semantics/dict.k:101` | syntax (function) | function | `10fc860d42b9` | syntax Val ::= dGet(ValSeq, ValSeq, Val) [function] |
| `reference-semantics/semantics/dict.k:102` | ordinary rule | — | `acfc6ddc0886` | rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K |
| `reference-semantics/semantics/dict.k:103` | ordinary rule | — | `6971aef40103` | rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K) |
| `reference-semantics/semantics/float.k:20` | syntax | — | `f206c1a5ca92` | syntax Val ::= Float |
| `reference-semantics/semantics/float.k:21` | ordinary rule | — | `958c3574357c` | rule <k> Float(F:Float) => F ... </k> |
| `reference-semantics/semantics/float.k:24` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(intFloatDiv), total | `f4862b43f760` | syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators] |
| `reference-semantics/semantics/float.k:25` | concrete rule | concrete | `be877732fabb` | rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete] |
| `reference-semantics/semantics/float.k:27` | ordinary rule | — | `ad4088a17a28` | rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) |
| `reference-semantics/semantics/float.k:30` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(divII), total | `3c7cef5fcc77` | syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators] |
| `reference-semantics/semantics/float.k:31` | concrete rule | concrete | `111c0e226da2` | rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete] |
| `reference-semantics/semantics/float.k:32` | ordinary rule | — | `4f674380fdd4` | rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) |
| `reference-semantics/semantics/float.k:37` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(floatMod), total | `26237ef2edca` | syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators] |
| `reference-semantics/semantics/float.k:38` | concrete rule | concrete | `f0f814d6f918` | rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete] |
| `reference-semantics/semantics/float.k:39` | ordinary rule | — | `b992bea3c102` | rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) |
| `reference-semantics/semantics/float.k:43` | ordinary rule | — | `ce568cc9c8ae` | rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2 |
| `reference-semantics/semantics/float.k:44` | ordinary rule | — | `08c0b0dbc97f` | rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) |
| `reference-semantics/semantics/float.k:50` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(floatLt), total | `9675cd9c7a22` | syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators] |
| `reference-semantics/semantics/float.k:51` | concrete rule | concrete | `2a8121a4d91f` | rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete] |
| `reference-semantics/semantics/float.k:52` | ordinary rule | — | `c073d8cee697` | rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2) |
| `reference-semantics/semantics/float.k:54` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(absF), total | `12a1faf44cdf` | syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators] |
| `reference-semantics/semantics/float.k:55` | concrete rule | concrete | `b00b8066b8e9` | rule absF(F:Float) => absFloat(F) [concrete] |
| `reference-semantics/semantics/float.k:56` | ordinary rule | — | `ea3ec435ee8e` | rule applyBuiltin("abs", F:Float, .Vals) => absF(F) |
| `reference-semantics/semantics/float.k:61` | ordinary rule | — | `b7f366ac2fd2` | rule <k> Import(_:String) => .K ... </k> |
| `reference-semantics/semantics/float.k:65` | syntax | — | `b46507b52502` | syntax KItem ::= "#mathCeil" |
| `reference-semantics/semantics/float.k:66` | priority rule | priority(40) | `6731784767d2` | rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)] |
| `reference-semantics/semantics/float.k:67` | ordinary rule | — | `43dd41b1a295` | rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> |
| `reference-semantics/semantics/float.k:70` | syntax | — | `7182dabba367` | syntax KItem ::= "#mathFloor" |
| `reference-semantics/semantics/float.k:71` | priority rule | priority(40) | `8c6ed970676f` | rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)] |
| `reference-semantics/semantics/float.k:72` | ordinary rule | — | `65f0f3138bd4` | rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k> |
| `reference-semantics/semantics/float.k:73` | syntax (function, total) | function, symbol(floorFI), total | `bb414e98ce7c` | syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)] |
| `reference-semantics/semantics/float.k:74` | concrete rule | concrete | `f37a1802fdee` | rule floorFI(I:Int) => I [concrete] |
| `reference-semantics/semantics/float.k:75` | concrete rule | concrete | `c5cd79cd77b2` | rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] |
| `reference-semantics/semantics/float.k:78` | ordinary rule | — | `4f4ffc4a6628` | rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V) |
| `reference-semantics/semantics/float.k:79` | ordinary rule | — | `7bedc8cbfda8` | rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V) |
| `reference-semantics/semantics/float.k:82` | syntax | — | `533ce2092684` | syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val) |
| `reference-semantics/semantics/float.k:83` | priority rule | priority(40) | `841a8e8cad16` | rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)] |
| `reference-semantics/semantics/float.k:84` | ordinary rule | — | `fbcd9d035631` | rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k> |
| `reference-semantics/semantics/float.k:85` | ordinary rule | — | `f6ee2424cb4d` | rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k> |
| `reference-semantics/semantics/float.k:86` | syntax (function, total) | function, symbol(toF), total | `5506be323911` | syntax Float ::= toF(Val) [function, total, symbol(toF)] |
| `reference-semantics/semantics/float.k:87` | concrete rule | concrete | `f04a867ac1b6` | rule toF(F:Float) => F [concrete] |
| `reference-semantics/semantics/float.k:88` | concrete rule | concrete | `cc5f238f41ea` | rule toF(I:Int) => intToF(I) [concrete] |
| `reference-semantics/semantics/float.k:93` | syntax (function, total) | function, symbol(ceilF), total | `526754603124` | syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)] |
| `reference-semantics/semantics/float.k:94` | concrete rule | concrete | `e87663a71975` | rule ceilF(I:Int) => I [concrete] |
| `reference-semantics/semantics/float.k:95` | concrete rule | concrete | `01d36090dbec` | rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] |
| `reference-semantics/semantics/float.k:99` | ordinary rule | — | `0360ea94a438` | rule applyUn("-", F:Float) => 0.0 -Float F |
| `reference-semantics/semantics/float.k:103` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(subF), total | `bd9289f118f1` | syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators] |
| `reference-semantics/semantics/float.k:104` | concrete rule | concrete | `12f60d082454` | rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete] |
| `reference-semantics/semantics/float.k:105` | ordinary rule | — | `600f864e0d4d` | rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2) |
| `reference-semantics/semantics/float.k:107` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(divF), total | `91e03f2ac9cf` | syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators] |
| `reference-semantics/semantics/float.k:108` | concrete rule | concrete | `26654b7bcf19` | rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete] |
| `reference-semantics/semantics/float.k:109` | ordinary rule | — | `ef46ce780b55` | rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2) |
| `reference-semantics/semantics/float.k:111` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(addF), total | `2398531263a9` | syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators] |
| `reference-semantics/semantics/float.k:112` | concrete rule | concrete | `3f45f3747744` | rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete] |
| `reference-semantics/semantics/float.k:113` | ordinary rule | — | `034cf2b77672` | rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2) |
| `reference-semantics/semantics/float.k:115` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(mulF), total | `4e0d8b299c85` | syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators] |
| `reference-semantics/semantics/float.k:116` | concrete rule | concrete | `46a5b95d90aa` | rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete] |
| `reference-semantics/semantics/float.k:117` | ordinary rule | — | `7bc5c419eaac` | rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2) |
| `reference-semantics/semantics/float.k:119` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(powF), total | `47a046af374b` | syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators] |
| `reference-semantics/semantics/float.k:120` | concrete rule | concrete | `88f0b7d20137` | rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete] |
| `reference-semantics/semantics/float.k:121` | ordinary rule | — | `661e867f27fd` | rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) |
| `reference-semantics/semantics/float.k:125` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(gtF), total | `9fdcc02ab4ee` | syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators] |
| `reference-semantics/semantics/float.k:126` | concrete rule | concrete | `088703ce3653` | rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete] |
| `reference-semantics/semantics/float.k:127` | ordinary rule | — | `f0c90e2b4e5c` | rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2) |
| `reference-semantics/semantics/float.k:128` | ordinary rule | — | `5eb9299eb06c` | rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2) |
| `reference-semantics/semantics/float.k:129` | ordinary rule | — | `714c6765e587` | rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) |
| `reference-semantics/semantics/float.k:132` | ordinary rule | — | `f16ef18fbd1d` | rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F) |
| `reference-semantics/semantics/float.k:133` | ordinary rule | — | `6353492521ad` | rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:134` | ordinary rule | — | `04cafcfbec72` | rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F) |
| `reference-semantics/semantics/float.k:135` | ordinary rule | — | `3262fc150fee` | rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:136` | ordinary rule | — | `167f6a0aa189` | rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F) |
| `reference-semantics/semantics/float.k:137` | ordinary rule | — | `4af2b331bab8` | rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:138` | ordinary rule | — | `96e9b55afb28` | rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F) |
| `reference-semantics/semantics/float.k:139` | ordinary rule | — | `287151051c6e` | rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:142` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(eqF), total | `4d0d2ce425b4` | syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators] |
| `reference-semantics/semantics/float.k:143` | concrete rule | concrete | `9653dcd55b20` | rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete] |
| `reference-semantics/semantics/float.k:144` | ordinary rule | — | `ac77f892cfc0` | rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F) |
| `reference-semantics/semantics/float.k:145` | ordinary rule | — | `722beef5b388` | rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:146` | ordinary rule | — | `15bc1d1e3d08` | rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F) |
| `reference-semantics/semantics/float.k:147` | ordinary rule | — | `330ac8e38f2c` | rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:148` | ordinary rule | — | `124e1c20285e` | rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F) |
| `reference-semantics/semantics/float.k:149` | ordinary rule | — | `37d0e64b6946` | rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I)) |
| `reference-semantics/semantics/float.k:150` | ordinary rule | — | `f4596c34e133` | rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F) |
| `reference-semantics/semantics/float.k:151` | ordinary rule | — | `54db876cc1ea` | rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:154` | ordinary rule | — | `ed4df68a2d97` | rule applyCmp("==", V:Val, noneV) => V ==K noneV |
| `reference-semantics/semantics/float.k:155` | ordinary rule | — | `2a477f6ab023` | rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) |
| `reference-semantics/semantics/float.k:160` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(decStrToF), total | `588f5768440e` | syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators] |
| `reference-semantics/semantics/float.k:161` | concrete rule | concrete | `32ad68f36a35` | rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete] |
| `reference-semantics/semantics/float.k:162` | concrete rule | concrete | `4eca371f8a9e` | rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete] |
| `reference-semantics/semantics/float.k:165` | syntax (function) | function | `7ccb5a6fa421` | syntax Int ::= headIS(IntSeq) [function] |
| `reference-semantics/semantics/float.k:166` | ordinary rule | — | `87f97131d232` | rule headIS(iCons(C:Int, _:IntSeq)) => C |
| `reference-semantics/semantics/float.k:167` | syntax (function, total) | function, total | `81addd4f5596` | syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total] |
| `reference-semantics/semantics/float.k:168` | ordinary rule | — | `8628f4bdac5b` | rule intPart(CS:IntSeq) => intPartAcc(CS, 0) |
| `reference-semantics/semantics/float.k:169` | ordinary rule | — | `b0b8a3b71d8b` | rule intPartAcc(.IntSeq, A:Int) => A |
| `reference-semantics/semantics/float.k:170` | ordinary rule | — | `afe4cef68f53` | rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A |
| `reference-semantics/semantics/float.k:171` | ordinary rule | — | `3bb38774e1e4` | rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46 |
| `reference-semantics/semantics/float.k:173` | syntax (function, total) | function, total | `89e3dfc58231` | syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total] |
| `reference-semantics/semantics/float.k:174` | ordinary rule | — | `63e7386de829` | rule fracPart(.IntSeq) => 0 |
| `reference-semantics/semantics/float.k:175` | ordinary rule | — | `336f8c20b7a9` | rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0) |
| `reference-semantics/semantics/float.k:176` | ordinary rule | — | `517a796c8a51` | rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46 |
| `reference-semantics/semantics/float.k:177` | ordinary rule | — | `3a7473c8713b` | rule fracAcc(.IntSeq, A:Int) => A |
| `reference-semantics/semantics/float.k:178` | ordinary rule | — | `a87341fff574` | rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48)) |
| `reference-semantics/semantics/float.k:179` | syntax (function, total) | function, total | `dffc425acef9` | syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total] |
| `reference-semantics/semantics/float.k:180` | ordinary rule | — | `f006d2881246` | rule fracScale(.IntSeq) => 1 |
| `reference-semantics/semantics/float.k:181` | ordinary rule | — | `abcd00241d75` | rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1) |
| `reference-semantics/semantics/float.k:182` | ordinary rule | — | `abd5cc4adcbe` | rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46 |
| `reference-semantics/semantics/float.k:183` | ordinary rule | — | `1e74ce0b2611` | rule fscAcc(.IntSeq, A:Int) => A |
| `reference-semantics/semantics/float.k:184` | ordinary rule | — | `21eab0b39d56` | rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10) |
| `reference-semantics/semantics/float.k:185` | ordinary rule | — | `a528cb142102` | rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS) |
| `reference-semantics/semantics/float.k:186` | ordinary rule | — | `80d889ec0b35` | rule applyBuiltin("float", I:Int, .Vals) => intToF(I) |
| `reference-semantics/semantics/float.k:187` | ordinary rule | — | `6fb1be69dcea` | rule applyBuiltin("float", F:Float, .Vals) => F |
| `reference-semantics/semantics/float.k:190` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(divFloatIntV), total | `f49cc043a05b` | syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators] |
| `reference-semantics/semantics/float.k:191` | concrete rule | concrete | `a71c4a7b3d8c` | rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete] |
| `reference-semantics/semantics/float.k:192` | ordinary rule | — | `a2200023b7cc` | rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) |
| `reference-semantics/semantics/float.k:195` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(intToF), total | `4f21c29912e1` | syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators] |
| `reference-semantics/semantics/float.k:196` | concrete rule | concrete | `389178d3dfd7` | rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete] |
| `reference-semantics/semantics/float.k:197` | ordinary rule | — | `695a4d4bdd54` | rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F) |
| `reference-semantics/semantics/float.k:198` | ordinary rule | — | `8105c256a812` | rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:199` | ordinary rule | — | `7b68c3069735` | rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F) |
| `reference-semantics/semantics/float.k:200` | ordinary rule | — | `1409954604e5` | rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:201` | ordinary rule | — | `74e2f8b58bc6` | rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F) |
| `reference-semantics/semantics/float.k:202` | ordinary rule | — | `de611e1415d1` | rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:203` | ordinary rule | — | `1714c1550770` | rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F) |
| `reference-semantics/semantics/float.k:204` | ordinary rule | — | `a3b308b7b2c2` | rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I)) |
| `reference-semantics/semantics/float.k:205` | ordinary rule | — | `fc6de3b7c2f9` | rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F) |
| `reference-semantics/semantics/float.k:206` | ordinary rule | — | `18ff729bf687` | rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) |
| `reference-semantics/semantics/float.k:209` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(truncF), total | `11c17aa2d431` | syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators] |
| `reference-semantics/semantics/float.k:210` | concrete rule | concrete | `bee730d1e871` | rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete] |
| `reference-semantics/semantics/float.k:211` | ordinary rule | — | `651a7c3ee92f` | rule applyBuiltin("int", F:Float, .Vals) => truncF(F) |
| `reference-semantics/semantics/float.k:213` | ordinary rule | — | `d009baabfcf1` | rule applyBuiltin("float", I:Int, .Vals) => intToF(I) |
| `reference-semantics/semantics/float.k:214` | ordinary rule | — | `e38c88c120d0` | rule applyBuiltin("float", F:Float, .Vals) => F |
| `reference-semantics/semantics/float.k:217` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(roundF), total | `d0b7f75c69f6` | syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators] |
| `reference-semantics/semantics/float.k:218` | concrete rule | concrete | `71a93adeb3de` | rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete] |
| `reference-semantics/semantics/float.k:223` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(roundFN), total | `73ff3255d50d` | syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators] |
| `reference-semantics/semantics/float.k:224` | concrete rule | concrete | `7dd52ea7b2ef` | rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete] |
| `reference-semantics/semantics/float.k:227` | ordinary rule | — | `a41ad11a3b0b` | rule applyBuiltin("round", F:Float, .Vals) => roundF(F) |
| `reference-semantics/semantics/float.k:228` | ordinary rule | — | `053cb084a542` | rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N) |
| `reference-semantics/semantics/float.k:230` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(sqrtF), total | `ccbc57547039` | syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators] |
| `reference-semantics/semantics/float.k:231` | concrete rule | concrete | `6233ea5230d8` | rule sqrtF(F:Float) => sqrtFloat(F) [concrete] |
| `reference-semantics/semantics/float.k:232` | syntax | — | `cf723364ca5d` | syntax KItem ::= "#mathSqrt" |
| `reference-semantics/semantics/float.k:233` | priority rule | priority(40) | `9708f9876df9` | rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)] |
| `reference-semantics/semantics/float.k:234` | ordinary rule | — | `7e79b6dbd8c0` | rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k> |
| `reference-semantics/semantics/float.k:235` | ordinary rule | — | `c4013b0dca36` | rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> |
| `reference-semantics/semantics/float.k:243` | syntax | — | `a63f310fdba5` | syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float) |
| `reference-semantics/semantics/float.k:244` | ordinary rule | — | `838b90fdad47` | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V) |
| `reference-semantics/semantics/float.k:245` | ordinary rule | — | `dfa99d6b3002` | rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k> |
| `reference-semantics/semantics/float.k:246` | ordinary rule | — | `35a797d2ae5f` | rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k> |
| `reference-semantics/semantics/float.k:247` | ordinary rule | — | `62e0de8abff0` | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V) |
| `reference-semantics/semantics/float.k:250` | syntax | — | `cd35b1a80916` | syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float) |
| `reference-semantics/semantics/float.k:251` | ordinary rule | — | `785007e31d6e` | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V) |
| `reference-semantics/semantics/float.k:252` | ordinary rule | — | `6b8405dae8d4` | rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k> |
| `reference-semantics/semantics/float.k:253` | ordinary rule | — | `700ae0c8579a` | rule <k> #iterDone ~> #minContF(M:Float) => M ... </k> |
| `reference-semantics/semantics/float.k:254` | ordinary rule | — | `20f5bd8c50ce` | rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) |
| `reference-semantics/semantics/float.k:261` | syntax | — | `0abd52ddf475` | syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float) |
| `reference-semantics/semantics/float.k:262` | ordinary rule | — | `37c9e8542e68` | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V)) |
| `reference-semantics/semantics/float.k:265` | ordinary rule | — | `65c1e01d9cd3` | rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k> |
| `reference-semantics/semantics/float.k:266` | ordinary rule | — | `a39fca22a153` | rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k> |
| `reference-semantics/semantics/float.k:267` | ordinary rule | — | `666c7bfe3488` | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V) |
| `reference-semantics/semantics/float.k:270` | ordinary rule | — | `53789ad2c50a` | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V) |
| `reference-semantics/semantics/functions.k:8` | syntax | — | `b4b39d2075f5` | syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall" |
| `reference-semantics/semantics/functions.k:14` | ordinary rule | — | `3d9d7b82c79b` | rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes> |
| `reference-semantics/semantics/functions.k:18` | syntax | — | `a6aeea98e7de` | syntax Expr ::= closureExpr(ParamNames, Stmts) |
| `reference-semantics/semantics/functions.k:19` | ordinary rule | — | `35af1b9f9cd1` | rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> |
| `reference-semantics/semantics/functions.k:27` | syntax | — | `f8d9de7aaced` | syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) |
| `reference-semantics/semantics/functions.k:31` | syntax | — | `2874a00eb4f8` | syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map) |
| `reference-semantics/semantics/functions.k:33` | ordinary rule | — | `eeed22781654` | rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k> |
| `reference-semantics/semantics/functions.k:36` | ordinary rule | — | `da212052370e` | rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M) |
| `reference-semantics/semantics/functions.k:42` | ordinary rule | — | `1baa1ec6b80e` | rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes> |
| `reference-semantics/semantics/functions.k:47` | ordinary rule | — | `df3f1718f0fa` | rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env> |
| `reference-semantics/semantics/functions.k:50` | ordinary rule | — | `23034bad3097` | rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k> |
| `reference-semantics/semantics/functions.k:53` | ordinary rule | — | `9d4bb562bd67` | rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M) |
| `reference-semantics/semantics/functions.k:59` | ordinary rule | — | `c9d889107f8b` | rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> |
| `reference-semantics/semantics/functions.k:63` | ordinary rule | — | `e3671d9bac62` | rule <k> #bindP(.ParamNames, .Vals) => .K ... </k> |
| `reference-semantics/semantics/functions.k:64` | ordinary rule | — | `00aa592629d2` | rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes> // a param that is a cellvar was pre-bound to its cell at frame entry |
| `reference-semantics/semantics/functions.k:68` | priority rule | priority(40) | `9279b324c710` | rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] |
| `reference-semantics/semantics/functions.k:78` | ordinary rule | — | `1c5a24070b0f` | rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret> |
| `reference-semantics/semantics/functions.k:80` | ordinary rule | — | `50321bd01cb5` | rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0). |
| `reference-semantics/semantics/functions.k:85` | ordinary rule | — | `102fe224b1a3` | rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc> |
| `reference-semantics/semantics/int.k:7` | ordinary rule | — | `bea824a9d0c7` | rule applyUn("-", I:Int) => 0 -Int I |
| `reference-semantics/semantics/int.k:9` | ordinary rule | — | `c1356f411510` | rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2 // Bool participates in int arithmetic (x += (a == b)) |
| `reference-semantics/semantics/int.k:11` | ordinary rule | — | `161421e6a696` | rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi |
| `reference-semantics/semantics/int.k:12` | ordinary rule | — | `aea33156fe56` | rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I |
| `reference-semantics/semantics/int.k:13` | ordinary rule | — | `3ed75ef0b6a5` | rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2 |
| `reference-semantics/semantics/int.k:14` | ordinary rule | — | `08fc0a4f5088` | rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2 |
| `reference-semantics/semantics/int.k:15` | ordinary rule | — | `b6d3e6ecd7f8` | rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2) |
| `reference-semantics/semantics/int.k:16` | ordinary rule | — | `85afa4d25d14` | rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2 |
| `reference-semantics/semantics/int.k:17` | ordinary rule | — | `614ae406522b` | rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0 |
| `reference-semantics/semantics/int.k:19` | syntax (function) | function | `c131b0a21233` | syntax Int ::= pyMod(Int, Int) [function] |
| `reference-semantics/semantics/int.k:20` | ordinary rule | — | `e3bb9293bfde` | rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2 |
| `reference-semantics/semantics/int.k:22` | ordinary rule | — | `060cdde57487` | rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2 |
| `reference-semantics/semantics/int.k:23` | ordinary rule | — | `6feefb9796ed` | rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2 |
| `reference-semantics/semantics/int.k:24` | ordinary rule | — | `96c9008e9527` | rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2 |
| `reference-semantics/semantics/int.k:25` | ordinary rule | — | `a2928e82e850` | rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2 |
| `reference-semantics/semantics/int.k:26` | ordinary rule | — | `2814f20ec081` | rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2 |
| `reference-semantics/semantics/int.k:27` | ordinary rule | — | `098913bfaf25` | rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2 |
| `reference-semantics/semantics/iter.k:8` | syntax | — | `2fa814827c66` | syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable) |
| `reference-semantics/semantics/list.k:9` | ordinary rule | — | `6fbad02eed13` | rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k> |
| `reference-semantics/semantics/list.k:10` | ordinary rule | — | `b39b7937bce1` | rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> |
| `reference-semantics/semantics/list.k:13` | syntax | — | `3d024af826bb` | syntax ApplyK ::= "toList" |
| `reference-semantics/semantics/list.k:14` | ordinary rule | — | `f3163ec1febd` | rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k> |
| `reference-semantics/semantics/list.k:15` | ordinary rule | — | `70e0fbd42323` | rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> |
| `reference-semantics/semantics/list.k:18` | syntax (function, total) | function, total | `ac8c744da9bb` | syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total] |
| `reference-semantics/semantics/list.k:19` | ordinary rule | — | `f058ddea1c85` | rule valSeqConcat(.ValSeq, T:ValSeq) => T |
| `reference-semantics/semantics/list.k:20` | ordinary rule | — | `89ea4e872855` | rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) |
| `reference-semantics/semantics/list.k:24` | priority rule | priority(45) | `7c2e29a9bff3` | rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)] |
| `reference-semantics/semantics/list.k:27` | ordinary rule | — | `408c1dfb03ff` | rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B |
| `reference-semantics/semantics/list.k:28` | ordinary rule | — | `8b89879a64e7` | rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) |
| `reference-semantics/semantics/list.k:33` | syntax (function, total) | function, total | `afe83d38567e` | syntax Bool ::= hasRefVS(ValSeq) [function, total] |
| `reference-semantics/semantics/list.k:34` | ordinary rule | — | `c6097b5c360d` | rule hasRefVS(.ValSeq) => false |
| `reference-semantics/semantics/list.k:35` | ordinary rule | — | `3e47ea875f2d` | rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R) |
| `reference-semantics/semantics/list.k:37` | syntax (function) | function | `c331eb24453a` | syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map) [function] |
| `reference-semantics/semantics/list.k:39` | ordinary rule | — | `2394eddeadea` | rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true |
| `reference-semantics/semantics/list.k:40` | ordinary rule | — | `e2fba1091261` | rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false |
| `reference-semantics/semantics/list.k:41` | ordinary rule | — | `20bfecdfc83c` | rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false |
| `reference-semantics/semantics/list.k:42` | ordinary rule | — | `d7909ad8764a` | rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP) |
| `reference-semantics/semantics/list.k:45` | ordinary rule | — | `f950fd8a48ac` | rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP) |
| `reference-semantics/semantics/list.k:47` | ordinary rule | — | `0fefe5738b32` | rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP) |
| `reference-semantics/semantics/list.k:49` | ordinary rule | — | `3863900e8a58` | rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP) |
| `reference-semantics/semantics/list.k:50` | owise rule | owise | `5d6c5490e16b` | rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] |
| `reference-semantics/semantics/list.k:53` | priority rule | priority(40) | `74ec9bb67d8a` | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] |
| `reference-semantics/semantics/list.k:58` | syntax | — | `e171041153df` | syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB" |
| `reference-semantics/semantics/list.k:59` | ordinary rule | — | `ebd1399faaff` | rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k> |
| `reference-semantics/semantics/list.k:60` | ordinary rule | — | `81419bc508ae` | rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k> |
| `reference-semantics/semantics/list.k:61` | ordinary rule | — | `e84f869d57a9` | rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k> |
| `reference-semantics/semantics/list.k:62` | ordinary rule | — | `d8442792286c` | rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k> |
| `reference-semantics/semantics/list.k:63` | ordinary rule | — | `5d0b63b75b9c` | rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V |
| `reference-semantics/semantics/list.k:65` | ordinary rule | — | `9f843c144870` | rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V) |
| `reference-semantics/semantics/list.k:67` | ordinary rule | — | `5511f8c4ec44` | rule <k> B:Bool ~> #notB => notBool B ... </k> |
| `reference-semantics/semantics/methods.k:10` | syntax (function) | function | `bcd6321cf1a2` | syntax Val ::= applyMethod(Val, String, Vals) [function] |
| `reference-semantics/semantics/methods.k:13` | ordinary rule | — | `328b30a3774c` | rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS) |
| `reference-semantics/semantics/methods.k:14` | ordinary rule | — | `a6ae81f68d63` | rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS) |
| `reference-semantics/semantics/methods.k:15` | ordinary rule | — | `eb11f68e6087` | rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS) |
| `reference-semantics/semantics/methods.k:16` | ordinary rule | — | `03ce90d0bcd9` | rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) |
| `reference-semantics/semantics/methods.k:19` | ordinary rule | — | `8ac3d7a0baa7` | rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS)) |
| `reference-semantics/semantics/methods.k:20` | ordinary rule | — | `ec5cf79a45b0` | rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS)) |
| `reference-semantics/semantics/methods.k:21` | ordinary rule | — | `30f5704dc33a` | rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) |
| `reference-semantics/semantics/methods.k:26` | ordinary rule | — | `7c16ae8ffba7` | rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS)) |
| `reference-semantics/semantics/methods.k:27` | syntax (function, total) | function, total | `8449bace9b91` | syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total] |
| `reference-semantics/semantics/methods.k:28` | ordinary rule | — | `dcb47502ba71` | rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq |
| `reference-semantics/semantics/methods.k:29` | ordinary rule | — | `f2558775f8da` | rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS |
| `reference-semantics/semantics/methods.k:30` | ordinary rule | — | `b4b93bd868a6` | rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) |
| `reference-semantics/semantics/methods.k:34` | ordinary rule | — | `21c9fe9f7420` | rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC) |
| `reference-semantics/semantics/methods.k:35` | syntax (function) | function | `277077c74e8e` | syntax Int ::= cntSub(IntSeq, IntSeq) [function] |
| `reference-semantics/semantics/methods.k:36` | ordinary rule | — | `f4dfc7d2f461` | rule cntSub(.IntSeq, _:IntSeq) => 0 |
| `reference-semantics/semantics/methods.k:37` | ordinary rule | — | `3dfe01810fca` | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0 |
| `reference-semantics/semantics/methods.k:39` | ordinary rule | — | `b8d3c3017ae1` | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0 |
| `reference-semantics/semantics/methods.k:41` | syntax (function, total) | function, total | `121d0c58dbca` | syntax IntSeq ::= dropIS(IntSeq, Int) [function, total] |
| `reference-semantics/semantics/methods.k:42` | ordinary rule | — | `036bd013d44b` | rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0 |
| `reference-semantics/semantics/methods.k:43` | owise rule | owise | `f7a542230356` | rule dropIS(.IntSeq, _:Int) => .IntSeq [owise] |
| `reference-semantics/semantics/methods.k:44` | ordinary rule | — | `5f16ac6adf64` | rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 |
| `reference-semantics/semantics/methods.k:47` | ordinary rule | — | `fc495b2dc6ff` | rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS))))) |
| `reference-semantics/semantics/methods.k:48` | syntax (function, total) | function, total | `4eeafed3826b` | syntax IntSeq ::= trimWS(IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:49` | ordinary rule | — | `4291267251ce` | rule trimWS(.IntSeq) => .IntSeq |
| `reference-semantics/semantics/methods.k:50` | ordinary rule | — | `879a0736a8b4` | rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C) |
| `reference-semantics/semantics/methods.k:51` | ordinary rule | — | `988ee980274c` | rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C) |
| `reference-semantics/semantics/methods.k:52` | syntax (function, total) | function, total | `588afa88ddb7` | syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:53` | ordinary rule | — | `f72cb5914e4a` | rule revIS(S:IntSeq) => revISAcc(S, .IntSeq) |
| `reference-semantics/semantics/methods.k:54` | ordinary rule | — | `24b1a05b8e5d` | rule revISAcc(.IntSeq, A:IntSeq) => A |
| `reference-semantics/semantics/methods.k:55` | ordinary rule | — | `a743803ce5fe` | rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) |
| `reference-semantics/semantics/methods.k:58` | ordinary rule | — | `46cee75aa03a` | rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) |
| `reference-semantics/semantics/methods.k:61` | ordinary rule | — | `905e9a90f217` | rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) |
| `reference-semantics/semantics/methods.k:64` | ordinary rule | — | `bf346f893e63` | rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V) |
| `reference-semantics/semantics/methods.k:65` | syntax (function, total) | function, total | `b0bd756c2169` | syntax Int ::= cntOccVS(ValSeq, Val) [function, total] |
| `reference-semantics/semantics/methods.k:66` | ordinary rule | — | `3123629a3981` | rule cntOccVS(.ValSeq, _:Val) => 0 |
| `reference-semantics/semantics/methods.k:67` | ordinary rule | — | `87d9bfa2c6dc` | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V |
| `reference-semantics/semantics/methods.k:68` | ordinary rule | — | `e6d7b509c27b` | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V) |
| `reference-semantics/semantics/methods.k:72` | priority rule | priority(40) | `f87f16cdb41a` | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)] |
| `reference-semantics/semantics/methods.k:75` | syntax (function) | function | `c6cbf0518fb6` | syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result |
| `reference-semantics/semantics/methods.k:76` | ordinary rule | — | `e52130b97cee` | rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR) |
| `reference-semantics/semantics/methods.k:77` | ordinary rule | — | `f030838ce6a9` | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C) |
| `reference-semantics/semantics/methods.k:79` | ordinary rule | — | `c1b92498fe1d` | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) // flush the current token to the result list iff non-empty. |
| `reference-semantics/semantics/methods.k:82` | syntax (function) | function | `002dffc41af2` | syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function] |
| `reference-semantics/semantics/methods.k:83` | ordinary rule | — | `2fce7516e2f0` | rule flushTok(ACC:ValSeq, .IntSeq) => ACC |
| `reference-semantics/semantics/methods.k:84` | ordinary rule | — | `0c970d4acf65` | rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq)) |
| `reference-semantics/semantics/methods.k:85` | syntax (function, total) | function, total | `37f133bfa155` | syntax Bool ::= isWSC(Int) [function, total] |
| `reference-semantics/semantics/methods.k:86` | ordinary rule | — | `8175fabb1057` | rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 |
| `reference-semantics/semantics/methods.k:89` | priority rule | priority(39) | `548cf93e2c92` | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] |
| `reference-semantics/semantics/methods.k:94` | priority rule | priority(40) | `3ec5aa46cf78` | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)] |
| `reference-semantics/semantics/methods.k:97` | syntax (function) | function | `c7f1e785bafc` | syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token |
| `reference-semantics/semantics/methods.k:98` | ordinary rule | — | `3e2b8460ffa2` | rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq) |
| `reference-semantics/semantics/methods.k:99` | ordinary rule | — | `101dfa34ca8c` | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP |
| `reference-semantics/semantics/methods.k:101` | ordinary rule | — | `cc530b70412e` | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP) |
| `reference-semantics/semantics/methods.k:104` | ordinary rule | — | `a8e93dddcc5a` | rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B)) |
| `reference-semantics/semantics/methods.k:106` | syntax (function, total) | function, total | `6c0dfc288cc6` | syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total] |
| `reference-semantics/semantics/methods.k:107` | ordinary rule | — | `2e484a1f777c` | rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq |
| `reference-semantics/semantics/methods.k:108` | ordinary rule | — | `439491c83162` | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A |
| `reference-semantics/semantics/methods.k:109` | ordinary rule | — | `9e3d155b87f6` | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) |
| `reference-semantics/semantics/methods.k:112` | syntax (function, total) | function, total | `d60af3772ac0` | syntax Bool ::= isUpperC(Int) [function, total] |
| `reference-semantics/semantics/methods.k:113` | ordinary rule | — | `885fc4123b60` | rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90 |
| `reference-semantics/semantics/methods.k:115` | syntax (function, total) | function, total | `9dc54db4cfe6` | syntax Bool ::= isLowerC(Int) [function, total] |
| `reference-semantics/semantics/methods.k:116` | ordinary rule | — | `35a981d9ee7c` | rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122 |
| `reference-semantics/semantics/methods.k:118` | syntax (function, total) | function, total | `219ceeed6ce7` | syntax Bool ::= isAlphaC(Int) [function, total] |
| `reference-semantics/semantics/methods.k:119` | ordinary rule | — | `63bc2def4f48` | rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C) |
| `reference-semantics/semantics/methods.k:121` | syntax (function, total) | function, total | `86d0c30136f3` | syntax Bool ::= isDigitC(Int) [function, total] |
| `reference-semantics/semantics/methods.k:122` | ordinary rule | — | `12088c599f6a` | rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57 |
| `reference-semantics/semantics/methods.k:124` | syntax (function, total) | function, total | `79b65077c768` | syntax Bool ::= hasUpper(IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:125` | ordinary rule | — | `f3875f726b38` | rule hasUpper(.IntSeq) => false |
| `reference-semantics/semantics/methods.k:126` | ordinary rule | — | `bb1d921fad33` | rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S) |
| `reference-semantics/semantics/methods.k:128` | syntax (function, total) | function, total | `6e2fe9388187` | syntax Bool ::= hasLower(IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:129` | ordinary rule | — | `abfddcd09b06` | rule hasLower(.IntSeq) => false |
| `reference-semantics/semantics/methods.k:130` | ordinary rule | — | `92b0385b9092` | rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S) |
| `reference-semantics/semantics/methods.k:132` | syntax (function, total) | function, total | `436a79dc0dbd` | syntax Bool ::= allAlpha(IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:133` | ordinary rule | — | `2c1e5b1f9b4f` | rule allAlpha(.IntSeq) => true |
| `reference-semantics/semantics/methods.k:134` | ordinary rule | — | `5e18a35dd26e` | rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S) |
| `reference-semantics/semantics/methods.k:136` | syntax (function, total) | function, total | `1f98366143eb` | syntax Bool ::= allDigit(IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:137` | ordinary rule | — | `f2d51c623b4f` | rule allDigit(.IntSeq) => true |
| `reference-semantics/semantics/methods.k:138` | ordinary rule | — | `5aeec07d2a56` | rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S) |
| `reference-semantics/semantics/methods.k:140` | syntax (function, total) | function, total | `6bbb30e0ba93` | syntax Int ::= lowerC(Int) [function, total] |
| `reference-semantics/semantics/methods.k:142` | ordinary rule | — | `16ec3ccc73d9` | rule lowerC(C:Int) => C +Int 32 requires isUpperC(C) |
| `reference-semantics/semantics/methods.k:143` | owise rule | owise | `fa575fdac7d9` | rule lowerC(C:Int) => C [owise] |
| `reference-semantics/semantics/methods.k:145` | syntax (function, total) | function, total | `b6e1b4db46d4` | syntax Int ::= upperC(Int) [function, total] |
| `reference-semantics/semantics/methods.k:146` | ordinary rule | — | `36f1da2397a7` | rule upperC(C:Int) => C -Int 32 requires isLowerC(C) |
| `reference-semantics/semantics/methods.k:147` | owise rule | owise | `9c78f8050595` | rule upperC(C:Int) => C [owise] |
| `reference-semantics/semantics/methods.k:149` | syntax (function, total) | function, total | `3d8ce436184a` | syntax Int ::= swapC(Int) [function, total] |
| `reference-semantics/semantics/methods.k:150` | ordinary rule | — | `ec05513118cd` | rule swapC(C:Int) => C +Int 32 requires isUpperC(C) |
| `reference-semantics/semantics/methods.k:151` | ordinary rule | — | `960de195b818` | rule swapC(C:Int) => C -Int 32 requires isLowerC(C) |
| `reference-semantics/semantics/methods.k:152` | owise rule | owise | `ae88e3ca76da` | rule swapC(C:Int) => C [owise] |
| `reference-semantics/semantics/methods.k:154` | syntax (function, total) | function, total | `0fb973df4891` | syntax IntSeq ::= mapLower(IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:155` | ordinary rule | — | `5cd9c020c2bd` | rule mapLower(.IntSeq) => .IntSeq |
| `reference-semantics/semantics/methods.k:156` | ordinary rule | — | `da21f8430ee4` | rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S)) |
| `reference-semantics/semantics/methods.k:158` | syntax (function, total) | function, total | `82523acd09b2` | syntax IntSeq ::= mapUpper(IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:159` | ordinary rule | — | `b31cc456b204` | rule mapUpper(.IntSeq) => .IntSeq |
| `reference-semantics/semantics/methods.k:160` | ordinary rule | — | `2c01ef3cfffe` | rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S)) |
| `reference-semantics/semantics/methods.k:162` | syntax (function, total) | function, total | `39e9100dbb4b` | syntax IntSeq ::= mapSwap(IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:163` | ordinary rule | — | `6de81779e3a0` | rule mapSwap(.IntSeq) => .IntSeq |
| `reference-semantics/semantics/methods.k:164` | ordinary rule | — | `039a7b17bd02` | rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S)) |
| `reference-semantics/semantics/methods.k:166` | syntax (function, total) | function, total | `6f6a4aa0687d` | syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/methods.k:167` | ordinary rule | — | `0d4624ea4695` | rule startsWith(.IntSeq, _:IntSeq) => true |
| `reference-semantics/semantics/methods.k:168` | ordinary rule | — | `c22b5ffce270` | rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| `reference-semantics/semantics/methods.k:169` | ordinary rule | — | `4e5497c6f435` | rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs) |
| `reference-semantics/semantics/operators.k:10` | ordinary rule | — | `ec04b29e2d1b` | rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k> |
| `reference-semantics/semantics/operators.k:12` | ordinary rule | — | `df8d1cba28a9` | rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> |
| `reference-semantics/semantics/operators.k:15` | context | — | `e4932b24484a` | context Compare(HOLE, _) |
| `reference-semantics/semantics/operators.k:16` | context | — | `ca9e40a2c27b` | context Compare(_:Val, CmpOp(_, HOLE)) |
| `reference-semantics/semantics/operators.k:17` | owise rule | owise | `262226c0a44f` | rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise] |
| `reference-semantics/semantics/operators.k:19` | ordinary rule | — | `30c0e5930768` | rule applyCmp("is", V:Val, noneV) => V ==K noneV |
| `reference-semantics/semantics/operators.k:20` | ordinary rule | — | `e6679786edcc` | rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) |
| `reference-semantics/semantics/operators.k:25` | priority rule | priority(40) | `a0cb682355d9` | rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/operators.k:28` | priority rule | priority(40) | `39a1fff9641f` | rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] |
| `reference-semantics/semantics/operators.k:34` | priority rule | priority(40) | `ca104b09a61f` | rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)] |
| `reference-semantics/semantics/operators.k:38` | priority rule | priority(40) | `e0069c80841c` | rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)] |
| `reference-semantics/semantics/operators.k:44` | priority rule | priority(40) | `ad34ddf8843f` | rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/range.k:9` | syntax (function, total) | function, total | `dec39b9740c8` | syntax Bool ::= inRange(Int, Int, Int) [function, total] |
| `reference-semantics/semantics/range.k:10` | ordinary rule | — | `f93b1245c723` | rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI) |
| `reference-semantics/semantics/range.k:12` | syntax (function) | function | `9f9f1aaeaee2` | syntax Int ::= rangeLen(Int, Int, Int) [function] |
| `reference-semantics/semantics/range.k:13` | ordinary rule | — | `86948590010c` | rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO |
| `reference-semantics/semantics/range.k:15` | ordinary rule | — | `f92c137c0eb7` | rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO |
| `reference-semantics/semantics/range.k:17` | ordinary rule | — | `954aadd3bd47` | rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO) |
| `reference-semantics/semantics/range.k:20` | ordinary rule | — | `df9306db7d3b` | rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST) |
| `reference-semantics/semantics/range.k:23` | ordinary rule | — | `b1dd4699b330` | rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST) |
| `reference-semantics/semantics/set.k:8` | syntax | — | `ceff1f1bd25d` | syntax Val ::= setV(IntSeq) |
| `reference-semantics/semantics/set.k:11` | syntax (function, total) | function, total | `be0ae2291d5d` | syntax Bool ::= codeIn(Int, IntSeq) [function, total] |
| `reference-semantics/semantics/set.k:12` | ordinary rule | — | `be0e691e3c2c` | rule codeIn(_:Int, .IntSeq) => false |
| `reference-semantics/semantics/set.k:13` | ordinary rule | — | `df05d7c47e63` | rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) |
| `reference-semantics/semantics/set.k:16` | syntax (function, total) | function, total | `1128bf4578c0` | syntax IntSeq ::= dedupCodes(IntSeq) [function, total] \| dedupFrom(IntSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/set.k:18` | ordinary rule | — | `d766b83ec2d8` | rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq) |
| `reference-semantics/semantics/set.k:19` | ordinary rule | — | `43f63938c987` | rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC |
| `reference-semantics/semantics/set.k:20` | ordinary rule | — | `bc0cbdf40272` | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC) |
| `reference-semantics/semantics/set.k:22` | ordinary rule | — | `cdcf7512adc5` | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC) |
| `reference-semantics/semantics/set.k:25` | syntax (function, total) | function, total | `c59b599a912d` | syntax IntSeq ::= snocCode(IntSeq, Int) [function, total] |
| `reference-semantics/semantics/set.k:26` | ordinary rule | — | `054d50d68e36` | rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq) |
| `reference-semantics/semantics/set.k:27` | ordinary rule | — | `0caac9972e04` | rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) |
| `reference-semantics/semantics/set.k:31` | syntax (function, total) | function, total | `b1d04ee84fab` | syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/set.k:32` | ordinary rule | — | `d53c3df008c3` | rule subsetCodes(.IntSeq, _:IntSeq) => true |
| `reference-semantics/semantics/set.k:33` | ordinary rule | — | `850be538170a` | rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B) |
| `reference-semantics/semantics/set.k:35` | syntax (function, total) | function, total | `6156266fe9d9` | syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/set.k:36` | ordinary rule | — | `973ec0dc7d1d` | rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) |
| `reference-semantics/semantics/set.k:39` | ordinary rule | — | `7a5ed6b4e8d6` | rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B) |
| `reference-semantics/semantics/sort.k:18` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(sortVS), total | `c6d761b986e3` | syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators] |
| `reference-semantics/semantics/sort.k:19` | syntax (function) | function | `0a76cca66b26` | syntax ValSeq ::= insVS(Int, ValSeq) [function] |
| `reference-semantics/semantics/sort.k:20` | concrete rule | concrete | `47b723f10a23` | rule sortVS(.ValSeq) => .ValSeq [concrete] |
| `reference-semantics/semantics/sort.k:21` | concrete rule | concrete | `afe20c3cfa1a` | rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete] |
| `reference-semantics/semantics/sort.k:22` | concrete rule | concrete | `c51e9071fd27` | rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete] |
| `reference-semantics/semantics/sort.k:23` | concrete rule | concrete | `e38dbfdea30a` | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete] |
| `reference-semantics/semantics/sort.k:24` | concrete rule | concrete | `28954fe82fc6` | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete] // str elements insert by the shared lexicographic strLt (methods.k) |
| `reference-semantics/semantics/sort.k:26` | syntax (function) | function | `f778a322aece` | syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function] |
| `reference-semantics/semantics/sort.k:27` | concrete rule | concrete | `f56269f2805f` | rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete] |
| `reference-semantics/semantics/sort.k:28` | concrete rule | concrete | `1f2df95775eb` | rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete] |
| `reference-semantics/semantics/sort.k:29` | concrete rule | concrete | `6da9281774d2` | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete] |
| `reference-semantics/semantics/sort.k:31` | concrete rule | concrete | `b081a4533cc7` | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] |
| `reference-semantics/semantics/sort.k:36` | ordinary rule | — | `eef7a2274d34` | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> |
| `reference-semantics/semantics/sort.k:40` | priority rule | priority(40) | `d65d54fc6663` | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] |
| `reference-semantics/semantics/sort.k:49` | syntax (function, total, no-evaluators) | function, no-evaluators, symbol(sortKeyVS), total | `f2ac55ee34d8` | syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators] |
| `reference-semantics/semantics/sort.k:51` | syntax (function, total) | function, total | `4cc64fd11b54` | syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total] |
| `reference-semantics/semantics/sort.k:53` | ordinary rule | — | `ce0aa18a5360` | rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq) |
| `reference-semantics/semantics/sort.k:54` | ordinary rule | — | `726a2866a59e` | rule revVSAcc(.ValSeq, A:ValSeq) => A |
| `reference-semantics/semantics/sort.k:55` | ordinary rule | — | `5fd679052347` | rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A)) |
| `reference-semantics/semantics/sort.k:57` | syntax (function, total) | function, total | `7e8ff8d017c7` | syntax ValSeq ::= condRev(ValSeq, Bool) [function, total] |
| `reference-semantics/semantics/sort.k:58` | ordinary rule | — | `a1e37b0851c3` | rule condRev(S:ValSeq, false) => S |
| `reference-semantics/semantics/sort.k:59` | ordinary rule | — | `c4ff333dfa8c` | rule condRev(S:ValSeq, true) => revVS(S) |
| `reference-semantics/semantics/sort.k:61` | ordinary rule | — | `f3941ef08218` | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k> |
| `reference-semantics/semantics/sort.k:63` | ordinary rule | — | `b949e0b45750` | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k> |
| `reference-semantics/semantics/sort.k:65` | ordinary rule | — | `ee87483936ca` | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> |
| `reference-semantics/semantics/str.k:8` | ordinary rule | — | `5aea34cb3320` | rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k> |
| `reference-semantics/semantics/str.k:9` | ordinary rule | — | `56a5f597c313` | rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> |
| `reference-semantics/semantics/str.k:13` | syntax (function) | function | `4c7f66efcd88` | syntax IntSeq ::= strToCodes(String) [function] |
| `reference-semantics/semantics/str.k:14` | ordinary rule | — | `70d0a8a99357` | rule <k> Str(S:String) => str(strToCodes(S)) ... </k> |
| `reference-semantics/semantics/str.k:15` | ordinary rule | — | `c7b4b4fc80bd` | rule strToCodes("") => .IntSeq |
| `reference-semantics/semantics/str.k:16` | ordinary rule | — | `51298b6c4778` | rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 |
| `reference-semantics/semantics/str.k:20` | syntax (function, total) | function, total | `4dcfe32d71db` | syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/str.k:21` | ordinary rule | — | `91549ced5945` | rule seqConcat(.IntSeq, T:IntSeq) => T |
| `reference-semantics/semantics/str.k:22` | ordinary rule | — | `b8aaa07a8414` | rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T)) |
| `reference-semantics/semantics/str.k:24` | ordinary rule | — | `8fc5d2cd4bed` | rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B)) |
| `reference-semantics/semantics/str.k:25` | ordinary rule | — | `8039b62069c1` | rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B |
| `reference-semantics/semantics/str.k:26` | ordinary rule | — | `efca9467c64c` | rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) |
| `reference-semantics/semantics/str.k:29` | ordinary rule | — | `96acbdc1af10` | rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X) |
| `reference-semantics/semantics/str.k:30` | ordinary rule | — | `b646f3d3387b` | rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X) |
| `reference-semantics/semantics/str.k:32` | syntax (function, total) | function, total | `0c2a240d2f88` | syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/str.k:33` | ordinary rule | — | `4144b5588234` | rule strPrefix(.IntSeq, _:IntSeq) => true |
| `reference-semantics/semantics/str.k:34` | ordinary rule | — | `0e758c7b129d` | rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| `reference-semantics/semantics/str.k:35` | ordinary rule | — | `d6816398ab16` | rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs) |
| `reference-semantics/semantics/str.k:37` | syntax (function, total) | function, total | `e5d82a70ec2a` | syntax Bool ::= strContains(IntSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/str.k:38` | ordinary rule | — | `34700463fbce` | rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X) |
| `reference-semantics/semantics/str.k:39` | ordinary rule | — | `af56f9463481` | rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq) |
| `reference-semantics/semantics/str.k:40` | ordinary rule | — | `8a306aa50740` | rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) |
| `reference-semantics/semantics/str.k:48` | syntax (function, total) | function, total | `e6a79420c495` | syntax Bool ::= strLt(IntSeq, IntSeq) [function, total] |
| `reference-semantics/semantics/str.k:49` | ordinary rule | — | `3dbb3480331f` | rule strLt(.IntSeq, .IntSeq) => false |
| `reference-semantics/semantics/str.k:50` | ordinary rule | — | `1d055a6c97d4` | rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true |
| `reference-semantics/semantics/str.k:51` | ordinary rule | — | `d1e1c922c4b2` | rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| `reference-semantics/semantics/str.k:52` | ordinary rule | — | `1af5632197a6` | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B |
| `reference-semantics/semantics/str.k:53` | ordinary rule | — | `66583c4efcfd` | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B |
| `reference-semantics/semantics/str.k:54` | ordinary rule | — | `d72e4a9c68cd` | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B |
| `reference-semantics/semantics/str.k:56` | ordinary rule | — | `eca13b5d6543` | rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B) |
| `reference-semantics/semantics/str.k:57` | ordinary rule | — | `8d9e17848541` | rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A) |
| `reference-semantics/semantics/str.k:58` | ordinary rule | — | `fd8254e2aad6` | rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A) |
| `reference-semantics/semantics/str.k:59` | ordinary rule | — | `0bb37c9e5117` | rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B) |
| `reference-semantics/semantics/subscript.k:11` | syntax (function, total) | function, total | `92dd5a3cbdae` | syntax Val ::= valSeqAt(ValSeq, Int) [function, total] |
| `reference-semantics/semantics/subscript.k:12` | ordinary rule | — | `be09883d26ef` | rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V |
| `reference-semantics/semantics/subscript.k:13` | ordinary rule | — | `8a6a88c38c3d` | rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0 |
| `reference-semantics/semantics/subscript.k:16` | syntax (function) | function | `d573fee41395` | syntax Int ::= intSeqAt(IntSeq, Int) [function] |
| `reference-semantics/semantics/subscript.k:17` | ordinary rule | — | `df3c3702e26d` | rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C |
| `reference-semantics/semantics/subscript.k:18` | ordinary rule | — | `6dded3b88658` | rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0 |
| `reference-semantics/semantics/subscript.k:21` | syntax (function, total) | function, total | `8d0629ddf60a` | syntax Int ::= normIdx(Int, Int) [function, total] |
| `reference-semantics/semantics/subscript.k:22` | ordinary rule | — | `b98d45a6a45b` | rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0 |
| `reference-semantics/semantics/subscript.k:23` | ordinary rule | — | `f9e7cd4854b6` | rule normIdx(I:Int, _:Int) => I requires I >=Int 0 |
| `reference-semantics/semantics/subscript.k:27` | context | — | `e235a553cf79` | context Subscript(HOLE, _) |
| `reference-semantics/semantics/subscript.k:28` | context | — | `0ea5351709e9` | context Subscript(_:Val, HOLE:Expr) |
| `reference-semantics/semantics/subscript.k:31` | priority rule | priority(40) | `14b58651f9c5` | rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/subscript.k:35` | ordinary rule | — | `e2cbe99533f0` | rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k> |
| `reference-semantics/semantics/subscript.k:37` | syntax (function) | function | `83aa86951e42` | syntax Val ::= applyIndex(Val, Int) [function] |
| `reference-semantics/semantics/subscript.k:38` | ordinary rule | — | `48f741540df2` | rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS))) |
| `reference-semantics/semantics/subscript.k:39` | ordinary rule | — | `52ab84557b24` | rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS))) |
| `reference-semantics/semantics/subscript.k:40` | ordinary rule | — | `b9eedb76886e` | rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) |
| `reference-semantics/semantics/subscript.k:44` | syntax | — | `170630aa9dee` | syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt) |
| `reference-semantics/semantics/subscript.k:49` | syntax | — | `560ebb71a2e1` | syntax OptInt ::= "noB" \| someB(Int) |
| `reference-semantics/semantics/subscript.k:50` | ordinary rule | — | `8bfda75b10b5` | rule <k> #evalB(NoBound) => noB ... </k> |
| `reference-semantics/semantics/subscript.k:51` | ordinary rule | — | `d96ec0c4fa39` | rule <k> #evalB(E:Expr) => E ~> #toSome ... </k> |
| `reference-semantics/semantics/subscript.k:52` | ordinary rule | — | `55c49487ba78` | rule <k> I:Int ~> #toSome => someB(I) ... </k> |
| `reference-semantics/semantics/subscript.k:54` | ordinary rule | — | `b39cd50c6c41` | rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k> |
| `reference-semantics/semantics/subscript.k:55` | ordinary rule | — | `57331568a526` | rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k> |
| `reference-semantics/semantics/subscript.k:56` | ordinary rule | — | `9de5529341d6` | rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> // a list slice constructs a NEW object; a str slice stays a value |
| `reference-semantics/semantics/subscript.k:58` | priority rule | priority(45) | `a66a9e5be1e7` | rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)] |
| `reference-semantics/semantics/subscript.k:61` | ordinary rule | — | `4b6c937f1b27` | rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k> |
| `reference-semantics/semantics/subscript.k:63` | syntax (function) | function | `35803b4f4140` | syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function] |
| `reference-semantics/semantics/subscript.k:64` | ordinary rule | — | `42ed1f69b35d` | rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| `reference-semantics/semantics/subscript.k:66` | ordinary rule | — | `82d3fca1e37e` | rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| `reference-semantics/semantics/subscript.k:68` | ordinary rule | — | `1d29f0d5c61e` | rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) |
| `reference-semantics/semantics/subscript.k:72` | syntax (function, total) | function, total | `3673727509ac` | syntax Int ::= slStep(OptInt) [function, total] |
| `reference-semantics/semantics/subscript.k:73` | ordinary rule | — | `7c2511c1afc3` | rule slStep(noB) => 1 |
| `reference-semantics/semantics/subscript.k:74` | ordinary rule | — | `38520b2d08df` | rule slStep(someB(S:Int)) => S |
| `reference-semantics/semantics/subscript.k:76` | syntax (function) | function | `12940b25c9d8` | syntax Int ::= slStart(OptInt, OptInt, Int) [function] |
| `reference-semantics/semantics/subscript.k:77` | ordinary rule | — | `d1245451058b` | rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0 |
| `reference-semantics/semantics/subscript.k:79` | ordinary rule | — | `32a8543ade1c` | rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0 |
| `reference-semantics/semantics/subscript.k:81` | ordinary rule | — | `eb72ac47325f` | rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST)) |
| `reference-semantics/semantics/subscript.k:83` | syntax (function) | function | `def902114717` | syntax Int ::= slStop(OptInt, OptInt, Int) [function] |
| `reference-semantics/semantics/subscript.k:84` | ordinary rule | — | `74fd2b418d13` | rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0 |
| `reference-semantics/semantics/subscript.k:86` | ordinary rule | — | `ff38d06e869b` | rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0 |
| `reference-semantics/semantics/subscript.k:88` | ordinary rule | — | `adb5792d3852` | rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST)) |
| `reference-semantics/semantics/subscript.k:90` | syntax (function, total) | function, total | `9ec1896aa81d` | syntax Int ::= slAdjust(Int, Int, Int) [function, total] |
| `reference-semantics/semantics/subscript.k:91` | ordinary rule | — | `a33fd3355164` | rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0 |
| `reference-semantics/semantics/subscript.k:93` | ordinary rule | — | `753b0f615233` | rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0 |
| `reference-semantics/semantics/subscript.k:96` | syntax (function, total) | function, total | `74b1e671d5bc` | syntax Int ::= clampLo(Int, Int) [function, total] |
| `reference-semantics/semantics/subscript.k:97` | ordinary rule | — | `e393553cb99a` | rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0 |
| `reference-semantics/semantics/subscript.k:99` | ordinary rule | — | `df573f70389c` | rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0 |
| `reference-semantics/semantics/subscript.k:102` | syntax (function, total) | function, total | `cf49fd584aa0` | syntax Int ::= clampHi(Int, Int, Int) [function, total] |
| `reference-semantics/semantics/subscript.k:103` | ordinary rule | — | `edcd350fd0b8` | rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN |
| `reference-semantics/semantics/subscript.k:105` | ordinary rule | — | `ae77268386ff` | rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN |
| `reference-semantics/semantics/subscript.k:109` | syntax (function) | function | `328023ed0539` | syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function] |
| `reference-semantics/semantics/subscript.k:110` | ordinary rule | — | `32b99cf6a66c` | rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP) |
| `reference-semantics/semantics/subscript.k:113` | ordinary rule | — | `257fa9fa471a` | rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)) |
| `reference-semantics/semantics/subscript.k:116` | syntax (function) | function | `0a55bc39332c` | syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function] |
| `reference-semantics/semantics/subscript.k:117` | ordinary rule | — | `443572026d5c` | rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP) |
| `reference-semantics/semantics/subscript.k:120` | ordinary rule | — | `0f259c668431` | rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)) |
| `reference-semantics/semantics/syntax.k:9` | syntax (macro) | macro, strict(1), strict(2) | `b137de7fc427` | syntax Expr ::= "Int" "(" Int ")" \| "Float" "(" Float ")" \| "Bool" "(" Bool ")" \| "Name" "(" String ")" \| "Str" "(" String ")" \| "UnaryOp" "(" String "," Expr ")" [strict(2)] \| "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp" "(" String "," Exprs ")" \| "ListExpr" "(" Exprs ")" \| "DictExpr" "(" Entries ")" \| "ListComp" "(" Expr "," CompFors ")" [macro] \| "GenExp" "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs "... |
| `reference-semantics/semantics/syntax.k:32` | syntax | — | `79e0572a08cb` | syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" |
| `reference-semantics/semantics/syntax.k:33` | syntax | — | `8985681d39e2` | syntax Entry ::= "Entry" "(" Expr "," Expr ")" |
| `reference-semantics/semantics/syntax.k:34` | syntax | — | `1523104ecc07` | syntax Entries ::= List{Entry, ","} |
| `reference-semantics/semantics/syntax.k:35` | syntax | — | `d77836cca454` | syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")" |
| `reference-semantics/semantics/syntax.k:36` | syntax | — | `76d2ff7278fb` | syntax CompFors ::= List{CompFor, ""} |
| `reference-semantics/semantics/syntax.k:37` | syntax | — | `e680c1e2f7b6` | syntax Exprs ::= List{Expr, ","} |
| `reference-semantics/semantics/syntax.k:38` | syntax | — | `b3f9e60ba967` | syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")" |
| `reference-semantics/semantics/syntax.k:39` | syntax | — | `c5203ebf1422` | syntax Bound ::= Expr \| "NoBound" |
| `reference-semantics/semantics/syntax.k:41` | syntax | strict, strict(1), strict(2), strict(3) | `6e900c516e20` | syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] \| "Import" "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While" "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return" "(" Expr ")" [strict] \| "Assert" "(" Expr ")" [strict] \| "Expr" "(" Expr ")" [strict] ... |
| `reference-semantics/semantics/syntax.k:56` | syntax | — | `c2eb1faa5708` | syntax Stmts ::= List{Stmt, ""} |
| `reference-semantics/semantics/syntax.k:57` | syntax | — | `bc2dc3cfbacd` | syntax Params ::= "Params" "(" ParamNames ")" |
| `reference-semantics/semantics/syntax.k:58` | syntax | — | `6081c51206f1` | syntax CellVars ::= "CellVars" "(" ParamNames ")" |
| `reference-semantics/semantics/syntax.k:59` | syntax | — | `2bd8e51bc504` | syntax FreeVars ::= "FreeVars" "(" ParamNames ")" |
| `reference-semantics/semantics/syntax.k:60` | syntax | — | `8788a8da7c08` | syntax ParamNames ::= List{String, ","} |
| `reference-semantics/semantics/syntax.k:61` | syntax | — | `f7e6da5815fd` | syntax Module ::= "Module" "(" Stmts ")" |
| `reference-semantics/semantics/tuple.k:10` | ordinary rule | — | `8571b818781f` | rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k> |
| `reference-semantics/semantics/tuple.k:11` | ordinary rule | — | `d8c8d186a0d0` | rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> |
| `reference-semantics/semantics/tuple.k:14` | syntax | — | `508a95f61aed` | syntax ApplyK ::= "toTuple" |
| `reference-semantics/semantics/tuple.k:15` | ordinary rule | — | `ff193ea2849e` | rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k> |
| `reference-semantics/semantics/tuple.k:16` | ordinary rule | — | `b0d84d481730` | rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k> |
| `reference-semantics/semantics/tuple.k:18` | ordinary rule | — | `85f06205d3ec` | rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B // membership routes through the same k-cell fold as lists (list.k) |
| `reference-semantics/semantics/tuple.k:20` | ordinary rule | — | `1b68f3cf2df9` | rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k> |
| `reference-semantics/semantics/tuple.k:21` | ordinary rule | — | `0233eca33017` | rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> // t.index(v): first index of v (ValueError out of subset) |
| `reference-semantics/semantics/tuple.k:23` | ordinary rule | — | `bd7254bbf110` | rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0) |
| `reference-semantics/semantics/tuple.k:24` | syntax (function) | function | `df13ef70912b` | syntax Int ::= idxOfVS(ValSeq, Val, Int) [function] |
| `reference-semantics/semantics/tuple.k:25` | ordinary rule | — | `663f7ddf889d` | rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V |
| `reference-semantics/semantics/tuple.k:26` | ordinary rule | — | `0fcb8941c5fc` | rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V) |
| `reference-semantics/semantics/tuple.k:28` | ordinary rule | — | `aef9af9e2003` | rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) |
| `reference-semantics/semantics/tuple.k:31` | syntax | — | `98b229b9b432` | syntax KItem ::= #bindTgt(Expr, Val) |
| `reference-semantics/semantics/tuple.k:32` | ordinary rule | — | `14aff46eab0f` | rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes> |
| `reference-semantics/semantics/tuple.k:35` | priority rule | priority(40) | `00b05b2c0ef5` | rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)] |
| `reference-semantics/semantics/tuple.k:42` | ordinary rule | — | `0d5b4092fa17` | rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| `reference-semantics/semantics/tuple.k:43` | ordinary rule | — | `ac45b93d13bf` | rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| `reference-semantics/semantics/tuple.k:44` | priority rule | priority(40) | `194bee85b47a` | rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/tuple.k:49` | syntax | — | `7dbe45ad3aa2` | syntax KItem ::= #unpackSeq(Exprs, ValSeq) |
| `reference-semantics/semantics/tuple.k:50` | ordinary rule | — | `3187abeadb72` | rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| `reference-semantics/semantics/tuple.k:51` | ordinary rule | — | `867fac1e6227` | rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| `reference-semantics/semantics/tuple.k:52` | priority rule | priority(40) | `c2d1189c7fd5` | rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| `reference-semantics/semantics/tuple.k:55` | ordinary rule | — | `006177fc1c70` | rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k> |
| `reference-semantics/semantics/tuple.k:57` | ordinary rule | — | `2377fb943da1` | rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k> |
| `verification.k:7` | syntax (macro) | macro | `b567d4d623e8` | syntax Module ::= "solutionProgram" [macro] |
| `verification.k:8` | ordinary rule | — | `b8f7e873c2cd` | rule solutionProgram => Module( FuncDef("_evaluate", Params("operator", "operand", "start", "end", "level"), If(Compare(Name("level"), CmpOp("==", Int(0))), Assign(Name("i"), BinOp("-", Name("end"), Int(1))) While(Compare(Name("i"), CmpOp(">=", Name("start"))), If(Compare(Subscript(Name("operator"), Name("i")), CmpOp("==", Str("+"))), Return( BinOp("+", Call(Name("_evaluate"), Name("operator"), Name("operand"), Name("start"), Name("i"), Int(0)), Call(Na... |
| `verification.k:85` | syntax (macro) | macro | `2227e1aa9b86` | syntax Str ::= "plusV" [macro] \| "minusV" [macro] \| "timesV" [macro] \| "floorDivV" [macro] \| "powerV" [macro] |
| `verification.k:90` | ordinary rule | — | `67ac38234ec7` | rule plusV => str(iCons(43, .IntSeq)) |
| `verification.k:91` | ordinary rule | — | `85a812b263d2` | rule minusV => str(iCons(45, .IntSeq)) |
| `verification.k:92` | ordinary rule | — | `ff32cef443e4` | rule timesV => str(iCons(42, .IntSeq)) |
| `verification.k:93` | ordinary rule | — | `bf2282fcb64a` | rule floorDivV => str(iCons(47, iCons(47, .IntSeq))) |
| `verification.k:94` | ordinary rule | — | `219a500114ce` | rule powerV => str(iCons(42, iCons(42, .IntSeq))) |
| `verification.k:97` | syntax (function, total) | function, total | `8fcd32491353` | syntax Int ::= floorQuot(Int, Int) [function, total] |
| `verification.k:98` | ordinary rule | — | `9145fe9a4b1f` | rule floorQuot(A:Int, B:Int) => (A -Int pyMod(A, B)) /Int B |
| `verification.k:100` | syntax | — | `5a89f7de2023` | syntax KItem ::= runDoAlgebra(ValSeq, ValSeq) |
| `verification.k:101` | ordinary rule | — | `9b3072806b05` | rule <k> runDoAlgebra(OPS:ValSeq, NDS:ValSeq) => #loadAll(solutionProgram) ~> Call(Name("do_algebra"), list(OPS), list(NDS)) ... </k> |
| `spec.k:9` | claim | — | `dba23073a373` | claim <k> runDoAlgebra( vCons(plusV, .ValSeq), vCons(A:Int, vCons(B:Int, .ValSeq))) => A +Int B </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires A >=Int 0 andBool B >=Int 0 [label(plus)] |
| `spec.k:31` | claim | — | `d93409144f50` | claim <k> runDoAlgebra( vCons(minusV, .ValSeq), vCons(A:Int, vCons(B:Int, .ValSeq))) => A -Int B </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires A >=Int 0 andBool B >=Int 0 [label(minus)] |
| `spec.k:53` | claim | — | `f7b358456d8e` | claim <k> runDoAlgebra( vCons(timesV, .ValSeq), vCons(A:Int, vCons(B:Int, .ValSeq))) => A *Int B </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires A >=Int 0 andBool B >=Int 0 [label(times)] |
| `spec.k:75` | claim | — | `cf46330e62b0` | claim <k> runDoAlgebra( vCons(floorDivV, .ValSeq), vCons(A:Int, vCons(B:Int, .ValSeq))) => floorQuot(A, B) </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires A >=Int 0 andBool B >Int 0 [label(floor)] |
| `spec.k:97` | claim | — | `6eb4c663a529` | claim <k> runDoAlgebra( vCons(powerV, .ValSeq), vCons(2, vCons(5, .ValSeq))) => 32 </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> [label(power)] |
| `spec.k:119` | claim | — | `b42009b27473` | claim <k> runDoAlgebra( vCons(minusV, vCons(minusV, .ValSeq)), vCons(A:Int, vCons(B:Int, vCons(C:Int, .ValSeq)))) => (A -Int B) -Int C </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires A >=Int 0 andBool B >=Int 0 andBool C >=... |
| `spec.k:142` | claim | — | `ae7646125629` | claim <k> runDoAlgebra( vCons(floorDivV, vCons(floorDivV, .ValSeq)), vCons(20, vCons(3, vCons(2, .ValSeq)))) => 3 </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> [label(floor-assoc)] |
| `spec.k:164` | claim | — | `ed50a8ee1e22` | claim <k> runDoAlgebra( vCons(powerV, vCons(powerV, .ValSeq)), vCons(2, vCons(3, vCons(2, .ValSeq)))) => 512 </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> [label(power-assoc)] |
| `spec.k:186` | claim | — | `070a45aedef0` | claim <k> runDoAlgebra( vCons(plusV, vCons(timesV, vCons(minusV, .ValSeq))), vCons(A:Int, vCons(B:Int, vCons(C:Int, vCons(D:Int, .ValSeq))))) => (A +Int (B *Int C)) -Int D </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires A >... |
| `spec.k:210` | claim | — | `7622fde96b07` | claim <k> runDoAlgebra( vCons(plusV, vCons(timesV, vCons(powerV, vCons(floorDivV, vCons(minusV, .ValSeq))))), vCons(A:Int, vCons(B:Int, vCons(2, vCons(3, vCons(E:Int, vCons(F:Int, .ValSeq))))))) => (A +Int floorQuot(B *Int 8, E)) -Int F </k> <env> 0 </env> <scopes> (0 \|-> scope(.Map, parent(-1))) (-1 \|-> builtinsScope) => ?FINAL_SCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet ... |

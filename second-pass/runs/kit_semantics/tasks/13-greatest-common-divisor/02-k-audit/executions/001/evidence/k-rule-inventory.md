# Exhaustive K declaration and rule inventory

Inventory SHA-256: `ec054996094f700acd4a31dd662b7d92f38554e1e8787984f313e5a1a6175b83`

Total outer declarations/rules/claims: 933

Keyword counts: claim=2, configuration=1, context=5, rule=697, syntax=228

Role counts: configuration=1, evaluation-context=5, fixed-semantic+ordinary-rule=589, fixed-semantic+ordinary-rule+concrete=35, fixed-semantic+ordinary-rule+owise=26, fixed-semantic+ordinary-rule+priority=45, macro-or-alias=4, proof-local+simplification-rule=2, reachability-claim=2, syntax-declaration=78, syntax-declaration+function=38, syntax-declaration+function+total=83, syntax-declaration+function+total+symbol=3, syntax-declaration+function+total+symbol+no-evaluators=22

## Per-source counts

| Source | Count |
|---|---:|
| `reference-semantics/semantics/assert.k` | 3 |
| `reference-semantics/semantics/bool.k` | 14 |
| `reference-semantics/semantics/builtins.k` | 175 |
| `reference-semantics/semantics/call.k` | 24 |
| `reference-semantics/semantics/comprehension.k` | 10 |
| `reference-semantics/semantics/concrete.k` | 21 |
| `reference-semantics/semantics/controls.k` | 37 |
| `reference-semantics/semantics/core.k` | 84 |
| `reference-semantics/semantics/dict.k` | 40 |
| `reference-semantics/semantics/float.k` | 155 |
| `reference-semantics/semantics/functions.k` | 19 |
| `reference-semantics/semantics/int.k` | 17 |
| `reference-semantics/semantics/iter.k` | 1 |
| `reference-semantics/semantics/list.k` | 32 |
| `reference-semantics/semantics/methods.k` | 102 |
| `reference-semantics/semantics/operators.k` | 12 |
| `reference-semantics/semantics/range.k` | 8 |
| `reference-semantics/semantics/set.k` | 18 |
| `reference-semantics/semantics/sort.k` | 25 |
| `reference-semantics/semantics/str.k` | 33 |
| `reference-semantics/semantics/subscript.k` | 57 |
| `reference-semantics/semantics/syntax.k` | 16 |
| `reference-semantics/semantics/tuple.k` | 25 |
| `spec.k` | 2 |
| `verification.k` | 3 |

## Every inventoried sentence

| ID | Source:lines | Kind / attributes / role | Normalized text |
|---|---|---|---|
| `e50a39df9acf25cf` | `reference-semantics/semantics/assert.k:6-7` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| `85739355183cc22c` | `reference-semantics/semantics/assert.k:8-11` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| `22a87fb43f5f6c75` | `reference-semantics/semantics/assert.k:13-15` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `56397dfc49f76e8c` | `reference-semantics/semantics/bool.k:8-8` | rule; none; fixed-semantic+ordinary-rule | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| `720d1aef95b3e42a` | `reference-semantics/semantics/bool.k:10-10` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| `ce03e26801d349d0` | `reference-semantics/semantics/bool.k:11-15` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| `a6804b93d5823155` | `reference-semantics/semantics/bool.k:16-16` | context; none; evaluation-context | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| `6c8018e5a3d11715` | `reference-semantics/semantics/bool.k:17-17` | rule; none; fixed-semantic+ordinary-rule | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| `a1c7f785bae5aa8e` | `reference-semantics/semantics/bool.k:18-19` | rule; none; fixed-semantic+ordinary-rule | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| `b29fdf0aaf24d345` | `reference-semantics/semantics/bool.k:20-21` | rule; none; fixed-semantic+ordinary-rule | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| `e3233d19e421bdc9` | `reference-semantics/semantics/bool.k:22-23` | rule; none; fixed-semantic+ordinary-rule | `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| `2f314ec8a65ba9a9` | `reference-semantics/semantics/bool.k:24-28` | rule; none; fixed-semantic+ordinary-rule | `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` |
| `1e17840be78009a6` | `reference-semantics/semantics/bool.k:29-30` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| `270a3874b9096090` | `reference-semantics/semantics/bool.k:31-34` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| `dc65e7909df0fdc6` | `reference-semantics/semantics/bool.k:35-38` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| `656866a829c915c4` | `reference-semantics/semantics/bool.k:39-42` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| `9e86b6ffb4b4ee18` | `reference-semantics/semantics/bool.k:43-46` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| `3e0b7cde50032619` | `reference-semantics/semantics/builtins.k:17-19` | syntax; function; syntax-declaration+function | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| `564b2cbd516ddd98` | `reference-semantics/semantics/builtins.k:20-20` | syntax; function; syntax-declaration+function | `syntax Int ::= seqLen(Val) [function]` |
| `1ff3b68aff7892b5` | `reference-semantics/semantics/builtins.k:21-21` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| `3703f7085035444c` | `reference-semantics/semantics/builtins.k:22-22` | rule; none; fixed-semantic+ordinary-rule | `rule seqLen(list(VS:ValSeq)) => vsLen(VS)` |
| `814828010934428b` | `reference-semantics/semantics/builtins.k:23-23` | rule; none; fixed-semantic+ordinary-rule | `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)` |
| `66911ee1d284b88a` | `reference-semantics/semantics/builtins.k:24-24` | rule; none; fixed-semantic+ordinary-rule | `rule seqLen(str(IS:IntSeq)) => isLen(IS)` |
| `f71bb8aabf9bb912` | `reference-semantics/semantics/builtins.k:25-25` | rule; none; fixed-semantic+ordinary-rule | `rule seqLen(setV(DS:IntSeq)) => isLen(DS)` |
| `d9ed37396c29f566` | `reference-semantics/semantics/builtins.k:26-31` | rule; none; fixed-semantic+ordinary-rule | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| `6a54465800fbffca` | `reference-semantics/semantics/builtins.k:32-32` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| `745257a05f3b4588` | `reference-semantics/semantics/builtins.k:33-33` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| `0c3acd210dc4ddbb` | `reference-semantics/semantics/builtins.k:34-34` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>` |
| `401457ff85266d64` | `reference-semantics/semantics/builtins.k:35-35` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>` |
| `00c5226a70a26444` | `reference-semantics/semantics/builtins.k:36-36` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| `cf89f49191c7573d` | `reference-semantics/semantics/builtins.k:37-37` | rule; none; fixed-semantic+ordinary-rule | `rule charsOf(.IntSeq) => .ValSeq` |
| `f17451970138c408` | `reference-semantics/semantics/builtins.k:38-40` | rule; none; fixed-semantic+ordinary-rule | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| `124ba098b038b4a1` | `reference-semantics/semantics/builtins.k:41-43` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| `83238ffa2b15843f` | `reference-semantics/semantics/builtins.k:44-46` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| `624e01d2686a06d7` | `reference-semantics/semantics/builtins.k:47-47` | syntax; none; syntax-declaration | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| `62efcd31679928f4` | `reference-semantics/semantics/builtins.k:48-48` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| `70989845d98139b7` | `reference-semantics/semantics/builtins.k:49-49` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| `2fc3626b26236d51` | `reference-semantics/semantics/builtins.k:50-52` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| `1273544f09d35970` | `reference-semantics/semantics/builtins.k:54-54` | syntax; function; syntax-declaration+function | `syntax Int ::= intOf(Val) [function]` |
| `fd637a7acae15f5a` | `reference-semantics/semantics/builtins.k:55-55` | rule; none; fixed-semantic+ordinary-rule | `rule intOf(I:Int) => I` |
| `1be0c4beac20bf0a` | `reference-semantics/semantics/builtins.k:56-58` | rule; none; fixed-semantic+ordinary-rule | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| `e0519f7dcb8fe882` | `reference-semantics/semantics/builtins.k:59-59` | syntax; none; syntax-declaration | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| `331b69398eb451a8` | `reference-semantics/semantics/builtins.k:60-60` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| `54cea64f8eb14c80` | `reference-semantics/semantics/builtins.k:61-61` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| `4529e2fd9b9025ae` | `reference-semantics/semantics/builtins.k:62-63` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| `d317cd32d2ca30a4` | `reference-semantics/semantics/builtins.k:64-65` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| `fea1f743162a1b31` | `reference-semantics/semantics/builtins.k:67-67` | syntax; none; syntax-declaration | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| `762a95cb32f93fc4` | `reference-semantics/semantics/builtins.k:68-68` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| `a9d85dab881ac721` | `reference-semantics/semantics/builtins.k:69-69` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| `ca7a734eaec5fa4b` | `reference-semantics/semantics/builtins.k:70-71` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| `eae3b6eb669e6e23` | `reference-semantics/semantics/builtins.k:72-75` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` |
| `7b195bc6f39ef005` | `reference-semantics/semantics/builtins.k:76-76` | syntax; none; syntax-declaration | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| `3764e007dda765bd` | `reference-semantics/semantics/builtins.k:77-77` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| `a5d42b6d32265636` | `reference-semantics/semantics/builtins.k:78-79` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| `2d5f96ffc5088ad0` | `reference-semantics/semantics/builtins.k:80-80` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| `68c9c8524defbb52` | `reference-semantics/semantics/builtins.k:81-81` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| `ec4821de2aef96c1` | `reference-semantics/semantics/builtins.k:82-84` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| `902379806d57381d` | `reference-semantics/semantics/builtins.k:86-86` | syntax; none; syntax-declaration | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| `4fa7240988a179f5` | `reference-semantics/semantics/builtins.k:87-87` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| `7aa0c0f2d6e9a753` | `reference-semantics/semantics/builtins.k:88-89` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| `6389b138a09da560` | `reference-semantics/semantics/builtins.k:90-90` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| `004f68a51eeb163e` | `reference-semantics/semantics/builtins.k:91-91` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| `8aae8d4c9314e650` | `reference-semantics/semantics/builtins.k:92-96` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| `3b508c16497a7cbb` | `reference-semantics/semantics/builtins.k:97-97` | syntax; function; syntax-declaration+function | `syntax Int ::= maxVals(Int, Vals) [function]` |
| `2693a8ecdfdfb80a` | `reference-semantics/semantics/builtins.k:98-98` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| `0d0572aae80fc417` | `reference-semantics/semantics/builtins.k:99-99` | rule; none; fixed-semantic+ordinary-rule | `rule maxVals(M:Int, .Vals) => M` |
| `4efe23088d367ba3` | `reference-semantics/semantics/builtins.k:100-100` | rule; none; fixed-semantic+ordinary-rule | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| `712f7d220cefb231` | `reference-semantics/semantics/builtins.k:102-102` | syntax; function; syntax-declaration+function | `syntax Int ::= minVals(Int, Vals) [function]` |
| `6494a8cd516dcc4f` | `reference-semantics/semantics/builtins.k:103-103` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| `efd996015d9f25a2` | `reference-semantics/semantics/builtins.k:104-104` | rule; none; fixed-semantic+ordinary-rule | `rule minVals(M:Int, .Vals) => M` |
| `5d0db3e42a365f64` | `reference-semantics/semantics/builtins.k:105-107` | rule; none; fixed-semantic+ordinary-rule | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| `675800a52ddfd799` | `reference-semantics/semantics/builtins.k:108-110` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` |
| `bab641e877dc62db` | `reference-semantics/semantics/builtins.k:111-113` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| `0828721b6d9dc60d` | `reference-semantics/semantics/builtins.k:114-114` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| `ca0989d3af2af8ce` | `reference-semantics/semantics/builtins.k:115-115` | rule; none; fixed-semantic+ordinary-rule | `rule binCodes(0) => iCons(48, .IntSeq)` |
| `c04454db7df05600` | `reference-semantics/semantics/builtins.k:116-116` | rule; none; fixed-semantic+ordinary-rule | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| `cae01e3bd26f455e` | `reference-semantics/semantics/builtins.k:117-117` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| `2569a98a5787be40` | `reference-semantics/semantics/builtins.k:118-118` | rule; none; fixed-semantic+ordinary-rule | `rule binAcc(0, ACC:IntSeq) => ACC` |
| `7aa34c45ff172780` | `reference-semantics/semantics/builtins.k:119-123` | rule; none; fixed-semantic+ordinary-rule | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` |
| `a526029da31db785` | `reference-semantics/semantics/builtins.k:124-125` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| `299c4f9429fadac8` | `reference-semantics/semantics/builtins.k:126-126` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| `ed114d050cb1acdc` | `reference-semantics/semantics/builtins.k:127-127` | rule; none; fixed-semantic+ordinary-rule | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| `3c7c50ffb5f5f005` | `reference-semantics/semantics/builtins.k:128-131` | rule; none; fixed-semantic+ordinary-rule | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` |
| `702a4bb7f951628c` | `reference-semantics/semantics/builtins.k:132-133` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| `852db701e07c886a` | `reference-semantics/semantics/builtins.k:134-134` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| `e5637c3c37250e17` | `reference-semantics/semantics/builtins.k:135-135` | rule; none; fixed-semantic+ordinary-rule | `rule mapStrVS(.ValSeq) => .ValSeq` |
| `a23bd99fa1dbd1ee` | `reference-semantics/semantics/builtins.k:136-136` | rule; none; fixed-semantic+ordinary-rule | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| `96e77db63ace191c` | `reference-semantics/semantics/builtins.k:137-139` | rule; none; fixed-semantic+ordinary-rule | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| `eca4f774ab434a5f` | `reference-semantics/semantics/builtins.k:140-142` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| `8ef7aba5c509c5f7` | `reference-semantics/semantics/builtins.k:143-143` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| `565a93233d0b217e` | `reference-semantics/semantics/builtins.k:144-147` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` |
| `d37972826368f345` | `reference-semantics/semantics/builtins.k:148-148` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))` |
| `aab0ae4c0b349647` | `reference-semantics/semantics/builtins.k:149-151` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| `460c8c0564363330` | `reference-semantics/semantics/builtins.k:152-155` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` |
| `f4fd1870a48b7be8` | `reference-semantics/semantics/builtins.k:156-157` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| `6d9afa1333807d8e` | `reference-semantics/semantics/builtins.k:158-158` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| `a369e22a902c44cb` | `reference-semantics/semantics/builtins.k:159-159` | rule; none; fixed-semantic+ordinary-rule | `rule intDigAcc(.IntSeq, ACC:Int) => ACC` |
| `26f27e644b6e8ec3` | `reference-semantics/semantics/builtins.k:160-162` | rule; none; fixed-semantic+ordinary-rule | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| `e258c4be689a27e3` | `reference-semantics/semantics/builtins.k:163-163` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| `b361200f9a8ba073` | `reference-semantics/semantics/builtins.k:164-166` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B)` |
| `f234c3f9eb15b747` | `reference-semantics/semantics/builtins.k:167-168` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| `2d6e77b1a73b2ce8` | `reference-semantics/semantics/builtins.k:169-169` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>` |
| `c3e93b685495d682` | `reference-semantics/semantics/builtins.k:170-170` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| `f20a3f0d0e511368` | `reference-semantics/semantics/builtins.k:171-172` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| `0347127e346345d3` | `reference-semantics/semantics/builtins.k:173-173` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>` |
| `12645447bad6d116` | `reference-semantics/semantics/builtins.k:174-176` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| `41e7d35b1742ae47` | `reference-semantics/semantics/builtins.k:177-177` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)` |
| `8b23721abfad0b46` | `reference-semantics/semantics/builtins.k:178-178` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)` |
| `13b497a3121e64f6` | `reference-semantics/semantics/builtins.k:179-186` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` |
| `20da5355a0fce5e1` | `reference-semantics/semantics/builtins.k:187-187` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| `51b632661d2d7a2f` | `reference-semantics/semantics/builtins.k:188-188` | syntax; function; syntax-declaration+function | `syntax Int ::= evalArith(IntSeq) [function]` |
| `d994524353fa05ee` | `reference-semantics/semantics/builtins.k:189-190` | rule; none; fixed-semantic+ordinary-rule | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| `32fd863b7241e3cc` | `reference-semantics/semantics/builtins.k:192-192` | syntax; none; syntax-declaration | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| `5a0f19acdbe46c4c` | `reference-semantics/semantics/builtins.k:194-194` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= evDigit(Int) [function, total]` |
| `6f277fb320c4e907` | `reference-semantics/semantics/builtins.k:195-195` | rule; none; fixed-semantic+ordinary-rule | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `2ad0d6458124078d` | `reference-semantics/semantics/builtins.k:196-196` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| `923907ff3213a8bf` | `reference-semantics/semantics/builtins.k:197-197` | rule; none; fixed-semantic+ordinary-rule | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| `81c22b20b33db623` | `reference-semantics/semantics/builtins.k:198-198` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule evHead42(_:IntSeq) => false [owise]` |
| `de6b7acad8920b46` | `reference-semantics/semantics/builtins.k:199-199` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| `304ac4cafe811702` | `reference-semantics/semantics/builtins.k:200-200` | rule; none; fixed-semantic+ordinary-rule | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| `c6965052f275c2e3` | `reference-semantics/semantics/builtins.k:201-201` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule evHead47(_:IntSeq) => false [owise]` |
| `04630eaa4885e064` | `reference-semantics/semantics/builtins.k:203-203` | syntax; function,total; syntax-declaration+function+total | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| `bb3c0c227da6e66b` | `reference-semantics/semantics/builtins.k:204-204` | rule; none; fixed-semantic+ordinary-rule | `rule tokOps(.IntSeq) => .OpSeq` |
| `678f603564bf45ff` | `reference-semantics/semantics/builtins.k:205-205` | rule; none; fixed-semantic+ordinary-rule | `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)` |
| `6247967eebb3307c` | `reference-semantics/semantics/builtins.k:206-206` | rule; none; fixed-semantic+ordinary-rule | `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)` |
| `5a6928e92f25ca49` | `reference-semantics/semantics/builtins.k:207-207` | rule; none; fixed-semantic+ordinary-rule | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| `ceae33f4fce466cd` | `reference-semantics/semantics/builtins.k:208-208` | rule; none; fixed-semantic+ordinary-rule | `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| `247640370dc0a71b` | `reference-semantics/semantics/builtins.k:209-209` | rule; none; fixed-semantic+ordinary-rule | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| `a6672cde16c62331` | `reference-semantics/semantics/builtins.k:210-210` | rule; none; fixed-semantic+ordinary-rule | `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| `f7aec14e1995864f` | `reference-semantics/semantics/builtins.k:211-211` | rule; none; fixed-semantic+ordinary-rule | `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))` |
| `d6c4ac8bbf21f625` | `reference-semantics/semantics/builtins.k:212-212` | rule; none; fixed-semantic+ordinary-rule | `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))` |
| `6fc46a24325be6af` | `reference-semantics/semantics/builtins.k:214-215` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| `8d7a933400eadd8e` | `reference-semantics/semantics/builtins.k:216-216` | rule; none; fixed-semantic+ordinary-rule | `rule tokNds(.IntSeq) => .IntSeq` |
| `ca5ff31bb3269e3d` | `reference-semantics/semantics/builtins.k:217-217` | rule; none; fixed-semantic+ordinary-rule | `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)` |
| `39b57c20ca0c2089` | `reference-semantics/semantics/builtins.k:218-218` | rule; none; fixed-semantic+ordinary-rule | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| `6a1156f22de377ad` | `reference-semantics/semantics/builtins.k:219-220` | rule; none; fixed-semantic+ordinary-rule | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| `86d161269b94a8ca` | `reference-semantics/semantics/builtins.k:221-222` | rule; none; fixed-semantic+ordinary-rule | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| `a665f343044caea9` | `reference-semantics/semantics/builtins.k:223-223` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| `ad5eb4fb95cdd5eb` | `reference-semantics/semantics/builtins.k:225-225` | syntax; none; syntax-declaration | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| `4598c9129a465de0` | `reference-semantics/semantics/builtins.k:226-226` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| `de53f0bb43800ee1` | `reference-semantics/semantics/builtins.k:227-227` | rule; none; fixed-semantic+ordinary-rule | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| `f0b011f2143ceac6` | `reference-semantics/semantics/builtins.k:228-228` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule firstNdE(_:EvPair) => 0 [owise]` |
| `466cc6c5b82b2492` | `reference-semantics/semantics/builtins.k:230-230` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| `00690a65ec768800` | `reference-semantics/semantics/builtins.k:231-231` | rule; none; fixed-semantic+ordinary-rule | `rule applyOpE("+", A:Int, B:Int) => A +Int B` |
| `a4e62e575d18c2fb` | `reference-semantics/semantics/builtins.k:232-232` | rule; none; fixed-semantic+ordinary-rule | `rule applyOpE("-", A:Int, B:Int) => A -Int B` |
| `65863c517fd30367` | `reference-semantics/semantics/builtins.k:233-233` | rule; none; fixed-semantic+ordinary-rule | `rule applyOpE("*", A:Int, B:Int) => A *Int B` |
| `15aeedde3449d1de` | `reference-semantics/semantics/builtins.k:234-234` | rule; none; fixed-semantic+ordinary-rule | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| `149844234e578269` | `reference-semantics/semantics/builtins.k:235-235` | rule; none; fixed-semantic+ordinary-rule | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| `124063830531122b` | `reference-semantics/semantics/builtins.k:236-236` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| `32410a2b1380d0b8` | `reference-semantics/semantics/builtins.k:238-238` | syntax; function,total; syntax-declaration+function+total | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| `f76cf01b464526a0` | `reference-semantics/semantics/builtins.k:239-239` | rule; none; fixed-semantic+ordinary-rule | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| `01c728fd4edd2667` | `reference-semantics/semantics/builtins.k:240-240` | rule; none; fixed-semantic+ordinary-rule | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| `e04a040b7f7e68a4` | `reference-semantics/semantics/builtins.k:241-242` | rule; none; fixed-semantic+ordinary-rule | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| `13cb4514123c1257` | `reference-semantics/semantics/builtins.k:243-243` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| `f0efe5de8e10af5e` | `reference-semantics/semantics/builtins.k:244-244` | syntax; function,total; syntax-declaration+function+total | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| `ea7f9d362a300546` | `reference-semantics/semantics/builtins.k:245-245` | rule; none; fixed-semantic+ordinary-rule | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| `3309f96be1a2785b` | `reference-semantics/semantics/builtins.k:246-246` | rule; none; fixed-semantic+ordinary-rule | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| `97a30a9531ac4e5f` | `reference-semantics/semantics/builtins.k:247-247` | syntax; function,total; syntax-declaration+function+total | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| `1e2c7505839efbfb` | `reference-semantics/semantics/builtins.k:248-248` | rule; none; fixed-semantic+ordinary-rule | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| `bcd433e78c3df55a` | `reference-semantics/semantics/builtins.k:250-250` | syntax; function,total; syntax-declaration+function+total | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| `fb64f01c7321fac4` | `reference-semantics/semantics/builtins.k:251-251` | rule; none; fixed-semantic+ordinary-rule | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `a4e5f5a048664dc0` | `reference-semantics/semantics/builtins.k:252-252` | rule; none; fixed-semantic+ordinary-rule | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `69980e4b3a4220d0` | `reference-semantics/semantics/builtins.k:253-253` | rule; none; fixed-semantic+ordinary-rule | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `576903e0c20dc2d9` | `reference-semantics/semantics/builtins.k:254-254` | rule; none; fixed-semantic+ordinary-rule | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `4aafb465922cc622` | `reference-semantics/semantics/builtins.k:255-255` | syntax; function,total; syntax-declaration+function+total | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| `3163a73c07a9cd83` | `reference-semantics/semantics/builtins.k:256-256` | rule; none; fixed-semantic+ordinary-rule | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| `02ad947374070b61` | `reference-semantics/semantics/builtins.k:257-259` | rule; none; fixed-semantic+ordinary-rule | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| `5fad413f22de6121` | `reference-semantics/semantics/builtins.k:260-262` | rule; none; fixed-semantic+ordinary-rule | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| `74bdc22240a07c56` | `reference-semantics/semantics/builtins.k:263-264` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| `1a7f91b5e966889d` | `reference-semantics/semantics/builtins.k:265-265` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| `4310a9aa3d775fa2` | `reference-semantics/semantics/builtins.k:266-266` | rule; none; fixed-semantic+ordinary-rule | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| `9a8ba2507e9309d8` | `reference-semantics/semantics/builtins.k:267-267` | rule; none; fixed-semantic+ordinary-rule | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| `06593d1347e80759` | `reference-semantics/semantics/builtins.k:268-268` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule inLevelE(_:String, _:String) => false [owise]` |
| `a2e938d9186bc9ba` | `reference-semantics/semantics/builtins.k:269-269` | syntax; function,total; syntax-declaration+function+total | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| `bf505833c4ccea5f` | `reference-semantics/semantics/builtins.k:270-270` | rule; none; fixed-semantic+ordinary-rule | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| `170955dbca412293` | `reference-semantics/semantics/builtins.k:271-271` | rule; none; fixed-semantic+ordinary-rule | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| `f872814c8e17b8cb` | `reference-semantics/semantics/builtins.k:272-272` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| `a7a39392db27b702` | `reference-semantics/semantics/builtins.k:273-273` | rule; none; fixed-semantic+ordinary-rule | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| `b2ba6c294bda471f` | `reference-semantics/semantics/builtins.k:274-278` | rule; none; fixed-semantic+ordinary-rule | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| `ff8d2495e2fbb504` | `reference-semantics/semantics/builtins.k:279-279` | syntax; none; syntax-declaration | `syntax KItem ::= "#md5"` |
| `3fb0cac094a085dd` | `reference-semantics/semantics/builtins.k:280-281` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| `6a717834db5e76dd` | `reference-semantics/semantics/builtins.k:282-282` | rule; none; fixed-semantic+ordinary-rule | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| `424a888bdd2b03bf` | `reference-semantics/semantics/builtins.k:283-283` | syntax; none; syntax-declaration | `syntax Val ::= md5Obj(IntSeq)` |
| `10a5e50b4f9b488f` | `reference-semantics/semantics/builtins.k:284-284` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| `479b3d31363253a3` | `reference-semantics/semantics/builtins.k:285-290` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| `b464996768f1c59c` | `reference-semantics/semantics/builtins.k:291-291` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| `7c91f857a4af3fa8` | `reference-semantics/semantics/builtins.k:292-292` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| `809814f2132c9ba6` | `reference-semantics/semantics/builtins.k:293-293` | syntax; function; syntax-declaration+function | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| `325ab95f0f733980` | `reference-semantics/semantics/builtins.k:294-294` | rule; none; fixed-semantic+ordinary-rule | `rule isIntV(_:Int) => true` |
| `92105f3790376454` | `reference-semantics/semantics/builtins.k:295-295` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule isIntV(_:Val) => false [owise]` |
| `b0415f249643d3d8` | `reference-semantics/semantics/builtins.k:296-296` | rule; none; fixed-semantic+ordinary-rule | `rule isStrV(str(_:IntSeq)) => true` |
| `ab8db1be294d1ccd` | `reference-semantics/semantics/builtins.k:297-297` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule isStrV(_:Val) => false [owise]` |
| `725bde93634526cf` | `reference-semantics/semantics/call.k:16-18` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| `d1f7ab7d0f4397a1` | `reference-semantics/semantics/call.k:19-19` | syntax; none; syntax-declaration | `syntax KItem ::= #callee(Exprs)` |
| `8fecdc76400f6c3a` | `reference-semantics/semantics/call.k:20-20` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| `80d3eac8aba4e288` | `reference-semantics/semantics/call.k:21-23` | rule; none; fixed-semantic+ordinary-rule | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| `74ea371bb8f5f209` | `reference-semantics/semantics/call.k:24-24` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| `22297e3480a41702` | `reference-semantics/semantics/call.k:26-26` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| `c5f332a687bb08e6` | `reference-semantics/semantics/call.k:27-27` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>` |
| `95bbd7b665d52550` | `reference-semantics/semantics/call.k:28-28` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>` |
| `b83825e4bbb6afdb` | `reference-semantics/semantics/call.k:29-29` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>` |
| `bb075cdaef21579d` | `reference-semantics/semantics/call.k:30-30` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>` |
| `50e438ae7231cd0a` | `reference-semantics/semantics/call.k:31-31` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| `0810212cbd10b2bf` | `reference-semantics/semantics/call.k:32-37` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k>` |
| `538630eb2d91bf4b` | `reference-semantics/semantics/call.k:38-41` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `f503621be45783d4` | `reference-semantics/semantics/call.k:42-46` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| `aad62437a644c39a` | `reference-semantics/semantics/call.k:47-50` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `9d7988bf2c5d19be` | `reference-semantics/semantics/call.k:52-52` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= isMutMethod(String) [function, total]` |
| `b5787f38c3842b4f` | `reference-semantics/semantics/call.k:53-55` | rule; none; fixed-semantic+ordinary-rule | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| `cc9ee0d0b42663ca` | `reference-semantics/semantics/call.k:56-62` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` |
| `b686c25fa1c24377` | `reference-semantics/semantics/call.k:63-67` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| `e2453a86a1cfee9c` | `reference-semantics/semantics/call.k:69-79` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| `52d15d9a6aff1391` | `reference-semantics/semantics/call.k:80-85` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| `808dff0bb67cdb75` | `reference-semantics/semantics/call.k:87-87` | syntax; none; syntax-declaration | `syntax KItem ::= #allocCells(ParamNames)` |
| `944e5b61dc6f7b46` | `reference-semantics/semantics/call.k:88-88` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| `bac57097cbf06239` | `reference-semantics/semantics/call.k:89-94` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| `c242e6d30efa14e2` | `reference-semantics/semantics/comprehension.k:11-11` | rule; none; fixed-semantic+ordinary-rule | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `8e13e7129a14a0c0` | `reference-semantics/semantics/comprehension.k:12-12` | rule; none; fixed-semantic+ordinary-rule | `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `844cc4a0bef992c1` | `reference-semantics/semantics/comprehension.k:14-14` | syntax; macro; macro-or-alias | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| `cb47e20214da1a14` | `reference-semantics/semantics/comprehension.k:15-16` | rule; none; fixed-semantic+ordinary-rule | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| `6ff019a443c2e5b0` | `reference-semantics/semantics/comprehension.k:18-18` | syntax; macro; macro-or-alias | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| `b2ac8bc5bbf8a3b9` | `reference-semantics/semantics/comprehension.k:19-20` | rule; none; fixed-semantic+ordinary-rule | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| `63ab35d155e4ba59` | `reference-semantics/semantics/comprehension.k:21-22` | rule; none; fixed-semantic+ordinary-rule | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| `4feb040c88e1a8be` | `reference-semantics/semantics/comprehension.k:24-24` | syntax; macro; macro-or-alias | `syntax Expr ::= compGuard(Exprs) [macro]` |
| `4bb7c611e6745d72` | `reference-semantics/semantics/comprehension.k:25-25` | rule; none; fixed-semantic+ordinary-rule | `rule compGuard(.Exprs) => Bool(true)` |
| `753c0c03bf73a1e1` | `reference-semantics/semantics/comprehension.k:26-26` | rule; none; fixed-semantic+ordinary-rule | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| `0751fc4503754a77` | `reference-semantics/semantics/concrete.k:13-15` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| `065d0ce849021004` | `reference-semantics/semantics/concrete.k:16-24` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| `f95ee23c21d40e1e` | `reference-semantics/semantics/concrete.k:25-25` | syntax; none; syntax-declaration | `syntax Val ::= kvP(Val, Val)` |
| `2ba54268b6f65995` | `reference-semantics/semantics/concrete.k:26-27` | syntax; none; syntax-declaration | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| `0757a4636ec858e2` | `reference-semantics/semantics/concrete.k:28-30` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| `c915de6fbf890445` | `reference-semantics/semantics/concrete.k:31-33` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| `4faa6808af757158` | `reference-semantics/semantics/concrete.k:34-35` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| `4e5fc14dc3daed83` | `reference-semantics/semantics/concrete.k:36-37` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| `e5ff8ddceb0fb422` | `reference-semantics/semantics/concrete.k:38-40` | rule; none; fixed-semantic+ordinary-rule | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| `13f2b1e6b724dace` | `reference-semantics/semantics/concrete.k:42-42` | syntax; function; syntax-declaration+function | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| `5c88ae0ed01648d1` | `reference-semantics/semantics/concrete.k:43-43` | rule; none; fixed-semantic+ordinary-rule | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| `3a79633f7762f4db` | `reference-semantics/semantics/concrete.k:44-46` | rule; none; fixed-semantic+ordinary-rule | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| `a331212401a678b1` | `reference-semantics/semantics/concrete.k:47-49` | rule; none; fixed-semantic+ordinary-rule | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| `77c18609fa600ed7` | `reference-semantics/semantics/concrete.k:51-51` | syntax; function; syntax-declaration+function | `syntax Bool ::= kLt(Val, Val) [function]` |
| `20ac928d8ae3a1e0` | `reference-semantics/semantics/concrete.k:52-52` | rule; none; fixed-semantic+ordinary-rule | `rule kLt(I1:Int, I2:Int) => I1 <Int I2` |
| `ee46dec38e4856cf` | `reference-semantics/semantics/concrete.k:53-53` | rule; none; fixed-semantic+ordinary-rule | `rule kLt(F1:Float, F2:Float) => F1 <Float F2` |
| `62efb909c60243cd` | `reference-semantics/semantics/concrete.k:54-54` | rule; none; fixed-semantic+ordinary-rule | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `c72a6120b905ee21` | `reference-semantics/semantics/concrete.k:56-56` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| `2812f38938027592` | `reference-semantics/semantics/concrete.k:57-57` | rule; none; fixed-semantic+ordinary-rule | `rule unpairVS(.ValSeq) => .ValSeq` |
| `bfbae234308a0269` | `reference-semantics/semantics/concrete.k:58-58` | rule; none; fixed-semantic+ordinary-rule | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| `215cdfd6c2ec9343` | `reference-semantics/semantics/concrete.k:59-59` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| `f21002cb58ff71cf` | `reference-semantics/semantics/controls.k:9-11` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| `8fd7fa1515c5af05` | `reference-semantics/semantics/controls.k:12-18` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| `2d28c8f9234508ff` | `reference-semantics/semantics/controls.k:20-26` | rule; none; fixed-semantic+ordinary-rule | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` |
| `a901ecc214b3d0d8` | `reference-semantics/semantics/controls.k:27-34` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]` |
| `a723d3702a991dac` | `reference-semantics/semantics/controls.k:35-35` | rule; none; fixed-semantic+ordinary-rule | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| `872b50dc26fe5953` | `reference-semantics/semantics/controls.k:36-36` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| `b3a7bf23dc0325ba` | `reference-semantics/semantics/controls.k:37-37` | syntax; none; syntax-declaration | `syntax KItem ::= #bindImports(ParamNames)` |
| `32efd2f0f9d07205` | `reference-semantics/semantics/controls.k:38-38` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| `1ff6bd78289bc4f4` | `reference-semantics/semantics/controls.k:39-42` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| `151a75b8e50cc080` | `reference-semantics/semantics/controls.k:43-47` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` |
| `1cf7c009861ac9aa` | `reference-semantics/semantics/controls.k:48-50` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Expr(_:Val) => .K ... </k>` |
| `1e7e7017b9f1d65f` | `reference-semantics/semantics/controls.k:51-51` | syntax; none; syntax-declaration | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| `4c922fa231effc54` | `reference-semantics/semantics/controls.k:52-52` | rule; none; fixed-semantic+ordinary-rule | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| `ba3099460c6d33b2` | `reference-semantics/semantics/controls.k:53-53` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>` |
| `fd7256024f42fc4c` | `reference-semantics/semantics/controls.k:54-56` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| `bcc7d5197c5292c2` | `reference-semantics/semantics/controls.k:57-58` | rule; none; fixed-semantic+ordinary-rule | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| `6d9153016b562f15` | `reference-semantics/semantics/controls.k:59-64` | rule; none; fixed-semantic+ordinary-rule | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` |
| `1ad74297e4901d8a` | `reference-semantics/semantics/controls.k:65-67` | syntax; none; syntax-declaration | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| `60244ec44f2e568b` | `reference-semantics/semantics/controls.k:69-69` | rule; none; fixed-semantic+ordinary-rule | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| `d61cf4d9acc363c6` | `reference-semantics/semantics/controls.k:71-71` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| `b3b04623e5122daf` | `reference-semantics/semantics/controls.k:72-72` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| `1cddeb542429769b` | `reference-semantics/semantics/controls.k:73-76` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` |
| `3fe05d38fca6cae6` | `reference-semantics/semantics/controls.k:77-77` | rule; none; fixed-semantic+ordinary-rule | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| `407e02196cb49b2a` | `reference-semantics/semantics/controls.k:78-78` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| `73a85b07f3e9b280` | `reference-semantics/semantics/controls.k:79-80` | rule; none; fixed-semantic+ordinary-rule | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| `aeb806979449afc3` | `reference-semantics/semantics/controls.k:81-84` | rule; none; fixed-semantic+ordinary-rule | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` |
| `2b4a8a98e931b52f` | `reference-semantics/semantics/controls.k:85-85` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `3013980243c51e30` | `reference-semantics/semantics/controls.k:86-86` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Continue => #cont ... </k>` |
| `5e2cf2a6750a4918` | `reference-semantics/semantics/controls.k:87-87` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Break => #brk ... </k>` |
| `d93bc620b6633b3d` | `reference-semantics/semantics/controls.k:88-88` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `dd3f28d8cd921631` | `reference-semantics/semantics/controls.k:89-89` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| `12a57b17267f5075` | `reference-semantics/semantics/controls.k:90-90` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| `8b4f60987f7aadaa` | `reference-semantics/semantics/controls.k:91-94` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| `ca1d9bc712f89ad0` | `reference-semantics/semantics/controls.k:95-97` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `b9b9051c5e0ae3b4` | `reference-semantics/semantics/controls.k:98-100` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `eddcfc697379f8b6` | `reference-semantics/semantics/controls.k:101-105` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `b0ee670333d939b1` | `reference-semantics/semantics/controls.k:106-108` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `3f8f0bc7bfdfb931` | `reference-semantics/semantics/core.k:13-13` | syntax; none; syntax-declaration | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| `898e15a3c72fbe1a` | `reference-semantics/semantics/core.k:14-14` | syntax; none; syntax-declaration | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| `9124dead059a8571` | `reference-semantics/semantics/core.k:15-17` | syntax; none; syntax-declaration | `syntax Str ::= str(IntSeq)` |
| `c9946ddf15bf179e` | `reference-semantics/semantics/core.k:18-23` | syntax; none; syntax-declaration | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| `6b384cd90ba07dc9` | `reference-semantics/semantics/core.k:25-34` | syntax; none; syntax-declaration | `syntax Val ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) \| cellRef(Int) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) \| builtinV(String) \| boundMethodV(Val, String)` |
| `d801fd764f1ed49d` | `reference-semantics/semantics/core.k:36-36` | syntax; none; syntax-declaration | `syntax Parent ::= "root" \| parent(Int)` |
| `796aa7a72fb190eb` | `reference-semantics/semantics/core.k:37-37` | syntax; none; syntax-declaration | `syntax Scope ::= scope(Map, Parent)` |
| `01deb462a81b39a6` | `reference-semantics/semantics/core.k:38-38` | syntax; none; syntax-declaration | `syntax KResult ::= Val` |
| `1aad04b07800c2d2` | `reference-semantics/semantics/core.k:39-39` | syntax; none; syntax-declaration | `syntax Expr ::= Val` |
| `98e0dc762b7996f4` | `reference-semantics/semantics/core.k:40-40` | syntax; none; syntax-declaration | `syntax Vals ::= List{Val, ","}` |
| `61695d7bf043899e` | `reference-semantics/semantics/core.k:41-41` | syntax; none; syntax-declaration | `syntax Exc ::= "NoExc" \| "AssertionError"` |
| `b0ff967d2bfffa5b` | `reference-semantics/semantics/core.k:42-48` | syntax; none; syntax-declaration | `syntax RetState ::= "noRet" \| retV(Val)` |
| `0a686f1a987d72df` | `reference-semantics/semantics/core.k:49-67` | configuration; none; configuration | `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code>` |
| `55c8b371207e5de6` | `reference-semantics/semantics/core.k:68-68` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= isRefV(Val) [function, total]` |
| `09d12eed60001e68` | `reference-semantics/semantics/core.k:69-69` | rule; none; fixed-semantic+ordinary-rule | `rule isRefV(ref(_:Int)) => true` |
| `dbefb0c672a00b48` | `reference-semantics/semantics/core.k:70-74` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule isRefV(_:Val) => false [owise]` |
| `9fc3080241754e43` | `reference-semantics/semantics/core.k:75-75` | syntax; none; syntax-declaration | `syntax HeapVal ::= cellV(Val)` |
| `c1546bc506d85435` | `reference-semantics/semantics/core.k:76-76` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= isCellRef(Val) [function, total]` |
| `c640c5bd46f33608` | `reference-semantics/semantics/core.k:77-77` | rule; none; fixed-semantic+ordinary-rule | `rule isCellRef(cellRef(_:Int)) => true` |
| `40a44f311d691235` | `reference-semantics/semantics/core.k:78-84` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule isCellRef(_:Val) => false [owise]` |
| `c67c62b15affc867` | `reference-semantics/semantics/core.k:85-94` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` |
| `575741e4db9fdfe4` | `reference-semantics/semantics/core.k:95-95` | syntax; none; syntax-declaration | `syntax Val ::= kwV(String, Val)` |
| `6723f28594ca54d9` | `reference-semantics/semantics/core.k:96-96` | syntax; none; syntax-declaration | `syntax KItem ::= #kwTag(String)` |
| `5839095a518bfa5d` | `reference-semantics/semantics/core.k:97-97` | rule; none; fixed-semantic+ordinary-rule | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| `de6cedd55b3f24e3` | `reference-semantics/semantics/core.k:98-99` | rule; none; fixed-semantic+ordinary-rule | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| `b8cd5d8cfc795d70` | `reference-semantics/semantics/core.k:100-100` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= isKwV(Val) [function, total]` |
| `9b1dc1a19249f8a7` | `reference-semantics/semantics/core.k:101-101` | rule; none; fixed-semantic+ordinary-rule | `rule isKwV(kwV(_:String, _:Val)) => true` |
| `ea24fbbbe186abd8` | `reference-semantics/semantics/core.k:102-105` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule isKwV(_:Val) => false [owise]` |
| `abfa0a5e6f101103` | `reference-semantics/semantics/core.k:106-106` | syntax; none; syntax-declaration | `syntax Val ::= cellsMark(ParamNames)` |
| `a10952f78c433683` | `reference-semantics/semantics/core.k:107-107` | syntax; function; syntax-declaration+function | `syntax ParamNames ::= cellsOf(Val) [function]` |
| `fd7653eb4aa3f3ab` | `reference-semantics/semantics/core.k:108-108` | rule; none; fixed-semantic+ordinary-rule | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| `01a311fde23c4492` | `reference-semantics/semantics/core.k:109-109` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| `2ceef043ca51ec15` | `reference-semantics/semantics/core.k:110-110` | rule; none; fixed-semantic+ordinary-rule | `rule pnMember(_:String, .ParamNames) => false` |
| `bbcc01fd06f7e883` | `reference-semantics/semantics/core.k:111-111` | rule; none; fixed-semantic+ordinary-rule | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| `b12125474e2b136d` | `reference-semantics/semantics/core.k:113-113` | syntax; none; syntax-declaration | `syntax KItem ::= #cellW(Val, Val)` |
| `a45a00e094188a00` | `reference-semantics/semantics/core.k:114-115` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| `d6a80ac78d5bbe01` | `reference-semantics/semantics/core.k:117-117` | syntax; none; syntax-declaration | `syntax KItem ::= #alloc(Val)` |
| `2e26c307ea632f7d` | `reference-semantics/semantics/core.k:118-123` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| `df3f479665e81ce7` | `reference-semantics/semantics/core.k:124-124` | syntax; none; syntax-declaration | `syntax KItem ::= #loadAll(Module)` |
| `3775a747e8f81f4b` | `reference-semantics/semantics/core.k:125-125` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| `ded4ac10a122c872` | `reference-semantics/semantics/core.k:126-126` | rule; none; fixed-semantic+ordinary-rule | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| `413651bea65853f7` | `reference-semantics/semantics/core.k:127-129` | rule; none; fixed-semantic+ordinary-rule | `rule <k> .Stmts => .K ... </k>` |
| `0e3d3fe6c94b1464` | `reference-semantics/semantics/core.k:130-130` | syntax; none; syntax-declaration | `syntax KItem ::= #look(String, Int)` |
| `4f12616023a66449` | `reference-semantics/semantics/core.k:131-131` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| `b39695218e72ae41` | `reference-semantics/semantics/core.k:132-144` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` |
| `5a376f4934bbb74c` | `reference-semantics/semantics/core.k:145-151` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| `fc9712cb11be6037` | `reference-semantics/semantics/core.k:152-156` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` |
| `6d0dfe236575e057` | `reference-semantics/semantics/core.k:157-157` | syntax; function,total; syntax-declaration+function+total | `syntax Scope ::= "builtinsScope" [function, total]` |
| `401b2f9674ef288a` | `reference-semantics/semantics/core.k:158-184` | rule; none; fixed-semantic+ordinary-rule | `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root)` |
| `2e9f9a73acd7a081` | `reference-semantics/semantics/core.k:185-185` | syntax; none; syntax-declaration | `syntax ApplyK ::= toCall(Val)` |
| `1d09ac19bd89f19c` | `reference-semantics/semantics/core.k:186-188` | syntax; none; syntax-declaration | `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| `46bfb0513bcaf560` | `reference-semantics/semantics/core.k:189-189` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| `e97088c38f4e9a59` | `reference-semantics/semantics/core.k:190-190` | rule; none; fixed-semantic+ordinary-rule | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| `fab05d368095e912` | `reference-semantics/semantics/core.k:191-193` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| `4ec1bde2809c79ae` | `reference-semantics/semantics/core.k:194-194` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Int(I:Int) => I ... </k>` |
| `3d99eae3e73483fd` | `reference-semantics/semantics/core.k:195-195` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Bool(B:Bool) => B ... </k>` |
| `6734534bdb7c4812` | `reference-semantics/semantics/core.k:196-198` | rule; none; fixed-semantic+ordinary-rule | `rule <k> NoneVal => noneV ... </k>` |
| `811c386a5ac173a4` | `reference-semantics/semantics/core.k:199-199` | syntax; function; syntax-declaration+function | `syntax Bool ::= truthy(Val) [function]` |
| `e42256ed399af459` | `reference-semantics/semantics/core.k:200-200` | rule; none; fixed-semantic+ordinary-rule | `rule truthy(B:Bool) => B` |
| `05d404421cde7f80` | `reference-semantics/semantics/core.k:201-201` | rule; none; fixed-semantic+ordinary-rule | `rule truthy(noneV) => false` |
| `eb7027323afa3227` | `reference-semantics/semantics/core.k:202-202` | rule; none; fixed-semantic+ordinary-rule | `rule truthy(I:Int) => I =/=Int 0` |
| `db224456ce9c7477` | `reference-semantics/semantics/core.k:203-203` | rule; none; fixed-semantic+ordinary-rule | `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)` |
| `6994c292e69f32eb` | `reference-semantics/semantics/core.k:204-204` | rule; none; fixed-semantic+ordinary-rule | `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| `865cef374604a265` | `reference-semantics/semantics/core.k:205-207` | rule; none; fixed-semantic+ordinary-rule | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| `26cfad6b9ccb2a40` | `reference-semantics/semantics/core.k:208-208` | syntax; function; syntax-declaration+function | `syntax Val ::= applyUn(String, Val) [function]` |
| `cd061697df8a19f3` | `reference-semantics/semantics/core.k:209-209` | syntax; function; syntax-declaration+function | `syntax Val ::= applyBin(String, Val, Val) [function]` |
| `50bd20e5e20b9c62` | `reference-semantics/semantics/core.k:210-212` | syntax; function; syntax-declaration+function | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| `f57ec7d82e43cc78` | `reference-semantics/semantics/core.k:213-213` | syntax; function,total; syntax-declaration+function+total | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| `6eae9a2ce540e483` | `reference-semantics/semantics/core.k:214-214` | rule; none; fixed-semantic+ordinary-rule | `rule appendVal(.Vals, V:Val) => V , .Vals` |
| `ffcb0b50d3b67d44` | `reference-semantics/semantics/core.k:215-215` | rule; none; fixed-semantic+ordinary-rule | `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)` |
| `04fc2b0ea8f966ff` | `reference-semantics/semantics/core.k:217-217` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| `e73932e583830d99` | `reference-semantics/semantics/core.k:218-218` | rule; none; fixed-semantic+ordinary-rule | `rule vals2valSeq(.Vals) => .ValSeq` |
| `5e8e89b63c7ca649` | `reference-semantics/semantics/core.k:219-222` | rule; none; fixed-semantic+ordinary-rule | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| `cbbada8786e61f87` | `reference-semantics/semantics/core.k:223-223` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| `b5bf738435d0432a` | `reference-semantics/semantics/core.k:224-224` | rule; none; fixed-semantic+ordinary-rule | `rule vsLen(.ValSeq) => 0` |
| `50d4533579dbc941` | `reference-semantics/semantics/core.k:225-225` | rule; none; fixed-semantic+ordinary-rule | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| `99c10f0bb9c0295b` | `reference-semantics/semantics/core.k:227-227` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= isLen(IntSeq) [function, total]` |
| `4163c7081afba768` | `reference-semantics/semantics/core.k:228-228` | rule; none; fixed-semantic+ordinary-rule | `rule isLen(.IntSeq) => 0` |
| `6adc807c0df8e4d2` | `reference-semantics/semantics/core.k:229-232` | rule; none; fixed-semantic+ordinary-rule | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| `86a83e44652799f8` | `reference-semantics/semantics/core.k:233-233` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| `b62d23afa8d3a010` | `reference-semantics/semantics/core.k:234-234` | rule; none; fixed-semantic+ordinary-rule | `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq` |
| `92128ad446c7ec23` | `reference-semantics/semantics/core.k:235-235` | rule; none; fixed-semantic+ordinary-rule | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)` |
| `13ed0c6d2ec034a3` | `reference-semantics/semantics/core.k:236-237` | rule; none; fixed-semantic+ordinary-rule | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| `bd5ecd3ee5d9b2be` | `reference-semantics/semantics/core.k:238-239` | rule; none; fixed-semantic+ordinary-rule | `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0` |
| `4f6d31758a19d3df` | `reference-semantics/semantics/dict.k:20-22` | syntax; none; syntax-declaration | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| `8bb4aadc4215ef17` | `reference-semantics/semantics/dict.k:23-25` | syntax; none; syntax-declaration | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| `614bff9dd4458185` | `reference-semantics/semantics/dict.k:26-26` | rule; none; fixed-semantic+ordinary-rule | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| `d3090eea8740fcf9` | `reference-semantics/semantics/dict.k:27-27` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| `d11c786b7d68e958` | `reference-semantics/semantics/dict.k:28-29` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| `51e5aba6e06401da` | `reference-semantics/semantics/dict.k:30-31` | rule; none; fixed-semantic+ordinary-rule | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| `be3b2bccaa740197` | `reference-semantics/semantics/dict.k:32-36` | rule; none; fixed-semantic+ordinary-rule | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` |
| `5d41b0b265785441` | `reference-semantics/semantics/dict.k:37-37` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| `7e79f3e321f9bd8a` | `reference-semantics/semantics/dict.k:38-38` | rule; none; fixed-semantic+ordinary-rule | `rule dHasKey(.ValSeq, _:Val) => false` |
| `128a5d08d4db481c` | `reference-semantics/semantics/dict.k:39-39` | rule; none; fixed-semantic+ordinary-rule | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K` |
| `81b9089fe0f18d00` | `reference-semantics/semantics/dict.k:40-42` | rule; none; fixed-semantic+ordinary-rule | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| `62577bb36e61b12b` | `reference-semantics/semantics/dict.k:43-43` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| `a02b45024d0dd3c9` | `reference-semantics/semantics/dict.k:44-44` | rule; none; fixed-semantic+ordinary-rule | `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)` |
| `6101f4a16620d6b4` | `reference-semantics/semantics/dict.k:45-48` | rule; none; fixed-semantic+ordinary-rule | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| `a7b085264c44354d` | `reference-semantics/semantics/dict.k:49-49` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| `25fc26ea986fa0b0` | `reference-semantics/semantics/dict.k:50-51` | rule; none; fixed-semantic+ordinary-rule | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K` |
| `baa3edec22fdc74e` | `reference-semantics/semantics/dict.k:52-53` | rule; none; fixed-semantic+ordinary-rule | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| `fe6fecf0d1c09063` | `reference-semantics/semantics/dict.k:54-57` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| `5fedbea72f8f807c` | `reference-semantics/semantics/dict.k:58-62` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` |
| `e6b7984fd24b46d6` | `reference-semantics/semantics/dict.k:63-63` | rule; none; fixed-semantic+ordinary-rule | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| `faca222cb38def35` | `reference-semantics/semantics/dict.k:64-64` | syntax; function; syntax-declaration+function | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| `56db8dd24d7971b4` | `reference-semantics/semantics/dict.k:65-69` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` |
| `9da886d1fb7593bd` | `reference-semantics/semantics/dict.k:70-70` | syntax; function; syntax-declaration+function | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| `8f2e666a07f69fbb` | `reference-semantics/semantics/dict.k:71-75` | rule; none; fixed-semantic+ordinary-rule | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| `fff2a14e7ad734a3` | `reference-semantics/semantics/dict.k:76-76` | syntax; none; syntax-declaration | `syntax KItem ::= #dsetK(String, Val)` |
| `47ebb4864d28fa76` | `reference-semantics/semantics/dict.k:77-77` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| `1836a07f505ce258` | `reference-semantics/semantics/dict.k:78-81` | rule; none; fixed-semantic+ordinary-rule | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| `42c09b78b58a2bcd` | `reference-semantics/semantics/dict.k:82-85` | rule; none; fixed-semantic+ordinary-rule | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| `c7d7448a9a0a9b19` | `reference-semantics/semantics/dict.k:86-86` | syntax; none; syntax-declaration | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| `c1cb7f5b1a0db6f7` | `reference-semantics/semantics/dict.k:87-89` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` |
| `ec3308f4a4f3324e` | `reference-semantics/semantics/dict.k:90-90` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| `b2ea340a2ea5f1a5` | `reference-semantics/semantics/dict.k:91-91` | rule; none; fixed-semantic+ordinary-rule | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| `b991b2c3d10c5826` | `reference-semantics/semantics/dict.k:92-94` | rule; none; fixed-semantic+ordinary-rule | `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0` |
| `683cf3cb2f477516` | `reference-semantics/semantics/dict.k:95-96` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| `acf462edb8618595` | `reference-semantics/semantics/dict.k:97-97` | syntax; function; syntax-declaration+function | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| `d23ca9e33dba4af1` | `reference-semantics/semantics/dict.k:98-98` | rule; none; fixed-semantic+ordinary-rule | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| `0ccb24271e3af4f9` | `reference-semantics/semantics/dict.k:99-100` | rule; none; fixed-semantic+ordinary-rule | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| `4ad85b70a655ee89` | `reference-semantics/semantics/dict.k:101-101` | syntax; function; syntax-declaration+function | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| `c87acea230ab5794` | `reference-semantics/semantics/dict.k:102-102` | rule; none; fixed-semantic+ordinary-rule | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K` |
| `288724f24a12591a` | `reference-semantics/semantics/dict.k:103-103` | rule; none; fixed-semantic+ordinary-rule | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| `9c463e5c987611a3` | `reference-semantics/semantics/float.k:20-20` | syntax; none; syntax-declaration | `syntax Val ::= Float` |
| `035276d79b60c372` | `reference-semantics/semantics/float.k:21-23` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Float(F:Float) => F ... </k>` |
| `476c595cda8ce666` | `reference-semantics/semantics/float.k:24-24` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| `04c00a6fdd132ffd` | `reference-semantics/semantics/float.k:25-25` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| `b26ffb9ac0b50f28` | `reference-semantics/semantics/float.k:27-29` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| `82dda28b6587e605` | `reference-semantics/semantics/float.k:30-30` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| `aea6184e120f3364` | `reference-semantics/semantics/float.k:31-31` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| `ce6d8965323aa403` | `reference-semantics/semantics/float.k:32-36` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| `5d1066bb71e17863` | `reference-semantics/semantics/float.k:37-37` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| `f0ef58fee49293cd` | `reference-semantics/semantics/float.k:38-38` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| `a642633a22863861` | `reference-semantics/semantics/float.k:39-42` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| `e1bf270cd81ea695` | `reference-semantics/semantics/float.k:43-43` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| `85bb7f0720e6819a` | `reference-semantics/semantics/float.k:44-49` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| `123d95f9e6bdc3e2` | `reference-semantics/semantics/float.k:50-50` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| `48a96836260758fe` | `reference-semantics/semantics/float.k:51-51` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| `7a38cfb0f7f94e66` | `reference-semantics/semantics/float.k:52-52` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| `1533a6c042247e2a` | `reference-semantics/semantics/float.k:54-54` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| `b0508a598daff2cd` | `reference-semantics/semantics/float.k:55-55` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule absF(F:Float) => absFloat(F) [concrete]` |
| `6748f54da9cb7a87` | `reference-semantics/semantics/float.k:56-60` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| `7e5ca6467e25b156` | `reference-semantics/semantics/float.k:61-64` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Import(_:String) => .K ... </k>` |
| `2afbe7345c6d0e54` | `reference-semantics/semantics/float.k:65-65` | syntax; none; syntax-declaration | `syntax KItem ::= "#mathCeil"` |
| `a5112faf5e8e9ce9` | `reference-semantics/semantics/float.k:66-66` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| `1d7746ff0ff98815` | `reference-semantics/semantics/float.k:67-69` | rule; none; fixed-semantic+ordinary-rule | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| `7acd296d2ed629c2` | `reference-semantics/semantics/float.k:70-70` | syntax; none; syntax-declaration | `syntax KItem ::= "#mathFloor"` |
| `db65c7919de329ae` | `reference-semantics/semantics/float.k:71-71` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| `202fa1a0d94a9d83` | `reference-semantics/semantics/float.k:72-72` | rule; none; fixed-semantic+ordinary-rule | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| `7c6ef60fa6ad64bf` | `reference-semantics/semantics/float.k:73-73` | syntax; function,symbol,total; syntax-declaration+function+total+symbol | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| `96160f60d5684c76` | `reference-semantics/semantics/float.k:74-74` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule floorFI(I:Int) => I [concrete]` |
| `cce04cf488e11b13` | `reference-semantics/semantics/float.k:75-77` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| `2873e3fd33dec7cf` | `reference-semantics/semantics/float.k:78-78` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| `16f35ec7a47ecc38` | `reference-semantics/semantics/float.k:79-81` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V)` |
| `5d4bfdcfb2508e2f` | `reference-semantics/semantics/float.k:82-82` | syntax; none; syntax-declaration | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| `6cc88abcedbc1769` | `reference-semantics/semantics/float.k:83-83` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| `167131a20d99433f` | `reference-semantics/semantics/float.k:84-84` | rule; none; fixed-semantic+ordinary-rule | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| `2b29388d4fdc6dd2` | `reference-semantics/semantics/float.k:85-85` | rule; none; fixed-semantic+ordinary-rule | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| `12ba19140666cb16` | `reference-semantics/semantics/float.k:86-86` | syntax; function,symbol,total; syntax-declaration+function+total+symbol | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| `6845a631b8233930` | `reference-semantics/semantics/float.k:87-87` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule toF(F:Float) => F [concrete]` |
| `192d6e7b3d057b7e` | `reference-semantics/semantics/float.k:88-92` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule toF(I:Int) => intToF(I) [concrete]` |
| `cb49f575d09a79e2` | `reference-semantics/semantics/float.k:93-93` | syntax; function,symbol,total; syntax-declaration+function+total+symbol | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| `2383204948c3889e` | `reference-semantics/semantics/float.k:94-94` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule ceilF(I:Int) => I [concrete]` |
| `3c6bd58d9a09c5a1` | `reference-semantics/semantics/float.k:95-98` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| `bb643fdd27dcc9c6` | `reference-semantics/semantics/float.k:99-102` | rule; none; fixed-semantic+ordinary-rule | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| `0214210c6e61bbc0` | `reference-semantics/semantics/float.k:103-103` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| `ec9898b2bc5b9df0` | `reference-semantics/semantics/float.k:104-104` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| `49cc1aa09704f59a` | `reference-semantics/semantics/float.k:105-105` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| `8b5c356c9037a08a` | `reference-semantics/semantics/float.k:107-107` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| `42de9904a38dd668` | `reference-semantics/semantics/float.k:108-108` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| `e5f25eb6bfc56567` | `reference-semantics/semantics/float.k:109-109` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| `82fb0e65aaa9b994` | `reference-semantics/semantics/float.k:111-111` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| `d211ec7cb508e036` | `reference-semantics/semantics/float.k:112-112` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| `2364b407632d736c` | `reference-semantics/semantics/float.k:113-113` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| `479b4986889dface` | `reference-semantics/semantics/float.k:115-115` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| `034e542ccd0fd9c5` | `reference-semantics/semantics/float.k:116-116` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| `b55d46715fd04c05` | `reference-semantics/semantics/float.k:117-117` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| `3a412d74717c95fe` | `reference-semantics/semantics/float.k:119-119` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| `0f57d31160b90f0a` | `reference-semantics/semantics/float.k:120-120` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| `4374ce8c9eb9eaae` | `reference-semantics/semantics/float.k:121-124` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| `3ea0c4072d4f42bc` | `reference-semantics/semantics/float.k:125-125` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| `6c37a5a5fab7988b` | `reference-semantics/semantics/float.k:126-126` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| `255eab1c16180633` | `reference-semantics/semantics/float.k:127-127` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)` |
| `7dba40a2ca1f59ad` | `reference-semantics/semantics/float.k:128-128` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| `7e1377cc79b5c5e1` | `reference-semantics/semantics/float.k:129-131` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| `ead42da726423493` | `reference-semantics/semantics/float.k:132-132` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| `883dafc0a0f13973` | `reference-semantics/semantics/float.k:133-133` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| `04b60c6a9d7736cf` | `reference-semantics/semantics/float.k:134-134` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| `44ed716db5256556` | `reference-semantics/semantics/float.k:135-135` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| `62267c07e260fb6e` | `reference-semantics/semantics/float.k:136-136` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| `0171d5fa040ca34c` | `reference-semantics/semantics/float.k:137-137` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| `9e8a7a381cabfba6` | `reference-semantics/semantics/float.k:138-138` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| `a1c211f0fd17b111` | `reference-semantics/semantics/float.k:139-141` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| `78e8d7d3325809d1` | `reference-semantics/semantics/float.k:142-142` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| `ead243a69d4f544f` | `reference-semantics/semantics/float.k:143-143` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| `23852ba090369367` | `reference-semantics/semantics/float.k:144-144` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| `534c0b6f3318c51d` | `reference-semantics/semantics/float.k:145-145` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| `290dfc8081bc8101` | `reference-semantics/semantics/float.k:146-146` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| `d351c6a7929b77b2` | `reference-semantics/semantics/float.k:147-147` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| `82e1e1a902400718` | `reference-semantics/semantics/float.k:148-148` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| `84cd7be4ef964043` | `reference-semantics/semantics/float.k:149-149` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| `329468afb7726616` | `reference-semantics/semantics/float.k:150-150` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| `6e49cf5ddd2cf05f` | `reference-semantics/semantics/float.k:151-153` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| `583d469949518876` | `reference-semantics/semantics/float.k:154-154` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| `32b1c942a59deef1` | `reference-semantics/semantics/float.k:155-159` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| `a105b4c5b19e3630` | `reference-semantics/semantics/float.k:160-160` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| `2c163864b513bb1f` | `reference-semantics/semantics/float.k:161-161` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| `b760f6990b670399` | `reference-semantics/semantics/float.k:162-164` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| `316096e73acdfa05` | `reference-semantics/semantics/float.k:165-165` | syntax; function; syntax-declaration+function | `syntax Int ::= headIS(IntSeq) [function]` |
| `95c662e0509cfd14` | `reference-semantics/semantics/float.k:166-166` | rule; none; fixed-semantic+ordinary-rule | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| `c6b40cd500ef491e` | `reference-semantics/semantics/float.k:167-167` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| `9fcf1e655289db3e` | `reference-semantics/semantics/float.k:168-168` | rule; none; fixed-semantic+ordinary-rule | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| `f1adc9839becd43c` | `reference-semantics/semantics/float.k:169-169` | rule; none; fixed-semantic+ordinary-rule | `rule intPartAcc(.IntSeq, A:Int) => A` |
| `34eb88ab5a4db317` | `reference-semantics/semantics/float.k:170-170` | rule; none; fixed-semantic+ordinary-rule | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| `1780ff47d6e3edb6` | `reference-semantics/semantics/float.k:171-172` | rule; none; fixed-semantic+ordinary-rule | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| `8d1160cfabe6e422` | `reference-semantics/semantics/float.k:173-173` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| `51427c09a3c6bfda` | `reference-semantics/semantics/float.k:174-174` | rule; none; fixed-semantic+ordinary-rule | `rule fracPart(.IntSeq) => 0` |
| `77993f80b2939f15` | `reference-semantics/semantics/float.k:175-175` | rule; none; fixed-semantic+ordinary-rule | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| `2e703b38937bff51` | `reference-semantics/semantics/float.k:176-176` | rule; none; fixed-semantic+ordinary-rule | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| `8d2ae82eb212b13b` | `reference-semantics/semantics/float.k:177-177` | rule; none; fixed-semantic+ordinary-rule | `rule fracAcc(.IntSeq, A:Int) => A` |
| `53ef341c213ea4e9` | `reference-semantics/semantics/float.k:178-178` | rule; none; fixed-semantic+ordinary-rule | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| `40c61e253274a42c` | `reference-semantics/semantics/float.k:179-179` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| `6fe8101a48727424` | `reference-semantics/semantics/float.k:180-180` | rule; none; fixed-semantic+ordinary-rule | `rule fracScale(.IntSeq) => 1` |
| `ae206169646bb4cb` | `reference-semantics/semantics/float.k:181-181` | rule; none; fixed-semantic+ordinary-rule | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| `42382de9087aec32` | `reference-semantics/semantics/float.k:182-182` | rule; none; fixed-semantic+ordinary-rule | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| `ad2ccd2818545e9f` | `reference-semantics/semantics/float.k:183-183` | rule; none; fixed-semantic+ordinary-rule | `rule fscAcc(.IntSeq, A:Int) => A` |
| `96bfa28715e72ee8` | `reference-semantics/semantics/float.k:184-184` | rule; none; fixed-semantic+ordinary-rule | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| `e61223e8e7852f75` | `reference-semantics/semantics/float.k:185-185` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| `553a79b526d46040` | `reference-semantics/semantics/float.k:186-186` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| `5f07e8e11c37412c` | `reference-semantics/semantics/float.k:187-189` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| `42219fae9595011c` | `reference-semantics/semantics/float.k:190-190` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| `f22dfbd6a8e5a355` | `reference-semantics/semantics/float.k:191-191` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| `00eb1273148d272d` | `reference-semantics/semantics/float.k:192-194` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| `90f4986c87d47ad2` | `reference-semantics/semantics/float.k:195-195` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| `d262b34d57f3ea3f` | `reference-semantics/semantics/float.k:196-196` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| `f2bc52ab3aac6064` | `reference-semantics/semantics/float.k:197-197` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| `bad76868f4312786` | `reference-semantics/semantics/float.k:198-198` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| `882dbf85ad2d5884` | `reference-semantics/semantics/float.k:199-199` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| `a92dda6c0a458387` | `reference-semantics/semantics/float.k:200-200` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| `d2bb4e61af13243f` | `reference-semantics/semantics/float.k:201-201` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| `57b31713922cfd31` | `reference-semantics/semantics/float.k:202-202` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| `2e1efc58c0004a2c` | `reference-semantics/semantics/float.k:203-203` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| `5f4d0da689764bca` | `reference-semantics/semantics/float.k:204-204` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| `c012641f27373a74` | `reference-semantics/semantics/float.k:205-205` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| `527b7ce6bd6705ed` | `reference-semantics/semantics/float.k:206-208` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| `809e549825aff299` | `reference-semantics/semantics/float.k:209-209` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| `7705498815b2f6de` | `reference-semantics/semantics/float.k:210-210` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| `ea7b0cfddc5b72f4` | `reference-semantics/semantics/float.k:211-211` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| `d455da414379b4ab` | `reference-semantics/semantics/float.k:213-213` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| `7f4ab69bc24bddb3` | `reference-semantics/semantics/float.k:214-216` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| `bc453e48deefa7ee` | `reference-semantics/semantics/float.k:217-217` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| `42fdc9f5f224845d` | `reference-semantics/semantics/float.k:218-222` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| `62f19023f7766e27` | `reference-semantics/semantics/float.k:223-223` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| `7a137db5d8982337` | `reference-semantics/semantics/float.k:224-226` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| `fcce905cb2b21ac2` | `reference-semantics/semantics/float.k:227-227` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)` |
| `fb032a1f7d62d3d1` | `reference-semantics/semantics/float.k:228-228` | rule; none; fixed-semantic+ordinary-rule | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| `b3cfe91173aecd76` | `reference-semantics/semantics/float.k:230-230` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| `079766c293ed3d42` | `reference-semantics/semantics/float.k:231-231` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| `65f7e59681970be8` | `reference-semantics/semantics/float.k:232-232` | syntax; none; syntax-declaration | `syntax KItem ::= "#mathSqrt"` |
| `7561106a2277cd47` | `reference-semantics/semantics/float.k:233-233` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| `2bfd1ecc60b1efdc` | `reference-semantics/semantics/float.k:234-234` | rule; none; fixed-semantic+ordinary-rule | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| `b7e9d43d653879d0` | `reference-semantics/semantics/float.k:235-242` | rule; none; fixed-semantic+ordinary-rule | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| `f9bd016af0678c86` | `reference-semantics/semantics/float.k:243-243` | syntax; none; syntax-declaration | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| `9b99607094071c60` | `reference-semantics/semantics/float.k:244-244` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `6984d94d7694e2b0` | `reference-semantics/semantics/float.k:245-245` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| `95f63471544f82c1` | `reference-semantics/semantics/float.k:246-246` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| `429dccd0dacf6634` | `reference-semantics/semantics/float.k:247-248` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| `a0a9b3f375ae6fea` | `reference-semantics/semantics/float.k:250-250` | syntax; none; syntax-declaration | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| `46a73efd209622ae` | `reference-semantics/semantics/float.k:251-251` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `9a9d01e8a68997fc` | `reference-semantics/semantics/float.k:252-252` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| `b7778072d1070b9f` | `reference-semantics/semantics/float.k:253-253` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| `082db8d558af2808` | `reference-semantics/semantics/float.k:254-260` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| `7a4b610b769656a9` | `reference-semantics/semantics/float.k:261-261` | syntax; none; syntax-declaration | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| `8d1454a1b5483d8d` | `reference-semantics/semantics/float.k:262-264` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| `06431682574dbca3` | `reference-semantics/semantics/float.k:265-265` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| `6945e670e93a3994` | `reference-semantics/semantics/float.k:266-266` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| `23ff350fb485a3de` | `reference-semantics/semantics/float.k:267-269` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| `3888a9f59e768500` | `reference-semantics/semantics/float.k:270-272` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| `b67ef5117abef887` | `reference-semantics/semantics/functions.k:8-13` | syntax; none; syntax-declaration | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall"` |
| `f52a29aeaa5c3cc2` | `reference-semantics/semantics/functions.k:14-16` | rule; none; fixed-semantic+ordinary-rule | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| `4249f67e2d65f2ed` | `reference-semantics/semantics/functions.k:18-18` | syntax; none; syntax-declaration | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| `cabe731bd2a6777d` | `reference-semantics/semantics/functions.k:19-26` | rule; none; fixed-semantic+ordinary-rule | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` |
| `723ebb3135566621` | `reference-semantics/semantics/functions.k:27-30` | syntax; none; syntax-declaration | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| `c699c9db4753ea05` | `reference-semantics/semantics/functions.k:31-32` | syntax; none; syntax-declaration | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| `75b361801ad7ecea` | `reference-semantics/semantics/functions.k:33-35` | rule; none; fixed-semantic+ordinary-rule | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| `6b56e05b0227160b` | `reference-semantics/semantics/functions.k:36-41` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| `fa0ed76e337633e1` | `reference-semantics/semantics/functions.k:42-45` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| `5f2b86306b95ee4e` | `reference-semantics/semantics/functions.k:47-49` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| `aa2d5b9854aa4089` | `reference-semantics/semantics/functions.k:50-52` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| `01d4e0d4519ccdcb` | `reference-semantics/semantics/functions.k:53-58` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| `04c28e057709bebf` | `reference-semantics/semantics/functions.k:59-62` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` |
| `3e723dcad4809a33` | `reference-semantics/semantics/functions.k:63-63` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| `60c4df73d7906b44` | `reference-semantics/semantics/functions.k:64-67` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes>` |
| `9bddb06f1c296518` | `reference-semantics/semantics/functions.k:68-77` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]` |
| `8c445d7ea511b207` | `reference-semantics/semantics/functions.k:78-79` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| `5db85d0d167f5599` | `reference-semantics/semantics/functions.k:80-84` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` |
| `5c6039a3d98e4eb4` | `reference-semantics/semantics/functions.k:85-90` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |
| `e8730451653796b2` | `reference-semantics/semantics/int.k:7-7` | rule; none; fixed-semantic+ordinary-rule | `rule applyUn("-", I:Int) => 0 -Int I` |
| `7507bdcdb42029dd` | `reference-semantics/semantics/int.k:9-10` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2` |
| `cac875305643db65` | `reference-semantics/semantics/int.k:11-11` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| `d5e5abd8cfe90ab8` | `reference-semantics/semantics/int.k:12-12` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| `6ca0acf3c2f7c75f` | `reference-semantics/semantics/int.k:13-13` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2` |
| `076f2bbf7144abb5` | `reference-semantics/semantics/int.k:14-14` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2` |
| `23c841e60c9d7684` | `reference-semantics/semantics/int.k:15-15` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)` |
| `30b4960240beee45` | `reference-semantics/semantics/int.k:16-16` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| `686dcf6e2ffe3d62` | `reference-semantics/semantics/int.k:17-17` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| `237b09d3a8a5c3de` | `reference-semantics/semantics/int.k:19-19` | syntax; function; syntax-declaration+function | `syntax Int ::= pyMod(Int, Int) [function]` |
| `dd63ca61d0ee589f` | `reference-semantics/semantics/int.k:20-20` | rule; none; fixed-semantic+ordinary-rule | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| `b3a11a94f5e2ad15` | `reference-semantics/semantics/int.k:22-22` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` |
| `9364d26920c830ba` | `reference-semantics/semantics/int.k:23-23` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2` |
| `1e7b22cef01d0e61` | `reference-semantics/semantics/int.k:24-24` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` |
| `d2b1b43baf2cbc87` | `reference-semantics/semantics/int.k:25-25` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2` |
| `b0ff2cbbf096dd39` | `reference-semantics/semantics/int.k:26-26` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2` |
| `c38b12934f82bbb9` | `reference-semantics/semantics/int.k:27-27` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2` |
| `5dfc620f7220ca12` | `reference-semantics/semantics/iter.k:8-8` | syntax; none; syntax-declaration | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| `a02d8a18cded1cc9` | `reference-semantics/semantics/list.k:9-9` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>` |
| `527e3920153b13f4` | `reference-semantics/semantics/list.k:10-12` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| `67164d0d9b888928` | `reference-semantics/semantics/list.k:13-13` | syntax; none; syntax-declaration | `syntax ApplyK ::= "toList"` |
| `abc22074edba2c66` | `reference-semantics/semantics/list.k:14-14` | rule; none; fixed-semantic+ordinary-rule | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| `6a3237794a89d632` | `reference-semantics/semantics/list.k:15-17` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| `a5b2ff9f95f673c4` | `reference-semantics/semantics/list.k:18-18` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| `73b38effa2dda932` | `reference-semantics/semantics/list.k:19-19` | rule; none; fixed-semantic+ordinary-rule | `rule valSeqConcat(.ValSeq, T:ValSeq) => T` |
| `8a21b5e3db1e5737` | `reference-semantics/semantics/list.k:20-23` | rule; none; fixed-semantic+ordinary-rule | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| `0910480ddafe7a7a` | `reference-semantics/semantics/list.k:24-25` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| `9bd346df9af90c9f` | `reference-semantics/semantics/list.k:27-27` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| `d02c6e8fdb76a66e` | `reference-semantics/semantics/list.k:28-32` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| `6b370019f66b1f69` | `reference-semantics/semantics/list.k:33-33` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| `86ee6a4a678c7118` | `reference-semantics/semantics/list.k:34-34` | rule; none; fixed-semantic+ordinary-rule | `rule hasRefVS(.ValSeq) => false` |
| `270f92755edbfe2e` | `reference-semantics/semantics/list.k:35-35` | rule; none; fixed-semantic+ordinary-rule | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| `04c15d79af6e3862` | `reference-semantics/semantics/list.k:37-38` | syntax; function; syntax-declaration+function | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map) [function]` |
| `a4e76a7eba29a7af` | `reference-semantics/semantics/list.k:39-39` | rule; none; fixed-semantic+ordinary-rule | `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true` |
| `b8122200ccefeb99` | `reference-semantics/semantics/list.k:40-40` | rule; none; fixed-semantic+ordinary-rule | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false` |
| `290bec4cea1892bb` | `reference-semantics/semantics/list.k:41-41` | rule; none; fixed-semantic+ordinary-rule | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false` |
| `bb515c4d869d2b0f` | `reference-semantics/semantics/list.k:42-43` | rule; none; fixed-semantic+ordinary-rule | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| `26d582910227341e` | `reference-semantics/semantics/list.k:45-46` | rule; none; fixed-semantic+ordinary-rule | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| `c5a7d32872ff18d2` | `reference-semantics/semantics/list.k:47-48` | rule; none; fixed-semantic+ordinary-rule | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| `6e6c73e4e78d19a8` | `reference-semantics/semantics/list.k:49-49` | rule; none; fixed-semantic+ordinary-rule | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| `607a8352a9fa519f` | `reference-semantics/semantics/list.k:50-52` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| `76b4c6aaec14446e` | `reference-semantics/semantics/list.k:53-57` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` |
| `e47725f115e3aace` | `reference-semantics/semantics/list.k:58-58` | syntax; none; syntax-declaration | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| `3967ab15a776a1a3` | `reference-semantics/semantics/list.k:59-59` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| `7987cc8664243924` | `reference-semantics/semantics/list.k:60-60` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| `29896bd26a2cad78` | `reference-semantics/semantics/list.k:61-61` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| `6ff9b8ce192190e5` | `reference-semantics/semantics/list.k:62-62` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| `06ad45aa800bf5ad` | `reference-semantics/semantics/list.k:63-64` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| `258ece647548116a` | `reference-semantics/semantics/list.k:65-66` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| `ed58eea4a2372b40` | `reference-semantics/semantics/list.k:67-67` | rule; none; fixed-semantic+ordinary-rule | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| `1b39ad5372d2312f` | `reference-semantics/semantics/methods.k:10-12` | syntax; function; syntax-declaration+function | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| `8c09346642264944` | `reference-semantics/semantics/methods.k:13-13` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| `547ca7218be80546` | `reference-semantics/semantics/methods.k:14-14` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| `1644ffbbbdebd939` | `reference-semantics/semantics/methods.k:15-15` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| `40c80aa9cfe7bef2` | `reference-semantics/semantics/methods.k:16-18` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| `44f56bc4f337e8b7` | `reference-semantics/semantics/methods.k:19-19` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))` |
| `6b847ca33bb0367c` | `reference-semantics/semantics/methods.k:20-20` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))` |
| `9bd563ccca2459ea` | `reference-semantics/semantics/methods.k:21-25` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| `c44bb409637ac6df` | `reference-semantics/semantics/methods.k:26-26` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| `6c88fe90b97cd455` | `reference-semantics/semantics/methods.k:27-27` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| `b8d083db70664326` | `reference-semantics/semantics/methods.k:28-28` | rule; none; fixed-semantic+ordinary-rule | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| `dea56f362b9e564a` | `reference-semantics/semantics/methods.k:29-29` | rule; none; fixed-semantic+ordinary-rule | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| `e82ccef9c2b242d7` | `reference-semantics/semantics/methods.k:30-33` | rule; none; fixed-semantic+ordinary-rule | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` |
| `9031509e773f24a7` | `reference-semantics/semantics/methods.k:34-34` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| `d8ef328eaffabc71` | `reference-semantics/semantics/methods.k:35-35` | syntax; function; syntax-declaration+function | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| `12c427914a1fc0f6` | `reference-semantics/semantics/methods.k:36-36` | rule; none; fixed-semantic+ordinary-rule | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| `f009b25f36ee9c76` | `reference-semantics/semantics/methods.k:37-38` | rule; none; fixed-semantic+ordinary-rule | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| `6031b5d83224d0df` | `reference-semantics/semantics/methods.k:39-40` | rule; none; fixed-semantic+ordinary-rule | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| `c910907169f547fb` | `reference-semantics/semantics/methods.k:41-41` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| `bafd984ad9a8591a` | `reference-semantics/semantics/methods.k:42-42` | rule; none; fixed-semantic+ordinary-rule | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| `1d2d37b2f7e08cfc` | `reference-semantics/semantics/methods.k:43-43` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| `927414750b5c366b` | `reference-semantics/semantics/methods.k:44-46` | rule; none; fixed-semantic+ordinary-rule | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| `5c0aa6c510d530c2` | `reference-semantics/semantics/methods.k:47-47` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| `e2dbe39213013b29` | `reference-semantics/semantics/methods.k:48-48` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| `713d3ece9d5a67ad` | `reference-semantics/semantics/methods.k:49-49` | rule; none; fixed-semantic+ordinary-rule | `rule trimWS(.IntSeq) => .IntSeq` |
| `a73fdd11f6683a48` | `reference-semantics/semantics/methods.k:50-50` | rule; none; fixed-semantic+ordinary-rule | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| `05818f5920a05840` | `reference-semantics/semantics/methods.k:51-51` | rule; none; fixed-semantic+ordinary-rule | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| `7f96449c6b62e33a` | `reference-semantics/semantics/methods.k:52-52` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| `84de275fefc9853f` | `reference-semantics/semantics/methods.k:53-53` | rule; none; fixed-semantic+ordinary-rule | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| `ec1c4a34d6e26ff5` | `reference-semantics/semantics/methods.k:54-54` | rule; none; fixed-semantic+ordinary-rule | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| `3a016e58eff6718f` | `reference-semantics/semantics/methods.k:55-57` | rule; none; fixed-semantic+ordinary-rule | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| `3cc5d3f011372b04` | `reference-semantics/semantics/methods.k:58-60` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| `70d96f312451f2bd` | `reference-semantics/semantics/methods.k:61-63` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| `3d4ab57a7c18f0f1` | `reference-semantics/semantics/methods.k:64-64` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| `425092ec41cd26bc` | `reference-semantics/semantics/methods.k:65-65` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| `d253be7818e1f330` | `reference-semantics/semantics/methods.k:66-66` | rule; none; fixed-semantic+ordinary-rule | `rule cntOccVS(.ValSeq, _:Val) => 0` |
| `a42bebf0b88f6856` | `reference-semantics/semantics/methods.k:67-67` | rule; none; fixed-semantic+ordinary-rule | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| `936a96821f2f1c56` | `reference-semantics/semantics/methods.k:68-71` | rule; none; fixed-semantic+ordinary-rule | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V)` |
| `70d317a78cd0c40e` | `reference-semantics/semantics/methods.k:72-74` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| `21a12d62771c7e14` | `reference-semantics/semantics/methods.k:75-75` | syntax; function; syntax-declaration+function | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]` |
| `fa16cc16cb2ccfb9` | `reference-semantics/semantics/methods.k:76-76` | rule; none; fixed-semantic+ordinary-rule | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| `b4c2df11621a337c` | `reference-semantics/semantics/methods.k:77-78` | rule; none; fixed-semantic+ordinary-rule | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| `ff46b0c030545d6e` | `reference-semantics/semantics/methods.k:79-81` | rule; none; fixed-semantic+ordinary-rule | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` |
| `ecba0d4da13fb344` | `reference-semantics/semantics/methods.k:82-82` | syntax; function; syntax-declaration+function | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| `893b444e22eaf4b6` | `reference-semantics/semantics/methods.k:83-83` | rule; none; fixed-semantic+ordinary-rule | `rule flushTok(ACC:ValSeq, .IntSeq) => ACC` |
| `bb0b384d1bc3b67d` | `reference-semantics/semantics/methods.k:84-84` | rule; none; fixed-semantic+ordinary-rule | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| `7803aae1cb334e3b` | `reference-semantics/semantics/methods.k:85-85` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= isWSC(Int) [function, total]` |
| `5b829882acfadf6d` | `reference-semantics/semantics/methods.k:86-88` | rule; none; fixed-semantic+ordinary-rule | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| `7ea4196602ce08e3` | `reference-semantics/semantics/methods.k:89-93` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` |
| `cfcd3ab2d110426f` | `reference-semantics/semantics/methods.k:94-96` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| `fa603f37744a5a7e` | `reference-semantics/semantics/methods.k:97-97` | syntax; function; syntax-declaration+function | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]` |
| `88c4b4105871204b` | `reference-semantics/semantics/methods.k:98-98` | rule; none; fixed-semantic+ordinary-rule | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)` |
| `5b1ad556c8762b07` | `reference-semantics/semantics/methods.k:99-100` | rule; none; fixed-semantic+ordinary-rule | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| `5c457ecc171934ba` | `reference-semantics/semantics/methods.k:101-102` | rule; none; fixed-semantic+ordinary-rule | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| `c0b7731b79751b7c` | `reference-semantics/semantics/methods.k:104-105` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| `5cb5443d06d1dc49` | `reference-semantics/semantics/methods.k:106-106` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| `3643545554090f65` | `reference-semantics/semantics/methods.k:107-107` | rule; none; fixed-semantic+ordinary-rule | `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq` |
| `e03d935bd6b93984` | `reference-semantics/semantics/methods.k:108-108` | rule; none; fixed-semantic+ordinary-rule | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| `71e996b6c5b069fb` | `reference-semantics/semantics/methods.k:109-111` | rule; none; fixed-semantic+ordinary-rule | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| `86fa771722b7744e` | `reference-semantics/semantics/methods.k:112-112` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= isUpperC(Int) [function, total]` |
| `7cb53d2a35dc4cf1` | `reference-semantics/semantics/methods.k:113-113` | rule; none; fixed-semantic+ordinary-rule | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| `b7651cbfb7cb3a33` | `reference-semantics/semantics/methods.k:115-115` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= isLowerC(Int) [function, total]` |
| `5c806e2eb881483d` | `reference-semantics/semantics/methods.k:116-116` | rule; none; fixed-semantic+ordinary-rule | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| `21104c9bb37f9bce` | `reference-semantics/semantics/methods.k:118-118` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| `75e972812e0a8387` | `reference-semantics/semantics/methods.k:119-119` | rule; none; fixed-semantic+ordinary-rule | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| `707ecfc9113bc61c` | `reference-semantics/semantics/methods.k:121-121` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= isDigitC(Int) [function, total]` |
| `e08d0edf0391d13c` | `reference-semantics/semantics/methods.k:122-122` | rule; none; fixed-semantic+ordinary-rule | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `a35d2293a96fe363` | `reference-semantics/semantics/methods.k:124-124` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| `beada6364a217a39` | `reference-semantics/semantics/methods.k:125-125` | rule; none; fixed-semantic+ordinary-rule | `rule hasUpper(.IntSeq) => false` |
| `e2cc74a97ebffd79` | `reference-semantics/semantics/methods.k:126-126` | rule; none; fixed-semantic+ordinary-rule | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| `96bbfca105017556` | `reference-semantics/semantics/methods.k:128-128` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| `3f7786f8b2bf1e4c` | `reference-semantics/semantics/methods.k:129-129` | rule; none; fixed-semantic+ordinary-rule | `rule hasLower(.IntSeq) => false` |
| `59d6785606da6284` | `reference-semantics/semantics/methods.k:130-130` | rule; none; fixed-semantic+ordinary-rule | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| `a6941edab0c5e028` | `reference-semantics/semantics/methods.k:132-132` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| `24a4e57e16d1c6d7` | `reference-semantics/semantics/methods.k:133-133` | rule; none; fixed-semantic+ordinary-rule | `rule allAlpha(.IntSeq) => true` |
| `7df457aa0efebc9c` | `reference-semantics/semantics/methods.k:134-134` | rule; none; fixed-semantic+ordinary-rule | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| `837c6992ce63f1af` | `reference-semantics/semantics/methods.k:136-136` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| `1197b2b22192e165` | `reference-semantics/semantics/methods.k:137-137` | rule; none; fixed-semantic+ordinary-rule | `rule allDigit(.IntSeq) => true` |
| `7814887cd9a0de0f` | `reference-semantics/semantics/methods.k:138-138` | rule; none; fixed-semantic+ordinary-rule | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| `6742e187ee523636` | `reference-semantics/semantics/methods.k:140-140` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= lowerC(Int) [function, total]` |
| `3cacb500e7ccca9e` | `reference-semantics/semantics/methods.k:142-142` | rule; none; fixed-semantic+ordinary-rule | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `7a2c77592c7313f0` | `reference-semantics/semantics/methods.k:143-143` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule lowerC(C:Int) => C [owise]` |
| `4ea84a24758e2a11` | `reference-semantics/semantics/methods.k:145-145` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= upperC(Int) [function, total]` |
| `4ba52f800891da61` | `reference-semantics/semantics/methods.k:146-146` | rule; none; fixed-semantic+ordinary-rule | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `58c81c03be24536a` | `reference-semantics/semantics/methods.k:147-147` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule upperC(C:Int) => C [owise]` |
| `675e57d521253797` | `reference-semantics/semantics/methods.k:149-149` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= swapC(Int) [function, total]` |
| `ef17a7409c95c13b` | `reference-semantics/semantics/methods.k:150-150` | rule; none; fixed-semantic+ordinary-rule | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `f73306b5585b81a0` | `reference-semantics/semantics/methods.k:151-151` | rule; none; fixed-semantic+ordinary-rule | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `645ac85e88787541` | `reference-semantics/semantics/methods.k:152-152` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule swapC(C:Int) => C [owise]` |
| `e20f49d78428579c` | `reference-semantics/semantics/methods.k:154-154` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| `e95d96cc7777ed4c` | `reference-semantics/semantics/methods.k:155-155` | rule; none; fixed-semantic+ordinary-rule | `rule mapLower(.IntSeq) => .IntSeq` |
| `c84c2dee555bdd78` | `reference-semantics/semantics/methods.k:156-156` | rule; none; fixed-semantic+ordinary-rule | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| `1fb5a8392a915a6d` | `reference-semantics/semantics/methods.k:158-158` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| `8ccc486825593983` | `reference-semantics/semantics/methods.k:159-159` | rule; none; fixed-semantic+ordinary-rule | `rule mapUpper(.IntSeq) => .IntSeq` |
| `15d40b5ed773eb52` | `reference-semantics/semantics/methods.k:160-160` | rule; none; fixed-semantic+ordinary-rule | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| `553ceba3e608c058` | `reference-semantics/semantics/methods.k:162-162` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| `55c4477ef06f4494` | `reference-semantics/semantics/methods.k:163-163` | rule; none; fixed-semantic+ordinary-rule | `rule mapSwap(.IntSeq) => .IntSeq` |
| `cffe75da18ef8b0a` | `reference-semantics/semantics/methods.k:164-164` | rule; none; fixed-semantic+ordinary-rule | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| `968a83f4824d5c8e` | `reference-semantics/semantics/methods.k:166-166` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| `2ca26c755a21f32b` | `reference-semantics/semantics/methods.k:167-167` | rule; none; fixed-semantic+ordinary-rule | `rule startsWith(.IntSeq, _:IntSeq) => true` |
| `76dde9ca988a74a5` | `reference-semantics/semantics/methods.k:168-168` | rule; none; fixed-semantic+ordinary-rule | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `08e3745098830020` | `reference-semantics/semantics/methods.k:169-169` | rule; none; fixed-semantic+ordinary-rule | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| `65f4b1ece3a17105` | `reference-semantics/semantics/operators.k:10-10` | rule; none; fixed-semantic+ordinary-rule | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| `9f015feb9b25efd2` | `reference-semantics/semantics/operators.k:12-14` | rule; none; fixed-semantic+ordinary-rule | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| `57c3f4c71c7e70f5` | `reference-semantics/semantics/operators.k:15-15` | context; none; evaluation-context | `context Compare(HOLE, _)` |
| `0e9389a66bc90399` | `reference-semantics/semantics/operators.k:16-16` | context; none; evaluation-context | `context Compare(_:Val, CmpOp(_, HOLE))` |
| `75ed2884a3973b00` | `reference-semantics/semantics/operators.k:17-17` | rule; owise; fixed-semantic+ordinary-rule+owise | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| `a7c1f1c21375407f` | `reference-semantics/semantics/operators.k:19-19` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("is", V:Val, noneV) => V ==K noneV` |
| `c72652bbbeb51d23` | `reference-semantics/semantics/operators.k:20-24` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| `c001f2d42e67344a` | `reference-semantics/semantics/operators.k:25-27` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `1aefb53317084d60` | `reference-semantics/semantics/operators.k:28-33` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` |
| `5a3f27d093e6060a` | `reference-semantics/semantics/operators.k:34-37` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| `35c071381c25e93b` | `reference-semantics/semantics/operators.k:38-42` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| `b99ddba98ca50583` | `reference-semantics/semantics/operators.k:44-46` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `5bb999e627355f8d` | `reference-semantics/semantics/range.k:9-9` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| `21c149a717cd042a` | `reference-semantics/semantics/range.k:10-10` | rule; none; fixed-semantic+ordinary-rule | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| `988f7ea5ea2b4261` | `reference-semantics/semantics/range.k:12-12` | syntax; function; syntax-declaration+function | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| `ebfe50bfd001165a` | `reference-semantics/semantics/range.k:13-14` | rule; none; fixed-semantic+ordinary-rule | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| `0a5eaced5c1853d3` | `reference-semantics/semantics/range.k:15-16` | rule; none; fixed-semantic+ordinary-rule | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| `31f1cfc772933e3f` | `reference-semantics/semantics/range.k:17-18` | rule; none; fixed-semantic+ordinary-rule | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| `60d8a3743479db29` | `reference-semantics/semantics/range.k:20-22` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| `3f901ff66bd07e7b` | `reference-semantics/semantics/range.k:23-24` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| `745442f944a06895` | `reference-semantics/semantics/set.k:8-10` | syntax; none; syntax-declaration | `syntax Val ::= setV(IntSeq)` |
| `3588ecd893fb3eab` | `reference-semantics/semantics/set.k:11-11` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| `dee883428b77b7c5` | `reference-semantics/semantics/set.k:12-12` | rule; none; fixed-semantic+ordinary-rule | `rule codeIn(_:Int, .IntSeq) => false` |
| `d1c31249adcafeb5` | `reference-semantics/semantics/set.k:13-15` | rule; none; fixed-semantic+ordinary-rule | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| `19456b234e1d0cbe` | `reference-semantics/semantics/set.k:16-17` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] \| dedupFrom(IntSeq, IntSeq) [function, total]` |
| `0622f6a7b2fd5938` | `reference-semantics/semantics/set.k:18-18` | rule; none; fixed-semantic+ordinary-rule | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| `3c78a4c70f19d20d` | `reference-semantics/semantics/set.k:19-19` | rule; none; fixed-semantic+ordinary-rule | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| `95ca35db7bca8976` | `reference-semantics/semantics/set.k:20-21` | rule; none; fixed-semantic+ordinary-rule | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| `e9fd5d0c7abce00d` | `reference-semantics/semantics/set.k:22-23` | rule; none; fixed-semantic+ordinary-rule | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| `fd5c61edb8b868a9` | `reference-semantics/semantics/set.k:25-25` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| `98a2fe6f5c1e2b48` | `reference-semantics/semantics/set.k:26-26` | rule; none; fixed-semantic+ordinary-rule | `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)` |
| `af2b65f7df03dda0` | `reference-semantics/semantics/set.k:27-30` | rule; none; fixed-semantic+ordinary-rule | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| `bd0440f8ae082f53` | `reference-semantics/semantics/set.k:31-31` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| `3f84f7b1104214f9` | `reference-semantics/semantics/set.k:32-32` | rule; none; fixed-semantic+ordinary-rule | `rule subsetCodes(.IntSeq, _:IntSeq) => true` |
| `f5deee2b2d022804` | `reference-semantics/semantics/set.k:33-33` | rule; none; fixed-semantic+ordinary-rule | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| `6fc5ae334d111010` | `reference-semantics/semantics/set.k:35-35` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| `b6d9d9ee9102f7b3` | `reference-semantics/semantics/set.k:36-38` | rule; none; fixed-semantic+ordinary-rule | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| `76f48ccca641e205` | `reference-semantics/semantics/set.k:39-39` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| `1eb41a149b64d85c` | `reference-semantics/semantics/sort.k:18-18` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| `7b7daf67a2fb64cd` | `reference-semantics/semantics/sort.k:19-19` | syntax; function; syntax-declaration+function | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| `64d0ee6e31c4ad8e` | `reference-semantics/semantics/sort.k:20-20` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule sortVS(.ValSeq) => .ValSeq [concrete]` |
| `f1ebeb6fe4cc4628` | `reference-semantics/semantics/sort.k:21-21` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| `1055f2853eb4d68d` | `reference-semantics/semantics/sort.k:22-22` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]` |
| `040aefae86111871` | `reference-semantics/semantics/sort.k:23-23` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| `caed38701bca25a4` | `reference-semantics/semantics/sort.k:24-25` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete]` |
| `a8a70e7829e67a28` | `reference-semantics/semantics/sort.k:26-26` | syntax; function; syntax-declaration+function | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| `291a5dcfd305adea` | `reference-semantics/semantics/sort.k:27-27` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| `cbf1a18884f5dd24` | `reference-semantics/semantics/sort.k:28-28` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| `7f813f3d86de53bc` | `reference-semantics/semantics/sort.k:29-30` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| `ec231dc980512195` | `reference-semantics/semantics/sort.k:31-35` | rule; concrete; fixed-semantic+ordinary-rule+concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` |
| `1c8f53b02166c835` | `reference-semantics/semantics/sort.k:36-39` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` |
| `29395c3c8991db92` | `reference-semantics/semantics/sort.k:40-48` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` |
| `e1071f0da0147363` | `reference-semantics/semantics/sort.k:49-49` | syntax; function,no-evaluators,symbol,total; syntax-declaration+function+total+symbol+no-evaluators | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| `f9ab30ffdef38fc3` | `reference-semantics/semantics/sort.k:51-52` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| `99eb00a955794fd7` | `reference-semantics/semantics/sort.k:53-53` | rule; none; fixed-semantic+ordinary-rule | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| `9e4d5d55a337c156` | `reference-semantics/semantics/sort.k:54-54` | rule; none; fixed-semantic+ordinary-rule | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| `35abf0e23fc9d273` | `reference-semantics/semantics/sort.k:55-55` | rule; none; fixed-semantic+ordinary-rule | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| `f1d1312bd468adc1` | `reference-semantics/semantics/sort.k:57-57` | syntax; function,total; syntax-declaration+function+total | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| `a43e2ad39f07fdb7` | `reference-semantics/semantics/sort.k:58-58` | rule; none; fixed-semantic+ordinary-rule | `rule condRev(S:ValSeq, false) => S` |
| `611ec889558a246e` | `reference-semantics/semantics/sort.k:59-59` | rule; none; fixed-semantic+ordinary-rule | `rule condRev(S:ValSeq, true) => revVS(S)` |
| `59fc5c29962a50b7` | `reference-semantics/semantics/sort.k:61-62` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| `8d744c44c44fc509` | `reference-semantics/semantics/sort.k:63-64` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| `d67239fdb703bf38` | `reference-semantics/semantics/sort.k:65-71` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` |
| `76021855f72d4792` | `reference-semantics/semantics/str.k:8-8` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>` |
| `fce0d9e436f043bc` | `reference-semantics/semantics/str.k:9-12` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` |
| `45f67978a3cfda48` | `reference-semantics/semantics/str.k:13-13` | syntax; function; syntax-declaration+function | `syntax IntSeq ::= strToCodes(String) [function]` |
| `1057dcefb01b2d97` | `reference-semantics/semantics/str.k:14-14` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| `3232b26d24bfa678` | `reference-semantics/semantics/str.k:15-15` | rule; none; fixed-semantic+ordinary-rule | `rule strToCodes("") => .IntSeq` |
| `2e58bcf7196c35d5` | `reference-semantics/semantics/str.k:16-19` | rule; none; fixed-semantic+ordinary-rule | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` |
| `4ddb158e60b5c9ff` | `reference-semantics/semantics/str.k:20-20` | syntax; function,total; syntax-declaration+function+total | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| `b1151e9c72c016fb` | `reference-semantics/semantics/str.k:21-21` | rule; none; fixed-semantic+ordinary-rule | `rule seqConcat(.IntSeq, T:IntSeq) => T` |
| `dc1c9132bac35c0b` | `reference-semantics/semantics/str.k:22-22` | rule; none; fixed-semantic+ordinary-rule | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| `4dd91d7480dc13a6` | `reference-semantics/semantics/str.k:24-24` | rule; none; fixed-semantic+ordinary-rule | `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| `32eaa5c2e7763708` | `reference-semantics/semantics/str.k:25-25` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| `bed088a5b6dc8b88` | `reference-semantics/semantics/str.k:26-28` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| `8b4a765118181a0e` | `reference-semantics/semantics/str.k:29-29` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| `19e3cc308017de38` | `reference-semantics/semantics/str.k:30-30` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| `58af581d3292bc84` | `reference-semantics/semantics/str.k:32-32` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| `adc329e4e6f0e829` | `reference-semantics/semantics/str.k:33-33` | rule; none; fixed-semantic+ordinary-rule | `rule strPrefix(.IntSeq, _:IntSeq) => true` |
| `4b30ab478b767787` | `reference-semantics/semantics/str.k:34-34` | rule; none; fixed-semantic+ordinary-rule | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `46a31468ef4b1ecb` | `reference-semantics/semantics/str.k:35-35` | rule; none; fixed-semantic+ordinary-rule | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| `f3a70b25f4cf17f6` | `reference-semantics/semantics/str.k:37-37` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| `356be0a4fe01bf36` | `reference-semantics/semantics/str.k:38-38` | rule; none; fixed-semantic+ordinary-rule | `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)` |
| `3609b0622a1726ae` | `reference-semantics/semantics/str.k:39-39` | rule; none; fixed-semantic+ordinary-rule | `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)` |
| `f513f865fc89431f` | `reference-semantics/semantics/str.k:40-47` | rule; none; fixed-semantic+ordinary-rule | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` |
| `af0832c35703fb56` | `reference-semantics/semantics/str.k:48-48` | syntax; function,total; syntax-declaration+function+total | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| `c953470aec9ea4a8` | `reference-semantics/semantics/str.k:49-49` | rule; none; fixed-semantic+ordinary-rule | `rule strLt(.IntSeq, .IntSeq) => false` |
| `595febc4e1085b52` | `reference-semantics/semantics/str.k:50-50` | rule; none; fixed-semantic+ordinary-rule | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| `e0e9810b5f96f92a` | `reference-semantics/semantics/str.k:51-51` | rule; none; fixed-semantic+ordinary-rule | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `a2d0793aea5b3d7c` | `reference-semantics/semantics/str.k:52-52` | rule; none; fixed-semantic+ordinary-rule | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B` |
| `72bb88a03f4ce9f3` | `reference-semantics/semantics/str.k:53-53` | rule; none; fixed-semantic+ordinary-rule | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B` |
| `fe7095795c963b98` | `reference-semantics/semantics/str.k:54-54` | rule; none; fixed-semantic+ordinary-rule | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| `72927b54074c625a` | `reference-semantics/semantics/str.k:56-56` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `7429746b52fe2672` | `reference-semantics/semantics/str.k:57-57` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| `044a3848766425a3` | `reference-semantics/semantics/str.k:58-58` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| `4e655f2e1fdfbc7c` | `reference-semantics/semantics/str.k:59-59` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| `4b1a924c19657110` | `reference-semantics/semantics/subscript.k:11-11` | syntax; function,total; syntax-declaration+function+total | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| `a65c1ed915b03377` | `reference-semantics/semantics/subscript.k:12-12` | rule; none; fixed-semantic+ordinary-rule | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V` |
| `dcebdeb833b75ae4` | `reference-semantics/semantics/subscript.k:13-14` | rule; none; fixed-semantic+ordinary-rule | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| `d12e4ba4e629956c` | `reference-semantics/semantics/subscript.k:16-16` | syntax; function; syntax-declaration+function | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| `b9f5a5a364c1103a` | `reference-semantics/semantics/subscript.k:17-17` | rule; none; fixed-semantic+ordinary-rule | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C` |
| `b15ae57756a9e5ad` | `reference-semantics/semantics/subscript.k:18-19` | rule; none; fixed-semantic+ordinary-rule | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| `eb976a8ed2dbc15b` | `reference-semantics/semantics/subscript.k:21-21` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| `5795710641c478f6` | `reference-semantics/semantics/subscript.k:22-22` | rule; none; fixed-semantic+ordinary-rule | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| `6f6e30df564ee1ec` | `reference-semantics/semantics/subscript.k:23-26` | rule; none; fixed-semantic+ordinary-rule | `rule normIdx(I:Int, _:Int) => I requires I >=Int 0` |
| `5abdddfee73fa378` | `reference-semantics/semantics/subscript.k:27-27` | context; none; evaluation-context | `context Subscript(HOLE, _)` |
| `c7d9531b01a5e2d5` | `reference-semantics/semantics/subscript.k:28-30` | context; none; evaluation-context | `context Subscript(_:Val, HOLE:Expr)` |
| `a9c400fcd1ea37cd` | `reference-semantics/semantics/subscript.k:31-33` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `01c66b80ae0f1b00` | `reference-semantics/semantics/subscript.k:35-35` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| `fc326ec18dff96ab` | `reference-semantics/semantics/subscript.k:37-37` | syntax; function; syntax-declaration+function | `syntax Val ::= applyIndex(Val, Int) [function]` |
| `fa620f34dfecc012` | `reference-semantics/semantics/subscript.k:38-38` | rule; none; fixed-semantic+ordinary-rule | `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `d26210e6a32b00a5` | `reference-semantics/semantics/subscript.k:39-39` | rule; none; fixed-semantic+ordinary-rule | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `2e34c7fb49b94705` | `reference-semantics/semantics/subscript.k:40-43` | rule; none; fixed-semantic+ordinary-rule | `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` |
| `5e0f08b916e3e2d2` | `reference-semantics/semantics/subscript.k:44-47` | syntax; none; syntax-declaration | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| `54230f2246ae5286` | `reference-semantics/semantics/subscript.k:49-49` | syntax; none; syntax-declaration | `syntax OptInt ::= "noB" \| someB(Int)` |
| `26b8c2b6646dc040` | `reference-semantics/semantics/subscript.k:50-50` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #evalB(NoBound) => noB ... </k>` |
| `d4bb0dd850e787ee` | `reference-semantics/semantics/subscript.k:51-51` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>` |
| `ce283df07ca78b87` | `reference-semantics/semantics/subscript.k:52-52` | rule; none; fixed-semantic+ordinary-rule | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| `f5cceba733e2fee2` | `reference-semantics/semantics/subscript.k:54-54` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| `ee330ba53af38e58` | `reference-semantics/semantics/subscript.k:55-55` | rule; none; fixed-semantic+ordinary-rule | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| `54524f4cf7d806b8` | `reference-semantics/semantics/subscript.k:56-57` | rule; none; fixed-semantic+ordinary-rule | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| `00c076ab05ffbd7a` | `reference-semantics/semantics/subscript.k:58-60` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| `a069bb343f48e1d3` | `reference-semantics/semantics/subscript.k:61-61` | rule; none; fixed-semantic+ordinary-rule | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| `e4388ae8349ddaad` | `reference-semantics/semantics/subscript.k:63-63` | syntax; function; syntax-declaration+function | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| `3d9a73aa4d46a781` | `reference-semantics/semantics/subscript.k:64-65` | rule; none; fixed-semantic+ordinary-rule | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| `8a26484f467b1b1c` | `reference-semantics/semantics/subscript.k:66-67` | rule; none; fixed-semantic+ordinary-rule | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| `f6dff620c7b782c9` | `reference-semantics/semantics/subscript.k:68-71` | rule; none; fixed-semantic+ordinary-rule | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` |
| `275e604cf5682b61` | `reference-semantics/semantics/subscript.k:72-72` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= slStep(OptInt) [function, total]` |
| `24a30b91d4af6297` | `reference-semantics/semantics/subscript.k:73-73` | rule; none; fixed-semantic+ordinary-rule | `rule slStep(noB) => 1` |
| `ce0ff22ba34bb53c` | `reference-semantics/semantics/subscript.k:74-74` | rule; none; fixed-semantic+ordinary-rule | `rule slStep(someB(S:Int)) => S` |
| `a00deafa681ecb53` | `reference-semantics/semantics/subscript.k:76-76` | syntax; function; syntax-declaration+function | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| `1b226a779a401299` | `reference-semantics/semantics/subscript.k:77-78` | rule; none; fixed-semantic+ordinary-rule | `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| `91eee5504516a9ed` | `reference-semantics/semantics/subscript.k:79-80` | rule; none; fixed-semantic+ordinary-rule | `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0` |
| `4c0c7f511acff912` | `reference-semantics/semantics/subscript.k:81-81` | rule; none; fixed-semantic+ordinary-rule | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| `396daad011c3354c` | `reference-semantics/semantics/subscript.k:83-83` | syntax; function; syntax-declaration+function | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| `e8f53feef88907c9` | `reference-semantics/semantics/subscript.k:84-85` | rule; none; fixed-semantic+ordinary-rule | `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0` |
| `911b87bd57637cd8` | `reference-semantics/semantics/subscript.k:86-87` | rule; none; fixed-semantic+ordinary-rule | `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| `a27be61a16630b70` | `reference-semantics/semantics/subscript.k:88-88` | rule; none; fixed-semantic+ordinary-rule | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| `9fbf6ac53528ba1d` | `reference-semantics/semantics/subscript.k:90-90` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| `47cb6df7aaa3122c` | `reference-semantics/semantics/subscript.k:91-92` | rule; none; fixed-semantic+ordinary-rule | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0` |
| `a6903ef9677367f5` | `reference-semantics/semantics/subscript.k:93-94` | rule; none; fixed-semantic+ordinary-rule | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| `2b7fa04bbad26a1a` | `reference-semantics/semantics/subscript.k:96-96` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| `739057aea4f0bae1` | `reference-semantics/semantics/subscript.k:97-98` | rule; none; fixed-semantic+ordinary-rule | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| `dd939205f4d73dc4` | `reference-semantics/semantics/subscript.k:99-100` | rule; none; fixed-semantic+ordinary-rule | `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| `52ebc06ec75418ed` | `reference-semantics/semantics/subscript.k:102-102` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| `b62486276bb5d7ad` | `reference-semantics/semantics/subscript.k:103-104` | rule; none; fixed-semantic+ordinary-rule | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN` |
| `95aec02e861865aa` | `reference-semantics/semantics/subscript.k:105-108` | rule; none; fixed-semantic+ordinary-rule | `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` |
| `895c8871bab6986f` | `reference-semantics/semantics/subscript.k:109-109` | syntax; function; syntax-declaration+function | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| `ea3de8718f6b4da8` | `reference-semantics/semantics/subscript.k:110-112` | rule; none; fixed-semantic+ordinary-rule | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| `0f5bc7115ed3dfda` | `reference-semantics/semantics/subscript.k:113-114` | rule; none; fixed-semantic+ordinary-rule | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| `e037f8452584028c` | `reference-semantics/semantics/subscript.k:116-116` | syntax; function; syntax-declaration+function | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| `0548502e672b2576` | `reference-semantics/semantics/subscript.k:117-119` | rule; none; fixed-semantic+ordinary-rule | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| `0c2cb828d8456512` | `reference-semantics/semantics/subscript.k:120-121` | rule; none; fixed-semantic+ordinary-rule | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| `3406bb279e559e0a` | `reference-semantics/semantics/syntax.k:9-30` | syntax; macro,seqstrict,strict; macro-or-alias | `syntax Expr ::= "Int" "(" Int ")" \| "Float" "(" Float ")" \| "Bool" "(" Bool ")" \| "Name" "(" String ")" \| "Str" "(" String ")" \| "UnaryOp" "(" String "," Expr ")" [strict(2)] \| "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp" "(" String "," Exprs ")" \| "ListExpr" "(" Exprs ")" \| "DictExpr" "(" Entries ")" \| "ListComp" "(" Expr "," CompFors ")" [macro] \| "GenExp" "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda" "(" Params "," Expr ")" \| "KwArg" "(" String "," Expr ")" \| "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call" "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare" "(" Expr "," CmpOp ")"` |
| `d7bcee886a341a34` | `reference-semantics/semantics/syntax.k:32-32` | syntax; none; syntax-declaration | `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"` |
| `3c0858ebcb2767a8` | `reference-semantics/semantics/syntax.k:33-33` | syntax; none; syntax-declaration | `syntax Entry ::= "Entry" "(" Expr "," Expr ")"` |
| `6d78e696c0630fb1` | `reference-semantics/semantics/syntax.k:34-34` | syntax; none; syntax-declaration | `syntax Entries ::= List{Entry, ","}` |
| `98bccb7e873de4ce` | `reference-semantics/semantics/syntax.k:35-35` | syntax; none; syntax-declaration | `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| `e64d2b9cbdfa9e17` | `reference-semantics/semantics/syntax.k:36-36` | syntax; none; syntax-declaration | `syntax CompFors ::= List{CompFor, ""}` |
| `cf43efe2aec689ff` | `reference-semantics/semantics/syntax.k:37-37` | syntax; none; syntax-declaration | `syntax Exprs ::= List{Expr, ","}` |
| `9cd0847a8398c937` | `reference-semantics/semantics/syntax.k:38-38` | syntax; none; syntax-declaration | `syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| `d2e84ffc5c0aa1bf` | `reference-semantics/semantics/syntax.k:39-39` | syntax; none; syntax-declaration | `syntax Bound ::= Expr \| "NoBound"` |
| `952f94c67437610f` | `reference-semantics/semantics/syntax.k:41-54` | syntax; strict; syntax-declaration | `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] \| "Import" "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While" "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return" "(" Expr ")" [strict] \| "Assert" "(" Expr ")" [strict] \| "Expr" "(" Expr ")" [strict] \| "FuncDef" "(" String "," Params "," Stmts ")" \| "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` |
| `c3de41ebe7b68c78` | `reference-semantics/semantics/syntax.k:56-56` | syntax; none; syntax-declaration | `syntax Stmts ::= List{Stmt, ""}` |
| `598d7a233e230122` | `reference-semantics/semantics/syntax.k:57-57` | syntax; none; syntax-declaration | `syntax Params ::= "Params" "(" ParamNames ")"` |
| `ef7b331b83887807` | `reference-semantics/semantics/syntax.k:58-58` | syntax; none; syntax-declaration | `syntax CellVars ::= "CellVars" "(" ParamNames ")"` |
| `9a403c2ceaa7e3c9` | `reference-semantics/semantics/syntax.k:59-59` | syntax; none; syntax-declaration | `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"` |
| `3f16a47b70ac43e4` | `reference-semantics/semantics/syntax.k:60-60` | syntax; none; syntax-declaration | `syntax ParamNames ::= List{String, ","}` |
| `1d7095d18e6be655` | `reference-semantics/semantics/syntax.k:61-61` | syntax; none; syntax-declaration | `syntax Module ::= "Module" "(" Stmts ")"` |
| `2d8702f58264c54f` | `reference-semantics/semantics/tuple.k:10-10` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>` |
| `07f7a8b7e262413f` | `reference-semantics/semantics/tuple.k:11-13` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| `c552fa9db621ba66` | `reference-semantics/semantics/tuple.k:14-14` | syntax; none; syntax-declaration | `syntax ApplyK ::= "toTuple"` |
| `b9ef54af54f3d06c` | `reference-semantics/semantics/tuple.k:15-15` | rule; none; fixed-semantic+ordinary-rule | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| `008bebe27521787c` | `reference-semantics/semantics/tuple.k:16-16` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| `015c305504e39b86` | `reference-semantics/semantics/tuple.k:18-19` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| `1974389be8861ed3` | `reference-semantics/semantics/tuple.k:20-20` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| `97b63d3106aad43c` | `reference-semantics/semantics/tuple.k:21-22` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| `248b9d3cd1bc9772` | `reference-semantics/semantics/tuple.k:23-23` | rule; none; fixed-semantic+ordinary-rule | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| `b179f0092867986b` | `reference-semantics/semantics/tuple.k:24-24` | syntax; function; syntax-declaration+function | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| `bc51158c4c2765b3` | `reference-semantics/semantics/tuple.k:25-25` | rule; none; fixed-semantic+ordinary-rule | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| `e28143c73f8d957c` | `reference-semantics/semantics/tuple.k:26-27` | rule; none; fixed-semantic+ordinary-rule | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| `f6743969c2e600ff` | `reference-semantics/semantics/tuple.k:28-30` | rule; none; fixed-semantic+ordinary-rule | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| `b40ad1280313b43b` | `reference-semantics/semantics/tuple.k:31-31` | syntax; none; syntax-declaration | `syntax KItem ::= #bindTgt(Expr, Val)` |
| `1fb4fd933f76d472` | `reference-semantics/semantics/tuple.k:32-34` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| `d121ed9f0f10bf7e` | `reference-semantics/semantics/tuple.k:35-41` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| `3c286e2bd0f5a992` | `reference-semantics/semantics/tuple.k:42-42` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `3d1f6f72dee9dc5e` | `reference-semantics/semantics/tuple.k:43-43` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `dc554a9b9245ffc9` | `reference-semantics/semantics/tuple.k:44-48` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `d57fb7432141f027` | `reference-semantics/semantics/tuple.k:49-49` | syntax; none; syntax-declaration | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| `a20bede20f1a30fc` | `reference-semantics/semantics/tuple.k:50-50` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `9426c12da876aca7` | `reference-semantics/semantics/tuple.k:51-51` | rule; none; fixed-semantic+ordinary-rule | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `e70baa07383b4778` | `reference-semantics/semantics/tuple.k:52-54` | rule; priority; fixed-semantic+ordinary-rule+priority | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| `cf9076dcb359d262` | `reference-semantics/semantics/tuple.k:55-56` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| `bff530acc8e0a632` | `reference-semantics/semantics/tuple.k:57-57` | rule; none; fixed-semantic+ordinary-rule | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| `a19cfe5fc346e4cb` | `verification.k:12-12` | syntax; function,total; syntax-declaration+function+total | `syntax Int ::= gcdEuclid(Int, Int) [function, total]` |
| `ef54aedd53e26411` | `verification.k:13-13` | rule; simplification; proof-local+simplification-rule | `rule gcdEuclid(A:Int, 0) => absInt(A) [simplification]` |
| `0798a8d1421064b1` | `verification.k:14-16` | rule; simplification; proof-local+simplification-rule | `rule gcdEuclid(A:Int, B:Int) => gcdEuclid(B, pyMod(A, B)) requires B =/=Int 0 [simplification]` |
| `4868801bbc6fc524` | `spec.k:6-40` | claim; none; reachability-claim | `claim [gcd-loop]: <k> #while( Compare(Name("b"), CmpOp("!=", Int(0))), Assign(Name("remainder"), BinOp("%", Name("a"), Name("b"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("remainder")) ) ~> (Return(Call(Name("abs"), Name("a"))) .Stmts) ~> #endcall => gcdEuclid(A, B) ~> CONT </k> <env> 1 => 0 </env> <scopes> ( 0 \|-> scope(GLOBALS, parent(-1)) 1 \|-> scope( "a" \|-> A "b" \|-> B "remainder" \|-> _R, parent(0) ) -1 \|-> builtinsScope ) => ( 0 \|-> scope(GLOBALS, parent(-1)) -1 \|-> builtinsScope ) </scopes> <scopeLoc> 2 => 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> ListItem(frame(CONT, 0, 1)) => .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires notBool ("abs" in_keys(GLOBALS))` |
| `6ebcb5fa6f7ac3be` | `spec.k:42-117` | claim; none; reachability-claim | `claim [gcd-entry]: <k> Call( Name("greatest_common_divisor"), Int(A), Int(B) ) => #while( Compare(Name("b"), CmpOp("!=", Int(0))), Assign(Name("remainder"), BinOp("%", Name("a"), Name("b"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("remainder")) ) ~> (Return(Call(Name("abs"), Name("a"))) .Stmts) ~> #endcall </k> <env> 0 => 1 </env> <scopes> ( 0 \|-> scope( "greatest_common_divisor" \|-> closureVal( ("a", "b"), Expr( Str("Return the non-negative greatest common divisor of a and b.") ) Assign(Name("remainder"), Int(0)) While( Compare(Name("b"), CmpOp("!=", Int(0))), Assign(Name("remainder"), BinOp("%", Name("a"), Name("b"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("remainder")) ) Return(Call(Name("abs"), Name("a"))), 0 ), parent(-1) ) -1 \|-> builtinsScope ) => ( 0 \|-> scope( "greatest_common_divisor" \|-> closureVal( ("a", "b"), Expr( Str("Return the non-negative greatest common divisor of a and b.") ) Assign(Name("remainder"), Int(0)) While( Compare(Name("b"), CmpOp("!=", Int(0))), Assign(Name("remainder"), BinOp("%", Name("a"), Name("b"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("remainder")) ) Return(Call(Name("abs"), Name("a"))), 0 ), parent(-1) ) 1 \|-> scope( "a" \|-> A "b" \|-> B "remainder" \|-> 0, parent(0) ) -1 \|-> builtinsScope ) </scopes> <scopeLoc> 1 => 2 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List => ListItem(frame(.K, 0, 1)) </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code>` |

# Exhaustive lexical K inventory

Source root: `/tmp/audit-work/reconstruction`

Files: 26; records: 1160

Sentence counts: `{'claim': 5, 'configuration': 1, 'context': 5, 'endmodule': 27, 'imports': 88, 'module': 27, 'requires': 25, 'rule': 740, 'syntax': 242}`

Rule tags: `{'ordinary': 730, 'owise': 29, 'priority': 70, 'simplification': 10}`

Syntax tags: `{'function': 152, 'macro': 11, 'symbol': 25, 'token': 2, 'total': 113}`

| # | File:line | Kind | Tags | Full normalized sentence |
|---:|---|---|---|---|
| 1 | `reference-semantics/semantics/assert.k:3` | module |  | `module MPY-ASSERT` |
| 2 | `reference-semantics/semantics/assert.k:4` | imports |  | `imports MPY-CORE` |
| 3 | `reference-semantics/semantics/assert.k:6` | rule | ordinary | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| 4 | `reference-semantics/semantics/assert.k:8` | rule | ordinary | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| 5 | `reference-semantics/semantics/assert.k:13` | rule | ordinary, priority | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 6 | `reference-semantics/semantics/assert.k:16` | endmodule |  | `endmodule` |
| 7 | `reference-semantics/semantics/bool.k:5` | module |  | `module MPY-BOOL` |
| 8 | `reference-semantics/semantics/bool.k:6` | imports |  | `imports MPY-CORE` |
| 9 | `reference-semantics/semantics/bool.k:8` | rule | ordinary | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 10 | `reference-semantics/semantics/bool.k:10` | rule | ordinary | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 11 | `reference-semantics/semantics/bool.k:11` | rule | ordinary | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 // ==== BoolOp: short-circuit, value-returning and / or ===================== // the node is its own accumulator: heat the HEAD element only, then either return it // (short-circuit) or drop it and continue` |
| 12 | `reference-semantics/semantics/bool.k:16` | context |  | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 13 | `reference-semantics/semantics/bool.k:17` | rule | ordinary | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 14 | `reference-semantics/semantics/bool.k:18` | rule | ordinary | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| 15 | `reference-semantics/semantics/bool.k:20` | rule | ordinary | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| 16 | `reference-semantics/semantics/bool.k:22` | rule | ordinary | `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| 17 | `reference-semantics/semantics/bool.k:24` | rule | ordinary | `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the // operand — and/or return the OBJECT itself (Python identity), not its structure` |
| 18 | `reference-semantics/semantics/bool.k:29` | rule | ordinary, priority | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| 19 | `reference-semantics/semantics/bool.k:31` | rule | ordinary, priority | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 20 | `reference-semantics/semantics/bool.k:35` | rule | ordinary, priority | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 21 | `reference-semantics/semantics/bool.k:39` | rule | ordinary, priority | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 22 | `reference-semantics/semantics/bool.k:43` | rule | ordinary, priority | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 23 | `reference-semantics/semantics/bool.k:47` | endmodule |  | `endmodule` |
| 24 | `reference-semantics/semantics/builtins.k:3` | module |  | `module MPY-BUILTINS` |
| 25 | `reference-semantics/semantics/builtins.k:4` | imports |  | `imports MPY-CORE` |
| 26 | `reference-semantics/semantics/builtins.k:5` | imports |  | `imports MPY-STR` |
| 27 | `reference-semantics/semantics/builtins.k:6` | imports |  | `imports MPY-SET` |
| 28 | `reference-semantics/semantics/builtins.k:7` | imports |  | `imports MPY-ITER` |
| 29 | `reference-semantics/semantics/builtins.k:8` | imports |  | `imports MPY-RANGE` |
| 30 | `reference-semantics/semantics/builtins.k:9` | imports |  | `imports MPY-INT` |
| 31 | `reference-semantics/semantics/builtins.k:10` | imports |  | `imports MPY-METHODS // the builtins REGISTRY is core.k's builtinsScope (the -1 frame); names resolve by lookup // Call routing + argument evaluation live in call.k, which also routes the fold // builtins (sum/all/any/max/min) to the #_Acc folds below and everything else to // applyBuiltin. This module owns applyBuiltin + the fold implementations.` |
| 32 | `reference-semantics/semantics/builtins.k:17` | syntax | function | `syntax Val ::= applyBuiltin(String, Vals) [function] // ==== len(obj) — O(1) per kind ============================================` |
| 33 | `reference-semantics/semantics/builtins.k:20` | syntax | function | `syntax Int ::= seqLen(Val) [function]` |
| 34 | `reference-semantics/semantics/builtins.k:21` | rule | ordinary | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 35 | `reference-semantics/semantics/builtins.k:22` | rule | ordinary | `rule seqLen(list(VS:ValSeq)) => vsLen(VS)` |
| 36 | `reference-semantics/semantics/builtins.k:23` | rule | ordinary | `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)` |
| 37 | `reference-semantics/semantics/builtins.k:24` | rule | ordinary | `rule seqLen(str(IS:IntSeq)) => isLen(IS)` |
| 38 | `reference-semantics/semantics/builtins.k:25` | rule | ordinary | `rule seqLen(setV(DS:IntSeq)) => isLen(DS)` |
| 39 | `reference-semantics/semantics/builtins.k:26` | rule | ordinary | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) == // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order). // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed. // (k-cell — list() constructs a NEW object)` |
| 40 | `reference-semantics/semantics/builtins.k:32` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 41 | `reference-semantics/semantics/builtins.k:33` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 42 | `reference-semantics/semantics/builtins.k:34` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>` |
| 43 | `reference-semantics/semantics/builtins.k:35` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>` |
| 44 | `reference-semantics/semantics/builtins.k:36` | syntax | function, total | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 45 | `reference-semantics/semantics/builtins.k:37` | rule | ordinary | `rule charsOf(.IntSeq) => .ValSeq` |
| 46 | `reference-semantics/semantics/builtins.k:38` | rule | ordinary | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) // ==== set(str) — distinct character codes =================================` |
| 47 | `reference-semantics/semantics/builtins.k:41` | rule | ordinary | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) // ==== abs(int) ============================================================` |
| 48 | `reference-semantics/semantics/builtins.k:44` | rule | ordinary | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==` |
| 49 | `reference-semantics/semantics/builtins.k:47` | syntax |  | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 50 | `reference-semantics/semantics/builtins.k:48` | rule | ordinary | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 51 | `reference-semantics/semantics/builtins.k:49` | rule | ordinary | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 52 | `reference-semantics/semantics/builtins.k:50` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| 53 | `reference-semantics/semantics/builtins.k:54` | syntax | function | `syntax Int ::= intOf(Val) [function]` |
| 54 | `reference-semantics/semantics/builtins.k:55` | rule | ordinary | `rule intOf(I:Int) => I` |
| 55 | `reference-semantics/semantics/builtins.k:56` | rule | ordinary | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi // ==== all / any (short-circuiting #iterNext folds) ========================` |
| 56 | `reference-semantics/semantics/builtins.k:59` | syntax |  | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 57 | `reference-semantics/semantics/builtins.k:60` | rule | ordinary | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 58 | `reference-semantics/semantics/builtins.k:61` | rule | ordinary | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 59 | `reference-semantics/semantics/builtins.k:62` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| 60 | `reference-semantics/semantics/builtins.k:64` | rule | ordinary | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| 61 | `reference-semantics/semantics/builtins.k:67` | syntax |  | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 62 | `reference-semantics/semantics/builtins.k:68` | rule | ordinary | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 63 | `reference-semantics/semantics/builtins.k:69` | rule | ordinary | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 64 | `reference-semantics/semantics/builtins.k:70` | rule | ordinary | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| 65 | `reference-semantics/semantics/builtins.k:72` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) // ==== max / min over an iterable (#iterNext folds; first element seeds) ====` |
| 66 | `reference-semantics/semantics/builtins.k:76` | syntax |  | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 67 | `reference-semantics/semantics/builtins.k:77` | rule | ordinary | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 68 | `reference-semantics/semantics/builtins.k:78` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 69 | `reference-semantics/semantics/builtins.k:80` | rule | ordinary | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 70 | `reference-semantics/semantics/builtins.k:81` | rule | ordinary | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 71 | `reference-semantics/semantics/builtins.k:82` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 72 | `reference-semantics/semantics/builtins.k:86` | syntax |  | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 73 | `reference-semantics/semantics/builtins.k:87` | rule | ordinary | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 74 | `reference-semantics/semantics/builtins.k:88` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 75 | `reference-semantics/semantics/builtins.k:90` | rule | ordinary | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 76 | `reference-semantics/semantics/builtins.k:91` | rule | ordinary | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 77 | `reference-semantics/semantics/builtins.k:92` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) // ==== variadic max / min (a Vals fold) ====================================` |
| 78 | `reference-semantics/semantics/builtins.k:97` | syntax | function | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 79 | `reference-semantics/semantics/builtins.k:98` | rule | ordinary | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 80 | `reference-semantics/semantics/builtins.k:99` | rule | ordinary | `rule maxVals(M:Int, .Vals) => M` |
| 81 | `reference-semantics/semantics/builtins.k:100` | rule | ordinary | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| 82 | `reference-semantics/semantics/builtins.k:102` | syntax | function | `syntax Int ::= minVals(Int, Vals) [function]` |
| 83 | `reference-semantics/semantics/builtins.k:103` | rule | ordinary | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 84 | `reference-semantics/semantics/builtins.k:104` | rule | ordinary | `rule minVals(M:Int, .Vals) => M` |
| 85 | `reference-semantics/semantics/builtins.k:105` | rule | ordinary | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==` |
| 86 | `reference-semantics/semantics/builtins.k:108` | rule | ordinary | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 // negative operand: the '-' sign prefixes the magnitude's digits` |
| 87 | `reference-semantics/semantics/builtins.k:111` | rule | ordinary | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| 88 | `reference-semantics/semantics/builtins.k:114` | syntax | function, total | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 89 | `reference-semantics/semantics/builtins.k:115` | rule | ordinary | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 90 | `reference-semantics/semantics/builtins.k:116` | rule | ordinary | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 91 | `reference-semantics/semantics/builtins.k:117` | syntax | function, total | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 92 | `reference-semantics/semantics/builtins.k:118` | rule | ordinary | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 93 | `reference-semantics/semantics/builtins.k:119` | rule | ordinary | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========` |
| 94 | `reference-semantics/semantics/builtins.k:124` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| 95 | `reference-semantics/semantics/builtins.k:126` | syntax | function, total | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 96 | `reference-semantics/semantics/builtins.k:127` | rule | ordinary | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 97 | `reference-semantics/semantics/builtins.k:128` | rule | ordinary | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) // ==== map(str, xs) — eager (only the str case is in the subset) =============` |
| 98 | `reference-semantics/semantics/builtins.k:132` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| 99 | `reference-semantics/semantics/builtins.k:134` | syntax | function, total | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 100 | `reference-semantics/semantics/builtins.k:135` | rule | ordinary | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 101 | `reference-semantics/semantics/builtins.k:136` | rule | ordinary | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 102 | `reference-semantics/semantics/builtins.k:137` | rule | ordinary | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) // ==== int(x) identities (int(round(x)) composes through) ====================` |
| 103 | `reference-semantics/semantics/builtins.k:140` | rule | ordinary | `rule applyBuiltin("int", I:Int, .Vals) => I // ==== ord / chr ===========================================================` |
| 104 | `reference-semantics/semantics/builtins.k:143` | rule | ordinary | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 105 | `reference-semantics/semantics/builtins.k:144` | rule | ordinary | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 // ==== str(int) / str(str) =================================================` |
| 106 | `reference-semantics/semantics/builtins.k:148` | rule | ordinary | `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))` |
| 107 | `reference-semantics/semantics/builtins.k:149` | rule | ordinary | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====` |
| 108 | `reference-semantics/semantics/builtins.k:152` | rule | ordinary | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)` |
| 109 | `reference-semantics/semantics/builtins.k:156` | rule | ordinary | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| 110 | `reference-semantics/semantics/builtins.k:158` | syntax | function, total | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 111 | `reference-semantics/semantics/builtins.k:159` | rule | ordinary | `rule intDigAcc(.IntSeq, ACC:Int) => ACC` |
| 112 | `reference-semantics/semantics/builtins.k:160` | rule | ordinary | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====` |
| 113 | `reference-semantics/semantics/builtins.k:163` | rule | ordinary | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 114 | `reference-semantics/semantics/builtins.k:164` | rule | ordinary | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B) // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)` |
| 115 | `reference-semantics/semantics/builtins.k:167` | rule | ordinary | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| 116 | `reference-semantics/semantics/builtins.k:169` | rule | ordinary | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>` |
| 117 | `reference-semantics/semantics/builtins.k:170` | rule | ordinary | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 118 | `reference-semantics/semantics/builtins.k:171` | rule | ordinary | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| 119 | `reference-semantics/semantics/builtins.k:173` | rule | ordinary | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>` |
| 120 | `reference-semantics/semantics/builtins.k:174` | rule | ordinary | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> // ==== range(stop) / range(start, stop) / range(start, stop, step) =========` |
| 121 | `reference-semantics/semantics/builtins.k:177` | rule | ordinary | `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)` |
| 122 | `reference-semantics/semantics/builtins.k:178` | rule | ordinary | `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)` |
| 123 | `reference-semantics/semantics/builtins.k:179` | rule | ordinary | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ======== // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's // trusted pass evaluator, now DEFINED in the reference and driven by a // code-level tokenizer. Reduces on concrete strings (krun); a symbolic // argument leaves the call unevaluated for problem-level folds.` |
| 124 | `reference-semantics/semantics/builtins.k:187` | rule | ordinary | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 125 | `reference-semantics/semantics/builtins.k:188` | syntax | function | `syntax Int ::= evalArith(IntSeq) [function]` |
| 126 | `reference-semantics/semantics/builtins.k:189` | rule | ordinary | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| 127 | `reference-semantics/semantics/builtins.k:192` | syntax |  | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| 128 | `reference-semantics/semantics/builtins.k:194` | syntax | function, total | `syntax Bool ::= evDigit(Int) [function, total]` |
| 129 | `reference-semantics/semantics/builtins.k:195` | rule | ordinary | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 130 | `reference-semantics/semantics/builtins.k:196` | syntax | function, total | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 131 | `reference-semantics/semantics/builtins.k:197` | rule | ordinary | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 132 | `reference-semantics/semantics/builtins.k:198` | rule | ordinary, owise | `rule evHead42(_:IntSeq) => false [owise]` |
| 133 | `reference-semantics/semantics/builtins.k:199` | syntax | function, total | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 134 | `reference-semantics/semantics/builtins.k:200` | rule | ordinary | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 135 | `reference-semantics/semantics/builtins.k:201` | rule | ordinary, owise | `rule evHead47(_:IntSeq) => false [owise]` |
| 136 | `reference-semantics/semantics/builtins.k:203` | syntax | function, total | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 137 | `reference-semantics/semantics/builtins.k:204` | rule | ordinary | `rule tokOps(.IntSeq) => .OpSeq` |
| 138 | `reference-semantics/semantics/builtins.k:205` | rule | ordinary | `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)` |
| 139 | `reference-semantics/semantics/builtins.k:206` | rule | ordinary | `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)` |
| 140 | `reference-semantics/semantics/builtins.k:207` | rule | ordinary | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 141 | `reference-semantics/semantics/builtins.k:208` | rule | ordinary | `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 142 | `reference-semantics/semantics/builtins.k:209` | rule | ordinary | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 143 | `reference-semantics/semantics/builtins.k:210` | rule | ordinary | `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 144 | `reference-semantics/semantics/builtins.k:211` | rule | ordinary | `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))` |
| 145 | `reference-semantics/semantics/builtins.k:212` | rule | ordinary | `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))` |
| 146 | `reference-semantics/semantics/builtins.k:214` | syntax | function, total | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| 147 | `reference-semantics/semantics/builtins.k:216` | rule | ordinary | `rule tokNds(.IntSeq) => .IntSeq` |
| 148 | `reference-semantics/semantics/builtins.k:217` | rule | ordinary | `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)` |
| 149 | `reference-semantics/semantics/builtins.k:218` | rule | ordinary | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 150 | `reference-semantics/semantics/builtins.k:219` | rule | ordinary | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| 151 | `reference-semantics/semantics/builtins.k:221` | rule | ordinary | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| 152 | `reference-semantics/semantics/builtins.k:223` | rule | ordinary, owise | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 153 | `reference-semantics/semantics/builtins.k:225` | syntax |  | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 154 | `reference-semantics/semantics/builtins.k:226` | syntax | function, total | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 155 | `reference-semantics/semantics/builtins.k:227` | rule | ordinary | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 156 | `reference-semantics/semantics/builtins.k:228` | rule | ordinary, owise | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 157 | `reference-semantics/semantics/builtins.k:230` | syntax | function, total | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 158 | `reference-semantics/semantics/builtins.k:231` | rule | ordinary | `rule applyOpE("+", A:Int, B:Int) => A +Int B` |
| 159 | `reference-semantics/semantics/builtins.k:232` | rule | ordinary | `rule applyOpE("-", A:Int, B:Int) => A -Int B` |
| 160 | `reference-semantics/semantics/builtins.k:233` | rule | ordinary | `rule applyOpE("*", A:Int, B:Int) => A *Int B` |
| 161 | `reference-semantics/semantics/builtins.k:234` | rule | ordinary | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 162 | `reference-semantics/semantics/builtins.k:235` | rule | ordinary | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 163 | `reference-semantics/semantics/builtins.k:236` | rule | ordinary, owise | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 164 | `reference-semantics/semantics/builtins.k:238` | syntax | function, total | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 165 | `reference-semantics/semantics/builtins.k:239` | rule | ordinary | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 166 | `reference-semantics/semantics/builtins.k:240` | rule | ordinary | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 167 | `reference-semantics/semantics/builtins.k:241` | rule | ordinary | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| 168 | `reference-semantics/semantics/builtins.k:243` | rule | ordinary, owise | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 169 | `reference-semantics/semantics/builtins.k:244` | syntax | function, total | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 170 | `reference-semantics/semantics/builtins.k:245` | rule | ordinary | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 171 | `reference-semantics/semantics/builtins.k:246` | rule | ordinary | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 172 | `reference-semantics/semantics/builtins.k:247` | syntax | function, total | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 173 | `reference-semantics/semantics/builtins.k:248` | rule | ordinary | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 174 | `reference-semantics/semantics/builtins.k:250` | syntax | function, total | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 175 | `reference-semantics/semantics/builtins.k:251` | rule | ordinary | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 176 | `reference-semantics/semantics/builtins.k:252` | rule | ordinary | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 177 | `reference-semantics/semantics/builtins.k:253` | rule | ordinary | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 178 | `reference-semantics/semantics/builtins.k:254` | rule | ordinary | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 179 | `reference-semantics/semantics/builtins.k:255` | syntax | function, total | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 180 | `reference-semantics/semantics/builtins.k:256` | rule | ordinary | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 181 | `reference-semantics/semantics/builtins.k:257` | rule | ordinary | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| 182 | `reference-semantics/semantics/builtins.k:260` | rule | ordinary | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| 183 | `reference-semantics/semantics/builtins.k:263` | rule | ordinary, owise | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| 184 | `reference-semantics/semantics/builtins.k:265` | syntax | function, total | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 185 | `reference-semantics/semantics/builtins.k:266` | rule | ordinary | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 186 | `reference-semantics/semantics/builtins.k:267` | rule | ordinary | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 187 | `reference-semantics/semantics/builtins.k:268` | rule | ordinary, owise | `rule inLevelE(_:String, _:String) => false [owise]` |
| 188 | `reference-semantics/semantics/builtins.k:269` | syntax | function, total | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 189 | `reference-semantics/semantics/builtins.k:270` | rule | ordinary | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 190 | `reference-semantics/semantics/builtins.k:271` | rule | ordinary | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 191 | `reference-semantics/semantics/builtins.k:272` | syntax | function, total | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 192 | `reference-semantics/semantics/builtins.k:273` | rule | ordinary | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 193 | `reference-semantics/semantics/builtins.k:274` | rule | ordinary | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ================== // The md5 value itself is a named shared trust (sortVS-style, no concrete // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).` |
| 194 | `reference-semantics/semantics/builtins.k:279` | syntax |  | `syntax KItem ::= "#md5"` |
| 195 | `reference-semantics/semantics/builtins.k:280` | rule | ordinary, priority | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| 196 | `reference-semantics/semantics/builtins.k:282` | rule | ordinary | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 197 | `reference-semantics/semantics/builtins.k:283` | syntax |  | `syntax Val ::= md5Obj(IntSeq)` |
| 198 | `reference-semantics/semantics/builtins.k:284` | rule | ordinary | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 199 | `reference-semantics/semantics/builtins.k:285` | syntax | function, total, symbol | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] // ==== isinstance(V, int\|str) — an ordinary 2-arg builtin =================== // The type argument (int/str) is an ordinary name that resolves via the builtins frame to // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).` |
| 200 | `reference-semantics/semantics/builtins.k:291` | rule | ordinary | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 201 | `reference-semantics/semantics/builtins.k:292` | rule | ordinary | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 202 | `reference-semantics/semantics/builtins.k:293` | syntax | function | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 203 | `reference-semantics/semantics/builtins.k:294` | rule | ordinary | `rule isIntV(_:Int) => true` |
| 204 | `reference-semantics/semantics/builtins.k:295` | rule | ordinary, owise | `rule isIntV(_:Val) => false [owise]` |
| 205 | `reference-semantics/semantics/builtins.k:296` | rule | ordinary | `rule isStrV(str(_:IntSeq)) => true` |
| 206 | `reference-semantics/semantics/builtins.k:297` | rule | ordinary, owise | `rule isStrV(_:Val) => false [owise]` |
| 207 | `reference-semantics/semantics/builtins.k:298` | endmodule |  | `endmodule` |
| 208 | `reference-semantics/semantics/call.k:10` | module |  | `module MPY-CALL` |
| 209 | `reference-semantics/semantics/call.k:11` | imports |  | `imports MPY-METHODS` |
| 210 | `reference-semantics/semantics/call.k:12` | imports |  | `imports MPY-BUILTINS` |
| 211 | `reference-semantics/semantics/call.k:13` | imports |  | `imports MPY-FUNCTIONS // a cooled attribute is a bound method value` |
| 212 | `reference-semantics/semantics/call.k:16` | rule | ordinary, owise | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)` |
| 213 | `reference-semantics/semantics/call.k:19` | syntax |  | `syntax KItem ::= #callee(Exprs)` |
| 214 | `reference-semantics/semantics/call.k:20` | rule | ordinary, owise | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 215 | `reference-semantics/semantics/call.k:21` | rule | ordinary | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> // ==== dispatch on the callee value ========================================` |
| 216 | `reference-semantics/semantics/call.k:24` | rule | ordinary | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 217 | `reference-semantics/semantics/call.k:26` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 218 | `reference-semantics/semantics/call.k:27` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>` |
| 219 | `reference-semantics/semantics/call.k:28` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>` |
| 220 | `reference-semantics/semantics/call.k:29` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>` |
| 221 | `reference-semantics/semantics/call.k:30` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>` |
| 222 | `reference-semantics/semantics/call.k:31` | rule | ordinary, owise | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 223 | `reference-semantics/semantics/call.k:32` | rule | ordinary | `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k> // ==== heap-object arguments/receivers ===================================== // Builtins and type calls READ structure — deref the first two arg positions // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list // methods take the ref itself; every other method receiver is deref'd.` |
| 224 | `reference-semantics/semantics/call.k:38` | rule | ordinary, priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 225 | `reference-semantics/semantics/call.k:42` | rule | ordinary, priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| 226 | `reference-semantics/semantics/call.k:47` | rule | ordinary, priority | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 227 | `reference-semantics/semantics/call.k:52` | syntax | function, total | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 228 | `reference-semantics/semantics/call.k:53` | rule | ordinary | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| 229 | `reference-semantics/semantics/call.k:56` | rule | ordinary, priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] // non-mutating methods READ their heap-object arguments too (join's list); // mutators keep refs (append of a list into a list-of-lists stays aliased)` |
| 230 | `reference-semantics/semantics/call.k:63` | rule | ordinary, priority | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| 231 | `reference-semantics/semantics/call.k:69` | rule | ordinary | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> // annotated closure: the frame starts with the captured freevar cells, its // parent is the module scope (all enclosing-local reads go through cells), // and the cellvars' fresh cells allocate before params bind (a cellvar param // then writes through its cell in #bindP).` |
| 232 | `reference-semantics/semantics/call.k:80` | rule | ordinary | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| 233 | `reference-semantics/semantics/call.k:87` | syntax |  | `syntax KItem ::= #allocCells(ParamNames)` |
| 234 | `reference-semantics/semantics/call.k:88` | rule | ordinary | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 235 | `reference-semantics/semantics/call.k:89` | rule | ordinary | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 236 | `reference-semantics/semantics/call.k:95` | endmodule |  | `endmodule` |
| 237 | `reference-semantics/semantics/comprehension.k:3` | module |  | `module MPY-COMPREHENSION` |
| 238 | `reference-semantics/semantics/comprehension.k:4` | imports |  | `imports MPY-CORE` |
| 239 | `reference-semantics/semantics/comprehension.k:5` | imports |  | `imports MPY-OPERATORS` |
| 240 | `reference-semantics/semantics/comprehension.k:6` | imports |  | `imports MPY-LIST` |
| 241 | `reference-semantics/semantics/comprehension.k:7` | imports |  | `imports MPY-CONTROLS` |
| 242 | `reference-semantics/semantics/comprehension.k:8` | imports |  | `imports MPY-FUNCTIONS // A comprehension is pure syntactic sugar` |
| 243 | `reference-semantics/semantics/comprehension.k:11` | rule | ordinary | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 244 | `reference-semantics/semantics/comprehension.k:12` | rule | ordinary | `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 245 | `reference-semantics/semantics/comprehension.k:14` | syntax | macro | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 246 | `reference-semantics/semantics/comprehension.k:15` | rule | ordinary | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| 247 | `reference-semantics/semantics/comprehension.k:18` | syntax | macro | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 248 | `reference-semantics/semantics/comprehension.k:19` | rule | ordinary | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| 249 | `reference-semantics/semantics/comprehension.k:21` | rule | ordinary | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| 250 | `reference-semantics/semantics/comprehension.k:24` | syntax | macro | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 251 | `reference-semantics/semantics/comprehension.k:25` | rule | ordinary | `rule compGuard(.Exprs) => Bool(true)` |
| 252 | `reference-semantics/semantics/comprehension.k:26` | rule | ordinary | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| 253 | `reference-semantics/semantics/comprehension.k:27` | endmodule |  | `endmodule` |
| 254 | `reference-semantics/semantics/concrete.k:8` | module |  | `module MPY-CONCRETE` |
| 255 | `reference-semantics/semantics/concrete.k:9` | imports |  | `imports MPY // deep equality for list compares whose elements are heap objects // (list-of-lists): Python == is structural at every depth.` |
| 256 | `reference-semantics/semantics/concrete.k:13` | rule | ordinary | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 257 | `reference-semantics/semantics/concrete.k:16` | rule | ordinary, priority | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) // ==== keyed sort, concrete leg ============================================ // Computes each key by a REAL call through the uniform #callee machinery // (closures, len, type objects all work), stable-inserts on the key, and // allocates the result. priority(40) beats sort.k's opaque rules, so krun // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.` |
| 258 | `reference-semantics/semantics/concrete.k:25` | syntax |  | `syntax Val ::= kvP(Val, Val)` |
| 259 | `reference-semantics/semantics/concrete.k:26` | syntax |  | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| 260 | `reference-semantics/semantics/concrete.k:28` | rule | ordinary, priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| 261 | `reference-semantics/semantics/concrete.k:31` | rule | ordinary, priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| 262 | `reference-semantics/semantics/concrete.k:34` | rule | ordinary | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| 263 | `reference-semantics/semantics/concrete.k:36` | rule | ordinary | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| 264 | `reference-semantics/semantics/concrete.k:38` | rule | ordinary | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| 265 | `reference-semantics/semantics/concrete.k:42` | syntax | function | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 266 | `reference-semantics/semantics/concrete.k:43` | rule | ordinary | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 267 | `reference-semantics/semantics/concrete.k:44` | rule | ordinary | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| 268 | `reference-semantics/semantics/concrete.k:47` | rule | ordinary | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| 269 | `reference-semantics/semantics/concrete.k:51` | syntax | function | `syntax Bool ::= kLt(Val, Val) [function]` |
| 270 | `reference-semantics/semantics/concrete.k:52` | rule | ordinary | `rule kLt(I1:Int, I2:Int) => I1 <Int I2` |
| 271 | `reference-semantics/semantics/concrete.k:53` | rule | ordinary | `rule kLt(F1:Float, F2:Float) => F1 <Float F2` |
| 272 | `reference-semantics/semantics/concrete.k:54` | rule | ordinary | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 273 | `reference-semantics/semantics/concrete.k:56` | syntax | function, total | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 274 | `reference-semantics/semantics/concrete.k:57` | rule | ordinary | `rule unpairVS(.ValSeq) => .ValSeq` |
| 275 | `reference-semantics/semantics/concrete.k:58` | rule | ordinary | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 276 | `reference-semantics/semantics/concrete.k:59` | rule | ordinary, owise | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| 277 | `reference-semantics/semantics/concrete.k:60` | endmodule |  | `endmodule` |
| 278 | `reference-semantics/semantics/controls.k:3` | module |  | `module MPY-CONTROLS` |
| 279 | `reference-semantics/semantics/controls.k:4` | imports |  | `imports MPY-CORE` |
| 280 | `reference-semantics/semantics/controls.k:5` | imports |  | `imports MPY-TUPLE` |
| 281 | `reference-semantics/semantics/controls.k:6` | imports |  | `imports MPY-ITER // ==== Assign / AugAssign (write the current scope; RHS evaluated by strictness) ==` |
| 282 | `reference-semantics/semantics/controls.k:9` | rule | ordinary | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 283 | `reference-semantics/semantics/controls.k:12` | rule | ordinary, priority | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 284 | `reference-semantics/semantics/controls.k:20` | rule | ordinary | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).` |
| 285 | `reference-semantics/semantics/controls.k:27` | rule | ordinary, priority | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] // ==== import trivia: `from math import floor, ceil` binds the supported // names as builtins in the current scope; every other import is a no-op` |
| 286 | `reference-semantics/semantics/controls.k:35` | rule | ordinary | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 287 | `reference-semantics/semantics/controls.k:36` | rule | ordinary, owise | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 288 | `reference-semantics/semantics/controls.k:37` | syntax |  | `syntax KItem ::= #bindImports(ParamNames)` |
| 289 | `reference-semantics/semantics/controls.k:38` | rule | ordinary | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 290 | `reference-semantics/semantics/controls.k:39` | rule | ordinary | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| 291 | `reference-semantics/semantics/controls.k:43` | rule | ordinary | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") // ==== Expr statement: evaluate for effect, discard the value =============== // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)` |
| 292 | `reference-semantics/semantics/controls.k:48` | rule | ordinary | `rule <k> Expr(_:Val) => .K ... </k> // ==== If (condition evaluated by strictness) ==============================` |
| 293 | `reference-semantics/semantics/controls.k:51` | syntax |  | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 294 | `reference-semantics/semantics/controls.k:52` | rule | ordinary | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 295 | `reference-semantics/semantics/controls.k:53` | rule | ordinary | `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>` |
| 296 | `reference-semantics/semantics/controls.k:54` | rule | ordinary | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> // ==== IfExp: ternary T if C else E ========================================` |
| 297 | `reference-semantics/semantics/controls.k:57` | rule | ordinary | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| 298 | `reference-semantics/semantics/controls.k:59` | rule | ordinary | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) // ==== For: one loop, in-cell continuation, over #iterNext ================= // (the iterable is evaluated once, by strictness; the protocol stays rewrites — // circularities anchor on #loop and narrowing substitutes the structure)` |
| 299 | `reference-semantics/semantics/controls.k:65` | syntax |  | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| 300 | `reference-semantics/semantics/controls.k:69` | rule | ordinary | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 301 | `reference-semantics/semantics/controls.k:71` | rule | ordinary | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 302 | `reference-semantics/semantics/controls.k:72` | rule | ordinary | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 303 | `reference-semantics/semantics/controls.k:73` | rule | ordinary | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> // ==== While ==============================================================` |
| 304 | `reference-semantics/semantics/controls.k:77` | rule | ordinary | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 305 | `reference-semantics/semantics/controls.k:78` | rule | ordinary | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 306 | `reference-semantics/semantics/controls.k:79` | rule | ordinary | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| 307 | `reference-semantics/semantics/controls.k:81` | rule | ordinary | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) // ==== loop control (break / continue) =====================================` |
| 308 | `reference-semantics/semantics/controls.k:85` | rule | ordinary | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 309 | `reference-semantics/semantics/controls.k:86` | rule | ordinary | `rule <k> Continue => #cont ... </k>` |
| 310 | `reference-semantics/semantics/controls.k:87` | rule | ordinary | `rule <k> Break => #brk ... </k>` |
| 311 | `reference-semantics/semantics/controls.k:88` | rule | ordinary | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 312 | `reference-semantics/semantics/controls.k:89` | rule | ordinary, owise | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 313 | `reference-semantics/semantics/controls.k:90` | rule | ordinary | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 314 | `reference-semantics/semantics/controls.k:91` | rule | ordinary, priority, owise | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] // ==== heap-object deref at the truthiness/iteration consumers ============== // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)` |
| 315 | `reference-semantics/semantics/controls.k:95` | rule | ordinary, priority | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 316 | `reference-semantics/semantics/controls.k:98` | rule | ordinary, priority | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 317 | `reference-semantics/semantics/controls.k:101` | rule | ordinary, priority | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // For derefs its iterable ONCE at loop start (iteration is over the snapshot; // mutating the iterated list inside its own loop is outside the subset)` |
| 318 | `reference-semantics/semantics/controls.k:106` | rule | ordinary, priority | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 319 | `reference-semantics/semantics/controls.k:109` | endmodule |  | `endmodule` |
| 320 | `reference-semantics/semantics/core.k:3` | module |  | `module MPY-CORE` |
| 321 | `reference-semantics/semantics/core.k:4` | imports |  | `imports MPY-SYNTAX` |
| 322 | `reference-semantics/semantics/core.k:5` | imports |  | `imports INT` |
| 323 | `reference-semantics/semantics/core.k:6` | imports |  | `imports BOOL` |
| 324 | `reference-semantics/semantics/core.k:7` | imports |  | `imports STRING` |
| 325 | `reference-semantics/semantics/core.k:8` | imports |  | `imports MAP` |
| 326 | `reference-semantics/semantics/core.k:9` | imports |  | `imports LIST` |
| 327 | `reference-semantics/semantics/core.k:10` | imports |  | `imports K-EQUAL // ==== values, the algebraic lists, and the scope heap =====================` |
| 328 | `reference-semantics/semantics/core.k:13` | syntax |  | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 329 | `reference-semantics/semantics/core.k:14` | syntax |  | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 330 | `reference-semantics/semantics/core.k:15` | syntax |  | `syntax Str ::= str(IntSeq) // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)` |
| 331 | `reference-semantics/semantics/core.k:18` | syntax |  | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| 332 | `reference-semantics/semantics/core.k:25` | syntax | function | `syntax Val ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) // a heap object: <heap> holds its list(VS) \| cellRef(Int) // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) // a type object (int/str), resolved from the builtins frame \| builtinV(String) // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String) // a cooled Attribute: obj.method` |
| 333 | `reference-semantics/semantics/core.k:36` | syntax |  | `syntax Parent ::= "root" \| parent(Int)` |
| 334 | `reference-semantics/semantics/core.k:37` | syntax |  | `syntax Scope ::= scope(Map, Parent)` |
| 335 | `reference-semantics/semantics/core.k:38` | syntax |  | `syntax KResult ::= Val` |
| 336 | `reference-semantics/semantics/core.k:39` | syntax |  | `syntax Expr ::= Val // cooling puts results back into expression holes` |
| 337 | `reference-semantics/semantics/core.k:40` | syntax |  | `syntax Vals ::= List{Val, ","}` |
| 338 | `reference-semantics/semantics/core.k:41` | syntax |  | `syntax Exc ::= "NoExc" \| "AssertionError"` |
| 339 | `reference-semantics/semantics/core.k:42` | syntax |  | `syntax RetState ::= "noRet" \| retV(Val) // ==== configuration ======================================================= // The builtins namespace is a real scope at reserved location -1 (the bottom of every // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0) // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str` // resolve to their type objects; any local/global binding shadows them via normal lookup.` |
| 340 | `reference-semantics/semantics/core.k:49` | configuration |  | `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code> // ==== heap allocation (constructed lists become objects) ================== // Cons-form emission with a freshness guard (the heap-list-probe discipline: // an update-form H[N <- _] never re-normalizes symbolically). heapLoc is // monotonic — it does NOT wind back at #pop: returned lists escape by ref. // A bare list(VS) Val stays legal (read-only inputs in claims flow unboxed); // only CONSTRUCTORS in program syntax allocate.` |
| 341 | `reference-semantics/semantics/core.k:68` | syntax | function, total | `syntax Bool ::= isRefV(Val) [function, total]` |
| 342 | `reference-semantics/semantics/core.k:69` | rule | ordinary | `rule isRefV(ref(_:Int)) => true` |
| 343 | `reference-semantics/semantics/core.k:70` | rule | ordinary, owise | `rule isRefV(_:Val) => false [owise] // closure cells (Python-faithful capture): the heap holds cellV(V); a // cellRef surfacing as the k-redex reads through (lookup is the only use — // cellRefs never escape to user-visible values)` |
| 344 | `reference-semantics/semantics/core.k:75` | syntax |  | `syntax HeapVal ::= cellV(Val)` |
| 345 | `reference-semantics/semantics/core.k:76` | syntax | function, total | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 346 | `reference-semantics/semantics/core.k:77` | rule | ordinary | `rule isCellRef(cellRef(_:Int)) => true` |
| 347 | `reference-semantics/semantics/core.k:78` | rule | ordinary, owise | `rule isCellRef(_:Val) => false [owise] // k-top deref for cell-bound reads surfacing INSIDE the annotated frame // (AugAssign's in-place read and friends). The "$cells" guard keeps this // DECIDABLY inapplicable in plain frames — an unguarded rule lets the // prover narrow abstract k-top values into cellRef junk (probed on // 26-remove-duplicates). Cross-frame reads (a comprehension closure // reading the enclosing function's cellvar) deref inside #look instead.` |
| 348 | `reference-semantics/semantics/core.k:85` | rule | ordinary, priority | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] // write through a cell (Assign / #bindP / #bindTgt dispatch here on // cell-bound names) // a keyword argument cools to a TAGGED value (consumed by kw-aware builtins)` |
| 349 | `reference-semantics/semantics/core.k:95` | syntax |  | `syntax Val ::= kwV(String, Val)` |
| 350 | `reference-semantics/semantics/core.k:96` | syntax |  | `syntax KItem ::= #kwTag(String)` |
| 351 | `reference-semantics/semantics/core.k:97` | rule | ordinary | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 352 | `reference-semantics/semantics/core.k:98` | rule | ordinary | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| 353 | `reference-semantics/semantics/core.k:100` | syntax | function, total | `syntax Bool ::= isKwV(Val) [function, total]` |
| 354 | `reference-semantics/semantics/core.k:101` | rule | ordinary | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 355 | `reference-semantics/semantics/core.k:102` | rule | ordinary, owise | `rule isKwV(_:Val) => false [owise] // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch // decides by pnMember even over an abstract frame rest (no prover branching)` |
| 356 | `reference-semantics/semantics/core.k:106` | syntax |  | `syntax Val ::= cellsMark(ParamNames)` |
| 357 | `reference-semantics/semantics/core.k:107` | syntax | function | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 358 | `reference-semantics/semantics/core.k:108` | rule | ordinary | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 359 | `reference-semantics/semantics/core.k:109` | syntax | function, total | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 360 | `reference-semantics/semantics/core.k:110` | rule | ordinary | `rule pnMember(_:String, .ParamNames) => false` |
| 361 | `reference-semantics/semantics/core.k:111` | rule | ordinary | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 362 | `reference-semantics/semantics/core.k:113` | syntax |  | `syntax KItem ::= #cellW(Val, Val)` |
| 363 | `reference-semantics/semantics/core.k:114` | rule | ordinary | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| 364 | `reference-semantics/semantics/core.k:117` | syntax |  | `syntax KItem ::= #alloc(Val)` |
| 365 | `reference-semantics/semantics/core.k:118` | rule | ordinary | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) // ==== module load + statement sequencing ==================================` |
| 366 | `reference-semantics/semantics/core.k:124` | syntax |  | `syntax KItem ::= #loadAll(Module)` |
| 367 | `reference-semantics/semantics/core.k:125` | rule | ordinary | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 368 | `reference-semantics/semantics/core.k:126` | rule | ordinary | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 369 | `reference-semantics/semantics/core.k:127` | rule | ordinary | `rule <k> .Stmts => .K ... </k> // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====` |
| 370 | `reference-semantics/semantics/core.k:130` | syntax |  | `syntax KItem ::= #look(String, Int)` |
| 371 | `reference-semantics/semantics/core.k:131` | rule | ordinary | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 372 | `reference-semantics/semantics/core.k:132` | rule | ordinary | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE // LOOKUP (higher priority beats the plain return above on concrete cell // bindings; abstract claim values take the plain rule unchanged) — this // covers cross-frame cell reads (a comprehension closure reading the // enclosing function's cellvar) without a narrowing-prone k-top redex // guarded on the FOUND frame's DECLARED cellvars (pnMember over the // cellsMark): decidable for every concrete frame pin — plain frames and // non-cell names prune outright, so an abstract looked-up value never // drags a narrowing cellV heap match along (probed on 5-intersperse and // Q4's abstract `numbers` in the annotated frame)` |
| 373 | `reference-semantics/semantics/core.k:145` | rule | ordinary, priority | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| 374 | `reference-semantics/semantics/core.k:152` | rule | ordinary | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) // the ONE predefined builtins scope (the -1 frame; claims write `-1 \|-> builtinsScope`)` |
| 375 | `reference-semantics/semantics/core.k:157` | syntax | function, total | `syntax Scope ::= "builtinsScope" [function, total]` |
| 376 | `reference-semantics/semantics/core.k:158` | rule | ordinary | `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root) // ==== argument/element evaluation: ONE left-to-right loop, tagged by destination == // (list/tuple literals and calls all use it; modules extend ApplyK with their tags)` |
| 377 | `reference-semantics/semantics/core.k:185` | syntax |  | `syntax ApplyK ::= toCall(Val)` |
| 378 | `reference-semantics/semantics/core.k:186` | syntax |  | `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| 379 | `reference-semantics/semantics/core.k:189` | rule | ordinary | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 380 | `reference-semantics/semantics/core.k:190` | rule | ordinary | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 381 | `reference-semantics/semantics/core.k:191` | rule | ordinary | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> // ==== Int / Bool / None literals ==========================================` |
| 382 | `reference-semantics/semantics/core.k:194` | rule | ordinary | `rule <k> Int(I:Int) => I ... </k>` |
| 383 | `reference-semantics/semantics/core.k:195` | rule | ordinary | `rule <k> Bool(B:Bool) => B ... </k>` |
| 384 | `reference-semantics/semantics/core.k:196` | rule | ordinary | `rule <k> NoneVal => noneV ... </k> // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================` |
| 385 | `reference-semantics/semantics/core.k:199` | syntax | function | `syntax Bool ::= truthy(Val) [function]` |
| 386 | `reference-semantics/semantics/core.k:200` | rule | ordinary | `rule truthy(B:Bool) => B` |
| 387 | `reference-semantics/semantics/core.k:201` | rule | ordinary | `rule truthy(noneV) => false` |
| 388 | `reference-semantics/semantics/core.k:202` | rule | ordinary | `rule truthy(I:Int) => I =/=Int 0` |
| 389 | `reference-semantics/semantics/core.k:203` | rule | ordinary | `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)` |
| 390 | `reference-semantics/semantics/core.k:204` | rule | ordinary | `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 391 | `reference-semantics/semantics/core.k:205` | rule | ordinary | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) // ==== extensible operator dispatch (cases added by the construct modules) ==` |
| 392 | `reference-semantics/semantics/core.k:208` | syntax | function | `syntax Val ::= applyUn(String, Val) [function]` |
| 393 | `reference-semantics/semantics/core.k:209` | syntax | function | `syntax Val ::= applyBin(String, Val, Val) [function]` |
| 394 | `reference-semantics/semantics/core.k:210` | syntax | function | `syntax Bool ::= applyCmp(String, Val, Val) [function] // ==== shared list helpers =================================================` |
| 395 | `reference-semantics/semantics/core.k:213` | syntax | function, total | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 396 | `reference-semantics/semantics/core.k:214` | rule | ordinary | `rule appendVal(.Vals, V:Val) => V , .Vals` |
| 397 | `reference-semantics/semantics/core.k:215` | rule | ordinary | `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)` |
| 398 | `reference-semantics/semantics/core.k:217` | syntax | function, total | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 399 | `reference-semantics/semantics/core.k:218` | rule | ordinary | `rule vals2valSeq(.Vals) => .ValSeq` |
| 400 | `reference-semantics/semantics/core.k:219` | rule | ordinary | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) // ==== shared sequence length (len / summaries across many modules) ======== // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)` |
| 401 | `reference-semantics/semantics/core.k:223` | syntax | function, total | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 402 | `reference-semantics/semantics/core.k:224` | rule | ordinary | `rule vsLen(.ValSeq) => 0` |
| 403 | `reference-semantics/semantics/core.k:225` | rule | ordinary | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 404 | `reference-semantics/semantics/core.k:227` | syntax | function, total | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 405 | `reference-semantics/semantics/core.k:228` | rule | ordinary | `rule isLen(.IntSeq) => 0` |
| 406 | `reference-semantics/semantics/core.k:229` | rule | ordinary | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)` |
| 407 | `reference-semantics/semantics/core.k:233` | syntax | function, total | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 408 | `reference-semantics/semantics/core.k:234` | rule | ordinary | `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq` |
| 409 | `reference-semantics/semantics/core.k:235` | rule | ordinary | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)` |
| 410 | `reference-semantics/semantics/core.k:236` | rule | ordinary | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| 411 | `reference-semantics/semantics/core.k:238` | rule | ordinary | `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0` |
| 412 | `reference-semantics/semantics/core.k:240` | endmodule |  | `endmodule` |
| 413 | `reference-semantics/semantics/dict.k:13` | module |  | `module MPY-DICT` |
| 414 | `reference-semantics/semantics/dict.k:14` | imports |  | `imports MPY-CORE` |
| 415 | `reference-semantics/semantics/dict.k:15` | imports |  | `imports MPY-ITER` |
| 416 | `reference-semantics/semantics/dict.k:16` | imports |  | `imports MPY-METHODS` |
| 417 | `reference-semantics/semantics/dict.k:17` | imports |  | `imports MPY-LIST // dict as PARALLEL ordered key/value ValSeqs (same length; keys distinct).` |
| 418 | `reference-semantics/semantics/dict.k:20` | syntax |  | `syntax Val ::= dictV(ValSeq, ValSeq) // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.` |
| 419 | `reference-semantics/semantics/dict.k:23` | syntax |  | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| 420 | `reference-semantics/semantics/dict.k:26` | rule | ordinary | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 421 | `reference-semantics/semantics/dict.k:27` | rule | ordinary | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 422 | `reference-semantics/semantics/dict.k:28` | rule | ordinary | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| 423 | `reference-semantics/semantics/dict.k:30` | rule | ordinary | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| 424 | `reference-semantics/semantics/dict.k:32` | rule | ordinary | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.` |
| 425 | `reference-semantics/semantics/dict.k:37` | syntax | function, total | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 426 | `reference-semantics/semantics/dict.k:38` | rule | ordinary | `rule dHasKey(.ValSeq, _:Val) => false` |
| 427 | `reference-semantics/semantics/dict.k:39` | rule | ordinary | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K` |
| 428 | `reference-semantics/semantics/dict.k:40` | rule | ordinary | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) // dPutK: KS unchanged if K already present, else append K (keep-first-position).` |
| 429 | `reference-semantics/semantics/dict.k:43` | syntax | function, total | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 430 | `reference-semantics/semantics/dict.k:44` | rule | ordinary | `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)` |
| 431 | `reference-semantics/semantics/dict.k:45` | rule | ordinary, owise | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).` |
| 432 | `reference-semantics/semantics/dict.k:49` | syntax | function, total | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 433 | `reference-semantics/semantics/dict.k:50` | rule | ordinary | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K` |
| 434 | `reference-semantics/semantics/dict.k:52` | rule | ordinary | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| 435 | `reference-semantics/semantics/dict.k:54` | rule | ordinary, owise | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] // ==== dict methods ======================================================== // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).` |
| 436 | `reference-semantics/semantics/dict.k:58` | rule | ordinary, priority | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==` |
| 437 | `reference-semantics/semantics/dict.k:63` | rule | ordinary | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 438 | `reference-semantics/semantics/dict.k:64` | syntax | function | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 439 | `reference-semantics/semantics/dict.k:65` | rule | ordinary, priority | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] // ==== dict subscript-assign: d[k] = v (insert/update in place) ============= // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.` |
| 440 | `reference-semantics/semantics/dict.k:70` | syntax | function | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 441 | `reference-semantics/semantics/dict.k:71` | rule | ordinary | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope // value: a bare dict updates in the scope (dicts stay values); a ref (a heap // list — or a heap dict later) writes the heap in place.` |
| 442 | `reference-semantics/semantics/dict.k:76` | syntax |  | `syntax KItem ::= #dsetK(String, Val)` |
| 443 | `reference-semantics/semantics/dict.k:77` | rule | ordinary | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 444 | `reference-semantics/semantics/dict.k:78` | rule | ordinary | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| 445 | `reference-semantics/semantics/dict.k:82` | rule | ordinary | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| 446 | `reference-semantics/semantics/dict.k:86` | syntax |  | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 447 | `reference-semantics/semantics/dict.k:87` | rule | ordinary | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> // negative-index normalization local to the write (subscript.k's is not imported here)` |
| 448 | `reference-semantics/semantics/dict.k:90` | syntax | function, total | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 449 | `reference-semantics/semantics/dict.k:91` | rule | ordinary | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 450 | `reference-semantics/semantics/dict.k:92` | rule | ordinary | `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0 // ==== dict == (order-insensitive: same size + same key->value pairs) =======` |
| 451 | `reference-semantics/semantics/dict.k:95` | rule | ordinary | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| 452 | `reference-semantics/semantics/dict.k:97` | syntax | function | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 453 | `reference-semantics/semantics/dict.k:98` | rule | ordinary | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 454 | `reference-semantics/semantics/dict.k:99` | rule | ordinary | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| 455 | `reference-semantics/semantics/dict.k:101` | syntax | function | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 456 | `reference-semantics/semantics/dict.k:102` | rule | ordinary | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K` |
| 457 | `reference-semantics/semantics/dict.k:103` | rule | ordinary | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| 458 | `reference-semantics/semantics/dict.k:104` | endmodule |  | `endmodule` |
| 459 | `reference-semantics/semantics/float.k:14` | module |  | `module MPY-FLOAT` |
| 460 | `reference-semantics/semantics/float.k:15` | imports |  | `imports MPY-OPERATORS` |
| 461 | `reference-semantics/semantics/float.k:16` | imports |  | `imports MPY-BUILTINS` |
| 462 | `reference-semantics/semantics/float.k:17` | imports |  | `imports FLOAT // Float is a value; the float literal evaluates to the K Float.` |
| 463 | `reference-semantics/semantics/float.k:20` | syntax |  | `syntax Val ::= Float` |
| 464 | `reference-semantics/semantics/float.k:21` | rule | ordinary | `rule <k> Float(F:Float) => F ... </k> // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.` |
| 465 | `reference-semantics/semantics/float.k:24` | syntax | function, total, symbol | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 466 | `reference-semantics/semantics/float.k:25` | rule | ordinary | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 467 | `reference-semantics/semantics/float.k:27` | rule | ordinary | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.` |
| 468 | `reference-semantics/semantics/float.k:30` | syntax | function, total, symbol | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 469 | `reference-semantics/semantics/float.k:31` | rule | ordinary | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 470 | `reference-semantics/semantics/float.k:32` | rule | ordinary | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).` |
| 471 | `reference-semantics/semantics/float.k:37` | syntax | function, total, symbol | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 472 | `reference-semantics/semantics/float.k:38` | rule | ordinary | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 473 | `reference-semantics/semantics/float.k:39` | rule | ordinary | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on // concrete floats. kprove proofs return floats structurally and do not compare them.` |
| 474 | `reference-semantics/semantics/float.k:43` | rule | ordinary | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 475 | `reference-semantics/semantics/float.k:44` | rule | ordinary | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade), // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise // `abs(a-b) < t` proximity test.)` |
| 476 | `reference-semantics/semantics/float.k:50` | syntax | function, total, symbol | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 477 | `reference-semantics/semantics/float.k:51` | rule | ordinary | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 478 | `reference-semantics/semantics/float.k:52` | rule | ordinary | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 479 | `reference-semantics/semantics/float.k:54` | syntax | function, total, symbol | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 480 | `reference-semantics/semantics/float.k:55` | rule | ordinary | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 481 | `reference-semantics/semantics/float.k:56` | rule | ordinary | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F) // ==== math.ceil =========================================================== // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is // never bound as a value).` |
| 482 | `reference-semantics/semantics/float.k:61` | rule | ordinary | `rule <k> Import(_:String) => .K ... </k> // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher // priority than the generic Attribute/method dispatch in call.k).` |
| 483 | `reference-semantics/semantics/float.k:65` | syntax |  | `syntax KItem ::= "#mathCeil"` |
| 484 | `reference-semantics/semantics/float.k:66` | rule | ordinary, priority | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 485 | `reference-semantics/semantics/float.k:67` | rule | ordinary | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> // math.floor(x) — same interception shape as math.ceil` |
| 486 | `reference-semantics/semantics/float.k:70` | syntax |  | `syntax KItem ::= "#mathFloor"` |
| 487 | `reference-semantics/semantics/float.k:71` | rule | ordinary, priority | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 488 | `reference-semantics/semantics/float.k:72` | rule | ordinary | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 489 | `reference-semantics/semantics/float.k:73` | syntax | function, total, symbol | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 490 | `reference-semantics/semantics/float.k:74` | rule | ordinary | `rule floorFI(I:Int) => I [concrete]` |
| 491 | `reference-semantics/semantics/float.k:75` | rule | ordinary | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] // bare floor/ceil (bound by `from math import floor, ceil`)` |
| 492 | `reference-semantics/semantics/float.k:78` | rule | ordinary | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 493 | `reference-semantics/semantics/float.k:79` | rule | ordinary | `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V) // math.pow(x, y) — a two-arg interception onto powF (ints promote)` |
| 494 | `reference-semantics/semantics/float.k:82` | syntax |  | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 495 | `reference-semantics/semantics/float.k:83` | rule | ordinary, priority | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 496 | `reference-semantics/semantics/float.k:84` | rule | ordinary | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 497 | `reference-semantics/semantics/float.k:85` | rule | ordinary | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 498 | `reference-semantics/semantics/float.k:86` | syntax | function, total, symbol | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 499 | `reference-semantics/semantics/float.k:87` | rule | ordinary | `rule toF(F:Float) => F [concrete]` |
| 500 | `reference-semantics/semantics/float.k:88` | rule | ordinary | `rule toF(I:Int) => intToF(I) [concrete] // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm). // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).` |
| 501 | `reference-semantics/semantics/float.k:93` | syntax | function, total, symbol | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 502 | `reference-semantics/semantics/float.k:94` | rule | ordinary | `rule ceilF(I:Int) => I [concrete]` |
| 503 | `reference-semantics/semantics/float.k:95` | rule | ordinary | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun; // proofs use symbolic elements, never a float literal.` |
| 504 | `reference-semantics/semantics/float.k:99` | rule | ordinary | `rule applyUn("-", F:Float) => 0.0 -Float F // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.` |
| 505 | `reference-semantics/semantics/float.k:103` | syntax | function, total, symbol | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 506 | `reference-semantics/semantics/float.k:104` | rule | ordinary | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 507 | `reference-semantics/semantics/float.k:105` | rule | ordinary | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 508 | `reference-semantics/semantics/float.k:107` | syntax | function, total, symbol | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 509 | `reference-semantics/semantics/float.k:108` | rule | ordinary | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 510 | `reference-semantics/semantics/float.k:109` | rule | ordinary | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 511 | `reference-semantics/semantics/float.k:111` | syntax | function, total, symbol | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 512 | `reference-semantics/semantics/float.k:112` | rule | ordinary | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 513 | `reference-semantics/semantics/float.k:113` | rule | ordinary | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 514 | `reference-semantics/semantics/float.k:115` | syntax | function, total, symbol | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 515 | `reference-semantics/semantics/float.k:116` | rule | ordinary | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 516 | `reference-semantics/semantics/float.k:117` | rule | ordinary | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 517 | `reference-semantics/semantics/float.k:119` | syntax | function, total, symbol | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 518 | `reference-semantics/semantics/float.k:120` | rule | ordinary | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 519 | `reference-semantics/semantics/float.k:121` | rule | ordinary | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) // ---- the remaining comparisons (gtF promoted from find_zero — its summaries // case-split on the atom; >= / <= derive from the two opaque compares) ----` |
| 520 | `reference-semantics/semantics/float.k:125` | syntax | function, total, symbol | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 521 | `reference-semantics/semantics/float.k:126` | rule | ordinary | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 522 | `reference-semantics/semantics/float.k:127` | rule | ordinary | `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)` |
| 523 | `reference-semantics/semantics/float.k:128` | rule | ordinary | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 524 | `reference-semantics/semantics/float.k:129` | rule | ordinary | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----` |
| 525 | `reference-semantics/semantics/float.k:132` | rule | ordinary | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 526 | `reference-semantics/semantics/float.k:133` | rule | ordinary | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 527 | `reference-semantics/semantics/float.k:134` | rule | ordinary | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 528 | `reference-semantics/semantics/float.k:135` | rule | ordinary | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 529 | `reference-semantics/semantics/float.k:136` | rule | ordinary | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 530 | `reference-semantics/semantics/float.k:137` | rule | ordinary | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 531 | `reference-semantics/semantics/float.k:138` | rule | ordinary | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 532 | `reference-semantics/semantics/float.k:139` | rule | ordinary | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----` |
| 533 | `reference-semantics/semantics/float.k:142` | syntax | function, total, symbol | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 534 | `reference-semantics/semantics/float.k:143` | rule | ordinary | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 535 | `reference-semantics/semantics/float.k:144` | rule | ordinary | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 536 | `reference-semantics/semantics/float.k:145` | rule | ordinary | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 537 | `reference-semantics/semantics/float.k:146` | rule | ordinary | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 538 | `reference-semantics/semantics/float.k:147` | rule | ordinary | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 539 | `reference-semantics/semantics/float.k:148` | rule | ordinary | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 540 | `reference-semantics/semantics/float.k:149` | rule | ordinary | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 541 | `reference-semantics/semantics/float.k:150` | rule | ordinary | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 542 | `reference-semantics/semantics/float.k:151` | rule | ordinary | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- x == None (promoted from 137; `is` cases live in operators.k) ----` |
| 543 | `reference-semantics/semantics/float.k:154` | rule | ordinary | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 544 | `reference-semantics/semantics/float.k:155` | rule | ordinary | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) // ---- float(str): decimal parse (promoted from 137's defined chain) ---- // digits '.' digits, optional leading '-'; concrete evaluation only (the // symbolic side stays an opaque decStrToF term a proof case-splits on).` |
| 545 | `reference-semantics/semantics/float.k:160` | syntax | function, total, symbol | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 546 | `reference-semantics/semantics/float.k:161` | rule | ordinary | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 547 | `reference-semantics/semantics/float.k:162` | rule | ordinary | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| 548 | `reference-semantics/semantics/float.k:165` | syntax | function | `syntax Int ::= headIS(IntSeq) [function]` |
| 549 | `reference-semantics/semantics/float.k:166` | rule | ordinary | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 550 | `reference-semantics/semantics/float.k:167` | syntax | function, total | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 551 | `reference-semantics/semantics/float.k:168` | rule | ordinary | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 552 | `reference-semantics/semantics/float.k:169` | rule | ordinary | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 553 | `reference-semantics/semantics/float.k:170` | rule | ordinary | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 554 | `reference-semantics/semantics/float.k:171` | rule | ordinary | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| 555 | `reference-semantics/semantics/float.k:173` | syntax | function, total | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 556 | `reference-semantics/semantics/float.k:174` | rule | ordinary | `rule fracPart(.IntSeq) => 0` |
| 557 | `reference-semantics/semantics/float.k:175` | rule | ordinary | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 558 | `reference-semantics/semantics/float.k:176` | rule | ordinary | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 559 | `reference-semantics/semantics/float.k:177` | rule | ordinary | `rule fracAcc(.IntSeq, A:Int) => A` |
| 560 | `reference-semantics/semantics/float.k:178` | rule | ordinary | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 561 | `reference-semantics/semantics/float.k:179` | syntax | function, total | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 562 | `reference-semantics/semantics/float.k:180` | rule | ordinary | `rule fracScale(.IntSeq) => 1` |
| 563 | `reference-semantics/semantics/float.k:181` | rule | ordinary | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 564 | `reference-semantics/semantics/float.k:182` | rule | ordinary | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 565 | `reference-semantics/semantics/float.k:183` | rule | ordinary | `rule fscAcc(.IntSeq, A:Int) => A` |
| 566 | `reference-semantics/semantics/float.k:184` | rule | ordinary | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 567 | `reference-semantics/semantics/float.k:185` | rule | ordinary | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 568 | `reference-semantics/semantics/float.k:186` | rule | ordinary | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 569 | `reference-semantics/semantics/float.k:187` | rule | ordinary | `rule applyBuiltin("float", F:Float, .Vals) => F // ---- float / int division (promoted from mean_absolute_deviation) ----` |
| 570 | `reference-semantics/semantics/float.k:190` | syntax | function, total, symbol | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 571 | `reference-semantics/semantics/float.k:191` | rule | ordinary | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 572 | `reference-semantics/semantics/float.k:192` | rule | ordinary | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) // ---- int -> float promotion for the remaining mixed arithmetic/compares ----` |
| 573 | `reference-semantics/semantics/float.k:195` | syntax | function, total, symbol | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 574 | `reference-semantics/semantics/float.k:196` | rule | ordinary | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 575 | `reference-semantics/semantics/float.k:197` | rule | ordinary | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 576 | `reference-semantics/semantics/float.k:198` | rule | ordinary | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 577 | `reference-semantics/semantics/float.k:199` | rule | ordinary | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 578 | `reference-semantics/semantics/float.k:200` | rule | ordinary | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 579 | `reference-semantics/semantics/float.k:201` | rule | ordinary | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 580 | `reference-semantics/semantics/float.k:202` | rule | ordinary | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 581 | `reference-semantics/semantics/float.k:203` | rule | ordinary | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 582 | `reference-semantics/semantics/float.k:204` | rule | ordinary | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 583 | `reference-semantics/semantics/float.k:205` | rule | ordinary | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 584 | `reference-semantics/semantics/float.k:206` | rule | ordinary | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----` |
| 585 | `reference-semantics/semantics/float.k:209` | syntax | function, total, symbol | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 586 | `reference-semantics/semantics/float.k:210` | rule | ordinary | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 587 | `reference-semantics/semantics/float.k:211` | rule | ordinary | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 588 | `reference-semantics/semantics/float.k:213` | rule | ordinary | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 589 | `reference-semantics/semantics/float.k:214` | rule | ordinary | `rule applyBuiltin("float", F:Float, .Vals) => F // round: Python half-even (banker's); round(F, N) scales by 10^N` |
| 590 | `reference-semantics/semantics/float.k:217` | syntax | function, total, symbol | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 591 | `reference-semantics/semantics/float.k:218` | rule | ordinary | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| 592 | `reference-semantics/semantics/float.k:223` | syntax | function, total, symbol | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 593 | `reference-semantics/semantics/float.k:224` | rule | ordinary | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| 594 | `reference-semantics/semantics/float.k:227` | rule | ordinary | `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)` |
| 595 | `reference-semantics/semantics/float.k:228` | rule | ordinary | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 596 | `reference-semantics/semantics/float.k:230` | syntax | function, total, symbol | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 597 | `reference-semantics/semantics/float.k:231` | rule | ordinary | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 598 | `reference-semantics/semantics/float.k:232` | syntax |  | `syntax KItem ::= "#mathSqrt"` |
| 599 | `reference-semantics/semantics/float.k:233` | rule | ordinary, priority | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 600 | `reference-semantics/semantics/float.k:234` | rule | ordinary | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 601 | `reference-semantics/semantics/float.k:235` | rule | ordinary | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive: // the isFloat guard is disjoint from the existing isInt one.` |
| 602 | `reference-semantics/semantics/float.k:243` | syntax |  | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 603 | `reference-semantics/semantics/float.k:244` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 604 | `reference-semantics/semantics/float.k:245` | rule | ordinary | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 605 | `reference-semantics/semantics/float.k:246` | rule | ordinary | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 606 | `reference-semantics/semantics/float.k:247` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 607 | `reference-semantics/semantics/float.k:250` | syntax |  | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 608 | `reference-semantics/semantics/float.k:251` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 609 | `reference-semantics/semantics/float.k:252` | rule | ordinary | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 610 | `reference-semantics/semantics/float.k:253` | rule | ordinary | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 611 | `reference-semantics/semantics/float.k:254` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin). // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof // with isInt(V) in its path condition refutes this branch without sort reasoning.` |
| 612 | `reference-semantics/semantics/float.k:261` | syntax |  | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 613 | `reference-semantics/semantics/float.k:262` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| 614 | `reference-semantics/semantics/float.k:265` | rule | ordinary | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 615 | `reference-semantics/semantics/float.k:266` | rule | ordinary | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 616 | `reference-semantics/semantics/float.k:267` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| 617 | `reference-semantics/semantics/float.k:270` | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| 618 | `reference-semantics/semantics/float.k:273` | endmodule |  | `endmodule` |
| 619 | `reference-semantics/semantics/functions.k:3` | module |  | `module MPY-FUNCTIONS` |
| 620 | `reference-semantics/semantics/functions.k:4` | imports |  | `imports MPY-CORE // call routing + callee/arg evaluation (#callee/#args/#argCont) live in call.k; // this module owns the frame lifecycle (bind params, return, pop).` |
| 621 | `reference-semantics/semantics/functions.k:8` | syntax |  | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall" // ==== def / anonymous closure =============================================` |
| 622 | `reference-semantics/semantics/functions.k:14` | rule | ordinary | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| 623 | `reference-semantics/semantics/functions.k:18` | syntax |  | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 624 | `reference-semantics/semantics/functions.k:19` | rule | ordinary | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> // ==== annotated def/lambda (closure cells; spec 2.3) ====================== // closureValC(params, cellvars, body, captured-cells). No frame anchor: all // enclosing-local reads are freevars (symtable-complete) and go through the // captured cells; everything else is global/builtin, so the callee frame's // parent is the module scope (0) — sound after the defining frame dies.` |
| 625 | `reference-semantics/semantics/functions.k:27` | syntax |  | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) // capture: resolve each freevar to the enclosing frame's cellRef, then bind // (FuncDef) or yield (Lambda) the closure value.` |
| 626 | `reference-semantics/semantics/functions.k:31` | syntax |  | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 627 | `reference-semantics/semantics/functions.k:33` | rule | ordinary | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| 628 | `reference-semantics/semantics/functions.k:36` | rule | ordinary | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 629 | `reference-semantics/semantics/functions.k:42` | rule | ordinary | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| 630 | `reference-semantics/semantics/functions.k:47` | rule | ordinary | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| 631 | `reference-semantics/semantics/functions.k:50` | rule | ordinary | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| 632 | `reference-semantics/semantics/functions.k:53` | rule | ordinary | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 633 | `reference-semantics/semantics/functions.k:59` | rule | ordinary | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> // ==== bind params ========================================================` |
| 634 | `reference-semantics/semantics/functions.k:63` | rule | ordinary | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 635 | `reference-semantics/semantics/functions.k:64` | rule | ordinary | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes> // a param that is a cellvar was pre-bound to its cell at frame entry` |
| 636 | `reference-semantics/semantics/functions.k:68` | rule | ordinary, priority | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] // ==== return / pop the frame (the returned expr evaluates by strictness) ==` |
| 637 | `reference-semantics/semantics/functions.k:78` | rule | ordinary | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| 638 | `reference-semantics/semantics/functions.k:80` | rule | ordinary | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).` |
| 639 | `reference-semantics/semantics/functions.k:85` | rule | ordinary | `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |
| 640 | `reference-semantics/semantics/functions.k:91` | endmodule |  | `endmodule` |
| 641 | `reference-semantics/semantics/int.k:4` | module |  | `module MPY-INT` |
| 642 | `reference-semantics/semantics/int.k:5` | imports |  | `imports MPY-CORE` |
| 643 | `reference-semantics/semantics/int.k:7` | rule | ordinary | `rule applyUn("-", I:Int) => 0 -Int I` |
| 644 | `reference-semantics/semantics/int.k:9` | rule | ordinary | `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2 // Bool participates in int arithmetic (x += (a == b))` |
| 645 | `reference-semantics/semantics/int.k:11` | rule | ordinary | `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 646 | `reference-semantics/semantics/int.k:12` | rule | ordinary | `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 647 | `reference-semantics/semantics/int.k:13` | rule | ordinary | `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2` |
| 648 | `reference-semantics/semantics/int.k:14` | rule | ordinary | `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2` |
| 649 | `reference-semantics/semantics/int.k:15` | rule | ordinary | `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)` |
| 650 | `reference-semantics/semantics/int.k:16` | rule | ordinary | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 651 | `reference-semantics/semantics/int.k:17` | rule | ordinary | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 652 | `reference-semantics/semantics/int.k:19` | syntax | function | `syntax Int ::= pyMod(Int, Int) [function]` |
| 653 | `reference-semantics/semantics/int.k:20` | rule | ordinary | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 654 | `reference-semantics/semantics/int.k:22` | rule | ordinary | `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` |
| 655 | `reference-semantics/semantics/int.k:23` | rule | ordinary | `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2` |
| 656 | `reference-semantics/semantics/int.k:24` | rule | ordinary | `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` |
| 657 | `reference-semantics/semantics/int.k:25` | rule | ordinary | `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2` |
| 658 | `reference-semantics/semantics/int.k:26` | rule | ordinary | `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2` |
| 659 | `reference-semantics/semantics/int.k:27` | rule | ordinary | `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2` |
| 660 | `reference-semantics/semantics/int.k:28` | endmodule |  | `endmodule` |
| 661 | `reference-semantics/semantics/iter.k:6` | module |  | `module MPY-ITER` |
| 662 | `reference-semantics/semantics/iter.k:7` | imports |  | `imports MPY-CORE` |
| 663 | `reference-semantics/semantics/iter.k:8` | syntax |  | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| 664 | `reference-semantics/semantics/iter.k:9` | endmodule |  | `endmodule` |
| 665 | `reference-semantics/semantics/list.k:3` | module |  | `module MPY-LIST` |
| 666 | `reference-semantics/semantics/list.k:4` | imports |  | `imports MPY-CORE` |
| 667 | `reference-semantics/semantics/list.k:5` | imports |  | `imports MPY-ITER` |
| 668 | `reference-semantics/semantics/list.k:6` | imports |  | `imports MPY-OPERATORS // ==== iteration (the iterator protocol's list case) =======================` |
| 669 | `reference-semantics/semantics/list.k:9` | rule | ordinary | `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>` |
| 670 | `reference-semantics/semantics/list.k:10` | rule | ordinary | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> // ==== ListExpr: [...] literal -> a fresh heap object =======================` |
| 671 | `reference-semantics/semantics/list.k:13` | syntax |  | `syntax ApplyK ::= "toList"` |
| 672 | `reference-semantics/semantics/list.k:14` | rule | ordinary | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 673 | `reference-semantics/semantics/list.k:15` | rule | ordinary | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> // ==== list ops: + / == / != ===============================================` |
| 674 | `reference-semantics/semantics/list.k:18` | syntax | function, total | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 675 | `reference-semantics/semantics/list.k:19` | rule | ordinary | `rule valSeqConcat(.ValSeq, T:ValSeq) => T` |
| 676 | `reference-semantics/semantics/list.k:20` | rule | ordinary, priority | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) // list + list constructs a NEW object (k-cell — it allocates; operands land here // already deref'd). priority(45) beats the generic BinOp dispatch.` |
| 677 | `reference-semantics/semantics/list.k:24` | rule | ordinary, priority | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| 678 | `reference-semantics/semantics/list.k:27` | rule | ordinary | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 679 | `reference-semantics/semantics/list.k:28` | rule | ordinary | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) // ==== deep equality when elements are heap objects (list-of-lists) ======== // Python == is structural at every depth. Fires ONLY when a ref is present // (the guard decides on concrete seqs); the plain ==K path above is unchanged.` |
| 680 | `reference-semantics/semantics/list.k:33` | syntax | function, total | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 681 | `reference-semantics/semantics/list.k:34` | rule | ordinary | `rule hasRefVS(.ValSeq) => false` |
| 682 | `reference-semantics/semantics/list.k:35` | rule | ordinary | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 683 | `reference-semantics/semantics/list.k:37` | syntax | function | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map) [function]` |
| 684 | `reference-semantics/semantics/list.k:39` | rule | ordinary | `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true` |
| 685 | `reference-semantics/semantics/list.k:40` | rule | ordinary | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false` |
| 686 | `reference-semantics/semantics/list.k:41` | rule | ordinary | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false` |
| 687 | `reference-semantics/semantics/list.k:42` | rule | ordinary | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| 688 | `reference-semantics/semantics/list.k:45` | rule | ordinary | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| 689 | `reference-semantics/semantics/list.k:47` | rule | ordinary | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| 690 | `reference-semantics/semantics/list.k:49` | rule | ordinary | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 691 | `reference-semantics/semantics/list.k:50` | rule | ordinary, owise | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] // ==== mutator: xs.append(v) — an in-place heap write ======================` |
| 692 | `reference-semantics/semantics/list.k:53` | rule | ordinary, priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] // ==== `x in list` — a <k>-cell fold over #iterNext ========================` |
| 693 | `reference-semantics/semantics/list.k:58` | syntax |  | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 694 | `reference-semantics/semantics/list.k:59` | rule | ordinary | `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 695 | `reference-semantics/semantics/list.k:60` | rule | ordinary | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 696 | `reference-semantics/semantics/list.k:61` | rule | ordinary | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 697 | `reference-semantics/semantics/list.k:62` | rule | ordinary | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 698 | `reference-semantics/semantics/list.k:63` | rule | ordinary | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| 699 | `reference-semantics/semantics/list.k:65` | rule | ordinary | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| 700 | `reference-semantics/semantics/list.k:67` | rule | ordinary | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| 701 | `reference-semantics/semantics/list.k:68` | endmodule |  | `endmodule` |
| 702 | `reference-semantics/semantics/methods.k:3` | module |  | `module MPY-METHODS` |
| 703 | `reference-semantics/semantics/methods.k:4` | imports |  | `imports MPY-CORE` |
| 704 | `reference-semantics/semantics/methods.k:5` | imports |  | `imports K-EQUAL` |
| 705 | `reference-semantics/semantics/methods.k:6` | imports |  | `imports MPY-STR` |
| 706 | `reference-semantics/semantics/methods.k:7` | imports |  | `imports MPY-LIST // method-call routing + arg-eval live in call.k; this module owns applyMethod.` |
| 707 | `reference-semantics/semantics/methods.k:10` | syntax | function | `syntax Val ::= applyMethod(Val, String, Vals) [function] // ==== string predicates (Python semantics) =================================` |
| 708 | `reference-semantics/semantics/methods.k:13` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 709 | `reference-semantics/semantics/methods.k:14` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 710 | `reference-semantics/semantics/methods.k:15` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 711 | `reference-semantics/semantics/methods.k:16` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) // ==== case maps ============================================================` |
| 712 | `reference-semantics/semantics/methods.k:19` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))` |
| 713 | `reference-semantics/semantics/methods.k:20` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))` |
| 714 | `reference-semantics/semantics/methods.k:21` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) // ==== join / count / strip / encode ======================================== // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by // the call layer; the result str is a value)` |
| 715 | `reference-semantics/semantics/methods.k:26` | rule | ordinary | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 716 | `reference-semantics/semantics/methods.k:27` | syntax | function, total | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 717 | `reference-semantics/semantics/methods.k:28` | rule | ordinary | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 718 | `reference-semantics/semantics/methods.k:29` | rule | ordinary | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 719 | `reference-semantics/semantics/methods.k:30` | rule | ordinary | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) // S.count(sub): non-overlapping window scan (Python str.count)` |
| 720 | `reference-semantics/semantics/methods.k:34` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 721 | `reference-semantics/semantics/methods.k:35` | syntax | function | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 722 | `reference-semantics/semantics/methods.k:36` | rule | ordinary | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 723 | `reference-semantics/semantics/methods.k:37` | rule | ordinary | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| 724 | `reference-semantics/semantics/methods.k:39` | rule | ordinary | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| 725 | `reference-semantics/semantics/methods.k:41` | syntax | function, total | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 726 | `reference-semantics/semantics/methods.k:42` | rule | ordinary | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 727 | `reference-semantics/semantics/methods.k:43` | rule | ordinary, owise | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 728 | `reference-semantics/semantics/methods.k:44` | rule | ordinary | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 // S.strip(): trim whitespace runs from both ends` |
| 729 | `reference-semantics/semantics/methods.k:47` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 730 | `reference-semantics/semantics/methods.k:48` | syntax | function, total | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 731 | `reference-semantics/semantics/methods.k:49` | rule | ordinary | `rule trimWS(.IntSeq) => .IntSeq` |
| 732 | `reference-semantics/semantics/methods.k:50` | rule | ordinary | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 733 | `reference-semantics/semantics/methods.k:51` | rule | ordinary | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 734 | `reference-semantics/semantics/methods.k:52` | syntax | function, total | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 735 | `reference-semantics/semantics/methods.k:53` | rule | ordinary | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 736 | `reference-semantics/semantics/methods.k:54` | rule | ordinary | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 737 | `reference-semantics/semantics/methods.k:55` | rule | ordinary | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) // S.encode('ascii'): identity on the code-sequence model (bytes == codes)` |
| 738 | `reference-semantics/semantics/methods.k:58` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) // ==== prefix ===============================================================` |
| 739 | `reference-semantics/semantics/methods.k:61` | rule | ordinary | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========` |
| 740 | `reference-semantics/semantics/methods.k:64` | rule | ordinary | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 741 | `reference-semantics/semantics/methods.k:65` | syntax | function, total | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 742 | `reference-semantics/semantics/methods.k:66` | rule | ordinary | `rule cntOccVS(.ValSeq, _:Val) => 0` |
| 743 | `reference-semantics/semantics/methods.k:67` | rule | ordinary | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 744 | `reference-semantics/semantics/methods.k:68` | rule | ordinary | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V) // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ========== // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.` |
| 745 | `reference-semantics/semantics/methods.k:72` | rule | ordinary, priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| 746 | `reference-semantics/semantics/methods.k:75` | syntax | function, token | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result` |
| 747 | `reference-semantics/semantics/methods.k:76` | rule | ordinary | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 748 | `reference-semantics/semantics/methods.k:77` | rule | ordinary | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| 749 | `reference-semantics/semantics/methods.k:79` | rule | ordinary | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) // flush the current token to the result list iff non-empty.` |
| 750 | `reference-semantics/semantics/methods.k:82` | syntax | function | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 751 | `reference-semantics/semantics/methods.k:83` | rule | ordinary | `rule flushTok(ACC:ValSeq, .IntSeq) => ACC` |
| 752 | `reference-semantics/semantics/methods.k:84` | rule | ordinary | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 753 | `reference-semantics/semantics/methods.k:85` | syntax | function, total | `syntax Bool ::= isWSC(Int) [function, total]` |
| 754 | `reference-semantics/semantics/methods.k:86` | rule | ordinary | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 // split(sep='x') keyword form delegates to the positional k-cell rule` |
| 755 | `reference-semantics/semantics/methods.k:89` | rule | ordinary, priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).` |
| 756 | `reference-semantics/semantics/methods.k:94` | rule | ordinary, priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| 757 | `reference-semantics/semantics/methods.k:97` | syntax | function, token | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token` |
| 758 | `reference-semantics/semantics/methods.k:98` | rule | ordinary | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)` |
| 759 | `reference-semantics/semantics/methods.k:99` | rule | ordinary | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| 760 | `reference-semantics/semantics/methods.k:101` | rule | ordinary | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| 761 | `reference-semantics/semantics/methods.k:104` | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| 762 | `reference-semantics/semantics/methods.k:106` | syntax | function, total | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 763 | `reference-semantics/semantics/methods.k:107` | rule | ordinary | `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq` |
| 764 | `reference-semantics/semantics/methods.k:108` | rule | ordinary | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 765 | `reference-semantics/semantics/methods.k:109` | rule | ordinary | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) // ==== char helpers =========================================================` |
| 766 | `reference-semantics/semantics/methods.k:112` | syntax | function, total | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 767 | `reference-semantics/semantics/methods.k:113` | rule | ordinary | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 768 | `reference-semantics/semantics/methods.k:115` | syntax | function, total | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 769 | `reference-semantics/semantics/methods.k:116` | rule | ordinary | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 770 | `reference-semantics/semantics/methods.k:118` | syntax | function, total | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 771 | `reference-semantics/semantics/methods.k:119` | rule | ordinary | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 772 | `reference-semantics/semantics/methods.k:121` | syntax | function, total | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 773 | `reference-semantics/semantics/methods.k:122` | rule | ordinary | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 774 | `reference-semantics/semantics/methods.k:124` | syntax | function, total | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 775 | `reference-semantics/semantics/methods.k:125` | rule | ordinary | `rule hasUpper(.IntSeq) => false` |
| 776 | `reference-semantics/semantics/methods.k:126` | rule | ordinary | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 777 | `reference-semantics/semantics/methods.k:128` | syntax | function, total | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 778 | `reference-semantics/semantics/methods.k:129` | rule | ordinary | `rule hasLower(.IntSeq) => false` |
| 779 | `reference-semantics/semantics/methods.k:130` | rule | ordinary | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 780 | `reference-semantics/semantics/methods.k:132` | syntax | function, total | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 781 | `reference-semantics/semantics/methods.k:133` | rule | ordinary | `rule allAlpha(.IntSeq) => true` |
| 782 | `reference-semantics/semantics/methods.k:134` | rule | ordinary | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 783 | `reference-semantics/semantics/methods.k:136` | syntax | function, total | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 784 | `reference-semantics/semantics/methods.k:137` | rule | ordinary | `rule allDigit(.IntSeq) => true` |
| 785 | `reference-semantics/semantics/methods.k:138` | rule | ordinary | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 786 | `reference-semantics/semantics/methods.k:140` | syntax | function, total | `syntax Int ::= lowerC(Int) [function, total]` |
| 787 | `reference-semantics/semantics/methods.k:142` | rule | ordinary | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 788 | `reference-semantics/semantics/methods.k:143` | rule | ordinary, owise | `rule lowerC(C:Int) => C [owise]` |
| 789 | `reference-semantics/semantics/methods.k:145` | syntax | function, total | `syntax Int ::= upperC(Int) [function, total]` |
| 790 | `reference-semantics/semantics/methods.k:146` | rule | ordinary | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 791 | `reference-semantics/semantics/methods.k:147` | rule | ordinary, owise | `rule upperC(C:Int) => C [owise]` |
| 792 | `reference-semantics/semantics/methods.k:149` | syntax | function, total | `syntax Int ::= swapC(Int) [function, total]` |
| 793 | `reference-semantics/semantics/methods.k:150` | rule | ordinary | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 794 | `reference-semantics/semantics/methods.k:151` | rule | ordinary | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 795 | `reference-semantics/semantics/methods.k:152` | rule | ordinary, owise | `rule swapC(C:Int) => C [owise]` |
| 796 | `reference-semantics/semantics/methods.k:154` | syntax | function, total | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 797 | `reference-semantics/semantics/methods.k:155` | rule | ordinary | `rule mapLower(.IntSeq) => .IntSeq` |
| 798 | `reference-semantics/semantics/methods.k:156` | rule | ordinary | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 799 | `reference-semantics/semantics/methods.k:158` | syntax | function, total | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 800 | `reference-semantics/semantics/methods.k:159` | rule | ordinary | `rule mapUpper(.IntSeq) => .IntSeq` |
| 801 | `reference-semantics/semantics/methods.k:160` | rule | ordinary | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 802 | `reference-semantics/semantics/methods.k:162` | syntax | function, total | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 803 | `reference-semantics/semantics/methods.k:163` | rule | ordinary | `rule mapSwap(.IntSeq) => .IntSeq` |
| 804 | `reference-semantics/semantics/methods.k:164` | rule | ordinary | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 805 | `reference-semantics/semantics/methods.k:166` | syntax | function, total | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 806 | `reference-semantics/semantics/methods.k:167` | rule | ordinary | `rule startsWith(.IntSeq, _:IntSeq) => true` |
| 807 | `reference-semantics/semantics/methods.k:168` | rule | ordinary | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 808 | `reference-semantics/semantics/methods.k:169` | rule | ordinary | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| 809 | `reference-semantics/semantics/methods.k:170` | endmodule |  | `endmodule` |
| 810 | `reference-semantics/semantics/operators.k:6` | module |  | `module MPY-OPERATORS` |
| 811 | `reference-semantics/semantics/operators.k:7` | imports |  | `imports MPY-CORE` |
| 812 | `reference-semantics/semantics/operators.k:8` | imports |  | `imports MPY-ITER` |
| 813 | `reference-semantics/semantics/operators.k:10` | rule | ordinary | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 814 | `reference-semantics/semantics/operators.k:12` | rule | ordinary | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes` |
| 815 | `reference-semantics/semantics/operators.k:15` | context |  | `context Compare(HOLE, _)` |
| 816 | `reference-semantics/semantics/operators.k:16` | context |  | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 817 | `reference-semantics/semantics/operators.k:17` | rule | ordinary, owise | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 818 | `reference-semantics/semantics/operators.k:19` | rule | ordinary | `rule applyCmp("is", V:Val, noneV) => V ==K noneV` |
| 819 | `reference-semantics/semantics/operators.k:20` | rule | ordinary, priority | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) // ==== operand deref: heap objects combine/compare by STRUCTURE ============ // (Python: list == is structural; identity only via `is`.) priority(40) // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.` |
| 820 | `reference-semantics/semantics/operators.k:25` | rule | ordinary, priority | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 821 | `reference-semantics/semantics/operators.k:28` | rule | ordinary, priority | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd` |
| 822 | `reference-semantics/semantics/operators.k:34` | rule | ordinary, priority | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| 823 | `reference-semantics/semantics/operators.k:38` | rule | ordinary, priority | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| 824 | `reference-semantics/semantics/operators.k:44` | rule | ordinary, priority | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 825 | `reference-semantics/semantics/operators.k:47` | endmodule |  | `endmodule` |
| 826 | `reference-semantics/semantics/range.k:5` | module |  | `module MPY-RANGE` |
| 827 | `reference-semantics/semantics/range.k:6` | imports |  | `imports MPY-CORE` |
| 828 | `reference-semantics/semantics/range.k:7` | imports |  | `imports MPY-ITER` |
| 829 | `reference-semantics/semantics/range.k:9` | syntax | function, total | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 830 | `reference-semantics/semantics/range.k:10` | rule | ordinary | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 831 | `reference-semantics/semantics/range.k:12` | syntax | function | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 832 | `reference-semantics/semantics/range.k:13` | rule | ordinary | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| 833 | `reference-semantics/semantics/range.k:15` | rule | ordinary | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| 834 | `reference-semantics/semantics/range.k:17` | rule | ordinary | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| 835 | `reference-semantics/semantics/range.k:20` | rule | ordinary | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| 836 | `reference-semantics/semantics/range.k:23` | rule | ordinary | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| 837 | `reference-semantics/semantics/range.k:25` | endmodule |  | `endmodule` |
| 838 | `reference-semantics/semantics/set.k:3` | module |  | `module MPY-SET` |
| 839 | `reference-semantics/semantics/set.k:4` | imports |  | `imports MPY-CORE // a set value, carried as its distinct codes in first-seen order (order is irrelevant // to membership/cardinality — the two observations sets support here).` |
| 840 | `reference-semantics/semantics/set.k:8` | syntax |  | `syntax Val ::= setV(IntSeq) // membership of a code in the accumulated distinct-code sequence` |
| 841 | `reference-semantics/semantics/set.k:11` | syntax | function, total | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 842 | `reference-semantics/semantics/set.k:12` | rule | ordinary | `rule codeIn(_:Int, .IntSeq) => false` |
| 843 | `reference-semantics/semantics/set.k:13` | rule | ordinary | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) // the distinct codes of CS (insert-if-absent fold, first-seen order)` |
| 844 | `reference-semantics/semantics/set.k:16` | syntax | function, total | `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] \| dedupFrom(IntSeq, IntSeq) [function, total]` |
| 845 | `reference-semantics/semantics/set.k:18` | rule | ordinary | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 846 | `reference-semantics/semantics/set.k:19` | rule | ordinary | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 847 | `reference-semantics/semantics/set.k:20` | rule | ordinary | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| 848 | `reference-semantics/semantics/set.k:22` | rule | ordinary | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| 849 | `reference-semantics/semantics/set.k:25` | syntax | function, total | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 850 | `reference-semantics/semantics/set.k:26` | rule | ordinary | `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)` |
| 851 | `reference-semantics/semantics/set.k:27` | rule | ordinary | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) // ==== set equality: two sets are equal iff mutually subsuming ============== // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).` |
| 852 | `reference-semantics/semantics/set.k:31` | syntax | function, total | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 853 | `reference-semantics/semantics/set.k:32` | rule | ordinary | `rule subsetCodes(.IntSeq, _:IntSeq) => true` |
| 854 | `reference-semantics/semantics/set.k:33` | rule | ordinary | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 855 | `reference-semantics/semantics/set.k:35` | syntax | function, total | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 856 | `reference-semantics/semantics/set.k:36` | rule | ordinary | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) // set == set (the only comparison sets support here)` |
| 857 | `reference-semantics/semantics/set.k:39` | rule | ordinary | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| 858 | `reference-semantics/semantics/set.k:40` | endmodule |  | `endmodule` |
| 859 | `reference-semantics/semantics/sort.k:10` | module |  | `module MPY-SORT` |
| 860 | `reference-semantics/semantics/sort.k:11` | imports |  | `imports MPY-BUILTINS` |
| 861 | `reference-semantics/semantics/sort.k:12` | imports |  | `imports MPY-SUBSCRIPT // sortVS(VS): the ascending sort of the Val list VS. Opaque for symbolic VS (no-evaluators); // concrete insertion sort for krun. // Concrete sort matches Int-sorted elements directly (an int Val IS an Int); projectIntTotal // (lemmas-only) is not available in the semantics. Int and str lists.` |
| 862 | `reference-semantics/semantics/sort.k:18` | syntax | function, total, symbol | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 863 | `reference-semantics/semantics/sort.k:19` | syntax | function | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 864 | `reference-semantics/semantics/sort.k:20` | rule | ordinary | `rule sortVS(.ValSeq) => .ValSeq [concrete]` |
| 865 | `reference-semantics/semantics/sort.k:21` | rule | ordinary | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 866 | `reference-semantics/semantics/sort.k:22` | rule | ordinary | `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]` |
| 867 | `reference-semantics/semantics/sort.k:23` | rule | ordinary | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 868 | `reference-semantics/semantics/sort.k:24` | rule | ordinary | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete] // str elements insert by the shared lexicographic strLt (methods.k)` |
| 869 | `reference-semantics/semantics/sort.k:26` | syntax | function | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 870 | `reference-semantics/semantics/sort.k:27` | rule | ordinary | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 871 | `reference-semantics/semantics/sort.k:28` | rule | ordinary | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 872 | `reference-semantics/semantics/sort.k:29` | rule | ordinary | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| 873 | `reference-semantics/semantics/sort.k:31` | rule | ordinary, owise | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise] // applyBuiltin routing in call.k) so the result allocates.` |
| 874 | `reference-semantics/semantics/sort.k:36` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> // mutator: xs.sort() — the in-place heap write over the same trusted sortVS` |
| 875 | `reference-semantics/semantics/sort.k:40` | rule | ordinary, priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] // ==== keyed / reversed sorted() (WP2) ===================================== // sortKeyVS(VS, KV): the stable ascending sort of VS by the key value KV // (a closure/builtin/type — anything callable). OPAQUE here; the concrete // leg (MPY-CONCRETE, llvm only) computes keys by REAL calls and stable- // inserts, at priority(40) over these.` |
| 876 | `reference-semantics/semantics/sort.k:49` | syntax | function, total, symbol | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 877 | `reference-semantics/semantics/sort.k:51` | syntax | function, total | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| 878 | `reference-semantics/semantics/sort.k:53` | rule | ordinary | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 879 | `reference-semantics/semantics/sort.k:54` | rule | ordinary | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 880 | `reference-semantics/semantics/sort.k:55` | rule | ordinary | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 881 | `reference-semantics/semantics/sort.k:57` | syntax | function, total | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 882 | `reference-semantics/semantics/sort.k:58` | rule | ordinary | `rule condRev(S:ValSeq, false) => S` |
| 883 | `reference-semantics/semantics/sort.k:59` | rule | ordinary | `rule condRev(S:ValSeq, true) => revVS(S)` |
| 884 | `reference-semantics/semantics/sort.k:61` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| 885 | `reference-semantics/semantics/sort.k:63` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| 886 | `reference-semantics/semantics/sort.k:65` | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write // their postcondition directly as valSeqAt(sortVS(VS), …).` |
| 887 | `reference-semantics/semantics/sort.k:72` | endmodule |  | `endmodule` |
| 888 | `reference-semantics/semantics/str.k:3` | module |  | `module MPY-STR` |
| 889 | `reference-semantics/semantics/str.k:4` | imports |  | `imports MPY-CORE` |
| 890 | `reference-semantics/semantics/str.k:5` | imports |  | `imports MPY-ITER // ==== iteration (the iterator protocol's str case; yields 1-char strings) ==` |
| 891 | `reference-semantics/semantics/str.k:8` | rule | ordinary | `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>` |
| 892 | `reference-semantics/semantics/str.k:9` | rule | ordinary | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> // ==== str literal (ASCII-only) ============================================` |
| 893 | `reference-semantics/semantics/str.k:13` | syntax | function | `syntax IntSeq ::= strToCodes(String) [function]` |
| 894 | `reference-semantics/semantics/str.k:14` | rule | ordinary | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 895 | `reference-semantics/semantics/str.k:15` | rule | ordinary | `rule strToCodes("") => .IntSeq` |
| 896 | `reference-semantics/semantics/str.k:16` | rule | ordinary | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 // ==== operators: + / == / != / in =========================================` |
| 897 | `reference-semantics/semantics/str.k:20` | syntax | function, total | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 898 | `reference-semantics/semantics/str.k:21` | rule | ordinary | `rule seqConcat(.IntSeq, T:IntSeq) => T` |
| 899 | `reference-semantics/semantics/str.k:22` | rule | ordinary | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 900 | `reference-semantics/semantics/str.k:24` | rule | ordinary | `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 901 | `reference-semantics/semantics/str.k:25` | rule | ordinary | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 902 | `reference-semantics/semantics/str.k:26` | rule | ordinary | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) // substring membership: `P in X` iff the code-seq P occurs contiguously in X` |
| 903 | `reference-semantics/semantics/str.k:29` | rule | ordinary | `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 904 | `reference-semantics/semantics/str.k:30` | rule | ordinary | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 905 | `reference-semantics/semantics/str.k:32` | syntax | function, total | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 906 | `reference-semantics/semantics/str.k:33` | rule | ordinary | `rule strPrefix(.IntSeq, _:IntSeq) => true` |
| 907 | `reference-semantics/semantics/str.k:34` | rule | ordinary | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 908 | `reference-semantics/semantics/str.k:35` | rule | ordinary | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 909 | `reference-semantics/semantics/str.k:37` | syntax | function, total | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 910 | `reference-semantics/semantics/str.k:38` | rule | ordinary | `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)` |
| 911 | `reference-semantics/semantics/str.k:39` | rule | ordinary | `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)` |
| 912 | `reference-semantics/semantics/str.k:40` | rule | ordinary | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on // str </<=/>/>= comparisons.` |
| 913 | `reference-semantics/semantics/str.k:48` | syntax | function, total | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 914 | `reference-semantics/semantics/str.k:49` | rule | ordinary | `rule strLt(.IntSeq, .IntSeq) => false` |
| 915 | `reference-semantics/semantics/str.k:50` | rule | ordinary | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 916 | `reference-semantics/semantics/str.k:51` | rule | ordinary | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 917 | `reference-semantics/semantics/str.k:52` | rule | ordinary | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B` |
| 918 | `reference-semantics/semantics/str.k:53` | rule | ordinary | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B` |
| 919 | `reference-semantics/semantics/str.k:54` | rule | ordinary | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 920 | `reference-semantics/semantics/str.k:56` | rule | ordinary | `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 921 | `reference-semantics/semantics/str.k:57` | rule | ordinary | `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 922 | `reference-semantics/semantics/str.k:58` | rule | ordinary | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 923 | `reference-semantics/semantics/str.k:59` | rule | ordinary | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| 924 | `reference-semantics/semantics/str.k:60` | endmodule |  | `endmodule` |
| 925 | `reference-semantics/semantics/subscript.k:3` | module |  | `module MPY-SUBSCRIPT` |
| 926 | `reference-semantics/semantics/subscript.k:4` | imports |  | `imports MPY-CORE // ==== positional access + negative-index normalization (used only here) === // valSeqAt is [total]: in-bounds vCons access reduces as usual; on an OPAQUE sequence (e.g. // a trusted sort's sortVS(VS)) or OOB it stays an abstract total value — so indexing the // opaque sorted list is DEFINED (no undischarged #Ceil), matching the old semantics' total // atK. K trusts the [total] annotation; valid programs index in-bounds.` |
| 927 | `reference-semantics/semantics/subscript.k:11` | syntax | function, total | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 928 | `reference-semantics/semantics/subscript.k:12` | rule | ordinary | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V` |
| 929 | `reference-semantics/semantics/subscript.k:13` | rule | ordinary | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| 930 | `reference-semantics/semantics/subscript.k:16` | syntax | function | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 931 | `reference-semantics/semantics/subscript.k:17` | rule | ordinary | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C` |
| 932 | `reference-semantics/semantics/subscript.k:18` | rule | ordinary | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| 933 | `reference-semantics/semantics/subscript.k:21` | syntax | function, total | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 934 | `reference-semantics/semantics/subscript.k:22` | rule | ordinary | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 935 | `reference-semantics/semantics/subscript.k:23` | rule | ordinary | `rule normIdx(I:Int, _:Int) => I requires I >=Int 0 // ==== Subscript: indexing obj[i] (list / tuple / str) ===================== // contexts (not strict attrs): the Index slot's Slice alternative must never heat` |
| 936 | `reference-semantics/semantics/subscript.k:27` | context |  | `context Subscript(HOLE, _)` |
| 937 | `reference-semantics/semantics/subscript.k:28` | context |  | `context Subscript(_:Val, HOLE:Expr) // heap-object deref (covers both the index and slice forms via the Index slot)` |
| 938 | `reference-semantics/semantics/subscript.k:31` | rule | ordinary, priority | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 939 | `reference-semantics/semantics/subscript.k:35` | rule | ordinary | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 940 | `reference-semantics/semantics/subscript.k:37` | syntax | function | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 941 | `reference-semantics/semantics/subscript.k:38` | rule | ordinary | `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 942 | `reference-semantics/semantics/subscript.k:39` | rule | ordinary | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 943 | `reference-semantics/semantics/subscript.k:40` | rule | ordinary | `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========` |
| 944 | `reference-semantics/semantics/subscript.k:44` | syntax |  | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| 945 | `reference-semantics/semantics/subscript.k:49` | syntax |  | `syntax OptInt ::= "noB" \| someB(Int)` |
| 946 | `reference-semantics/semantics/subscript.k:50` | rule | ordinary | `rule <k> #evalB(NoBound) => noB ... </k>` |
| 947 | `reference-semantics/semantics/subscript.k:51` | rule | ordinary | `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>` |
| 948 | `reference-semantics/semantics/subscript.k:52` | rule | ordinary | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 949 | `reference-semantics/semantics/subscript.k:54` | rule | ordinary | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 950 | `reference-semantics/semantics/subscript.k:55` | rule | ordinary | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 951 | `reference-semantics/semantics/subscript.k:56` | rule | ordinary | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> // a list slice constructs a NEW object; a str slice stays a value` |
| 952 | `reference-semantics/semantics/subscript.k:58` | rule | ordinary, priority | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| 953 | `reference-semantics/semantics/subscript.k:61` | rule | ordinary | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 954 | `reference-semantics/semantics/subscript.k:63` | syntax | function | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 955 | `reference-semantics/semantics/subscript.k:64` | rule | ordinary | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 956 | `reference-semantics/semantics/subscript.k:66` | rule | ordinary | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 957 | `reference-semantics/semantics/subscript.k:68` | rule | ordinary | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) // ==== slice.indices: step / start / stop / clamp ==========================` |
| 958 | `reference-semantics/semantics/subscript.k:72` | syntax | function, total | `syntax Int ::= slStep(OptInt) [function, total]` |
| 959 | `reference-semantics/semantics/subscript.k:73` | rule | ordinary | `rule slStep(noB) => 1` |
| 960 | `reference-semantics/semantics/subscript.k:74` | rule | ordinary | `rule slStep(someB(S:Int)) => S` |
| 961 | `reference-semantics/semantics/subscript.k:76` | syntax | function | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 962 | `reference-semantics/semantics/subscript.k:77` | rule | ordinary | `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| 963 | `reference-semantics/semantics/subscript.k:79` | rule | ordinary | `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0` |
| 964 | `reference-semantics/semantics/subscript.k:81` | rule | ordinary | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 965 | `reference-semantics/semantics/subscript.k:83` | syntax | function | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 966 | `reference-semantics/semantics/subscript.k:84` | rule | ordinary | `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0` |
| 967 | `reference-semantics/semantics/subscript.k:86` | rule | ordinary | `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| 968 | `reference-semantics/semantics/subscript.k:88` | rule | ordinary | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 969 | `reference-semantics/semantics/subscript.k:90` | syntax | function, total | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 970 | `reference-semantics/semantics/subscript.k:91` | rule | ordinary | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0` |
| 971 | `reference-semantics/semantics/subscript.k:93` | rule | ordinary | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| 972 | `reference-semantics/semantics/subscript.k:96` | syntax | function, total | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 973 | `reference-semantics/semantics/subscript.k:97` | rule | ordinary | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| 974 | `reference-semantics/semantics/subscript.k:99` | rule | ordinary | `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| 975 | `reference-semantics/semantics/subscript.k:102` | syntax | function, total | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 976 | `reference-semantics/semantics/subscript.k:103` | rule | ordinary | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN` |
| 977 | `reference-semantics/semantics/subscript.k:105` | rule | ordinary | `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN // ==== build the strided sub-sequence (indices in range by construction) ====` |
| 978 | `reference-semantics/semantics/subscript.k:109` | syntax | function | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 979 | `reference-semantics/semantics/subscript.k:110` | rule | ordinary | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 980 | `reference-semantics/semantics/subscript.k:113` | rule | ordinary | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 981 | `reference-semantics/semantics/subscript.k:116` | syntax | function | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 982 | `reference-semantics/semantics/subscript.k:117` | rule | ordinary | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 983 | `reference-semantics/semantics/subscript.k:120` | rule | ordinary | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 984 | `reference-semantics/semantics/subscript.k:122` | endmodule |  | `endmodule` |
| 985 | `reference-semantics/semantics/syntax.k:3` | module |  | `module MPY-SYNTAX` |
| 986 | `reference-semantics/semantics/syntax.k:4` | imports |  | `imports INT-SYNTAX` |
| 987 | `reference-semantics/semantics/syntax.k:5` | imports |  | `imports FLOAT-SYNTAX` |
| 988 | `reference-semantics/semantics/syntax.k:6` | imports |  | `imports BOOL-SYNTAX` |
| 989 | `reference-semantics/semantics/syntax.k:7` | imports |  | `imports STRING-SYNTAX` |
| 990 | `reference-semantics/semantics/syntax.k:9` | syntax | macro | `syntax Expr ::= "Int" "(" Int ")" \| "Float" "(" Float ")" \| "Bool" "(" Bool ")" \| "Name" "(" String ")" \| "Str" "(" String ")" \| "UnaryOp" "(" String "," Expr ")" [strict(2)] \| "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp" "(" String "," Exprs ")" \| "ListExpr" "(" Exprs ")" \| "DictExpr" "(" Entries ")" \| "ListComp" "(" Expr "," CompFors ")" [macro] \| "GenExp" "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda" "(" Params "," Expr ")" \| "KwArg" "(" String "," Expr ")" \| "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call" "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare" "(" Expr "," CmpOp ")"` |
| 991 | `reference-semantics/semantics/syntax.k:32` | syntax |  | `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"` |
| 992 | `reference-semantics/semantics/syntax.k:33` | syntax |  | `syntax Entry ::= "Entry" "(" Expr "," Expr ")"` |
| 993 | `reference-semantics/semantics/syntax.k:34` | syntax |  | `syntax Entries ::= List{Entry, ","}` |
| 994 | `reference-semantics/semantics/syntax.k:35` | syntax |  | `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 995 | `reference-semantics/semantics/syntax.k:36` | syntax |  | `syntax CompFors ::= List{CompFor, ""}` |
| 996 | `reference-semantics/semantics/syntax.k:37` | syntax |  | `syntax Exprs ::= List{Expr, ","}` |
| 997 | `reference-semantics/semantics/syntax.k:38` | syntax |  | `syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 998 | `reference-semantics/semantics/syntax.k:39` | syntax |  | `syntax Bound ::= Expr \| "NoBound"` |
| 999 | `reference-semantics/semantics/syntax.k:41` | syntax |  | `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] \| "Import" "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While" "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return" "(" Expr ")" [strict] \| "Assert" "(" Expr ")" [strict] \| "Expr" "(" Expr ")" [strict] \| "FuncDef" "(" String "," Params "," Stmts ")" \| "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` |
| 1000 | `reference-semantics/semantics/syntax.k:56` | syntax |  | `syntax Stmts ::= List{Stmt, ""}` |
| 1001 | `reference-semantics/semantics/syntax.k:57` | syntax |  | `syntax Params ::= "Params" "(" ParamNames ")"` |
| 1002 | `reference-semantics/semantics/syntax.k:58` | syntax |  | `syntax CellVars ::= "CellVars" "(" ParamNames ")"` |
| 1003 | `reference-semantics/semantics/syntax.k:59` | syntax |  | `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"` |
| 1004 | `reference-semantics/semantics/syntax.k:60` | syntax |  | `syntax ParamNames ::= List{String, ","}` |
| 1005 | `reference-semantics/semantics/syntax.k:61` | syntax |  | `syntax Module ::= "Module" "(" Stmts ")"` |
| 1006 | `reference-semantics/semantics/syntax.k:62` | endmodule |  | `endmodule` |
| 1007 | `reference-semantics/semantics/tuple.k:3` | module |  | `module MPY-TUPLE` |
| 1008 | `reference-semantics/semantics/tuple.k:4` | imports |  | `imports MPY-CORE` |
| 1009 | `reference-semantics/semantics/tuple.k:5` | imports |  | `imports MPY-ITER` |
| 1010 | `reference-semantics/semantics/tuple.k:6` | imports |  | `imports MPY-LIST` |
| 1011 | `reference-semantics/semantics/tuple.k:7` | imports |  | `imports MPY-METHODS // ==== iteration (the iterator protocol's tuple case) ======================` |
| 1012 | `reference-semantics/semantics/tuple.k:10` | rule | ordinary | `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>` |
| 1013 | `reference-semantics/semantics/tuple.k:11` | rule | ordinary | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================` |
| 1014 | `reference-semantics/semantics/tuple.k:14` | syntax |  | `syntax ApplyK ::= "toTuple"` |
| 1015 | `reference-semantics/semantics/tuple.k:15` | rule | ordinary | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 1016 | `reference-semantics/semantics/tuple.k:16` | rule | ordinary | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 1017 | `reference-semantics/semantics/tuple.k:18` | rule | ordinary | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B // membership routes through the same k-cell fold as lists (list.k)` |
| 1018 | `reference-semantics/semantics/tuple.k:20` | rule | ordinary | `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 1019 | `reference-semantics/semantics/tuple.k:21` | rule | ordinary | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> // t.index(v): first index of v (ValueError out of subset)` |
| 1020 | `reference-semantics/semantics/tuple.k:23` | rule | ordinary | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 1021 | `reference-semantics/semantics/tuple.k:24` | syntax | function | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 1022 | `reference-semantics/semantics/tuple.k:25` | rule | ordinary | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 1023 | `reference-semantics/semantics/tuple.k:26` | rule | ordinary | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| 1024 | `reference-semantics/semantics/tuple.k:28` | rule | ordinary | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) // ==== target binding: bind a Name or a TupleExpr target to a value ========` |
| 1025 | `reference-semantics/semantics/tuple.k:31` | syntax |  | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 1026 | `reference-semantics/semantics/tuple.k:32` | rule | ordinary | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 1027 | `reference-semantics/semantics/tuple.k:35` | rule | ordinary, priority | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 1028 | `reference-semantics/semantics/tuple.k:42` | rule | ordinary | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 1029 | `reference-semantics/semantics/tuple.k:43` | rule | ordinary | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 1030 | `reference-semantics/semantics/tuple.k:44` | rule | ordinary, priority | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // ==== unpacking: a, b = <tuple\|list> (RHS evaluated by strictness) ========` |
| 1031 | `reference-semantics/semantics/tuple.k:49` | syntax |  | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 1032 | `reference-semantics/semantics/tuple.k:50` | rule | ordinary | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 1033 | `reference-semantics/semantics/tuple.k:51` | rule | ordinary | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 1034 | `reference-semantics/semantics/tuple.k:52` | rule | ordinary, priority | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 1035 | `reference-semantics/semantics/tuple.k:55` | rule | ordinary | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| 1036 | `reference-semantics/semantics/tuple.k:57` | rule | ordinary | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| 1037 | `reference-semantics/semantics/tuple.k:58` | endmodule |  | `endmodule` |
| 1038 | `reference-semantics/semantics.k:34` | requires |  | `requires "semantics/syntax.k"` |
| 1039 | `reference-semantics/semantics.k:35` | requires |  | `requires "semantics/core.k"` |
| 1040 | `reference-semantics/semantics.k:36` | requires |  | `requires "semantics/iter.k"` |
| 1041 | `reference-semantics/semantics.k:37` | requires |  | `requires "semantics/range.k"` |
| 1042 | `reference-semantics/semantics.k:38` | requires |  | `requires "semantics/operators.k"` |
| 1043 | `reference-semantics/semantics.k:39` | requires |  | `requires "semantics/int.k"` |
| 1044 | `reference-semantics/semantics.k:40` | requires |  | `requires "semantics/bool.k"` |
| 1045 | `reference-semantics/semantics.k:41` | requires |  | `requires "semantics/float.k"` |
| 1046 | `reference-semantics/semantics.k:42` | requires |  | `requires "semantics/str.k"` |
| 1047 | `reference-semantics/semantics.k:43` | requires |  | `requires "semantics/set.k"` |
| 1048 | `reference-semantics/semantics.k:44` | requires |  | `requires "semantics/list.k"` |
| 1049 | `reference-semantics/semantics.k:45` | requires |  | `requires "semantics/tuple.k"` |
| 1050 | `reference-semantics/semantics.k:46` | requires |  | `requires "semantics/subscript.k"` |
| 1051 | `reference-semantics/semantics.k:47` | requires |  | `requires "semantics/comprehension.k"` |
| 1052 | `reference-semantics/semantics.k:48` | requires |  | `requires "semantics/methods.k"` |
| 1053 | `reference-semantics/semantics.k:49` | requires |  | `requires "semantics/controls.k"` |
| 1054 | `reference-semantics/semantics.k:50` | requires |  | `requires "semantics/functions.k"` |
| 1055 | `reference-semantics/semantics.k:51` | requires |  | `requires "semantics/builtins.k"` |
| 1056 | `reference-semantics/semantics.k:52` | requires |  | `requires "semantics/call.k"` |
| 1057 | `reference-semantics/semantics.k:53` | requires |  | `requires "semantics/sort.k"` |
| 1058 | `reference-semantics/semantics.k:54` | requires |  | `requires "semantics/assert.k"` |
| 1059 | `reference-semantics/semantics.k:55` | requires |  | `requires "semantics/dict.k"` |
| 1060 | `reference-semantics/semantics.k:56` | requires |  | `requires "semantics/concrete.k"` |
| 1061 | `reference-semantics/semantics.k:58` | module |  | `module MPY` |
| 1062 | `reference-semantics/semantics.k:59` | imports |  | `imports MPY-CORE` |
| 1063 | `reference-semantics/semantics.k:60` | imports |  | `imports MPY-ITER` |
| 1064 | `reference-semantics/semantics.k:61` | imports |  | `imports MPY-RANGE` |
| 1065 | `reference-semantics/semantics.k:62` | imports |  | `imports MPY-OPERATORS` |
| 1066 | `reference-semantics/semantics.k:63` | imports |  | `imports MPY-INT` |
| 1067 | `reference-semantics/semantics.k:64` | imports |  | `imports MPY-BOOL` |
| 1068 | `reference-semantics/semantics.k:65` | imports |  | `imports MPY-FLOAT` |
| 1069 | `reference-semantics/semantics.k:66` | imports |  | `imports MPY-STR` |
| 1070 | `reference-semantics/semantics.k:67` | imports |  | `imports MPY-SET` |
| 1071 | `reference-semantics/semantics.k:68` | imports |  | `imports MPY-LIST` |
| 1072 | `reference-semantics/semantics.k:69` | imports |  | `imports MPY-TUPLE` |
| 1073 | `reference-semantics/semantics.k:70` | imports |  | `imports MPY-SUBSCRIPT` |
| 1074 | `reference-semantics/semantics.k:71` | imports |  | `imports MPY-COMPREHENSION` |
| 1075 | `reference-semantics/semantics.k:72` | imports |  | `imports MPY-METHODS` |
| 1076 | `reference-semantics/semantics.k:73` | imports |  | `imports MPY-CONTROLS` |
| 1077 | `reference-semantics/semantics.k:74` | imports |  | `imports MPY-FUNCTIONS` |
| 1078 | `reference-semantics/semantics.k:75` | imports |  | `imports MPY-BUILTINS` |
| 1079 | `reference-semantics/semantics.k:76` | imports |  | `imports MPY-CALL` |
| 1080 | `reference-semantics/semantics.k:77` | imports |  | `imports MPY-SORT` |
| 1081 | `reference-semantics/semantics.k:78` | imports |  | `imports MPY-ASSERT` |
| 1082 | `reference-semantics/semantics.k:79` | imports |  | `imports MPY-DICT` |
| 1083 | `reference-semantics/semantics.k:80` | endmodule |  | `endmodule // The krun (llvm) main module: MPY plus the concrete-only legs (keyed sort's // real key calls, deep list equality). Verification builds import MPY and // never see MPY-CONCRETE. The llvm kompile MUST use --main-module MPY-KRUN — // with plain MPY the concrete legs are silently absent (this was live for a // while: sorted-key stuck and comprehension asserted wrong under krun).` |
| 1084 | `reference-semantics/semantics.k:87` | module |  | `module MPY-KRUN` |
| 1085 | `reference-semantics/semantics.k:88` | imports |  | `imports MPY` |
| 1086 | `reference-semantics/semantics.k:89` | imports |  | `imports MPY-CONCRETE` |
| 1087 | `reference-semantics/semantics.k:90` | endmodule |  | `endmodule` |
| 1088 | `verification.k:1` | requires |  | `requires "reference-semantics/semantics.k"` |
| 1089 | `verification.k:3` | module |  | `module VERIFICATION` |
| 1090 | `verification.k:4` | imports |  | `imports MPY // Explicit form of Map deletion used by function-frame teardown.` |
| 1091 | `verification.k:7` | rule | simplification | `rule (((X:KItem \|-> _:KItem) M:Map) [ X <- undef ]) => M requires notBool (X in_keys(M)) [simplification]` |
| 1092 | `verification.k:10` | rule | simplification | `rule (M:Map [ X:KItem <- V:KItem ]) => (X \|-> V) M requires notBool (X in_keys(M)) [simplification] // Proof-normalization lemmas for ordinary (non-closure-cell) frames. These // are guarded specializations of MPY's existing rules; the priority prevents // the symbolic prover from exploring impossible cellRef branches after the // guard has established that "$cells" is absent.` |
| 1093 | `verification.k:18` | rule | ordinary, priority | `rule <k> Name(X:String) => {M[X]}:>Val ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) andBool notBool ("$cells" in_keys(M)) [priority(39)]` |
| 1094 | `verification.k:24` | rule | ordinary, priority | `rule <k> Name(X:String) => V:Val ... </k> <env> L:Int </env> <scopes> ... L \|-> scope((X \|-> V) M:Map, _:Parent) ... </scopes> requires notBool (X in_keys(M)) andBool notBool ("$cells" in_keys((X \|-> V) M)) [priority(38)]` |
| 1095 | `verification.k:31` | rule | ordinary, priority | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _:Parent) ... </scopes> requires notBool ("$cells" in_keys(M)) [priority(39)] // Direct literal cooling, equivalent to Int(I) => I followed by Assign's // strictness context. Keeping it explicit avoids a symbolic freezer branch // at loop-summary boundaries.` |
| 1096 | `verification.k:40` | rule | ordinary, priority | `rule <k> Assign(Name(X:String), Int(I:Int)) => Assign(Name(X), I) ... </k> [priority(39)]` |
| 1097 | `verification.k:43` | rule | ordinary, priority | `rule <k> Assign(Name(X:String), Bool(B:Bool)) => Assign(Name(X), B) ... </k> [priority(39)]` |
| 1098 | `verification.k:46` | rule | ordinary, priority | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope( ((X \|-> _:Val) M:Map => (X \|-> V) M), _:Parent) ... </scopes> requires notBool (X in_keys(M)) andBool notBool ("$cells" in_keys((X \|-> V) M)) [priority(38)]` |
| 1099 | `verification.k:55` | rule | ordinary, priority | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope( M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _:Parent) ... </scopes> requires X in_keys(M) andBool notBool ("$cells" in_keys(M)) andBool notBool isRefV({M[X]}:>Val) [priority(39)]` |
| 1100 | `verification.k:65` | rule | ordinary, priority | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope( ((X \|-> A:Val) M:Map => (X \|-> applyBin(OP, A, V)) M), _:Parent) ... </scopes> requires notBool (X in_keys(M)) andBool notBool ("$cells" in_keys((X \|-> A) M)) andBool notBool isRefV(A) [priority(38)]` |
| 1101 | `verification.k:75` | rule | ordinary, priority | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _:Parent) ... </scopes> requires notBool ("$cells" in_keys(M)) [priority(39)]` |
| 1102 | `verification.k:81` | rule | ordinary, priority | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope( ((X \|-> _:Val) M:Map => (X \|-> V) M), _:Parent) ... </scopes> requires notBool (X in_keys(M)) andBool notBool ("$cells" in_keys((X \|-> V) M)) [priority(38)] // Strictness-normalized forms used by the outer list loop.` |
| 1103 | `verification.k:91` | rule | ordinary, priority | `rule <k> Compare(Name(X:String), CmpOp(OP:String, Name(Y:String))) => applyCmp(OP, A, B) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope( (X \|-> A:Val) (Y \|-> B:Val) M:Map, _:Parent) ... </scopes> requires X =/=String Y andBool notBool (X in_keys(M)) andBool notBool (Y in_keys(M)) andBool notBool ("$cells" in_keys((X \|-> A) (Y \|-> B) M)) [priority(38)]` |
| 1104 | `verification.k:103` | rule | ordinary, priority | `rule <k> Compare(Name(X:String), CmpOp(OP:String, Int(I:Int))) => applyCmp(OP, A, I) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope((X \|-> A:Val) M:Map, _:Parent) ... </scopes> requires notBool (X in_keys(M)) andBool notBool ("$cells" in_keys((X \|-> A) M)) [priority(38)]` |
| 1105 | `verification.k:111` | rule | ordinary, priority | `rule <k> If(Name(X:String), T:Stmts, E:Stmts) => #branch(truthy(V), T, E) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope((X \|-> V:Val) M:Map, _:Parent) ... </scopes> requires notBool (X in_keys(M)) andBool notBool ("$cells" in_keys((X \|-> V) M)) [priority(38)]` |
| 1106 | `verification.k:119` | rule | ordinary, priority | `rule <k> Assign(Name(X:String), Name(Y:String)) => Assign(Name(X), V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope((Y \|-> V:Val) M:Map, _:Parent) ... </scopes> requires notBool (Y in_keys(M)) andBool notBool ("$cells" in_keys((Y \|-> V) M)) [priority(38)]` |
| 1107 | `verification.k:127` | rule | ordinary, priority | `rule <k> Return(Name(X:String)) => Return(V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope((X \|-> V:Val) M:Map, _:Parent) ... </scopes> requires notBool (X in_keys(M)) andBool notBool ("$cells" in_keys((X \|-> V) M)) [priority(38)]` |
| 1108 | `verification.k:134` | rule | ordinary, priority | `rule <k> For(T:Expr, Name(X:String), B:Stmts) => #loop(V, T, B) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope((X \|-> V:Val) M:Map, _:Parent) ... </scopes> requires notBool (X in_keys(M)) andBool notBool ("$cells" in_keys((X \|-> V) M)) [priority(38)]` |
| 1109 | `verification.k:142` | rule | ordinary, priority | `rule <k> Call( Name("skjkasdkd"), (list(asVals(IS:IntList)), .Exprs)) => #applyK( toCall(closureVal( ("lst", .ParamNames), #functionBody, 0)), (list(asVals(IS)), .Vals)) ... </k> <env> 0 </env> <scopes> ... 0 \|-> scope( ("skjkasdkd" \|-> closureVal( ("lst", .ParamNames), #functionBody, 0)) M:Map, parent(-1)) ... </scopes> requires notBool ("skjkasdkd" in_keys(M)) [priority(38)]` |
| 1110 | `verification.k:166` | rule | ordinary, priority | `rule <k> Assign( Name("prime"), Compare(Name("number"), CmpOp(">=", Int(2)))) => Assign(Name("prime"), N >=Int 2) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(("number" \|-> N:Int) M:Map, _:Parent) ... </scopes> requires notBool ("number" in_keys(M)) andBool notBool ("$cells" in_keys(("number" \|-> N) M)) [priority(38)] // Integer-only input lists. This sort makes the task's stated input // precondition structural, so symbolic execution never admits a non-int // element.` |
| 1111 | `verification.k:181` | syntax |  | `syntax IntList ::= ".IntList" \| intCons(Int, IntList)` |
| 1112 | `verification.k:183` | syntax |  | `syntax ValSeq ::= asVals(IntList) // Structural iterator cases expose IntList's constructors to narrowing.` |
| 1113 | `verification.k:186` | rule | ordinary, priority | `rule <k> #iterNext(list(asVals(.IntList))) => #iterDone ... </k> [priority(39)]` |
| 1114 | `verification.k:188` | rule | ordinary, priority | `rule <k> #iterNext(list(asVals(intCons(I:Int, IS:IntList)))) => #iterYield(I, list(asVals(IS))) ... </k> [priority(39)] // The mathematical primality oracle follows the implementation's trial // division exactly. false means that an earlier divisor was already found.` |
| 1115 | `verification.k:194` | syntax | function, total | `syntax Bool ::= trialPrime(Int, Int, Bool) [function, total]` |
| 1116 | `verification.k:195` | rule | ordinary | `rule trialPrime(_:Int, _:Int, false) => false` |
| 1117 | `verification.k:196` | rule | ordinary | `rule trialPrime(N:Int, D:Int, true) => true requires D *Int D >Int N` |
| 1118 | `verification.k:198` | rule | simplification | `rule trialPrime(N:Int, D:Int, true) => false requires D *Int D <=Int N andBool pyMod(N, D) ==Int 0 [simplification]` |
| 1119 | `verification.k:201` | rule | simplification | `rule trialPrime(N:Int, D:Int, true) => trialPrime(N, D +Int 1, true) requires D *Int D <=Int N andBool notBool (pyMod(N, D) ==Int 0) [simplification] // The final divisor value is specified too, allowing the loop invariant to // describe the whole local store rather than hiding a side effect.` |
| 1120 | `verification.k:208` | syntax | function, total | `syntax Int ::= trialDivisor(Int, Int, Bool) [function, total]` |
| 1121 | `verification.k:209` | rule | ordinary | `rule trialDivisor(_:Int, D:Int, false) => D` |
| 1122 | `verification.k:210` | rule | ordinary | `rule trialDivisor(N:Int, D:Int, true) => D requires D *Int D >Int N` |
| 1123 | `verification.k:212` | rule | simplification | `rule trialDivisor(N:Int, D:Int, true) => D +Int 1 requires D *Int D <=Int N andBool pyMod(N, D) ==Int 0 [simplification]` |
| 1124 | `verification.k:215` | rule | simplification | `rule trialDivisor(N:Int, D:Int, true) => trialDivisor(N, D +Int 1, true) requires D *Int D <=Int N andBool notBool (pyMod(N, D) ==Int 0) [simplification]` |
| 1125 | `verification.k:221` | syntax | function, total | `syntax Bool ::= isPrime(Int) [function, total]` |
| 1126 | `verification.k:222` | rule | ordinary | `rule isPrime(N:Int) => trialPrime(N, 2, N >=Int 2)` |
| 1127 | `verification.k:224` | syntax | function, total | `syntax Int ::= largestPrime(IntList, Int) [function, total]` |
| 1128 | `verification.k:225` | rule | ordinary | `rule largestPrime(.IntList, CUR:Int) => CUR` |
| 1129 | `verification.k:226` | rule | simplification | `rule largestPrime(intCons(N:Int, IS:IntList), CUR:Int) => largestPrime(IS, N) requires N >Int CUR andBool isPrime(N) [simplification]` |
| 1130 | `verification.k:230` | rule | simplification | `rule largestPrime(intCons(N:Int, IS:IntList), CUR:Int) => largestPrime(IS, CUR) requires N <=Int CUR orBool (N >Int CUR andBool notBool isPrime(N)) [simplification]` |
| 1131 | `verification.k:236` | syntax | function, total | `syntax Int ::= digitAcc(Int, Int) [function, total]` |
| 1132 | `verification.k:237` | rule | simplification | `rule digitAcc(N:Int, A:Int) => A requires N <=Int 0 [simplification]` |
| 1133 | `verification.k:240` | rule | simplification | `rule digitAcc(N:Int, A:Int) => digitAcc( (N -Int pyMod(N, 10)) /Int 10, A +Int pyMod(N, 10)) requires N >Int 0 [simplification]` |
| 1134 | `verification.k:247` | syntax | function, total | `syntax Int ::= digitSum(Int) [function, total]` |
| 1135 | `verification.k:248` | rule | ordinary | `rule digitSum(N:Int) => digitAcc(N, 0) // Exact AST fragments emitted by py2mpy.py for solution.py.` |
| 1136 | `verification.k:251` | syntax | macro | `syntax Expr ::= "#primeCond" [macro]` |
| 1137 | `verification.k:252` | rule | ordinary | `rule #primeCond => BoolOp( "and", Name("prime"), Compare( BinOp("*", Name("divisor"), Name("divisor")), CmpOp("<=", Name("number"))))` |
| 1138 | `verification.k:259` | syntax | macro | `syntax Stmts ::= "#primeBody" [macro]` |
| 1139 | `verification.k:260` | rule | ordinary | `rule #primeBody => If(Compare( BinOp("%", Name("number"), Name("divisor")), CmpOp("==", Int(0))), Assign(Name("prime"), Bool(false)), .Stmts) AugAssign(Name("divisor"), "+", Int(1))` |
| 1140 | `verification.k:268` | syntax | macro | `syntax Stmts ::= "#scanBody" [macro]` |
| 1141 | `verification.k:269` | rule | ordinary | `rule #scanBody => If(Compare(Name("number"), CmpOp(">", Name("largest"))), Assign(Name("divisor"), Int(2)) Assign( Name("prime"), Compare(Name("number"), CmpOp(">=", Int(2)))) While(#primeCond, #primeBody) If(Name("prime"), Assign(Name("largest"), Name("number")), .Stmts), .Stmts)` |
| 1142 | `verification.k:281` | syntax | macro | `syntax Expr ::= "#digitCond" [macro]` |
| 1143 | `verification.k:282` | rule | ordinary | `rule #digitCond => Compare(Name("largest"), CmpOp(">", Int(0)))` |
| 1144 | `verification.k:285` | syntax | macro | `syntax Stmts ::= "#digitBody" [macro]` |
| 1145 | `verification.k:286` | rule | ordinary | `rule #digitBody => AugAssign( Name("digit_total"), "+", BinOp("%", Name("largest"), Int(10))) AugAssign(Name("largest"), "//", Int(10))` |
| 1146 | `verification.k:293` | syntax | macro | `syntax Stmts ::= "#functionBody" [macro]` |
| 1147 | `verification.k:294` | rule | ordinary | `rule #functionBody => Assign(Name("largest"), Int(0)) Assign(Name("number"), Int(0)) Assign(Name("divisor"), Int(2)) Assign(Name("prime"), Bool(false)) Assign(Name("digit_total"), Int(0)) For(Name("number"), Name("lst"), #scanBody) While(#digitCond, #digitBody) Return(Name("digit_total")) // Bounded entry-prefix summary. It is the direct composition of MPY-CALL's // frame allocation, #bindP, the five literal assignments, and For's // one-time iterable evaluation. No loop iteration is summarized here.` |
| 1148 | `verification.k:307` | rule | ordinary, priority | `rule <k> #applyK( toCall(closureVal( ("lst", .ParamNames), #functionBody, 0)), (list(asVals(IS:IntList)), .Vals)) => #loop(list(asVals(IS)), Name("number"), #scanBody) ~> While(#digitCond, #digitBody) ~> Return(Name("digit_total")) ~> #endcall </k> <env> 0 => 1 </env> <scopes> MOD:Map => MOD 1 \|-> scope( ("lst" \|-> list(asVals(IS))) ("largest" \|-> 0) ("number" \|-> 0) ("divisor" \|-> 2) ("prime" \|-> false) ("digit_total" \|-> 0), parent(0)) </scopes> <scopeLoc> 1 => 2 </scopeLoc> <stack> .List => ListItem(frame(.K, 0, 1)) </stack> requires notBool (1 in_keys(MOD)) [priority(37)]` |
| 1149 | `verification.k:341` | syntax | macro | `syntax Module ::= "solutionModule" [macro]` |
| 1150 | `verification.k:342` | rule | ordinary | `rule solutionModule => Module(FuncDef("skjkasdkd", Params("lst"), #functionBody))` |
| 1151 | `verification.k:344` | endmodule |  | `endmodule` |
| 1152 | `spec.k:1` | requires |  | `requires "verification.k"` |
| 1153 | `spec.k:3` | module |  | `module SPEC` |
| 1154 | `spec.k:4` | imports |  | `imports VERIFICATION // Trial-division loop invariant.` |
| 1155 | `spec.k:7` | claim |  | `claim [prime-loop]: <k> #while(#primeCond, #primeBody) ~> K:K => K </k> <env> L:Int </env> <scopes> SC:Map L \|-> scope( ("number" \|-> N:Int) ("divisor" \|-> D:Int) ("prime" \|-> B:Bool) REST:Map, P:Parent) => SC L \|-> scope( ("number" \|-> N) ("divisor" \|-> trialDivisor(N, D, B)) ("prime" \|-> trialPrime(N, D, B)) REST, P) </scopes> requires D >=Int 2 andBool (notBool B orBool N >=Int 2) andBool notBool ("number" in_keys(REST)) andBool notBool ("divisor" in_keys(REST)) andBool notBool ("prime" in_keys(REST)) andBool notBool ("$cells" in_keys(REST)) andBool notBool ("$cells" in_keys( ("number" \|-> N) ("divisor" \|-> D) ("prime" \|-> B) REST)) // Decimal digit accumulation loop invariant.` |
| 1156 | `spec.k:42` | claim |  | `claim [digit-loop]: <k> #while(#digitCond, #digitBody) ~> K:K => K </k> <env> L:Int </env> <scopes> SC:Map L \|-> scope( ("largest" \|-> N:Int) ("digit_total" \|-> A:Int) REST:Map, P:Parent) => SC L \|-> scope( ("largest" \|-> 0) ("digit_total" \|-> digitAcc(N, A)) REST, P) </scopes> requires N >=Int 0 andBool notBool ("largest" in_keys(REST)) andBool notBool ("digit_total" in_keys(REST)) andBool notBool ("$cells" in_keys(REST)) andBool notBool ("$cells" in_keys( ("largest" \|-> N) ("digit_total" \|-> A) REST)) // The list-loop invariant includes the fixed suffix of the function. On // completion it returns to the caller, so temporary locals are unobservable.` |
| 1157 | `spec.k:73` | claim |  | `claim [scan-loop]: <k> #loop(list(asVals(IS:IntList)), Name("number"), #scanBody) ~> While(#digitCond, #digitBody) ~> Return(Name("digit_total")) ~> #endcall => digitSum(largestPrime(IS, CUR)) ~> CONT:K </k> <env> S:Int => CALLER:Int </env> <scopes> BASE:Map S \|-> scope( ("largest" \|-> CUR:Int) ("number" \|-> OLDN:Int) ("divisor" \|-> OLDD:Int) ("prime" \|-> OLDB:Bool) ("digit_total" \|-> 0) REST:Map, parent(0)) => BASE </scopes> <scopeLoc> S +Int 1 => S </scopeLoc> <stack> ListItem(frame(CONT, CALLER, S)) STACK:List => STACK </stack> <ret> noRet </ret> requires CUR >=Int 0 andBool notBool ("largest" in_keys(REST)) andBool notBool ("number" in_keys(REST)) andBool notBool ("divisor" in_keys(REST)) andBool notBool ("prime" in_keys(REST)) andBool notBool ("digit_total" in_keys(REST)) andBool notBool ("$cells" in_keys(REST)) andBool notBool ("$cells" in_keys( ("largest" \|-> CUR) ("number" \|-> OLDN) ("divisor" \|-> OLDD) ("prime" \|-> OLDB) ("digit_total" \|-> 0) REST)) andBool notBool (S in_keys(BASE)) // Function-call theorem. The bounded entry prefix reaches scan-loop; the // proven scan-loop invariant then discharges the unbounded computation.` |
| 1158 | `spec.k:118` | claim |  | `claim [entry-prefix]: <k> #applyK( toCall(closureVal( ("lst", .ParamNames), #functionBody, 0)), (list(asVals(IS:IntList)), .Vals)) => digitSum(largestPrime(IS, 0)) </k> <env> 0 </env> <scopes> MOD:Map </scopes> <scopeLoc> 1 </scopeLoc> <stack> .List </stack> <ret> noRet </ret> requires notBool (1 in_keys(MOD)) // End-to-end theorem: the translated function, loaded into the supplied // Python semantics, returns the digit sum of the largest prime in any // integer list (or zero when no prime exists).` |
| 1159 | `spec.k:138` | claim |  | `claim [main-correct]: <k> #loadAll(solutionModule) ~> Call(Name("skjkasdkd"), (list(asVals(IS:IntList)), .Exprs)) => digitSum(largestPrime(IS, 0)) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope => 0 \|-> scope( "skjkasdkd" \|-> closureVal( ("lst", .ParamNames), #functionBody, 0), parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code>` |
| 1160 | `spec.k:164` | endmodule |  | `endmodule` |

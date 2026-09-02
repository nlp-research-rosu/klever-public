# Exhaustive K declaration and rule inventory

Generated from the independently copied, integrity-checked supplied semantics plus the submitted `verification.k` and `spec.k`.

- Source files: 26
- Inventory entries: 946
- Kinds: `{'claim': 2, 'configuration': 1, 'context': 5, 'rule': 707, 'syntax': 231}`
- Classes: `{'claim declaration': 2, 'concrete-only equation': 50, 'configuration declaration': 1, 'context declaration': 5, 'opaque symbol declaration': 22, 'ordinary rule/equation': 599, 'priority semantic rule': 52, 'simplification rule': 6, 'syntax declaration': 209}`
- Slice tags: `{'fixed/outside theorem slice': 751, 'fixed/used theorem slice': 177, 'proof-local/claim': 18}`

| # | Source | Line | Kind/class | Slice | Declaration or rule |
|---:|---|---:|---|---|---|
| 1 | `semantics/assert.k` | 6 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| 2 | `semantics/assert.k` | 8 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| 3 | `semantics/assert.k` | 13 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 4 | `semantics/bool.k` | 8 | ordinary rule/equation | fixed/outside theorem slice | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 5 | `semantics/bool.k` | 10 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 6 | `semantics/bool.k` | 11 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 // ==== BoolOp: short-circuit, value-returning and / or ===================== // the node is its own accumulator: heat the HEAD element only, then either return i...` |
| 7 | `semantics/bool.k` | 16 | context declaration | fixed/outside theorem slice | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 8 | `semantics/bool.k` | 17 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 9 | `semantics/bool.k` | 18 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| 10 | `semantics/bool.k` | 20 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| 11 | `semantics/bool.k` | 22 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| 12 | `semantics/bool.k` | 24 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the // operand — and/or ret...` |
| 13 | `semantics/bool.k` | 29 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| 14 | `semantics/bool.k` | 31 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 15 | `semantics/bool.k` | 35 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 16 | `semantics/bool.k` | 39 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 17 | `semantics/bool.k` | 43 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 18 | `semantics/builtins.k` | 17 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Val ::= applyBuiltin(String, Vals) [function] // ==== len(obj) — O(1) per kind ============================================` |
| 19 | `semantics/builtins.k` | 20 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Int ::= seqLen(Val) [function]` |
| 20 | `semantics/builtins.k` | 21 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 21 | `semantics/builtins.k` | 22 | ordinary rule/equation | fixed/used theorem slice | `rule seqLen(list(VS:ValSeq)) => vsLen(VS)` |
| 22 | `semantics/builtins.k` | 23 | ordinary rule/equation | fixed/used theorem slice | `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)` |
| 23 | `semantics/builtins.k` | 24 | ordinary rule/equation | fixed/used theorem slice | `rule seqLen(str(IS:IntSeq)) => isLen(IS)` |
| 24 | `semantics/builtins.k` | 25 | ordinary rule/equation | fixed/used theorem slice | `rule seqLen(setV(DS:IntSeq)) => isLen(DS)` |
| 25 | `semantics/builtins.k` | 26 | ordinary rule/equation | fixed/used theorem slice | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) == // Minimal: the "copy a sequence" case (list of a list is itself;...` |
| 26 | `semantics/builtins.k` | 32 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 27 | `semantics/builtins.k` | 33 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 28 | `semantics/builtins.k` | 34 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>` |
| 29 | `semantics/builtins.k` | 35 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>` |
| 30 | `semantics/builtins.k` | 36 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 31 | `semantics/builtins.k` | 37 | ordinary rule/equation | fixed/outside theorem slice | `rule charsOf(.IntSeq) => .ValSeq` |
| 32 | `semantics/builtins.k` | 38 | ordinary rule/equation | fixed/outside theorem slice | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) // ==== set(str) — distinct character codes =================================` |
| 33 | `semantics/builtins.k` | 41 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) // ==== abs(int) ============================================================` |
| 34 | `semantics/builtins.k` | 44 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==` |
| 35 | `semantics/builtins.k` | 47 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 36 | `semantics/builtins.k` | 48 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 37 | `semantics/builtins.k` | 49 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 38 | `semantics/builtins.k` | 50 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| 39 | `semantics/builtins.k` | 54 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Int ::= intOf(Val) [function]` |
| 40 | `semantics/builtins.k` | 55 | ordinary rule/equation | fixed/outside theorem slice | `rule intOf(I:Int) => I` |
| 41 | `semantics/builtins.k` | 56 | ordinary rule/equation | fixed/outside theorem slice | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi // ==== all / any (short-circuiting #iterNext folds) ========================` |
| 42 | `semantics/builtins.k` | 59 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 43 | `semantics/builtins.k` | 60 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 44 | `semantics/builtins.k` | 61 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 45 | `semantics/builtins.k` | 62 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| 46 | `semantics/builtins.k` | 64 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| 47 | `semantics/builtins.k` | 67 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 48 | `semantics/builtins.k` | 68 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 49 | `semantics/builtins.k` | 69 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 50 | `semantics/builtins.k` | 70 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| 51 | `semantics/builtins.k` | 72 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) // ==== max / min over an iterable (#iterNext folds; first element seeds) ====` |
| 52 | `semantics/builtins.k` | 76 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 53 | `semantics/builtins.k` | 77 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 54 | `semantics/builtins.k` | 78 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 55 | `semantics/builtins.k` | 80 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 56 | `semantics/builtins.k` | 81 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 57 | `semantics/builtins.k` | 82 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 58 | `semantics/builtins.k` | 86 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 59 | `semantics/builtins.k` | 87 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 60 | `semantics/builtins.k` | 88 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 61 | `semantics/builtins.k` | 90 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 62 | `semantics/builtins.k` | 91 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 63 | `semantics/builtins.k` | 92 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) // ==== variadic max / min (a Vals fold) ====================================` |
| 64 | `semantics/builtins.k` | 97 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 65 | `semantics/builtins.k` | 98 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 66 | `semantics/builtins.k` | 99 | ordinary rule/equation | fixed/outside theorem slice | `rule maxVals(M:Int, .Vals) => M` |
| 67 | `semantics/builtins.k` | 100 | ordinary rule/equation | fixed/outside theorem slice | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| 68 | `semantics/builtins.k` | 102 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Int ::= minVals(Int, Vals) [function]` |
| 69 | `semantics/builtins.k` | 103 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 70 | `semantics/builtins.k` | 104 | ordinary rule/equation | fixed/outside theorem slice | `rule minVals(M:Int, .Vals) => M` |
| 71 | `semantics/builtins.k` | 105 | ordinary rule/equation | fixed/outside theorem slice | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==` |
| 72 | `semantics/builtins.k` | 108 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 // negative operand: the '-' sign prefixes the magnitude's digits` |
| 73 | `semantics/builtins.k` | 111 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| 74 | `semantics/builtins.k` | 114 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 75 | `semantics/builtins.k` | 115 | ordinary rule/equation | fixed/outside theorem slice | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 76 | `semantics/builtins.k` | 116 | ordinary rule/equation | fixed/outside theorem slice | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 77 | `semantics/builtins.k` | 117 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 78 | `semantics/builtins.k` | 118 | ordinary rule/equation | fixed/outside theorem slice | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 79 | `semantics/builtins.k` | 119 | ordinary rule/equation | fixed/outside theorem slice | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========` |
| 80 | `semantics/builtins.k` | 124 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| 81 | `semantics/builtins.k` | 126 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 82 | `semantics/builtins.k` | 127 | ordinary rule/equation | fixed/outside theorem slice | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 83 | `semantics/builtins.k` | 128 | ordinary rule/equation | fixed/outside theorem slice | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) // ==== map(str, xs) — eager (only the str case is in the subset) =============` |
| 84 | `semantics/builtins.k` | 132 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| 85 | `semantics/builtins.k` | 134 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 86 | `semantics/builtins.k` | 135 | ordinary rule/equation | fixed/outside theorem slice | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 87 | `semantics/builtins.k` | 136 | ordinary rule/equation | fixed/outside theorem slice | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 88 | `semantics/builtins.k` | 137 | ordinary rule/equation | fixed/outside theorem slice | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) // ==== int(x) identities (int(round(x)) composes through) ====================` |
| 89 | `semantics/builtins.k` | 140 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("int", I:Int, .Vals) => I // ==== ord / chr ===========================================================` |
| 90 | `semantics/builtins.k` | 143 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 91 | `semantics/builtins.k` | 144 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 // ==== str(int) / str(str) =================================================` |
| 92 | `semantics/builtins.k` | 148 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))` |
| 93 | `semantics/builtins.k` | 149 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====` |
| 94 | `semantics/builtins.k` | 152 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)` |
| 95 | `semantics/builtins.k` | 156 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| 96 | `semantics/builtins.k` | 158 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 97 | `semantics/builtins.k` | 159 | ordinary rule/equation | fixed/outside theorem slice | `rule intDigAcc(.IntSeq, ACC:Int) => ACC` |
| 98 | `semantics/builtins.k` | 160 | ordinary rule/equation | fixed/outside theorem slice | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====` |
| 99 | `semantics/builtins.k` | 163 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 100 | `semantics/builtins.k` | 164 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B) // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)` |
| 101 | `semantics/builtins.k` | 167 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| 102 | `semantics/builtins.k` | 169 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>` |
| 103 | `semantics/builtins.k` | 170 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 104 | `semantics/builtins.k` | 171 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| 105 | `semantics/builtins.k` | 173 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>` |
| 106 | `semantics/builtins.k` | 174 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> // ==== range(stop) / range(start, stop) / range(start, stop, step) =========` |
| 107 | `semantics/builtins.k` | 177 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)` |
| 108 | `semantics/builtins.k` | 178 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)` |
| 109 | `semantics/builtins.k` | 179 | concrete-only equation; attrs=concrete | fixed/used theorem slice | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ======== // Python precedence: ** right-assoc, the...` |
| 110 | `semantics/builtins.k` | 187 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 111 | `semantics/builtins.k` | 188 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Int ::= evalArith(IntSeq) [function]` |
| 112 | `semantics/builtins.k` | 189 | ordinary rule/equation | fixed/outside theorem slice | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| 113 | `semantics/builtins.k` | 192 | syntax declaration | fixed/outside theorem slice | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| 114 | `semantics/builtins.k` | 194 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= evDigit(Int) [function, total]` |
| 115 | `semantics/builtins.k` | 195 | ordinary rule/equation | fixed/outside theorem slice | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 116 | `semantics/builtins.k` | 196 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 117 | `semantics/builtins.k` | 197 | ordinary rule/equation | fixed/outside theorem slice | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 118 | `semantics/builtins.k` | 198 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule evHead42(_:IntSeq) => false [owise]` |
| 119 | `semantics/builtins.k` | 199 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 120 | `semantics/builtins.k` | 200 | ordinary rule/equation | fixed/outside theorem slice | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 121 | `semantics/builtins.k` | 201 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule evHead47(_:IntSeq) => false [owise]` |
| 122 | `semantics/builtins.k` | 203 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 123 | `semantics/builtins.k` | 204 | ordinary rule/equation | fixed/outside theorem slice | `rule tokOps(.IntSeq) => .OpSeq` |
| 124 | `semantics/builtins.k` | 205 | ordinary rule/equation | fixed/outside theorem slice | `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)` |
| 125 | `semantics/builtins.k` | 206 | ordinary rule/equation | fixed/outside theorem slice | `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)` |
| 126 | `semantics/builtins.k` | 207 | ordinary rule/equation | fixed/outside theorem slice | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 127 | `semantics/builtins.k` | 208 | ordinary rule/equation | fixed/outside theorem slice | `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 128 | `semantics/builtins.k` | 209 | ordinary rule/equation | fixed/outside theorem slice | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 129 | `semantics/builtins.k` | 210 | ordinary rule/equation | fixed/outside theorem slice | `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 130 | `semantics/builtins.k` | 211 | ordinary rule/equation | fixed/outside theorem slice | `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))` |
| 131 | `semantics/builtins.k` | 212 | ordinary rule/equation | fixed/outside theorem slice | `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))` |
| 132 | `semantics/builtins.k` | 214 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| 133 | `semantics/builtins.k` | 216 | ordinary rule/equation | fixed/outside theorem slice | `rule tokNds(.IntSeq) => .IntSeq` |
| 134 | `semantics/builtins.k` | 217 | ordinary rule/equation | fixed/outside theorem slice | `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)` |
| 135 | `semantics/builtins.k` | 218 | ordinary rule/equation | fixed/outside theorem slice | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 136 | `semantics/builtins.k` | 219 | ordinary rule/equation | fixed/outside theorem slice | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| 137 | `semantics/builtins.k` | 221 | ordinary rule/equation | fixed/outside theorem slice | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| 138 | `semantics/builtins.k` | 223 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 139 | `semantics/builtins.k` | 225 | syntax declaration | fixed/outside theorem slice | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 140 | `semantics/builtins.k` | 226 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 141 | `semantics/builtins.k` | 227 | ordinary rule/equation | fixed/outside theorem slice | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 142 | `semantics/builtins.k` | 228 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 143 | `semantics/builtins.k` | 230 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 144 | `semantics/builtins.k` | 231 | ordinary rule/equation | fixed/outside theorem slice | `rule applyOpE("+", A:Int, B:Int) => A +Int B` |
| 145 | `semantics/builtins.k` | 232 | ordinary rule/equation | fixed/outside theorem slice | `rule applyOpE("-", A:Int, B:Int) => A -Int B` |
| 146 | `semantics/builtins.k` | 233 | ordinary rule/equation | fixed/outside theorem slice | `rule applyOpE("*", A:Int, B:Int) => A *Int B` |
| 147 | `semantics/builtins.k` | 234 | ordinary rule/equation | fixed/outside theorem slice | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 148 | `semantics/builtins.k` | 235 | ordinary rule/equation | fixed/outside theorem slice | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 149 | `semantics/builtins.k` | 236 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 150 | `semantics/builtins.k` | 238 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 151 | `semantics/builtins.k` | 239 | ordinary rule/equation | fixed/outside theorem slice | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 152 | `semantics/builtins.k` | 240 | ordinary rule/equation | fixed/outside theorem slice | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 153 | `semantics/builtins.k` | 241 | ordinary rule/equation | fixed/outside theorem slice | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| 154 | `semantics/builtins.k` | 243 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 155 | `semantics/builtins.k` | 244 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 156 | `semantics/builtins.k` | 245 | ordinary rule/equation | fixed/outside theorem slice | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 157 | `semantics/builtins.k` | 246 | ordinary rule/equation | fixed/outside theorem slice | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 158 | `semantics/builtins.k` | 247 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 159 | `semantics/builtins.k` | 248 | ordinary rule/equation | fixed/outside theorem slice | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 160 | `semantics/builtins.k` | 250 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 161 | `semantics/builtins.k` | 251 | ordinary rule/equation | fixed/outside theorem slice | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 162 | `semantics/builtins.k` | 252 | ordinary rule/equation | fixed/outside theorem slice | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 163 | `semantics/builtins.k` | 253 | ordinary rule/equation | fixed/outside theorem slice | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 164 | `semantics/builtins.k` | 254 | ordinary rule/equation | fixed/outside theorem slice | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 165 | `semantics/builtins.k` | 255 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 166 | `semantics/builtins.k` | 256 | ordinary rule/equation | fixed/outside theorem slice | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 167 | `semantics/builtins.k` | 257 | ordinary rule/equation | fixed/outside theorem slice | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| 168 | `semantics/builtins.k` | 260 | ordinary rule/equation | fixed/outside theorem slice | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| 169 | `semantics/builtins.k` | 263 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| 170 | `semantics/builtins.k` | 265 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 171 | `semantics/builtins.k` | 266 | ordinary rule/equation | fixed/outside theorem slice | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 172 | `semantics/builtins.k` | 267 | ordinary rule/equation | fixed/outside theorem slice | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 173 | `semantics/builtins.k` | 268 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule inLevelE(_:String, _:String) => false [owise]` |
| 174 | `semantics/builtins.k` | 269 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 175 | `semantics/builtins.k` | 270 | ordinary rule/equation | fixed/outside theorem slice | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 176 | `semantics/builtins.k` | 271 | ordinary rule/equation | fixed/outside theorem slice | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 177 | `semantics/builtins.k` | 272 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 178 | `semantics/builtins.k` | 273 | ordinary rule/equation | fixed/outside theorem slice | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 179 | `semantics/builtins.k` | 274 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ================== // The md5 value itself is a named shared trust (sortVS-style, n...` |
| 180 | `semantics/builtins.k` | 279 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= "#md5"` |
| 181 | `semantics/builtins.k` | 280 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| 182 | `semantics/builtins.k` | 282 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 183 | `semantics/builtins.k` | 283 | syntax declaration | fixed/outside theorem slice | `syntax Val ::= md5Obj(IntSeq)` |
| 184 | `semantics/builtins.k` | 284 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 185 | `semantics/builtins.k` | 285 | opaque symbol declaration; attrs=function,total,concrete,owise,symbol,no-evaluators | fixed/outside theorem slice | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] // ==== isinstance(V, int\|str) — an ordinary 2-arg builtin =================== // The type argument (int/str) is an ordinary...` |
| 186 | `semantics/builtins.k` | 291 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 187 | `semantics/builtins.k` | 292 | ordinary rule/equation | fixed/used theorem slice | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 188 | `semantics/builtins.k` | 293 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 189 | `semantics/builtins.k` | 294 | ordinary rule/equation | fixed/outside theorem slice | `rule isIntV(_:Int) => true` |
| 190 | `semantics/builtins.k` | 295 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule isIntV(_:Val) => false [owise]` |
| 191 | `semantics/builtins.k` | 296 | ordinary rule/equation | fixed/outside theorem slice | `rule isStrV(str(_:IntSeq)) => true` |
| 192 | `semantics/builtins.k` | 297 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule isStrV(_:Val) => false [owise]` |
| 193 | `semantics/call.k` | 16 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)` |
| 194 | `semantics/call.k` | 19 | syntax declaration | fixed/used theorem slice | `syntax KItem ::= #callee(Exprs)` |
| 195 | `semantics/call.k` | 20 | ordinary rule/equation; attrs=owise | fixed/used theorem slice | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 196 | `semantics/call.k` | 21 | ordinary rule/equation | fixed/used theorem slice | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> // ==== dispatch on the callee value ========================================` |
| 197 | `semantics/call.k` | 24 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 198 | `semantics/call.k` | 26 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 199 | `semantics/call.k` | 27 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>` |
| 200 | `semantics/call.k` | 28 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>` |
| 201 | `semantics/call.k` | 29 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>` |
| 202 | `semantics/call.k` | 30 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>` |
| 203 | `semantics/call.k` | 31 | ordinary rule/equation; attrs=owise | fixed/used theorem slice | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 204 | `semantics/call.k` | 32 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k> // ==== heap-object arguments/receivers ===================================== // Builtins and type calls READ structure — deref the ...` |
| 205 | `semantics/call.k` | 38 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 206 | `semantics/call.k` | 42 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| 207 | `semantics/call.k` | 47 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 208 | `semantics/call.k` | 52 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 209 | `semantics/call.k` | 53 | ordinary rule/equation | fixed/outside theorem slice | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| 210 | `semantics/call.k` | 56 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] // non-mut...` |
| 211 | `semantics/call.k` | 63 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBo...` |
| 212 | `semantics/call.k` | 69 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.M...` |
| 213 | `semantics/call.k` | 80 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> ST...` |
| 214 | `semantics/call.k` | 87 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #allocCells(ParamNames)` |
| 215 | `semantics/call.k` | 88 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 216 | `semantics/call.k` | 89 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N \|-> cellV(noneV)) H </heap>...` |
| 217 | `semantics/comprehension.k` | 11 | ordinary rule/equation | fixed/outside theorem slice | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 218 | `semantics/comprehension.k` | 12 | ordinary rule/equation | fixed/outside theorem slice | `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 219 | `semantics/comprehension.k` | 14 | syntax declaration; attrs=macro | fixed/outside theorem slice | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 220 | `semantics/comprehension.k` | 15 | ordinary rule/equation | fixed/outside theorem slice | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| 221 | `semantics/comprehension.k` | 18 | syntax declaration; attrs=macro | fixed/outside theorem slice | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 222 | `semantics/comprehension.k` | 19 | ordinary rule/equation | fixed/outside theorem slice | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| 223 | `semantics/comprehension.k` | 21 | ordinary rule/equation | fixed/outside theorem slice | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| 224 | `semantics/comprehension.k` | 24 | syntax declaration; attrs=macro | fixed/outside theorem slice | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 225 | `semantics/comprehension.k` | 25 | ordinary rule/equation | fixed/outside theorem slice | `rule compGuard(.Exprs) => Bool(true)` |
| 226 | `semantics/comprehension.k` | 26 | ordinary rule/equation | fixed/outside theorem slice | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| 227 | `semantics/concrete.k` | 13 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 228 | `semantics/concrete.k` | 16 | priority semantic rule; attrs=priority,concrete | fixed/outside theorem slice | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) // ==== keyed sort, concrete leg =====================...` |
| 229 | `semantics/concrete.k` | 25 | syntax declaration | fixed/outside theorem slice | `syntax Val ::= kvP(Val, Val)` |
| 230 | `semantics/concrete.k` | 26 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| 231 | `semantics/concrete.k` | 28 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| 232 | `semantics/concrete.k` | 31 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| 233 | `semantics/concrete.k` | 34 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| 234 | `semantics/concrete.k` | 36 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| 235 | `semantics/concrete.k` | 38 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| 236 | `semantics/concrete.k` | 42 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 237 | `semantics/concrete.k` | 43 | ordinary rule/equation | fixed/outside theorem slice | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 238 | `semantics/concrete.k` | 44 | ordinary rule/equation | fixed/outside theorem slice | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| 239 | `semantics/concrete.k` | 47 | ordinary rule/equation | fixed/outside theorem slice | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| 240 | `semantics/concrete.k` | 51 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Bool ::= kLt(Val, Val) [function]` |
| 241 | `semantics/concrete.k` | 52 | ordinary rule/equation | fixed/outside theorem slice | `rule kLt(I1:Int, I2:Int) => I1 <Int I2` |
| 242 | `semantics/concrete.k` | 53 | ordinary rule/equation | fixed/outside theorem slice | `rule kLt(F1:Float, F2:Float) => F1 <Float F2` |
| 243 | `semantics/concrete.k` | 54 | ordinary rule/equation | fixed/outside theorem slice | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 244 | `semantics/concrete.k` | 56 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 245 | `semantics/concrete.k` | 57 | ordinary rule/equation | fixed/outside theorem slice | `rule unpairVS(.ValSeq) => .ValSeq` |
| 246 | `semantics/concrete.k` | 58 | ordinary rule/equation | fixed/outside theorem slice | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 247 | `semantics/concrete.k` | 59 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| 248 | `semantics/controls.k` | 9 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 249 | `semantics/controls.k` | 12 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Va...` |
| 250 | `semantics/controls.k` | 20 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) // `lst += [..]...` |
| 251 | `semantics/controls.k` | 27 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:...` |
| 252 | `semantics/controls.k` | 35 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 253 | `semantics/controls.k` | 36 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 254 | `semantics/controls.k` | 37 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #bindImports(ParamNames)` |
| 255 | `semantics/controls.k` | 38 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 256 | `semantics/controls.k` | 39 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==Strin...` |
| 257 | `semantics/controls.k` | 43 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") // ==== Expr statement: evaluate for effect, discard the value =============...` |
| 258 | `semantics/controls.k` | 48 | ordinary rule/equation | fixed/used theorem slice | `rule <k> Expr(_:Val) => .K ... </k> // ==== If (condition evaluated by strictness) ==============================` |
| 259 | `semantics/controls.k` | 51 | syntax declaration | fixed/used theorem slice | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 260 | `semantics/controls.k` | 52 | ordinary rule/equation | fixed/used theorem slice | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 261 | `semantics/controls.k` | 53 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>` |
| 262 | `semantics/controls.k` | 54 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> // ==== IfExp: ternary T if C else E ========================================` |
| 263 | `semantics/controls.k` | 57 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| 264 | `semantics/controls.k` | 59 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) // ==== For: one loop, in-cell continuation, over #iterNext ================= // (the iterable is evaluated once, by strictness; the proto...` |
| 265 | `semantics/controls.k` | 65 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| 266 | `semantics/controls.k` | 69 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 267 | `semantics/controls.k` | 71 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 268 | `semantics/controls.k` | 72 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 269 | `semantics/controls.k` | 73 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> // ==== While ==============================================================` |
| 270 | `semantics/controls.k` | 77 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 271 | `semantics/controls.k` | 78 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 272 | `semantics/controls.k` | 79 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| 273 | `semantics/controls.k` | 81 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) // ==== loop control (break / continue) =====================================` |
| 274 | `semantics/controls.k` | 85 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 275 | `semantics/controls.k` | 86 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Continue => #cont ... </k>` |
| 276 | `semantics/controls.k` | 87 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Break => #brk ... </k>` |
| 277 | `semantics/controls.k` | 88 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 278 | `semantics/controls.k` | 89 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 279 | `semantics/controls.k` | 90 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 280 | `semantics/controls.k` | 91 | priority semantic rule; attrs=priority,owise | fixed/outside theorem slice | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] // ==== heap-object deref at the truthiness/iteration consumers ============== // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)` |
| 281 | `semantics/controls.k` | 95 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 282 | `semantics/controls.k` | 98 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 283 | `semantics/controls.k` | 101 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // For derefs its iterable ONCE at loop start (iteration is over the snapshot; //...` |
| 284 | `semantics/controls.k` | 106 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 285 | `semantics/core.k` | 13 | syntax declaration | fixed/used theorem slice | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 286 | `semantics/core.k` | 14 | syntax declaration | fixed/outside theorem slice | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 287 | `semantics/core.k` | 15 | syntax declaration | fixed/used theorem slice | `syntax Str ::= str(IntSeq) // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)` |
| 288 | `semantics/core.k` | 18 | syntax declaration | fixed/outside theorem slice | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| 289 | `semantics/core.k` | 25 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Val ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) // a heap object: <heap> holds its list(VS) \| cellRef(Int) // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String)...` |
| 290 | `semantics/core.k` | 36 | syntax declaration | fixed/used theorem slice | `syntax Parent ::= "root" \| parent(Int)` |
| 291 | `semantics/core.k` | 37 | syntax declaration | fixed/used theorem slice | `syntax Scope ::= scope(Map, Parent)` |
| 292 | `semantics/core.k` | 38 | syntax declaration | fixed/used theorem slice | `syntax KResult ::= Val` |
| 293 | `semantics/core.k` | 39 | syntax declaration | fixed/used theorem slice | `syntax Expr ::= Val // cooling puts results back into expression holes` |
| 294 | `semantics/core.k` | 40 | syntax declaration | fixed/used theorem slice | `syntax Vals ::= List{Val, ","}` |
| 295 | `semantics/core.k` | 41 | syntax declaration | fixed/used theorem slice | `syntax Exc ::= "NoExc" \| "AssertionError"` |
| 296 | `semantics/core.k` | 42 | syntax declaration | fixed/used theorem slice | `syntax RetState ::= "noRet" \| retV(Val) // ==== configuration ======================================================= // The builtins namespace is a real scope at reserved location -1 (the bottom of every // chain; s...` |
| 297 | `semantics/core.k` | 49 | configuration declaration | fixed/used theorem slice | `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </s...` |
| 298 | `semantics/core.k` | 68 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= isRefV(Val) [function, total]` |
| 299 | `semantics/core.k` | 69 | ordinary rule/equation | fixed/outside theorem slice | `rule isRefV(ref(_:Int)) => true` |
| 300 | `semantics/core.k` | 70 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule isRefV(_:Val) => false [owise] // closure cells (Python-faithful capture): the heap holds cellV(V); a // cellRef surfacing as the k-redex reads through (lookup is the only use — // cellRefs never escape to user-v...` |
| 301 | `semantics/core.k` | 75 | syntax declaration | fixed/outside theorem slice | `syntax HeapVal ::= cellV(Val)` |
| 302 | `semantics/core.k` | 76 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 303 | `semantics/core.k` | 77 | ordinary rule/equation | fixed/outside theorem slice | `rule isCellRef(cellRef(_:Int)) => true` |
| 304 | `semantics/core.k` | 78 | ordinary rule/equation; attrs=function,owise | fixed/used theorem slice | `rule isCellRef(_:Val) => false [owise] // k-top deref for cell-bound reads surfacing INSIDE the annotated frame // (AugAssign's in-place read and friends). The "$cells" guard keeps this // DECIDABLY inapplicable in pl...` |
| 305 | `semantics/core.k` | 85 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] // write through a cell...` |
| 306 | `semantics/core.k` | 95 | syntax declaration | fixed/used theorem slice | `syntax Val ::= kwV(String, Val)` |
| 307 | `semantics/core.k` | 96 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #kwTag(String)` |
| 308 | `semantics/core.k` | 97 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 309 | `semantics/core.k` | 98 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| 310 | `semantics/core.k` | 100 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= isKwV(Val) [function, total]` |
| 311 | `semantics/core.k` | 101 | ordinary rule/equation | fixed/outside theorem slice | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 312 | `semantics/core.k` | 102 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule isKwV(_:Val) => false [owise] // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch // decides by pnMember even over an abstract frame rest (no prover branching)` |
| 313 | `semantics/core.k` | 106 | syntax declaration | fixed/used theorem slice | `syntax Val ::= cellsMark(ParamNames)` |
| 314 | `semantics/core.k` | 107 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 315 | `semantics/core.k` | 108 | ordinary rule/equation | fixed/outside theorem slice | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 316 | `semantics/core.k` | 109 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 317 | `semantics/core.k` | 110 | ordinary rule/equation | fixed/outside theorem slice | `rule pnMember(_:String, .ParamNames) => false` |
| 318 | `semantics/core.k` | 111 | ordinary rule/equation | fixed/outside theorem slice | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 319 | `semantics/core.k` | 113 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #cellW(Val, Val)` |
| 320 | `semantics/core.k` | 114 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| 321 | `semantics/core.k` | 117 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #alloc(Val)` |
| 322 | `semantics/core.k` | 118 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) // ==== module load + statement sequencing ==========================...` |
| 323 | `semantics/core.k` | 124 | syntax declaration | fixed/used theorem slice | `syntax KItem ::= #loadAll(Module)` |
| 324 | `semantics/core.k` | 125 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 325 | `semantics/core.k` | 126 | ordinary rule/equation | fixed/used theorem slice | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 326 | `semantics/core.k` | 127 | ordinary rule/equation | fixed/used theorem slice | `rule <k> .Stmts => .K ... </k> // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====` |
| 327 | `semantics/core.k` | 130 | syntax declaration | fixed/used theorem slice | `syntax KItem ::= #look(String, Int)` |
| 328 | `semantics/core.k` | 131 | ordinary rule/equation | fixed/used theorem slice | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 329 | `semantics/core.k` | 132 | priority semantic rule; attrs=function,priority,concrete | fixed/used theorem slice | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE // LOOKUP (h...` |
| 330 | `semantics/core.k` | 145 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, c...` |
| 331 | `semantics/core.k` | 152 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) // the ONE predefined builtins scope (the -1 frame; claims write `-...` |
| 332 | `semantics/core.k` | 157 | syntax declaration; attrs=function,total | fixed/used theorem slice | `syntax Scope ::= "builtinsScope" [function, total]` |
| 333 | `semantics/core.k` | 158 | ordinary rule/equation | fixed/used theorem slice | `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <-...` |
| 334 | `semantics/core.k` | 185 | syntax declaration | fixed/outside theorem slice | `syntax ApplyK ::= toCall(Val)` |
| 335 | `semantics/core.k` | 186 | syntax declaration | fixed/used theorem slice | `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| 336 | `semantics/core.k` | 189 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 337 | `semantics/core.k` | 190 | ordinary rule/equation | fixed/used theorem slice | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 338 | `semantics/core.k` | 191 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> // ==== Int / Bool / None literals ==========================================` |
| 339 | `semantics/core.k` | 194 | ordinary rule/equation | fixed/used theorem slice | `rule <k> Int(I:Int) => I ... </k>` |
| 340 | `semantics/core.k` | 195 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Bool(B:Bool) => B ... </k>` |
| 341 | `semantics/core.k` | 196 | ordinary rule/equation | fixed/used theorem slice | `rule <k> NoneVal => noneV ... </k> // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================` |
| 342 | `semantics/core.k` | 199 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Bool ::= truthy(Val) [function]` |
| 343 | `semantics/core.k` | 200 | ordinary rule/equation | fixed/used theorem slice | `rule truthy(B:Bool) => B` |
| 344 | `semantics/core.k` | 201 | ordinary rule/equation | fixed/used theorem slice | `rule truthy(noneV) => false` |
| 345 | `semantics/core.k` | 202 | ordinary rule/equation | fixed/used theorem slice | `rule truthy(I:Int) => I =/=Int 0` |
| 346 | `semantics/core.k` | 203 | ordinary rule/equation | fixed/used theorem slice | `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)` |
| 347 | `semantics/core.k` | 204 | ordinary rule/equation | fixed/used theorem slice | `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 348 | `semantics/core.k` | 205 | ordinary rule/equation | fixed/used theorem slice | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) // ==== extensible operator dispatch (cases added by the construct modules) ==` |
| 349 | `semantics/core.k` | 208 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Val ::= applyUn(String, Val) [function]` |
| 350 | `semantics/core.k` | 209 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Val ::= applyBin(String, Val, Val) [function]` |
| 351 | `semantics/core.k` | 210 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Bool ::= applyCmp(String, Val, Val) [function] // ==== shared list helpers =================================================` |
| 352 | `semantics/core.k` | 213 | syntax declaration; attrs=function,total | fixed/used theorem slice | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 353 | `semantics/core.k` | 214 | ordinary rule/equation | fixed/used theorem slice | `rule appendVal(.Vals, V:Val) => V , .Vals` |
| 354 | `semantics/core.k` | 215 | ordinary rule/equation | fixed/used theorem slice | `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)` |
| 355 | `semantics/core.k` | 217 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 356 | `semantics/core.k` | 218 | ordinary rule/equation | fixed/outside theorem slice | `rule vals2valSeq(.Vals) => .ValSeq` |
| 357 | `semantics/core.k` | 219 | ordinary rule/equation | fixed/outside theorem slice | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) // ==== shared sequence length (len / summaries across many modules) ======== // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)` |
| 358 | `semantics/core.k` | 223 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 359 | `semantics/core.k` | 224 | ordinary rule/equation | fixed/outside theorem slice | `rule vsLen(.ValSeq) => 0` |
| 360 | `semantics/core.k` | 225 | ordinary rule/equation | fixed/outside theorem slice | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 361 | `semantics/core.k` | 227 | syntax declaration; attrs=function,total | fixed/used theorem slice | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 362 | `semantics/core.k` | 228 | ordinary rule/equation | fixed/used theorem slice | `rule isLen(.IntSeq) => 0` |
| 363 | `semantics/core.k` | 229 | ordinary rule/equation; attrs=total | fixed/used theorem slice | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecifie...` |
| 364 | `semantics/core.k` | 233 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 365 | `semantics/core.k` | 234 | ordinary rule/equation | fixed/outside theorem slice | `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq` |
| 366 | `semantics/core.k` | 235 | ordinary rule/equation | fixed/outside theorem slice | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)` |
| 367 | `semantics/core.k` | 236 | ordinary rule/equation | fixed/outside theorem slice | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| 368 | `semantics/core.k` | 238 | ordinary rule/equation | fixed/outside theorem slice | `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0` |
| 369 | `semantics/dict.k` | 20 | syntax declaration | fixed/outside theorem slice | `syntax Val ::= dictV(ValSeq, ValSeq) // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.` |
| 370 | `semantics/dict.k` | 23 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| 371 | `semantics/dict.k` | 26 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 372 | `semantics/dict.k` | 27 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 373 | `semantics/dict.k` | 28 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| 374 | `semantics/dict.k` | 30 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| 375 | `semantics/dict.k` | 32 | concrete-only equation; attrs=total,concrete | fixed/outside theorem slice | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so bui...` |
| 376 | `semantics/dict.k` | 37 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 377 | `semantics/dict.k` | 38 | ordinary rule/equation | fixed/outside theorem slice | `rule dHasKey(.ValSeq, _:Val) => false` |
| 378 | `semantics/dict.k` | 39 | ordinary rule/equation | fixed/outside theorem slice | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K` |
| 379 | `semantics/dict.k` | 40 | ordinary rule/equation | fixed/outside theorem slice | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) // dPutK: KS unchanged if K already present, else append K (keep-first-position).` |
| 380 | `semantics/dict.k` | 43 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 381 | `semantics/dict.k` | 44 | ordinary rule/equation | fixed/outside theorem slice | `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)` |
| 382 | `semantics/dict.k` | 45 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The // [owise] catch-a...` |
| 383 | `semantics/dict.k` | 49 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 384 | `semantics/dict.k` | 50 | ordinary rule/equation | fixed/outside theorem slice | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K` |
| 385 | `semantics/dict.k` | 52 | ordinary rule/equation | fixed/outside theorem slice | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| 386 | `semantics/dict.k` | 54 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] // ==== dict methods ======================================================== // d.keys() -> a FRESH list object of the o...` |
| 387 | `semantics/dict.k` | 58 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==` |
| 388 | `semantics/dict.k` | 63 | ordinary rule/equation | fixed/outside theorem slice | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 389 | `semantics/dict.k` | 64 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 390 | `semantics/dict.k` | 65 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] // ==== dict subscript-assign: d[k] = v (insert/update in place) ============= // Only for a LOCAL dict v...` |
| 391 | `semantics/dict.k` | 70 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 392 | `semantics/dict.k` | 71 | ordinary rule/equation | fixed/outside theorem slice | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope // value: a bare dict updates in the ...` |
| 393 | `semantics/dict.k` | 76 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #dsetK(String, Val)` |
| 394 | `semantics/dict.k` | 77 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 395 | `semantics/dict.k` | 78 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({...` |
| 396 | `semantics/dict.k` | 82 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| 397 | `semantics/dict.k` | 86 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 398 | `semantics/dict.k` | 87 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> // negative-index normalization local to the write (subscript.k's is n...` |
| 399 | `semantics/dict.k` | 90 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 400 | `semantics/dict.k` | 91 | ordinary rule/equation | fixed/outside theorem slice | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 401 | `semantics/dict.k` | 92 | ordinary rule/equation | fixed/outside theorem slice | `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0 // ==== dict == (order-insensitive: same size + same key->value pairs) =======` |
| 402 | `semantics/dict.k` | 95 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| 403 | `semantics/dict.k` | 97 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 404 | `semantics/dict.k` | 98 | ordinary rule/equation | fixed/outside theorem slice | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 405 | `semantics/dict.k` | 99 | ordinary rule/equation | fixed/outside theorem slice | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| 406 | `semantics/dict.k` | 101 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 407 | `semantics/dict.k` | 102 | ordinary rule/equation | fixed/outside theorem slice | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K` |
| 408 | `semantics/dict.k` | 103 | ordinary rule/equation | fixed/outside theorem slice | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| 409 | `semantics/float.k` | 20 | syntax declaration | fixed/outside theorem slice | `syntax Val ::= Float` |
| 410 | `semantics/float.k` | 21 | concrete-only equation; attrs=concrete,no-evaluators | fixed/outside theorem slice | `rule <k> Float(F:Float) => F ... </k> // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.` |
| 411 | `semantics/float.k` | 24 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 412 | `semantics/float.k` | 25 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 413 | `semantics/float.k` | 27 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.` |
| 414 | `semantics/float.k` | 30 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 415 | `semantics/float.k` | 31 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 416 | `semantics/float.k` | 32 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K...` |
| 417 | `semantics/float.k` | 37 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 418 | `semantics/float.k` | 38 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 419 | `semantics/float.k` | 39 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on // concrete floats. kprove proofs return floats structurally ...` |
| 420 | `semantics/float.k` | 43 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 421 | `semantics/float.k` | 44 | concrete-only equation; attrs=concrete,no-evaluators | fixed/outside theorem slice | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an // uninterpreted Bool a proof case-splits on — a SINGL...` |
| 422 | `semantics/float.k` | 50 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 423 | `semantics/float.k` | 51 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 424 | `semantics/float.k` | 52 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 425 | `semantics/float.k` | 54 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 426 | `semantics/float.k` | 55 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 427 | `semantics/float.k` | 56 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F) // ==== math.ceil =========================================================== // `import X` is a no-op (we intercept the specific math functions syntactically; `math...` |
| 428 | `semantics/float.k` | 61 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Import(_:String) => .K ... </k> // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher // priority than the generic Attribute/method dispatch in call.k).` |
| 429 | `semantics/float.k` | 65 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= "#mathCeil"` |
| 430 | `semantics/float.k` | 66 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 431 | `semantics/float.k` | 67 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> // math.floor(x) — same interception shape as math.ceil` |
| 432 | `semantics/float.k` | 70 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= "#mathFloor"` |
| 433 | `semantics/float.k` | 71 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 434 | `semantics/float.k` | 72 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 435 | `semantics/float.k` | 73 | syntax declaration; attrs=function,total,symbol | fixed/outside theorem slice | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 436 | `semantics/float.k` | 74 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule floorFI(I:Int) => I [concrete]` |
| 437 | `semantics/float.k` | 75 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] // bare floor/ceil (bound by `from math import floor, ceil`)` |
| 438 | `semantics/float.k` | 78 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 439 | `semantics/float.k` | 79 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V) // math.pow(x, y) — a two-arg interception onto powF (ints promote)` |
| 440 | `semantics/float.k` | 82 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 441 | `semantics/float.k` | 83 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 442 | `semantics/float.k` | 84 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 443 | `semantics/float.k` | 85 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 444 | `semantics/float.k` | 86 | syntax declaration; attrs=function,total,symbol | fixed/outside theorem slice | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 445 | `semantics/float.k` | 87 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule toF(F:Float) => F [concrete]` |
| 446 | `semantics/float.k` | 88 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule toF(I:Int) => intToF(I) [concrete] // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for kru...` |
| 447 | `semantics/float.k` | 93 | syntax declaration; attrs=function,total,symbol | fixed/outside theorem slice | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 448 | `semantics/float.k` | 94 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule ceilF(I:Int) => I [concrete]` |
| 449 | `semantics/float.k` | 95 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun; // proofs use symbolic elements, never a float literal.` |
| 450 | `semantics/float.k` | 99 | concrete-only equation; attrs=concrete,no-evaluators | fixed/outside theorem slice | `rule applyUn("-", F:Float) => 0.0 -Float F // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjo...` |
| 451 | `semantics/float.k` | 103 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 452 | `semantics/float.k` | 104 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 453 | `semantics/float.k` | 105 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 454 | `semantics/float.k` | 107 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 455 | `semantics/float.k` | 108 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 456 | `semantics/float.k` | 109 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 457 | `semantics/float.k` | 111 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 458 | `semantics/float.k` | 112 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 459 | `semantics/float.k` | 113 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 460 | `semantics/float.k` | 115 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 461 | `semantics/float.k` | 116 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 462 | `semantics/float.k` | 117 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 463 | `semantics/float.k` | 119 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 464 | `semantics/float.k` | 120 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 465 | `semantics/float.k` | 121 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) // ---- the remaining comparisons (gtF promoted from find_zero — its summaries // case-split on the atom; >= / <= derive from the two opaque compares) ----` |
| 466 | `semantics/float.k` | 125 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 467 | `semantics/float.k` | 126 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 468 | `semantics/float.k` | 127 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)` |
| 469 | `semantics/float.k` | 128 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 470 | `semantics/float.k` | 129 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----` |
| 471 | `semantics/float.k` | 132 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 472 | `semantics/float.k` | 133 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 473 | `semantics/float.k` | 134 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 474 | `semantics/float.k` | 135 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 475 | `semantics/float.k` | 136 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 476 | `semantics/float.k` | 137 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 477 | `semantics/float.k` | 138 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 478 | `semantics/float.k` | 139 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----` |
| 479 | `semantics/float.k` | 142 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 480 | `semantics/float.k` | 143 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 481 | `semantics/float.k` | 144 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 482 | `semantics/float.k` | 145 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 483 | `semantics/float.k` | 146 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 484 | `semantics/float.k` | 147 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 485 | `semantics/float.k` | 148 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 486 | `semantics/float.k` | 149 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 487 | `semantics/float.k` | 150 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 488 | `semantics/float.k` | 151 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- x == None (promoted from 137; `is` cases live in operators.k) ----` |
| 489 | `semantics/float.k` | 154 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 490 | `semantics/float.k` | 155 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) // ---- float(str): decimal parse (promoted from 137's defined chain) ---- // digits '.' digits, optional leading '-'; concrete evaluation only (the // symbol...` |
| 491 | `semantics/float.k` | 160 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 492 | `semantics/float.k` | 161 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 493 | `semantics/float.k` | 162 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| 494 | `semantics/float.k` | 165 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Int ::= headIS(IntSeq) [function]` |
| 495 | `semantics/float.k` | 166 | ordinary rule/equation | fixed/outside theorem slice | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 496 | `semantics/float.k` | 167 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 497 | `semantics/float.k` | 168 | ordinary rule/equation | fixed/outside theorem slice | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 498 | `semantics/float.k` | 169 | ordinary rule/equation | fixed/outside theorem slice | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 499 | `semantics/float.k` | 170 | ordinary rule/equation | fixed/outside theorem slice | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 500 | `semantics/float.k` | 171 | ordinary rule/equation | fixed/outside theorem slice | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| 501 | `semantics/float.k` | 173 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 502 | `semantics/float.k` | 174 | ordinary rule/equation | fixed/outside theorem slice | `rule fracPart(.IntSeq) => 0` |
| 503 | `semantics/float.k` | 175 | ordinary rule/equation | fixed/outside theorem slice | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 504 | `semantics/float.k` | 176 | ordinary rule/equation | fixed/outside theorem slice | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 505 | `semantics/float.k` | 177 | ordinary rule/equation | fixed/outside theorem slice | `rule fracAcc(.IntSeq, A:Int) => A` |
| 506 | `semantics/float.k` | 178 | ordinary rule/equation | fixed/outside theorem slice | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 507 | `semantics/float.k` | 179 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 508 | `semantics/float.k` | 180 | ordinary rule/equation | fixed/outside theorem slice | `rule fracScale(.IntSeq) => 1` |
| 509 | `semantics/float.k` | 181 | ordinary rule/equation | fixed/outside theorem slice | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 510 | `semantics/float.k` | 182 | ordinary rule/equation | fixed/outside theorem slice | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 511 | `semantics/float.k` | 183 | ordinary rule/equation | fixed/outside theorem slice | `rule fscAcc(.IntSeq, A:Int) => A` |
| 512 | `semantics/float.k` | 184 | ordinary rule/equation | fixed/outside theorem slice | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 513 | `semantics/float.k` | 185 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 514 | `semantics/float.k` | 186 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 515 | `semantics/float.k` | 187 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("float", F:Float, .Vals) => F // ---- float / int division (promoted from mean_absolute_deviation) ----` |
| 516 | `semantics/float.k` | 190 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 517 | `semantics/float.k` | 191 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 518 | `semantics/float.k` | 192 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) // ---- int -> float promotion for the remaining mixed arithmetic/compares ----` |
| 519 | `semantics/float.k` | 195 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 520 | `semantics/float.k` | 196 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 521 | `semantics/float.k` | 197 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 522 | `semantics/float.k` | 198 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 523 | `semantics/float.k` | 199 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 524 | `semantics/float.k` | 200 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 525 | `semantics/float.k` | 201 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 526 | `semantics/float.k` | 202 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 527 | `semantics/float.k` | 203 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 528 | `semantics/float.k` | 204 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 529 | `semantics/float.k` | 205 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 530 | `semantics/float.k` | 206 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----` |
| 531 | `semantics/float.k` | 209 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 532 | `semantics/float.k` | 210 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 533 | `semantics/float.k` | 211 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 534 | `semantics/float.k` | 213 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` |
| 535 | `semantics/float.k` | 214 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("float", F:Float, .Vals) => F // round: Python half-even (banker's); round(F, N) scales by 10^N` |
| 536 | `semantics/float.k` | 217 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 537 | `semantics/float.k` | 218 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float...` |
| 538 | `semantics/float.k` | 223 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 539 | `semantics/float.k` | 224 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| 540 | `semantics/float.k` | 227 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)` |
| 541 | `semantics/float.k` | 228 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 542 | `semantics/float.k` | 230 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 543 | `semantics/float.k` | 231 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 544 | `semantics/float.k` | 232 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= "#mathSqrt"` |
| 545 | `semantics/float.k` | 233 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 546 | `semantics/float.k` | 234 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 547 | `semantics/float.k` | 235 | priority semantic rule; attrs=priority,concrete | fixed/outside theorem slice | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which // seed/step with `requires isInt(V)`, so they are STUCK on fl...` |
| 548 | `semantics/float.k` | 243 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 549 | `semantics/float.k` | 244 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 550 | `semantics/float.k` | 245 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 551 | `semantics/float.k` | 246 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 552 | `semantics/float.k` | 247 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 553 | `semantics/float.k` | 250 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 554 | `semantics/float.k` | 251 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 555 | `semantics/float.k` | 252 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 556 | `semantics/float.k` | 253 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 557 | `semantics/float.k` | 254 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only sha...` |
| 558 | `semantics/float.k` | 261 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 559 | `semantics/float.k` | 262 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| 560 | `semantics/float.k` | 265 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 561 | `semantics/float.k` | 266 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 562 | `semantics/float.k` | 267 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| 563 | `semantics/float.k` | 270 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| 564 | `semantics/functions.k` | 8 | syntax declaration | fixed/used theorem slice | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall" // ==== def / anonymous closure =============================================` |
| 565 | `semantics/functions.k` | 14 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| 566 | `semantics/functions.k` | 18 | syntax declaration | fixed/outside theorem slice | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 567 | `semantics/functions.k` | 19 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> // ==== annotated def/lambda (closure cells; spec 2.3) ====================== // closureValC(params, cellvars, b...` |
| 568 | `semantics/functions.k` | 27 | syntax declaration | fixed/outside theorem slice | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) // capture: resolve each freevar to the enclosing frame's cellRef, then bind // (FuncDef) or yield (Lambda) the closure value.` |
| 569 | `semantics/functions.k` | 31 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 570 | `semantics/functions.k` | 33 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| 571 | `semantics/functions.k` | 36 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... ...` |
| 572 | `semantics/functions.k` | 42 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </...` |
| 573 | `semantics/functions.k` | 47 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| 574 | `semantics/functions.k` | 50 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| 575 | `semantics/functions.k` | 53 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:...` |
| 576 | `semantics/functions.k` | 59 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> // ==== bind params ========================================================` |
| 577 | `semantics/functions.k` | 63 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 578 | `semantics/functions.k` | 64 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes> // a param that is a cellvar was pre-bound t...` |
| 579 | `semantics/functions.k` | 68 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBo...` |
| 580 | `semantics/functions.k` | 78 | ordinary rule/equation | fixed/used theorem slice | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| 581 | `semantics/functions.k` | 80 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation // makes the saved loc the callee frame's own loc). Sound ...` |
| 582 | `semantics/functions.k` | 85 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes>...` |
| 583 | `semantics/int.k` | 7 | ordinary rule/equation | fixed/outside theorem slice | `rule applyUn("-", I:Int) => 0 -Int I` |
| 584 | `semantics/int.k` | 9 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2 // Bool participates in int arithmetic (x += (a == b))` |
| 585 | `semantics/int.k` | 11 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 586 | `semantics/int.k` | 12 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 587 | `semantics/int.k` | 13 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2` |
| 588 | `semantics/int.k` | 14 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2` |
| 589 | `semantics/int.k` | 15 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)` |
| 590 | `semantics/int.k` | 16 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 591 | `semantics/int.k` | 17 | ordinary rule/equation | fixed/outside theorem slice | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 592 | `semantics/int.k` | 19 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Int ::= pyMod(Int, Int) [function]` |
| 593 | `semantics/int.k` | 20 | ordinary rule/equation | fixed/outside theorem slice | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 594 | `semantics/int.k` | 22 | ordinary rule/equation | fixed/used theorem slice | `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` |
| 595 | `semantics/int.k` | 23 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2` |
| 596 | `semantics/int.k` | 24 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` |
| 597 | `semantics/int.k` | 25 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2` |
| 598 | `semantics/int.k` | 26 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2` |
| 599 | `semantics/int.k` | 27 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2` |
| 600 | `semantics/iter.k` | 8 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| 601 | `semantics/list.k` | 9 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>` |
| 602 | `semantics/list.k` | 10 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> // ==== ListExpr: [...] literal -> a fresh heap object =======================` |
| 603 | `semantics/list.k` | 13 | syntax declaration | fixed/outside theorem slice | `syntax ApplyK ::= "toList"` |
| 604 | `semantics/list.k` | 14 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 605 | `semantics/list.k` | 15 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> // ==== list ops: + / == / != ===============================================` |
| 606 | `semantics/list.k` | 18 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 607 | `semantics/list.k` | 19 | ordinary rule/equation | fixed/outside theorem slice | `rule valSeqConcat(.ValSeq, T:ValSeq) => T` |
| 608 | `semantics/list.k` | 20 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) // list + list constructs a NEW object (k-cell — it allocates; operands land here // already deref'd). priority(45) beats the generic...` |
| 609 | `semantics/list.k` | 24 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| 610 | `semantics/list.k` | 27 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 611 | `semantics/list.k` | 28 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) // ==== deep equality when elements are heap objects (list-of-lists) ======== // Python == is structural at every depth. Fires ONLY when a ref i...` |
| 612 | `semantics/list.k` | 33 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 613 | `semantics/list.k` | 34 | ordinary rule/equation | fixed/outside theorem slice | `rule hasRefVS(.ValSeq) => false` |
| 614 | `semantics/list.k` | 35 | ordinary rule/equation | fixed/outside theorem slice | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 615 | `semantics/list.k` | 37 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map) [function]` |
| 616 | `semantics/list.k` | 39 | ordinary rule/equation | fixed/outside theorem slice | `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true` |
| 617 | `semantics/list.k` | 40 | ordinary rule/equation | fixed/outside theorem slice | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false` |
| 618 | `semantics/list.k` | 41 | ordinary rule/equation | fixed/outside theorem slice | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false` |
| 619 | `semantics/list.k` | 42 | ordinary rule/equation | fixed/outside theorem slice | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| 620 | `semantics/list.k` | 45 | ordinary rule/equation | fixed/outside theorem slice | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| 621 | `semantics/list.k` | 47 | ordinary rule/equation | fixed/outside theorem slice | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| 622 | `semantics/list.k` | 49 | ordinary rule/equation | fixed/outside theorem slice | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 623 | `semantics/list.k` | 50 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] // ==== mutator: xs.append(v) — an in-place heap write ======================` |
| 624 | `semantics/list.k` | 53 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] // ==== `x in list` — ...` |
| 625 | `semantics/list.k` | 58 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 626 | `semantics/list.k` | 59 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 627 | `semantics/list.k` | 60 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 628 | `semantics/list.k` | 61 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 629 | `semantics/list.k` | 62 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 630 | `semantics/list.k` | 63 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| 631 | `semantics/list.k` | 65 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| 632 | `semantics/list.k` | 67 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| 633 | `semantics/methods.k` | 10 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Val ::= applyMethod(Val, String, Vals) [function] // ==== string predicates (Python semantics) =================================` |
| 634 | `semantics/methods.k` | 13 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 635 | `semantics/methods.k` | 14 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 636 | `semantics/methods.k` | 15 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 637 | `semantics/methods.k` | 16 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) // ==== case maps ============================================================` |
| 638 | `semantics/methods.k` | 19 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))` |
| 639 | `semantics/methods.k` | 20 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))` |
| 640 | `semantics/methods.k` | 21 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) // ==== join / count / strip / encode ======================================== // S.join(list-of-str): fold with separator codes (receiver + arg ...` |
| 641 | `semantics/methods.k` | 26 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 642 | `semantics/methods.k` | 27 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 643 | `semantics/methods.k` | 28 | ordinary rule/equation | fixed/outside theorem slice | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 644 | `semantics/methods.k` | 29 | ordinary rule/equation | fixed/outside theorem slice | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 645 | `semantics/methods.k` | 30 | ordinary rule/equation | fixed/outside theorem slice | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) // S.count(sub): non-overlapping window scan (Python str.count)` |
| 646 | `semantics/methods.k` | 34 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 647 | `semantics/methods.k` | 35 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 648 | `semantics/methods.k` | 36 | ordinary rule/equation | fixed/outside theorem slice | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 649 | `semantics/methods.k` | 37 | ordinary rule/equation | fixed/outside theorem slice | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| 650 | `semantics/methods.k` | 39 | ordinary rule/equation | fixed/outside theorem slice | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| 651 | `semantics/methods.k` | 41 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 652 | `semantics/methods.k` | 42 | ordinary rule/equation | fixed/outside theorem slice | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 653 | `semantics/methods.k` | 43 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 654 | `semantics/methods.k` | 44 | ordinary rule/equation | fixed/outside theorem slice | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 // S.strip(): trim whitespace runs from both ends` |
| 655 | `semantics/methods.k` | 47 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 656 | `semantics/methods.k` | 48 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 657 | `semantics/methods.k` | 49 | ordinary rule/equation | fixed/outside theorem slice | `rule trimWS(.IntSeq) => .IntSeq` |
| 658 | `semantics/methods.k` | 50 | ordinary rule/equation | fixed/outside theorem slice | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 659 | `semantics/methods.k` | 51 | ordinary rule/equation | fixed/outside theorem slice | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 660 | `semantics/methods.k` | 52 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 661 | `semantics/methods.k` | 53 | ordinary rule/equation | fixed/outside theorem slice | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 662 | `semantics/methods.k` | 54 | ordinary rule/equation | fixed/outside theorem slice | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 663 | `semantics/methods.k` | 55 | ordinary rule/equation | fixed/outside theorem slice | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) // S.encode('ascii'): identity on the code-sequence model (bytes == codes)` |
| 664 | `semantics/methods.k` | 58 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) // ==== prefix ===============================================================` |
| 665 | `semantics/methods.k` | 61 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========` |
| 666 | `semantics/methods.k` | 64 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 667 | `semantics/methods.k` | 65 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 668 | `semantics/methods.k` | 66 | ordinary rule/equation | fixed/outside theorem slice | `rule cntOccVS(.ValSeq, _:Val) => 0` |
| 669 | `semantics/methods.k` | 67 | ordinary rule/equation | fixed/outside theorem slice | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 670 | `semantics/methods.k` | 68 | ordinary rule/equation | fixed/outside theorem slice | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V) // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ========== // Concrete string ops for...` |
| 671 | `semantics/methods.k` | 72 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| 672 | `semantics/methods.k` | 75 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result` |
| 673 | `semantics/methods.k` | 76 | ordinary rule/equation | fixed/outside theorem slice | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 674 | `semantics/methods.k` | 77 | ordinary rule/equation | fixed/outside theorem slice | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| 675 | `semantics/methods.k` | 79 | ordinary rule/equation | fixed/outside theorem slice | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) // flush the current token to the result list iff non-empty.` |
| 676 | `semantics/methods.k` | 82 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 677 | `semantics/methods.k` | 83 | ordinary rule/equation | fixed/outside theorem slice | `rule flushTok(ACC:ValSeq, .IntSeq) => ACC` |
| 678 | `semantics/methods.k` | 84 | ordinary rule/equation | fixed/outside theorem slice | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 679 | `semantics/methods.k` | 85 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= isWSC(Int) [function, total]` |
| 680 | `semantics/methods.k` | 86 | ordinary rule/equation | fixed/outside theorem slice | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 // split(sep='x') keyword form delegates to the positional k-cell rule` |
| 681 | `semantics/methods.k` | 89 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] // str.split(sep) — singl...` |
| 682 | `semantics/methods.k` | 94 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| 683 | `semantics/methods.k` | 97 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token` |
| 684 | `semantics/methods.k` | 98 | ordinary rule/equation | fixed/outside theorem slice | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)` |
| 685 | `semantics/methods.k` | 99 | ordinary rule/equation | fixed/outside theorem slice | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| 686 | `semantics/methods.k` | 101 | ordinary rule/equation | fixed/outside theorem slice | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| 687 | `semantics/methods.k` | 104 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| 688 | `semantics/methods.k` | 106 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 689 | `semantics/methods.k` | 107 | ordinary rule/equation | fixed/outside theorem slice | `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq` |
| 690 | `semantics/methods.k` | 108 | ordinary rule/equation | fixed/outside theorem slice | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 691 | `semantics/methods.k` | 109 | ordinary rule/equation | fixed/outside theorem slice | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) // ==== char helpers =========================================================` |
| 692 | `semantics/methods.k` | 112 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 693 | `semantics/methods.k` | 113 | ordinary rule/equation | fixed/outside theorem slice | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 694 | `semantics/methods.k` | 115 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 695 | `semantics/methods.k` | 116 | ordinary rule/equation | fixed/outside theorem slice | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 696 | `semantics/methods.k` | 118 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 697 | `semantics/methods.k` | 119 | ordinary rule/equation | fixed/outside theorem slice | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 698 | `semantics/methods.k` | 121 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 699 | `semantics/methods.k` | 122 | ordinary rule/equation | fixed/outside theorem slice | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 700 | `semantics/methods.k` | 124 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 701 | `semantics/methods.k` | 125 | ordinary rule/equation | fixed/outside theorem slice | `rule hasUpper(.IntSeq) => false` |
| 702 | `semantics/methods.k` | 126 | ordinary rule/equation | fixed/outside theorem slice | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 703 | `semantics/methods.k` | 128 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 704 | `semantics/methods.k` | 129 | ordinary rule/equation | fixed/outside theorem slice | `rule hasLower(.IntSeq) => false` |
| 705 | `semantics/methods.k` | 130 | ordinary rule/equation | fixed/outside theorem slice | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 706 | `semantics/methods.k` | 132 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 707 | `semantics/methods.k` | 133 | ordinary rule/equation | fixed/outside theorem slice | `rule allAlpha(.IntSeq) => true` |
| 708 | `semantics/methods.k` | 134 | ordinary rule/equation | fixed/outside theorem slice | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 709 | `semantics/methods.k` | 136 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 710 | `semantics/methods.k` | 137 | ordinary rule/equation | fixed/outside theorem slice | `rule allDigit(.IntSeq) => true` |
| 711 | `semantics/methods.k` | 138 | ordinary rule/equation | fixed/outside theorem slice | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 712 | `semantics/methods.k` | 140 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= lowerC(Int) [function, total]` |
| 713 | `semantics/methods.k` | 142 | ordinary rule/equation | fixed/outside theorem slice | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 714 | `semantics/methods.k` | 143 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule lowerC(C:Int) => C [owise]` |
| 715 | `semantics/methods.k` | 145 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= upperC(Int) [function, total]` |
| 716 | `semantics/methods.k` | 146 | ordinary rule/equation | fixed/outside theorem slice | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 717 | `semantics/methods.k` | 147 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule upperC(C:Int) => C [owise]` |
| 718 | `semantics/methods.k` | 149 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Int ::= swapC(Int) [function, total]` |
| 719 | `semantics/methods.k` | 150 | ordinary rule/equation | fixed/outside theorem slice | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 720 | `semantics/methods.k` | 151 | ordinary rule/equation | fixed/outside theorem slice | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 721 | `semantics/methods.k` | 152 | ordinary rule/equation; attrs=owise | fixed/outside theorem slice | `rule swapC(C:Int) => C [owise]` |
| 722 | `semantics/methods.k` | 154 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 723 | `semantics/methods.k` | 155 | ordinary rule/equation | fixed/outside theorem slice | `rule mapLower(.IntSeq) => .IntSeq` |
| 724 | `semantics/methods.k` | 156 | ordinary rule/equation | fixed/outside theorem slice | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 725 | `semantics/methods.k` | 158 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 726 | `semantics/methods.k` | 159 | ordinary rule/equation | fixed/outside theorem slice | `rule mapUpper(.IntSeq) => .IntSeq` |
| 727 | `semantics/methods.k` | 160 | ordinary rule/equation | fixed/outside theorem slice | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 728 | `semantics/methods.k` | 162 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 729 | `semantics/methods.k` | 163 | ordinary rule/equation | fixed/outside theorem slice | `rule mapSwap(.IntSeq) => .IntSeq` |
| 730 | `semantics/methods.k` | 164 | ordinary rule/equation | fixed/outside theorem slice | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 731 | `semantics/methods.k` | 166 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 732 | `semantics/methods.k` | 167 | ordinary rule/equation | fixed/outside theorem slice | `rule startsWith(.IntSeq, _:IntSeq) => true` |
| 733 | `semantics/methods.k` | 168 | ordinary rule/equation | fixed/outside theorem slice | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 734 | `semantics/methods.k` | 169 | ordinary rule/equation | fixed/outside theorem slice | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| 735 | `semantics/operators.k` | 10 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 736 | `semantics/operators.k` | 12 | ordinary rule/equation | fixed/used theorem slice | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes` |
| 737 | `semantics/operators.k` | 15 | context declaration | fixed/used theorem slice | `context Compare(HOLE, _)` |
| 738 | `semantics/operators.k` | 16 | context declaration | fixed/used theorem slice | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 739 | `semantics/operators.k` | 17 | ordinary rule/equation; attrs=owise | fixed/used theorem slice | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 740 | `semantics/operators.k` | 19 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("is", V:Val, noneV) => V ==K noneV` |
| 741 | `semantics/operators.k` | 20 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) // ==== operand deref: heap objects combine/compare by STRUCTURE ============ // (Python: list == is structural; identity only via `is`.) priority(40) // ...` |
| 742 | `semantics/operators.k` | 25 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 743 | `semantics/operators.k` | 28 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] // the left operand of `in`/`not in` is an ELEMENT (compares by ==...` |
| 744 | `semantics/operators.k` | 34 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| 745 | `semantics/operators.k` | 38 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| 746 | `semantics/operators.k` | 44 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 747 | `semantics/range.k` | 9 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 748 | `semantics/range.k` | 10 | ordinary rule/equation | fixed/outside theorem slice | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 749 | `semantics/range.k` | 12 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 750 | `semantics/range.k` | 13 | ordinary rule/equation | fixed/outside theorem slice | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| 751 | `semantics/range.k` | 15 | ordinary rule/equation | fixed/outside theorem slice | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| 752 | `semantics/range.k` | 17 | ordinary rule/equation | fixed/outside theorem slice | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| 753 | `semantics/range.k` | 20 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| 754 | `semantics/range.k` | 23 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| 755 | `semantics/set.k` | 8 | syntax declaration | fixed/outside theorem slice | `syntax Val ::= setV(IntSeq) // membership of a code in the accumulated distinct-code sequence` |
| 756 | `semantics/set.k` | 11 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 757 | `semantics/set.k` | 12 | ordinary rule/equation | fixed/outside theorem slice | `rule codeIn(_:Int, .IntSeq) => false` |
| 758 | `semantics/set.k` | 13 | ordinary rule/equation | fixed/outside theorem slice | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) // the distinct codes of CS (insert-if-absent fold, first-seen order)` |
| 759 | `semantics/set.k` | 16 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] \| dedupFrom(IntSeq, IntSeq) [function, total]` |
| 760 | `semantics/set.k` | 18 | ordinary rule/equation | fixed/outside theorem slice | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 761 | `semantics/set.k` | 19 | ordinary rule/equation | fixed/outside theorem slice | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 762 | `semantics/set.k` | 20 | ordinary rule/equation | fixed/outside theorem slice | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| 763 | `semantics/set.k` | 22 | ordinary rule/equation | fixed/outside theorem slice | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| 764 | `semantics/set.k` | 25 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 765 | `semantics/set.k` | 26 | ordinary rule/equation | fixed/outside theorem slice | `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)` |
| 766 | `semantics/set.k` | 27 | ordinary rule/equation | fixed/outside theorem slice | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) // ==== set equality: two sets are equal iff mutually subsuming ============== // subsetCodes(A, B) — every code of A occurs in B (duplicates in...` |
| 767 | `semantics/set.k` | 31 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 768 | `semantics/set.k` | 32 | ordinary rule/equation | fixed/outside theorem slice | `rule subsetCodes(.IntSeq, _:IntSeq) => true` |
| 769 | `semantics/set.k` | 33 | ordinary rule/equation | fixed/outside theorem slice | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 770 | `semantics/set.k` | 35 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 771 | `semantics/set.k` | 36 | ordinary rule/equation | fixed/outside theorem slice | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) // set == set (the only comparison sets support here)` |
| 772 | `semantics/set.k` | 39 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| 773 | `semantics/sort.k` | 18 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 774 | `semantics/sort.k` | 19 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 775 | `semantics/sort.k` | 20 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule sortVS(.ValSeq) => .ValSeq [concrete]` |
| 776 | `semantics/sort.k` | 21 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 777 | `semantics/sort.k` | 22 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]` |
| 778 | `semantics/sort.k` | 23 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 779 | `semantics/sort.k` | 24 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete] // str elements insert by the shared lexicographic strLt (methods.k)` |
| 780 | `semantics/sort.k` | 26 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 781 | `semantics/sort.k` | 27 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 782 | `semantics/sort.k` | 28 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 783 | `semantics/sort.k` | 29 | concrete-only equation; attrs=concrete | fixed/outside theorem slice | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| 784 | `semantics/sort.k` | 31 | concrete-only equation; attrs=concrete,owise | fixed/outside theorem slice | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [ow...` |
| 785 | `semantics/sort.k` | 36 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> // mutator: xs.sort() — the in-place heap write over the same trusted sortVS` |
| 786 | `semantics/sort.k` | 40 | priority semantic rule; attrs=priority,concrete | fixed/outside theorem slice | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] // ==== keyed / reversed sorted() (WP2) ==================...` |
| 787 | `semantics/sort.k` | 49 | opaque symbol declaration; attrs=function,total,symbol,no-evaluators | fixed/outside theorem slice | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 788 | `semantics/sort.k` | 51 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| 789 | `semantics/sort.k` | 53 | ordinary rule/equation | fixed/outside theorem slice | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 790 | `semantics/sort.k` | 54 | ordinary rule/equation | fixed/outside theorem slice | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 791 | `semantics/sort.k` | 55 | ordinary rule/equation | fixed/outside theorem slice | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 792 | `semantics/sort.k` | 57 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 793 | `semantics/sort.k` | 58 | ordinary rule/equation | fixed/outside theorem slice | `rule condRev(S:ValSeq, false) => S` |
| 794 | `semantics/sort.k` | 59 | ordinary rule/equation | fixed/outside theorem slice | `rule condRev(S:ValSeq, true) => revVS(S)` |
| 795 | `semantics/sort.k` | 61 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| 796 | `semantics/sort.k` | 63 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| 797 | `semantics/sort.k` | 65 | concrete-only equation; attrs=total,concrete | fixed/outside theorem slice | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINE...` |
| 798 | `semantics/str.k` | 8 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>` |
| 799 | `semantics/str.k` | 9 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> // ==== str literal (ASCII-only) ============================================` |
| 800 | `semantics/str.k` | 13 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax IntSeq ::= strToCodes(String) [function]` |
| 801 | `semantics/str.k` | 14 | ordinary rule/equation | fixed/used theorem slice | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 802 | `semantics/str.k` | 15 | ordinary rule/equation | fixed/used theorem slice | `rule strToCodes("") => .IntSeq` |
| 803 | `semantics/str.k` | 16 | ordinary rule/equation | fixed/used theorem slice | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 // ==== operators: + / == / !...` |
| 804 | `semantics/str.k` | 20 | syntax declaration; attrs=function,total | fixed/used theorem slice | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 805 | `semantics/str.k` | 21 | ordinary rule/equation | fixed/used theorem slice | `rule seqConcat(.IntSeq, T:IntSeq) => T` |
| 806 | `semantics/str.k` | 22 | ordinary rule/equation | fixed/used theorem slice | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 807 | `semantics/str.k` | 24 | ordinary rule/equation | fixed/used theorem slice | `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 808 | `semantics/str.k` | 25 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 809 | `semantics/str.k` | 26 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) // substring membership: `P in X` iff the code-seq P occurs contiguously in X` |
| 810 | `semantics/str.k` | 29 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 811 | `semantics/str.k` | 30 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 812 | `semantics/str.k` | 32 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 813 | `semantics/str.k` | 33 | ordinary rule/equation | fixed/outside theorem slice | `rule strPrefix(.IntSeq, _:IntSeq) => true` |
| 814 | `semantics/str.k` | 34 | ordinary rule/equation | fixed/outside theorem slice | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 815 | `semantics/str.k` | 35 | ordinary rule/equation | fixed/outside theorem slice | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 816 | `semantics/str.k` | 37 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 817 | `semantics/str.k` | 38 | ordinary rule/equation | fixed/outside theorem slice | `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)` |
| 818 | `semantics/str.k` | 39 | ordinary rule/equation | fixed/outside theorem slice | `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)` |
| 819 | `semantics/str.k` | 40 | ordinary rule/equation | fixed/outside theorem slice | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code // model...` |
| 820 | `semantics/str.k` | 48 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 821 | `semantics/str.k` | 49 | ordinary rule/equation | fixed/outside theorem slice | `rule strLt(.IntSeq, .IntSeq) => false` |
| 822 | `semantics/str.k` | 50 | ordinary rule/equation | fixed/outside theorem slice | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 823 | `semantics/str.k` | 51 | ordinary rule/equation | fixed/outside theorem slice | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 824 | `semantics/str.k` | 52 | ordinary rule/equation | fixed/outside theorem slice | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B` |
| 825 | `semantics/str.k` | 53 | ordinary rule/equation | fixed/outside theorem slice | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B` |
| 826 | `semantics/str.k` | 54 | ordinary rule/equation | fixed/outside theorem slice | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 827 | `semantics/str.k` | 56 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 828 | `semantics/str.k` | 57 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 829 | `semantics/str.k` | 58 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 830 | `semantics/str.k` | 59 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| 831 | `semantics/subscript.k` | 11 | syntax declaration; attrs=function,total | fixed/outside theorem slice | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 832 | `semantics/subscript.k` | 12 | ordinary rule/equation | fixed/outside theorem slice | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V` |
| 833 | `semantics/subscript.k` | 13 | ordinary rule/equation | fixed/outside theorem slice | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| 834 | `semantics/subscript.k` | 16 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 835 | `semantics/subscript.k` | 17 | ordinary rule/equation | fixed/used theorem slice | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C` |
| 836 | `semantics/subscript.k` | 18 | ordinary rule/equation | fixed/used theorem slice | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| 837 | `semantics/subscript.k` | 21 | syntax declaration; attrs=function,total | fixed/used theorem slice | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 838 | `semantics/subscript.k` | 22 | ordinary rule/equation | fixed/used theorem slice | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` |
| 839 | `semantics/subscript.k` | 23 | ordinary rule/equation; attrs=strict | fixed/used theorem slice | `rule normIdx(I:Int, _:Int) => I requires I >=Int 0 // ==== Subscript: indexing obj[i] (list / tuple / str) ===================== // contexts (not strict attrs): the Index slot's Slice alternative must never heat` |
| 840 | `semantics/subscript.k` | 27 | context declaration | fixed/used theorem slice | `context Subscript(HOLE, _)` |
| 841 | `semantics/subscript.k` | 28 | context declaration | fixed/used theorem slice | `context Subscript(_:Val, HOLE:Expr) // heap-object deref (covers both the index and slice forms via the Index slot)` |
| 842 | `semantics/subscript.k` | 31 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 843 | `semantics/subscript.k` | 35 | ordinary rule/equation | fixed/used theorem slice | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 844 | `semantics/subscript.k` | 37 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 845 | `semantics/subscript.k` | 38 | ordinary rule/equation | fixed/used theorem slice | `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 846 | `semantics/subscript.k` | 39 | ordinary rule/equation | fixed/used theorem slice | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 847 | `semantics/subscript.k` | 40 | ordinary rule/equation | fixed/used theorem slice | `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========` |
| 848 | `semantics/subscript.k` | 44 | syntax declaration | fixed/used theorem slice | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| 849 | `semantics/subscript.k` | 49 | syntax declaration | fixed/outside theorem slice | `syntax OptInt ::= "noB" \| someB(Int)` |
| 850 | `semantics/subscript.k` | 50 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #evalB(NoBound) => noB ... </k>` |
| 851 | `semantics/subscript.k` | 51 | ordinary rule/equation | fixed/used theorem slice | `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>` |
| 852 | `semantics/subscript.k` | 52 | ordinary rule/equation | fixed/used theorem slice | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 853 | `semantics/subscript.k` | 54 | ordinary rule/equation | fixed/used theorem slice | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 854 | `semantics/subscript.k` | 55 | ordinary rule/equation | fixed/used theorem slice | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 855 | `semantics/subscript.k` | 56 | ordinary rule/equation | fixed/used theorem slice | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> // a list slice constructs a NEW object; a str slice stays a value` |
| 856 | `semantics/subscript.k` | 58 | priority semantic rule; attrs=priority | fixed/used theorem slice | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| 857 | `semantics/subscript.k` | 61 | ordinary rule/equation | fixed/used theorem slice | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 858 | `semantics/subscript.k` | 63 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 859 | `semantics/subscript.k` | 64 | ordinary rule/equation | fixed/used theorem slice | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 860 | `semantics/subscript.k` | 66 | ordinary rule/equation | fixed/used theorem slice | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 861 | `semantics/subscript.k` | 68 | ordinary rule/equation | fixed/used theorem slice | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) // ==== slice.indices: step / start / stop / clamp =================...` |
| 862 | `semantics/subscript.k` | 72 | syntax declaration; attrs=function,total | fixed/used theorem slice | `syntax Int ::= slStep(OptInt) [function, total]` |
| 863 | `semantics/subscript.k` | 73 | ordinary rule/equation | fixed/used theorem slice | `rule slStep(noB) => 1` |
| 864 | `semantics/subscript.k` | 74 | ordinary rule/equation | fixed/used theorem slice | `rule slStep(someB(S:Int)) => S` |
| 865 | `semantics/subscript.k` | 76 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 866 | `semantics/subscript.k` | 77 | ordinary rule/equation | fixed/used theorem slice | `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| 867 | `semantics/subscript.k` | 79 | ordinary rule/equation | fixed/used theorem slice | `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0` |
| 868 | `semantics/subscript.k` | 81 | ordinary rule/equation | fixed/used theorem slice | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 869 | `semantics/subscript.k` | 83 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 870 | `semantics/subscript.k` | 84 | ordinary rule/equation | fixed/used theorem slice | `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0` |
| 871 | `semantics/subscript.k` | 86 | ordinary rule/equation | fixed/used theorem slice | `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| 872 | `semantics/subscript.k` | 88 | ordinary rule/equation | fixed/used theorem slice | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` |
| 873 | `semantics/subscript.k` | 90 | syntax declaration; attrs=function,total | fixed/used theorem slice | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 874 | `semantics/subscript.k` | 91 | ordinary rule/equation | fixed/used theorem slice | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0` |
| 875 | `semantics/subscript.k` | 93 | ordinary rule/equation | fixed/used theorem slice | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| 876 | `semantics/subscript.k` | 96 | syntax declaration; attrs=function,total | fixed/used theorem slice | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 877 | `semantics/subscript.k` | 97 | ordinary rule/equation | fixed/used theorem slice | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| 878 | `semantics/subscript.k` | 99 | ordinary rule/equation | fixed/used theorem slice | `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| 879 | `semantics/subscript.k` | 102 | syntax declaration; attrs=function,total | fixed/used theorem slice | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 880 | `semantics/subscript.k` | 103 | ordinary rule/equation | fixed/used theorem slice | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN` |
| 881 | `semantics/subscript.k` | 105 | ordinary rule/equation | fixed/used theorem slice | `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN // ==== build the strided sub-sequence (indices in range by construction) ====` |
| 882 | `semantics/subscript.k` | 109 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 883 | `semantics/subscript.k` | 110 | ordinary rule/equation | fixed/outside theorem slice | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 884 | `semantics/subscript.k` | 113 | ordinary rule/equation | fixed/outside theorem slice | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 885 | `semantics/subscript.k` | 116 | syntax declaration; attrs=function | fixed/used theorem slice | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 886 | `semantics/subscript.k` | 117 | ordinary rule/equation | fixed/used theorem slice | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 887 | `semantics/subscript.k` | 120 | ordinary rule/equation | fixed/used theorem slice | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 888 | `semantics/syntax.k` | 9 | syntax declaration; attrs=macro,strict,seqstrict | fixed/used theorem slice | `syntax Expr ::= "Int" "(" Int ")" \| "Float" "(" Float ")" \| "Bool" "(" Bool ")" \| "Name" "(" String ")" \| "Str" "(" String ")" \| "UnaryOp" "(" String "," Expr ")" [strict(2)] \| "BinOp" "(" String "," Expr "," Ex...` |
| 889 | `semantics/syntax.k` | 32 | syntax declaration | fixed/used theorem slice | `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"` |
| 890 | `semantics/syntax.k` | 33 | syntax declaration | fixed/outside theorem slice | `syntax Entry ::= "Entry" "(" Expr "," Expr ")"` |
| 891 | `semantics/syntax.k` | 34 | syntax declaration | fixed/outside theorem slice | `syntax Entries ::= List{Entry, ","}` |
| 892 | `semantics/syntax.k` | 35 | syntax declaration | fixed/outside theorem slice | `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 893 | `semantics/syntax.k` | 36 | syntax declaration | fixed/outside theorem slice | `syntax CompFors ::= List{CompFor, ""}` |
| 894 | `semantics/syntax.k` | 37 | syntax declaration | fixed/used theorem slice | `syntax Exprs ::= List{Expr, ","}` |
| 895 | `semantics/syntax.k` | 38 | syntax declaration | fixed/used theorem slice | `syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 896 | `semantics/syntax.k` | 39 | syntax declaration | fixed/used theorem slice | `syntax Bound ::= Expr \| "NoBound"` |
| 897 | `semantics/syntax.k` | 41 | syntax declaration; attrs=strict | fixed/used theorem slice | `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] \| "Import" "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For" "(" Expr "," Exp...` |
| 898 | `semantics/syntax.k` | 56 | syntax declaration | fixed/used theorem slice | `syntax Stmts ::= List{Stmt, ""}` |
| 899 | `semantics/syntax.k` | 57 | syntax declaration | fixed/used theorem slice | `syntax Params ::= "Params" "(" ParamNames ")"` |
| 900 | `semantics/syntax.k` | 58 | syntax declaration | fixed/outside theorem slice | `syntax CellVars ::= "CellVars" "(" ParamNames ")"` |
| 901 | `semantics/syntax.k` | 59 | syntax declaration | fixed/outside theorem slice | `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"` |
| 902 | `semantics/syntax.k` | 60 | syntax declaration | fixed/used theorem slice | `syntax ParamNames ::= List{String, ","}` |
| 903 | `semantics/syntax.k` | 61 | syntax declaration | fixed/used theorem slice | `syntax Module ::= "Module" "(" Stmts ")"` |
| 904 | `semantics/tuple.k` | 10 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>` |
| 905 | `semantics/tuple.k` | 11 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================` |
| 906 | `semantics/tuple.k` | 14 | syntax declaration | fixed/outside theorem slice | `syntax ApplyK ::= "toTuple"` |
| 907 | `semantics/tuple.k` | 15 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 908 | `semantics/tuple.k` | 16 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 909 | `semantics/tuple.k` | 18 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B // membership routes through the same k-cell fold as lists (list.k)` |
| 910 | `semantics/tuple.k` | 20 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 911 | `semantics/tuple.k` | 21 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> // t.index(v): first index of v (ValueError out of subset)` |
| 912 | `semantics/tuple.k` | 23 | ordinary rule/equation | fixed/outside theorem slice | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 913 | `semantics/tuple.k` | 24 | syntax declaration; attrs=function | fixed/outside theorem slice | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 914 | `semantics/tuple.k` | 25 | ordinary rule/equation | fixed/outside theorem slice | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 915 | `semantics/tuple.k` | 26 | ordinary rule/equation | fixed/outside theorem slice | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| 916 | `semantics/tuple.k` | 28 | ordinary rule/equation | fixed/outside theorem slice | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) // ==== target binding: bind a Name or a TupleExpr target to a value ========` |
| 917 | `semantics/tuple.k` | 31 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 918 | `semantics/tuple.k` | 32 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 919 | `semantics/tuple.k` | 35 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>...` |
| 920 | `semantics/tuple.k` | 42 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 921 | `semantics/tuple.k` | 43 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 922 | `semantics/tuple.k` | 44 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] // ==== unpacking: a, b = <tuple\|list> (RHS evaluated by strictness) ========` |
| 923 | `semantics/tuple.k` | 49 | syntax declaration | fixed/outside theorem slice | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 924 | `semantics/tuple.k` | 50 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 925 | `semantics/tuple.k` | 51 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 926 | `semantics/tuple.k` | 52 | priority semantic rule; attrs=priority | fixed/outside theorem slice | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 927 | `semantics/tuple.k` | 55 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| 928 | `semantics/tuple.k` | 57 | ordinary rule/equation | fixed/outside theorem slice | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| 929 | `verification.k` | 7 | syntax declaration; attrs=macro | proof-local/claim | `syntax Stmts ::= "decodeBody" [macro]` |
| 930 | `verification.k` | 8 | ordinary rule/equation; attrs=function | proof-local/claim | `rule decodeBody => Expr( Str( "\n takes as input string encoded with encode_cyclic function. Returns decoded string.\n ")) If(Compare(Call(Name("len"), Name("s")), CmpOp("<", Int(3))), Return(Name("s")), .Stmts) Retur...` |
| 931 | `verification.k` | 26 | syntax declaration; attrs=macro | proof-local/claim | `syntax Val ::= "decodeClosure" [macro]` |
| 932 | `verification.k` | 27 | ordinary rule/equation | proof-local/claim | `rule decodeClosure => closureVal("s", decodeBody, 0) // Independent recursive specification: rotate every complete block of // three codes to the right, and preserve a final block of length < 3. // It is phrased with ...` |
| 933 | `verification.k` | 34 | syntax declaration; attrs=function,total | proof-local/claim | `syntax IntSeq ::= decodeCodes(IntSeq) [function, total]` |
| 934 | `verification.k` | 35 | ordinary rule/equation | proof-local/claim | `rule decodeCodes(CS:IntSeq) => CS requires isLen(CS) <Int 3` |
| 935 | `verification.k` | 37 | ordinary rule/equation | proof-local/claim | `rule decodeCodes(CS:IntSeq) => seqConcat( seqConcat( iCons(intSeqAt(CS, 2), .IntSeq), buildIS(CS, 0, 2, 1)), decodeCodes(buildIS(CS, 3, isLen(CS), 1))) requires isLen(CS) >=Int 3 // Symbolic slice-length lemma for s[3...` |
| 936 | `verification.k` | 47 | simplification rule; attrs=simplification | proof-local/claim | `rule isLen(buildIS(CS:IntSeq, clampHi(3, isLen(CS), 1), isLen(CS), 1)) => isLen(CS) -Int 3 requires isLen(CS) >=Int 3 [simplification]` |
| 937 | `verification.k` | 55 | simplification rule; attrs=simplification | proof-local/claim | `rule clampHi(3, isLen(CS:IntSeq), 1) => 3 requires isLen(CS) >=Int 3 [simplification] // Scope locations are allocated monotonically. keysBelow records the // corresponding invariant for the abstract remainder of a sc...` |
| 938 | `verification.k` | 61 | syntax declaration; attrs=function | proof-local/claim | `syntax Bool ::= keysBelow(Map, Int) [function]` |
| 939 | `verification.k` | 62 | ordinary rule/equation | proof-local/claim | `rule keysBelow(.Map, _N:Int) => true` |
| 940 | `verification.k` | 63 | ordinary rule/equation | proof-local/claim | `rule keysBelow((I:Int \|-> _S:Scope) REST:Map, N:Int) => (I <Int N) andBool keysBelow(REST, N)` |
| 941 | `verification.k` | 66 | simplification rule; attrs=simplification | proof-local/claim | `rule keysBelow(M:Map, N:Int +Int 1) => true requires keysBelow(M, N) [simplification]` |
| 942 | `verification.k` | 70 | simplification rule; attrs=simplification | proof-local/claim | `rule N:Int in_keys(M:Map) => false requires keysBelow(M, N) [simplification]` |
| 943 | `verification.k` | 74 | simplification rule; attrs=simplification | proof-local/claim | `rule (M:Map [ N:Int <- S:Scope ]) => (N \|-> S) M requires keysBelow(M, N) [simplification]` |
| 944 | `verification.k` | 78 | simplification rule; attrs=simplification | proof-local/claim | `rule (((N:Int \|-> _S:Scope) M:Map) [ N <- undef]) => M requires keysBelow(M, N) [simplification]` |
| 945 | `spec.k` | 8 | claim declaration | proof-local/claim | `claim <k> decodeBody ~> #endcall => #pop </k> <env> L </env> <scopes> 0 \|-> scope("decode_cyclic" \|-> decodeClosure, parent(-1)) L \|-> scope("s" \|-> str(CS), parent(0)) -1 \|-> builtinsScope SC:Map </scopes> <scop...` |
| 946 | `spec.k` | 30 | claim declaration | proof-local/claim | `claim <k> Call(Name("decode_cyclic"), (str(CS), .Exprs)) => str(decodeCodes(CS)) </k> <env> 0 </env> <scopes> 0 \|-> scope("decode_cyclic" \|-> decodeClosure, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 <...` |

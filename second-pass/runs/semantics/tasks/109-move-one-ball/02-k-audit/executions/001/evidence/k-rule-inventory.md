# Exhaustive K declaration and rule inventory

Generated from the fresh scratch source tree. Every top-level `configuration`, `syntax`, `context`, `rule`, and `claim` declaration is listed once.

## Module manifest

| File | Modules |
|---|---|
| `reference-semantics/semantics.k` | `MPY, MPY-KRUN` |
| `reference-semantics/semantics/assert.k` | `MPY-ASSERT` |
| `reference-semantics/semantics/bool.k` | `MPY-BOOL` |
| `reference-semantics/semantics/builtins.k` | `MPY-BUILTINS` |
| `reference-semantics/semantics/call.k` | `MPY-CALL` |
| `reference-semantics/semantics/comprehension.k` | `MPY-COMPREHENSION` |
| `reference-semantics/semantics/concrete.k` | `MPY-CONCRETE` |
| `reference-semantics/semantics/controls.k` | `MPY-CONTROLS` |
| `reference-semantics/semantics/core.k` | `MPY-CORE` |
| `reference-semantics/semantics/dict.k` | `MPY-DICT` |
| `reference-semantics/semantics/float.k` | `MPY-FLOAT` |
| `reference-semantics/semantics/functions.k` | `MPY-FUNCTIONS` |
| `reference-semantics/semantics/int.k` | `MPY-INT` |
| `reference-semantics/semantics/iter.k` | `MPY-ITER` |
| `reference-semantics/semantics/list.k` | `MPY-LIST` |
| `reference-semantics/semantics/methods.k` | `MPY-METHODS` |
| `reference-semantics/semantics/operators.k` | `MPY-OPERATORS` |
| `reference-semantics/semantics/range.k` | `MPY-RANGE` |
| `reference-semantics/semantics/set.k` | `MPY-SET` |
| `reference-semantics/semantics/sort.k` | `MPY-SORT` |
| `reference-semantics/semantics/str.k` | `MPY-STR` |
| `reference-semantics/semantics/subscript.k` | `MPY-SUBSCRIPT` |
| `reference-semantics/semantics/syntax.k` | `MPY-SYNTAX` |
| `reference-semantics/semantics/tuple.k` | `MPY-TUPLE` |
| `verification.k` | `VERIFICATION` |
| `spec.k` | `SPEC` |

## Counts

| File | Configuration | Syntax | Context | Rule | Claim | Total |
|---|---:|---:|---:|---:|---:|---:|
| `reference-semantics/semantics.k` | 0 | 0 | 0 | 0 | 0 | 0 |
| `reference-semantics/semantics/assert.k` | 0 | 0 | 0 | 3 | 0 | 3 |
| `reference-semantics/semantics/bool.k` | 0 | 0 | 1 | 13 | 0 | 14 |
| `reference-semantics/semantics/builtins.k` | 0 | 38 | 0 | 137 | 0 | 175 |
| `reference-semantics/semantics/call.k` | 0 | 3 | 0 | 21 | 0 | 24 |
| `reference-semantics/semantics/comprehension.k` | 0 | 3 | 0 | 7 | 0 | 10 |
| `reference-semantics/semantics/concrete.k` | 0 | 5 | 0 | 16 | 0 | 21 |
| `reference-semantics/semantics/controls.k` | 0 | 3 | 0 | 34 | 0 | 37 |
| `reference-semantics/semantics/core.k` | 1 | 37 | 0 | 46 | 0 | 84 |
| `reference-semantics/semantics/dict.k` | 0 | 12 | 0 | 28 | 0 | 40 |
| `reference-semantics/semantics/float.k` | 0 | 34 | 0 | 121 | 0 | 155 |
| `reference-semantics/semantics/functions.k` | 0 | 4 | 0 | 15 | 0 | 19 |
| `reference-semantics/semantics/int.k` | 0 | 1 | 0 | 16 | 0 | 17 |
| `reference-semantics/semantics/iter.k` | 0 | 1 | 0 | 0 | 0 | 1 |
| `reference-semantics/semantics/list.k` | 0 | 5 | 0 | 27 | 0 | 32 |
| `reference-semantics/semantics/methods.k` | 0 | 27 | 0 | 75 | 0 | 102 |
| `reference-semantics/semantics/operators.k` | 0 | 0 | 2 | 10 | 0 | 12 |
| `reference-semantics/semantics/range.k` | 0 | 2 | 0 | 6 | 0 | 8 |
| `reference-semantics/semantics/set.k` | 0 | 6 | 0 | 12 | 0 | 18 |
| `reference-semantics/semantics/sort.k` | 0 | 6 | 0 | 19 | 0 | 25 |
| `reference-semantics/semantics/str.k` | 0 | 5 | 0 | 28 | 0 | 33 |
| `reference-semantics/semantics/subscript.k` | 0 | 15 | 2 | 40 | 0 | 57 |
| `reference-semantics/semantics/syntax.k` | 0 | 16 | 0 | 0 | 0 | 16 |
| `reference-semantics/semantics/tuple.k` | 0 | 4 | 0 | 21 | 0 | 25 |
| `verification.k` | 0 | 9 | 0 | 22 | 0 | 31 |
| `spec.k` | 0 | 0 | 0 | 0 | 3 | 3 |
| **TOTAL** | 1 | 236 | 5 | 717 | 3 | 962 |

## Entries

| # | Source class | Location | Kind | Attributes | Declaration / rule |
|---:|---|---|---|---|---|
| 1 | supplied fixed semantics | `reference-semantics/semantics/assert.k:6-7` | rule | none | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| 2 | supplied fixed semantics | `reference-semantics/semantics/assert.k:8-12` | rule | none | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| 3 | supplied fixed semantics | `reference-semantics/semantics/assert.k:13-15` | rule | priority | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 4 | supplied fixed semantics | `reference-semantics/semantics/bool.k:8-9` | rule | none | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 5 | supplied fixed semantics | `reference-semantics/semantics/bool.k:10-10` | rule | none | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 6 | supplied fixed semantics | `reference-semantics/semantics/bool.k:11-15` | rule | none | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| 7 | supplied fixed semantics | `reference-semantics/semantics/bool.k:16-16` | context | none | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 8 | supplied fixed semantics | `reference-semantics/semantics/bool.k:17-17` | rule | none | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 9 | supplied fixed semantics | `reference-semantics/semantics/bool.k:18-19` | rule | none | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| 10 | supplied fixed semantics | `reference-semantics/semantics/bool.k:20-21` | rule | none | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| 11 | supplied fixed semantics | `reference-semantics/semantics/bool.k:22-23` | rule | none | `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| 12 | supplied fixed semantics | `reference-semantics/semantics/bool.k:24-28` | rule | none | `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` |
| 13 | supplied fixed semantics | `reference-semantics/semantics/bool.k:29-30` | rule | priority | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| 14 | supplied fixed semantics | `reference-semantics/semantics/bool.k:31-34` | rule | priority | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 15 | supplied fixed semantics | `reference-semantics/semantics/bool.k:35-38` | rule | priority | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 16 | supplied fixed semantics | `reference-semantics/semantics/bool.k:39-42` | rule | priority | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 17 | supplied fixed semantics | `reference-semantics/semantics/bool.k:43-46` | rule | priority | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 18 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:17-19` | syntax | function | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| 19 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:20-20` | syntax | function | `syntax Int ::= seqLen(Val) [function]` |
| 20 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:21-21` | rule | none | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 21 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:22-22` | rule | none | `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)` |
| 22 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:23-23` | rule | none | `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)` |
| 23 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:24-24` | rule | none | `rule seqLen(str(IS:IntSeq))                   => isLen(IS)` |
| 24 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:25-25` | rule | none | `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)` |
| 25 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:26-31` | rule | none | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| 26 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:32-32` | rule | none | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>` |
| 27 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:33-33` | rule | none | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 28 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:34-34` | rule | none | `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>` |
| 29 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:35-35` | rule | none | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>` |
| 30 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:36-36` | syntax | function, total | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 31 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:37-37` | rule | none | `rule charsOf(.IntSeq)                => .ValSeq` |
| 32 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:38-40` | rule | none | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| 33 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:41-43` | rule | none | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| 34 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:44-46` | rule | none | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| 35 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:47-47` | syntax | none | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 36 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:48-48` | rule | none | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 37 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:49-49` | rule | none | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 38 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:50-53` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| 39 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:54-54` | syntax | function | `syntax Int ::= intOf(Val) [function]` |
| 40 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:55-55` | rule | none | `rule intOf(I:Int)  => I` |
| 41 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:56-58` | rule | none | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| 42 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:59-59` | syntax | none | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 43 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:60-60` | rule | none | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 44 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:61-61` | rule | none | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 45 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:62-63` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| 46 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:64-66` | rule | none | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| 47 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:67-67` | syntax | none | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 48 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:68-68` | rule | none | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 49 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:69-69` | rule | none | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 50 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:70-71` | rule | none | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| 51 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:72-75` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` |
| 52 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:76-76` | syntax | none | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 53 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:77-77` | rule | none | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 54 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:78-79` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 55 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:80-80` | rule | none | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 56 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:81-81` | rule | none | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 57 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:82-85` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 58 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:86-86` | syntax | none | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 59 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:87-87` | rule | none | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 60 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:88-89` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 61 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:90-90` | rule | none | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 62 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:91-91` | rule | none | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 63 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:92-96` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 64 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:97-97` | syntax | function | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 65 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:98-98` | rule | none | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 66 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:99-99` | rule | none | `rule maxVals(M:Int, .Vals)           => M` |
| 67 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:100-101` | rule | none | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| 68 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:102-102` | syntax | function | `syntax Int ::= minVals(Int, Vals) [function]` |
| 69 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:103-103` | rule | none | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 70 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:104-104` | rule | none | `rule minVals(M:Int, .Vals)           => M` |
| 71 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:105-107` | rule | none | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| 72 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:108-110` | rule | none | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` |
| 73 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:111-113` | rule | none | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| 74 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:114-114` | syntax | function, total | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 75 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:115-115` | rule | none | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 76 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:116-116` | rule | none | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 77 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:117-117` | syntax | function, total | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 78 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:118-118` | rule | none | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 79 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:119-123` | rule | none | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` |
| 80 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:124-125` | rule | none | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| 81 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:126-126` | syntax | function, total | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 82 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:127-127` | rule | none | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 83 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:128-131` | rule | none | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` |
| 84 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:132-133` | rule | none | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| 85 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:134-134` | syntax | function, total | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 86 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:135-135` | rule | none | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 87 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:136-136` | rule | none | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 88 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:137-139` | rule | none | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| 89 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:140-142` | rule | none | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| 90 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:143-143` | rule | none | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 91 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:144-147` | rule | none | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` |
| 92 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:148-148` | rule | none | `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))` |
| 93 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:149-151` | rule | none | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| 94 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:152-155` | rule | none | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` |
| 95 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:156-157` | rule | none | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| 96 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:158-158` | syntax | function, total | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 97 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:159-159` | rule | none | `rule intDigAcc(.IntSeq, ACC:Int)             => ACC` |
| 98 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:160-162` | rule | none | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| 99 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:163-163` | rule | none | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 100 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:164-166` | rule | none | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)` |
| 101 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:167-168` | rule | none | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| 102 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:169-169` | rule | none | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>` |
| 103 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:170-170` | rule | none | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 104 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:171-172` | rule | none | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| 105 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:173-173` | rule | none | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>` |
| 106 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:174-176` | rule | none | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| 107 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:177-177` | rule | none | `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)` |
| 108 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:178-178` | rule | none | `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)` |
| 109 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:179-186` | rule | none | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` |
| 110 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:187-187` | rule | none | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 111 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:188-188` | syntax | function | `syntax Int ::= evalArith(IntSeq) [function]` |
| 112 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:189-191` | rule | none | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| 113 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:192-193` | syntax | none | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| 114 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:194-194` | syntax | function, total | `syntax Bool ::= evDigit(Int) [function, total]` |
| 115 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:195-195` | rule | none | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 116 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:196-196` | syntax | function, total | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 117 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:197-197` | rule | none | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 118 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:198-198` | rule | owise | `rule evHead42(_:IntSeq)            => false [owise]` |
| 119 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:199-199` | syntax | function, total | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 120 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:200-200` | rule | none | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 121 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:201-202` | rule | owise | `rule evHead47(_:IntSeq)            => false [owise]` |
| 122 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:203-203` | syntax | function, total | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 123 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:204-204` | rule | none | `rule tokOps(.IntSeq)                 => .OpSeq` |
| 124 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:205-205` | rule | none | `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)` |
| 125 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:206-206` | rule | none | `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)` |
| 126 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:207-207` | rule | none | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 127 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:208-208` | rule | none | `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 128 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:209-209` | rule | none | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("` |
| 129 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:210-210` | rule | none | `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 130 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:211-211` | rule | none | `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))` |
| 131 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:212-213` | rule | none | `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))` |
| 132 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:214-215` | syntax | function, total | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| 133 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:216-216` | rule | none | `rule tokNds(.IntSeq)                => .IntSeq` |
| 134 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:217-217` | rule | none | `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)` |
| 135 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:218-218` | rule | none | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 136 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:219-220` | rule | none | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| 137 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:221-222` | rule | none | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| 138 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:223-224` | rule | owise | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 139 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:225-225` | syntax | none | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 140 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:226-226` | syntax | function, total | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 141 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:227-227` | rule | none | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 142 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:228-229` | rule | owise | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 143 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:230-230` | syntax | function, total | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 144 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:231-231` | rule | none | `rule applyOpE("+",  A:Int, B:Int) => A +Int B` |
| 145 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:232-232` | rule | none | `rule applyOpE("-",  A:Int, B:Int) => A -Int B` |
| 146 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:233-233` | rule | none | `rule applyOpE("*",  A:Int, B:Int) => A *Int B` |
| 147 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:234-234` | rule | none | `rule applyOpE("` |
| 148 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:235-235` | rule | none | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 149 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:236-237` | rule | owise | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 150 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:238-238` | syntax | function, total | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 151 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:239-239` | rule | none | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 152 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:240-240` | rule | none | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 153 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:241-242` | rule | none | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| 154 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:243-243` | rule | owise | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 155 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:244-244` | syntax | function, total | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 156 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:245-245` | rule | none | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 157 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:246-246` | rule | none | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 158 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:247-247` | syntax | function, total | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 159 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:248-249` | rule | none | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 160 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:250-250` | syntax | function, total | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 161 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:251-251` | rule | none | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 162 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:252-252` | rule | none | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 163 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:253-253` | rule | none | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 164 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:254-254` | rule | none | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 165 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:255-255` | syntax | function, total | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 166 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:256-256` | rule | none | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 167 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:257-259` | rule | none | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| 168 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:260-262` | rule | none | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| 169 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:263-264` | rule | owise | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| 170 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:265-265` | syntax | function, total | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 171 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:266-266` | rule | none | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "` |
| 172 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:267-267` | rule | none | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 173 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:268-268` | rule | owise | `rule inLevelE(_:String, _:String) => false [owise]` |
| 174 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:269-269` | syntax | function, total | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 175 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:270-270` | rule | none | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 176 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:271-271` | rule | none | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 177 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:272-272` | syntax | function, total | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 178 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:273-273` | rule | none | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 179 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:274-278` | rule | none | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| 180 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:279-279` | syntax | none | `syntax KItem ::= "#md5"` |
| 181 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:280-281` | rule | priority | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| 182 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:282-282` | rule | none | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 183 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:283-283` | syntax | none | `syntax Val ::= md5Obj(IntSeq)` |
| 184 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:284-284` | rule | none | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 185 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:285-290` | syntax | function, total, symbol, no-evaluators | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| 186 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:291-291` | rule | none | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 187 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:292-292` | rule | none | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 188 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:293-293` | syntax | function | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 189 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:294-294` | rule | none | `rule isIntV(_:Int)         => true` |
| 190 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:295-295` | rule | owise | `rule isIntV(_:Val)         => false [owise]` |
| 191 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:296-296` | rule | none | `rule isStrV(str(_:IntSeq)) => true` |
| 192 | supplied fixed semantics | `reference-semantics/semantics/builtins.k:297-297` | rule | owise | `rule isStrV(_:Val)         => false [owise]` |
| 193 | supplied fixed semantics | `reference-semantics/semantics/call.k:16-18` | rule | none | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| 194 | supplied fixed semantics | `reference-semantics/semantics/call.k:19-19` | syntax | none | `syntax KItem ::= #callee(Exprs)` |
| 195 | supplied fixed semantics | `reference-semantics/semantics/call.k:20-20` | rule | owise | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 196 | supplied fixed semantics | `reference-semantics/semantics/call.k:21-23` | rule | none | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| 197 | supplied fixed semantics | `reference-semantics/semantics/call.k:24-25` | rule | none | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 198 | supplied fixed semantics | `reference-semantics/semantics/call.k:26-26` | rule | none | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 199 | supplied fixed semantics | `reference-semantics/semantics/call.k:27-27` | rule | none | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>` |
| 200 | supplied fixed semantics | `reference-semantics/semantics/call.k:28-28` | rule | none | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>` |
| 201 | supplied fixed semantics | `reference-semantics/semantics/call.k:29-29` | rule | none | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>` |
| 202 | supplied fixed semantics | `reference-semantics/semantics/call.k:30-30` | rule | none | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>` |
| 203 | supplied fixed semantics | `reference-semantics/semantics/call.k:31-31` | rule | owise | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 204 | supplied fixed semantics | `reference-semantics/semantics/call.k:32-37` | rule | none | `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>` |
| 205 | supplied fixed semantics | `reference-semantics/semantics/call.k:38-41` | rule | priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 206 | supplied fixed semantics | `reference-semantics/semantics/call.k:42-46` | rule | priority | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| 207 | supplied fixed semantics | `reference-semantics/semantics/call.k:47-51` | rule | priority | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 208 | supplied fixed semantics | `reference-semantics/semantics/call.k:52-52` | syntax | function, total | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 209 | supplied fixed semantics | `reference-semantics/semantics/call.k:53-55` | rule | none | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| 210 | supplied fixed semantics | `reference-semantics/semantics/call.k:56-62` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` |
| 211 | supplied fixed semantics | `reference-semantics/semantics/call.k:63-68` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| 212 | supplied fixed semantics | `reference-semantics/semantics/call.k:69-79` | rule | none | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| 213 | supplied fixed semantics | `reference-semantics/semantics/call.k:80-86` | rule | none | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| 214 | supplied fixed semantics | `reference-semantics/semantics/call.k:87-87` | syntax | none | `syntax KItem ::= #allocCells(ParamNames)` |
| 215 | supplied fixed semantics | `reference-semantics/semantics/call.k:88-88` | rule | none | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 216 | supplied fixed semantics | `reference-semantics/semantics/call.k:89-94` | rule | none | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 217 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:11-11` | rule | none | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 218 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:12-13` | rule | none | `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 219 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:14-14` | syntax | none | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 220 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:15-17` | rule | none | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| 221 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:18-18` | syntax | none | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 222 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:19-20` | rule | none | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| 223 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:21-23` | rule | none | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| 224 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:24-24` | syntax | none | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 225 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:25-25` | rule | none | `rule compGuard(.Exprs)             => Bool(true)` |
| 226 | supplied fixed semantics | `reference-semantics/semantics/comprehension.k:26-26` | rule | none | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| 227 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:13-15` | rule | none | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 228 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:16-24` | rule | none | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 229 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:25-25` | syntax | none | `syntax Val ::= kvP(Val, Val)` |
| 230 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:26-27` | syntax | none | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| 231 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:28-30` | rule | priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| 232 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:31-33` | rule | priority | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| 233 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:34-35` | rule | none | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| 234 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:36-37` | rule | none | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| 235 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:38-41` | rule | none | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| 236 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:42-42` | syntax | function | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 237 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:43-43` | rule | none | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 238 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:44-46` | rule | none | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| 239 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:47-50` | rule | none | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| 240 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:51-51` | syntax | function | `syntax Bool ::= kLt(Val, Val) [function]` |
| 241 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:52-52` | rule | none | `rule kLt(I1:Int, I2:Int)             => I1 <Int I2` |
| 242 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:53-53` | rule | none | `rule kLt(F1:Float, F2:Float)         => F1 <Float F2` |
| 243 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:54-55` | rule | none | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 244 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:56-56` | syntax | function, total | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 245 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:57-57` | rule | none | `rule unpairVS(.ValSeq) => .ValSeq` |
| 246 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:58-58` | rule | none | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 247 | supplied fixed semantics | `reference-semantics/semantics/concrete.k:59-59` | rule | owise | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| 248 | supplied fixed semantics | `reference-semantics/semantics/controls.k:9-11` | rule | none | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 249 | supplied fixed semantics | `reference-semantics/semantics/controls.k:12-19` | rule | priority | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 250 | supplied fixed semantics | `reference-semantics/semantics/controls.k:20-26` | rule | none | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` |
| 251 | supplied fixed semantics | `reference-semantics/semantics/controls.k:27-34` | rule | priority | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]` |
| 252 | supplied fixed semantics | `reference-semantics/semantics/controls.k:35-35` | rule | none | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 253 | supplied fixed semantics | `reference-semantics/semantics/controls.k:36-36` | rule | owise | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 254 | supplied fixed semantics | `reference-semantics/semantics/controls.k:37-37` | syntax | none | `syntax KItem ::= #bindImports(ParamNames)` |
| 255 | supplied fixed semantics | `reference-semantics/semantics/controls.k:38-38` | rule | none | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 256 | supplied fixed semantics | `reference-semantics/semantics/controls.k:39-42` | rule | none | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| 257 | supplied fixed semantics | `reference-semantics/semantics/controls.k:43-47` | rule | none | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` |
| 258 | supplied fixed semantics | `reference-semantics/semantics/controls.k:48-50` | rule | none | `rule <k> Expr(_:Val) => .K ... </k>` |
| 259 | supplied fixed semantics | `reference-semantics/semantics/controls.k:51-51` | syntax | none | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 260 | supplied fixed semantics | `reference-semantics/semantics/controls.k:52-52` | rule | none | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 261 | supplied fixed semantics | `reference-semantics/semantics/controls.k:53-53` | rule | none | `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>` |
| 262 | supplied fixed semantics | `reference-semantics/semantics/controls.k:54-56` | rule | none | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| 263 | supplied fixed semantics | `reference-semantics/semantics/controls.k:57-58` | rule | none | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| 264 | supplied fixed semantics | `reference-semantics/semantics/controls.k:59-64` | rule | none | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` |
| 265 | supplied fixed semantics | `reference-semantics/semantics/controls.k:65-68` | syntax | none | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| 266 | supplied fixed semantics | `reference-semantics/semantics/controls.k:69-70` | rule | none | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 267 | supplied fixed semantics | `reference-semantics/semantics/controls.k:71-71` | rule | none | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 268 | supplied fixed semantics | `reference-semantics/semantics/controls.k:72-72` | rule | none | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 269 | supplied fixed semantics | `reference-semantics/semantics/controls.k:73-76` | rule | none | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` |
| 270 | supplied fixed semantics | `reference-semantics/semantics/controls.k:77-77` | rule | none | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 271 | supplied fixed semantics | `reference-semantics/semantics/controls.k:78-78` | rule | none | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 272 | supplied fixed semantics | `reference-semantics/semantics/controls.k:79-80` | rule | none | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| 273 | supplied fixed semantics | `reference-semantics/semantics/controls.k:81-84` | rule | none | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` |
| 274 | supplied fixed semantics | `reference-semantics/semantics/controls.k:85-85` | rule | none | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 275 | supplied fixed semantics | `reference-semantics/semantics/controls.k:86-86` | rule | none | `rule <k> Continue => #cont ... </k>` |
| 276 | supplied fixed semantics | `reference-semantics/semantics/controls.k:87-87` | rule | none | `rule <k> Break => #brk ... </k>` |
| 277 | supplied fixed semantics | `reference-semantics/semantics/controls.k:88-88` | rule | none | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 278 | supplied fixed semantics | `reference-semantics/semantics/controls.k:89-89` | rule | owise | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 279 | supplied fixed semantics | `reference-semantics/semantics/controls.k:90-90` | rule | none | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 280 | supplied fixed semantics | `reference-semantics/semantics/controls.k:91-94` | rule | owise | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| 281 | supplied fixed semantics | `reference-semantics/semantics/controls.k:95-97` | rule | priority | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 282 | supplied fixed semantics | `reference-semantics/semantics/controls.k:98-100` | rule | priority | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 283 | supplied fixed semantics | `reference-semantics/semantics/controls.k:101-105` | rule | priority | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 284 | supplied fixed semantics | `reference-semantics/semantics/controls.k:106-108` | rule | priority | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 285 | supplied fixed semantics | `reference-semantics/semantics/core.k:13-13` | syntax | none | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 286 | supplied fixed semantics | `reference-semantics/semantics/core.k:14-14` | syntax | none | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 287 | supplied fixed semantics | `reference-semantics/semantics/core.k:15-17` | syntax | none | `syntax Str    ::= str(IntSeq)` |
| 288 | supplied fixed semantics | `reference-semantics/semantics/core.k:18-24` | syntax | none | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| 289 | supplied fixed semantics | `reference-semantics/semantics/core.k:25-35` | syntax | none | `syntax Val      ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) \| cellRef(Int) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) \| builtinV(String) \| boundMethodV(Val, String)` |
| 290 | supplied fixed semantics | `reference-semantics/semantics/core.k:36-36` | syntax | none | `syntax Parent   ::= "root" \| parent(Int)` |
| 291 | supplied fixed semantics | `reference-semantics/semantics/core.k:37-37` | syntax | none | `syntax Scope    ::= scope(Map, Parent)` |
| 292 | supplied fixed semantics | `reference-semantics/semantics/core.k:38-38` | syntax | none | `syntax KResult  ::= Val` |
| 293 | supplied fixed semantics | `reference-semantics/semantics/core.k:39-39` | syntax | none | `syntax Expr     ::= Val` |
| 294 | supplied fixed semantics | `reference-semantics/semantics/core.k:40-40` | syntax | none | `syntax Vals     ::= List{Val, ","}` |
| 295 | supplied fixed semantics | `reference-semantics/semantics/core.k:41-41` | syntax | none | `syntax Exc      ::= "NoExc" \| "AssertionError"` |
| 296 | supplied fixed semantics | `reference-semantics/semantics/core.k:42-48` | syntax | none | `syntax RetState ::= "noRet" \| retV(Val)` |
| 297 | supplied fixed semantics | `reference-semantics/semantics/core.k:49-67` | configuration | none | `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     \|-> scope(.Map, parent(-1)) -1    \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code>` |
| 298 | supplied fixed semantics | `reference-semantics/semantics/core.k:68-68` | syntax | function, total | `syntax Bool ::= isRefV(Val) [function, total]` |
| 299 | supplied fixed semantics | `reference-semantics/semantics/core.k:69-69` | rule | none | `rule isRefV(ref(_:Int)) => true` |
| 300 | supplied fixed semantics | `reference-semantics/semantics/core.k:70-74` | rule | owise | `rule isRefV(_:Val)      => false [owise]` |
| 301 | supplied fixed semantics | `reference-semantics/semantics/core.k:75-75` | syntax | none | `syntax HeapVal ::= cellV(Val)` |
| 302 | supplied fixed semantics | `reference-semantics/semantics/core.k:76-76` | syntax | function, total | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 303 | supplied fixed semantics | `reference-semantics/semantics/core.k:77-77` | rule | none | `rule isCellRef(cellRef(_:Int)) => true` |
| 304 | supplied fixed semantics | `reference-semantics/semantics/core.k:78-84` | rule | owise | `rule isCellRef(_:Val)          => false [owise]` |
| 305 | supplied fixed semantics | `reference-semantics/semantics/core.k:85-94` | rule | priority | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` |
| 306 | supplied fixed semantics | `reference-semantics/semantics/core.k:95-95` | syntax | none | `syntax Val ::= kwV(String, Val)` |
| 307 | supplied fixed semantics | `reference-semantics/semantics/core.k:96-96` | syntax | none | `syntax KItem ::= #kwTag(String)` |
| 308 | supplied fixed semantics | `reference-semantics/semantics/core.k:97-97` | rule | none | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 309 | supplied fixed semantics | `reference-semantics/semantics/core.k:98-99` | rule | none | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| 310 | supplied fixed semantics | `reference-semantics/semantics/core.k:100-100` | syntax | function, total | `syntax Bool ::= isKwV(Val) [function, total]` |
| 311 | supplied fixed semantics | `reference-semantics/semantics/core.k:101-101` | rule | none | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 312 | supplied fixed semantics | `reference-semantics/semantics/core.k:102-105` | rule | owise | `rule isKwV(_:Val)                => false [owise]` |
| 313 | supplied fixed semantics | `reference-semantics/semantics/core.k:106-106` | syntax | none | `syntax Val ::= cellsMark(ParamNames)` |
| 314 | supplied fixed semantics | `reference-semantics/semantics/core.k:107-107` | syntax | function | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 315 | supplied fixed semantics | `reference-semantics/semantics/core.k:108-108` | rule | none | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 316 | supplied fixed semantics | `reference-semantics/semantics/core.k:109-109` | syntax | function, total | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 317 | supplied fixed semantics | `reference-semantics/semantics/core.k:110-110` | rule | none | `rule pnMember(_:String, .ParamNames) => false` |
| 318 | supplied fixed semantics | `reference-semantics/semantics/core.k:111-112` | rule | none | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 319 | supplied fixed semantics | `reference-semantics/semantics/core.k:113-113` | syntax | none | `syntax KItem ::= #cellW(Val, Val)` |
| 320 | supplied fixed semantics | `reference-semantics/semantics/core.k:114-116` | rule | none | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| 321 | supplied fixed semantics | `reference-semantics/semantics/core.k:117-117` | syntax | none | `syntax KItem ::= #alloc(Val)` |
| 322 | supplied fixed semantics | `reference-semantics/semantics/core.k:118-123` | rule | none | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 323 | supplied fixed semantics | `reference-semantics/semantics/core.k:124-124` | syntax | none | `syntax KItem ::= #loadAll(Module)` |
| 324 | supplied fixed semantics | `reference-semantics/semantics/core.k:125-125` | rule | none | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 325 | supplied fixed semantics | `reference-semantics/semantics/core.k:126-126` | rule | none | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 326 | supplied fixed semantics | `reference-semantics/semantics/core.k:127-129` | rule | none | `rule <k> .Stmts => .K ... </k>` |
| 327 | supplied fixed semantics | `reference-semantics/semantics/core.k:130-130` | syntax | none | `syntax KItem ::= #look(String, Int)` |
| 328 | supplied fixed semantics | `reference-semantics/semantics/core.k:131-131` | rule | none | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 329 | supplied fixed semantics | `reference-semantics/semantics/core.k:132-144` | rule | none | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` |
| 330 | supplied fixed semantics | `reference-semantics/semantics/core.k:145-151` | rule | priority | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| 331 | supplied fixed semantics | `reference-semantics/semantics/core.k:152-156` | rule | none | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` |
| 332 | supplied fixed semantics | `reference-semantics/semantics/core.k:157-157` | syntax | function, total | `syntax Scope ::= "builtinsScope" [function, total]` |
| 333 | supplied fixed semantics | `reference-semantics/semantics/core.k:158-184` | rule | none | `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root)` |
| 334 | supplied fixed semantics | `reference-semantics/semantics/core.k:185-185` | syntax | none | `syntax ApplyK ::= toCall(Val)` |
| 335 | supplied fixed semantics | `reference-semantics/semantics/core.k:186-188` | syntax | none | `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| 336 | supplied fixed semantics | `reference-semantics/semantics/core.k:189-189` | rule | none | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 337 | supplied fixed semantics | `reference-semantics/semantics/core.k:190-190` | rule | none | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 338 | supplied fixed semantics | `reference-semantics/semantics/core.k:191-193` | rule | none | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| 339 | supplied fixed semantics | `reference-semantics/semantics/core.k:194-194` | rule | none | `rule <k> Int(I:Int)   => I ... </k>` |
| 340 | supplied fixed semantics | `reference-semantics/semantics/core.k:195-195` | rule | none | `rule <k> Bool(B:Bool) => B ... </k>` |
| 341 | supplied fixed semantics | `reference-semantics/semantics/core.k:196-198` | rule | none | `rule <k> NoneVal      => noneV ... </k>` |
| 342 | supplied fixed semantics | `reference-semantics/semantics/core.k:199-199` | syntax | function | `syntax Bool ::= truthy(Val) [function]` |
| 343 | supplied fixed semantics | `reference-semantics/semantics/core.k:200-200` | rule | none | `rule truthy(B:Bool)          => B` |
| 344 | supplied fixed semantics | `reference-semantics/semantics/core.k:201-201` | rule | none | `rule truthy(noneV)           => false` |
| 345 | supplied fixed semantics | `reference-semantics/semantics/core.k:202-202` | rule | none | `rule truthy(I:Int)           => I =/=Int 0` |
| 346 | supplied fixed semantics | `reference-semantics/semantics/core.k:203-203` | rule | none | `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)` |
| 347 | supplied fixed semantics | `reference-semantics/semantics/core.k:204-204` | rule | none | `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)` |
| 348 | supplied fixed semantics | `reference-semantics/semantics/core.k:205-207` | rule | none | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 349 | supplied fixed semantics | `reference-semantics/semantics/core.k:208-208` | syntax | function | `syntax Val  ::= applyUn(String, Val) [function]` |
| 350 | supplied fixed semantics | `reference-semantics/semantics/core.k:209-209` | syntax | function | `syntax Val  ::= applyBin(String, Val, Val) [function]` |
| 351 | supplied fixed semantics | `reference-semantics/semantics/core.k:210-212` | syntax | function | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| 352 | supplied fixed semantics | `reference-semantics/semantics/core.k:213-213` | syntax | function, total | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 353 | supplied fixed semantics | `reference-semantics/semantics/core.k:214-214` | rule | none | `rule appendVal(.Vals, V:Val)              => V , .Vals` |
| 354 | supplied fixed semantics | `reference-semantics/semantics/core.k:215-216` | rule | none | `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)` |
| 355 | supplied fixed semantics | `reference-semantics/semantics/core.k:217-217` | syntax | function, total | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 356 | supplied fixed semantics | `reference-semantics/semantics/core.k:218-218` | rule | none | `rule vals2valSeq(.Vals)            => .ValSeq` |
| 357 | supplied fixed semantics | `reference-semantics/semantics/core.k:219-222` | rule | none | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| 358 | supplied fixed semantics | `reference-semantics/semantics/core.k:223-223` | syntax | function, total | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 359 | supplied fixed semantics | `reference-semantics/semantics/core.k:224-224` | rule | none | `rule vsLen(.ValSeq)                => 0` |
| 360 | supplied fixed semantics | `reference-semantics/semantics/core.k:225-226` | rule | none | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 361 | supplied fixed semantics | `reference-semantics/semantics/core.k:227-227` | syntax | function, total | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 362 | supplied fixed semantics | `reference-semantics/semantics/core.k:228-228` | rule | none | `rule isLen(.IntSeq)                => 0` |
| 363 | supplied fixed semantics | `reference-semantics/semantics/core.k:229-232` | rule | none | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| 364 | supplied fixed semantics | `reference-semantics/semantics/core.k:233-233` | syntax | function, total | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 365 | supplied fixed semantics | `reference-semantics/semantics/core.k:234-234` | rule | none | `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq` |
| 366 | supplied fixed semantics | `reference-semantics/semantics/core.k:235-235` | rule | none | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)` |
| 367 | supplied fixed semantics | `reference-semantics/semantics/core.k:236-237` | rule | none | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| 368 | supplied fixed semantics | `reference-semantics/semantics/core.k:238-239` | rule | none | `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0` |
| 369 | supplied fixed semantics | `reference-semantics/semantics/dict.k:20-22` | syntax | none | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| 370 | supplied fixed semantics | `reference-semantics/semantics/dict.k:23-25` | syntax | none | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| 371 | supplied fixed semantics | `reference-semantics/semantics/dict.k:26-26` | rule | none | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 372 | supplied fixed semantics | `reference-semantics/semantics/dict.k:27-27` | rule | none | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 373 | supplied fixed semantics | `reference-semantics/semantics/dict.k:28-29` | rule | none | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| 374 | supplied fixed semantics | `reference-semantics/semantics/dict.k:30-31` | rule | none | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| 375 | supplied fixed semantics | `reference-semantics/semantics/dict.k:32-36` | rule | none | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` |
| 376 | supplied fixed semantics | `reference-semantics/semantics/dict.k:37-37` | syntax | function, total | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 377 | supplied fixed semantics | `reference-semantics/semantics/dict.k:38-38` | rule | none | `rule dHasKey(.ValSeq, _:Val)                => false` |
| 378 | supplied fixed semantics | `reference-semantics/semantics/dict.k:39-39` | rule | none | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K` |
| 379 | supplied fixed semantics | `reference-semantics/semantics/dict.k:40-42` | rule | none | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| 380 | supplied fixed semantics | `reference-semantics/semantics/dict.k:43-43` | syntax | function, total | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 381 | supplied fixed semantics | `reference-semantics/semantics/dict.k:44-44` | rule | none | `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)` |
| 382 | supplied fixed semantics | `reference-semantics/semantics/dict.k:45-48` | rule | none | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| 383 | supplied fixed semantics | `reference-semantics/semantics/dict.k:49-49` | syntax | function, total | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 384 | supplied fixed semantics | `reference-semantics/semantics/dict.k:50-51` | rule | none | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K` |
| 385 | supplied fixed semantics | `reference-semantics/semantics/dict.k:52-53` | rule | none | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| 386 | supplied fixed semantics | `reference-semantics/semantics/dict.k:54-57` | rule | owise | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| 387 | supplied fixed semantics | `reference-semantics/semantics/dict.k:58-62` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` |
| 388 | supplied fixed semantics | `reference-semantics/semantics/dict.k:63-63` | rule | none | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 389 | supplied fixed semantics | `reference-semantics/semantics/dict.k:64-64` | syntax | function | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 390 | supplied fixed semantics | `reference-semantics/semantics/dict.k:65-69` | rule | priority | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` |
| 391 | supplied fixed semantics | `reference-semantics/semantics/dict.k:70-70` | syntax | function | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 392 | supplied fixed semantics | `reference-semantics/semantics/dict.k:71-75` | rule | none | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| 393 | supplied fixed semantics | `reference-semantics/semantics/dict.k:76-76` | syntax | none | `syntax KItem ::= #dsetK(String, Val)` |
| 394 | supplied fixed semantics | `reference-semantics/semantics/dict.k:77-77` | rule | none | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 395 | supplied fixed semantics | `reference-semantics/semantics/dict.k:78-81` | rule | none | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| 396 | supplied fixed semantics | `reference-semantics/semantics/dict.k:82-85` | rule | none | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| 397 | supplied fixed semantics | `reference-semantics/semantics/dict.k:86-86` | syntax | none | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 398 | supplied fixed semantics | `reference-semantics/semantics/dict.k:87-89` | rule | none | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` |
| 399 | supplied fixed semantics | `reference-semantics/semantics/dict.k:90-90` | syntax | function, total | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 400 | supplied fixed semantics | `reference-semantics/semantics/dict.k:91-91` | rule | none | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 401 | supplied fixed semantics | `reference-semantics/semantics/dict.k:92-94` | rule | none | `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0` |
| 402 | supplied fixed semantics | `reference-semantics/semantics/dict.k:95-96` | rule | none | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| 403 | supplied fixed semantics | `reference-semantics/semantics/dict.k:97-97` | syntax | function | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 404 | supplied fixed semantics | `reference-semantics/semantics/dict.k:98-98` | rule | none | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 405 | supplied fixed semantics | `reference-semantics/semantics/dict.k:99-100` | rule | none | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| 406 | supplied fixed semantics | `reference-semantics/semantics/dict.k:101-101` | syntax | function | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 407 | supplied fixed semantics | `reference-semantics/semantics/dict.k:102-102` | rule | none | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K` |
| 408 | supplied fixed semantics | `reference-semantics/semantics/dict.k:103-103` | rule | none | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| 409 | supplied fixed semantics | `reference-semantics/semantics/float.k:20-20` | syntax | none | `syntax Val ::= Float` |
| 410 | supplied fixed semantics | `reference-semantics/semantics/float.k:21-23` | rule | none | `rule <k> Float(F:Float) => F ... </k>` |
| 411 | supplied fixed semantics | `reference-semantics/semantics/float.k:24-24` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 412 | supplied fixed semantics | `reference-semantics/semantics/float.k:25-26` | rule | concrete | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 413 | supplied fixed semantics | `reference-semantics/semantics/float.k:27-29` | rule | none | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| 414 | supplied fixed semantics | `reference-semantics/semantics/float.k:30-30` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 415 | supplied fixed semantics | `reference-semantics/semantics/float.k:31-31` | rule | concrete | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 416 | supplied fixed semantics | `reference-semantics/semantics/float.k:32-36` | rule | none | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| 417 | supplied fixed semantics | `reference-semantics/semantics/float.k:37-37` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 418 | supplied fixed semantics | `reference-semantics/semantics/float.k:38-38` | rule | concrete | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 419 | supplied fixed semantics | `reference-semantics/semantics/float.k:39-42` | rule | none | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| 420 | supplied fixed semantics | `reference-semantics/semantics/float.k:43-43` | rule | none | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 421 | supplied fixed semantics | `reference-semantics/semantics/float.k:44-49` | rule | none | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| 422 | supplied fixed semantics | `reference-semantics/semantics/float.k:50-50` | syntax | function, total, symbol, no-evaluators | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 423 | supplied fixed semantics | `reference-semantics/semantics/float.k:51-51` | rule | concrete | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 424 | supplied fixed semantics | `reference-semantics/semantics/float.k:52-53` | rule | none | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 425 | supplied fixed semantics | `reference-semantics/semantics/float.k:54-54` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 426 | supplied fixed semantics | `reference-semantics/semantics/float.k:55-55` | rule | concrete | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 427 | supplied fixed semantics | `reference-semantics/semantics/float.k:56-60` | rule | none | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| 428 | supplied fixed semantics | `reference-semantics/semantics/float.k:61-64` | rule | none | `rule <k> Import(_:String) => .K ... </k>` |
| 429 | supplied fixed semantics | `reference-semantics/semantics/float.k:65-65` | syntax | none | `syntax KItem ::= "#mathCeil"` |
| 430 | supplied fixed semantics | `reference-semantics/semantics/float.k:66-66` | rule | priority | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 431 | supplied fixed semantics | `reference-semantics/semantics/float.k:67-69` | rule | none | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| 432 | supplied fixed semantics | `reference-semantics/semantics/float.k:70-70` | syntax | none | `syntax KItem ::= "#mathFloor"` |
| 433 | supplied fixed semantics | `reference-semantics/semantics/float.k:71-71` | rule | priority | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 434 | supplied fixed semantics | `reference-semantics/semantics/float.k:72-72` | rule | none | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 435 | supplied fixed semantics | `reference-semantics/semantics/float.k:73-73` | syntax | function, total, symbol | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 436 | supplied fixed semantics | `reference-semantics/semantics/float.k:74-74` | rule | concrete | `rule floorFI(I:Int)   => I                        [concrete]` |
| 437 | supplied fixed semantics | `reference-semantics/semantics/float.k:75-77` | rule | concrete | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| 438 | supplied fixed semantics | `reference-semantics/semantics/float.k:78-78` | rule | none | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 439 | supplied fixed semantics | `reference-semantics/semantics/float.k:79-81` | rule | none | `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)` |
| 440 | supplied fixed semantics | `reference-semantics/semantics/float.k:82-82` | syntax | none | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 441 | supplied fixed semantics | `reference-semantics/semantics/float.k:83-83` | rule | priority | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 442 | supplied fixed semantics | `reference-semantics/semantics/float.k:84-84` | rule | none | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 443 | supplied fixed semantics | `reference-semantics/semantics/float.k:85-85` | rule | none | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 444 | supplied fixed semantics | `reference-semantics/semantics/float.k:86-86` | syntax | function, total, symbol | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 445 | supplied fixed semantics | `reference-semantics/semantics/float.k:87-87` | rule | concrete | `rule toF(F:Float) => F        [concrete]` |
| 446 | supplied fixed semantics | `reference-semantics/semantics/float.k:88-92` | rule | concrete | `rule toF(I:Int)   => intToF(I) [concrete]` |
| 447 | supplied fixed semantics | `reference-semantics/semantics/float.k:93-93` | syntax | function, total, symbol | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 448 | supplied fixed semantics | `reference-semantics/semantics/float.k:94-94` | rule | concrete | `rule ceilF(I:Int)   => I                       [concrete]` |
| 449 | supplied fixed semantics | `reference-semantics/semantics/float.k:95-98` | rule | concrete | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| 450 | supplied fixed semantics | `reference-semantics/semantics/float.k:99-102` | rule | none | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| 451 | supplied fixed semantics | `reference-semantics/semantics/float.k:103-103` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 452 | supplied fixed semantics | `reference-semantics/semantics/float.k:104-104` | rule | concrete | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 453 | supplied fixed semantics | `reference-semantics/semantics/float.k:105-106` | rule | none | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 454 | supplied fixed semantics | `reference-semantics/semantics/float.k:107-107` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 455 | supplied fixed semantics | `reference-semantics/semantics/float.k:108-108` | rule | concrete | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 456 | supplied fixed semantics | `reference-semantics/semantics/float.k:109-110` | rule | none | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 457 | supplied fixed semantics | `reference-semantics/semantics/float.k:111-111` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 458 | supplied fixed semantics | `reference-semantics/semantics/float.k:112-112` | rule | concrete | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 459 | supplied fixed semantics | `reference-semantics/semantics/float.k:113-114` | rule | none | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 460 | supplied fixed semantics | `reference-semantics/semantics/float.k:115-115` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 461 | supplied fixed semantics | `reference-semantics/semantics/float.k:116-116` | rule | concrete | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 462 | supplied fixed semantics | `reference-semantics/semantics/float.k:117-118` | rule | none | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 463 | supplied fixed semantics | `reference-semantics/semantics/float.k:119-119` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 464 | supplied fixed semantics | `reference-semantics/semantics/float.k:120-120` | rule | concrete | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 465 | supplied fixed semantics | `reference-semantics/semantics/float.k:121-124` | rule | none | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| 466 | supplied fixed semantics | `reference-semantics/semantics/float.k:125-125` | syntax | function, total, symbol, no-evaluators | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 467 | supplied fixed semantics | `reference-semantics/semantics/float.k:126-126` | rule | concrete | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 468 | supplied fixed semantics | `reference-semantics/semantics/float.k:127-127` | rule | none | `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)` |
| 469 | supplied fixed semantics | `reference-semantics/semantics/float.k:128-128` | rule | none | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 470 | supplied fixed semantics | `reference-semantics/semantics/float.k:129-131` | rule | none | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| 471 | supplied fixed semantics | `reference-semantics/semantics/float.k:132-132` | rule | none | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 472 | supplied fixed semantics | `reference-semantics/semantics/float.k:133-133` | rule | none | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 473 | supplied fixed semantics | `reference-semantics/semantics/float.k:134-134` | rule | none | `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)` |
| 474 | supplied fixed semantics | `reference-semantics/semantics/float.k:135-135` | rule | none | `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))` |
| 475 | supplied fixed semantics | `reference-semantics/semantics/float.k:136-136` | rule | none | `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)` |
| 476 | supplied fixed semantics | `reference-semantics/semantics/float.k:137-137` | rule | none | `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))` |
| 477 | supplied fixed semantics | `reference-semantics/semantics/float.k:138-138` | rule | none | `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)` |
| 478 | supplied fixed semantics | `reference-semantics/semantics/float.k:139-141` | rule | none | `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))` |
| 479 | supplied fixed semantics | `reference-semantics/semantics/float.k:142-142` | syntax | function, total, symbol, no-evaluators | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 480 | supplied fixed semantics | `reference-semantics/semantics/float.k:143-143` | rule | concrete | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 481 | supplied fixed semantics | `reference-semantics/semantics/float.k:144-144` | rule | none | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 482 | supplied fixed semantics | `reference-semantics/semantics/float.k:145-145` | rule | none | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 483 | supplied fixed semantics | `reference-semantics/semantics/float.k:146-146` | rule | none | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 484 | supplied fixed semantics | `reference-semantics/semantics/float.k:147-147` | rule | none | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 485 | supplied fixed semantics | `reference-semantics/semantics/float.k:148-148` | rule | none | `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)` |
| 486 | supplied fixed semantics | `reference-semantics/semantics/float.k:149-149` | rule | none | `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))` |
| 487 | supplied fixed semantics | `reference-semantics/semantics/float.k:150-150` | rule | none | `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)` |
| 488 | supplied fixed semantics | `reference-semantics/semantics/float.k:151-153` | rule | none | `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))` |
| 489 | supplied fixed semantics | `reference-semantics/semantics/float.k:154-154` | rule | none | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 490 | supplied fixed semantics | `reference-semantics/semantics/float.k:155-159` | rule | none | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| 491 | supplied fixed semantics | `reference-semantics/semantics/float.k:160-160` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 492 | supplied fixed semantics | `reference-semantics/semantics/float.k:161-161` | rule | concrete | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 493 | supplied fixed semantics | `reference-semantics/semantics/float.k:162-164` | rule | concrete | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| 494 | supplied fixed semantics | `reference-semantics/semantics/float.k:165-165` | syntax | function | `syntax Int ::= headIS(IntSeq) [function]` |
| 495 | supplied fixed semantics | `reference-semantics/semantics/float.k:166-166` | rule | none | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 496 | supplied fixed semantics | `reference-semantics/semantics/float.k:167-167` | syntax | function, total | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 497 | supplied fixed semantics | `reference-semantics/semantics/float.k:168-168` | rule | none | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 498 | supplied fixed semantics | `reference-semantics/semantics/float.k:169-169` | rule | none | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 499 | supplied fixed semantics | `reference-semantics/semantics/float.k:170-170` | rule | none | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 500 | supplied fixed semantics | `reference-semantics/semantics/float.k:171-172` | rule | none | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| 501 | supplied fixed semantics | `reference-semantics/semantics/float.k:173-173` | syntax | function, total | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 502 | supplied fixed semantics | `reference-semantics/semantics/float.k:174-174` | rule | none | `rule fracPart(.IntSeq) => 0` |
| 503 | supplied fixed semantics | `reference-semantics/semantics/float.k:175-175` | rule | none | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 504 | supplied fixed semantics | `reference-semantics/semantics/float.k:176-176` | rule | none | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 505 | supplied fixed semantics | `reference-semantics/semantics/float.k:177-177` | rule | none | `rule fracAcc(.IntSeq, A:Int) => A` |
| 506 | supplied fixed semantics | `reference-semantics/semantics/float.k:178-178` | rule | none | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 507 | supplied fixed semantics | `reference-semantics/semantics/float.k:179-179` | syntax | function, total | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 508 | supplied fixed semantics | `reference-semantics/semantics/float.k:180-180` | rule | none | `rule fracScale(.IntSeq) => 1` |
| 509 | supplied fixed semantics | `reference-semantics/semantics/float.k:181-181` | rule | none | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 510 | supplied fixed semantics | `reference-semantics/semantics/float.k:182-182` | rule | none | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 511 | supplied fixed semantics | `reference-semantics/semantics/float.k:183-183` | rule | none | `rule fscAcc(.IntSeq, A:Int) => A` |
| 512 | supplied fixed semantics | `reference-semantics/semantics/float.k:184-184` | rule | none | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 513 | supplied fixed semantics | `reference-semantics/semantics/float.k:185-185` | rule | none | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 514 | supplied fixed semantics | `reference-semantics/semantics/float.k:186-186` | rule | none | `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)` |
| 515 | supplied fixed semantics | `reference-semantics/semantics/float.k:187-189` | rule | none | `rule applyBuiltin("float", F:Float, .Vals)        => F` |
| 516 | supplied fixed semantics | `reference-semantics/semantics/float.k:190-190` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 517 | supplied fixed semantics | `reference-semantics/semantics/float.k:191-191` | rule | concrete | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 518 | supplied fixed semantics | `reference-semantics/semantics/float.k:192-194` | rule | none | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| 519 | supplied fixed semantics | `reference-semantics/semantics/float.k:195-195` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 520 | supplied fixed semantics | `reference-semantics/semantics/float.k:196-196` | rule | concrete | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 521 | supplied fixed semantics | `reference-semantics/semantics/float.k:197-197` | rule | none | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 522 | supplied fixed semantics | `reference-semantics/semantics/float.k:198-198` | rule | none | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 523 | supplied fixed semantics | `reference-semantics/semantics/float.k:199-199` | rule | none | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 524 | supplied fixed semantics | `reference-semantics/semantics/float.k:200-200` | rule | none | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 525 | supplied fixed semantics | `reference-semantics/semantics/float.k:201-201` | rule | none | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 526 | supplied fixed semantics | `reference-semantics/semantics/float.k:202-202` | rule | none | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 527 | supplied fixed semantics | `reference-semantics/semantics/float.k:203-203` | rule | none | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 528 | supplied fixed semantics | `reference-semantics/semantics/float.k:204-204` | rule | none | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 529 | supplied fixed semantics | `reference-semantics/semantics/float.k:205-205` | rule | none | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 530 | supplied fixed semantics | `reference-semantics/semantics/float.k:206-208` | rule | none | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| 531 | supplied fixed semantics | `reference-semantics/semantics/float.k:209-209` | syntax | function, total, symbol, no-evaluators | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 532 | supplied fixed semantics | `reference-semantics/semantics/float.k:210-210` | rule | concrete | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 533 | supplied fixed semantics | `reference-semantics/semantics/float.k:211-212` | rule | none | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 534 | supplied fixed semantics | `reference-semantics/semantics/float.k:213-213` | rule | none | `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)` |
| 535 | supplied fixed semantics | `reference-semantics/semantics/float.k:214-216` | rule | none | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| 536 | supplied fixed semantics | `reference-semantics/semantics/float.k:217-217` | syntax | function, total, symbol, no-evaluators | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 537 | supplied fixed semantics | `reference-semantics/semantics/float.k:218-222` | rule | concrete | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| 538 | supplied fixed semantics | `reference-semantics/semantics/float.k:223-223` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 539 | supplied fixed semantics | `reference-semantics/semantics/float.k:224-226` | rule | concrete | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| 540 | supplied fixed semantics | `reference-semantics/semantics/float.k:227-227` | rule | none | `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)` |
| 541 | supplied fixed semantics | `reference-semantics/semantics/float.k:228-229` | rule | none | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 542 | supplied fixed semantics | `reference-semantics/semantics/float.k:230-230` | syntax | function, total, symbol, no-evaluators | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 543 | supplied fixed semantics | `reference-semantics/semantics/float.k:231-231` | rule | concrete | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 544 | supplied fixed semantics | `reference-semantics/semantics/float.k:232-232` | syntax | none | `syntax KItem ::= "#mathSqrt"` |
| 545 | supplied fixed semantics | `reference-semantics/semantics/float.k:233-233` | rule | priority | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 546 | supplied fixed semantics | `reference-semantics/semantics/float.k:234-234` | rule | none | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 547 | supplied fixed semantics | `reference-semantics/semantics/float.k:235-242` | rule | none | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| 548 | supplied fixed semantics | `reference-semantics/semantics/float.k:243-243` | syntax | none | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 549 | supplied fixed semantics | `reference-semantics/semantics/float.k:244-244` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 550 | supplied fixed semantics | `reference-semantics/semantics/float.k:245-245` | rule | none | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 551 | supplied fixed semantics | `reference-semantics/semantics/float.k:246-246` | rule | none | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 552 | supplied fixed semantics | `reference-semantics/semantics/float.k:247-249` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 553 | supplied fixed semantics | `reference-semantics/semantics/float.k:250-250` | syntax | none | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 554 | supplied fixed semantics | `reference-semantics/semantics/float.k:251-251` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 555 | supplied fixed semantics | `reference-semantics/semantics/float.k:252-252` | rule | none | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 556 | supplied fixed semantics | `reference-semantics/semantics/float.k:253-253` | rule | none | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 557 | supplied fixed semantics | `reference-semantics/semantics/float.k:254-260` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 558 | supplied fixed semantics | `reference-semantics/semantics/float.k:261-261` | syntax | none | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 559 | supplied fixed semantics | `reference-semantics/semantics/float.k:262-264` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| 560 | supplied fixed semantics | `reference-semantics/semantics/float.k:265-265` | rule | none | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 561 | supplied fixed semantics | `reference-semantics/semantics/float.k:266-266` | rule | none | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 562 | supplied fixed semantics | `reference-semantics/semantics/float.k:267-269` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| 563 | supplied fixed semantics | `reference-semantics/semantics/float.k:270-272` | rule | none | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |
| 564 | supplied fixed semantics | `reference-semantics/semantics/functions.k:8-13` | syntax | none | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall"` |
| 565 | supplied fixed semantics | `reference-semantics/semantics/functions.k:14-17` | rule | none | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| 566 | supplied fixed semantics | `reference-semantics/semantics/functions.k:18-18` | syntax | none | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 567 | supplied fixed semantics | `reference-semantics/semantics/functions.k:19-26` | rule | none | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` |
| 568 | supplied fixed semantics | `reference-semantics/semantics/functions.k:27-30` | syntax | none | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| 569 | supplied fixed semantics | `reference-semantics/semantics/functions.k:31-32` | syntax | none | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 570 | supplied fixed semantics | `reference-semantics/semantics/functions.k:33-35` | rule | none | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| 571 | supplied fixed semantics | `reference-semantics/semantics/functions.k:36-41` | rule | none | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 572 | supplied fixed semantics | `reference-semantics/semantics/functions.k:42-46` | rule | none | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| 573 | supplied fixed semantics | `reference-semantics/semantics/functions.k:47-49` | rule | none | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| 574 | supplied fixed semantics | `reference-semantics/semantics/functions.k:50-52` | rule | none | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| 575 | supplied fixed semantics | `reference-semantics/semantics/functions.k:53-58` | rule | none | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 576 | supplied fixed semantics | `reference-semantics/semantics/functions.k:59-62` | rule | none | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` |
| 577 | supplied fixed semantics | `reference-semantics/semantics/functions.k:63-63` | rule | none | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 578 | supplied fixed semantics | `reference-semantics/semantics/functions.k:64-67` | rule | none | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes>` |
| 579 | supplied fixed semantics | `reference-semantics/semantics/functions.k:68-77` | rule | priority | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]` |
| 580 | supplied fixed semantics | `reference-semantics/semantics/functions.k:78-79` | rule | none | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| 581 | supplied fixed semantics | `reference-semantics/semantics/functions.k:80-84` | rule | none | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` |
| 582 | supplied fixed semantics | `reference-semantics/semantics/functions.k:85-90` | rule | none | `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |
| 583 | supplied fixed semantics | `reference-semantics/semantics/int.k:7-8` | rule | none | `rule applyUn("-", I:Int) => 0 -Int I` |
| 584 | supplied fixed semantics | `reference-semantics/semantics/int.k:9-10` | rule | none | `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2` |
| 585 | supplied fixed semantics | `reference-semantics/semantics/int.k:11-11` | rule | none | `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 586 | supplied fixed semantics | `reference-semantics/semantics/int.k:12-12` | rule | none | `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 587 | supplied fixed semantics | `reference-semantics/semantics/int.k:13-13` | rule | none | `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2` |
| 588 | supplied fixed semantics | `reference-semantics/semantics/int.k:14-14` | rule | none | `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2` |
| 589 | supplied fixed semantics | `reference-semantics/semantics/int.k:15-15` | rule | none | `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)` |
| 590 | supplied fixed semantics | `reference-semantics/semantics/int.k:16-16` | rule | none | `rule applyBin("` |
| 591 | supplied fixed semantics | `reference-semantics/semantics/int.k:17-18` | rule | none | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 592 | supplied fixed semantics | `reference-semantics/semantics/int.k:19-19` | syntax | function | `syntax Int ::= pyMod(Int, Int) [function]` |
| 593 | supplied fixed semantics | `reference-semantics/semantics/int.k:20-21` | rule | none | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 594 | supplied fixed semantics | `reference-semantics/semantics/int.k:22-22` | rule | none | `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2` |
| 595 | supplied fixed semantics | `reference-semantics/semantics/int.k:23-23` | rule | none | `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2` |
| 596 | supplied fixed semantics | `reference-semantics/semantics/int.k:24-24` | rule | none | `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2` |
| 597 | supplied fixed semantics | `reference-semantics/semantics/int.k:25-25` | rule | none | `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2` |
| 598 | supplied fixed semantics | `reference-semantics/semantics/int.k:26-26` | rule | none | `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2` |
| 599 | supplied fixed semantics | `reference-semantics/semantics/int.k:27-27` | rule | none | `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2` |
| 600 | supplied fixed semantics | `reference-semantics/semantics/iter.k:8-8` | syntax | none | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| 601 | supplied fixed semantics | `reference-semantics/semantics/list.k:9-9` | rule | none | `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>` |
| 602 | supplied fixed semantics | `reference-semantics/semantics/list.k:10-12` | rule | none | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| 603 | supplied fixed semantics | `reference-semantics/semantics/list.k:13-13` | syntax | none | `syntax ApplyK ::= "toList"` |
| 604 | supplied fixed semantics | `reference-semantics/semantics/list.k:14-14` | rule | none | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 605 | supplied fixed semantics | `reference-semantics/semantics/list.k:15-17` | rule | none | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| 606 | supplied fixed semantics | `reference-semantics/semantics/list.k:18-18` | syntax | function, total | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 607 | supplied fixed semantics | `reference-semantics/semantics/list.k:19-19` | rule | none | `rule valSeqConcat(.ValSeq, T:ValSeq)                => T` |
| 608 | supplied fixed semantics | `reference-semantics/semantics/list.k:20-23` | rule | none | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| 609 | supplied fixed semantics | `reference-semantics/semantics/list.k:24-26` | rule | priority | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| 610 | supplied fixed semantics | `reference-semantics/semantics/list.k:27-27` | rule | none | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 611 | supplied fixed semantics | `reference-semantics/semantics/list.k:28-32` | rule | none | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| 612 | supplied fixed semantics | `reference-semantics/semantics/list.k:33-33` | syntax | function, total | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 613 | supplied fixed semantics | `reference-semantics/semantics/list.k:34-34` | rule | none | `rule hasRefVS(.ValSeq)                => false` |
| 614 | supplied fixed semantics | `reference-semantics/semantics/list.k:35-36` | rule | none | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 615 | supplied fixed semantics | `reference-semantics/semantics/list.k:37-38` | syntax | function | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map)        [function]` |
| 616 | supplied fixed semantics | `reference-semantics/semantics/list.k:39-39` | rule | none | `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true` |
| 617 | supplied fixed semantics | `reference-semantics/semantics/list.k:40-40` | rule | none | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false` |
| 618 | supplied fixed semantics | `reference-semantics/semantics/list.k:41-41` | rule | none | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false` |
| 619 | supplied fixed semantics | `reference-semantics/semantics/list.k:42-44` | rule | none | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| 620 | supplied fixed semantics | `reference-semantics/semantics/list.k:45-46` | rule | none | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| 621 | supplied fixed semantics | `reference-semantics/semantics/list.k:47-48` | rule | none | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| 622 | supplied fixed semantics | `reference-semantics/semantics/list.k:49-49` | rule | none | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 623 | supplied fixed semantics | `reference-semantics/semantics/list.k:50-52` | rule | owise | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| 624 | supplied fixed semantics | `reference-semantics/semantics/list.k:53-57` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` |
| 625 | supplied fixed semantics | `reference-semantics/semantics/list.k:58-58` | syntax | none | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 626 | supplied fixed semantics | `reference-semantics/semantics/list.k:59-59` | rule | none | `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 627 | supplied fixed semantics | `reference-semantics/semantics/list.k:60-60` | rule | none | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 628 | supplied fixed semantics | `reference-semantics/semantics/list.k:61-61` | rule | none | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 629 | supplied fixed semantics | `reference-semantics/semantics/list.k:62-62` | rule | none | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 630 | supplied fixed semantics | `reference-semantics/semantics/list.k:63-64` | rule | none | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| 631 | supplied fixed semantics | `reference-semantics/semantics/list.k:65-66` | rule | none | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| 632 | supplied fixed semantics | `reference-semantics/semantics/list.k:67-67` | rule | none | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| 633 | supplied fixed semantics | `reference-semantics/semantics/methods.k:10-12` | syntax | function | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| 634 | supplied fixed semantics | `reference-semantics/semantics/methods.k:13-13` | rule | none | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 635 | supplied fixed semantics | `reference-semantics/semantics/methods.k:14-14` | rule | none | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 636 | supplied fixed semantics | `reference-semantics/semantics/methods.k:15-15` | rule | none | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 637 | supplied fixed semantics | `reference-semantics/semantics/methods.k:16-18` | rule | none | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| 638 | supplied fixed semantics | `reference-semantics/semantics/methods.k:19-19` | rule | none | `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))` |
| 639 | supplied fixed semantics | `reference-semantics/semantics/methods.k:20-20` | rule | none | `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))` |
| 640 | supplied fixed semantics | `reference-semantics/semantics/methods.k:21-25` | rule | none | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| 641 | supplied fixed semantics | `reference-semantics/semantics/methods.k:26-26` | rule | none | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 642 | supplied fixed semantics | `reference-semantics/semantics/methods.k:27-27` | syntax | function, total | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 643 | supplied fixed semantics | `reference-semantics/semantics/methods.k:28-28` | rule | none | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 644 | supplied fixed semantics | `reference-semantics/semantics/methods.k:29-29` | rule | none | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 645 | supplied fixed semantics | `reference-semantics/semantics/methods.k:30-33` | rule | none | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` |
| 646 | supplied fixed semantics | `reference-semantics/semantics/methods.k:34-34` | rule | none | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 647 | supplied fixed semantics | `reference-semantics/semantics/methods.k:35-35` | syntax | function | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 648 | supplied fixed semantics | `reference-semantics/semantics/methods.k:36-36` | rule | none | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 649 | supplied fixed semantics | `reference-semantics/semantics/methods.k:37-38` | rule | none | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| 650 | supplied fixed semantics | `reference-semantics/semantics/methods.k:39-40` | rule | none | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| 651 | supplied fixed semantics | `reference-semantics/semantics/methods.k:41-41` | syntax | function, total | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 652 | supplied fixed semantics | `reference-semantics/semantics/methods.k:42-42` | rule | none | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 653 | supplied fixed semantics | `reference-semantics/semantics/methods.k:43-43` | rule | owise | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 654 | supplied fixed semantics | `reference-semantics/semantics/methods.k:44-46` | rule | none | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| 655 | supplied fixed semantics | `reference-semantics/semantics/methods.k:47-47` | rule | none | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 656 | supplied fixed semantics | `reference-semantics/semantics/methods.k:48-48` | syntax | function, total | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 657 | supplied fixed semantics | `reference-semantics/semantics/methods.k:49-49` | rule | none | `rule trimWS(.IntSeq) => .IntSeq` |
| 658 | supplied fixed semantics | `reference-semantics/semantics/methods.k:50-50` | rule | none | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 659 | supplied fixed semantics | `reference-semantics/semantics/methods.k:51-51` | rule | none | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 660 | supplied fixed semantics | `reference-semantics/semantics/methods.k:52-52` | syntax | function, total | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 661 | supplied fixed semantics | `reference-semantics/semantics/methods.k:53-53` | rule | none | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 662 | supplied fixed semantics | `reference-semantics/semantics/methods.k:54-54` | rule | none | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 663 | supplied fixed semantics | `reference-semantics/semantics/methods.k:55-57` | rule | none | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| 664 | supplied fixed semantics | `reference-semantics/semantics/methods.k:58-60` | rule | none | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| 665 | supplied fixed semantics | `reference-semantics/semantics/methods.k:61-63` | rule | none | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| 666 | supplied fixed semantics | `reference-semantics/semantics/methods.k:64-64` | rule | none | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 667 | supplied fixed semantics | `reference-semantics/semantics/methods.k:65-65` | syntax | function, total | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 668 | supplied fixed semantics | `reference-semantics/semantics/methods.k:66-66` | rule | none | `rule cntOccVS(.ValSeq, _:Val)                => 0` |
| 669 | supplied fixed semantics | `reference-semantics/semantics/methods.k:67-67` | rule | none | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 670 | supplied fixed semantics | `reference-semantics/semantics/methods.k:68-71` | rule | none | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)` |
| 671 | supplied fixed semantics | `reference-semantics/semantics/methods.k:72-74` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| 672 | supplied fixed semantics | `reference-semantics/semantics/methods.k:75-75` | syntax | function | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]` |
| 673 | supplied fixed semantics | `reference-semantics/semantics/methods.k:76-76` | rule | none | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 674 | supplied fixed semantics | `reference-semantics/semantics/methods.k:77-78` | rule | none | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| 675 | supplied fixed semantics | `reference-semantics/semantics/methods.k:79-81` | rule | none | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` |
| 676 | supplied fixed semantics | `reference-semantics/semantics/methods.k:82-82` | syntax | function | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 677 | supplied fixed semantics | `reference-semantics/semantics/methods.k:83-83` | rule | none | `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC` |
| 678 | supplied fixed semantics | `reference-semantics/semantics/methods.k:84-84` | rule | none | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 679 | supplied fixed semantics | `reference-semantics/semantics/methods.k:85-85` | syntax | function, total | `syntax Bool ::= isWSC(Int) [function, total]` |
| 680 | supplied fixed semantics | `reference-semantics/semantics/methods.k:86-88` | rule | none | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| 681 | supplied fixed semantics | `reference-semantics/semantics/methods.k:89-93` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` |
| 682 | supplied fixed semantics | `reference-semantics/semantics/methods.k:94-96` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| 683 | supplied fixed semantics | `reference-semantics/semantics/methods.k:97-97` | syntax | function | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]` |
| 684 | supplied fixed semantics | `reference-semantics/semantics/methods.k:98-98` | rule | none | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)` |
| 685 | supplied fixed semantics | `reference-semantics/semantics/methods.k:99-100` | rule | none | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| 686 | supplied fixed semantics | `reference-semantics/semantics/methods.k:101-103` | rule | none | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| 687 | supplied fixed semantics | `reference-semantics/semantics/methods.k:104-105` | rule | none | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| 688 | supplied fixed semantics | `reference-semantics/semantics/methods.k:106-106` | syntax | function, total | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 689 | supplied fixed semantics | `reference-semantics/semantics/methods.k:107-107` | rule | none | `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq` |
| 690 | supplied fixed semantics | `reference-semantics/semantics/methods.k:108-108` | rule | none | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 691 | supplied fixed semantics | `reference-semantics/semantics/methods.k:109-111` | rule | none | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| 692 | supplied fixed semantics | `reference-semantics/semantics/methods.k:112-112` | syntax | function, total | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 693 | supplied fixed semantics | `reference-semantics/semantics/methods.k:113-114` | rule | none | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 694 | supplied fixed semantics | `reference-semantics/semantics/methods.k:115-115` | syntax | function, total | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 695 | supplied fixed semantics | `reference-semantics/semantics/methods.k:116-117` | rule | none | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 696 | supplied fixed semantics | `reference-semantics/semantics/methods.k:118-118` | syntax | function, total | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 697 | supplied fixed semantics | `reference-semantics/semantics/methods.k:119-120` | rule | none | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 698 | supplied fixed semantics | `reference-semantics/semantics/methods.k:121-121` | syntax | function, total | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 699 | supplied fixed semantics | `reference-semantics/semantics/methods.k:122-123` | rule | none | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 700 | supplied fixed semantics | `reference-semantics/semantics/methods.k:124-124` | syntax | function, total | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 701 | supplied fixed semantics | `reference-semantics/semantics/methods.k:125-125` | rule | none | `rule hasUpper(.IntSeq) => false` |
| 702 | supplied fixed semantics | `reference-semantics/semantics/methods.k:126-127` | rule | none | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 703 | supplied fixed semantics | `reference-semantics/semantics/methods.k:128-128` | syntax | function, total | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 704 | supplied fixed semantics | `reference-semantics/semantics/methods.k:129-129` | rule | none | `rule hasLower(.IntSeq) => false` |
| 705 | supplied fixed semantics | `reference-semantics/semantics/methods.k:130-131` | rule | none | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 706 | supplied fixed semantics | `reference-semantics/semantics/methods.k:132-132` | syntax | function, total | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 707 | supplied fixed semantics | `reference-semantics/semantics/methods.k:133-133` | rule | none | `rule allAlpha(.IntSeq) => true` |
| 708 | supplied fixed semantics | `reference-semantics/semantics/methods.k:134-135` | rule | none | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 709 | supplied fixed semantics | `reference-semantics/semantics/methods.k:136-136` | syntax | function, total | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 710 | supplied fixed semantics | `reference-semantics/semantics/methods.k:137-137` | rule | none | `rule allDigit(.IntSeq) => true` |
| 711 | supplied fixed semantics | `reference-semantics/semantics/methods.k:138-139` | rule | none | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 712 | supplied fixed semantics | `reference-semantics/semantics/methods.k:140-141` | syntax | function, total | `syntax Int ::= lowerC(Int) [function, total]` |
| 713 | supplied fixed semantics | `reference-semantics/semantics/methods.k:142-142` | rule | none | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 714 | supplied fixed semantics | `reference-semantics/semantics/methods.k:143-144` | rule | owise | `rule lowerC(C:Int) => C         [owise]` |
| 715 | supplied fixed semantics | `reference-semantics/semantics/methods.k:145-145` | syntax | function, total | `syntax Int ::= upperC(Int) [function, total]` |
| 716 | supplied fixed semantics | `reference-semantics/semantics/methods.k:146-146` | rule | none | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 717 | supplied fixed semantics | `reference-semantics/semantics/methods.k:147-148` | rule | owise | `rule upperC(C:Int) => C         [owise]` |
| 718 | supplied fixed semantics | `reference-semantics/semantics/methods.k:149-149` | syntax | function, total | `syntax Int ::= swapC(Int) [function, total]` |
| 719 | supplied fixed semantics | `reference-semantics/semantics/methods.k:150-150` | rule | none | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 720 | supplied fixed semantics | `reference-semantics/semantics/methods.k:151-151` | rule | none | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 721 | supplied fixed semantics | `reference-semantics/semantics/methods.k:152-153` | rule | owise | `rule swapC(C:Int) => C         [owise]` |
| 722 | supplied fixed semantics | `reference-semantics/semantics/methods.k:154-154` | syntax | function, total | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 723 | supplied fixed semantics | `reference-semantics/semantics/methods.k:155-155` | rule | none | `rule mapLower(.IntSeq) => .IntSeq` |
| 724 | supplied fixed semantics | `reference-semantics/semantics/methods.k:156-157` | rule | none | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 725 | supplied fixed semantics | `reference-semantics/semantics/methods.k:158-158` | syntax | function, total | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 726 | supplied fixed semantics | `reference-semantics/semantics/methods.k:159-159` | rule | none | `rule mapUpper(.IntSeq) => .IntSeq` |
| 727 | supplied fixed semantics | `reference-semantics/semantics/methods.k:160-161` | rule | none | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 728 | supplied fixed semantics | `reference-semantics/semantics/methods.k:162-162` | syntax | function, total | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 729 | supplied fixed semantics | `reference-semantics/semantics/methods.k:163-163` | rule | none | `rule mapSwap(.IntSeq) => .IntSeq` |
| 730 | supplied fixed semantics | `reference-semantics/semantics/methods.k:164-165` | rule | none | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 731 | supplied fixed semantics | `reference-semantics/semantics/methods.k:166-166` | syntax | function, total | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 732 | supplied fixed semantics | `reference-semantics/semantics/methods.k:167-167` | rule | none | `rule startsWith(.IntSeq, _:IntSeq)               => true` |
| 733 | supplied fixed semantics | `reference-semantics/semantics/methods.k:168-168` | rule | none | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 734 | supplied fixed semantics | `reference-semantics/semantics/methods.k:169-169` | rule | none | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| 735 | supplied fixed semantics | `reference-semantics/semantics/operators.k:10-11` | rule | none | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 736 | supplied fixed semantics | `reference-semantics/semantics/operators.k:12-14` | rule | none | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| 737 | supplied fixed semantics | `reference-semantics/semantics/operators.k:15-15` | context | none | `context Compare(HOLE, _)` |
| 738 | supplied fixed semantics | `reference-semantics/semantics/operators.k:16-16` | context | none | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 739 | supplied fixed semantics | `reference-semantics/semantics/operators.k:17-18` | rule | owise | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 740 | supplied fixed semantics | `reference-semantics/semantics/operators.k:19-19` | rule | none | `rule applyCmp("is",     V:Val, noneV) => V ==K noneV` |
| 741 | supplied fixed semantics | `reference-semantics/semantics/operators.k:20-24` | rule | none | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| 742 | supplied fixed semantics | `reference-semantics/semantics/operators.k:25-27` | rule | priority | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 743 | supplied fixed semantics | `reference-semantics/semantics/operators.k:28-33` | rule | priority | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` |
| 744 | supplied fixed semantics | `reference-semantics/semantics/operators.k:34-37` | rule | priority | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| 745 | supplied fixed semantics | `reference-semantics/semantics/operators.k:38-43` | rule | priority | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| 746 | supplied fixed semantics | `reference-semantics/semantics/operators.k:44-46` | rule | priority | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 747 | supplied fixed semantics | `reference-semantics/semantics/range.k:9-9` | syntax | function, total | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 748 | supplied fixed semantics | `reference-semantics/semantics/range.k:10-11` | rule | none | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 749 | supplied fixed semantics | `reference-semantics/semantics/range.k:12-12` | syntax | function | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 750 | supplied fixed semantics | `reference-semantics/semantics/range.k:13-14` | rule | none | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| 751 | supplied fixed semantics | `reference-semantics/semantics/range.k:15-16` | rule | none | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| 752 | supplied fixed semantics | `reference-semantics/semantics/range.k:17-19` | rule | none | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| 753 | supplied fixed semantics | `reference-semantics/semantics/range.k:20-22` | rule | none | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| 754 | supplied fixed semantics | `reference-semantics/semantics/range.k:23-24` | rule | none | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |
| 755 | supplied fixed semantics | `reference-semantics/semantics/set.k:8-10` | syntax | none | `syntax Val ::= setV(IntSeq)` |
| 756 | supplied fixed semantics | `reference-semantics/semantics/set.k:11-11` | syntax | function, total | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 757 | supplied fixed semantics | `reference-semantics/semantics/set.k:12-12` | rule | none | `rule codeIn(_:Int, .IntSeq)                => false` |
| 758 | supplied fixed semantics | `reference-semantics/semantics/set.k:13-15` | rule | none | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| 759 | supplied fixed semantics | `reference-semantics/semantics/set.k:16-17` | syntax | function, total | `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] \| dedupFrom(IntSeq, IntSeq)  [function, total]` |
| 760 | supplied fixed semantics | `reference-semantics/semantics/set.k:18-18` | rule | none | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 761 | supplied fixed semantics | `reference-semantics/semantics/set.k:19-19` | rule | none | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 762 | supplied fixed semantics | `reference-semantics/semantics/set.k:20-21` | rule | none | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| 763 | supplied fixed semantics | `reference-semantics/semantics/set.k:22-24` | rule | none | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| 764 | supplied fixed semantics | `reference-semantics/semantics/set.k:25-25` | syntax | function, total | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 765 | supplied fixed semantics | `reference-semantics/semantics/set.k:26-26` | rule | none | `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)` |
| 766 | supplied fixed semantics | `reference-semantics/semantics/set.k:27-30` | rule | none | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| 767 | supplied fixed semantics | `reference-semantics/semantics/set.k:31-31` | syntax | function, total | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 768 | supplied fixed semantics | `reference-semantics/semantics/set.k:32-32` | rule | none | `rule subsetCodes(.IntSeq, _:IntSeq)                => true` |
| 769 | supplied fixed semantics | `reference-semantics/semantics/set.k:33-34` | rule | none | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 770 | supplied fixed semantics | `reference-semantics/semantics/set.k:35-35` | syntax | function, total | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 771 | supplied fixed semantics | `reference-semantics/semantics/set.k:36-38` | rule | none | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| 772 | supplied fixed semantics | `reference-semantics/semantics/set.k:39-39` | rule | none | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| 773 | supplied fixed semantics | `reference-semantics/semantics/sort.k:18-18` | syntax | function, total, symbol, no-evaluators | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 774 | supplied fixed semantics | `reference-semantics/semantics/sort.k:19-19` | syntax | function | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 775 | supplied fixed semantics | `reference-semantics/semantics/sort.k:20-20` | rule | concrete | `rule sortVS(.ValSeq)                => .ValSeq          [concrete]` |
| 776 | supplied fixed semantics | `reference-semantics/semantics/sort.k:21-21` | rule | concrete | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 777 | supplied fixed semantics | `reference-semantics/semantics/sort.k:22-22` | rule | concrete | `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]` |
| 778 | supplied fixed semantics | `reference-semantics/semantics/sort.k:23-23` | rule | concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 779 | supplied fixed semantics | `reference-semantics/semantics/sort.k:24-25` | rule | concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]` |
| 780 | supplied fixed semantics | `reference-semantics/semantics/sort.k:26-26` | syntax | function | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 781 | supplied fixed semantics | `reference-semantics/semantics/sort.k:27-27` | rule | concrete | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 782 | supplied fixed semantics | `reference-semantics/semantics/sort.k:28-28` | rule | concrete | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 783 | supplied fixed semantics | `reference-semantics/semantics/sort.k:29-30` | rule | concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| 784 | supplied fixed semantics | `reference-semantics/semantics/sort.k:31-35` | rule | concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` |
| 785 | supplied fixed semantics | `reference-semantics/semantics/sort.k:36-39` | rule | none | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` |
| 786 | supplied fixed semantics | `reference-semantics/semantics/sort.k:40-48` | rule | priority | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` |
| 787 | supplied fixed semantics | `reference-semantics/semantics/sort.k:49-50` | syntax | function, total, symbol, no-evaluators | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 788 | supplied fixed semantics | `reference-semantics/semantics/sort.k:51-52` | syntax | function, total | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| 789 | supplied fixed semantics | `reference-semantics/semantics/sort.k:53-53` | rule | none | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 790 | supplied fixed semantics | `reference-semantics/semantics/sort.k:54-54` | rule | none | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 791 | supplied fixed semantics | `reference-semantics/semantics/sort.k:55-56` | rule | none | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 792 | supplied fixed semantics | `reference-semantics/semantics/sort.k:57-57` | syntax | function, total | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 793 | supplied fixed semantics | `reference-semantics/semantics/sort.k:58-58` | rule | none | `rule condRev(S:ValSeq, false) => S` |
| 794 | supplied fixed semantics | `reference-semantics/semantics/sort.k:59-60` | rule | none | `rule condRev(S:ValSeq, true)  => revVS(S)` |
| 795 | supplied fixed semantics | `reference-semantics/semantics/sort.k:61-62` | rule | none | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| 796 | supplied fixed semantics | `reference-semantics/semantics/sort.k:63-64` | rule | none | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| 797 | supplied fixed semantics | `reference-semantics/semantics/sort.k:65-71` | rule | none | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` |
| 798 | supplied fixed semantics | `reference-semantics/semantics/str.k:8-8` | rule | none | `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>` |
| 799 | supplied fixed semantics | `reference-semantics/semantics/str.k:9-12` | rule | none | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` |
| 800 | supplied fixed semantics | `reference-semantics/semantics/str.k:13-13` | syntax | function | `syntax IntSeq ::= strToCodes(String) [function]` |
| 801 | supplied fixed semantics | `reference-semantics/semantics/str.k:14-14` | rule | none | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 802 | supplied fixed semantics | `reference-semantics/semantics/str.k:15-15` | rule | none | `rule strToCodes("") => .IntSeq` |
| 803 | supplied fixed semantics | `reference-semantics/semantics/str.k:16-19` | rule | none | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` |
| 804 | supplied fixed semantics | `reference-semantics/semantics/str.k:20-20` | syntax | function, total | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 805 | supplied fixed semantics | `reference-semantics/semantics/str.k:21-21` | rule | none | `rule seqConcat(.IntSeq, T:IntSeq)                => T` |
| 806 | supplied fixed semantics | `reference-semantics/semantics/str.k:22-23` | rule | none | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 807 | supplied fixed semantics | `reference-semantics/semantics/str.k:24-24` | rule | none | `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 808 | supplied fixed semantics | `reference-semantics/semantics/str.k:25-25` | rule | none | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 809 | supplied fixed semantics | `reference-semantics/semantics/str.k:26-28` | rule | none | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| 810 | supplied fixed semantics | `reference-semantics/semantics/str.k:29-29` | rule | none | `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 811 | supplied fixed semantics | `reference-semantics/semantics/str.k:30-31` | rule | none | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 812 | supplied fixed semantics | `reference-semantics/semantics/str.k:32-32` | syntax | function, total | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 813 | supplied fixed semantics | `reference-semantics/semantics/str.k:33-33` | rule | none | `rule strPrefix(.IntSeq, _:IntSeq)               => true` |
| 814 | supplied fixed semantics | `reference-semantics/semantics/str.k:34-34` | rule | none | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 815 | supplied fixed semantics | `reference-semantics/semantics/str.k:35-36` | rule | none | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 816 | supplied fixed semantics | `reference-semantics/semantics/str.k:37-37` | syntax | function, total | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 817 | supplied fixed semantics | `reference-semantics/semantics/str.k:38-38` | rule | none | `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)` |
| 818 | supplied fixed semantics | `reference-semantics/semantics/str.k:39-39` | rule | none | `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)` |
| 819 | supplied fixed semantics | `reference-semantics/semantics/str.k:40-47` | rule | none | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` |
| 820 | supplied fixed semantics | `reference-semantics/semantics/str.k:48-48` | syntax | function, total | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 821 | supplied fixed semantics | `reference-semantics/semantics/str.k:49-49` | rule | none | `rule strLt(.IntSeq, .IntSeq)                => false` |
| 822 | supplied fixed semantics | `reference-semantics/semantics/str.k:50-50` | rule | none | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 823 | supplied fixed semantics | `reference-semantics/semantics/str.k:51-51` | rule | none | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 824 | supplied fixed semantics | `reference-semantics/semantics/str.k:52-52` | rule | none | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B` |
| 825 | supplied fixed semantics | `reference-semantics/semantics/str.k:53-53` | rule | none | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B` |
| 826 | supplied fixed semantics | `reference-semantics/semantics/str.k:54-55` | rule | none | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 827 | supplied fixed semantics | `reference-semantics/semantics/str.k:56-56` | rule | none | `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 828 | supplied fixed semantics | `reference-semantics/semantics/str.k:57-57` | rule | none | `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 829 | supplied fixed semantics | `reference-semantics/semantics/str.k:58-58` | rule | none | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 830 | supplied fixed semantics | `reference-semantics/semantics/str.k:59-59` | rule | none | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| 831 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:11-11` | syntax | function, total | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 832 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:12-12` | rule | none | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V` |
| 833 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:13-15` | rule | none | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| 834 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:16-16` | syntax | function | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 835 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:17-17` | rule | none | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C` |
| 836 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:18-20` | rule | none | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| 837 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:21-21` | syntax | function, total | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 838 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:22-22` | rule | none | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 839 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:23-26` | rule | none | `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0` |
| 840 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:27-27` | context | none | `context Subscript(HOLE, _)` |
| 841 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:28-30` | context | none | `context Subscript(_:Val, HOLE:Expr)` |
| 842 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:31-34` | rule | priority | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 843 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:35-36` | rule | none | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 844 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:37-37` | syntax | function | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 845 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:38-38` | rule | none | `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 846 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:39-39` | rule | none | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 847 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:40-43` | rule | none | `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` |
| 848 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:44-48` | syntax | none | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| 849 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:49-49` | syntax | none | `syntax OptInt ::= "noB" \| someB(Int)` |
| 850 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:50-50` | rule | none | `rule <k> #evalB(NoBound)  => noB ... </k>` |
| 851 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:51-51` | rule | none | `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>` |
| 852 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:52-53` | rule | none | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 853 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:54-54` | rule | none | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 854 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:55-55` | rule | none | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 855 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:56-57` | rule | none | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| 856 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:58-60` | rule | priority | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| 857 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:61-62` | rule | none | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 858 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:63-63` | syntax | function | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 859 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:64-65` | rule | none | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 860 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:66-67` | rule | none | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 861 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:68-71` | rule | none | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` |
| 862 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:72-72` | syntax | function, total | `syntax Int ::= slStep(OptInt) [function, total]` |
| 863 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:73-73` | rule | none | `rule slStep(noB)          => 1` |
| 864 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:74-75` | rule | none | `rule slStep(someB(S:Int)) => S` |
| 865 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:76-76` | syntax | function | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 866 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:77-78` | rule | none | `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| 867 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:79-80` | rule | none | `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0` |
| 868 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:81-82` | rule | none | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 869 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:83-83` | syntax | function | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 870 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:84-85` | rule | none | `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0` |
| 871 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:86-87` | rule | none | `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| 872 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:88-89` | rule | none | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 873 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:90-90` | syntax | function, total | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 874 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:91-92` | rule | none | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0` |
| 875 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:93-95` | rule | none | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| 876 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:96-96` | syntax | function, total | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 877 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:97-98` | rule | none | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| 878 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:99-101` | rule | none | `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| 879 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:102-102` | syntax | function, total | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 880 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:103-104` | rule | none | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN` |
| 881 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:105-108` | rule | none | `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` |
| 882 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:109-109` | syntax | function | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 883 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:110-112` | rule | none | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 884 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:113-115` | rule | none | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 885 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:116-116` | syntax | function | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 886 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:117-119` | rule | none | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 887 | supplied fixed semantics | `reference-semantics/semantics/subscript.k:120-121` | rule | none | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 888 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:9-31` | syntax | strict, seqstrict | `syntax Expr ::= "Int"      "(" Int ")" \| "Float"    "(" Float ")" \| "Bool"     "(" Bool ")" \| "Name"     "(" String ")" \| "Str"      "(" String ")" \| "UnaryOp"  "(" String "," Expr ")" [strict(2)] \| "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp"    "(" String "," Exprs ")" \| "ListExpr"  "(" Exprs ")" \| "DictExpr"  "(" Entries ")" \| "ListComp"  "(" Expr "," CompFors ")" [macro] \| "GenExp"    "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda"    "(" Params "," Expr ")" \| "KwArg"     "(" String "," Expr ")" \| "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call"      "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare"   "(" Expr "," CmpOp ")"` |
| 889 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:32-32` | syntax | none | `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"` |
| 890 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:33-33` | syntax | none | `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"` |
| 891 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:34-34` | syntax | none | `syntax Entries  ::= List{Entry, ","}` |
| 892 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:35-35` | syntax | none | `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 893 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:36-36` | syntax | none | `syntax CompFors ::= List{CompFor, ""}` |
| 894 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:37-37` | syntax | none | `syntax Exprs    ::= List{Expr, ","}` |
| 895 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:38-38` | syntax | none | `syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 896 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:39-40` | syntax | none | `syntax Bound    ::= Expr \| "NoBound"` |
| 897 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:41-55` | syntax | strict | `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] \| "Import"    "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While"     "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return"    "(" Expr ")" [strict] \| "Assert"    "(" Expr ")" [strict] \| "Expr"      "(" Expr ")" [strict] \| "FuncDef"   "(" String "," Params "," Stmts ")" \| "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` |
| 898 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:56-56` | syntax | none | `syntax Stmts      ::= List{Stmt, ""}` |
| 899 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:57-57` | syntax | none | `syntax Params     ::= "Params" "(" ParamNames ")"` |
| 900 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:58-58` | syntax | none | `syntax CellVars   ::= "CellVars" "(" ParamNames ")"` |
| 901 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:59-59` | syntax | none | `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"` |
| 902 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:60-60` | syntax | none | `syntax ParamNames ::= List{String, ","}` |
| 903 | supplied fixed semantics | `reference-semantics/semantics/syntax.k:61-61` | syntax | none | `syntax Module     ::= "Module" "(" Stmts ")"` |
| 904 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:10-10` | rule | none | `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>` |
| 905 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:11-13` | rule | none | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| 906 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:14-14` | syntax | none | `syntax ApplyK ::= "toTuple"` |
| 907 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:15-15` | rule | none | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 908 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:16-17` | rule | none | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 909 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:18-19` | rule | none | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| 910 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:20-20` | rule | none | `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 911 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:21-22` | rule | none | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| 912 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:23-23` | rule | none | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 913 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:24-24` | syntax | function | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 914 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:25-25` | rule | none | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 915 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:26-27` | rule | none | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| 916 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:28-30` | rule | none | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| 917 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:31-31` | syntax | none | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 918 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:32-34` | rule | none | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 919 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:35-41` | rule | priority | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 920 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:42-42` | rule | none | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 921 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:43-43` | rule | none | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 922 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:44-48` | rule | priority | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 923 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:49-49` | syntax | none | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 924 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:50-50` | rule | none | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 925 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:51-51` | rule | none | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 926 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:52-54` | rule | priority | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 927 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:55-56` | rule | none | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| 928 | supplied fixed semantics | `reference-semantics/semantics/tuple.k:57-57` | rule | none | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| 929 | proof-local | `verification.k:9-9` | syntax | function | `syntax Stmts ::= "MOVE-ONE-BALL-LOOP-BODY" [function]` |
| 930 | proof-local | `verification.k:10-15` | rule | none | `rule MOVE-ONE-BALL-LOOP-BODY => If(Compare(Name("current"), CmpOp("<", Name("previous"))), AugAssign(Name("drops"), "+", Int(1)), .Stmts) Assign(Name("previous"), Name("current"))` |
| 931 | proof-local | `verification.k:16-16` | syntax | function | `syntax Stmts ::= "MOVE-ONE-BALL-BODY" [function]` |
| 932 | proof-local | `verification.k:17-29` | rule | none | `rule MOVE-ONE-BALL-BODY => If(Compare(Call(Name("len"), Name("arr")), CmpOp("==", Int(0))), Return(Bool(true)), .Stmts) Assign(Name("drops"), Int(0)) Assign(Name("first"), Subscript(Name("arr"), Int(0))) Assign(Name("previous"), Name("first")) For(Name("current"), Name("arr"), MOVE-ONE-BALL-LOOP-BODY) If(Compare(Name("first"), CmpOp("<", Name("previous"))), AugAssign(Name("drops"), "+", Int(1)), .Stmts) Return(Compare(Name("drops"), CmpOp("<", Int(2))))` |
| 933 | proof-local | `verification.k:30-30` | syntax | function | `syntax Val ::= "MOVE-ONE-BALL-CLOSURE" [function]` |
| 934 | proof-local | `verification.k:31-36` | rule | none | `rule MOVE-ONE-BALL-CLOSURE => closureVal("arr", MOVE-ONE-BALL-BODY, 0)` |
| 935 | proof-local | `verification.k:37-42` | syntax | none | `syntax ValSeq ::= intVals(IntSeq)` |
| 936 | proof-local | `verification.k:43-44` | rule | priority | `rule <k> #iterNext(list(intVals(.IntSeq))) => #iterDone ... </k> [priority(40)]` |
| 937 | proof-local | `verification.k:45-48` | rule | priority | `rule <k> #iterNext(list(intVals(iCons(I:Int, IS:IntSeq)))) => #iterYield(I, list(intVals(IS))) ... </k> [priority(40)]` |
| 938 | proof-local | `verification.k:49-52` | rule | priority | `rule <k> #applyK(toCall(builtinV("len")), (list(intVals(.IntSeq)), .Vals)) => 0 ... </k> [priority(40)]` |
| 939 | proof-local | `verification.k:53-59` | rule | priority | `rule <k> #applyK(toCall(builtinV("len")), (list(intVals(iCons(_I:Int, _IS:IntSeq))), .Vals)) => 1 ... </k> [priority(40)]` |
| 940 | proof-local | `verification.k:60-66` | rule | priority | `rule <k> Subscript(list(intVals(iCons(I:Int, _IS:IntSeq))), 0) => I ... </k> [priority(40)]` |
| 941 | proof-local | `verification.k:67-67` | syntax | function, total | `syntax Int ::= addDrop(Int, Int, Int) [function, total]` |
| 942 | proof-local | `verification.k:68-70` | rule | none | `rule addDrop(C:Int, P:Int, D:Int) => D +Int (#if C <Int P #then 1 #else 0 #fi)` |
| 943 | proof-local | `verification.k:71-71` | syntax | function, total | `syntax Int ::= scanDrops(ValSeq, Int, Int) [function, total]` |
| 944 | proof-local | `verification.k:72-72` | rule | none | `rule scanDrops(.ValSeq, _P:Int, D:Int) => D` |
| 945 | proof-local | `verification.k:73-74` | rule | none | `rule scanDrops(vCons(C:Int, R:ValSeq), P:Int, D:Int) => scanDrops(R, C, addDrop(C, P, D))` |
| 946 | proof-local | `verification.k:75-75` | rule | none | `rule scanDrops(intVals(.IntSeq), _P:Int, D:Int) => D` |
| 947 | proof-local | `verification.k:76-78` | rule | none | `rule scanDrops(intVals(iCons(C:Int, IS:IntSeq)), P:Int, D:Int) => scanDrops(intVals(IS), C, addDrop(C, P, D))` |
| 948 | proof-local | `verification.k:79-79` | syntax | function, total | `syntax Int ::= scanLast(ValSeq, Int) [function, total]` |
| 949 | proof-local | `verification.k:80-80` | rule | none | `rule scanLast(.ValSeq, P:Int) => P` |
| 950 | proof-local | `verification.k:81-82` | rule | none | `rule scanLast(vCons(C:Int, R:ValSeq), _P:Int) => scanLast(R, C)` |
| 951 | proof-local | `verification.k:83-83` | rule | none | `rule scanLast(intVals(.IntSeq), P:Int) => P` |
| 952 | proof-local | `verification.k:84-86` | rule | none | `rule scanLast(intVals(iCons(C:Int, IS:IntSeq)), _P:Int) => scanLast(intVals(IS), C)` |
| 953 | proof-local | `verification.k:87-87` | syntax | function, total | `syntax Int ::= circularDrops(Int, ValSeq) [function, total]` |
| 954 | proof-local | `verification.k:88-90` | rule | none | `rule circularDrops(F:Int, VS:ValSeq) => addDrop(F, scanLast(VS, F), scanDrops(VS, F, 0))` |
| 955 | proof-local | `verification.k:91-91` | syntax | function, total | `syntax Bool ::= moveOneBallSpec(ValSeq) [function, total]` |
| 956 | proof-local | `verification.k:92-92` | rule | none | `rule moveOneBallSpec(.ValSeq) => true` |
| 957 | proof-local | `verification.k:93-94` | rule | none | `rule moveOneBallSpec(vCons(F:Int, R:ValSeq)) => circularDrops(F, vCons(F, R)) <Int 2` |
| 958 | proof-local | `verification.k:95-95` | rule | none | `rule moveOneBallSpec(intVals(.IntSeq)) => true` |
| 959 | proof-local | `verification.k:96-98` | rule | none | `rule moveOneBallSpec(intVals(iCons(F:Int, IS:IntSeq))) => circularDrops(F, intVals(iCons(F, IS))) <Int 2` |
| 960 | proof-claim | `spec.k:9-42` | claim | none | `claim [move-one-ball-loop-induction]: <k> #loop(list(intVals(iCons(C:Int, IS:IntSeq))), Name("current"), MOVE-ONE-BALL-LOOP-BODY) ~> KONT:K => KONT </k> <env> 1 </env> <scopes> -1 \|-> BUILTINS:Scope 0 \|-> MODSCOPE:Scope 1 \|-> scope( "arr" \|-> ARR:Val "drops" \|-> D:Int "first" \|-> F:Int "previous" \|-> P:Int "current" \|-> _OLD:Int, parent(0)) => -1 \|-> BUILTINS 0 \|-> MODSCOPE 1 \|-> scope( "arr" \|-> ARR "drops" \|-> scanDrops(intVals(iCons(C, IS)), P, D) "first" \|-> F "previous" \|-> scanLast(intVals(iCons(C, IS)), P) "current" \|-> scanLast(intVals(iCons(C, IS)), P), parent(0)) </scopes>` |
| 961 | proof-claim | `spec.k:43-76` | claim | none | `claim [move-one-ball-loop-entry]: <k> #loop(list(intVals(iCons(C:Int, IS:IntSeq))), Name("current"), MOVE-ONE-BALL-LOOP-BODY) ~> KONT:K => KONT </k> <env> 1 </env> <scopes> -1 \|-> BUILTINS:Scope 0 \|-> MODSCOPE:Scope 1 \|-> scope( "arr" \|-> ARR:Val "drops" \|-> D:Int "first" \|-> F:Int "previous" \|-> P:Int, parent(0)) => -1 \|-> BUILTINS 0 \|-> MODSCOPE 1 \|-> scope( "arr" \|-> ARR "drops" \|-> scanDrops(intVals(iCons(C, IS)), P, D) "first" \|-> F "previous" \|-> scanLast(intVals(iCons(C, IS)), P) "current" \|-> scanLast(intVals(iCons(C, IS)), P), parent(0)) </scopes>` |
| 962 | proof-claim | `spec.k:77-96` | claim | none | `claim [move-one-ball-correct]: <k> Call(Name("move_one_ball"), list(intVals(IS:IntSeq))) => moveOneBallSpec(intVals(IS)) </k> <env> 0 </env> <scopes> 0  \|-> scope( "move_one_ball" \|-> MOVE-ONE-BALL-CLOSURE, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code>` |

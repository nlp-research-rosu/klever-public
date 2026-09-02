# Exhaustive local K declaration and rule inventory

Generated from the clean scratch source copy. Each entry contains the exact
source line range and a whitespace-normalized rendering of the complete
top-level statement.

## Counts

- Source files: 26
- `configuration` statements: 1
- `syntax` statements: 230
- `context` statements: 5
- `rule` statements: 698
- `claim` statements: 1
- Entries flagged `function`: 149
- Entries flagged `functional`: 0
- Entries flagged `total`: 107
- Entries flagged `symbol`: 25
- Entries flagged `no-evaluators`: 22
- Entries flagged `priority`: 45
- Entries flagged `simplification`: 0
- Entries flagged `concrete`: 35
- Entries flagged `owise`: 26
- Entries flagged `macro`: 4
- Entries flagged `hook`: 0
- Entries flagged `operational`: 238
- Entries flagged `equational/pure`: 460

## Per-file statement counts

| File | configuration | syntax | context | rule | claim |
|---|---:|---:|---:|---:|---:|
| `reference-semantics/semantics/assert.k` | 0 | 0 | 0 | 3 | 0 |
| `reference-semantics/semantics/bool.k` | 0 | 0 | 1 | 13 | 0 |
| `reference-semantics/semantics/builtins.k` | 0 | 38 | 0 | 137 | 0 |
| `reference-semantics/semantics/call.k` | 0 | 3 | 0 | 21 | 0 |
| `reference-semantics/semantics/comprehension.k` | 0 | 3 | 0 | 7 | 0 |
| `reference-semantics/semantics/concrete.k` | 0 | 5 | 0 | 16 | 0 |
| `reference-semantics/semantics/controls.k` | 0 | 3 | 0 | 34 | 0 |
| `reference-semantics/semantics/core.k` | 1 | 37 | 0 | 46 | 0 |
| `reference-semantics/semantics/dict.k` | 0 | 12 | 0 | 28 | 0 |
| `reference-semantics/semantics/float.k` | 0 | 34 | 0 | 121 | 0 |
| `reference-semantics/semantics/functions.k` | 0 | 4 | 0 | 15 | 0 |
| `reference-semantics/semantics/int.k` | 0 | 1 | 0 | 16 | 0 |
| `reference-semantics/semantics/iter.k` | 0 | 1 | 0 | 0 | 0 |
| `reference-semantics/semantics/list.k` | 0 | 5 | 0 | 27 | 0 |
| `reference-semantics/semantics/methods.k` | 0 | 27 | 0 | 75 | 0 |
| `reference-semantics/semantics/operators.k` | 0 | 0 | 2 | 10 | 0 |
| `reference-semantics/semantics/range.k` | 0 | 2 | 0 | 6 | 0 |
| `reference-semantics/semantics/set.k` | 0 | 6 | 0 | 12 | 0 |
| `reference-semantics/semantics/sort.k` | 0 | 6 | 0 | 19 | 0 |
| `reference-semantics/semantics/str.k` | 0 | 5 | 0 | 28 | 0 |
| `reference-semantics/semantics/subscript.k` | 0 | 15 | 2 | 40 | 0 |
| `reference-semantics/semantics/syntax.k` | 0 | 16 | 0 | 0 | 0 |
| `reference-semantics/semantics/tuple.k` | 0 | 4 | 0 | 21 | 0 |
| `reference-semantics/semantics.k` | 0 | 0 | 0 | 0 | 0 |
| `verification.k` | 0 | 3 | 0 | 3 | 0 |
| `spec.k` | 0 | 0 | 0 | 0 | 1 |

## `reference-semantics/semantics/assert.k`

- `rule` lines 6-7; flags: `operational` — `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)`
- `rule` lines 8-11; flags: `operational` — `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)`
- `rule` lines 13-15; flags: `priority, operational` — `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## `reference-semantics/semantics/bool.k`

- `rule` lines 8; flags: `equational/pure` — `rule applyUn("not", V:Val) => notBool truthy(V)`
- `rule` lines 10; flags: `equational/pure` — `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`
- `rule` lines 11; flags: `equational/pure` — `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2`
- `context` lines 16; flags: `none` — `context BoolOp(_, (HOLE:Expr, _:Exprs))`
- `rule` lines 17; flags: `operational` — `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`
- `rule` lines 18-19; flags: `operational` — `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)`
- `rule` lines 20-21; flags: `operational` — `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)`
- `rule` lines 22-23; flags: `operational` — `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)`
- `rule` lines 24-25; flags: `operational` — `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)`
- `rule` lines 29-30; flags: `priority, operational` — `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`
- `rule` lines 31-34; flags: `priority, operational` — `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`
- `rule` lines 35-38; flags: `priority, operational` — `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`
- `rule` lines 39-42; flags: `priority, operational` — `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`
- `rule` lines 43-46; flags: `priority, operational` — `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`

## `reference-semantics/semantics/builtins.k`

- `syntax` lines 17; flags: `function` — `syntax Val ::= applyBuiltin(String, Vals) [function]`
- `syntax` lines 20; flags: `function` — `syntax Int ::= seqLen(Val) [function]`
- `rule` lines 21; flags: `equational/pure` — `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`
- `rule` lines 22; flags: `equational/pure` — `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)`
- `rule` lines 23; flags: `equational/pure` — `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)`
- `rule` lines 24; flags: `equational/pure` — `rule seqLen(str(IS:IntSeq))                   => isLen(IS)`
- `rule` lines 25; flags: `equational/pure` — `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)`
- `rule` lines 26; flags: `equational/pure` — `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)`
- `rule` lines 32; flags: `operational` — `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>`
- `rule` lines 33; flags: `operational` — `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`
- `rule` lines 34; flags: `operational` — `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>`
- `rule` lines 35; flags: `operational` — `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>`
- `syntax` lines 36; flags: `function, total` — `syntax ValSeq ::= charsOf(IntSeq) [function, total]`
- `rule` lines 37; flags: `equational/pure` — `rule charsOf(.IntSeq)                => .ValSeq`
- `rule` lines 38; flags: `equational/pure` — `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))`
- `rule` lines 41; flags: `equational/pure` — `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))`
- `rule` lines 44; flags: `equational/pure` — `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)`
- `syntax` lines 47; flags: `none` — `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`
- `rule` lines 48; flags: `operational` — `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`
- `rule` lines 49; flags: `operational` — `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`
- `rule` lines 50-52; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)`
- `syntax` lines 54; flags: `function` — `syntax Int ::= intOf(Val) [function]`
- `rule` lines 55; flags: `equational/pure` — `rule intOf(I:Int)  => I`
- `rule` lines 56; flags: `equational/pure` — `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi`
- `syntax` lines 59; flags: `none` — `syntax KItem ::= #allAcc(Iterable) | "#allCont"`
- `rule` lines 60; flags: `operational` — `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`
- `rule` lines 61; flags: `operational` — `rule <k> #iterDone ~> #allCont => true ... </k>`
- `rule` lines 62-63; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)`
- `rule` lines 64-65; flags: `operational` — `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)`
- `syntax` lines 67; flags: `none` — `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`
- `rule` lines 68; flags: `operational` — `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`
- `rule` lines 69; flags: `operational` — `rule <k> #iterDone ~> #anyCont => false ... </k>`
- `rule` lines 70-71; flags: `operational` — `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)`
- `rule` lines 72-73; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)`
- `syntax` lines 76; flags: `none` — `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`
- `rule` lines 77; flags: `operational` — `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`
- `rule` lines 78-79; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)`
- `rule` lines 80; flags: `operational` — `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`
- `rule` lines 81; flags: `operational` — `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`
- `rule` lines 82-84; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)`
- `syntax` lines 86; flags: `none` — `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`
- `rule` lines 87; flags: `operational` — `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`
- `rule` lines 88-89; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)`
- `rule` lines 90; flags: `operational` — `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`
- `rule` lines 91; flags: `operational` — `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`
- `rule` lines 92-94; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)`
- `syntax` lines 97; flags: `function` — `syntax Int ::= maxVals(Int, Vals) [function]`
- `rule` lines 98; flags: `equational/pure` — `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`
- `rule` lines 99; flags: `equational/pure` — `rule maxVals(M:Int, .Vals)           => M`
- `rule` lines 100; flags: `equational/pure` — `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`
- `syntax` lines 102; flags: `function` — `syntax Int ::= minVals(Int, Vals) [function]`
- `rule` lines 103; flags: `equational/pure` — `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`
- `rule` lines 104; flags: `equational/pure` — `rule minVals(M:Int, .Vals)           => M`
- `rule` lines 105; flags: `equational/pure` — `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)`
- `rule` lines 108-109; flags: `equational/pure` — `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0`
- `rule` lines 111-113; flags: `equational/pure` — `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0`
- `syntax` lines 114; flags: `function, total` — `syntax IntSeq ::= binCodes(Int) [function, total]`
- `rule` lines 115; flags: `equational/pure` — `rule binCodes(0) => iCons(48, .IntSeq)`
- `rule` lines 116; flags: `equational/pure` — `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`
- `syntax` lines 117; flags: `function, total` — `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`
- `rule` lines 118; flags: `equational/pure` — `rule binAcc(0, ACC:IntSeq) => ACC`
- `rule` lines 119-121; flags: `equational/pure` — `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0`
- `rule` lines 124-125; flags: `operational` — `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`
- `syntax` lines 126; flags: `function, total` — `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`
- `rule` lines 127; flags: `equational/pure` — `rule enumVS(.ValSeq, _:Int) => .ValSeq`
- `rule` lines 128-129; flags: `equational/pure` — `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))`
- `rule` lines 132-133; flags: `operational` — `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`
- `syntax` lines 134; flags: `function, total` — `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`
- `rule` lines 135; flags: `equational/pure` — `rule mapStrVS(.ValSeq) => .ValSeq`
- `rule` lines 136; flags: `equational/pure` — `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`
- `rule` lines 137; flags: `equational/pure` — `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))`
- `rule` lines 140; flags: `equational/pure` — `rule applyBuiltin("int", I:Int, .Vals) => I`
- `rule` lines 143; flags: `equational/pure` — `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`
- `rule` lines 144-145; flags: `equational/pure` — `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128`
- `rule` lines 148; flags: `equational/pure` — `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))`
- `rule` lines 149; flags: `equational/pure` — `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)`
- `rule` lines 152-153; flags: `equational/pure` — `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57`
- `rule` lines 156-157; flags: `equational/pure` — `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2`
- `syntax` lines 158; flags: `function, total` — `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`
- `rule` lines 159; flags: `equational/pure` — `rule intDigAcc(.IntSeq, ACC:Int)             => ACC`
- `rule` lines 160; flags: `equational/pure` — `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))`
- `rule` lines 163; flags: `equational/pure` — `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`
- `rule` lines 164; flags: `equational/pure` — `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)`
- `rule` lines 167-168; flags: `operational` — `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`
- `rule` lines 169; flags: `operational` — `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>`
- `rule` lines 170; flags: `operational` — `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`
- `rule` lines 171-172; flags: `operational` — `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`
- `rule` lines 173; flags: `operational` — `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>`
- `rule` lines 174; flags: `operational` — `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>`
- `rule` lines 177; flags: `equational/pure` — `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)`
- `rule` lines 178; flags: `equational/pure` — `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)`
- `rule` lines 179-180; flags: `equational/pure` — `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0`
- `rule` lines 187; flags: `equational/pure` — `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`
- `syntax` lines 188; flags: `function` — `syntax Int ::= evalArith(IntSeq) [function]`
- `rule` lines 189-190; flags: `equational/pure` — `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`
- `syntax` lines 192; flags: `none` — `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`
- `syntax` lines 194; flags: `function, total` — `syntax Bool ::= evDigit(Int) [function, total]`
- `rule` lines 195; flags: `equational/pure` — `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`
- `syntax` lines 196; flags: `function, total` — `syntax Bool ::= evHead42(IntSeq) [function, total]`
- `rule` lines 197; flags: `equational/pure` — `rule evHead42(iCons(42, _:IntSeq)) => true`
- `rule` lines 198; flags: `owise, equational/pure` — `rule evHead42(_:IntSeq)            => false [owise]`
- `syntax` lines 199; flags: `function, total` — `syntax Bool ::= evHead47(IntSeq) [function, total]`
- `rule` lines 200; flags: `equational/pure` — `rule evHead47(iCons(47, _:IntSeq)) => true`
- `rule` lines 201; flags: `owise, equational/pure` — `rule evHead47(_:IntSeq)            => false [owise]`
- `syntax` lines 203; flags: `function, total` — `syntax OpSeq ::= tokOps(IntSeq) [function, total]`
- `rule` lines 204; flags: `equational/pure` — `rule tokOps(.IntSeq)                 => .OpSeq`
- `rule` lines 205; flags: `equational/pure` — `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)`
- `rule` lines 206; flags: `equational/pure` — `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)`
- `rule` lines 207; flags: `equational/pure` — `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`
- `rule` lines 208; flags: `equational/pure` — `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)`
- `rule` lines 209; flags: `equational/pure` — `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))`
- `rule` lines 210; flags: `equational/pure` — `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)`
- `rule` lines 211; flags: `equational/pure` — `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))`
- `rule` lines 212; flags: `equational/pure` — `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))`
- `syntax` lines 214-215; flags: `function, total` — `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`
- `rule` lines 216; flags: `equational/pure` — `rule tokNds(.IntSeq)                => .IntSeq`
- `rule` lines 217; flags: `equational/pure` — `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)`
- `rule` lines 218; flags: `equational/pure` — `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`
- `rule` lines 219-220; flags: `equational/pure` — `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32`
- `rule` lines 221-222; flags: `equational/pure` — `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)`
- `rule` lines 223; flags: `owise, equational/pure` — `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`
- `syntax` lines 225; flags: `none` — `syntax EvPair ::= evp(OpSeq, IntSeq)`
- `syntax` lines 226; flags: `function, total` — `syntax Int ::= firstNdE(EvPair) [function, total]`
- `rule` lines 227; flags: `equational/pure` — `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`
- `rule` lines 228; flags: `owise, equational/pure` — `rule firstNdE(_:EvPair) => 0 [owise]`
- `syntax` lines 230; flags: `function, total` — `syntax Int ::= applyOpE(String, Int, Int) [function, total]`
- `rule` lines 231; flags: `equational/pure` — `rule applyOpE("+",  A:Int, B:Int) => A +Int B`
- `rule` lines 232; flags: `equational/pure` — `rule applyOpE("-",  A:Int, B:Int) => A -Int B`
- `rule` lines 233; flags: `equational/pure` — `rule applyOpE("*",  A:Int, B:Int) => A *Int B`
- `rule` lines 234; flags: `equational/pure` — `rule applyOpE("//", A:Int, B:Int) => A divInt B`
- `rule` lines 235; flags: `equational/pure` — `rule applyOpE("**", A:Int, B:Int) => A ^Int B`
- `rule` lines 236; flags: `owise, equational/pure` — `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`
- `syntax` lines 238; flags: `function, total` — `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`
- `rule` lines 239; flags: `equational/pure` — `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`
- `rule` lines 240; flags: `equational/pure` — `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`
- `rule` lines 241-242; flags: `equational/pure` — `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"`
- `rule` lines 243; flags: `owise, equational/pure` — `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`
- `syntax` lines 244; flags: `function, total` — `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`
- `rule` lines 245; flags: `equational/pure` — `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`
- `rule` lines 246; flags: `equational/pure` — `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`
- `syntax` lines 247; flags: `function, total` — `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`
- `rule` lines 248; flags: `equational/pure` — `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`
- `syntax` lines 250; flags: `function, total` — `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`
- `rule` lines 251; flags: `equational/pure` — `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`
- `rule` lines 252; flags: `equational/pure` — `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
- `rule` lines 253; flags: `equational/pure` — `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`
- `rule` lines 254; flags: `equational/pure` — `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
- `syntax` lines 255; flags: `function, total` — `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`
- `rule` lines 256; flags: `equational/pure` — `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`
- `rule` lines 257-259; flags: `equational/pure` — `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)`
- `rule` lines 260-262; flags: `equational/pure` — `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)`
- `rule` lines 263-264; flags: `owise, equational/pure` — `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`
- `syntax` lines 265; flags: `function, total` — `syntax Bool ::= inLevelE(String, String) [function, total]`
- `rule` lines 266; flags: `equational/pure` — `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"`
- `rule` lines 267; flags: `equational/pure` — `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`
- `rule` lines 268; flags: `owise, equational/pure` — `rule inLevelE(_:String, _:String) => false [owise]`
- `syntax` lines 269; flags: `function, total` — `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`
- `rule` lines 270; flags: `equational/pure` — `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`
- `rule` lines 271; flags: `equational/pure` — `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`
- `syntax` lines 272; flags: `function, total` — `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`
- `rule` lines 273; flags: `equational/pure` — `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`
- `rule` lines 274; flags: `equational/pure` — `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))`
- `syntax` lines 279; flags: `none` — `syntax KItem ::= "#md5"`
- `rule` lines 280-281; flags: `priority, operational` — `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`
- `rule` lines 282; flags: `operational` — `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`
- `syntax` lines 283; flags: `none` — `syntax Val ::= md5Obj(IntSeq)`
- `rule` lines 284; flags: `equational/pure` — `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`
- `syntax` lines 285; flags: `function, total, symbol, no-evaluators` — `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`
- `rule` lines 291; flags: `equational/pure` — `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`
- `rule` lines 292; flags: `equational/pure` — `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`
- `syntax` lines 293; flags: `function` — `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`
- `rule` lines 294; flags: `equational/pure` — `rule isIntV(_:Int)         => true`
- `rule` lines 295; flags: `owise, equational/pure` — `rule isIntV(_:Val)         => false [owise]`
- `rule` lines 296; flags: `equational/pure` — `rule isStrV(str(_:IntSeq)) => true`
- `rule` lines 297; flags: `owise, equational/pure` — `rule isStrV(_:Val)         => false [owise]`

## `reference-semantics/semantics/call.k`

- `rule` lines 16; flags: `operational` — `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>`
- `syntax` lines 19; flags: `none` — `syntax KItem ::= #callee(Exprs)`
- `rule` lines 20; flags: `owise, operational` — `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`
- `rule` lines 21; flags: `operational` — `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>`
- `rule` lines 24; flags: `operational` — `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`
- `rule` lines 26; flags: `operational` — `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`
- `rule` lines 27; flags: `operational` — `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>`
- `rule` lines 28; flags: `operational` — `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>`
- `rule` lines 29; flags: `operational` — `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>`
- `rule` lines 30; flags: `operational` — `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>`
- `rule` lines 31; flags: `owise, operational` — `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`
- `rule` lines 32; flags: `operational` — `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>`
- `rule` lines 38-41; flags: `priority, operational` — `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` lines 42-46; flags: `priority, operational` — `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]`
- `rule` lines 47-50; flags: `priority, operational` — `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `syntax` lines 52; flags: `function, total` — `syntax Bool ::= isMutMethod(String) [function, total]`
- `rule` lines 53-55; flags: `equational/pure` — `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`
- `rule` lines 56-60; flags: `priority, operational` — `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]`
- `rule` lines 63-67; flags: `priority, operational` — `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]`
- `rule` lines 69-74; flags: `operational` — `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
- `rule` lines 80-85; flags: `operational` — `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
- `syntax` lines 87; flags: `none` — `syntax KItem ::= #allocCells(ParamNames)`
- `rule` lines 88; flags: `operational` — `rule <k> #allocCells(.ParamNames) => .K ... </k>`
- `rule` lines 89-94; flags: `operational` — `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`

## `reference-semantics/semantics/comprehension.k`

- `rule` lines 11; flags: `equational/pure` — `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
- `rule` lines 12; flags: `equational/pure` — `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
- `syntax` lines 14; flags: `macro` — `syntax Stmts ::= compBody(CompFors, Expr) [macro]`
- `rule` lines 15-16; flags: `equational/pure` — `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`
- `syntax` lines 18; flags: `macro` — `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`
- `rule` lines 19-20; flags: `equational/pure` — `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`
- `rule` lines 21-22; flags: `equational/pure` — `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`
- `syntax` lines 24; flags: `macro` — `syntax Expr ::= compGuard(Exprs) [macro]`
- `rule` lines 25; flags: `equational/pure` — `rule compGuard(.Exprs)             => Bool(true)`
- `rule` lines 26; flags: `equational/pure` — `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`

## `reference-semantics/semantics/concrete.k`

- `rule` lines 13-15; flags: `operational` — `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`
- `rule` lines 16-18; flags: `operational` — `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`
- `syntax` lines 25; flags: `none` — `syntax Val ::= kvP(Val, Val)`
- `syntax` lines 26-27; flags: `none` — `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`
- `rule` lines 28-30; flags: `priority, operational` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`
- `rule` lines 31-33; flags: `priority, operational` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`
- `rule` lines 34-35; flags: `operational` — `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`
- `rule` lines 36-37; flags: `operational` — `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`
- `rule` lines 38-40; flags: `operational` — `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)`
- `syntax` lines 42; flags: `function` — `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`
- `rule` lines 43; flags: `equational/pure` — `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`
- `rule` lines 44-46; flags: `equational/pure` — `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)`
- `rule` lines 47-49; flags: `equational/pure` — `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)`
- `syntax` lines 51; flags: `function` — `syntax Bool ::= kLt(Val, Val) [function]`
- `rule` lines 52; flags: `equational/pure` — `rule kLt(I1:Int, I2:Int)             => I1 <Int I2`
- `rule` lines 53; flags: `equational/pure` — `rule kLt(F1:Float, F2:Float)         => F1 <Float F2`
- `rule` lines 54; flags: `equational/pure` — `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
- `syntax` lines 56; flags: `function, total` — `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`
- `rule` lines 57; flags: `equational/pure` — `rule unpairVS(.ValSeq) => .ValSeq`
- `rule` lines 58; flags: `equational/pure` — `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`
- `rule` lines 59; flags: `owise, equational/pure` — `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`

## `reference-semantics/semantics/controls.k`

- `rule` lines 9-11; flags: `operational` — `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
- `rule` lines 12-18; flags: `priority, operational` — `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`
- `rule` lines 20-23; flags: `operational` — `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)`
- `rule` lines 27-31; flags: `priority, operational` — `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]`
- `rule` lines 35; flags: `operational` — `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`
- `rule` lines 36; flags: `owise, operational` — `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`
- `syntax` lines 37; flags: `none` — `syntax KItem ::= #bindImports(ParamNames)`
- `rule` lines 38; flags: `operational` — `rule <k> #bindImports(.ParamNames) => .K ... </k>`
- `rule` lines 39-42; flags: `operational` — `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"`
- `rule` lines 43-44; flags: `operational` — `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")`
- `rule` lines 48; flags: `operational` — `rule <k> Expr(_:Val) => .K ... </k>`
- `syntax` lines 51; flags: `none` — `syntax KItem ::= #branch(Bool, Stmts, Stmts)`
- `rule` lines 52; flags: `operational` — `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`
- `rule` lines 53; flags: `operational` — `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>`
- `rule` lines 54; flags: `operational` — `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>`
- `rule` lines 57-58; flags: `operational` — `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)`
- `rule` lines 59-60; flags: `operational` — `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)`
- `syntax` lines 65-67; flags: `none` — `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`
- `rule` lines 69; flags: `operational` — `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`
- `rule` lines 71; flags: `operational` — `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`
- `rule` lines 72; flags: `operational` — `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`
- `rule` lines 73-74; flags: `operational` — `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>`
- `rule` lines 77; flags: `operational` — `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`
- `rule` lines 78; flags: `operational` — `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`
- `rule` lines 79-80; flags: `operational` — `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)`
- `rule` lines 81-82; flags: `operational` — `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)`
- `rule` lines 85; flags: `operational` — `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`
- `rule` lines 86; flags: `operational` — `rule <k> Continue => #cont ... </k>`
- `rule` lines 87; flags: `operational` — `rule <k> Break => #brk ... </k>`
- `rule` lines 88; flags: `operational` — `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`
- `rule` lines 89; flags: `owise, operational` — `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`
- `rule` lines 90; flags: `operational` — `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`
- `rule` lines 91; flags: `owise, operational` — `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]`
- `rule` lines 95-97; flags: `priority, operational` — `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` lines 98-100; flags: `priority, operational` — `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` lines 101-103; flags: `priority, operational` — `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` lines 106-108; flags: `priority, operational` — `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## `reference-semantics/semantics/core.k`

- `syntax` lines 13; flags: `none` — `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`
- `syntax` lines 14; flags: `none` — `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`
- `syntax` lines 15; flags: `none` — `syntax Str    ::= str(IntSeq)`
- `syntax` lines 18-23; flags: `none` — `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`
- `syntax` lines 25-34; flags: `function` — `syntax Val      ::= Int | Bool | "noneV" | Iterable | ref(Int)          // a heap object: <heap> holds its list(VS) | cellRef(Int)      // a closure cell: <heap> holds cellV(V) | closureVal(ParamNames, Stmts, Int) | typeV(String)     // a type object (int/str), resolved from the builtins frame | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough) | boundMethodV(Val, String)   // a cooled Attribute: obj.method`
- `syntax` lines 36; flags: `none` — `syntax Parent   ::= "root" | parent(Int)`
- `syntax` lines 37; flags: `none` — `syntax Scope    ::= scope(Map, Parent)`
- `syntax` lines 38; flags: `none` — `syntax KResult  ::= Val`
- `syntax` lines 39; flags: `none` — `syntax Expr     ::= Val   // cooling puts results back into expression holes`
- `syntax` lines 40; flags: `none` — `syntax Vals     ::= List{Val, ","}`
- `syntax` lines 41; flags: `none` — `syntax Exc      ::= "NoExc" | "AssertionError"`
- `syntax` lines 42; flags: `none` — `syntax RetState ::= "noRet" | retV(Val)`
- `configuration` lines 49-60; flags: `none` — `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     |-> scope(.Map, parent(-1)) -1    |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code>`
- `syntax` lines 68; flags: `function, total` — `syntax Bool ::= isRefV(Val) [function, total]`
- `rule` lines 69; flags: `equational/pure` — `rule isRefV(ref(_:Int)) => true`
- `rule` lines 70; flags: `owise, equational/pure` — `rule isRefV(_:Val)      => false [owise]`
- `syntax` lines 75; flags: `none` — `syntax HeapVal ::= cellV(Val)`
- `syntax` lines 76; flags: `function, total` — `syntax Bool ::= isCellRef(Val) [function, total]`
- `rule` lines 77; flags: `equational/pure` — `rule isCellRef(cellRef(_:Int)) => true`
- `rule` lines 78; flags: `owise, equational/pure` — `rule isCellRef(_:Val)          => false [owise]`
- `rule` lines 85-90; flags: `priority, operational` — `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]`
- `syntax` lines 95; flags: `none` — `syntax Val ::= kwV(String, Val)`
- `syntax` lines 96; flags: `none` — `syntax KItem ::= #kwTag(String)`
- `rule` lines 97; flags: `operational` — `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`
- `rule` lines 98-99; flags: `operational` — `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)`
- `syntax` lines 100; flags: `function, total` — `syntax Bool ::= isKwV(Val) [function, total]`
- `rule` lines 101; flags: `equational/pure` — `rule isKwV(kwV(_:String, _:Val)) => true`
- `rule` lines 102; flags: `owise, equational/pure` — `rule isKwV(_:Val)                => false [owise]`
- `syntax` lines 106; flags: `none` — `syntax Val ::= cellsMark(ParamNames)`
- `syntax` lines 107; flags: `function` — `syntax ParamNames ::= cellsOf(Val) [function]`
- `rule` lines 108; flags: `equational/pure` — `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`
- `syntax` lines 109; flags: `function, total` — `syntax Bool ::= pnMember(String, ParamNames) [function, total]`
- `rule` lines 110; flags: `equational/pure` — `rule pnMember(_:String, .ParamNames) => false`
- `rule` lines 111; flags: `equational/pure` — `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`
- `syntax` lines 113; flags: `none` — `syntax KItem ::= #cellW(Val, Val)`
- `rule` lines 114-115; flags: `operational` — `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`
- `syntax` lines 117; flags: `none` — `syntax KItem ::= #alloc(Val)`
- `rule` lines 118-121; flags: `operational` — `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`
- `syntax` lines 124; flags: `none` — `syntax KItem ::= #loadAll(Module)`
- `rule` lines 125; flags: `operational` — `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`
- `rule` lines 126; flags: `operational` — `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`
- `rule` lines 127; flags: `operational` — `rule <k> .Stmts => .K ... </k>`
- `syntax` lines 130; flags: `none` — `syntax KItem ::= #look(String, Int)`
- `rule` lines 131; flags: `operational` — `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`
- `rule` lines 132-134; flags: `operational` — `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)`
- `rule` lines 145-151; flags: `priority, operational` — `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]`
- `rule` lines 152-154; flags: `operational` — `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))`
- `syntax` lines 157; flags: `function, total` — `syntax Scope ::= "builtinsScope" [function, total]`
- `rule` lines 158-181; flags: `equational/pure` — `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root)`
- `syntax` lines 185; flags: `none` — `syntax ApplyK ::= toCall(Val)`
- `syntax` lines 186-188; flags: `none` — `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`
- `rule` lines 189; flags: `operational` — `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`
- `rule` lines 190; flags: `operational` — `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`
- `rule` lines 191; flags: `operational` — `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>`
- `rule` lines 194; flags: `operational` — `rule <k> Int(I:Int)   => I ... </k>`
- `rule` lines 195; flags: `operational` — `rule <k> Bool(B:Bool) => B ... </k>`
- `rule` lines 196; flags: `operational` — `rule <k> NoneVal      => noneV ... </k>`
- `syntax` lines 199; flags: `function` — `syntax Bool ::= truthy(Val) [function]`
- `rule` lines 200; flags: `equational/pure` — `rule truthy(B:Bool)          => B`
- `rule` lines 201; flags: `equational/pure` — `rule truthy(noneV)           => false`
- `rule` lines 202; flags: `equational/pure` — `rule truthy(I:Int)           => I =/=Int 0`
- `rule` lines 203; flags: `equational/pure` — `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)`
- `rule` lines 204; flags: `equational/pure` — `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)`
- `rule` lines 205; flags: `equational/pure` — `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)`
- `syntax` lines 208; flags: `function` — `syntax Val  ::= applyUn(String, Val) [function]`
- `syntax` lines 209; flags: `function` — `syntax Val  ::= applyBin(String, Val, Val) [function]`
- `syntax` lines 210; flags: `function` — `syntax Bool ::= applyCmp(String, Val, Val) [function]`
- `syntax` lines 213; flags: `function, total` — `syntax Vals ::= appendVal(Vals, Val) [function, total]`
- `rule` lines 214; flags: `equational/pure` — `rule appendVal(.Vals, V:Val)              => V , .Vals`
- `rule` lines 215; flags: `equational/pure` — `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)`
- `syntax` lines 217; flags: `function, total` — `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`
- `rule` lines 218; flags: `equational/pure` — `rule vals2valSeq(.Vals)            => .ValSeq`
- `rule` lines 219; flags: `equational/pure` — `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))`
- `syntax` lines 223; flags: `function, total` — `syntax Int ::= vsLen(ValSeq) [function, total]`
- `rule` lines 224; flags: `equational/pure` — `rule vsLen(.ValSeq)                => 0`
- `rule` lines 225; flags: `equational/pure` — `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`
- `syntax` lines 227; flags: `function, total` — `syntax Int ::= isLen(IntSeq) [function, total]`
- `rule` lines 228; flags: `equational/pure` — `rule isLen(.IntSeq)                => 0`
- `rule` lines 229; flags: `equational/pure` — `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)`
- `syntax` lines 233; flags: `function, total` — `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`
- `rule` lines 234; flags: `equational/pure` — `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq`
- `rule` lines 235; flags: `equational/pure` — `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)`
- `rule` lines 236-237; flags: `equational/pure` — `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0`
- `rule` lines 238-239; flags: `equational/pure` — `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0`

## `reference-semantics/semantics/dict.k`

- `syntax` lines 20; flags: `none` — `syntax Val ::= dictV(ValSeq, ValSeq)`
- `syntax` lines 23-25; flags: `none` — `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`
- `rule` lines 26; flags: `operational` — `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`
- `rule` lines 27; flags: `operational` — `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`
- `rule` lines 28-29; flags: `operational` — `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`
- `rule` lines 30-31; flags: `operational` — `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`
- `rule` lines 32-33; flags: `operational` — `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>`
- `syntax` lines 37; flags: `function, total` — `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`
- `rule` lines 38; flags: `equational/pure` — `rule dHasKey(.ValSeq, _:Val)                => false`
- `rule` lines 39; flags: `equational/pure` — `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K`
- `rule` lines 40; flags: `equational/pure` — `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)`
- `syntax` lines 43; flags: `function, total` — `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`
- `rule` lines 44; flags: `equational/pure` — `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)`
- `rule` lines 45; flags: `equational/pure` — `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)`
- `syntax` lines 49; flags: `function, total` — `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`
- `rule` lines 50-51; flags: `equational/pure` — `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K`
- `rule` lines 52-53; flags: `equational/pure` — `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)`
- `rule` lines 54; flags: `owise, equational/pure` — `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]`
- `rule` lines 58-60; flags: `priority, operational` — `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]`
- `rule` lines 63; flags: `equational/pure` — `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`
- `syntax` lines 64; flags: `function` — `syntax Val ::= applyIndexD(Val, Val) [function]`
- `rule` lines 65-66; flags: `priority, operational` — `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]`
- `syntax` lines 70; flags: `function` — `syntax Val ::= dictSet(Val, Val, Val) [function]`
- `rule` lines 71; flags: `equational/pure` — `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))`
- `syntax` lines 76; flags: `none` — `syntax KItem ::= #dsetK(String, Val)`
- `rule` lines 77; flags: `operational` — `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`
- `rule` lines 78-81; flags: `operational` — `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)`
- `rule` lines 82-85; flags: `operational` — `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)`
- `syntax` lines 86; flags: `none` — `syntax KItem ::= #dsetV(Val, Val, Val)`
- `rule` lines 87-88; flags: `operational` — `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>`
- `syntax` lines 90; flags: `function, total` — `syntax Int ::= normIdxD(Int, Int) [function, total]`
- `rule` lines 91; flags: `equational/pure` — `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`
- `rule` lines 92; flags: `equational/pure` — `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0`
- `rule` lines 95-96; flags: `equational/pure` — `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`
- `syntax` lines 97; flags: `function` — `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`
- `rule` lines 98; flags: `equational/pure` — `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`
- `rule` lines 99-100; flags: `equational/pure` — `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`
- `syntax` lines 101; flags: `function` — `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`
- `rule` lines 102; flags: `equational/pure` — `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K`
- `rule` lines 103; flags: `equational/pure` — `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`

## `reference-semantics/semantics/float.k`

- `syntax` lines 20; flags: `none` — `syntax Val ::= Float`
- `rule` lines 21; flags: `operational` — `rule <k> Float(F:Float) => F ... </k>`
- `syntax` lines 24; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`
- `rule` lines 25; flags: `concrete, equational/pure` — `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`
- `rule` lines 27; flags: `equational/pure` — `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)`
- `syntax` lines 30; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`
- `rule` lines 31; flags: `concrete, equational/pure` — `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`
- `rule` lines 32; flags: `equational/pure` — `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)`
- `syntax` lines 37; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`
- `rule` lines 38; flags: `concrete, equational/pure` — `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`
- `rule` lines 39; flags: `equational/pure` — `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)`
- `rule` lines 43; flags: `equational/pure` — `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`
- `rule` lines 44; flags: `equational/pure` — `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)`
- `syntax` lines 50; flags: `function, total, symbol, no-evaluators` — `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`
- `rule` lines 51; flags: `concrete, equational/pure` — `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`
- `rule` lines 52; flags: `equational/pure` — `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`
- `syntax` lines 54; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`
- `rule` lines 55; flags: `concrete, equational/pure` — `rule absF(F:Float) => absFloat(F) [concrete]`
- `rule` lines 56; flags: `equational/pure` — `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)`
- `rule` lines 61; flags: `operational` — `rule <k> Import(_:String) => .K ... </k>`
- `syntax` lines 65; flags: `none` — `syntax KItem ::= "#mathCeil"`
- `rule` lines 66; flags: `priority, operational` — `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`
- `rule` lines 67; flags: `operational` — `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>`
- `syntax` lines 70; flags: `none` — `syntax KItem ::= "#mathFloor"`
- `rule` lines 71; flags: `priority, operational` — `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`
- `rule` lines 72; flags: `operational` — `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`
- `syntax` lines 73; flags: `function, total, symbol` — `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`
- `rule` lines 74; flags: `concrete, equational/pure` — `rule floorFI(I:Int)   => I                        [concrete]`
- `rule` lines 75; flags: `concrete, equational/pure` — `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]`
- `rule` lines 78; flags: `equational/pure` — `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`
- `rule` lines 79; flags: `equational/pure` — `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)`
- `syntax` lines 82; flags: `none` — `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`
- `rule` lines 83; flags: `priority, operational` — `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`
- `rule` lines 84; flags: `operational` — `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`
- `rule` lines 85; flags: `operational` — `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`
- `syntax` lines 86; flags: `function, total, symbol` — `syntax Float ::= toF(Val) [function, total, symbol(toF)]`
- `rule` lines 87; flags: `concrete, equational/pure` — `rule toF(F:Float) => F        [concrete]`
- `rule` lines 88; flags: `concrete, equational/pure` — `rule toF(I:Int)   => intToF(I) [concrete]`
- `syntax` lines 93; flags: `function, total, symbol` — `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`
- `rule` lines 94; flags: `concrete, equational/pure` — `rule ceilF(I:Int)   => I                       [concrete]`
- `rule` lines 95; flags: `concrete, equational/pure` — `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]`
- `rule` lines 99; flags: `equational/pure` — `rule applyUn("-", F:Float) => 0.0 -Float F`
- `syntax` lines 103; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`
- `rule` lines 104; flags: `concrete, equational/pure` — `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`
- `rule` lines 105; flags: `equational/pure` — `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`
- `syntax` lines 107; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`
- `rule` lines 108; flags: `concrete, equational/pure` — `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`
- `rule` lines 109; flags: `equational/pure` — `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`
- `syntax` lines 111; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`
- `rule` lines 112; flags: `concrete, equational/pure` — `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`
- `rule` lines 113; flags: `equational/pure` — `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`
- `syntax` lines 115; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`
- `rule` lines 116; flags: `concrete, equational/pure` — `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`
- `rule` lines 117; flags: `equational/pure` — `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`
- `syntax` lines 119; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`
- `rule` lines 120; flags: `concrete, equational/pure` — `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`
- `rule` lines 121; flags: `equational/pure` — `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)`
- `syntax` lines 125; flags: `function, total, symbol, no-evaluators` — `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`
- `rule` lines 126; flags: `concrete, equational/pure` — `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`
- `rule` lines 127; flags: `equational/pure` — `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)`
- `rule` lines 128; flags: `equational/pure` — `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`
- `rule` lines 129; flags: `equational/pure` — `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)`
- `rule` lines 132; flags: `equational/pure` — `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`
- `rule` lines 133; flags: `equational/pure` — `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`
- `rule` lines 134; flags: `equational/pure` — `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)`
- `rule` lines 135; flags: `equational/pure` — `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))`
- `rule` lines 136; flags: `equational/pure` — `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)`
- `rule` lines 137; flags: `equational/pure` — `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))`
- `rule` lines 138; flags: `equational/pure` — `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)`
- `rule` lines 139; flags: `equational/pure` — `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))`
- `syntax` lines 142; flags: `function, total, symbol, no-evaluators` — `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`
- `rule` lines 143; flags: `concrete, equational/pure` — `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`
- `rule` lines 144; flags: `equational/pure` — `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`
- `rule` lines 145; flags: `equational/pure` — `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`
- `rule` lines 146; flags: `equational/pure` — `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`
- `rule` lines 147; flags: `equational/pure` — `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`
- `rule` lines 148; flags: `equational/pure` — `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)`
- `rule` lines 149; flags: `equational/pure` — `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))`
- `rule` lines 150; flags: `equational/pure` — `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)`
- `rule` lines 151; flags: `equational/pure` — `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))`
- `rule` lines 154; flags: `equational/pure` — `rule applyCmp("==", V:Val, noneV) => V ==K noneV`
- `rule` lines 155; flags: `equational/pure` — `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)`
- `syntax` lines 160; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`
- `rule` lines 161; flags: `concrete, equational/pure` — `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`
- `rule` lines 162-164; flags: `concrete, equational/pure` — `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]`
- `syntax` lines 165; flags: `function` — `syntax Int ::= headIS(IntSeq) [function]`
- `rule` lines 166; flags: `equational/pure` — `rule headIS(iCons(C:Int, _:IntSeq)) => C`
- `syntax` lines 167; flags: `function, total` — `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`
- `rule` lines 168; flags: `equational/pure` — `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`
- `rule` lines 169; flags: `equational/pure` — `rule intPartAcc(.IntSeq, A:Int) => A`
- `rule` lines 170; flags: `equational/pure` — `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`
- `rule` lines 171-172; flags: `equational/pure` — `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46`
- `syntax` lines 173; flags: `function, total` — `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`
- `rule` lines 174; flags: `equational/pure` — `rule fracPart(.IntSeq) => 0`
- `rule` lines 175; flags: `equational/pure` — `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`
- `rule` lines 176; flags: `equational/pure` — `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`
- `rule` lines 177; flags: `equational/pure` — `rule fracAcc(.IntSeq, A:Int) => A`
- `rule` lines 178; flags: `equational/pure` — `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`
- `syntax` lines 179; flags: `function, total` — `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`
- `rule` lines 180; flags: `equational/pure` — `rule fracScale(.IntSeq) => 1`
- `rule` lines 181; flags: `equational/pure` — `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`
- `rule` lines 182; flags: `equational/pure` — `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`
- `rule` lines 183; flags: `equational/pure` — `rule fscAcc(.IntSeq, A:Int) => A`
- `rule` lines 184; flags: `equational/pure` — `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`
- `rule` lines 185; flags: `equational/pure` — `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`
- `rule` lines 186; flags: `equational/pure` — `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)`
- `rule` lines 187; flags: `equational/pure` — `rule applyBuiltin("float", F:Float, .Vals)        => F`
- `syntax` lines 190; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`
- `rule` lines 191; flags: `concrete, equational/pure` — `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`
- `rule` lines 192; flags: `equational/pure` — `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)`
- `syntax` lines 195; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`
- `rule` lines 196; flags: `concrete, equational/pure` — `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`
- `rule` lines 197; flags: `equational/pure` — `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`
- `rule` lines 198; flags: `equational/pure` — `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`
- `rule` lines 199; flags: `equational/pure` — `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`
- `rule` lines 200; flags: `equational/pure` — `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`
- `rule` lines 201; flags: `equational/pure` — `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`
- `rule` lines 202; flags: `equational/pure` — `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`
- `rule` lines 203; flags: `equational/pure` — `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`
- `rule` lines 204; flags: `equational/pure` — `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`
- `rule` lines 205; flags: `equational/pure` — `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`
- `rule` lines 206; flags: `equational/pure` — `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`
- `syntax` lines 209; flags: `function, total, symbol, no-evaluators` — `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`
- `rule` lines 210; flags: `concrete, equational/pure` — `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`
- `rule` lines 211; flags: `equational/pure` — `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`
- `rule` lines 213; flags: `equational/pure` — `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)`
- `rule` lines 214; flags: `equational/pure` — `rule applyBuiltin("float", F:Float, .Vals) => F`
- `syntax` lines 217; flags: `function, total, symbol, no-evaluators` — `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`
- `rule` lines 218-222; flags: `concrete, equational/pure` — `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`
- `syntax` lines 223; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`
- `rule` lines 224-226; flags: `concrete, equational/pure` — `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`
- `rule` lines 227; flags: `equational/pure` — `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)`
- `rule` lines 228; flags: `equational/pure` — `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`
- `syntax` lines 230; flags: `function, total, symbol, no-evaluators` — `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`
- `rule` lines 231; flags: `concrete, equational/pure` — `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`
- `syntax` lines 232; flags: `none` — `syntax KItem ::= "#mathSqrt"`
- `rule` lines 233; flags: `priority, operational` — `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`
- `rule` lines 234; flags: `operational` — `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`
- `rule` lines 235; flags: `operational` — `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>`
- `syntax` lines 243; flags: `none` — `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`
- `rule` lines 244; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
- `rule` lines 245; flags: `operational` — `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`
- `rule` lines 246; flags: `operational` — `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`
- `rule` lines 247-248; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`
- `syntax` lines 250; flags: `none` — `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`
- `rule` lines 251; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
- `rule` lines 252; flags: `operational` — `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`
- `rule` lines 253; flags: `operational` — `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`
- `rule` lines 254-255; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`
- `syntax` lines 261; flags: `none` — `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`
- `rule` lines 262-264; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))`
- `rule` lines 265; flags: `operational` — `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`
- `rule` lines 266; flags: `operational` — `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`
- `rule` lines 267-269; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)`
- `rule` lines 270-272; flags: `operational` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)`

## `reference-semantics/semantics/functions.k`

- `syntax` lines 8-11; flags: `none` — `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall"`
- `rule` lines 14-16; flags: `operational` — `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`
- `syntax` lines 18; flags: `none` — `syntax Expr ::= closureExpr(ParamNames, Stmts)`
- `rule` lines 19-20; flags: `operational` — `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>`
- `syntax` lines 27; flags: `none` — `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)`
- `syntax` lines 31-32; flags: `none` — `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`
- `rule` lines 33-35; flags: `operational` — `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`
- `rule` lines 36-41; flags: `operational` — `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`
- `rule` lines 42-45; flags: `operational` — `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`
- `rule` lines 47-49; flags: `operational` — `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`
- `rule` lines 50-52; flags: `operational` — `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`
- `rule` lines 53-58; flags: `operational` — `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`
- `rule` lines 59-60; flags: `operational` — `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>`
- `rule` lines 63; flags: `operational` — `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`
- `rule` lines 64-66; flags: `operational` — `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>`
- `rule` lines 68-75; flags: `priority, operational` — `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]`
- `rule` lines 78-79; flags: `operational` — `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`
- `rule` lines 80-81; flags: `operational` — `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>`
- `rule` lines 85-90; flags: `operational` — `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`

## `reference-semantics/semantics/int.k`

- `rule` lines 7; flags: `equational/pure` — `rule applyUn("-", I:Int) => 0 -Int I`
- `rule` lines 9; flags: `equational/pure` — `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2`
- `rule` lines 11; flags: `equational/pure` — `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`
- `rule` lines 12; flags: `equational/pure` — `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`
- `rule` lines 13; flags: `equational/pure` — `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2`
- `rule` lines 14; flags: `equational/pure` — `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2`
- `rule` lines 15; flags: `equational/pure` — `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)`
- `rule` lines 16; flags: `equational/pure` — `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2`
- `rule` lines 17; flags: `equational/pure` — `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`
- `syntax` lines 19; flags: `function` — `syntax Int ::= pyMod(Int, Int) [function]`
- `rule` lines 20; flags: `equational/pure` — `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`
- `rule` lines 22; flags: `equational/pure` — `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2`
- `rule` lines 23; flags: `equational/pure` — `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2`
- `rule` lines 24; flags: `equational/pure` — `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2`
- `rule` lines 25; flags: `equational/pure` — `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2`
- `rule` lines 26; flags: `equational/pure` — `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2`
- `rule` lines 27; flags: `equational/pure` — `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2`

## `reference-semantics/semantics/iter.k`

- `syntax` lines 8; flags: `none` — `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`

## `reference-semantics/semantics/list.k`

- `rule` lines 9; flags: `operational` — `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>`
- `rule` lines 10; flags: `operational` — `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>`
- `syntax` lines 13; flags: `none` — `syntax ApplyK ::= "toList"`
- `rule` lines 14; flags: `operational` — `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`
- `rule` lines 15; flags: `operational` — `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>`
- `syntax` lines 18; flags: `function, total` — `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`
- `rule` lines 19; flags: `equational/pure` — `rule valSeqConcat(.ValSeq, T:ValSeq)                => T`
- `rule` lines 20; flags: `equational/pure` — `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))`
- `rule` lines 24-25; flags: `priority, operational` — `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`
- `rule` lines 27; flags: `equational/pure` — `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`
- `rule` lines 28; flags: `equational/pure` — `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)`
- `syntax` lines 33; flags: `function, total` — `syntax Bool ::= hasRefVS(ValSeq) [function, total]`
- `rule` lines 34; flags: `equational/pure` — `rule hasRefVS(.ValSeq)                => false`
- `rule` lines 35; flags: `equational/pure` — `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`
- `syntax` lines 37-38; flags: `function` — `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map)        [function]`
- `rule` lines 39; flags: `equational/pure` — `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true`
- `rule` lines 40; flags: `equational/pure` — `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false`
- `rule` lines 41; flags: `equational/pure` — `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false`
- `rule` lines 42-43; flags: `equational/pure` — `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`
- `rule` lines 45-46; flags: `equational/pure` — `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)`
- `rule` lines 47-48; flags: `equational/pure` — `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)`
- `rule` lines 49; flags: `equational/pure` — `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`
- `rule` lines 50; flags: `owise, equational/pure` — `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]`
- `rule` lines 53-55; flags: `priority, operational` — `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]`
- `syntax` lines 58; flags: `none` — `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`
- `rule` lines 59; flags: `operational` — `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`
- `rule` lines 60; flags: `operational` — `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`
- `rule` lines 61; flags: `operational` — `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`
- `rule` lines 62; flags: `operational` — `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`
- `rule` lines 63-64; flags: `operational` — `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V`
- `rule` lines 65-66; flags: `operational` — `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)`
- `rule` lines 67; flags: `operational` — `rule <k> B:Bool ~> #notB => notBool B ... </k>`

## `reference-semantics/semantics/methods.k`

- `syntax` lines 10; flags: `function` — `syntax Val ::= applyMethod(Val, String, Vals) [function]`
- `rule` lines 13; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`
- `rule` lines 14; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`
- `rule` lines 15; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`
- `rule` lines 16; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)`
- `rule` lines 19; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))`
- `rule` lines 20; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))`
- `rule` lines 21; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))`
- `rule` lines 26; flags: `equational/pure` — `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`
- `syntax` lines 27; flags: `function, total` — `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`
- `rule` lines 28; flags: `equational/pure` — `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`
- `rule` lines 29; flags: `equational/pure` — `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`
- `rule` lines 30-31; flags: `equational/pure` — `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))`
- `rule` lines 34; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`
- `syntax` lines 35; flags: `function` — `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`
- `rule` lines 36; flags: `equational/pure` — `rule cntSub(.IntSeq, _:IntSeq) => 0`
- `rule` lines 37-38; flags: `equational/pure` — `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0`
- `rule` lines 39-40; flags: `equational/pure` — `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0`
- `syntax` lines 41; flags: `function, total` — `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`
- `rule` lines 42; flags: `equational/pure` — `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`
- `rule` lines 43; flags: `owise, equational/pure` — `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`
- `rule` lines 44; flags: `equational/pure` — `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0`
- `rule` lines 47; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`
- `syntax` lines 48; flags: `function, total` — `syntax IntSeq ::= trimWS(IntSeq) [function, total]`
- `rule` lines 49; flags: `equational/pure` — `rule trimWS(.IntSeq) => .IntSeq`
- `rule` lines 50; flags: `equational/pure` — `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`
- `rule` lines 51; flags: `equational/pure` — `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`
- `syntax` lines 52; flags: `function, total` — `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`
- `rule` lines 53; flags: `equational/pure` — `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`
- `rule` lines 54; flags: `equational/pure` — `rule revISAcc(.IntSeq, A:IntSeq) => A`
- `rule` lines 55; flags: `equational/pure` — `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))`
- `rule` lines 58; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)`
- `rule` lines 61; flags: `equational/pure` — `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)`
- `rule` lines 64; flags: `equational/pure` — `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`
- `syntax` lines 65; flags: `function, total` — `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`
- `rule` lines 66; flags: `equational/pure` — `rule cntOccVS(.ValSeq, _:Val)                => 0`
- `rule` lines 67; flags: `equational/pure` — `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`
- `rule` lines 68; flags: `equational/pure` — `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)`
- `rule` lines 72-74; flags: `priority, operational` — `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`
- `syntax` lines 75; flags: `function` — `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result`
- `rule` lines 76; flags: `equational/pure` — `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`
- `rule` lines 77-78; flags: `equational/pure` — `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)`
- `rule` lines 79-80; flags: `equational/pure` — `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)`
- `syntax` lines 82; flags: `function` — `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`
- `rule` lines 83; flags: `equational/pure` — `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC`
- `rule` lines 84; flags: `equational/pure` — `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`
- `syntax` lines 85; flags: `function, total` — `syntax Bool ::= isWSC(Int) [function, total]`
- `rule` lines 86; flags: `equational/pure` — `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13`
- `rule` lines 89-91; flags: `priority, operational` — `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]`
- `rule` lines 94-96; flags: `priority, operational` — `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`
- `syntax` lines 97; flags: `function` — `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token`
- `rule` lines 98; flags: `equational/pure` — `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)`
- `rule` lines 99-100; flags: `equational/pure` — `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP`
- `rule` lines 101-102; flags: `equational/pure` — `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)`
- `rule` lines 104-105; flags: `equational/pure` — `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`
- `syntax` lines 106; flags: `function, total` — `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`
- `rule` lines 107; flags: `equational/pure` — `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq`
- `rule` lines 108; flags: `equational/pure` — `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`
- `rule` lines 109; flags: `equational/pure` — `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)`
- `syntax` lines 112; flags: `function, total` — `syntax Bool ::= isUpperC(Int) [function, total]`
- `rule` lines 113; flags: `equational/pure` — `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`
- `syntax` lines 115; flags: `function, total` — `syntax Bool ::= isLowerC(Int) [function, total]`
- `rule` lines 116; flags: `equational/pure` — `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`
- `syntax` lines 118; flags: `function, total` — `syntax Bool ::= isAlphaC(Int) [function, total]`
- `rule` lines 119; flags: `equational/pure` — `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`
- `syntax` lines 121; flags: `function, total` — `syntax Bool ::= isDigitC(Int) [function, total]`
- `rule` lines 122; flags: `equational/pure` — `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`
- `syntax` lines 124; flags: `function, total` — `syntax Bool ::= hasUpper(IntSeq) [function, total]`
- `rule` lines 125; flags: `equational/pure` — `rule hasUpper(.IntSeq) => false`
- `rule` lines 126; flags: `equational/pure` — `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`
- `syntax` lines 128; flags: `function, total` — `syntax Bool ::= hasLower(IntSeq) [function, total]`
- `rule` lines 129; flags: `equational/pure` — `rule hasLower(.IntSeq) => false`
- `rule` lines 130; flags: `equational/pure` — `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`
- `syntax` lines 132; flags: `function, total` — `syntax Bool ::= allAlpha(IntSeq) [function, total]`
- `rule` lines 133; flags: `equational/pure` — `rule allAlpha(.IntSeq) => true`
- `rule` lines 134; flags: `equational/pure` — `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`
- `syntax` lines 136; flags: `function, total` — `syntax Bool ::= allDigit(IntSeq) [function, total]`
- `rule` lines 137; flags: `equational/pure` — `rule allDigit(.IntSeq) => true`
- `rule` lines 138; flags: `equational/pure` — `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`
- `syntax` lines 140; flags: `function, total` — `syntax Int ::= lowerC(Int) [function, total]`
- `rule` lines 142; flags: `equational/pure` — `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`
- `rule` lines 143; flags: `owise, equational/pure` — `rule lowerC(C:Int) => C         [owise]`
- `syntax` lines 145; flags: `function, total` — `syntax Int ::= upperC(Int) [function, total]`
- `rule` lines 146; flags: `equational/pure` — `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`
- `rule` lines 147; flags: `owise, equational/pure` — `rule upperC(C:Int) => C         [owise]`
- `syntax` lines 149; flags: `function, total` — `syntax Int ::= swapC(Int) [function, total]`
- `rule` lines 150; flags: `equational/pure` — `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`
- `rule` lines 151; flags: `equational/pure` — `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`
- `rule` lines 152; flags: `owise, equational/pure` — `rule swapC(C:Int) => C         [owise]`
- `syntax` lines 154; flags: `function, total` — `syntax IntSeq ::= mapLower(IntSeq) [function, total]`
- `rule` lines 155; flags: `equational/pure` — `rule mapLower(.IntSeq) => .IntSeq`
- `rule` lines 156; flags: `equational/pure` — `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`
- `syntax` lines 158; flags: `function, total` — `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`
- `rule` lines 159; flags: `equational/pure` — `rule mapUpper(.IntSeq) => .IntSeq`
- `rule` lines 160; flags: `equational/pure` — `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`
- `syntax` lines 162; flags: `function, total` — `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`
- `rule` lines 163; flags: `equational/pure` — `rule mapSwap(.IntSeq) => .IntSeq`
- `rule` lines 164; flags: `equational/pure` — `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`
- `syntax` lines 166; flags: `function, total` — `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`
- `rule` lines 167; flags: `equational/pure` — `rule startsWith(.IntSeq, _:IntSeq)               => true`
- `rule` lines 168; flags: `equational/pure` — `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`
- `rule` lines 169; flags: `equational/pure` — `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`

## `reference-semantics/semantics/operators.k`

- `rule` lines 10; flags: `operational` — `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`
- `rule` lines 12; flags: `operational` — `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>`
- `context` lines 15; flags: `none` — `context Compare(HOLE, _)`
- `context` lines 16; flags: `none` — `context Compare(_:Val, CmpOp(_, HOLE))`
- `rule` lines 17; flags: `owise, operational` — `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`
- `rule` lines 19; flags: `equational/pure` — `rule applyCmp("is",     V:Val, noneV) => V ==K noneV`
- `rule` lines 20; flags: `equational/pure` — `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)`
- `rule` lines 25-27; flags: `priority, operational` — `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` lines 28-31; flags: `priority, operational` — `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]`
- `rule` lines 34-37; flags: `priority, operational` — `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]`
- `rule` lines 38-42; flags: `priority, operational` — `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]`
- `rule` lines 44-46; flags: `priority, operational` — `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## `reference-semantics/semantics/range.k`

- `syntax` lines 9; flags: `function, total` — `syntax Bool ::= inRange(Int, Int, Int) [function, total]`
- `rule` lines 10; flags: `equational/pure` — `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`
- `syntax` lines 12; flags: `function` — `syntax Int ::= rangeLen(Int, Int, Int) [function]`
- `rule` lines 13-14; flags: `equational/pure` — `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO`
- `rule` lines 15-16; flags: `equational/pure` — `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO`
- `rule` lines 17-18; flags: `equational/pure` — `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)`
- `rule` lines 20-22; flags: `operational` — `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)`
- `rule` lines 23-24; flags: `operational` — `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)`

## `reference-semantics/semantics/set.k`

- `syntax` lines 8; flags: `none` — `syntax Val ::= setV(IntSeq)`
- `syntax` lines 11; flags: `function, total` — `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`
- `rule` lines 12; flags: `equational/pure` — `rule codeIn(_:Int, .IntSeq)                => false`
- `rule` lines 13; flags: `equational/pure` — `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)`
- `syntax` lines 16-17; flags: `function, total` — `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] | dedupFrom(IntSeq, IntSeq)  [function, total]`
- `rule` lines 18; flags: `equational/pure` — `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`
- `rule` lines 19; flags: `equational/pure` — `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`
- `rule` lines 20-21; flags: `equational/pure` — `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)`
- `rule` lines 22-23; flags: `equational/pure` — `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)`
- `syntax` lines 25; flags: `function, total` — `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`
- `rule` lines 26; flags: `equational/pure` — `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)`
- `rule` lines 27; flags: `equational/pure` — `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))`
- `syntax` lines 31; flags: `function, total` — `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`
- `rule` lines 32; flags: `equational/pure` — `rule subsetCodes(.IntSeq, _:IntSeq)                => true`
- `rule` lines 33; flags: `equational/pure` — `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`
- `syntax` lines 35; flags: `function, total` — `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`
- `rule` lines 36; flags: `equational/pure` — `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)`
- `rule` lines 39; flags: `equational/pure` — `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`

## `reference-semantics/semantics/sort.k`

- `syntax` lines 18; flags: `function, total, symbol, no-evaluators` — `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`
- `syntax` lines 19; flags: `function` — `syntax ValSeq ::= insVS(Int, ValSeq) [function]`
- `rule` lines 20; flags: `concrete, equational/pure` — `rule sortVS(.ValSeq)                => .ValSeq          [concrete]`
- `rule` lines 21; flags: `concrete, equational/pure` — `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`
- `rule` lines 22; flags: `concrete, equational/pure` — `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]`
- `rule` lines 23; flags: `concrete, equational/pure` — `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`
- `rule` lines 24; flags: `concrete, equational/pure` — `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]`
- `syntax` lines 26; flags: `function` — `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`
- `rule` lines 27; flags: `concrete, equational/pure` — `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`
- `rule` lines 28; flags: `concrete, equational/pure` — `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`
- `rule` lines 29-30; flags: `concrete, equational/pure` — `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]`
- `rule` lines 31-32; flags: `concrete, equational/pure` — `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]`
- `rule` lines 36-37; flags: `operational` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>`
- `rule` lines 40-42; flags: `priority, operational` — `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]`
- `syntax` lines 49; flags: `function, total, symbol, no-evaluators` — `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`
- `syntax` lines 51-52; flags: `function, total` — `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`
- `rule` lines 53; flags: `equational/pure` — `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`
- `rule` lines 54; flags: `equational/pure` — `rule revVSAcc(.ValSeq, A:ValSeq) => A`
- `rule` lines 55; flags: `equational/pure` — `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`
- `syntax` lines 57; flags: `function, total` — `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`
- `rule` lines 58; flags: `equational/pure` — `rule condRev(S:ValSeq, false) => S`
- `rule` lines 59; flags: `equational/pure` — `rule condRev(S:ValSeq, true)  => revVS(S)`
- `rule` lines 61-62; flags: `operational` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`
- `rule` lines 63-64; flags: `operational` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`
- `rule` lines 65-66; flags: `operational` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>`

## `reference-semantics/semantics/str.k`

- `rule` lines 8; flags: `operational` — `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>`
- `rule` lines 9-10; flags: `operational` — `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>`
- `syntax` lines 13; flags: `function` — `syntax IntSeq ::= strToCodes(String) [function]`
- `rule` lines 14; flags: `operational` — `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`
- `rule` lines 15; flags: `equational/pure` — `rule strToCodes("") => .IntSeq`
- `rule` lines 16-17; flags: `equational/pure` — `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128`
- `syntax` lines 20; flags: `function, total` — `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`
- `rule` lines 21; flags: `equational/pure` — `rule seqConcat(.IntSeq, T:IntSeq)                => T`
- `rule` lines 22; flags: `equational/pure` — `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`
- `rule` lines 24; flags: `equational/pure` — `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`
- `rule` lines 25; flags: `equational/pure` — `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`
- `rule` lines 26; flags: `equational/pure` — `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)`
- `rule` lines 29; flags: `equational/pure` — `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`
- `rule` lines 30; flags: `equational/pure` — `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`
- `syntax` lines 32; flags: `function, total` — `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`
- `rule` lines 33; flags: `equational/pure` — `rule strPrefix(.IntSeq, _:IntSeq)               => true`
- `rule` lines 34; flags: `equational/pure` — `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`
- `rule` lines 35; flags: `equational/pure` — `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`
- `syntax` lines 37; flags: `function, total` — `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`
- `rule` lines 38; flags: `equational/pure` — `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)`
- `rule` lines 39; flags: `equational/pure` — `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)`
- `rule` lines 40-41; flags: `equational/pure` — `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))`
- `syntax` lines 48; flags: `function, total` — `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`
- `rule` lines 49; flags: `equational/pure` — `rule strLt(.IntSeq, .IntSeq)                => false`
- `rule` lines 50; flags: `equational/pure` — `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`
- `rule` lines 51; flags: `equational/pure` — `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`
- `rule` lines 52; flags: `equational/pure` — `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B`
- `rule` lines 53; flags: `equational/pure` — `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B`
- `rule` lines 54; flags: `equational/pure` — `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`
- `rule` lines 56; flags: `equational/pure` — `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
- `rule` lines 57; flags: `equational/pure` — `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`
- `rule` lines 58; flags: `equational/pure` — `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`
- `rule` lines 59; flags: `equational/pure` — `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`

## `reference-semantics/semantics/subscript.k`

- `syntax` lines 11; flags: `function, total` — `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`
- `rule` lines 12; flags: `equational/pure` — `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V`
- `rule` lines 13-14; flags: `equational/pure` — `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0`
- `syntax` lines 16; flags: `function` — `syntax Int ::= intSeqAt(IntSeq, Int) [function]`
- `rule` lines 17; flags: `equational/pure` — `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C`
- `rule` lines 18-19; flags: `equational/pure` — `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0`
- `syntax` lines 21; flags: `function, total` — `syntax Int ::= normIdx(Int, Int) [function, total]`
- `rule` lines 22; flags: `equational/pure` — `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`
- `rule` lines 23; flags: `equational/pure` — `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0`
- `context` lines 27; flags: `none` — `context Subscript(HOLE, _)`
- `context` lines 28; flags: `none` — `context Subscript(_:Val, HOLE:Expr)`
- `rule` lines 31-33; flags: `priority, operational` — `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` lines 35; flags: `operational` — `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`
- `syntax` lines 37; flags: `function` — `syntax Val ::= applyIndex(Val, Int) [function]`
- `rule` lines 38; flags: `equational/pure` — `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
- `rule` lines 39; flags: `equational/pure` — `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
- `rule` lines 40-41; flags: `equational/pure` — `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))`
- `syntax` lines 44-47; flags: `none` — `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`
- `syntax` lines 49; flags: `none` — `syntax OptInt ::= "noB" | someB(Int)`
- `rule` lines 50; flags: `operational` — `rule <k> #evalB(NoBound)  => noB ... </k>`
- `rule` lines 51; flags: `operational` — `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>`
- `rule` lines 52; flags: `operational` — `rule <k> I:Int ~> #toSome => someB(I) ... </k>`
- `rule` lines 54; flags: `operational` — `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`
- `rule` lines 55; flags: `operational` — `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`
- `rule` lines 56; flags: `operational` — `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>`
- `rule` lines 58-60; flags: `priority, operational` — `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`
- `rule` lines 61; flags: `operational` — `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`
- `syntax` lines 63; flags: `function` — `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`
- `rule` lines 64-65; flags: `equational/pure` — `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
- `rule` lines 66-67; flags: `equational/pure` — `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
- `rule` lines 68-69; flags: `equational/pure` — `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))`
- `syntax` lines 72; flags: `function, total` — `syntax Int ::= slStep(OptInt) [function, total]`
- `rule` lines 73; flags: `equational/pure` — `rule slStep(noB)          => 1`
- `rule` lines 74; flags: `equational/pure` — `rule slStep(someB(S:Int)) => S`
- `syntax` lines 76; flags: `function` — `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`
- `rule` lines 77-78; flags: `equational/pure` — `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0`
- `rule` lines 79-80; flags: `equational/pure` — `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0`
- `rule` lines 81; flags: `equational/pure` — `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`
- `syntax` lines 83; flags: `function` — `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`
- `rule` lines 84-85; flags: `equational/pure` — `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0`
- `rule` lines 86-87; flags: `equational/pure` — `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0`
- `rule` lines 88; flags: `equational/pure` — `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`
- `syntax` lines 90; flags: `function, total` — `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`
- `rule` lines 91-92; flags: `equational/pure` — `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0`
- `rule` lines 93-94; flags: `equational/pure` — `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0`
- `syntax` lines 96; flags: `function, total` — `syntax Int ::= clampLo(Int, Int) [function, total]`
- `rule` lines 97-98; flags: `equational/pure` — `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0`
- `rule` lines 99-100; flags: `equational/pure` — `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0`
- `syntax` lines 102; flags: `function, total` — `syntax Int ::= clampHi(Int, Int, Int) [function, total]`
- `rule` lines 103-104; flags: `equational/pure` — `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN`
- `rule` lines 105-106; flags: `equational/pure` — `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN`
- `syntax` lines 109; flags: `function` — `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`
- `rule` lines 110-112; flags: `equational/pure` — `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
- `rule` lines 113-114; flags: `equational/pure` — `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`
- `syntax` lines 116; flags: `function` — `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`
- `rule` lines 117-119; flags: `equational/pure` — `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
- `rule` lines 120-121; flags: `equational/pure` — `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`

## `reference-semantics/semantics/syntax.k`

- `syntax` lines 9-30; flags: `macro` — `syntax Expr ::= "Int"      "(" Int ")" | "Float"    "(" Float ")" | "Bool"     "(" Bool ")" | "Name"     "(" String ")" | "Str"      "(" String ")" | "UnaryOp"  "(" String "," Expr ")" [strict(2)] | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp"    "(" String "," Exprs ")" | "ListExpr"  "(" Exprs ")" | "DictExpr"  "(" Entries ")" | "ListComp"  "(" Expr "," CompFors ")" [macro] | "GenExp"    "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda"    "(" Params "," Expr ")" | "KwArg"     "(" String "," Expr ")" | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call"      "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare"   "(" Expr "," CmpOp ")"`
- `syntax` lines 32; flags: `none` — `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"`
- `syntax` lines 33; flags: `none` — `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"`
- `syntax` lines 34; flags: `none` — `syntax Entries  ::= List{Entry, ","}`
- `syntax` lines 35; flags: `none` — `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`
- `syntax` lines 36; flags: `none` — `syntax CompFors ::= List{CompFor, ""}`
- `syntax` lines 37; flags: `none` — `syntax Exprs    ::= List{Expr, ","}`
- `syntax` lines 38; flags: `none` — `syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`
- `syntax` lines 39; flags: `none` — `syntax Bound    ::= Expr | "NoBound"`
- `syntax` lines 41-54; flags: `none` — `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] | "Import"    "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While"     "(" Expr "," Stmts ")" | "Break" | "Continue" | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return"    "(" Expr ")" [strict] | "Assert"    "(" Expr ")" [strict] | "Expr"      "(" Expr ")" [strict] | "FuncDef"   "(" String "," Params "," Stmts ")" | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`
- `syntax` lines 56; flags: `none` — `syntax Stmts      ::= List{Stmt, ""}`
- `syntax` lines 57; flags: `none` — `syntax Params     ::= "Params" "(" ParamNames ")"`
- `syntax` lines 58; flags: `none` — `syntax CellVars   ::= "CellVars" "(" ParamNames ")"`
- `syntax` lines 59; flags: `none` — `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"`
- `syntax` lines 60; flags: `none` — `syntax ParamNames ::= List{String, ","}`
- `syntax` lines 61; flags: `none` — `syntax Module     ::= "Module" "(" Stmts ")"`

## `reference-semantics/semantics/tuple.k`

- `rule` lines 10; flags: `operational` — `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>`
- `rule` lines 11; flags: `operational` — `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>`
- `syntax` lines 14; flags: `none` — `syntax ApplyK ::= "toTuple"`
- `rule` lines 15; flags: `operational` — `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`
- `rule` lines 16; flags: `operational` — `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`
- `rule` lines 18; flags: `equational/pure` — `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B`
- `rule` lines 20; flags: `operational` — `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`
- `rule` lines 21; flags: `operational` — `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>`
- `rule` lines 23; flags: `equational/pure` — `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`
- `syntax` lines 24; flags: `function` — `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`
- `rule` lines 25; flags: `equational/pure` — `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`
- `rule` lines 26-27; flags: `equational/pure` — `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)`
- `rule` lines 28; flags: `equational/pure` — `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)`
- `syntax` lines 31; flags: `none` — `syntax KItem ::= #bindTgt(Expr, Val)`
- `rule` lines 32-34; flags: `operational` — `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
- `rule` lines 35-41; flags: `priority, operational` — `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`
- `rule` lines 42; flags: `operational` — `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
- `rule` lines 43; flags: `operational` — `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`
- `rule` lines 44-46; flags: `priority, operational` — `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `syntax` lines 49; flags: `none` — `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`
- `rule` lines 50; flags: `operational` — `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
- `rule` lines 51; flags: `operational` — `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`
- `rule` lines 52-54; flags: `priority, operational` — `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
- `rule` lines 55-56; flags: `operational` — `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`
- `rule` lines 57; flags: `operational` — `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`

## `reference-semantics/semantics.k`

_No local configuration, syntax, context, rule, or claim statements._

## `verification.k`

- `syntax` lines 9; flags: `function` — `syntax Stmts ::= "modpBody" [function]`
- `rule` lines 10-12; flags: `equational/pure` — `rule modpBody => Expr(Str("Return 2^n modulo p.")) Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p")))`
- `syntax` lines 14; flags: `function` — `syntax Module ::= "modpProgram" [function]`
- `rule` lines 15-17; flags: `equational/pure` — `rule modpProgram => Module( FuncDef("modp", Params("n", "p"), modpBody))`
- `syntax` lines 22; flags: `function` — `syntax Int ::= specModp(Int, Int) [function]`
- `rule` lines 23-24; flags: `equational/pure` — `rule specModp(N:Int, P:Int) => pyMod(2 ^Int N, P) requires N >=Int 0 andBool P >Int 0`

## `spec.k`

- `claim` lines 6-30; flags: `none` — `claim <k> ( #loadAll(modpProgram) ~> Call(Name("modp"), (Int(N), Int(P), .Exprs)) ) => (specModp(N, P) ~> .K) </k> <env> 0 </env> <scopes> ( 0  |-> scope(.Map, parent(-1)) -1 |-> builtinsScope ) => ( 0  |-> scope( "modp" |-> closureVal( ("n", "p", .ParamNames), modpBody, 0), parent(-1)) -1 |-> builtinsScope ) </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires N >=Int 0 andBool P >Int 0`

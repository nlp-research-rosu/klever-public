# Exhaustive K source inventory

Generated from the fresh scratch source tree. A row is one top-level K sentence; multiline sentences retain their full source range and normalized text.

Total inventoried sentences: 1111

## Category counts

| Category | Count |
|---|---:|
| `claim` | 3 |
| `configuration` | 1 |
| `context` | 5 |
| `endmodule` | 29 |
| `imports` | 90 |
| `module` | 29 |
| `requires` | 25 |
| `rule` | 593 |
| `rule/concrete` | 35 |
| `rule/owise` | 26 |
| `rule/priority` | 45 |
| `rule/simplification` | 1 |
| `syntax` | 77 |
| `syntax/function` | 41 |
| `syntax/function/total` | 82 |
| `syntax/function/total/opaque-symbol` | 25 |
| `syntax/macro` | 4 |

## Opaque and symbolic declarations

- `semantics/builtins.k:285` — `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:24` — `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:30` — `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:37` — `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:50` — `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:54` — `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:73` — `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:86` — `syntax Float ::= toF(Val) [function, total, symbol(toF)]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:93` — `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:103` — `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:107` — `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:111` — `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:115` — `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:119` — `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:125` — `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:142` — `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:160` — `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:190` — `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:195` — `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:209` — `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:217` — `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:223` — `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/float.k:230` — `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/sort.k:18` — `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path
- `semantics/sort.k:49` — `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` — FIXED SUPPLIED opaque boundary; unreachable on target path

## Sentence-by-sentence inventory

| ID | Source | Category | Normalized sentence | Review disposition |
|---:|---|---|---|---|
| 1 | `semantics.k:34` | `requires` | `requires "semantics/syntax.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 2 | `semantics.k:35` | `requires` | `requires "semantics/core.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 3 | `semantics.k:36` | `requires` | `requires "semantics/iter.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 4 | `semantics.k:37` | `requires` | `requires "semantics/range.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 5 | `semantics.k:38` | `requires` | `requires "semantics/operators.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 6 | `semantics.k:39` | `requires` | `requires "semantics/int.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 7 | `semantics.k:40` | `requires` | `requires "semantics/bool.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 8 | `semantics.k:41` | `requires` | `requires "semantics/float.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 9 | `semantics.k:42` | `requires` | `requires "semantics/str.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 10 | `semantics.k:43` | `requires` | `requires "semantics/set.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 11 | `semantics.k:44` | `requires` | `requires "semantics/list.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 12 | `semantics.k:45` | `requires` | `requires "semantics/tuple.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 13 | `semantics.k:46` | `requires` | `requires "semantics/subscript.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 14 | `semantics.k:47` | `requires` | `requires "semantics/comprehension.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 15 | `semantics.k:48` | `requires` | `requires "semantics/methods.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 16 | `semantics.k:49` | `requires` | `requires "semantics/controls.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 17 | `semantics.k:50` | `requires` | `requires "semantics/functions.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 18 | `semantics.k:51` | `requires` | `requires "semantics/builtins.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 19 | `semantics.k:52` | `requires` | `requires "semantics/call.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 20 | `semantics.k:53` | `requires` | `requires "semantics/sort.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 21 | `semantics.k:54` | `requires` | `requires "semantics/assert.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 22 | `semantics.k:55` | `requires` | `requires "semantics/dict.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 23 | `semantics.k:56` | `requires` | `requires "semantics/concrete.k"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 24 | `semantics.k:58` | `module` | `module MPY` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 25 | `semantics.k:59` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 26 | `semantics.k:60` | `imports` | `imports MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 27 | `semantics.k:61` | `imports` | `imports MPY-RANGE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 28 | `semantics.k:62` | `imports` | `imports MPY-OPERATORS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 29 | `semantics.k:63` | `imports` | `imports MPY-INT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 30 | `semantics.k:64` | `imports` | `imports MPY-BOOL` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 31 | `semantics.k:65` | `imports` | `imports MPY-FLOAT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 32 | `semantics.k:66` | `imports` | `imports MPY-STR` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 33 | `semantics.k:67` | `imports` | `imports MPY-SET` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 34 | `semantics.k:68` | `imports` | `imports MPY-LIST` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 35 | `semantics.k:69` | `imports` | `imports MPY-TUPLE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 36 | `semantics.k:70` | `imports` | `imports MPY-SUBSCRIPT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 37 | `semantics.k:71` | `imports` | `imports MPY-COMPREHENSION` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 38 | `semantics.k:72` | `imports` | `imports MPY-METHODS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 39 | `semantics.k:73` | `imports` | `imports MPY-CONTROLS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 40 | `semantics.k:74` | `imports` | `imports MPY-FUNCTIONS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 41 | `semantics.k:75` | `imports` | `imports MPY-BUILTINS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 42 | `semantics.k:76` | `imports` | `imports MPY-CALL` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 43 | `semantics.k:77` | `imports` | `imports MPY-SORT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 44 | `semantics.k:78` | `imports` | `imports MPY-ASSERT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 45 | `semantics.k:79` | `imports` | `imports MPY-DICT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 46 | `semantics.k:80` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 47 | `semantics.k:87` | `module` | `module MPY-KRUN` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 48 | `semantics.k:88` | `imports` | `imports MPY` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 49 | `semantics.k:89` | `imports` | `imports MPY-CONCRETE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 50 | `semantics.k:90` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 51 | `semantics/assert.k:3` | `module` | `module MPY-ASSERT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 52 | `semantics/assert.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 53 | `semantics/assert.k:6-7` | `rule` | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 54 | `semantics/assert.k:8-11` | `rule` | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 55 | `semantics/assert.k:13-15` | `rule/priority` | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 56 | `semantics/assert.k:16` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 57 | `semantics/bool.k:5` | `module` | `module MPY-BOOL` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 58 | `semantics/bool.k:6` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 59 | `semantics/bool.k:8` | `rule` | `rule applyUn("not", V:Val) => notBool truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 60 | `semantics/bool.k:10` | `rule` | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 61 | `semantics/bool.k:11` | `rule` | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 62 | `semantics/bool.k:16` | `context` | `context BoolOp(_, (HOLE:Expr, _:Exprs))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 63 | `semantics/bool.k:17` | `rule` | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 64 | `semantics/bool.k:18-19` | `rule` | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 65 | `semantics/bool.k:20-21` | `rule` | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 66 | `semantics/bool.k:22-23` | `rule` | `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 67 | `semantics/bool.k:24-25` | `rule` | `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 68 | `semantics/bool.k:29-30` | `rule/priority` | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 69 | `semantics/bool.k:31-34` | `rule/priority` | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 70 | `semantics/bool.k:35-38` | `rule/priority` | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 71 | `semantics/bool.k:39-42` | `rule/priority` | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 72 | `semantics/bool.k:43-46` | `rule/priority` | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 73 | `semantics/bool.k:47` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 74 | `semantics/builtins.k:3` | `module` | `module MPY-BUILTINS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 75 | `semantics/builtins.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 76 | `semantics/builtins.k:5` | `imports` | `imports MPY-STR` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 77 | `semantics/builtins.k:6` | `imports` | `imports MPY-SET` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 78 | `semantics/builtins.k:7` | `imports` | `imports MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 79 | `semantics/builtins.k:8` | `imports` | `imports MPY-RANGE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 80 | `semantics/builtins.k:9` | `imports` | `imports MPY-INT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 81 | `semantics/builtins.k:10` | `imports` | `imports MPY-METHODS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 82 | `semantics/builtins.k:17` | `syntax/function` | `syntax Val ::= applyBuiltin(String, Vals) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 83 | `semantics/builtins.k:20` | `syntax/function` | `syntax Int ::= seqLen(Val) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 84 | `semantics/builtins.k:21` | `rule` | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 85 | `semantics/builtins.k:22` | `rule` | `rule seqLen(list(VS:ValSeq)) => vsLen(VS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 86 | `semantics/builtins.k:23` | `rule` | `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 87 | `semantics/builtins.k:24` | `rule` | `rule seqLen(str(IS:IntSeq)) => isLen(IS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 88 | `semantics/builtins.k:25` | `rule` | `rule seqLen(setV(DS:IntSeq)) => isLen(DS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 89 | `semantics/builtins.k:26` | `rule` | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 90 | `semantics/builtins.k:32` | `rule` | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 91 | `semantics/builtins.k:33` | `rule` | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 92 | `semantics/builtins.k:34` | `rule` | `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 93 | `semantics/builtins.k:35` | `rule` | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 94 | `semantics/builtins.k:36` | `syntax/function/total` | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 95 | `semantics/builtins.k:37` | `rule` | `rule charsOf(.IntSeq) => .ValSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 96 | `semantics/builtins.k:38` | `rule` | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 97 | `semantics/builtins.k:41` | `rule` | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 98 | `semantics/builtins.k:44` | `rule` | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 99 | `semantics/builtins.k:47` | `syntax` | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 100 | `semantics/builtins.k:48` | `rule` | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 101 | `semantics/builtins.k:49` | `rule` | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 102 | `semantics/builtins.k:50-52` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 103 | `semantics/builtins.k:54` | `syntax/function` | `syntax Int ::= intOf(Val) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 104 | `semantics/builtins.k:55` | `rule` | `rule intOf(I:Int) => I` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 105 | `semantics/builtins.k:56` | `rule` | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 106 | `semantics/builtins.k:59` | `syntax` | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 107 | `semantics/builtins.k:60` | `rule` | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 108 | `semantics/builtins.k:61` | `rule` | `rule <k> #iterDone ~> #allCont => true ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 109 | `semantics/builtins.k:62-63` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 110 | `semantics/builtins.k:64-65` | `rule` | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 111 | `semantics/builtins.k:67` | `syntax` | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 112 | `semantics/builtins.k:68` | `rule` | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 113 | `semantics/builtins.k:69` | `rule` | `rule <k> #iterDone ~> #anyCont => false ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 114 | `semantics/builtins.k:70-71` | `rule` | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 115 | `semantics/builtins.k:72-73` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 116 | `semantics/builtins.k:76` | `syntax` | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 117 | `semantics/builtins.k:77` | `rule` | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 118 | `semantics/builtins.k:78-79` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 119 | `semantics/builtins.k:80` | `rule` | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 120 | `semantics/builtins.k:81` | `rule` | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 121 | `semantics/builtins.k:82-84` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 122 | `semantics/builtins.k:86` | `syntax` | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 123 | `semantics/builtins.k:87` | `rule` | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 124 | `semantics/builtins.k:88-89` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 125 | `semantics/builtins.k:90` | `rule` | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 126 | `semantics/builtins.k:91` | `rule` | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 127 | `semantics/builtins.k:92-94` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 128 | `semantics/builtins.k:97` | `syntax/function` | `syntax Int ::= maxVals(Int, Vals) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 129 | `semantics/builtins.k:98` | `rule` | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 130 | `semantics/builtins.k:99` | `rule` | `rule maxVals(M:Int, .Vals) => M` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 131 | `semantics/builtins.k:100` | `rule` | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 132 | `semantics/builtins.k:102` | `syntax/function` | `syntax Int ::= minVals(Int, Vals) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 133 | `semantics/builtins.k:103` | `rule` | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 134 | `semantics/builtins.k:104` | `rule` | `rule minVals(M:Int, .Vals) => M` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 135 | `semantics/builtins.k:105` | `rule` | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 136 | `semantics/builtins.k:108-109` | `rule` | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 137 | `semantics/builtins.k:111-113` | `rule` | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 138 | `semantics/builtins.k:114` | `syntax/function/total` | `syntax IntSeq ::= binCodes(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 139 | `semantics/builtins.k:115` | `rule` | `rule binCodes(0) => iCons(48, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 140 | `semantics/builtins.k:116` | `rule` | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 141 | `semantics/builtins.k:117` | `syntax/function/total` | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 142 | `semantics/builtins.k:118` | `rule` | `rule binAcc(0, ACC:IntSeq) => ACC` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 143 | `semantics/builtins.k:119-121` | `rule` | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 144 | `semantics/builtins.k:124-125` | `rule` | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 145 | `semantics/builtins.k:126` | `syntax/function/total` | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 146 | `semantics/builtins.k:127` | `rule` | `rule enumVS(.ValSeq, _:Int) => .ValSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 147 | `semantics/builtins.k:128-129` | `rule` | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 148 | `semantics/builtins.k:132-133` | `rule` | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 149 | `semantics/builtins.k:134` | `syntax/function/total` | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 150 | `semantics/builtins.k:135` | `rule` | `rule mapStrVS(.ValSeq) => .ValSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 151 | `semantics/builtins.k:136` | `rule` | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 152 | `semantics/builtins.k:137` | `rule` | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 153 | `semantics/builtins.k:140` | `rule` | `rule applyBuiltin("int", I:Int, .Vals) => I` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 154 | `semantics/builtins.k:143` | `rule` | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 155 | `semantics/builtins.k:144-145` | `rule` | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 156 | `semantics/builtins.k:148` | `rule` | `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 157 | `semantics/builtins.k:149` | `rule` | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 158 | `semantics/builtins.k:152-153` | `rule` | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 159 | `semantics/builtins.k:156-157` | `rule` | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 160 | `semantics/builtins.k:158` | `syntax/function/total` | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 161 | `semantics/builtins.k:159` | `rule` | `rule intDigAcc(.IntSeq, ACC:Int) => ACC` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 162 | `semantics/builtins.k:160` | `rule` | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 163 | `semantics/builtins.k:163` | `rule` | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 164 | `semantics/builtins.k:164` | `rule` | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 165 | `semantics/builtins.k:167-168` | `rule` | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 166 | `semantics/builtins.k:169` | `rule` | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 167 | `semantics/builtins.k:170` | `rule` | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 168 | `semantics/builtins.k:171-172` | `rule` | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 169 | `semantics/builtins.k:173` | `rule` | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 170 | `semantics/builtins.k:174` | `rule` | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 171 | `semantics/builtins.k:177` | `rule` | `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 172 | `semantics/builtins.k:178` | `rule` | `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 173 | `semantics/builtins.k:179-180` | `rule` | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 174 | `semantics/builtins.k:187` | `rule` | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 175 | `semantics/builtins.k:188` | `syntax/function` | `syntax Int ::= evalArith(IntSeq) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 176 | `semantics/builtins.k:189-190` | `rule` | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 177 | `semantics/builtins.k:192` | `syntax` | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 178 | `semantics/builtins.k:194` | `syntax/function/total` | `syntax Bool ::= evDigit(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 179 | `semantics/builtins.k:195` | `rule` | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 180 | `semantics/builtins.k:196` | `syntax/function/total` | `syntax Bool ::= evHead42(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 181 | `semantics/builtins.k:197` | `rule` | `rule evHead42(iCons(42, _:IntSeq)) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 182 | `semantics/builtins.k:198` | `rule/owise` | `rule evHead42(_:IntSeq) => false [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 183 | `semantics/builtins.k:199` | `syntax/function/total` | `syntax Bool ::= evHead47(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 184 | `semantics/builtins.k:200` | `rule` | `rule evHead47(iCons(47, _:IntSeq)) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 185 | `semantics/builtins.k:201` | `rule/owise` | `rule evHead47(_:IntSeq) => false [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 186 | `semantics/builtins.k:203` | `syntax/function/total` | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 187 | `semantics/builtins.k:204` | `rule` | `rule tokOps(.IntSeq) => .OpSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 188 | `semantics/builtins.k:205` | `rule` | `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 189 | `semantics/builtins.k:206` | `rule` | `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 190 | `semantics/builtins.k:207` | `rule` | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 191 | `semantics/builtins.k:208` | `rule` | `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 192 | `semantics/builtins.k:209` | `rule` | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 193 | `semantics/builtins.k:210` | `rule` | `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 194 | `semantics/builtins.k:211` | `rule` | `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 195 | `semantics/builtins.k:212` | `rule` | `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 196 | `semantics/builtins.k:214-215` | `syntax/function/total` | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 197 | `semantics/builtins.k:216` | `rule` | `rule tokNds(.IntSeq) => .IntSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 198 | `semantics/builtins.k:217` | `rule` | `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 199 | `semantics/builtins.k:218` | `rule` | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 200 | `semantics/builtins.k:219-220` | `rule` | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 201 | `semantics/builtins.k:221-222` | `rule` | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 202 | `semantics/builtins.k:223` | `rule/owise` | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 203 | `semantics/builtins.k:225` | `syntax` | `syntax EvPair ::= evp(OpSeq, IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 204 | `semantics/builtins.k:226` | `syntax/function/total` | `syntax Int ::= firstNdE(EvPair) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 205 | `semantics/builtins.k:227` | `rule` | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 206 | `semantics/builtins.k:228` | `rule/owise` | `rule firstNdE(_:EvPair) => 0 [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 207 | `semantics/builtins.k:230` | `syntax/function/total` | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 208 | `semantics/builtins.k:231` | `rule` | `rule applyOpE("+", A:Int, B:Int) => A +Int B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 209 | `semantics/builtins.k:232` | `rule` | `rule applyOpE("-", A:Int, B:Int) => A -Int B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 210 | `semantics/builtins.k:233` | `rule` | `rule applyOpE("*", A:Int, B:Int) => A *Int B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 211 | `semantics/builtins.k:234` | `rule` | `rule applyOpE("//", A:Int, B:Int) => A divInt B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 212 | `semantics/builtins.k:235` | `rule` | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 213 | `semantics/builtins.k:236` | `rule/owise` | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 214 | `semantics/builtins.k:238` | `syntax/function/total` | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 215 | `semantics/builtins.k:239` | `rule` | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 216 | `semantics/builtins.k:240` | `rule` | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 217 | `semantics/builtins.k:241-242` | `rule` | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 218 | `semantics/builtins.k:243` | `rule/owise` | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 219 | `semantics/builtins.k:244` | `syntax/function/total` | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 220 | `semantics/builtins.k:245` | `rule` | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 221 | `semantics/builtins.k:246` | `rule` | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 222 | `semantics/builtins.k:247` | `syntax/function/total` | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 223 | `semantics/builtins.k:248` | `rule` | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 224 | `semantics/builtins.k:250` | `syntax/function/total` | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 225 | `semantics/builtins.k:251` | `rule` | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 226 | `semantics/builtins.k:252` | `rule` | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 227 | `semantics/builtins.k:253` | `rule` | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 228 | `semantics/builtins.k:254` | `rule` | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 229 | `semantics/builtins.k:255` | `syntax/function/total` | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 230 | `semantics/builtins.k:256` | `rule` | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 231 | `semantics/builtins.k:257-259` | `rule` | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 232 | `semantics/builtins.k:260-262` | `rule` | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 233 | `semantics/builtins.k:263-264` | `rule/owise` | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 234 | `semantics/builtins.k:265` | `syntax/function/total` | `syntax Bool ::= inLevelE(String, String) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 235 | `semantics/builtins.k:266` | `rule` | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 236 | `semantics/builtins.k:267` | `rule` | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 237 | `semantics/builtins.k:268` | `rule/owise` | `rule inLevelE(_:String, _:String) => false [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 238 | `semantics/builtins.k:269` | `syntax/function/total` | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 239 | `semantics/builtins.k:270` | `rule` | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 240 | `semantics/builtins.k:271` | `rule` | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 241 | `semantics/builtins.k:272` | `syntax/function/total` | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 242 | `semantics/builtins.k:273` | `rule` | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 243 | `semantics/builtins.k:274` | `rule` | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 244 | `semantics/builtins.k:279` | `syntax` | `syntax KItem ::= "#md5"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 245 | `semantics/builtins.k:280-281` | `rule/priority` | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 246 | `semantics/builtins.k:282` | `rule` | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 247 | `semantics/builtins.k:283` | `syntax` | `syntax Val ::= md5Obj(IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 248 | `semantics/builtins.k:284` | `rule` | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 249 | `semantics/builtins.k:285` | `syntax/function/total/opaque-symbol` | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 250 | `semantics/builtins.k:291` | `rule` | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 251 | `semantics/builtins.k:292` | `rule` | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 252 | `semantics/builtins.k:293` | `syntax/function` | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 253 | `semantics/builtins.k:294` | `rule` | `rule isIntV(_:Int) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 254 | `semantics/builtins.k:295` | `rule/owise` | `rule isIntV(_:Val) => false [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 255 | `semantics/builtins.k:296` | `rule` | `rule isStrV(str(_:IntSeq)) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 256 | `semantics/builtins.k:297` | `rule/owise` | `rule isStrV(_:Val) => false [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 257 | `semantics/builtins.k:298` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 258 | `semantics/call.k:10` | `module` | `module MPY-CALL` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 259 | `semantics/call.k:11` | `imports` | `imports MPY-METHODS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 260 | `semantics/call.k:12` | `imports` | `imports MPY-BUILTINS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 261 | `semantics/call.k:13` | `imports` | `imports MPY-FUNCTIONS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 262 | `semantics/call.k:16` | `rule` | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 263 | `semantics/call.k:19` | `syntax` | `syntax KItem ::= #callee(Exprs)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 264 | `semantics/call.k:20` | `rule/owise` | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 265 | `semantics/call.k:21` | `rule` | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 266 | `semantics/call.k:24` | `rule` | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 267 | `semantics/call.k:26` | `rule` | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 268 | `semantics/call.k:27` | `rule` | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 269 | `semantics/call.k:28` | `rule` | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 270 | `semantics/call.k:29` | `rule` | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 271 | `semantics/call.k:30` | `rule` | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 272 | `semantics/call.k:31` | `rule/owise` | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 273 | `semantics/call.k:32` | `rule` | `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 274 | `semantics/call.k:38-41` | `rule/priority` | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 275 | `semantics/call.k:42-46` | `rule/priority` | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 276 | `semantics/call.k:47-50` | `rule/priority` | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 277 | `semantics/call.k:52` | `syntax/function/total` | `syntax Bool ::= isMutMethod(String) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 278 | `semantics/call.k:53-55` | `rule` | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 279 | `semantics/call.k:56-60` | `rule/priority` | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 280 | `semantics/call.k:63-67` | `rule/priority` | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 281 | `semantics/call.k:69-74` | `rule` | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 282 | `semantics/call.k:80-85` | `rule` | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 283 | `semantics/call.k:87` | `syntax` | `syntax KItem ::= #allocCells(ParamNames)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 284 | `semantics/call.k:88` | `rule` | `rule <k> #allocCells(.ParamNames) => .K ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 285 | `semantics/call.k:89-94` | `rule` | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 286 | `semantics/call.k:95` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 287 | `semantics/comprehension.k:3` | `module` | `module MPY-COMPREHENSION` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 288 | `semantics/comprehension.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 289 | `semantics/comprehension.k:5` | `imports` | `imports MPY-OPERATORS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 290 | `semantics/comprehension.k:6` | `imports` | `imports MPY-LIST` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 291 | `semantics/comprehension.k:7` | `imports` | `imports MPY-CONTROLS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 292 | `semantics/comprehension.k:8` | `imports` | `imports MPY-FUNCTIONS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 293 | `semantics/comprehension.k:11` | `rule` | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 294 | `semantics/comprehension.k:12` | `rule` | `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 295 | `semantics/comprehension.k:14` | `syntax/macro` | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 296 | `semantics/comprehension.k:15-16` | `rule` | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 297 | `semantics/comprehension.k:18` | `syntax/macro` | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 298 | `semantics/comprehension.k:19-20` | `rule` | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 299 | `semantics/comprehension.k:21-22` | `rule` | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 300 | `semantics/comprehension.k:24` | `syntax/macro` | `syntax Expr ::= compGuard(Exprs) [macro]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 301 | `semantics/comprehension.k:25` | `rule` | `rule compGuard(.Exprs) => Bool(true)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 302 | `semantics/comprehension.k:26` | `rule` | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 303 | `semantics/comprehension.k:27` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 304 | `semantics/concrete.k:8` | `module` | `module MPY-CONCRETE` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 305 | `semantics/concrete.k:9` | `imports` | `imports MPY` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 306 | `semantics/concrete.k:13-15` | `rule` | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 307 | `semantics/concrete.k:16-18` | `rule` | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 308 | `semantics/concrete.k:25` | `syntax` | `syntax Val ::= kvP(Val, Val)` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 309 | `semantics/concrete.k:26-27` | `syntax` | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 310 | `semantics/concrete.k:28-30` | `rule/priority` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 311 | `semantics/concrete.k:31-33` | `rule/priority` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 312 | `semantics/concrete.k:34-35` | `rule` | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 313 | `semantics/concrete.k:36-37` | `rule` | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 314 | `semantics/concrete.k:38-40` | `rule` | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 315 | `semantics/concrete.k:42` | `syntax/function` | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 316 | `semantics/concrete.k:43` | `rule` | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 317 | `semantics/concrete.k:44-46` | `rule` | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 318 | `semantics/concrete.k:47-49` | `rule` | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 319 | `semantics/concrete.k:51` | `syntax/function` | `syntax Bool ::= kLt(Val, Val) [function]` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 320 | `semantics/concrete.k:52` | `rule` | `rule kLt(I1:Int, I2:Int) => I1 <Int I2` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 321 | `semantics/concrete.k:53` | `rule` | `rule kLt(F1:Float, F2:Float) => F1 <Float F2` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 322 | `semantics/concrete.k:54` | `rule` | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 323 | `semantics/concrete.k:56` | `syntax/function/total` | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 324 | `semantics/concrete.k:57` | `rule` | `rule unpairVS(.ValSeq) => .ValSeq` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 325 | `semantics/concrete.k:58` | `rule` | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 326 | `semantics/concrete.k:59` | `rule/owise` | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 327 | `semantics/concrete.k:60` | `endmodule` | `endmodule` | FIXED SUPPLIED, LLVM-only; excluded from proof definition |
| 328 | `semantics/controls.k:3` | `module` | `module MPY-CONTROLS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 329 | `semantics/controls.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 330 | `semantics/controls.k:5` | `imports` | `imports MPY-TUPLE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 331 | `semantics/controls.k:6` | `imports` | `imports MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 332 | `semantics/controls.k:9-11` | `rule` | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 333 | `semantics/controls.k:12-18` | `rule/priority` | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 334 | `semantics/controls.k:20-23` | `rule` | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 335 | `semantics/controls.k:27-31` | `rule/priority` | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 336 | `semantics/controls.k:35` | `rule` | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 337 | `semantics/controls.k:36` | `rule/owise` | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 338 | `semantics/controls.k:37` | `syntax` | `syntax KItem ::= #bindImports(ParamNames)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 339 | `semantics/controls.k:38` | `rule` | `rule <k> #bindImports(.ParamNames) => .K ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 340 | `semantics/controls.k:39-42` | `rule` | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 341 | `semantics/controls.k:43-44` | `rule` | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 342 | `semantics/controls.k:48` | `rule` | `rule <k> Expr(_:Val) => .K ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 343 | `semantics/controls.k:51` | `syntax` | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 344 | `semantics/controls.k:52` | `rule` | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 345 | `semantics/controls.k:53` | `rule` | `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 346 | `semantics/controls.k:54` | `rule` | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 347 | `semantics/controls.k:57-58` | `rule` | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 348 | `semantics/controls.k:59-60` | `rule` | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 349 | `semantics/controls.k:65-67` | `syntax` | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 350 | `semantics/controls.k:69` | `rule` | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 351 | `semantics/controls.k:71` | `rule` | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 352 | `semantics/controls.k:72` | `rule` | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 353 | `semantics/controls.k:73-74` | `rule` | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 354 | `semantics/controls.k:77` | `rule` | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 355 | `semantics/controls.k:78` | `rule` | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 356 | `semantics/controls.k:79-80` | `rule` | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 357 | `semantics/controls.k:81-82` | `rule` | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 358 | `semantics/controls.k:85` | `rule` | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 359 | `semantics/controls.k:86` | `rule` | `rule <k> Continue => #cont ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 360 | `semantics/controls.k:87` | `rule` | `rule <k> Break => #brk ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 361 | `semantics/controls.k:88` | `rule` | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 362 | `semantics/controls.k:89` | `rule/owise` | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 363 | `semantics/controls.k:90` | `rule` | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 364 | `semantics/controls.k:91` | `rule/owise` | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 365 | `semantics/controls.k:95-97` | `rule/priority` | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 366 | `semantics/controls.k:98-100` | `rule/priority` | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 367 | `semantics/controls.k:101-103` | `rule/priority` | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 368 | `semantics/controls.k:106-108` | `rule/priority` | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 369 | `semantics/controls.k:109` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 370 | `semantics/core.k:3` | `module` | `module MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 371 | `semantics/core.k:4` | `imports` | `imports MPY-SYNTAX` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 372 | `semantics/core.k:5` | `imports` | `imports INT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 373 | `semantics/core.k:6` | `imports` | `imports BOOL` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 374 | `semantics/core.k:7` | `imports` | `imports STRING` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 375 | `semantics/core.k:8` | `imports` | `imports MAP` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 376 | `semantics/core.k:9` | `imports` | `imports LIST` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 377 | `semantics/core.k:10` | `imports` | `imports K-EQUAL` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 378 | `semantics/core.k:13` | `syntax` | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 379 | `semantics/core.k:14` | `syntax` | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 380 | `semantics/core.k:15` | `syntax` | `syntax Str ::= str(IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 381 | `semantics/core.k:18-23` | `syntax` | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 382 | `semantics/core.k:25-34` | `syntax/function` | `syntax Val ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) // a heap object: <heap> holds its list(VS) \| cellRef(Int) // a closure cell: <heap> holds cellV(V) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) // a type object (int/str), resolved from the builtins frame \| builtinV(String) // a builtin function, resolved like any name (LEGB fallthrough) \| boundMethodV(Val, String) // a cooled Attribute: obj.method` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 383 | `semantics/core.k:36` | `syntax` | `syntax Parent ::= "root" \| parent(Int)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 384 | `semantics/core.k:37` | `syntax` | `syntax Scope ::= scope(Map, Parent)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 385 | `semantics/core.k:38` | `syntax` | `syntax KResult ::= Val` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 386 | `semantics/core.k:39` | `syntax` | `syntax Expr ::= Val // cooling puts results back into expression holes` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 387 | `semantics/core.k:40` | `syntax` | `syntax Vals ::= List{Val, ","}` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 388 | `semantics/core.k:41` | `syntax` | `syntax Exc ::= "NoExc" \| "AssertionError"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 389 | `semantics/core.k:42` | `syntax` | `syntax RetState ::= "noRet" \| retV(Val)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 390 | `semantics/core.k:49-60` | `configuration` | `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 391 | `semantics/core.k:68` | `syntax/function/total` | `syntax Bool ::= isRefV(Val) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 392 | `semantics/core.k:69` | `rule` | `rule isRefV(ref(_:Int)) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 393 | `semantics/core.k:70` | `rule/owise` | `rule isRefV(_:Val) => false [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 394 | `semantics/core.k:75` | `syntax` | `syntax HeapVal ::= cellV(Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 395 | `semantics/core.k:76` | `syntax/function/total` | `syntax Bool ::= isCellRef(Val) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 396 | `semantics/core.k:77` | `rule` | `rule isCellRef(cellRef(_:Int)) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 397 | `semantics/core.k:78` | `rule/owise` | `rule isCellRef(_:Val) => false [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 398 | `semantics/core.k:85-90` | `rule/priority` | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 399 | `semantics/core.k:95` | `syntax` | `syntax Val ::= kwV(String, Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 400 | `semantics/core.k:96` | `syntax` | `syntax KItem ::= #kwTag(String)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 401 | `semantics/core.k:97` | `rule` | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 402 | `semantics/core.k:98-99` | `rule` | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 403 | `semantics/core.k:100` | `syntax/function/total` | `syntax Bool ::= isKwV(Val) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 404 | `semantics/core.k:101` | `rule` | `rule isKwV(kwV(_:String, _:Val)) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 405 | `semantics/core.k:102` | `rule/owise` | `rule isKwV(_:Val) => false [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 406 | `semantics/core.k:106` | `syntax` | `syntax Val ::= cellsMark(ParamNames)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 407 | `semantics/core.k:107` | `syntax/function` | `syntax ParamNames ::= cellsOf(Val) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 408 | `semantics/core.k:108` | `rule` | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 409 | `semantics/core.k:109` | `syntax/function/total` | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 410 | `semantics/core.k:110` | `rule` | `rule pnMember(_:String, .ParamNames) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 411 | `semantics/core.k:111` | `rule` | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 412 | `semantics/core.k:113` | `syntax` | `syntax KItem ::= #cellW(Val, Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 413 | `semantics/core.k:114-115` | `rule` | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 414 | `semantics/core.k:117` | `syntax` | `syntax KItem ::= #alloc(Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 415 | `semantics/core.k:118-121` | `rule` | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 416 | `semantics/core.k:124` | `syntax` | `syntax KItem ::= #loadAll(Module)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 417 | `semantics/core.k:125` | `rule` | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 418 | `semantics/core.k:126` | `rule` | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 419 | `semantics/core.k:127` | `rule` | `rule <k> .Stmts => .K ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 420 | `semantics/core.k:130` | `syntax` | `syntax KItem ::= #look(String, Int)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 421 | `semantics/core.k:131` | `rule` | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 422 | `semantics/core.k:132-134` | `rule` | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 423 | `semantics/core.k:145-151` | `rule/priority` | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 424 | `semantics/core.k:152-154` | `rule` | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 425 | `semantics/core.k:157` | `syntax/function/total` | `syntax Scope ::= "builtinsScope" [function, total]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 426 | `semantics/core.k:158-181` | `rule` | `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 427 | `semantics/core.k:185` | `syntax` | `syntax ApplyK ::= toCall(Val)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 428 | `semantics/core.k:186-188` | `syntax` | `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 429 | `semantics/core.k:189` | `rule` | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 430 | `semantics/core.k:190` | `rule` | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 431 | `semantics/core.k:191` | `rule` | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 432 | `semantics/core.k:194` | `rule` | `rule <k> Int(I:Int) => I ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 433 | `semantics/core.k:195` | `rule` | `rule <k> Bool(B:Bool) => B ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 434 | `semantics/core.k:196` | `rule` | `rule <k> NoneVal => noneV ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 435 | `semantics/core.k:199` | `syntax/function` | `syntax Bool ::= truthy(Val) [function]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 436 | `semantics/core.k:200` | `rule` | `rule truthy(B:Bool) => B` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 437 | `semantics/core.k:201` | `rule` | `rule truthy(noneV) => false` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 438 | `semantics/core.k:202` | `rule` | `rule truthy(I:Int) => I =/=Int 0` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 439 | `semantics/core.k:203` | `rule` | `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 440 | `semantics/core.k:204` | `rule` | `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 441 | `semantics/core.k:205` | `rule` | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 442 | `semantics/core.k:208` | `syntax/function` | `syntax Val ::= applyUn(String, Val) [function]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 443 | `semantics/core.k:209` | `syntax/function` | `syntax Val ::= applyBin(String, Val, Val) [function]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 444 | `semantics/core.k:210` | `syntax/function` | `syntax Bool ::= applyCmp(String, Val, Val) [function]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 445 | `semantics/core.k:213` | `syntax/function/total` | `syntax Vals ::= appendVal(Vals, Val) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 446 | `semantics/core.k:214` | `rule` | `rule appendVal(.Vals, V:Val) => V , .Vals` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 447 | `semantics/core.k:215` | `rule` | `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 448 | `semantics/core.k:217` | `syntax/function/total` | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 449 | `semantics/core.k:218` | `rule` | `rule vals2valSeq(.Vals) => .ValSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 450 | `semantics/core.k:219` | `rule` | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 451 | `semantics/core.k:223` | `syntax/function/total` | `syntax Int ::= vsLen(ValSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 452 | `semantics/core.k:224` | `rule` | `rule vsLen(.ValSeq) => 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 453 | `semantics/core.k:225` | `rule` | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 454 | `semantics/core.k:227` | `syntax/function/total` | `syntax Int ::= isLen(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 455 | `semantics/core.k:228` | `rule` | `rule isLen(.IntSeq) => 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 456 | `semantics/core.k:229` | `rule` | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 457 | `semantics/core.k:233` | `syntax/function/total` | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 458 | `semantics/core.k:234` | `rule` | `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 459 | `semantics/core.k:235` | `rule` | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 460 | `semantics/core.k:236-237` | `rule` | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 461 | `semantics/core.k:238-239` | `rule` | `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 462 | `semantics/core.k:240` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 463 | `semantics/dict.k:13` | `module` | `module MPY-DICT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 464 | `semantics/dict.k:14` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 465 | `semantics/dict.k:15` | `imports` | `imports MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 466 | `semantics/dict.k:16` | `imports` | `imports MPY-METHODS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 467 | `semantics/dict.k:17` | `imports` | `imports MPY-LIST` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 468 | `semantics/dict.k:20` | `syntax` | `syntax Val ::= dictV(ValSeq, ValSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 469 | `semantics/dict.k:23-25` | `syntax` | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 470 | `semantics/dict.k:26` | `rule` | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 471 | `semantics/dict.k:27` | `rule` | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 472 | `semantics/dict.k:28-29` | `rule` | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 473 | `semantics/dict.k:30-31` | `rule` | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 474 | `semantics/dict.k:32-33` | `rule` | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 475 | `semantics/dict.k:37` | `syntax/function/total` | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 476 | `semantics/dict.k:38` | `rule` | `rule dHasKey(.ValSeq, _:Val) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 477 | `semantics/dict.k:39` | `rule` | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 478 | `semantics/dict.k:40` | `rule` | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 479 | `semantics/dict.k:43` | `syntax/function/total` | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 480 | `semantics/dict.k:44` | `rule` | `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 481 | `semantics/dict.k:45` | `rule` | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 482 | `semantics/dict.k:49` | `syntax/function/total` | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 483 | `semantics/dict.k:50-51` | `rule` | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 484 | `semantics/dict.k:52-53` | `rule` | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 485 | `semantics/dict.k:54` | `rule/owise` | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 486 | `semantics/dict.k:58-60` | `rule/priority` | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 487 | `semantics/dict.k:63` | `rule` | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 488 | `semantics/dict.k:64` | `syntax/function` | `syntax Val ::= applyIndexD(Val, Val) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 489 | `semantics/dict.k:65-66` | `rule/priority` | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 490 | `semantics/dict.k:70` | `syntax/function` | `syntax Val ::= dictSet(Val, Val, Val) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 491 | `semantics/dict.k:71` | `rule` | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 492 | `semantics/dict.k:76` | `syntax` | `syntax KItem ::= #dsetK(String, Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 493 | `semantics/dict.k:77` | `rule` | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 494 | `semantics/dict.k:78-81` | `rule` | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 495 | `semantics/dict.k:82-85` | `rule` | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 496 | `semantics/dict.k:86` | `syntax` | `syntax KItem ::= #dsetV(Val, Val, Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 497 | `semantics/dict.k:87-88` | `rule` | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 498 | `semantics/dict.k:90` | `syntax/function/total` | `syntax Int ::= normIdxD(Int, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 499 | `semantics/dict.k:91` | `rule` | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 500 | `semantics/dict.k:92` | `rule` | `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 501 | `semantics/dict.k:95-96` | `rule` | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 502 | `semantics/dict.k:97` | `syntax/function` | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 503 | `semantics/dict.k:98` | `rule` | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 504 | `semantics/dict.k:99-100` | `rule` | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 505 | `semantics/dict.k:101` | `syntax/function` | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 506 | `semantics/dict.k:102` | `rule` | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 507 | `semantics/dict.k:103` | `rule` | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 508 | `semantics/dict.k:104` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 509 | `semantics/float.k:14` | `module` | `module MPY-FLOAT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 510 | `semantics/float.k:15` | `imports` | `imports MPY-OPERATORS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 511 | `semantics/float.k:16` | `imports` | `imports MPY-BUILTINS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 512 | `semantics/float.k:17` | `imports` | `imports FLOAT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 513 | `semantics/float.k:20` | `syntax` | `syntax Val ::= Float` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 514 | `semantics/float.k:21` | `rule` | `rule <k> Float(F:Float) => F ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 515 | `semantics/float.k:24` | `syntax/function/total/opaque-symbol` | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 516 | `semantics/float.k:25` | `rule/concrete` | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 517 | `semantics/float.k:27` | `rule` | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 518 | `semantics/float.k:30` | `syntax/function/total/opaque-symbol` | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 519 | `semantics/float.k:31` | `rule/concrete` | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 520 | `semantics/float.k:32` | `rule` | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 521 | `semantics/float.k:37` | `syntax/function/total/opaque-symbol` | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 522 | `semantics/float.k:38` | `rule/concrete` | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 523 | `semantics/float.k:39` | `rule` | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 524 | `semantics/float.k:43` | `rule` | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 525 | `semantics/float.k:44` | `rule` | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 526 | `semantics/float.k:50` | `syntax/function/total/opaque-symbol` | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 527 | `semantics/float.k:51` | `rule/concrete` | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 528 | `semantics/float.k:52` | `rule` | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 529 | `semantics/float.k:54` | `syntax/function/total/opaque-symbol` | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 530 | `semantics/float.k:55` | `rule/concrete` | `rule absF(F:Float) => absFloat(F) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 531 | `semantics/float.k:56` | `rule` | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 532 | `semantics/float.k:61` | `rule` | `rule <k> Import(_:String) => .K ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 533 | `semantics/float.k:65` | `syntax` | `syntax KItem ::= "#mathCeil"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 534 | `semantics/float.k:66` | `rule/priority` | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 535 | `semantics/float.k:67` | `rule` | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 536 | `semantics/float.k:70` | `syntax` | `syntax KItem ::= "#mathFloor"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 537 | `semantics/float.k:71` | `rule/priority` | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 538 | `semantics/float.k:72` | `rule` | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 539 | `semantics/float.k:73` | `syntax/function/total/opaque-symbol` | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 540 | `semantics/float.k:74` | `rule/concrete` | `rule floorFI(I:Int) => I [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 541 | `semantics/float.k:75` | `rule/concrete` | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 542 | `semantics/float.k:78` | `rule` | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 543 | `semantics/float.k:79` | `rule` | `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 544 | `semantics/float.k:82` | `syntax` | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 545 | `semantics/float.k:83` | `rule/priority` | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 546 | `semantics/float.k:84` | `rule` | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 547 | `semantics/float.k:85` | `rule` | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 548 | `semantics/float.k:86` | `syntax/function/total/opaque-symbol` | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 549 | `semantics/float.k:87` | `rule/concrete` | `rule toF(F:Float) => F [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 550 | `semantics/float.k:88` | `rule/concrete` | `rule toF(I:Int) => intToF(I) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 551 | `semantics/float.k:93` | `syntax/function/total/opaque-symbol` | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 552 | `semantics/float.k:94` | `rule/concrete` | `rule ceilF(I:Int) => I [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 553 | `semantics/float.k:95` | `rule/concrete` | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 554 | `semantics/float.k:99` | `rule` | `rule applyUn("-", F:Float) => 0.0 -Float F` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 555 | `semantics/float.k:103` | `syntax/function/total/opaque-symbol` | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 556 | `semantics/float.k:104` | `rule/concrete` | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 557 | `semantics/float.k:105` | `rule` | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 558 | `semantics/float.k:107` | `syntax/function/total/opaque-symbol` | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 559 | `semantics/float.k:108` | `rule/concrete` | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 560 | `semantics/float.k:109` | `rule` | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 561 | `semantics/float.k:111` | `syntax/function/total/opaque-symbol` | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 562 | `semantics/float.k:112` | `rule/concrete` | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 563 | `semantics/float.k:113` | `rule` | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 564 | `semantics/float.k:115` | `syntax/function/total/opaque-symbol` | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 565 | `semantics/float.k:116` | `rule/concrete` | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 566 | `semantics/float.k:117` | `rule` | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 567 | `semantics/float.k:119` | `syntax/function/total/opaque-symbol` | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 568 | `semantics/float.k:120` | `rule/concrete` | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 569 | `semantics/float.k:121` | `rule` | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 570 | `semantics/float.k:125` | `syntax/function/total/opaque-symbol` | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 571 | `semantics/float.k:126` | `rule/concrete` | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 572 | `semantics/float.k:127` | `rule` | `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 573 | `semantics/float.k:128` | `rule` | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 574 | `semantics/float.k:129` | `rule` | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 575 | `semantics/float.k:132` | `rule` | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 576 | `semantics/float.k:133` | `rule` | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 577 | `semantics/float.k:134` | `rule` | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 578 | `semantics/float.k:135` | `rule` | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 579 | `semantics/float.k:136` | `rule` | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 580 | `semantics/float.k:137` | `rule` | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 581 | `semantics/float.k:138` | `rule` | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 582 | `semantics/float.k:139` | `rule` | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 583 | `semantics/float.k:142` | `syntax/function/total/opaque-symbol` | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 584 | `semantics/float.k:143` | `rule/concrete` | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 585 | `semantics/float.k:144` | `rule` | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 586 | `semantics/float.k:145` | `rule` | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 587 | `semantics/float.k:146` | `rule` | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 588 | `semantics/float.k:147` | `rule` | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 589 | `semantics/float.k:148` | `rule` | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 590 | `semantics/float.k:149` | `rule` | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 591 | `semantics/float.k:150` | `rule` | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 592 | `semantics/float.k:151` | `rule` | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 593 | `semantics/float.k:154` | `rule` | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 594 | `semantics/float.k:155` | `rule` | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 595 | `semantics/float.k:160` | `syntax/function/total/opaque-symbol` | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 596 | `semantics/float.k:161` | `rule/concrete` | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 597 | `semantics/float.k:162-164` | `rule/concrete` | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 598 | `semantics/float.k:165` | `syntax/function` | `syntax Int ::= headIS(IntSeq) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 599 | `semantics/float.k:166` | `rule` | `rule headIS(iCons(C:Int, _:IntSeq)) => C` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 600 | `semantics/float.k:167` | `syntax/function/total` | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 601 | `semantics/float.k:168` | `rule` | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 602 | `semantics/float.k:169` | `rule` | `rule intPartAcc(.IntSeq, A:Int) => A` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 603 | `semantics/float.k:170` | `rule` | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 604 | `semantics/float.k:171-172` | `rule` | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 605 | `semantics/float.k:173` | `syntax/function/total` | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 606 | `semantics/float.k:174` | `rule` | `rule fracPart(.IntSeq) => 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 607 | `semantics/float.k:175` | `rule` | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 608 | `semantics/float.k:176` | `rule` | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 609 | `semantics/float.k:177` | `rule` | `rule fracAcc(.IntSeq, A:Int) => A` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 610 | `semantics/float.k:178` | `rule` | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 611 | `semantics/float.k:179` | `syntax/function/total` | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 612 | `semantics/float.k:180` | `rule` | `rule fracScale(.IntSeq) => 1` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 613 | `semantics/float.k:181` | `rule` | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 614 | `semantics/float.k:182` | `rule` | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 615 | `semantics/float.k:183` | `rule` | `rule fscAcc(.IntSeq, A:Int) => A` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 616 | `semantics/float.k:184` | `rule` | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 617 | `semantics/float.k:185` | `rule` | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 618 | `semantics/float.k:186` | `rule` | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 619 | `semantics/float.k:187` | `rule` | `rule applyBuiltin("float", F:Float, .Vals) => F` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 620 | `semantics/float.k:190` | `syntax/function/total/opaque-symbol` | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 621 | `semantics/float.k:191` | `rule/concrete` | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 622 | `semantics/float.k:192` | `rule` | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 623 | `semantics/float.k:195` | `syntax/function/total/opaque-symbol` | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 624 | `semantics/float.k:196` | `rule/concrete` | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 625 | `semantics/float.k:197` | `rule` | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 626 | `semantics/float.k:198` | `rule` | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 627 | `semantics/float.k:199` | `rule` | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 628 | `semantics/float.k:200` | `rule` | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 629 | `semantics/float.k:201` | `rule` | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 630 | `semantics/float.k:202` | `rule` | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 631 | `semantics/float.k:203` | `rule` | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 632 | `semantics/float.k:204` | `rule` | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 633 | `semantics/float.k:205` | `rule` | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 634 | `semantics/float.k:206` | `rule` | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 635 | `semantics/float.k:209` | `syntax/function/total/opaque-symbol` | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 636 | `semantics/float.k:210` | `rule/concrete` | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 637 | `semantics/float.k:211` | `rule` | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 638 | `semantics/float.k:213` | `rule` | `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 639 | `semantics/float.k:214` | `rule` | `rule applyBuiltin("float", F:Float, .Vals) => F` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 640 | `semantics/float.k:217` | `syntax/function/total/opaque-symbol` | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 641 | `semantics/float.k:218-222` | `rule/concrete` | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 642 | `semantics/float.k:223` | `syntax/function/total/opaque-symbol` | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 643 | `semantics/float.k:224-226` | `rule/concrete` | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 644 | `semantics/float.k:227` | `rule` | `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 645 | `semantics/float.k:228` | `rule` | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 646 | `semantics/float.k:230` | `syntax/function/total/opaque-symbol` | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 647 | `semantics/float.k:231` | `rule/concrete` | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 648 | `semantics/float.k:232` | `syntax` | `syntax KItem ::= "#mathSqrt"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 649 | `semantics/float.k:233` | `rule/priority` | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 650 | `semantics/float.k:234` | `rule` | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 651 | `semantics/float.k:235` | `rule` | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 652 | `semantics/float.k:243` | `syntax` | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 653 | `semantics/float.k:244` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 654 | `semantics/float.k:245` | `rule` | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 655 | `semantics/float.k:246` | `rule` | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 656 | `semantics/float.k:247-248` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 657 | `semantics/float.k:250` | `syntax` | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 658 | `semantics/float.k:251` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 659 | `semantics/float.k:252` | `rule` | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 660 | `semantics/float.k:253` | `rule` | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 661 | `semantics/float.k:254-255` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 662 | `semantics/float.k:261` | `syntax` | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 663 | `semantics/float.k:262-264` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 664 | `semantics/float.k:265` | `rule` | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 665 | `semantics/float.k:266` | `rule` | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 666 | `semantics/float.k:267-269` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 667 | `semantics/float.k:270-272` | `rule` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 668 | `semantics/float.k:273` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 669 | `semantics/functions.k:3` | `module` | `module MPY-FUNCTIONS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 670 | `semantics/functions.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 671 | `semantics/functions.k:8-11` | `syntax` | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 672 | `semantics/functions.k:14-16` | `rule` | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 673 | `semantics/functions.k:18` | `syntax` | `syntax Expr ::= closureExpr(ParamNames, Stmts)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 674 | `semantics/functions.k:19-20` | `rule` | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 675 | `semantics/functions.k:27` | `syntax` | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 676 | `semantics/functions.k:31-32` | `syntax` | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 677 | `semantics/functions.k:33-35` | `rule` | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 678 | `semantics/functions.k:36-41` | `rule` | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 679 | `semantics/functions.k:42-45` | `rule` | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 680 | `semantics/functions.k:47-49` | `rule` | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 681 | `semantics/functions.k:50-52` | `rule` | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 682 | `semantics/functions.k:53-58` | `rule` | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 683 | `semantics/functions.k:59-60` | `rule` | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 684 | `semantics/functions.k:63` | `rule` | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 685 | `semantics/functions.k:64-66` | `rule` | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 686 | `semantics/functions.k:68-75` | `rule/priority` | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 687 | `semantics/functions.k:78-79` | `rule` | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 688 | `semantics/functions.k:80-81` | `rule` | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 689 | `semantics/functions.k:85-90` | `rule` | `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 690 | `semantics/functions.k:91` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 691 | `semantics/int.k:4` | `module` | `module MPY-INT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 692 | `semantics/int.k:5` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 693 | `semantics/int.k:7` | `rule` | `rule applyUn("-", I:Int) => 0 -Int I` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 694 | `semantics/int.k:9` | `rule` | `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 695 | `semantics/int.k:11` | `rule` | `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 696 | `semantics/int.k:12` | `rule` | `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 697 | `semantics/int.k:13` | `rule` | `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 698 | `semantics/int.k:14` | `rule` | `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 699 | `semantics/int.k:15` | `rule` | `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 700 | `semantics/int.k:16` | `rule` | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 701 | `semantics/int.k:17` | `rule` | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 702 | `semantics/int.k:19` | `syntax/function` | `syntax Int ::= pyMod(Int, Int) [function]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 703 | `semantics/int.k:20` | `rule` | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 704 | `semantics/int.k:22` | `rule` | `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 705 | `semantics/int.k:23` | `rule` | `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 706 | `semantics/int.k:24` | `rule` | `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 707 | `semantics/int.k:25` | `rule` | `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 708 | `semantics/int.k:26` | `rule` | `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 709 | `semantics/int.k:27` | `rule` | `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 710 | `semantics/int.k:28` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 711 | `semantics/iter.k:6` | `module` | `module MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 712 | `semantics/iter.k:7` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 713 | `semantics/iter.k:8` | `syntax` | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 714 | `semantics/iter.k:9` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 715 | `semantics/list.k:3` | `module` | `module MPY-LIST` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 716 | `semantics/list.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 717 | `semantics/list.k:5` | `imports` | `imports MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 718 | `semantics/list.k:6` | `imports` | `imports MPY-OPERATORS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 719 | `semantics/list.k:9` | `rule` | `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 720 | `semantics/list.k:10` | `rule` | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 721 | `semantics/list.k:13` | `syntax` | `syntax ApplyK ::= "toList"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 722 | `semantics/list.k:14` | `rule` | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 723 | `semantics/list.k:15` | `rule` | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 724 | `semantics/list.k:18` | `syntax/function/total` | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 725 | `semantics/list.k:19` | `rule` | `rule valSeqConcat(.ValSeq, T:ValSeq) => T` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 726 | `semantics/list.k:20` | `rule` | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 727 | `semantics/list.k:24-25` | `rule/priority` | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 728 | `semantics/list.k:27` | `rule` | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 729 | `semantics/list.k:28` | `rule` | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 730 | `semantics/list.k:33` | `syntax/function/total` | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 731 | `semantics/list.k:34` | `rule` | `rule hasRefVS(.ValSeq) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 732 | `semantics/list.k:35` | `rule` | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 733 | `semantics/list.k:37-38` | `syntax/function` | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 734 | `semantics/list.k:39` | `rule` | `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 735 | `semantics/list.k:40` | `rule` | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 736 | `semantics/list.k:41` | `rule` | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 737 | `semantics/list.k:42-43` | `rule` | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 738 | `semantics/list.k:45-46` | `rule` | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 739 | `semantics/list.k:47-48` | `rule` | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 740 | `semantics/list.k:49` | `rule` | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 741 | `semantics/list.k:50` | `rule/owise` | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 742 | `semantics/list.k:53-55` | `rule/priority` | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 743 | `semantics/list.k:58` | `syntax` | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 744 | `semantics/list.k:59` | `rule` | `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 745 | `semantics/list.k:60` | `rule` | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 746 | `semantics/list.k:61` | `rule` | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 747 | `semantics/list.k:62` | `rule` | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 748 | `semantics/list.k:63-64` | `rule` | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 749 | `semantics/list.k:65-66` | `rule` | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 750 | `semantics/list.k:67` | `rule` | `rule <k> B:Bool ~> #notB => notBool B ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 751 | `semantics/list.k:68` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 752 | `semantics/methods.k:3` | `module` | `module MPY-METHODS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 753 | `semantics/methods.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 754 | `semantics/methods.k:5` | `imports` | `imports K-EQUAL` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 755 | `semantics/methods.k:6` | `imports` | `imports MPY-STR` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 756 | `semantics/methods.k:7` | `imports` | `imports MPY-LIST` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 757 | `semantics/methods.k:10` | `syntax/function` | `syntax Val ::= applyMethod(Val, String, Vals) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 758 | `semantics/methods.k:13` | `rule` | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 759 | `semantics/methods.k:14` | `rule` | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 760 | `semantics/methods.k:15` | `rule` | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 761 | `semantics/methods.k:16` | `rule` | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 762 | `semantics/methods.k:19` | `rule` | `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 763 | `semantics/methods.k:20` | `rule` | `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 764 | `semantics/methods.k:21` | `rule` | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 765 | `semantics/methods.k:26` | `rule` | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 766 | `semantics/methods.k:27` | `syntax/function/total` | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 767 | `semantics/methods.k:28` | `rule` | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 768 | `semantics/methods.k:29` | `rule` | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 769 | `semantics/methods.k:30-31` | `rule` | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 770 | `semantics/methods.k:34` | `rule` | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 771 | `semantics/methods.k:35` | `syntax/function` | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 772 | `semantics/methods.k:36` | `rule` | `rule cntSub(.IntSeq, _:IntSeq) => 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 773 | `semantics/methods.k:37-38` | `rule` | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 774 | `semantics/methods.k:39-40` | `rule` | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 775 | `semantics/methods.k:41` | `syntax/function/total` | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 776 | `semantics/methods.k:42` | `rule` | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 777 | `semantics/methods.k:43` | `rule/owise` | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 778 | `semantics/methods.k:44` | `rule` | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 779 | `semantics/methods.k:47` | `rule` | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 780 | `semantics/methods.k:48` | `syntax/function/total` | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 781 | `semantics/methods.k:49` | `rule` | `rule trimWS(.IntSeq) => .IntSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 782 | `semantics/methods.k:50` | `rule` | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 783 | `semantics/methods.k:51` | `rule` | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 784 | `semantics/methods.k:52` | `syntax/function/total` | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 785 | `semantics/methods.k:53` | `rule` | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 786 | `semantics/methods.k:54` | `rule` | `rule revISAcc(.IntSeq, A:IntSeq) => A` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 787 | `semantics/methods.k:55` | `rule` | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 788 | `semantics/methods.k:58` | `rule` | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 789 | `semantics/methods.k:61` | `rule` | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 790 | `semantics/methods.k:64` | `rule` | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 791 | `semantics/methods.k:65` | `syntax/function/total` | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 792 | `semantics/methods.k:66` | `rule` | `rule cntOccVS(.ValSeq, _:Val) => 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 793 | `semantics/methods.k:67` | `rule` | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 794 | `semantics/methods.k:68` | `rule` | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 795 | `semantics/methods.k:72-74` | `rule/priority` | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 796 | `semantics/methods.k:75` | `syntax/function` | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] // remaining, current token, result` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 797 | `semantics/methods.k:76` | `rule` | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 798 | `semantics/methods.k:77-78` | `rule` | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 799 | `semantics/methods.k:79-80` | `rule` | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 800 | `semantics/methods.k:82` | `syntax/function` | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 801 | `semantics/methods.k:83` | `rule` | `rule flushTok(ACC:ValSeq, .IntSeq) => ACC` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 802 | `semantics/methods.k:84` | `rule` | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 803 | `semantics/methods.k:85` | `syntax/function/total` | `syntax Bool ::= isWSC(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 804 | `semantics/methods.k:86` | `rule` | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 805 | `semantics/methods.k:89-91` | `rule/priority` | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 806 | `semantics/methods.k:94-96` | `rule/priority` | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 807 | `semantics/methods.k:97` | `syntax/function` | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] // remaining, sep code, current token` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 808 | `semantics/methods.k:98` | `rule` | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 809 | `semantics/methods.k:99-100` | `rule` | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 810 | `semantics/methods.k:101-102` | `rule` | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 811 | `semantics/methods.k:104-105` | `rule` | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 812 | `semantics/methods.k:106` | `syntax/function/total` | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 813 | `semantics/methods.k:107` | `rule` | `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 814 | `semantics/methods.k:108` | `rule` | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 815 | `semantics/methods.k:109` | `rule` | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 816 | `semantics/methods.k:112` | `syntax/function/total` | `syntax Bool ::= isUpperC(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 817 | `semantics/methods.k:113` | `rule` | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 818 | `semantics/methods.k:115` | `syntax/function/total` | `syntax Bool ::= isLowerC(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 819 | `semantics/methods.k:116` | `rule` | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 820 | `semantics/methods.k:118` | `syntax/function/total` | `syntax Bool ::= isAlphaC(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 821 | `semantics/methods.k:119` | `rule` | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 822 | `semantics/methods.k:121` | `syntax/function/total` | `syntax Bool ::= isDigitC(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 823 | `semantics/methods.k:122` | `rule` | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 824 | `semantics/methods.k:124` | `syntax/function/total` | `syntax Bool ::= hasUpper(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 825 | `semantics/methods.k:125` | `rule` | `rule hasUpper(.IntSeq) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 826 | `semantics/methods.k:126` | `rule` | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 827 | `semantics/methods.k:128` | `syntax/function/total` | `syntax Bool ::= hasLower(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 828 | `semantics/methods.k:129` | `rule` | `rule hasLower(.IntSeq) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 829 | `semantics/methods.k:130` | `rule` | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 830 | `semantics/methods.k:132` | `syntax/function/total` | `syntax Bool ::= allAlpha(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 831 | `semantics/methods.k:133` | `rule` | `rule allAlpha(.IntSeq) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 832 | `semantics/methods.k:134` | `rule` | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 833 | `semantics/methods.k:136` | `syntax/function/total` | `syntax Bool ::= allDigit(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 834 | `semantics/methods.k:137` | `rule` | `rule allDigit(.IntSeq) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 835 | `semantics/methods.k:138` | `rule` | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 836 | `semantics/methods.k:140` | `syntax/function/total` | `syntax Int ::= lowerC(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 837 | `semantics/methods.k:142` | `rule` | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 838 | `semantics/methods.k:143` | `rule/owise` | `rule lowerC(C:Int) => C [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 839 | `semantics/methods.k:145` | `syntax/function/total` | `syntax Int ::= upperC(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 840 | `semantics/methods.k:146` | `rule` | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 841 | `semantics/methods.k:147` | `rule/owise` | `rule upperC(C:Int) => C [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 842 | `semantics/methods.k:149` | `syntax/function/total` | `syntax Int ::= swapC(Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 843 | `semantics/methods.k:150` | `rule` | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 844 | `semantics/methods.k:151` | `rule` | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 845 | `semantics/methods.k:152` | `rule/owise` | `rule swapC(C:Int) => C [owise]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 846 | `semantics/methods.k:154` | `syntax/function/total` | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 847 | `semantics/methods.k:155` | `rule` | `rule mapLower(.IntSeq) => .IntSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 848 | `semantics/methods.k:156` | `rule` | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 849 | `semantics/methods.k:158` | `syntax/function/total` | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 850 | `semantics/methods.k:159` | `rule` | `rule mapUpper(.IntSeq) => .IntSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 851 | `semantics/methods.k:160` | `rule` | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 852 | `semantics/methods.k:162` | `syntax/function/total` | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 853 | `semantics/methods.k:163` | `rule` | `rule mapSwap(.IntSeq) => .IntSeq` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 854 | `semantics/methods.k:164` | `rule` | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 855 | `semantics/methods.k:166` | `syntax/function/total` | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 856 | `semantics/methods.k:167` | `rule` | `rule startsWith(.IntSeq, _:IntSeq) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 857 | `semantics/methods.k:168` | `rule` | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 858 | `semantics/methods.k:169` | `rule` | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 859 | `semantics/methods.k:170` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 860 | `semantics/operators.k:6` | `module` | `module MPY-OPERATORS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 861 | `semantics/operators.k:7` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 862 | `semantics/operators.k:8` | `imports` | `imports MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 863 | `semantics/operators.k:10` | `rule` | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 864 | `semantics/operators.k:12` | `rule` | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 865 | `semantics/operators.k:15` | `context` | `context Compare(HOLE, _)` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 866 | `semantics/operators.k:16` | `context` | `context Compare(_:Val, CmpOp(_, HOLE))` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 867 | `semantics/operators.k:17` | `rule/owise` | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 868 | `semantics/operators.k:19` | `rule` | `rule applyCmp("is", V:Val, noneV) => V ==K noneV` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 869 | `semantics/operators.k:20` | `rule` | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 870 | `semantics/operators.k:25-27` | `rule/priority` | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 871 | `semantics/operators.k:28-31` | `rule/priority` | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 872 | `semantics/operators.k:34-37` | `rule/priority` | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 873 | `semantics/operators.k:38-42` | `rule/priority` | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 874 | `semantics/operators.k:44-46` | `rule/priority` | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 875 | `semantics/operators.k:47` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 876 | `semantics/range.k:5` | `module` | `module MPY-RANGE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 877 | `semantics/range.k:6` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 878 | `semantics/range.k:7` | `imports` | `imports MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 879 | `semantics/range.k:9` | `syntax/function/total` | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 880 | `semantics/range.k:10` | `rule` | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 881 | `semantics/range.k:12` | `syntax/function` | `syntax Int ::= rangeLen(Int, Int, Int) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 882 | `semantics/range.k:13-14` | `rule` | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 883 | `semantics/range.k:15-16` | `rule` | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 884 | `semantics/range.k:17-18` | `rule` | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 885 | `semantics/range.k:20-22` | `rule` | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 886 | `semantics/range.k:23-24` | `rule` | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 887 | `semantics/range.k:25` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 888 | `semantics/set.k:3` | `module` | `module MPY-SET` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 889 | `semantics/set.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 890 | `semantics/set.k:8` | `syntax` | `syntax Val ::= setV(IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 891 | `semantics/set.k:11` | `syntax/function/total` | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 892 | `semantics/set.k:12` | `rule` | `rule codeIn(_:Int, .IntSeq) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 893 | `semantics/set.k:13` | `rule` | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 894 | `semantics/set.k:16-17` | `syntax/function/total` | `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] \| dedupFrom(IntSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 895 | `semantics/set.k:18` | `rule` | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 896 | `semantics/set.k:19` | `rule` | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 897 | `semantics/set.k:20-21` | `rule` | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 898 | `semantics/set.k:22-23` | `rule` | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 899 | `semantics/set.k:25` | `syntax/function/total` | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 900 | `semantics/set.k:26` | `rule` | `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 901 | `semantics/set.k:27` | `rule` | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 902 | `semantics/set.k:31` | `syntax/function/total` | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 903 | `semantics/set.k:32` | `rule` | `rule subsetCodes(.IntSeq, _:IntSeq) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 904 | `semantics/set.k:33` | `rule` | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 905 | `semantics/set.k:35` | `syntax/function/total` | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 906 | `semantics/set.k:36` | `rule` | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 907 | `semantics/set.k:39` | `rule` | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 908 | `semantics/set.k:40` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 909 | `semantics/sort.k:10` | `module` | `module MPY-SORT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 910 | `semantics/sort.k:11` | `imports` | `imports MPY-BUILTINS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 911 | `semantics/sort.k:12` | `imports` | `imports MPY-SUBSCRIPT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 912 | `semantics/sort.k:18` | `syntax/function/total/opaque-symbol` | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 913 | `semantics/sort.k:19` | `syntax/function` | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 914 | `semantics/sort.k:20` | `rule/concrete` | `rule sortVS(.ValSeq) => .ValSeq [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 915 | `semantics/sort.k:21` | `rule/concrete` | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 916 | `semantics/sort.k:22` | `rule/concrete` | `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 917 | `semantics/sort.k:23` | `rule/concrete` | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 918 | `semantics/sort.k:24` | `rule/concrete` | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 919 | `semantics/sort.k:26` | `syntax/function` | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 920 | `semantics/sort.k:27` | `rule/concrete` | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 921 | `semantics/sort.k:28` | `rule/concrete` | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 922 | `semantics/sort.k:29-30` | `rule/concrete` | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 923 | `semantics/sort.k:31-32` | `rule/concrete` | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 924 | `semantics/sort.k:36-37` | `rule` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 925 | `semantics/sort.k:40-42` | `rule/priority` | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 926 | `semantics/sort.k:49` | `syntax/function/total/opaque-symbol` | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` | FIXED SUPPLIED opaque boundary; unreachable on target path |
| 927 | `semantics/sort.k:51-52` | `syntax/function/total` | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 928 | `semantics/sort.k:53` | `rule` | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 929 | `semantics/sort.k:54` | `rule` | `rule revVSAcc(.ValSeq, A:ValSeq) => A` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 930 | `semantics/sort.k:55` | `rule` | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 931 | `semantics/sort.k:57` | `syntax/function/total` | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 932 | `semantics/sort.k:58` | `rule` | `rule condRev(S:ValSeq, false) => S` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 933 | `semantics/sort.k:59` | `rule` | `rule condRev(S:ValSeq, true) => revVS(S)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 934 | `semantics/sort.k:61-62` | `rule` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 935 | `semantics/sort.k:63-64` | `rule` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 936 | `semantics/sort.k:65-66` | `rule` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 937 | `semantics/sort.k:72` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 938 | `semantics/str.k:3` | `module` | `module MPY-STR` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 939 | `semantics/str.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 940 | `semantics/str.k:5` | `imports` | `imports MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 941 | `semantics/str.k:8` | `rule` | `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 942 | `semantics/str.k:9-10` | `rule` | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 943 | `semantics/str.k:13` | `syntax/function` | `syntax IntSeq ::= strToCodes(String) [function]` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 944 | `semantics/str.k:14` | `rule` | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 945 | `semantics/str.k:15` | `rule` | `rule strToCodes("") => .IntSeq` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 946 | `semantics/str.k:16-17` | `rule` | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 947 | `semantics/str.k:20` | `syntax/function/total` | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 948 | `semantics/str.k:21` | `rule` | `rule seqConcat(.IntSeq, T:IntSeq) => T` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 949 | `semantics/str.k:22` | `rule` | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 950 | `semantics/str.k:24` | `rule` | `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 951 | `semantics/str.k:25` | `rule` | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 952 | `semantics/str.k:26` | `rule` | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 953 | `semantics/str.k:29` | `rule` | `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 954 | `semantics/str.k:30` | `rule` | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 955 | `semantics/str.k:32` | `syntax/function/total` | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 956 | `semantics/str.k:33` | `rule` | `rule strPrefix(.IntSeq, _:IntSeq) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 957 | `semantics/str.k:34` | `rule` | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 958 | `semantics/str.k:35` | `rule` | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 959 | `semantics/str.k:37` | `syntax/function/total` | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 960 | `semantics/str.k:38` | `rule` | `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 961 | `semantics/str.k:39` | `rule` | `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 962 | `semantics/str.k:40-41` | `rule` | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 963 | `semantics/str.k:48` | `syntax/function/total` | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 964 | `semantics/str.k:49` | `rule` | `rule strLt(.IntSeq, .IntSeq) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 965 | `semantics/str.k:50` | `rule` | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 966 | `semantics/str.k:51` | `rule` | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 967 | `semantics/str.k:52` | `rule` | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 968 | `semantics/str.k:53` | `rule` | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 969 | `semantics/str.k:54` | `rule` | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 970 | `semantics/str.k:56` | `rule` | `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 971 | `semantics/str.k:57` | `rule` | `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 972 | `semantics/str.k:58` | `rule` | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 973 | `semantics/str.k:59` | `rule` | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 974 | `semantics/str.k:60` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 975 | `semantics/subscript.k:3` | `module` | `module MPY-SUBSCRIPT` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 976 | `semantics/subscript.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 977 | `semantics/subscript.k:11` | `syntax/function/total` | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 978 | `semantics/subscript.k:12` | `rule` | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 979 | `semantics/subscript.k:13-14` | `rule` | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 980 | `semantics/subscript.k:16` | `syntax/function` | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 981 | `semantics/subscript.k:17` | `rule` | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 982 | `semantics/subscript.k:18-19` | `rule` | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 983 | `semantics/subscript.k:21` | `syntax/function/total` | `syntax Int ::= normIdx(Int, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 984 | `semantics/subscript.k:22` | `rule` | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 985 | `semantics/subscript.k:23` | `rule` | `rule normIdx(I:Int, _:Int) => I requires I >=Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 986 | `semantics/subscript.k:27` | `context` | `context Subscript(HOLE, _)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 987 | `semantics/subscript.k:28` | `context` | `context Subscript(_:Val, HOLE:Expr)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 988 | `semantics/subscript.k:31-33` | `rule/priority` | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 989 | `semantics/subscript.k:35` | `rule` | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 990 | `semantics/subscript.k:37` | `syntax/function` | `syntax Val ::= applyIndex(Val, Int) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 991 | `semantics/subscript.k:38` | `rule` | `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 992 | `semantics/subscript.k:39` | `rule` | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 993 | `semantics/subscript.k:40-41` | `rule` | `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 994 | `semantics/subscript.k:44-47` | `syntax` | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 995 | `semantics/subscript.k:49` | `syntax` | `syntax OptInt ::= "noB" \| someB(Int)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 996 | `semantics/subscript.k:50` | `rule` | `rule <k> #evalB(NoBound) => noB ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 997 | `semantics/subscript.k:51` | `rule` | `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 998 | `semantics/subscript.k:52` | `rule` | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 999 | `semantics/subscript.k:54` | `rule` | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1000 | `semantics/subscript.k:55` | `rule` | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1001 | `semantics/subscript.k:56` | `rule` | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1002 | `semantics/subscript.k:58-60` | `rule/priority` | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1003 | `semantics/subscript.k:61` | `rule` | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1004 | `semantics/subscript.k:63` | `syntax/function` | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1005 | `semantics/subscript.k:64-65` | `rule` | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1006 | `semantics/subscript.k:66-67` | `rule` | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1007 | `semantics/subscript.k:68-69` | `rule` | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1008 | `semantics/subscript.k:72` | `syntax/function/total` | `syntax Int ::= slStep(OptInt) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1009 | `semantics/subscript.k:73` | `rule` | `rule slStep(noB) => 1` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1010 | `semantics/subscript.k:74` | `rule` | `rule slStep(someB(S:Int)) => S` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1011 | `semantics/subscript.k:76` | `syntax/function` | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1012 | `semantics/subscript.k:77-78` | `rule` | `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1013 | `semantics/subscript.k:79-80` | `rule` | `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1014 | `semantics/subscript.k:81` | `rule` | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1015 | `semantics/subscript.k:83` | `syntax/function` | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1016 | `semantics/subscript.k:84-85` | `rule` | `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1017 | `semantics/subscript.k:86-87` | `rule` | `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1018 | `semantics/subscript.k:88` | `rule` | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1019 | `semantics/subscript.k:90` | `syntax/function/total` | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1020 | `semantics/subscript.k:91-92` | `rule` | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1021 | `semantics/subscript.k:93-94` | `rule` | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1022 | `semantics/subscript.k:96` | `syntax/function/total` | `syntax Int ::= clampLo(Int, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1023 | `semantics/subscript.k:97-98` | `rule` | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1024 | `semantics/subscript.k:99-100` | `rule` | `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1025 | `semantics/subscript.k:102` | `syntax/function/total` | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1026 | `semantics/subscript.k:103-104` | `rule` | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1027 | `semantics/subscript.k:105-106` | `rule` | `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1028 | `semantics/subscript.k:109` | `syntax/function` | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1029 | `semantics/subscript.k:110-112` | `rule` | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1030 | `semantics/subscript.k:113-114` | `rule` | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1031 | `semantics/subscript.k:116` | `syntax/function` | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1032 | `semantics/subscript.k:117-119` | `rule` | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1033 | `semantics/subscript.k:120-121` | `rule` | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1034 | `semantics/subscript.k:122` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1035 | `semantics/syntax.k:3` | `module` | `module MPY-SYNTAX` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1036 | `semantics/syntax.k:4` | `imports` | `imports INT-SYNTAX` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1037 | `semantics/syntax.k:5` | `imports` | `imports FLOAT-SYNTAX` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1038 | `semantics/syntax.k:6` | `imports` | `imports BOOL-SYNTAX` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1039 | `semantics/syntax.k:7` | `imports` | `imports STRING-SYNTAX` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1040 | `semantics/syntax.k:9-30` | `syntax/macro` | `syntax Expr ::= "Int" "(" Int ")" \| "Float" "(" Float ")" \| "Bool" "(" Bool ")" \| "Name" "(" String ")" \| "Str" "(" String ")" \| "UnaryOp" "(" String "," Expr ")" [strict(2)] \| "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp" "(" String "," Exprs ")" \| "ListExpr" "(" Exprs ")" \| "DictExpr" "(" Entries ")" \| "ListComp" "(" Expr "," CompFors ")" [macro] \| "GenExp" "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda" "(" Params "," Expr ")" \| "KwArg" "(" String "," Expr ")" \| "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call" "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare" "(" Expr "," CmpOp ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1041 | `semantics/syntax.k:32` | `syntax` | `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1042 | `semantics/syntax.k:33` | `syntax` | `syntax Entry ::= "Entry" "(" Expr "," Expr ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1043 | `semantics/syntax.k:34` | `syntax` | `syntax Entries ::= List{Entry, ","}` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1044 | `semantics/syntax.k:35` | `syntax` | `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1045 | `semantics/syntax.k:36` | `syntax` | `syntax CompFors ::= List{CompFor, ""}` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1046 | `semantics/syntax.k:37` | `syntax` | `syntax Exprs ::= List{Expr, ","}` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1047 | `semantics/syntax.k:38` | `syntax` | `syntax Index ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1048 | `semantics/syntax.k:39` | `syntax` | `syntax Bound ::= Expr \| "NoBound"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1049 | `semantics/syntax.k:41-54` | `syntax` | `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] \| "Import" "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While" "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return" "(" Expr ")" [strict] \| "Assert" "(" Expr ")" [strict] \| "Expr" "(" Expr ")" [strict] \| "FuncDef" "(" String "," Params "," Stmts ")" \| "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1050 | `semantics/syntax.k:56` | `syntax` | `syntax Stmts ::= List{Stmt, ""}` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1051 | `semantics/syntax.k:57` | `syntax` | `syntax Params ::= "Params" "(" ParamNames ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1052 | `semantics/syntax.k:58` | `syntax` | `syntax CellVars ::= "CellVars" "(" ParamNames ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1053 | `semantics/syntax.k:59` | `syntax` | `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1054 | `semantics/syntax.k:60` | `syntax` | `syntax ParamNames ::= List{String, ","}` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1055 | `semantics/syntax.k:61` | `syntax` | `syntax Module ::= "Module" "(" Stmts ")"` | FIXED SUPPLIED, target-path rule/declaration; reviewed in detail |
| 1056 | `semantics/syntax.k:62` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1057 | `semantics/tuple.k:3` | `module` | `module MPY-TUPLE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1058 | `semantics/tuple.k:4` | `imports` | `imports MPY-CORE` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1059 | `semantics/tuple.k:5` | `imports` | `imports MPY-ITER` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1060 | `semantics/tuple.k:6` | `imports` | `imports MPY-LIST` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1061 | `semantics/tuple.k:7` | `imports` | `imports MPY-METHODS` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1062 | `semantics/tuple.k:10` | `rule` | `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1063 | `semantics/tuple.k:11` | `rule` | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1064 | `semantics/tuple.k:14` | `syntax` | `syntax ApplyK ::= "toTuple"` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1065 | `semantics/tuple.k:15` | `rule` | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1066 | `semantics/tuple.k:16` | `rule` | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1067 | `semantics/tuple.k:18` | `rule` | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1068 | `semantics/tuple.k:20` | `rule` | `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1069 | `semantics/tuple.k:21` | `rule` | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1070 | `semantics/tuple.k:23` | `rule` | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1071 | `semantics/tuple.k:24` | `syntax/function` | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1072 | `semantics/tuple.k:25` | `rule` | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1073 | `semantics/tuple.k:26-27` | `rule` | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1074 | `semantics/tuple.k:28` | `rule` | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1075 | `semantics/tuple.k:31` | `syntax` | `syntax KItem ::= #bindTgt(Expr, Val)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1076 | `semantics/tuple.k:32-34` | `rule` | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1077 | `semantics/tuple.k:35-41` | `rule/priority` | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1078 | `semantics/tuple.k:42` | `rule` | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1079 | `semantics/tuple.k:43` | `rule` | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1080 | `semantics/tuple.k:44-46` | `rule/priority` | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1081 | `semantics/tuple.k:49` | `syntax` | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1082 | `semantics/tuple.k:50` | `rule` | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1083 | `semantics/tuple.k:51` | `rule` | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1084 | `semantics/tuple.k:52-54` | `rule/priority` | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1085 | `semantics/tuple.k:55-56` | `rule` | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1086 | `semantics/tuple.k:57` | `rule` | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1087 | `semantics/tuple.k:58` | `endmodule` | `endmodule` | FIXED SUPPLIED, unchanged and unreachable on target path |
| 1088 | `verification.k:1` | `requires` | `requires "reference-semantics/semantics.k"` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1089 | `verification.k:3` | `module` | `module VERIFICATION` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1090 | `verification.k:4` | `imports` | `imports MPY` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1091 | `verification.k:8` | `syntax/function` | `syntax Stmts ::= largestDivisorBody() [function]` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1092 | `verification.k:9-17` | `rule` | `rule largestDivisorBody() => Expr(Str("Return the largest positive divisor of n that is smaller than n.")) Assign(Name("divisor"), BinOp("-", Name("n"), Int(1))) While( Compare( BinOp("%", Name("n"), Name("divisor")), CmpOp("!=", Int(0))), AugAssign(Name("divisor"), "-", Int(1))) Return(Name("divisor"))` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1093 | `verification.k:22-23` | `syntax/function` | `syntax Int ::= largestProperDivisor(Int) [function] \| firstDivisorAtOrBelow(Int, Int) [function]` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1094 | `verification.k:25-26` | `rule` | `rule largestProperDivisor(N:Int) => firstDivisorAtOrBelow(N, N -Int 1)` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1095 | `verification.k:28-29` | `rule` | `rule firstDivisorAtOrBelow(N:Int, D:Int) => D requires D >Int 0 andBool pyMod(N, D) ==Int 0` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1096 | `verification.k:31-33` | `rule` | `rule firstDivisorAtOrBelow(N:Int, D:Int) => firstDivisorAtOrBelow(N, D -Int 1) requires D >Int 1 andBool pyMod(N, D) =/=Int 0` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1097 | `verification.k:38-41` | `rule/simplification` | `rule (1 \|-> _S:Scope SC:Map) [1 <- undef] => SC requires notBool 1 in_keys(SC) [simplification, label(deleteFreshFrame)]` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1098 | `verification.k:42` | `endmodule` | `endmodule` | PROOF-LOCAL: individually reviewed in REVIEW.md |
| 1099 | `spec.k:1` | `requires` | `requires "verification.k"` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1100 | `spec.k:3` | `module` | `module LOOP-SPEC` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1101 | `spec.k:4` | `imports` | `imports VERIFICATION` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1102 | `spec.k:9-38` | `claim` | `claim <k> #while( Compare( BinOp("%", Name("n"), Name("divisor")), CmpOp("!=", Int(0))), AugAssign(Name("divisor"), "-", Int(1))) ~> Return(Name("divisor")) .Stmts ~> #endcall => firstDivisorAtOrBelow(N, D) ~> .K </k> <env> 1 => 0 </env> <scopes> SC:Map 1 \|-> scope( "n" \|-> N "divisor" \|-> D, parent(0)) => SC </scopes> <scopeLoc> 2 => 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> ListItem(frame(.K, 0, 1)) => .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires N >Int 1 andBool D >=Int 1 andBool D <Int N [label(loopCorrect)]` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1103 | `spec.k:39` | `endmodule` | `endmodule` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1104 | `spec.k:41` | `module` | `module INIT-SPEC` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1105 | `spec.k:42` | `imports` | `imports VERIFICATION` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1106 | `spec.k:44-82` | `claim` | `claim <k> Assign(Name("divisor"), BinOp("-", Name("n"), Int(1))) While( Compare( BinOp("%", Name("n"), Name("divisor")), CmpOp("!=", Int(0))), AugAssign(Name("divisor"), "-", Int(1))) Return(Name("divisor")) ~> #endcall => #while( Compare( BinOp("%", Name("n"), Name("divisor")), CmpOp("!=", Int(0))), AugAssign(Name("divisor"), "-", Int(1))) ~> Return(Name("divisor")) .Stmts ~> #endcall </k> <env> 1 </env> <scopes> SC:Map 1 \|-> scope("n" \|-> N, parent(0)) => SC 1 \|-> scope( "n" \|-> N "divisor" \|-> ?D:Int, parent(0)) </scopes> <scopeLoc> 2 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> ListItem(frame(.K, 0, 1)) </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> ensures ?D ==Int N -Int 1 [label(initCorrect)]` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1107 | `spec.k:83` | `endmodule` | `endmodule` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1108 | `spec.k:85` | `module` | `module PREFIX-SPEC` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1109 | `spec.k:86` | `imports` | `imports VERIFICATION` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1110 | `spec.k:92-135` | `claim` | `claim <k> #loadAll( Module( FuncDef( "largest_divisor", Params("n"), largestDivisorBody()))) ~> Call(Name("largest_divisor"), Int(N)) => #while( Compare( BinOp("%", Name("n"), Name("divisor")), CmpOp("!=", Int(0))), AugAssign(Name("divisor"), "-", Int(1))) ~> Return(Name("divisor")) .Stmts ~> #endcall ~> .K </k> <env> 0 => 1 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope => 0 \|-> scope( "largest_divisor" \|-> closureVal("n", largestDivisorBody(), 0), parent(-1)) -1 \|-> builtinsScope 1 \|-> scope( "n" \|-> N "divisor" \|-> ?D:Int, parent(0)) </scopes> <scopeLoc> 1 => 2 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List => ListItem(frame(.K, 0, 1)) </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires N >Int 1 ensures ?D ==Int N -Int 1 [label(prefixCorrect)]` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |
| 1111 | `spec.k:136` | `endmodule` | `endmodule` | TARGET CLAIM: adequacy/composition reviewed in REVIEW.md |

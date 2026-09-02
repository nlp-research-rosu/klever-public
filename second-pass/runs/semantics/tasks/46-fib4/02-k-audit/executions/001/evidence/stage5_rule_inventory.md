# Exhaustive local K inventory

Scope: the trusted supplied-semantics scratch copy plus candidate `verification.k` and `spec.k`.
Imported K standard-library modules are outside this local-source inventory.

## Totals

| kind | count |
|---|---:|
| claim | 2 |
| configuration | 1 |
| context | 5 |
| endmodule | 27 |
| imports | 88 |
| module | 27 |
| rule | 695 |
| syntax | 227 |

## Attribute/classifier totals

| attribute/classifier | count |
|---|---:|
| function | 145 |
| no-evaluators | 22 |
| owise | 26 |
| priority(39) | 1 |
| priority(40) | 41 |
| priority(45) | 3 |
| total | 107 |

## Counts by file

| file | syntax | rule | claim | context | configuration | other directives |
|---|---:|---:|---:|---:|---:|---:|
| semantics.k | 0 | 0 | 0 | 0 | 0 | 27 |
| semantics/assert.k | 0 | 3 | 0 | 0 | 0 | 3 |
| semantics/bool.k | 0 | 13 | 0 | 1 | 0 | 3 |
| semantics/builtins.k | 38 | 137 | 0 | 0 | 0 | 9 |
| semantics/call.k | 3 | 21 | 0 | 0 | 0 | 5 |
| semantics/comprehension.k | 3 | 7 | 0 | 0 | 0 | 7 |
| semantics/concrete.k | 5 | 16 | 0 | 0 | 0 | 3 |
| semantics/controls.k | 3 | 34 | 0 | 0 | 0 | 5 |
| semantics/core.k | 37 | 46 | 0 | 0 | 1 | 9 |
| semantics/dict.k | 12 | 28 | 0 | 0 | 0 | 6 |
| semantics/float.k | 34 | 121 | 0 | 0 | 0 | 5 |
| semantics/functions.k | 4 | 15 | 0 | 0 | 0 | 3 |
| semantics/int.k | 1 | 16 | 0 | 0 | 0 | 3 |
| semantics/iter.k | 1 | 0 | 0 | 0 | 0 | 3 |
| semantics/list.k | 5 | 27 | 0 | 0 | 0 | 5 |
| semantics/methods.k | 27 | 75 | 0 | 0 | 0 | 6 |
| semantics/operators.k | 0 | 10 | 0 | 2 | 0 | 4 |
| semantics/range.k | 2 | 6 | 0 | 0 | 0 | 4 |
| semantics/set.k | 6 | 12 | 0 | 0 | 0 | 3 |
| semantics/sort.k | 6 | 19 | 0 | 0 | 0 | 4 |
| semantics/str.k | 5 | 28 | 0 | 0 | 0 | 4 |
| semantics/subscript.k | 15 | 40 | 0 | 2 | 0 | 3 |
| semantics/syntax.k | 16 | 0 | 0 | 0 | 0 | 6 |
| semantics/tuple.k | 4 | 21 | 0 | 0 | 0 | 6 |
| spec.k | 0 | 0 | 2 | 0 | 0 | 3 |
| verification.k | 0 | 0 | 0 | 0 | 0 | 3 |

## Every declaration, rule, and claim

| file:line | kind | attributes/classifiers | disposition | normalized source record |
|---|---|---|---|---|
| semantics.k:58 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY |
| semantics.k:59 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-CORE |
| semantics.k:60 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-ITER |
| semantics.k:61 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-RANGE |
| semantics.k:62 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-OPERATORS |
| semantics.k:63 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-INT |
| semantics.k:64 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-BOOL |
| semantics.k:65 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-FLOAT |
| semantics.k:66 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-STR |
| semantics.k:67 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-SET |
| semantics.k:68 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-LIST |
| semantics.k:69 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-TUPLE |
| semantics.k:70 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-SUBSCRIPT |
| semantics.k:71 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-COMPREHENSION |
| semantics.k:72 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-METHODS |
| semantics.k:73 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-CONTROLS |
| semantics.k:74 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-FUNCTIONS |
| semantics.k:75 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-BUILTINS |
| semantics.k:76 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-CALL |
| semantics.k:77 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-SORT |
| semantics.k:78 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-ASSERT |
| semantics.k:79 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-DICT |
| semantics.k:80 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics.k:87 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY-KRUN |
| semantics.k:88 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY |
| semantics.k:89 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-CONCRETE |
| semantics.k:90 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics/assert.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY-ASSERT |
| semantics/assert.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-CORE |
| semantics/assert.k:6 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Assert(V:Val) => .K ... </k> requires truthy(V) |
| semantics/assert.k:8 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V) |
| semantics/assert.k:13 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/assert.k:16 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics/bool.k:5 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-BOOL |
| semantics/bool.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/bool.k:8 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyUn("not", V:Val) => notBool truthy(V) |
| semantics/bool.k:10 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2 |
| semantics/bool.k:11 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 |
| semantics/bool.k:16 | context | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | context BoolOp(_, (HOLE:Expr, _:Exprs)) |
| semantics/bool.k:17 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k> |
| semantics/bool.k:18 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V) |
| semantics/bool.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V) |
| semantics/bool.k:22 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V) |
| semantics/bool.k:24 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) |
| semantics/bool.k:29 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)] |
| semantics/bool.k:31 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)] |
| semantics/bool.k:35 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)] |
| semantics/bool.k:39 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)] |
| semantics/bool.k:43 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)] |
| semantics/bool.k:47 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/builtins.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-BUILTINS |
| semantics/builtins.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/builtins.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-STR |
| semantics/builtins.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-SET |
| semantics/builtins.k:7 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-ITER |
| semantics/builtins.k:8 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-RANGE |
| semantics/builtins.k:9 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-INT |
| semantics/builtins.k:10 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-METHODS |
| semantics/builtins.k:17 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= applyBuiltin(String, Vals) [function] |
| semantics/builtins.k:20 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= seqLen(Val) [function] |
| semantics/builtins.k:21 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ) |
| semantics/builtins.k:22 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule seqLen(list(VS:ValSeq))                  => vsLen(VS) |
| semantics/builtins.k:23 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS) |
| semantics/builtins.k:24 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule seqLen(str(IS:IntSeq))                   => isLen(IS) |
| semantics/builtins.k:25 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule seqLen(setV(DS:IntSeq))                  => isLen(DS) |
| semantics/builtins.k:26 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) |
| semantics/builtins.k:32 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k> |
| semantics/builtins.k:33 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k> |
| semantics/builtins.k:34 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k> |
| semantics/builtins.k:35 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k> |
| semantics/builtins.k:36 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= charsOf(IntSeq) [function, total] |
| semantics/builtins.k:37 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule charsOf(.IntSeq)                => .ValSeq |
| semantics/builtins.k:38 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) |
| semantics/builtins.k:41 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) |
| semantics/builtins.k:44 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) |
| semantics/builtins.k:47 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int) |
| semantics/builtins.k:48 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k> |
| semantics/builtins.k:49 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k> |
| semantics/builtins.k:50 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V) |
| semantics/builtins.k:54 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= intOf(Val) [function] |
| semantics/builtins.k:55 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intOf(I:Int)  => I |
| semantics/builtins.k:56 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intOf(B:Bool) => #if B #then 1 #else 0 #fi |
| semantics/builtins.k:59 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #allAcc(Iterable) \| "#allCont" |
| semantics/builtins.k:60 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k> |
| semantics/builtins.k:61 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterDone ~> #allCont => true ... </k> |
| semantics/builtins.k:62 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V) |
| semantics/builtins.k:64 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V) |
| semantics/builtins.k:67 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #anyAcc(Iterable) \| "#anyCont" |
| semantics/builtins.k:68 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k> |
| semantics/builtins.k:69 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterDone ~> #anyCont => false ... </k> |
| semantics/builtins.k:70 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V) |
| semantics/builtins.k:72 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) |
| semantics/builtins.k:76 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int) |
| semantics/builtins.k:77 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k> |
| semantics/builtins.k:78 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V) |
| semantics/builtins.k:80 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k> |
| semantics/builtins.k:81 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k> |
| semantics/builtins.k:82 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V) |
| semantics/builtins.k:86 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int) |
| semantics/builtins.k:87 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k> |
| semantics/builtins.k:88 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V) |
| semantics/builtins.k:90 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k> |
| semantics/builtins.k:91 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterDone ~> #minCont(M:Int) => M ... </k> |
| semantics/builtins.k:92 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) |
| semantics/builtins.k:97 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= maxVals(Int, Vals) [function] |
| semantics/builtins.k:98 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST) |
| semantics/builtins.k:99 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule maxVals(M:Int, .Vals)           => M |
| semantics/builtins.k:100 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R) |
| semantics/builtins.k:102 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= minVals(Int, Vals) [function] |
| semantics/builtins.k:103 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST) |
| semantics/builtins.k:104 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule minVals(M:Int, .Vals)           => M |
| semantics/builtins.k:105 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) |
| semantics/builtins.k:108 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 |
| semantics/builtins.k:111 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0 |
| semantics/builtins.k:114 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= binCodes(Int) [function, total] |
| semantics/builtins.k:115 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule binCodes(0) => iCons(48, .IntSeq) |
| semantics/builtins.k:116 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0 |
| semantics/builtins.k:117 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= binAcc(Int, IntSeq) [function, total] |
| semantics/builtins.k:118 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule binAcc(0, ACC:IntSeq) => ACC |
| semantics/builtins.k:119 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 |
| semantics/builtins.k:124 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k> |
| semantics/builtins.k:126 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= enumVS(ValSeq, Int) [function, total] |
| semantics/builtins.k:127 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule enumVS(.ValSeq, _:Int) => .ValSeq |
| semantics/builtins.k:128 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) |
| semantics/builtins.k:132 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k> |
| semantics/builtins.k:134 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= mapStrVS(ValSeq) [function, total] |
| semantics/builtins.k:135 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mapStrVS(.ValSeq) => .ValSeq |
| semantics/builtins.k:136 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R)) |
| semantics/builtins.k:137 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) |
| semantics/builtins.k:140 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("int", I:Int, .Vals) => I |
| semantics/builtins.k:143 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C |
| semantics/builtins.k:144 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 |
| semantics/builtins.k:148 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I))) |
| semantics/builtins.k:149 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) |
| semantics/builtins.k:152 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 |
| semantics/builtins.k:156 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2 |
| semantics/builtins.k:158 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= intDigAcc(IntSeq, Int) [function, total] |
| semantics/builtins.k:159 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intDigAcc(.IntSeq, ACC:Int)             => ACC |
| semantics/builtins.k:160 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) |
| semantics/builtins.k:163 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B) |
| semantics/builtins.k:164 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B) |
| semantics/builtins.k:167 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k> |
| semantics/builtins.k:169 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k> |
| semantics/builtins.k:170 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k> |
| semantics/builtins.k:171 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k> |
| semantics/builtins.k:173 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k> |
| semantics/builtins.k:174 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> |
| semantics/builtins.k:177 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1) |
| semantics/builtins.k:178 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1) |
| semantics/builtins.k:179 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 |
| semantics/builtins.k:187 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS) |
| semantics/builtins.k:188 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= evalArith(IntSeq) [function] |
| semantics/builtins.k:189 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS))))) |
| semantics/builtins.k:192 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq) |
| semantics/builtins.k:194 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= evDigit(Int) [function, total] |
| semantics/builtins.k:195 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57 |
| semantics/builtins.k:196 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= evHead42(IntSeq) [function, total] |
| semantics/builtins.k:197 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule evHead42(iCons(42, _:IntSeq)) => true |
| semantics/builtins.k:198 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule evHead42(_:IntSeq)            => false [owise] |
| semantics/builtins.k:199 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= evHead47(IntSeq) [function, total] |
| semantics/builtins.k:200 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule evHead47(iCons(47, _:IntSeq)) => true |
| semantics/builtins.k:201 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule evHead47(_:IntSeq)            => false [owise] |
| semantics/builtins.k:203 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax OpSeq ::= tokOps(IntSeq) [function, total] |
| semantics/builtins.k:204 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokOps(.IntSeq)                 => .OpSeq |
| semantics/builtins.k:205 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokOps(iCons(32, R:IntSeq))     => tokOps(R) |
| semantics/builtins.k:206 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C) |
| semantics/builtins.k:207 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R)) |
| semantics/builtins.k:208 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R) |
| semantics/builtins.k:209 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons(" |
| semantics/builtins.k:210 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R) |
| semantics/builtins.k:211 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R)) |
| semantics/builtins.k:212 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R)) |
| semantics/builtins.k:214 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total] |
| semantics/builtins.k:216 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokNds(.IntSeq)                => .IntSeq |
| semantics/builtins.k:217 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokNds(iCons(32, R:IntSeq))    => tokNds(R) |
| semantics/builtins.k:218 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C) |
| semantics/builtins.k:219 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32 |
| semantics/builtins.k:221 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C) |
| semantics/builtins.k:223 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise] |
| semantics/builtins.k:225 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax EvPair ::= evp(OpSeq, IntSeq) |
| semantics/builtins.k:226 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= firstNdE(EvPair) [function, total] |
| semantics/builtins.k:227 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N |
| semantics/builtins.k:228 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule firstNdE(_:EvPair) => 0 [owise] |
| semantics/builtins.k:230 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= applyOpE(String, Int, Int) [function, total] |
| semantics/builtins.k:231 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyOpE("+",  A:Int, B:Int) => A +Int B |
| semantics/builtins.k:232 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyOpE("-",  A:Int, B:Int) => A -Int B |
| semantics/builtins.k:233 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyOpE("*",  A:Int, B:Int) => A *Int B |
| semantics/builtins.k:234 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyOpE(" |
| semantics/builtins.k:235 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyOpE("**", A:Int, B:Int) => A ^Int B |
| semantics/builtins.k:236 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyOpE(_:String, A:Int, _:Int) => A [owise] |
| semantics/builtins.k:238 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total] |
| semantics/builtins.k:239 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS) |
| semantics/builtins.k:240 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS)) |
| semantics/builtins.k:241 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**" |
| semantics/builtins.k:243 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise] |
| semantics/builtins.k:244 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax EvPair ::= powCombE(Int, EvPair) [function, total] |
| semantics/builtins.k:245 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST)) |
| semantics/builtins.k:246 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq)) |
| semantics/builtins.k:247 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total] |
| semantics/builtins.k:248 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS)) |
| semantics/builtins.k:250 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total] |
| semantics/builtins.k:251 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq) |
| semantics/builtins.k:252 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq) |
| semantics/builtins.k:253 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq) |
| semantics/builtins.k:254 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq) |
| semantics/builtins.k:255 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total] |
| semantics/builtins.k:256 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) |
| semantics/builtins.k:257 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O) |
| semantics/builtins.k:260 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O) |
| semantics/builtins.k:263 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise] |
| semantics/builtins.k:265 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= inLevelE(String, String) [function, total] |
| semantics/builtins.k:266 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String " |
| semantics/builtins.k:267 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-" |
| semantics/builtins.k:268 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule inLevelE(_:String, _:String) => false [owise] |
| semantics/builtins.k:269 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax OpSeq ::= appendOpE(OpSeq, String) [function, total] |
| semantics/builtins.k:270 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq) |
| semantics/builtins.k:271 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O)) |
| semantics/builtins.k:272 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= appendIE(IntSeq, Int) [function, total] |
| semantics/builtins.k:273 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq) |
| semantics/builtins.k:274 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) |
| semantics/builtins.k:279 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= "#md5" |
| semantics/builtins.k:280 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)] |
| semantics/builtins.k:282 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k> |
| semantics/builtins.k:283 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= md5Obj(IntSeq) |
| semantics/builtins.k:284 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS)) |
| semantics/builtins.k:285 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] |
| semantics/builtins.k:291 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V) |
| semantics/builtins.k:292 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V) |
| semantics/builtins.k:293 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function] |
| semantics/builtins.k:294 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule isIntV(_:Int)         => true |
| semantics/builtins.k:295 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule isIntV(_:Val)         => false [owise] |
| semantics/builtins.k:296 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule isStrV(str(_:IntSeq)) => true |
| semantics/builtins.k:297 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule isStrV(_:Val)         => false [owise] |
| semantics/builtins.k:298 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/call.k:10 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY-CALL |
| semantics/call.k:11 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-METHODS |
| semantics/call.k:12 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-BUILTINS |
| semantics/call.k:13 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-FUNCTIONS |
| semantics/call.k:16 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> |
| semantics/call.k:19 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #callee(Exprs) |
| semantics/call.k:20 | rule | owise | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise] |
| semantics/call.k:21 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> |
| semantics/call.k:24 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k> |
| semantics/call.k:26 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k> |
| semantics/call.k:27 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k> |
| semantics/call.k:28 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k> |
| semantics/call.k:29 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k> |
| semantics/call.k:30 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k> |
| semantics/call.k:31 | rule | owise | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise] |
| semantics/call.k:32 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k> |
| semantics/call.k:38 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/call.k:42 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)] |
| semantics/call.k:47 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/call.k:52 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Bool ::= isMutMethod(String) [function, total] |
| semantics/call.k:53 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove" |
| semantics/call.k:56 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] |
| semantics/call.k:63 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)] |
| semantics/call.k:69 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> |
| semantics/call.k:80 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> |
| semantics/call.k:87 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #allocCells(ParamNames) |
| semantics/call.k:88 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #allocCells(.ParamNames) => .K ... </k> |
| semantics/call.k:89 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) |
| semantics/call.k:95 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics/comprehension.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-COMPREHENSION |
| semantics/comprehension.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/comprehension.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-OPERATORS |
| semantics/comprehension.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-LIST |
| semantics/comprehension.k:7 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CONTROLS |
| semantics/comprehension.k:8 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-FUNCTIONS |
| semantics/comprehension.k:11 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| semantics/comprehension.k:12 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| semantics/comprehension.k:14 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Stmts ::= compBody(CompFors, Expr) [macro] |
| semantics/comprehension.k:15 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc")) |
| semantics/comprehension.k:18 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Stmt ::= compNest(CompFors, Expr) [macro-rec] |
| semantics/comprehension.k:19 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT))) |
| semantics/comprehension.k:21 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts)) |
| semantics/comprehension.k:24 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Expr ::= compGuard(Exprs) [macro] |
| semantics/comprehension.k:25 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule compGuard(.Exprs)             => Bool(true) |
| semantics/comprehension.k:26 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs)) |
| semantics/comprehension.k:27 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/concrete.k:8 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-CONCRETE |
| semantics/concrete.k:9 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY |
| semantics/concrete.k:13 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) |
| semantics/concrete.k:16 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) |
| semantics/concrete.k:25 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= kvP(Val, Val) |
| semantics/concrete.k:26 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool) |
| semantics/concrete.k:28 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)] |
| semantics/concrete.k:31 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)] |
| semantics/concrete.k:34 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k> |
| semantics/concrete.k:36 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k> |
| semantics/concrete.k:38 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K) |
| semantics/concrete.k:42 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= insPair(ValSeq, Val, Val) [function] |
| semantics/concrete.k:43 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq) |
| semantics/concrete.k:44 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2) |
| semantics/concrete.k:47 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2) |
| semantics/concrete.k:51 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= kLt(Val, Val) [function] |
| semantics/concrete.k:52 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule kLt(I1:Int, I2:Int)             => I1 <Int I2 |
| semantics/concrete.k:53 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule kLt(F1:Float, F2:Float)         => F1 <Float F2 |
| semantics/concrete.k:54 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B) |
| semantics/concrete.k:56 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= unpairVS(ValSeq) [function, total] |
| semantics/concrete.k:57 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule unpairVS(.ValSeq) => .ValSeq |
| semantics/concrete.k:58 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R)) |
| semantics/concrete.k:59 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise] |
| semantics/concrete.k:60 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/controls.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY-CONTROLS |
| semantics/controls.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-CORE |
| semantics/controls.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-TUPLE |
| semantics/controls.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-ITER |
| semantics/controls.k:9 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes> |
| semantics/controls.k:12 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)] |
| semantics/controls.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) |
| semantics/controls.k:27 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] |
| semantics/controls.k:35 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k> |
| semantics/controls.k:36 | rule | owise | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise] |
| semantics/controls.k:37 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #bindImports(ParamNames) |
| semantics/controls.k:38 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #bindImports(.ParamNames) => .K ... </k> |
| semantics/controls.k:39 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil" |
| semantics/controls.k:43 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") |
| semantics/controls.k:48 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Expr(_:Val) => .K ... </k> |
| semantics/controls.k:51 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #branch(Bool, Stmts, Stmts) |
| semantics/controls.k:52 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k> |
| semantics/controls.k:53 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k> |
| semantics/controls.k:54 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> |
| semantics/controls.k:57 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V) |
| semantics/controls.k:59 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) |
| semantics/controls.k:65 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk" |
| semantics/controls.k:69 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k> |
| semantics/controls.k:71 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k> |
| semantics/controls.k:72 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k> |
| semantics/controls.k:73 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> |
| semantics/controls.k:77 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k> |
| semantics/controls.k:78 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k> |
| semantics/controls.k:79 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V) |
| semantics/controls.k:81 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) |
| semantics/controls.k:85 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #loopLbl(NEXT:K) => NEXT ... </k> |
| semantics/controls.k:86 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Continue => #cont ... </k> |
| semantics/controls.k:87 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Break => #brk ... </k> |
| semantics/controls.k:88 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k> |
| semantics/controls.k:89 | rule | owise | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #cont ~> (_:KItem => .K) ... </k> [owise] |
| semantics/controls.k:90 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #brk ~> #loopLbl(_:K) => .K ... </k> |
| semantics/controls.k:91 | rule | owise | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] |
| semantics/controls.k:95 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/controls.k:98 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/controls.k:101 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/controls.k:106 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/controls.k:109 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics/core.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY-CORE |
| semantics/core.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-SYNTAX |
| semantics/core.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports INT |
| semantics/core.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports BOOL |
| semantics/core.k:7 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports STRING |
| semantics/core.k:8 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MAP |
| semantics/core.k:9 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports LIST |
| semantics/core.k:10 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports K-EQUAL |
| semantics/core.k:13 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq) |
| semantics/core.k:14 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq) |
| semantics/core.k:15 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Str    ::= str(IntSeq) |
| semantics/core.k:18 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq) |
| semantics/core.k:25 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Val      ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) \| cellRef(Int) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) \| builtinV(String) \| boundMethodV(Val, String) |
| semantics/core.k:36 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Parent   ::= "root" \| parent(Int) |
| semantics/core.k:37 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Scope    ::= scope(Map, Parent) |
| semantics/core.k:38 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KResult  ::= Val |
| semantics/core.k:39 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Expr     ::= Val |
| semantics/core.k:40 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Vals     ::= List{Val, ","} |
| semantics/core.k:41 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Exc      ::= "NoExc" \| "AssertionError" |
| semantics/core.k:42 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax RetState ::= "noRet" \| retV(Val) |
| semantics/core.k:49 | configuration | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     \|-> scope(.Map, parent(-1)) -1    \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code> |
| semantics/core.k:68 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Bool ::= isRefV(Val) [function, total] |
| semantics/core.k:69 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule isRefV(ref(_:Int)) => true |
| semantics/core.k:70 | rule | owise | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule isRefV(_:Val)      => false [owise] |
| semantics/core.k:75 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax HeapVal ::= cellV(Val) |
| semantics/core.k:76 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Bool ::= isCellRef(Val) [function, total] |
| semantics/core.k:77 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule isCellRef(cellRef(_:Int)) => true |
| semantics/core.k:78 | rule | owise | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule isCellRef(_:Val)          => false [owise] |
| semantics/core.k:85 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] |
| semantics/core.k:95 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Val ::= kwV(String, Val) |
| semantics/core.k:96 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #kwTag(String) |
| semantics/core.k:97 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k> |
| semantics/core.k:98 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V) |
| semantics/core.k:100 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Bool ::= isKwV(Val) [function, total] |
| semantics/core.k:101 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule isKwV(kwV(_:String, _:Val)) => true |
| semantics/core.k:102 | rule | owise | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule isKwV(_:Val)                => false [owise] |
| semantics/core.k:106 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Val ::= cellsMark(ParamNames) |
| semantics/core.k:107 | syntax | function | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax ParamNames ::= cellsOf(Val) [function] |
| semantics/core.k:108 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule cellsOf(cellsMark(CVS:ParamNames)) => CVS |
| semantics/core.k:109 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Bool ::= pnMember(String, ParamNames) [function, total] |
| semantics/core.k:110 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule pnMember(_:String, .ParamNames) => false |
| semantics/core.k:111 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R) |
| semantics/core.k:113 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #cellW(Val, Val) |
| semantics/core.k:114 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap> |
| semantics/core.k:117 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #alloc(Val) |
| semantics/core.k:118 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) |
| semantics/core.k:124 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #loadAll(Module) |
| semantics/core.k:125 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k> |
| semantics/core.k:126 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k> |
| semantics/core.k:127 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> .Stmts => .K ... </k> |
| semantics/core.k:130 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #look(String, Int) |
| semantics/core.k:131 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env> |
| semantics/core.k:132 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) |
| semantics/core.k:145 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)] |
| semantics/core.k:152 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) |
| semantics/core.k:157 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Scope ::= "builtinsScope" [function, total] |
| semantics/core.k:158 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root) |
| semantics/core.k:185 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax ApplyK ::= toCall(Val) |
| semantics/core.k:186 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals) |
| semantics/core.k:189 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k> |
| semantics/core.k:190 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k> |
| semantics/core.k:191 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> |
| semantics/core.k:194 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Int(I:Int)   => I ... </k> |
| semantics/core.k:195 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Bool(B:Bool) => B ... </k> |
| semantics/core.k:196 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> NoneVal      => noneV ... </k> |
| semantics/core.k:199 | syntax | function | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Bool ::= truthy(Val) [function] |
| semantics/core.k:200 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule truthy(B:Bool)          => B |
| semantics/core.k:201 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule truthy(noneV)           => false |
| semantics/core.k:202 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule truthy(I:Int)           => I =/=Int 0 |
| semantics/core.k:203 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq) |
| semantics/core.k:204 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq) |
| semantics/core.k:205 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) |
| semantics/core.k:208 | syntax | function | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Val  ::= applyUn(String, Val) [function] |
| semantics/core.k:209 | syntax | function | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Val  ::= applyBin(String, Val, Val) [function] |
| semantics/core.k:210 | syntax | function | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Bool ::= applyCmp(String, Val, Val) [function] |
| semantics/core.k:213 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Vals ::= appendVal(Vals, Val) [function, total] |
| semantics/core.k:214 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule appendVal(.Vals, V:Val)              => V , .Vals |
| semantics/core.k:215 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V) |
| semantics/core.k:217 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax ValSeq ::= vals2valSeq(Vals) [function, total] |
| semantics/core.k:218 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule vals2valSeq(.Vals)            => .ValSeq |
| semantics/core.k:219 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) |
| semantics/core.k:223 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Int ::= vsLen(ValSeq) [function, total] |
| semantics/core.k:224 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule vsLen(.ValSeq)                => 0 |
| semantics/core.k:225 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S) |
| semantics/core.k:227 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Int ::= isLen(IntSeq) [function, total] |
| semantics/core.k:228 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule isLen(.IntSeq)                => 0 |
| semantics/core.k:229 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) |
| semantics/core.k:233 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total] |
| semantics/core.k:234 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq |
| semantics/core.k:235 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S) |
| semantics/core.k:236 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0 |
| semantics/core.k:238 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0 |
| semantics/core.k:240 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics/dict.k:13 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-DICT |
| semantics/dict.k:14 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/dict.k:15 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-ITER |
| semantics/dict.k:16 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-METHODS |
| semantics/dict.k:17 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-LIST |
| semantics/dict.k:20 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= dictV(ValSeq, ValSeq) |
| semantics/dict.k:23 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq) |
| semantics/dict.k:26 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k> |
| semantics/dict.k:27 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k> |
| semantics/dict.k:28 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k> |
| semantics/dict.k:30 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k> |
| semantics/dict.k:32 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> |
| semantics/dict.k:37 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= dHasKey(ValSeq, Val) [function, total] |
| semantics/dict.k:38 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dHasKey(.ValSeq, _:Val)                => false |
| semantics/dict.k:39 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K |
| semantics/dict.k:40 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) |
| semantics/dict.k:43 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= dPutK(ValSeq, Val) [function, total] |
| semantics/dict.k:44 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K) |
| semantics/dict.k:45 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) |
| semantics/dict.k:49 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total] |
| semantics/dict.k:50 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K |
| semantics/dict.k:52 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K) |
| semantics/dict.k:54 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] |
| semantics/dict.k:58 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] |
| semantics/dict.k:63 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K) |
| semantics/dict.k:64 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= applyIndexD(Val, Val) [function] |
| semantics/dict.k:65 | rule | priority(45) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] |
| semantics/dict.k:70 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= dictSet(Val, Val, Val) [function] |
| semantics/dict.k:71 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) |
| semantics/dict.k:76 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #dsetK(String, Val) |
| semantics/dict.k:77 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k> |
| semantics/dict.k:78 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val) |
| semantics/dict.k:82 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) |
| semantics/dict.k:86 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #dsetV(Val, Val, Val) |
| semantics/dict.k:87 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> |
| semantics/dict.k:90 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= normIdxD(Int, Int) [function, total] |
| semantics/dict.k:91 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0 |
| semantics/dict.k:92 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0 |
| semantics/dict.k:95 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2) |
| semantics/dict.k:97 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function] |
| semantics/dict.k:98 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true |
| semantics/dict.k:99 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2) |
| semantics/dict.k:101 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= dGet(ValSeq, ValSeq, Val) [function] |
| semantics/dict.k:102 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K |
| semantics/dict.k:103 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K) |
| semantics/dict.k:104 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/float.k:14 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-FLOAT |
| semantics/float.k:15 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-OPERATORS |
| semantics/float.k:16 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-BUILTINS |
| semantics/float.k:17 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports FLOAT |
| semantics/float.k:20 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= Float |
| semantics/float.k:21 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Float(F:Float) => F ... </k> |
| semantics/float.k:24 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators] |
| semantics/float.k:25 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete] |
| semantics/float.k:27 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) |
| semantics/float.k:30 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators] |
| semantics/float.k:31 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete] |
| semantics/float.k:32 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) |
| semantics/float.k:37 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators] |
| semantics/float.k:38 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete] |
| semantics/float.k:39 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) |
| semantics/float.k:43 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2 |
| semantics/float.k:44 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) |
| semantics/float.k:50 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators] |
| semantics/float.k:51 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete] |
| semantics/float.k:52 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2) |
| semantics/float.k:54 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators] |
| semantics/float.k:55 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule absF(F:Float) => absFloat(F) [concrete] |
| semantics/float.k:56 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("abs", F:Float, .Vals) => absF(F) |
| semantics/float.k:61 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Import(_:String) => .K ... </k> |
| semantics/float.k:65 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= "#mathCeil" |
| semantics/float.k:66 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)] |
| semantics/float.k:67 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> |
| semantics/float.k:70 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= "#mathFloor" |
| semantics/float.k:71 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)] |
| semantics/float.k:72 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k> |
| semantics/float.k:73 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)] |
| semantics/float.k:74 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule floorFI(I:Int)   => I                        [concrete] |
| semantics/float.k:75 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] |
| semantics/float.k:78 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V) |
| semantics/float.k:79 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V) |
| semantics/float.k:82 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val) |
| semantics/float.k:83 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)] |
| semantics/float.k:84 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k> |
| semantics/float.k:85 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k> |
| semantics/float.k:86 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= toF(Val) [function, total, symbol(toF)] |
| semantics/float.k:87 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule toF(F:Float) => F        [concrete] |
| semantics/float.k:88 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule toF(I:Int)   => intToF(I) [concrete] |
| semantics/float.k:93 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)] |
| semantics/float.k:94 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule ceilF(I:Int)   => I                       [concrete] |
| semantics/float.k:95 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] |
| semantics/float.k:99 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyUn("-", F:Float) => 0.0 -Float F |
| semantics/float.k:103 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators] |
| semantics/float.k:104 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete] |
| semantics/float.k:105 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2) |
| semantics/float.k:107 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators] |
| semantics/float.k:108 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete] |
| semantics/float.k:109 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2) |
| semantics/float.k:111 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators] |
| semantics/float.k:112 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete] |
| semantics/float.k:113 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2) |
| semantics/float.k:115 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators] |
| semantics/float.k:116 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete] |
| semantics/float.k:117 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2) |
| semantics/float.k:119 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators] |
| semantics/float.k:120 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete] |
| semantics/float.k:121 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) |
| semantics/float.k:125 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators] |
| semantics/float.k:126 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete] |
| semantics/float.k:127 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2) |
| semantics/float.k:128 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2) |
| semantics/float.k:129 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) |
| semantics/float.k:132 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F) |
| semantics/float.k:133 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I)) |
| semantics/float.k:134 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F) |
| semantics/float.k:135 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I)) |
| semantics/float.k:136 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F) |
| semantics/float.k:137 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I)) |
| semantics/float.k:138 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F) |
| semantics/float.k:139 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I)) |
| semantics/float.k:142 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators] |
| semantics/float.k:143 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete] |
| semantics/float.k:144 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F) |
| semantics/float.k:145 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I)) |
| semantics/float.k:146 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F) |
| semantics/float.k:147 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I)) |
| semantics/float.k:148 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F) |
| semantics/float.k:149 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I)) |
| semantics/float.k:150 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F) |
| semantics/float.k:151 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I)) |
| semantics/float.k:154 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", V:Val, noneV) => V ==K noneV |
| semantics/float.k:155 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) |
| semantics/float.k:160 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators] |
| semantics/float.k:161 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete] |
| semantics/float.k:162 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete] |
| semantics/float.k:165 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= headIS(IntSeq) [function] |
| semantics/float.k:166 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule headIS(iCons(C:Int, _:IntSeq)) => C |
| semantics/float.k:167 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total] |
| semantics/float.k:168 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intPart(CS:IntSeq) => intPartAcc(CS, 0) |
| semantics/float.k:169 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intPartAcc(.IntSeq, A:Int) => A |
| semantics/float.k:170 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A |
| semantics/float.k:171 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46 |
| semantics/float.k:173 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total] |
| semantics/float.k:174 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fracPart(.IntSeq) => 0 |
| semantics/float.k:175 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0) |
| semantics/float.k:176 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46 |
| semantics/float.k:177 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fracAcc(.IntSeq, A:Int) => A |
| semantics/float.k:178 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48)) |
| semantics/float.k:179 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total] |
| semantics/float.k:180 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fracScale(.IntSeq) => 1 |
| semantics/float.k:181 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1) |
| semantics/float.k:182 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46 |
| semantics/float.k:183 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fscAcc(.IntSeq, A:Int) => A |
| semantics/float.k:184 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10) |
| semantics/float.k:185 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS) |
| semantics/float.k:186 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("float", I:Int, .Vals)          => intToF(I) |
| semantics/float.k:187 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("float", F:Float, .Vals)        => F |
| semantics/float.k:190 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators] |
| semantics/float.k:191 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete] |
| semantics/float.k:192 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) |
| semantics/float.k:195 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators] |
| semantics/float.k:196 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete] |
| semantics/float.k:197 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F) |
| semantics/float.k:198 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I)) |
| semantics/float.k:199 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F) |
| semantics/float.k:200 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I)) |
| semantics/float.k:201 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F) |
| semantics/float.k:202 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) |
| semantics/float.k:203 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F) |
| semantics/float.k:204 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I)) |
| semantics/float.k:205 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F) |
| semantics/float.k:206 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) |
| semantics/float.k:209 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators] |
| semantics/float.k:210 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete] |
| semantics/float.k:211 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("int", F:Float, .Vals) => truncF(F) |
| semantics/float.k:213 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("float", I:Int, .Vals)   => intToF(I) |
| semantics/float.k:214 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("float", F:Float, .Vals) => F |
| semantics/float.k:217 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators] |
| semantics/float.k:218 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete] |
| semantics/float.k:223 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators] |
| semantics/float.k:224 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete] |
| semantics/float.k:227 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("round", F:Float, .Vals)        => roundF(F) |
| semantics/float.k:228 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N) |
| semantics/float.k:230 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators] |
| semantics/float.k:231 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule sqrtF(F:Float) => sqrtFloat(F) [concrete] |
| semantics/float.k:232 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= "#mathSqrt" |
| semantics/float.k:233 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)] |
| semantics/float.k:234 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k> |
| semantics/float.k:235 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> |
| semantics/float.k:243 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float) |
| semantics/float.k:244 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V) |
| semantics/float.k:245 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k> |
| semantics/float.k:246 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k> |
| semantics/float.k:247 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V) |
| semantics/float.k:250 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float) |
| semantics/float.k:251 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V) |
| semantics/float.k:252 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k> |
| semantics/float.k:253 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterDone ~> #minContF(M:Float) => M ... </k> |
| semantics/float.k:254 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) |
| semantics/float.k:261 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float) |
| semantics/float.k:262 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V)) |
| semantics/float.k:265 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k> |
| semantics/float.k:266 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k> |
| semantics/float.k:267 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V) |
| semantics/float.k:270 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V) |
| semantics/float.k:273 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/functions.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY-FUNCTIONS |
| semantics/functions.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-CORE |
| semantics/functions.k:8 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall" |
| semantics/functions.k:14 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes> |
| semantics/functions.k:18 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Expr ::= closureExpr(ParamNames, Stmts) |
| semantics/functions.k:19 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> |
| semantics/functions.k:27 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) |
| semantics/functions.k:31 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map) |
| semantics/functions.k:33 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k> |
| semantics/functions.k:36 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M) |
| semantics/functions.k:42 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes> |
| semantics/functions.k:47 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env> |
| semantics/functions.k:50 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k> |
| semantics/functions.k:53 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M) |
| semantics/functions.k:59 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> |
| semantics/functions.k:63 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #bindP(.ParamNames, .Vals) => .K ... </k> |
| semantics/functions.k:64 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes> |
| semantics/functions.k:68 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] |
| semantics/functions.k:78 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret> |
| semantics/functions.k:80 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> |
| semantics/functions.k:85 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc> |
| semantics/functions.k:91 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics/int.k:4 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY-INT |
| semantics/int.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-CORE |
| semantics/int.k:7 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyUn("-", I:Int) => 0 -Int I |
| semantics/int.k:9 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2 |
| semantics/int.k:11 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi |
| semantics/int.k:12 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I |
| semantics/int.k:13 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2 |
| semantics/int.k:14 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2 |
| semantics/int.k:15 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2) |
| semantics/int.k:16 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyBin(" |
| semantics/int.k:17 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0 |
| semantics/int.k:19 | syntax | function | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Int ::= pyMod(Int, Int) [function] |
| semantics/int.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2 |
| semantics/int.k:22 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2 |
| semantics/int.k:23 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2 |
| semantics/int.k:24 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2 |
| semantics/int.k:25 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2 |
| semantics/int.k:26 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2 |
| semantics/int.k:27 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2 |
| semantics/int.k:28 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics/iter.k:6 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-ITER |
| semantics/iter.k:7 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/iter.k:8 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable) |
| semantics/iter.k:9 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/list.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-LIST |
| semantics/list.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/list.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-ITER |
| semantics/list.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-OPERATORS |
| semantics/list.k:9 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k> |
| semantics/list.k:10 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> |
| semantics/list.k:13 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ApplyK ::= "toList" |
| semantics/list.k:14 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k> |
| semantics/list.k:15 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> |
| semantics/list.k:18 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total] |
| semantics/list.k:19 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule valSeqConcat(.ValSeq, T:ValSeq)                => T |
| semantics/list.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) |
| semantics/list.k:24 | rule | priority(45) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)] |
| semantics/list.k:27 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B |
| semantics/list.k:28 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) |
| semantics/list.k:33 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= hasRefVS(ValSeq) [function, total] |
| semantics/list.k:34 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule hasRefVS(.ValSeq)                => false |
| semantics/list.k:35 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R) |
| semantics/list.k:37 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map)        [function] |
| semantics/list.k:39 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true |
| semantics/list.k:40 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false |
| semantics/list.k:41 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false |
| semantics/list.k:42 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP) |
| semantics/list.k:45 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP) |
| semantics/list.k:47 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP) |
| semantics/list.k:49 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP) |
| semantics/list.k:50 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] |
| semantics/list.k:53 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] |
| semantics/list.k:58 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB" |
| semantics/list.k:59 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k> |
| semantics/list.k:60 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k> |
| semantics/list.k:61 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k> |
| semantics/list.k:62 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k> |
| semantics/list.k:63 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V |
| semantics/list.k:65 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V) |
| semantics/list.k:67 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> B:Bool ~> #notB => notBool B ... </k> |
| semantics/list.k:68 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/methods.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-METHODS |
| semantics/methods.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/methods.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports K-EQUAL |
| semantics/methods.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-STR |
| semantics/methods.k:7 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-LIST |
| semantics/methods.k:10 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= applyMethod(Val, String, Vals) [function] |
| semantics/methods.k:13 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS) |
| semantics/methods.k:14 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS) |
| semantics/methods.k:15 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS) |
| semantics/methods.k:16 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) |
| semantics/methods.k:19 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS)) |
| semantics/methods.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS)) |
| semantics/methods.k:21 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) |
| semantics/methods.k:26 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS)) |
| semantics/methods.k:27 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total] |
| semantics/methods.k:28 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq |
| semantics/methods.k:29 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS |
| semantics/methods.k:30 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) |
| semantics/methods.k:34 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC) |
| semantics/methods.k:35 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= cntSub(IntSeq, IntSeq) [function] |
| semantics/methods.k:36 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule cntSub(.IntSeq, _:IntSeq) => 0 |
| semantics/methods.k:37 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0 |
| semantics/methods.k:39 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0 |
| semantics/methods.k:41 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= dropIS(IntSeq, Int) [function, total] |
| semantics/methods.k:42 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0 |
| semantics/methods.k:43 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dropIS(.IntSeq, _:Int) => .IntSeq [owise] |
| semantics/methods.k:44 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 |
| semantics/methods.k:47 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS))))) |
| semantics/methods.k:48 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= trimWS(IntSeq) [function, total] |
| semantics/methods.k:49 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule trimWS(.IntSeq) => .IntSeq |
| semantics/methods.k:50 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C) |
| semantics/methods.k:51 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C) |
| semantics/methods.k:52 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total] |
| semantics/methods.k:53 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule revIS(S:IntSeq) => revISAcc(S, .IntSeq) |
| semantics/methods.k:54 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule revISAcc(.IntSeq, A:IntSeq) => A |
| semantics/methods.k:55 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) |
| semantics/methods.k:58 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) |
| semantics/methods.k:61 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) |
| semantics/methods.k:64 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V) |
| semantics/methods.k:65 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= cntOccVS(ValSeq, Val) [function, total] |
| semantics/methods.k:66 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule cntOccVS(.ValSeq, _:Val)                => 0 |
| semantics/methods.k:67 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V |
| semantics/methods.k:68 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V) |
| semantics/methods.k:72 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)] |
| semantics/methods.k:75 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] |
| semantics/methods.k:76 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR) |
| semantics/methods.k:77 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C) |
| semantics/methods.k:79 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) |
| semantics/methods.k:82 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function] |
| semantics/methods.k:83 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule flushTok(ACC:ValSeq, .IntSeq)            => ACC |
| semantics/methods.k:84 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq)) |
| semantics/methods.k:85 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= isWSC(Int) [function, total] |
| semantics/methods.k:86 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 |
| semantics/methods.k:89 | rule | priority(39) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] |
| semantics/methods.k:94 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)] |
| semantics/methods.k:97 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] |
| semantics/methods.k:98 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq) |
| semantics/methods.k:99 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP |
| semantics/methods.k:101 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP) |
| semantics/methods.k:104 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B)) |
| semantics/methods.k:106 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total] |
| semantics/methods.k:107 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq |
| semantics/methods.k:108 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A |
| semantics/methods.k:109 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) |
| semantics/methods.k:112 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= isUpperC(Int) [function, total] |
| semantics/methods.k:113 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90 |
| semantics/methods.k:115 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= isLowerC(Int) [function, total] |
| semantics/methods.k:116 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122 |
| semantics/methods.k:118 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= isAlphaC(Int) [function, total] |
| semantics/methods.k:119 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C) |
| semantics/methods.k:121 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= isDigitC(Int) [function, total] |
| semantics/methods.k:122 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57 |
| semantics/methods.k:124 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= hasUpper(IntSeq) [function, total] |
| semantics/methods.k:125 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule hasUpper(.IntSeq) => false |
| semantics/methods.k:126 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S) |
| semantics/methods.k:128 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= hasLower(IntSeq) [function, total] |
| semantics/methods.k:129 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule hasLower(.IntSeq) => false |
| semantics/methods.k:130 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S) |
| semantics/methods.k:132 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= allAlpha(IntSeq) [function, total] |
| semantics/methods.k:133 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule allAlpha(.IntSeq) => true |
| semantics/methods.k:134 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S) |
| semantics/methods.k:136 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= allDigit(IntSeq) [function, total] |
| semantics/methods.k:137 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule allDigit(.IntSeq) => true |
| semantics/methods.k:138 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S) |
| semantics/methods.k:140 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= lowerC(Int) [function, total] |
| semantics/methods.k:142 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule lowerC(C:Int) => C +Int 32 requires isUpperC(C) |
| semantics/methods.k:143 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule lowerC(C:Int) => C         [owise] |
| semantics/methods.k:145 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= upperC(Int) [function, total] |
| semantics/methods.k:146 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule upperC(C:Int) => C -Int 32 requires isLowerC(C) |
| semantics/methods.k:147 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule upperC(C:Int) => C         [owise] |
| semantics/methods.k:149 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= swapC(Int) [function, total] |
| semantics/methods.k:150 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule swapC(C:Int) => C +Int 32 requires isUpperC(C) |
| semantics/methods.k:151 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule swapC(C:Int) => C -Int 32 requires isLowerC(C) |
| semantics/methods.k:152 | rule | owise | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule swapC(C:Int) => C         [owise] |
| semantics/methods.k:154 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= mapLower(IntSeq) [function, total] |
| semantics/methods.k:155 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mapLower(.IntSeq) => .IntSeq |
| semantics/methods.k:156 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S)) |
| semantics/methods.k:158 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= mapUpper(IntSeq) [function, total] |
| semantics/methods.k:159 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mapUpper(.IntSeq) => .IntSeq |
| semantics/methods.k:160 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S)) |
| semantics/methods.k:162 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= mapSwap(IntSeq) [function, total] |
| semantics/methods.k:163 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mapSwap(.IntSeq) => .IntSeq |
| semantics/methods.k:164 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S)) |
| semantics/methods.k:166 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total] |
| semantics/methods.k:167 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule startsWith(.IntSeq, _:IntSeq)               => true |
| semantics/methods.k:168 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| semantics/methods.k:169 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs) |
| semantics/methods.k:170 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/operators.k:6 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY-OPERATORS |
| semantics/operators.k:7 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-CORE |
| semantics/operators.k:8 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports MPY-ITER |
| semantics/operators.k:10 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k> |
| semantics/operators.k:12 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> |
| semantics/operators.k:15 | context | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | context Compare(HOLE, _) |
| semantics/operators.k:16 | context | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | context Compare(_:Val, CmpOp(_, HOLE)) |
| semantics/operators.k:17 | rule | owise | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise] |
| semantics/operators.k:19 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyCmp("is",     V:Val, noneV) => V ==K noneV |
| semantics/operators.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) |
| semantics/operators.k:25 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/operators.k:28 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] |
| semantics/operators.k:34 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)] |
| semantics/operators.k:38 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)] |
| semantics/operators.k:44 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_USED_PATH | rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/operators.k:47 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics/range.k:5 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-RANGE |
| semantics/range.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/range.k:7 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-ITER |
| semantics/range.k:9 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= inRange(Int, Int, Int) [function, total] |
| semantics/range.k:10 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI) |
| semantics/range.k:12 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= rangeLen(Int, Int, Int) [function] |
| semantics/range.k:13 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO |
| semantics/range.k:15 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO |
| semantics/range.k:17 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO) |
| semantics/range.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST) |
| semantics/range.k:23 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST) |
| semantics/range.k:25 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/set.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-SET |
| semantics/set.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/set.k:8 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= setV(IntSeq) |
| semantics/set.k:11 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= codeIn(Int, IntSeq) [function, total] |
| semantics/set.k:12 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule codeIn(_:Int, .IntSeq)                => false |
| semantics/set.k:13 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) |
| semantics/set.k:16 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] \| dedupFrom(IntSeq, IntSeq)  [function, total] |
| semantics/set.k:18 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq) |
| semantics/set.k:19 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC |
| semantics/set.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC) |
| semantics/set.k:22 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC) |
| semantics/set.k:25 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= snocCode(IntSeq, Int) [function, total] |
| semantics/set.k:26 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq) |
| semantics/set.k:27 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) |
| semantics/set.k:31 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total] |
| semantics/set.k:32 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule subsetCodes(.IntSeq, _:IntSeq)                => true |
| semantics/set.k:33 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B) |
| semantics/set.k:35 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total] |
| semantics/set.k:36 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) |
| semantics/set.k:39 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B) |
| semantics/set.k:40 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/sort.k:10 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-SORT |
| semantics/sort.k:11 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-BUILTINS |
| semantics/sort.k:12 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-SUBSCRIPT |
| semantics/sort.k:18 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators] |
| semantics/sort.k:19 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= insVS(Int, ValSeq) [function] |
| semantics/sort.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule sortVS(.ValSeq)                => .ValSeq          [concrete] |
| semantics/sort.k:21 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete] |
| semantics/sort.k:22 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete] |
| semantics/sort.k:23 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete] |
| semantics/sort.k:24 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete] |
| semantics/sort.k:26 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function] |
| semantics/sort.k:27 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete] |
| semantics/sort.k:28 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete] |
| semantics/sort.k:29 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete] |
| semantics/sort.k:31 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] |
| semantics/sort.k:36 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> |
| semantics/sort.k:40 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] |
| semantics/sort.k:49 | syntax | function,total,no-evaluators | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators] |
| semantics/sort.k:51 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total] |
| semantics/sort.k:53 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq) |
| semantics/sort.k:54 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule revVSAcc(.ValSeq, A:ValSeq) => A |
| semantics/sort.k:55 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A)) |
| semantics/sort.k:57 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= condRev(ValSeq, Bool) [function, total] |
| semantics/sort.k:58 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule condRev(S:ValSeq, false) => S |
| semantics/sort.k:59 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule condRev(S:ValSeq, true)  => revVS(S) |
| semantics/sort.k:61 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k> |
| semantics/sort.k:63 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k> |
| semantics/sort.k:65 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> |
| semantics/sort.k:72 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/str.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-STR |
| semantics/str.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/str.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-ITER |
| semantics/str.k:8 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k> |
| semantics/str.k:9 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> |
| semantics/str.k:13 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= strToCodes(String) [function] |
| semantics/str.k:14 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Str(S:String) => str(strToCodes(S)) ... </k> |
| semantics/str.k:15 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strToCodes("") => .IntSeq |
| semantics/str.k:16 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 |
| semantics/str.k:20 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total] |
| semantics/str.k:21 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule seqConcat(.IntSeq, T:IntSeq)                => T |
| semantics/str.k:22 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T)) |
| semantics/str.k:24 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B)) |
| semantics/str.k:25 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B |
| semantics/str.k:26 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) |
| semantics/str.k:29 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X) |
| semantics/str.k:30 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X) |
| semantics/str.k:32 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total] |
| semantics/str.k:33 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strPrefix(.IntSeq, _:IntSeq)               => true |
| semantics/str.k:34 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| semantics/str.k:35 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs) |
| semantics/str.k:37 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= strContains(IntSeq, IntSeq) [function, total] |
| semantics/str.k:38 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X) |
| semantics/str.k:39 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq) |
| semantics/str.k:40 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) |
| semantics/str.k:48 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Bool ::= strLt(IntSeq, IntSeq) [function, total] |
| semantics/str.k:49 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strLt(.IntSeq, .IntSeq)                => false |
| semantics/str.k:50 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true |
| semantics/str.k:51 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| semantics/str.k:52 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B |
| semantics/str.k:53 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B |
| semantics/str.k:54 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B |
| semantics/str.k:56 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B) |
| semantics/str.k:57 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A) |
| semantics/str.k:58 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A) |
| semantics/str.k:59 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B) |
| semantics/str.k:60 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/subscript.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-SUBSCRIPT |
| semantics/subscript.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/subscript.k:11 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= valSeqAt(ValSeq, Int) [function, total] |
| semantics/subscript.k:12 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V |
| semantics/subscript.k:13 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0 |
| semantics/subscript.k:16 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= intSeqAt(IntSeq, Int) [function] |
| semantics/subscript.k:17 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C |
| semantics/subscript.k:18 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0 |
| semantics/subscript.k:21 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= normIdx(Int, Int) [function, total] |
| semantics/subscript.k:22 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0 |
| semantics/subscript.k:23 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0 |
| semantics/subscript.k:27 | context | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | context Subscript(HOLE, _) |
| semantics/subscript.k:28 | context | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | context Subscript(_:Val, HOLE:Expr) |
| semantics/subscript.k:31 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/subscript.k:35 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k> |
| semantics/subscript.k:37 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= applyIndex(Val, Int) [function] |
| semantics/subscript.k:38 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS))) |
| semantics/subscript.k:39 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS))) |
| semantics/subscript.k:40 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) |
| semantics/subscript.k:44 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt) |
| semantics/subscript.k:49 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax OptInt ::= "noB" \| someB(Int) |
| semantics/subscript.k:50 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #evalB(NoBound)  => noB ... </k> |
| semantics/subscript.k:51 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k> |
| semantics/subscript.k:52 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> I:Int ~> #toSome => someB(I) ... </k> |
| semantics/subscript.k:54 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k> |
| semantics/subscript.k:55 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k> |
| semantics/subscript.k:56 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> |
| semantics/subscript.k:58 | rule | priority(45) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)] |
| semantics/subscript.k:61 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k> |
| semantics/subscript.k:63 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function] |
| semantics/subscript.k:64 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| semantics/subscript.k:66 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| semantics/subscript.k:68 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) |
| semantics/subscript.k:72 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= slStep(OptInt) [function, total] |
| semantics/subscript.k:73 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slStep(noB)          => 1 |
| semantics/subscript.k:74 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slStep(someB(S:Int)) => S |
| semantics/subscript.k:76 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= slStart(OptInt, OptInt, Int) [function] |
| semantics/subscript.k:77 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0 |
| semantics/subscript.k:79 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0 |
| semantics/subscript.k:81 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST)) |
| semantics/subscript.k:83 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= slStop(OptInt, OptInt, Int) [function] |
| semantics/subscript.k:84 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0 |
| semantics/subscript.k:86 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0 |
| semantics/subscript.k:88 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST)) |
| semantics/subscript.k:90 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= slAdjust(Int, Int, Int) [function, total] |
| semantics/subscript.k:91 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0 |
| semantics/subscript.k:93 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0 |
| semantics/subscript.k:96 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= clampLo(Int, Int) [function, total] |
| semantics/subscript.k:97 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0 |
| semantics/subscript.k:99 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0 |
| semantics/subscript.k:102 | syntax | function,total | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= clampHi(Int, Int, Int) [function, total] |
| semantics/subscript.k:103 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN |
| semantics/subscript.k:105 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN |
| semantics/subscript.k:109 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function] |
| semantics/subscript.k:110 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP) |
| semantics/subscript.k:113 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)) |
| semantics/subscript.k:116 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function] |
| semantics/subscript.k:117 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP) |
| semantics/subscript.k:120 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)) |
| semantics/subscript.k:122 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| semantics/syntax.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | module MPY-SYNTAX |
| semantics/syntax.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports INT-SYNTAX |
| semantics/syntax.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports FLOAT-SYNTAX |
| semantics/syntax.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports BOOL-SYNTAX |
| semantics/syntax.k:7 | imports | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | imports STRING-SYNTAX |
| semantics/syntax.k:9 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Expr ::= "Int"      "(" Int ")" \| "Float"    "(" Float ")" \| "Bool"     "(" Bool ")" \| "Name"     "(" String ")" \| "Str"      "(" String ")" \| "UnaryOp"  "(" String "," Expr ")" [strict(2)] \| "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp"    "(" String "," Exprs ")" \| "ListExpr"  "(" Exprs ")" \| "DictExpr"  "(" Entries ")" \| "ListComp"  "(" Expr "," CompFors ")" [macro] \| "GenExp"    "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda"    "(" Params "," Expr ")" \| "KwArg"     "(" String "," Expr ")" \| "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call"      "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare"   "(" Expr "," CmpOp ")" |
| semantics/syntax.k:32 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")" |
| semantics/syntax.k:33 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Entry    ::= "Entry" "(" Expr "," Expr ")" |
| semantics/syntax.k:34 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Entries  ::= List{Entry, ","} |
| semantics/syntax.k:35 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")" |
| semantics/syntax.k:36 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax CompFors ::= List{CompFor, ""} |
| semantics/syntax.k:37 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Exprs    ::= List{Expr, ","} |
| semantics/syntax.k:38 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")" |
| semantics/syntax.k:39 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Bound    ::= Expr \| "NoBound" |
| semantics/syntax.k:41 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] \| "Import"    "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While"     "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return"    "(" Expr ")" [strict] \| "Assert"    "(" Expr ")" [strict] \| "Expr"      "(" Expr ")" [strict] \| "FuncDef"   "(" String "," Params "," Stmts ")" \| "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")" |
| semantics/syntax.k:56 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Stmts      ::= List{Stmt, ""} |
| semantics/syntax.k:57 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Params     ::= "Params" "(" ParamNames ")" |
| semantics/syntax.k:58 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax CellVars   ::= "CellVars" "(" ParamNames ")" |
| semantics/syntax.k:59 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax FreeVars   ::= "FreeVars" "(" ParamNames ")" |
| semantics/syntax.k:60 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax ParamNames ::= List{String, ","} |
| semantics/syntax.k:61 | syntax | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | syntax Module     ::= "Module" "(" Stmts ")" |
| semantics/syntax.k:62 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_USED_PATH | endmodule |
| semantics/tuple.k:3 | module | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | module MPY-TUPLE |
| semantics/tuple.k:4 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-CORE |
| semantics/tuple.k:5 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-ITER |
| semantics/tuple.k:6 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-LIST |
| semantics/tuple.k:7 | imports | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | imports MPY-METHODS |
| semantics/tuple.k:10 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k> |
| semantics/tuple.k:11 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> |
| semantics/tuple.k:14 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax ApplyK ::= "toTuple" |
| semantics/tuple.k:15 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k> |
| semantics/tuple.k:16 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k> |
| semantics/tuple.k:18 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B |
| semantics/tuple.k:20 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k> |
| semantics/tuple.k:21 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> |
| semantics/tuple.k:23 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0) |
| semantics/tuple.k:24 | syntax | function | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax Int ::= idxOfVS(ValSeq, Val, Int) [function] |
| semantics/tuple.k:25 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V |
| semantics/tuple.k:26 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V) |
| semantics/tuple.k:28 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) |
| semantics/tuple.k:31 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #bindTgt(Expr, Val) |
| semantics/tuple.k:32 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes> |
| semantics/tuple.k:35 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)] |
| semantics/tuple.k:42 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| semantics/tuple.k:43 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k> |
| semantics/tuple.k:44 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/tuple.k:49 | syntax | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | syntax KItem ::= #unpackSeq(Exprs, ValSeq) |
| semantics/tuple.k:50 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| semantics/tuple.k:51 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k> |
| semantics/tuple.k:52 | rule | priority(40) | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)] |
| semantics/tuple.k:55 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k> |
| semantics/tuple.k:57 | rule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k> |
| semantics/tuple.k:58 | endmodule | - | ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH | endmodule |
| verification.k:3 | module | - | NO_PROOF_EXTENSION_IMPORT_ONLY | module FIB4-VERIFICATION |
| verification.k:4 | imports | - | NO_PROOF_EXTENSION_IMPORT_ONLY | imports MPY |
| verification.k:5 | endmodule | - | NO_PROOF_EXTENSION_IMPORT_ONLY | endmodule |
| spec.k:3 | module | - | CLAIM_REVIEWED_IN_STAGES_4_AND_6 | module FIB4-SPEC |
| spec.k:4 | imports | - | CLAIM_REVIEWED_IN_STAGES_4_AND_6 | imports FIB4-VERIFICATION |
| spec.k:9 | claim | - | CLAIM_REVIEWED_IN_STAGES_4_AND_6 | claim [loop-step]: <k> Assign( Name("next_value"), BinOp( "+", BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")), Name("d"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("c")) Assign(Name("c"), Name("d")) Assign(Name("d"), Name("next_value")) Assign(Name("i"), BinOp("+", Name("i"), Int(1))) => .K </k> <env> L:Int </env> <scopes> L \|-> scope( ( "a"          \|-> (A:Int => B) "b"          \|-> (B:Int => C) "c"          \|-> (C:Int => D) "d"          \|-> (D:Int => A +Int B +Int C +Int D) "next_value" \|-> (_E:Int => A +Int B +Int C +Int D) "i"          \|-> (I:Int => I +Int 1) ), P:Parent) </scopes> |
| spec.k:39 | claim | - | CLAIM_REVIEWED_IN_STAGES_4_AND_6 | claim [operational-cases]: <k> Assert(Compare(Call(Name("fib4"), Int(0)),  CmpOp("==", Int(0)))) Assert(Compare(Call(Name("fib4"), Int(1)),  CmpOp("==", Int(0)))) Assert(Compare(Call(Name("fib4"), Int(2)),  CmpOp("==", Int(2)))) Assert(Compare(Call(Name("fib4"), Int(3)),  CmpOp("==", Int(0)))) Assert(Compare(Call(Name("fib4"), Int(4)),  CmpOp("==", Int(2)))) Assert(Compare(Call(Name("fib4"), Int(5)),  CmpOp("==", Int(4)))) Assert(Compare(Call(Name("fib4"), Int(6)),  CmpOp("==", Int(8)))) Assert(Compare(Call(Name("fib4"), Int(7)),  CmpOp("==", Int(14)))) Assert(Compare(Call(Name("fib4"), Int(8)),  CmpOp("==", Int(28)))) Assert(Compare(Call(Name("fib4"), Int(9)),  CmpOp("==", Int(54)))) Assert(Compare(Call(Name("fib4"), Int(10)), CmpOp("==", Int(104)))) Assert(Compare(Call(Name("fib4"), Int(11)), CmpOp("==", Int(200)))) Assert(Compare(Call(Name("fib4"), Int(12)), CmpOp("==", Int(386)))) => .K </k> <env> 0 </env> <scopes> 0 \|-> scope( "fib4" \|-> closureVal( ("n", .ParamNames), If(Compare(Name("n"), CmpOp("==", Int(0))), Return(Int(0)) .Stmts, .Stmts) If(Compare(Name("n"), CmpOp("==", Int(1))), Return(Int(0)) .Stmts, .Stmts) If(Compare(Name("n"), CmpOp("==", Int(2))), Return(Int(2)) .Stmts, .Stmts) If(Compare(Name("n"), CmpOp("==", Int(3))), Return(Int(0)) .Stmts, .Stmts) Assign(Name("a"), Int(0)) Assign(Name("b"), Int(0)) Assign(Name("c"), Int(2)) Assign(Name("d"), Int(0)) Assign(Name("next_value"), Int(0)) Assign(Name("i"), Int(4)) While(Compare(Name("i"), CmpOp("<=", Name("n"))), Assign( Name("next_value"), BinOp( "+", BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")), Name("d"))) Assign(Name("a"), Name("b")) Assign(Name("b"), Name("c")) Assign(Name("c"), Name("d")) Assign(Name("d"), Name("next_value")) Assign(Name("i"), BinOp("+", Name("i"), Int(1)))) Return(Name("d")) .Stmts, 0), parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> |
| spec.k:104 | endmodule | - | CLAIM_REVIEWED_IN_STAGES_4_AND_6 | endmodule |

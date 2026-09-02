# Exhaustive K declaration and rule inventory

Generated from the trusted supplied-semantics tree plus the candidate's proof-local files. “Target-unreachable” means its LHS/sort/operator cannot occur on the submitted program's load/call path; it remains part of the fixed supplied trust boundary.

## semantics.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 34 | requires | — | ASSEMBLY | requires "semantics/syntax.k" |
| 35 | requires | — | ASSEMBLY | requires "semantics/core.k" |
| 36 | requires | — | ASSEMBLY | requires "semantics/iter.k" |
| 37 | requires | — | ASSEMBLY | requires "semantics/range.k" |
| 38 | requires | — | ASSEMBLY | requires "semantics/operators.k" |
| 39 | requires | — | ASSEMBLY | requires "semantics/int.k" |
| 40 | requires | — | ASSEMBLY | requires "semantics/bool.k" |
| 41 | requires | — | ASSEMBLY | requires "semantics/float.k" |
| 42 | requires | — | ASSEMBLY | requires "semantics/str.k" |
| 43 | requires | — | ASSEMBLY | requires "semantics/set.k" |
| 44 | requires | — | ASSEMBLY | requires "semantics/list.k" |
| 45 | requires | — | ASSEMBLY | requires "semantics/tuple.k" |
| 46 | requires | — | ASSEMBLY | requires "semantics/subscript.k" |
| 47 | requires | — | ASSEMBLY | requires "semantics/comprehension.k" |
| 48 | requires | — | ASSEMBLY | requires "semantics/methods.k" |
| 49 | requires | — | ASSEMBLY | requires "semantics/controls.k" |
| 50 | requires | — | ASSEMBLY | requires "semantics/functions.k" |
| 51 | requires | — | ASSEMBLY | requires "semantics/builtins.k" |
| 52 | requires | — | ASSEMBLY | requires "semantics/call.k" |
| 53 | requires | — | ASSEMBLY | requires "semantics/sort.k" |
| 54 | requires | — | ASSEMBLY | requires "semantics/assert.k" |
| 55 | requires | — | ASSEMBLY | requires "semantics/dict.k" |
| 56 | requires | concrete | ASSEMBLY | requires "semantics/concrete.k" |
| 58 | module | — | ASSEMBLY | module MPY |
| 59 | imports | — | ASSEMBLY | imports MPY-CORE |
| 60 | imports | — | ASSEMBLY | imports MPY-ITER |
| 61 | imports | — | ASSEMBLY | imports MPY-RANGE |
| 62 | imports | — | ASSEMBLY | imports MPY-OPERATORS |
| 63 | imports | — | ASSEMBLY | imports MPY-INT |
| 64 | imports | — | ASSEMBLY | imports MPY-BOOL |
| 65 | imports | — | ASSEMBLY | imports MPY-FLOAT |
| 66 | imports | — | ASSEMBLY | imports MPY-STR |
| 67 | imports | — | ASSEMBLY | imports MPY-SET |
| 68 | imports | — | ASSEMBLY | imports MPY-LIST |
| 69 | imports | — | ASSEMBLY | imports MPY-TUPLE |
| 70 | imports | — | ASSEMBLY | imports MPY-SUBSCRIPT |
| 71 | imports | — | ASSEMBLY | imports MPY-COMPREHENSION |
| 72 | imports | — | ASSEMBLY | imports MPY-METHODS |
| 73 | imports | — | ASSEMBLY | imports MPY-CONTROLS |
| 74 | imports | — | ASSEMBLY | imports MPY-FUNCTIONS |
| 75 | imports | — | ASSEMBLY | imports MPY-BUILTINS |
| 76 | imports | — | ASSEMBLY | imports MPY-CALL |
| 77 | imports | — | ASSEMBLY | imports MPY-SORT |
| 78 | imports | — | ASSEMBLY | imports MPY-ASSERT |
| 79 | imports | — | ASSEMBLY | imports MPY-DICT |
| 80 | endmodule | — | ASSEMBLY | endmodule |
| 87 | module | — | ASSEMBLY | module MPY-KRUN |
| 88 | imports | — | ASSEMBLY | imports MPY |
| 89 | imports | — | ASSEMBLY | imports MPY-CONCRETE |
| 90 | endmodule | — | ASSEMBLY | endmodule |

## semantics/assert.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-ASSERT |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 6-7 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Assert(V:Val) => .K ... </k> requires truthy(V) |
| 8-11 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V) |
| 13-15 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 16 | endmodule | — | ASSEMBLY | endmodule |

## semantics/bool.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 5 | module | — | ASSEMBLY | module MPY-BOOL |
| 6 | imports | — | ASSEMBLY | imports MPY-CORE |
| 8 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyUn("not", V:Val) => notBool truthy(V) |
| 10 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2 |
| 11 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2 |
| 16 | context | — | FIXED-SUPPLIED—target-unreachable | context BoolOp(_, (HOLE:Expr, _:Exprs)) |
| 17 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k> |
| 18-19 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V) |
| 20-21 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V) |
| 22-23 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V) |
| 24-25 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V) |
| 29-30 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)] |
| 31-34 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires truthy(V) [priority(40)] |
| 35-38 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool truthy(V) [priority(40)] |
| 39-42 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires truthy(V) [priority(40)] |
| 43-46 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool truthy(V) [priority(40)] |
| 47 | endmodule | — | ASSEMBLY | endmodule |

## semantics/builtins.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-BUILTINS |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 5 | imports | — | ASSEMBLY | imports MPY-STR |
| 6 | imports | — | ASSEMBLY | imports MPY-SET |
| 7 | imports | — | ASSEMBLY | imports MPY-ITER |
| 8 | imports | — | ASSEMBLY | imports MPY-RANGE |
| 9 | imports | — | ASSEMBLY | imports MPY-INT |
| 10 | imports | — | ASSEMBLY | imports MPY-METHODS |
| 17 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Val ::= applyBuiltin(String, Vals) [function] |
| 20 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= seqLen(Val) [function] |
| 21 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ) |
| 22 | rule | — | FIXED-SUPPLIED—target-unreachable | rule seqLen(list(VS:ValSeq))                  => vsLen(VS) |
| 23 | rule | — | FIXED-SUPPLIED—target-unreachable | rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS) |
| 24 | rule | — | FIXED-SUPPLIED—target-unreachable | rule seqLen(str(IS:IntSeq))                   => isLen(IS) |
| 25 | rule | — | FIXED-SUPPLIED—target-unreachable | rule seqLen(setV(DS:IntSeq))                  => isLen(DS) |
| 26 | rule | — | FIXED-SUPPLIED—target-unreachable | rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST) |
| 32 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k> |
| 33 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k> |
| 34 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k> |
| 35 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k> |
| 36 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= charsOf(IntSeq) [function, total] |
| 37 | rule | — | FIXED-SUPPLIED—target-unreachable | rule charsOf(.IntSeq)                => .ValSeq |
| 38 | rule | — | FIXED-SUPPLIED—target-unreachable | rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R)) |
| 41 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS)) |
| 44 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("abs", I:Int, .Vals) => absInt(I) |
| 47 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #sumAcc(Iterable, Int) &#124; #sumCont(Int) |
| 48 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k> |
| 49 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k> |
| 50-52 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V) |
| 54 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= intOf(Val) [function] |
| 55 | rule | — | FIXED-SUPPLIED—target-unreachable | rule intOf(I:Int)  => I |
| 56 | rule | — | FIXED-SUPPLIED—target-unreachable | rule intOf(B:Bool) => #if B #then 1 #else 0 #fi |
| 59 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #allAcc(Iterable) &#124; "#allCont" |
| 60 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k> |
| 61 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #allCont => true ... </k> |
| 62-63 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V) |
| 64-65 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V) |
| 67 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #anyAcc(Iterable) &#124; "#anyCont" |
| 68 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k> |
| 69 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #anyCont => false ... </k> |
| 70-71 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V) |
| 72-73 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V) |
| 76 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #maxAcc0(Iterable) &#124; "#maxCont0" &#124; #maxAcc(Iterable, Int) &#124; #maxCont(Int) |
| 77 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k> |
| 78-79 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V) |
| 80 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k> |
| 81 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k> |
| 82-84 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V) |
| 86 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #minAcc0(Iterable) &#124; "#minCont0" &#124; #minAcc(Iterable, Int) &#124; #minCont(Int) |
| 87 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k> |
| 88-89 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V) |
| 90 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k> |
| 91 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #minCont(M:Int) => M ... </k> |
| 92-94 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V) |
| 97 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= maxVals(Int, Vals) [function] |
| 98 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST) |
| 99 | rule | — | FIXED-SUPPLIED—target-unreachable | rule maxVals(M:Int, .Vals)           => M |
| 100 | rule | — | FIXED-SUPPLIED—target-unreachable | rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R) |
| 102 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= minVals(Int, Vals) [function] |
| 103 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST) |
| 104 | rule | — | FIXED-SUPPLIED—target-unreachable | rule minVals(M:Int, .Vals)           => M |
| 105 | rule | — | FIXED-SUPPLIED—target-unreachable | rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R) |
| 108-109 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0 |
| 111-113 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0 |
| 114 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= binCodes(Int) [function, total] |
| 115 | rule | — | FIXED-SUPPLIED—target-unreachable | rule binCodes(0) => iCons(48, .IntSeq) |
| 116 | rule | — | FIXED-SUPPLIED—target-unreachable | rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0 |
| 117 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= binAcc(Int, IntSeq) [function, total] |
| 118 | rule | — | FIXED-SUPPLIED—target-unreachable | rule binAcc(0, ACC:IntSeq) => ACC |
| 119-121 | rule | — | FIXED-SUPPLIED—target-unreachable | rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0 |
| 124-125 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k> |
| 126 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= enumVS(ValSeq, Int) [function, total] |
| 127 | rule | — | FIXED-SUPPLIED—target-unreachable | rule enumVS(.ValSeq, _:Int) => .ValSeq |
| 128-129 | rule | — | FIXED-SUPPLIED—target-unreachable | rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1)) |
| 132-133 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k> |
| 134 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= mapStrVS(ValSeq) [function, total] |
| 135 | rule | — | FIXED-SUPPLIED—target-unreachable | rule mapStrVS(.ValSeq) => .ValSeq |
| 136 | rule | — | FIXED-SUPPLIED—target-unreachable | rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R)) |
| 137 | rule | — | FIXED-SUPPLIED—target-unreachable | rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R)) |
| 140 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("int", I:Int, .Vals) => I |
| 143 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C |
| 144-145 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128 |
| 148 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I))) |
| 149 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS) |
| 152-153 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57 |
| 156-157 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2 |
| 158 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= intDigAcc(IntSeq, Int) [function, total] |
| 159 | rule | — | FIXED-SUPPLIED—target-unreachable | rule intDigAcc(.IntSeq, ACC:Int)             => ACC |
| 160 | rule | — | FIXED-SUPPLIED—target-unreachable | rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48)) |
| 163 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B) |
| 164 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B) |
| 167-168 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k> |
| 169 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k> |
| 170 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k> |
| 171-172 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k> |
| 173 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k> |
| 174 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k> |
| 177 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1) |
| 178 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1) |
| 179-180 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0 |
| 187 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS) |
| 188 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= evalArith(IntSeq) [function] |
| 189-190 | rule | — | FIXED-SUPPLIED—target-unreachable | rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS))))) |
| 192 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax OpSeq ::= ".OpSeq" &#124; oCons(String, OpSeq) |
| 194 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= evDigit(Int) [function, total] |
| 195 | rule | — | FIXED-SUPPLIED—target-unreachable | rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57 |
| 196 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= evHead42(IntSeq) [function, total] |
| 197 | rule | — | FIXED-SUPPLIED—target-unreachable | rule evHead42(iCons(42, _:IntSeq)) => true |
| 198 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule evHead42(_:IntSeq)            => false [owise] |
| 199 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= evHead47(IntSeq) [function, total] |
| 200 | rule | — | FIXED-SUPPLIED—target-unreachable | rule evHead47(iCons(47, _:IntSeq)) => true |
| 201 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule evHead47(_:IntSeq)            => false [owise] |
| 203 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax OpSeq ::= tokOps(IntSeq) [function, total] |
| 204 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokOps(.IntSeq)                 => .OpSeq |
| 205 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokOps(iCons(32, R:IntSeq))     => tokOps(R) |
| 206 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C) |
| 207 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R)) |
| 208 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R) |
| 209 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R)) |
| 210 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R) |
| 211 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R)) |
| 212 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R)) |
| 214-215 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= tokNds(IntSeq) [function, total] &#124; tokNdAcc(Int, IntSeq) [function, total] |
| 216 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokNds(.IntSeq)                => .IntSeq |
| 217 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokNds(iCons(32, R:IntSeq))    => tokNds(R) |
| 218 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C) |
| 219-220 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32 |
| 221-222 | rule | — | FIXED-SUPPLIED—target-unreachable | rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C) |
| 223 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise] |
| 225 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax EvPair ::= evp(OpSeq, IntSeq) |
| 226 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= firstNdE(EvPair) [function, total] |
| 227 | rule | — | FIXED-SUPPLIED—target-unreachable | rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N |
| 228 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule firstNdE(_:EvPair) => 0 [owise] |
| 230 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= applyOpE(String, Int, Int) [function, total] |
| 231 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyOpE("+",  A:Int, B:Int) => A +Int B |
| 232 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyOpE("-",  A:Int, B:Int) => A -Int B |
| 233 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyOpE("*",  A:Int, B:Int) => A *Int B |
| 234 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyOpE("//", A:Int, B:Int) => A divInt B |
| 235 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyOpE("**", A:Int, B:Int) => A ^Int B |
| 236 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule applyOpE(_:String, A:Int, _:Int) => A [owise] |
| 238 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total] |
| 239 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS) |
| 240 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS)) |
| 241-242 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**" |
| 243 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise] |
| 244 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax EvPair ::= powCombE(Int, EvPair) [function, total] |
| 245 | rule | — | FIXED-SUPPLIED—target-unreachable | rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST)) |
| 246 | rule | — | FIXED-SUPPLIED—target-unreachable | rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq)) |
| 247 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total] |
| 248 | rule | — | FIXED-SUPPLIED—target-unreachable | rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS)) |
| 250 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax EvPair ::= passMulE(EvPair) [function, total] &#124; passAddE(EvPair) [function, total] |
| 251 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq) |
| 252 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq) |
| 253 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq) |
| 254 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq) |
| 255 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total] |
| 256 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) |
| 257-259 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O) |
| 260-262 | rule | — | FIXED-SUPPLIED—target-unreachable | rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O) |
| 263-264 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise] |
| 265 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= inLevelE(String, String) [function, total] |
| 266 | rule | — | FIXED-SUPPLIED—target-unreachable | rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/" |
| 267 | rule | — | FIXED-SUPPLIED—target-unreachable | rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-" |
| 268 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule inLevelE(_:String, _:String) => false [owise] |
| 269 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax OpSeq ::= appendOpE(OpSeq, String) [function, total] |
| 270 | rule | — | FIXED-SUPPLIED—target-unreachable | rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq) |
| 271 | rule | — | FIXED-SUPPLIED—target-unreachable | rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O)) |
| 272 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= appendIE(IntSeq, Int) [function, total] |
| 273 | rule | — | FIXED-SUPPLIED—target-unreachable | rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq) |
| 274 | rule | — | FIXED-SUPPLIED—target-unreachable | rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N)) |
| 279 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= "#md5" |
| 280-281 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)] |
| 282 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k> |
| 283 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Val ::= md5Obj(IntSeq) |
| 284 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS)) |
| 285 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators] |
| 291 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V) |
| 292 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V) |
| 293 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isIntV(Val) [function] &#124; isStrV(Val) [function] |
| 294 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isIntV(_:Int)         => true |
| 295 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule isIntV(_:Val)         => false [owise] |
| 296 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isStrV(str(_:IntSeq)) => true |
| 297 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule isStrV(_:Val)         => false [owise] |
| 298 | endmodule | — | ASSEMBLY | endmodule |

## semantics/call.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 10 | module | — | ASSEMBLY | module MPY-CALL |
| 11 | imports | — | ASSEMBLY | imports MPY-METHODS |
| 12 | imports | — | ASSEMBLY | imports MPY-BUILTINS |
| 13 | imports | — | ASSEMBLY | imports MPY-FUNCTIONS |
| 16 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k> |
| 19 | syntax | — | FIXED-SUPPLIED—target/load path | syntax KItem ::= #callee(Exprs) |
| 20 | rule | owise | FIXED-SUPPLIED—target/load path | rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise] |
| 21 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k> |
| 24 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k> |
| 26 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k> |
| 27 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k> |
| 28 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k> |
| 29 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k> |
| 30 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k> |
| 31 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise] |
| 32 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k> |
| 38-41 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 42-46 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)] |
| 47-50 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 52 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isMutMethod(String) [function, total] |
| 53-55 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove" |
| 56-60 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)] |
| 63-67 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)] |
| 69-74 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> |
| 80-85 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack> |
| 87 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #allocCells(ParamNames) |
| 88 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #allocCells(.ParamNames) => .K ... </k> |
| 89-94 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N &#124;-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) |
| 95 | endmodule | — | ASSEMBLY | endmodule |

## semantics/comprehension.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-COMPREHENSION |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 5 | imports | — | ASSEMBLY | imports MPY-OPERATORS |
| 6 | imports | — | ASSEMBLY | imports MPY-LIST |
| 7 | imports | — | ASSEMBLY | imports MPY-CONTROLS |
| 8 | imports | — | ASSEMBLY | imports MPY-FUNCTIONS |
| 11 | rule | — | FIXED-SUPPLIED—target-unreachable | rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| 12 | rule | — | FIXED-SUPPLIED—target-unreachable | rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs) |
| 14 | syntax | macro | FIXED-SUPPLIED—target-unreachable | syntax Stmts ::= compBody(CompFors, Expr) [macro] |
| 15-16 | rule | — | FIXED-SUPPLIED—target-unreachable | rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc")) |
| 18 | syntax | macro-rec, macro | FIXED-SUPPLIED—target-unreachable | syntax Stmt ::= compNest(CompFors, Expr) [macro-rec] |
| 19-20 | rule | — | FIXED-SUPPLIED—target-unreachable | rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT))) |
| 21-22 | rule | — | FIXED-SUPPLIED—target-unreachable | rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts)) |
| 24 | syntax | macro | FIXED-SUPPLIED—target-unreachable | syntax Expr ::= compGuard(Exprs) [macro] |
| 25 | rule | — | FIXED-SUPPLIED—target-unreachable | rule compGuard(.Exprs)             => Bool(true) |
| 26 | rule | — | FIXED-SUPPLIED—target-unreachable | rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs)) |
| 27 | endmodule | — | ASSEMBLY | endmodule |

## semantics/concrete.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 8 | module | — | ASSEMBLY | module MPY-CONCRETE |
| 9 | imports | — | ASSEMBLY | imports MPY |
| 13-15 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) |
| 16-18 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B) |
| 25 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Val ::= kvP(Val, Val) |
| 26-27 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) &#124; #ksIns(Val, ValSeq, Val, ValSeq, Bool) |
| 28-30 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)] |
| 31-33 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)] |
| 34-35 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k> |
| 36-37 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k> |
| 38-40 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K) |
| 42 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= insPair(ValSeq, Val, Val) [function] |
| 43 | rule | — | FIXED-SUPPLIED—target-unreachable | rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq) |
| 44-46 | rule | — | FIXED-SUPPLIED—target-unreachable | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2) |
| 47-49 | rule | — | FIXED-SUPPLIED—target-unreachable | rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2) |
| 51 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= kLt(Val, Val) [function] |
| 52 | rule | — | FIXED-SUPPLIED—target-unreachable | rule kLt(I1:Int, I2:Int)             => I1 <Int I2 |
| 53 | rule | — | FIXED-SUPPLIED—target-unreachable | rule kLt(F1:Float, F2:Float)         => F1 <Float F2 |
| 54 | rule | — | FIXED-SUPPLIED—target-unreachable | rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B) |
| 56 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= unpairVS(ValSeq) [function, total] |
| 57 | rule | — | FIXED-SUPPLIED—target-unreachable | rule unpairVS(.ValSeq) => .ValSeq |
| 58 | rule | — | FIXED-SUPPLIED—target-unreachable | rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R)) |
| 59 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise] |
| 60 | endmodule | — | ASSEMBLY | endmodule |

## semantics/controls.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-CONTROLS |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 5 | imports | — | ASSEMBLY | imports MPY-TUPLE |
| 6 | imports | — | ASSEMBLY | imports MPY-ITER |
| 9-11 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ X <- V ], _) ... </scopes> |
| 12-18 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)] |
| 20-23 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M) |
| 27-31 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)] |
| 35 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k> |
| 36 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise] |
| 37 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #bindImports(ParamNames) |
| 38 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #bindImports(.ParamNames) => .K ... </k> |
| 39-42 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil" |
| 43-44 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil") |
| 48 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Expr(_:Val) => .K ... </k> |
| 51 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #branch(Bool, Stmts, Stmts) |
| 52 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k> |
| 53 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k> |
| 54 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k> |
| 57-58 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V) |
| 59-60 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V) |
| 65-67 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #loop(Val, Expr, Stmts) &#124; #loopStep(Expr, Stmts) &#124; #while(Expr, Stmts) &#124; #whileCond(Expr, Stmts) &#124; #loopLbl(K) &#124; "#cont" &#124; "#brk" |
| 69 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k> |
| 71 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k> |
| 72 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k> |
| 73-74 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k> |
| 77 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k> |
| 78 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k> |
| 79-80 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V) |
| 81-82 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V) |
| 85 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #loopLbl(NEXT:K) => NEXT ... </k> |
| 86 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Continue => #cont ... </k> |
| 87 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Break => #brk ... </k> |
| 88 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k> |
| 89 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule <k> #cont ~> (_:KItem => .K) ... </k> [owise] |
| 90 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #brk ~> #loopLbl(_:K) => .K ... </k> |
| 91 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule <k> #brk ~> (_:KItem => .K) ... </k> [owise] |
| 95-97 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 98-100 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 101-103 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 106-108 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 109 | endmodule | — | ASSEMBLY | endmodule |

## semantics/core.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-CORE |
| 4 | imports | — | ASSEMBLY | imports MPY-SYNTAX |
| 5 | imports | — | ASSEMBLY | imports INT |
| 6 | imports | — | ASSEMBLY | imports BOOL |
| 7 | imports | — | ASSEMBLY | imports STRING |
| 8 | imports | — | ASSEMBLY | imports MAP |
| 9 | imports | — | ASSEMBLY | imports LIST |
| 10 | imports | — | ASSEMBLY | imports K-EQUAL |
| 13 | syntax | — | FIXED-SUPPLIED—target/load path | syntax IntSeq ::= ".IntSeq" &#124; iCons(Int, IntSeq) |
| 14 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= ".ValSeq" &#124; vCons(Val, ValSeq) |
| 15 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Str    ::= str(IntSeq) |
| 18-23 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Iterable ::= list(ValSeq) &#124; tuple(ValSeq) &#124; Str &#124; rangeObj(Int, Int, Int) &#124; zipObj(ValSeq, ValSeq) &#124; zipObjS(IntSeq, IntSeq) |
| 25-34 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Val      ::= Int &#124; Bool &#124; "noneV" &#124; Iterable &#124; ref(Int) &#124; cellRef(Int) &#124; closureVal(ParamNames, Stmts, Int) &#124; typeV(String) &#124; builtinV(String) &#124; boundMethodV(Val, String) |
| 36 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Parent   ::= "root" &#124; parent(Int) |
| 37 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Scope    ::= scope(Map, Parent) |
| 38 | syntax | — | FIXED-SUPPLIED—target/load path | syntax KResult  ::= Val |
| 39 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Expr     ::= Val |
| 40 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Vals     ::= List{Val, ","} |
| 41 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Exc      ::= "NoExc" &#124; "AssertionError" |
| 42 | syntax | — | FIXED-SUPPLIED—target/load path | syntax RetState ::= "noRet" &#124; retV(Val) |
| 49-60 | configuration | — | FIXED-SUPPLIED—target/load path | configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     &#124;-> scope(.Map, parent(-1)) -1    &#124;-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code> |
| 68 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isRefV(Val) [function, total] |
| 69 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isRefV(ref(_:Int)) => true |
| 70 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule isRefV(_:Val)      => false [owise] |
| 75 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax HeapVal ::= cellV(Val) |
| 76 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isCellRef(Val) [function, total] |
| 77 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isCellRef(cellRef(_:Int)) => true |
| 78 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule isCellRef(_:Val)          => false [owise] |
| 85-90 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> <heap> ... H &#124;-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)] |
| 95 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Val ::= kwV(String, Val) |
| 96 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #kwTag(String) |
| 97 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k> |
| 98-99 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V) |
| 100 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isKwV(Val) [function, total] |
| 101 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isKwV(kwV(_:String, _:Val)) => true |
| 102 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule isKwV(_:Val)                => false [owise] |
| 106 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Val ::= cellsMark(ParamNames) |
| 107 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax ParamNames ::= cellsOf(Val) [function] |
| 108 | rule | — | FIXED-SUPPLIED—target-unreachable | rule cellsOf(cellsMark(CVS:ParamNames)) => CVS |
| 109 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= pnMember(String, ParamNames) [function, total] |
| 110 | rule | — | FIXED-SUPPLIED—target-unreachable | rule pnMember(_:String, .ParamNames) => false |
| 111 | rule | — | FIXED-SUPPLIED—target-unreachable | rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R) |
| 113 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #cellW(Val, Val) |
| 114-115 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H &#124;-> cellV(_:Val => V) ... </heap> |
| 117 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #alloc(Val) |
| 118-121 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N &#124;-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H) |
| 124 | syntax | — | FIXED-SUPPLIED—target/load path | syntax KItem ::= #loadAll(Module) |
| 125 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k> |
| 126 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k> |
| 127 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> .Stmts => .K ... </k> |
| 130 | syntax | — | FIXED-SUPPLIED—target/load path | syntax KItem ::= #look(String, Int) |
| 131 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env> |
| 132-134 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L &#124;-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M) |
| 145-151 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L &#124;-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H &#124;-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)] |
| 152-154 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L &#124;-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M)) |
| 157 | syntax | function, total | FIXED-SUPPLIED—target/load path | syntax Scope ::= "builtinsScope" [function, total] |
| 158-181 | rule | — | FIXED-SUPPLIED—target/load path | rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root) |
| 185 | syntax | — | FIXED-SUPPLIED—target/load path | syntax ApplyK ::= toCall(Val) |
| 186-188 | syntax | — | FIXED-SUPPLIED—target/load path | syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) &#124; #evalArgCont(Exprs, Vals, ApplyK) &#124; #applyK(ApplyK, Vals) |
| 189 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k> |
| 190 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k> |
| 191 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k> |
| 194 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> Int(I:Int)   => I ... </k> |
| 195 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Bool(B:Bool) => B ... </k> |
| 196 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> NoneVal      => noneV ... </k> |
| 199 | syntax | function | FIXED-SUPPLIED—target/load path | syntax Bool ::= truthy(Val) [function] |
| 200 | rule | — | FIXED-SUPPLIED—target-unreachable | rule truthy(B:Bool)          => B |
| 201 | rule | — | FIXED-SUPPLIED—target-unreachable | rule truthy(noneV)           => false |
| 202 | rule | — | FIXED-SUPPLIED—target-unreachable | rule truthy(I:Int)           => I =/=Int 0 |
| 203 | rule | — | FIXED-SUPPLIED—target/load path | rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq) |
| 204 | rule | — | FIXED-SUPPLIED—target-unreachable | rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq) |
| 205 | rule | — | FIXED-SUPPLIED—target-unreachable | rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq) |
| 208 | syntax | function | FIXED-SUPPLIED—target/load path | syntax Val  ::= applyUn(String, Val) [function] |
| 209 | syntax | function | FIXED-SUPPLIED—target/load path | syntax Val  ::= applyBin(String, Val, Val) [function] |
| 210 | syntax | function | FIXED-SUPPLIED—target/load path | syntax Bool ::= applyCmp(String, Val, Val) [function] |
| 213 | syntax | function, total | FIXED-SUPPLIED—target/load path | syntax Vals ::= appendVal(Vals, Val) [function, total] |
| 214 | rule | — | FIXED-SUPPLIED—target/load path | rule appendVal(.Vals, V:Val)              => V , .Vals |
| 215 | rule | — | FIXED-SUPPLIED—target/load path | rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V) |
| 217 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= vals2valSeq(Vals) [function, total] |
| 218 | rule | — | FIXED-SUPPLIED—target-unreachable | rule vals2valSeq(.Vals)            => .ValSeq |
| 219 | rule | — | FIXED-SUPPLIED—target-unreachable | rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS)) |
| 223 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= vsLen(ValSeq) [function, total] |
| 224 | rule | — | FIXED-SUPPLIED—target-unreachable | rule vsLen(.ValSeq)                => 0 |
| 225 | rule | — | FIXED-SUPPLIED—target-unreachable | rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S) |
| 227 | syntax | function, total | FIXED-SUPPLIED—target/load path | syntax Int ::= isLen(IntSeq) [function, total] |
| 228 | rule | — | FIXED-SUPPLIED—target/load path | rule isLen(.IntSeq)                => 0 |
| 229 | rule | — | FIXED-SUPPLIED—target/load path | rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S) |
| 233 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total] |
| 234 | rule | — | FIXED-SUPPLIED—target-unreachable | rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq |
| 235 | rule | — | FIXED-SUPPLIED—target-unreachable | rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S) |
| 236-237 | rule | — | FIXED-SUPPLIED—target-unreachable | rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0 |
| 238-239 | rule | — | FIXED-SUPPLIED—target-unreachable | rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0 |
| 240 | endmodule | — | ASSEMBLY | endmodule |

## semantics/dict.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 13 | module | — | ASSEMBLY | module MPY-DICT |
| 14 | imports | — | ASSEMBLY | imports MPY-CORE |
| 15 | imports | — | ASSEMBLY | imports MPY-ITER |
| 16 | imports | — | ASSEMBLY | imports MPY-METHODS |
| 17 | imports | — | ASSEMBLY | imports MPY-LIST |
| 20 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Val ::= dictV(ValSeq, ValSeq) |
| 23-25 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) &#124; #dictKey(Expr, Entries, ValSeq, ValSeq) &#124; #dictVal(Val, Entries, ValSeq, ValSeq) |
| 26 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k> |
| 27 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k> |
| 28-29 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k> |
| 30-31 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k> |
| 32-33 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k> |
| 37 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= dHasKey(ValSeq, Val) [function, total] |
| 38 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dHasKey(.ValSeq, _:Val)                => false |
| 39 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K |
| 40 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K) |
| 43 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= dPutK(ValSeq, Val) [function, total] |
| 44 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K) |
| 45 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K) |
| 49 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total] |
| 50-51 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K |
| 52-53 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K) |
| 54 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise] |
| 58-60 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)] |
| 63 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K) |
| 64 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Val ::= applyIndexD(Val, Val) [function] |
| 65-66 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)] |
| 70 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Val ::= dictSet(Val, Val, Val) [function] |
| 71 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V)) |
| 76 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #dsetK(String, Val) |
| 77 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k> |
| 78-81 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val) |
| 82-85 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) |
| 86 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #dsetV(Val, Val, Val) |
| 87-88 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H &#124;-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap> |
| 90 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= normIdxD(Int, Int) [function, total] |
| 91 | rule | — | FIXED-SUPPLIED—target-unreachable | rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0 |
| 92 | rule | — | FIXED-SUPPLIED—target-unreachable | rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0 |
| 95-96 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2) |
| 97 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function] |
| 98 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true |
| 99-100 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2) |
| 101 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Val ::= dGet(ValSeq, ValSeq, Val) [function] |
| 102 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K |
| 103 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K) |
| 104 | endmodule | — | ASSEMBLY | endmodule |

## semantics/float.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 14 | module | — | ASSEMBLY | module MPY-FLOAT |
| 15 | imports | — | ASSEMBLY | imports MPY-OPERATORS |
| 16 | imports | — | ASSEMBLY | imports MPY-BUILTINS |
| 17 | imports | — | ASSEMBLY | imports FLOAT |
| 20 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Val ::= Float |
| 21 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Float(F:Float) => F ... </k> |
| 24 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators] |
| 25 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete] |
| 27 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F) |
| 30 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators] |
| 31 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete] |
| 32 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2) |
| 37 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators] |
| 38 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete] |
| 39 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2) |
| 43 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2 |
| 44 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2) |
| 50 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators] |
| 51 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete] |
| 52 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2) |
| 54 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators] |
| 55 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule absF(F:Float) => absFloat(F) [concrete] |
| 56 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("abs", F:Float, .Vals) => absF(F) |
| 61 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Import(_:String) => .K ... </k> |
| 65 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= "#mathCeil" |
| 66 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)] |
| 67 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k> |
| 70 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= "#mathFloor" |
| 71 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)] |
| 72 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k> |
| 73 | syntax | function, total, symbol | FIXED-SUPPLIED—target-unreachable | syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)] |
| 74 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule floorFI(I:Int)   => I                        [concrete] |
| 75 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete] |
| 78 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V) |
| 79 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V) |
| 82 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #mathPow1(Expr) &#124; #mathPow2(Val) |
| 83 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)] |
| 84 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k> |
| 85 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k> |
| 86 | syntax | function, total, symbol | FIXED-SUPPLIED—target-unreachable | syntax Float ::= toF(Val) [function, total, symbol(toF)] |
| 87 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule toF(F:Float) => F        [concrete] |
| 88 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule toF(I:Int)   => intToF(I) [concrete] |
| 93 | syntax | function, total, symbol | FIXED-SUPPLIED—target-unreachable | syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)] |
| 94 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule ceilF(I:Int)   => I                       [concrete] |
| 95 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete] |
| 99 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyUn("-", F:Float) => 0.0 -Float F |
| 103 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators] |
| 104 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete] |
| 105 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2) |
| 107 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators] |
| 108 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete] |
| 109 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2) |
| 111 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators] |
| 112 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete] |
| 113 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2) |
| 115 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators] |
| 116 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete] |
| 117 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2) |
| 119 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators] |
| 120 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete] |
| 121 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2) |
| 125 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators] |
| 126 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete] |
| 127 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2) |
| 128 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2) |
| 129 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2) |
| 132 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F) |
| 133 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I)) |
| 134 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F) |
| 135 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I)) |
| 136 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F) |
| 137 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I)) |
| 138 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F) |
| 139 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I)) |
| 142 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators] |
| 143 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete] |
| 144 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F) |
| 145 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I)) |
| 146 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F) |
| 147 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I)) |
| 148 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F) |
| 149 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I)) |
| 150 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F) |
| 151 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I)) |
| 154 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", V:Val, noneV) => V ==K noneV |
| 155 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV) |
| 160 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators] |
| 161 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete] |
| 162-164 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete] |
| 165 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= headIS(IntSeq) [function] |
| 166 | rule | — | FIXED-SUPPLIED—target-unreachable | rule headIS(iCons(C:Int, _:IntSeq)) => C |
| 167 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= intPart(IntSeq) [function, total] &#124; intPartAcc(IntSeq, Int) [function, total] |
| 168 | rule | — | FIXED-SUPPLIED—target-unreachable | rule intPart(CS:IntSeq) => intPartAcc(CS, 0) |
| 169 | rule | — | FIXED-SUPPLIED—target-unreachable | rule intPartAcc(.IntSeq, A:Int) => A |
| 170 | rule | — | FIXED-SUPPLIED—target-unreachable | rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A |
| 171-172 | rule | — | FIXED-SUPPLIED—target-unreachable | rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46 |
| 173 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= fracPart(IntSeq) [function, total] &#124; fracAcc(IntSeq, Int) [function, total] |
| 174 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fracPart(.IntSeq) => 0 |
| 175 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0) |
| 176 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46 |
| 177 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fracAcc(.IntSeq, A:Int) => A |
| 178 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48)) |
| 179 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= fracScale(IntSeq) [function, total] &#124; fscAcc(IntSeq, Int) [function, total] |
| 180 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fracScale(.IntSeq) => 1 |
| 181 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1) |
| 182 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46 |
| 183 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fscAcc(.IntSeq, A:Int) => A |
| 184 | rule | — | FIXED-SUPPLIED—target-unreachable | rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10) |
| 185 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS) |
| 186 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("float", I:Int, .Vals)          => intToF(I) |
| 187 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("float", F:Float, .Vals)        => F |
| 190 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators] |
| 191 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete] |
| 192 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I) |
| 195 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators] |
| 196 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete] |
| 197 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F) |
| 198 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I)) |
| 199 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F) |
| 200 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I)) |
| 201 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F) |
| 202 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I)) |
| 203 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F) |
| 204 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I)) |
| 205 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F) |
| 206 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I)) |
| 209 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators] |
| 210 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete] |
| 211 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("int", F:Float, .Vals) => truncF(F) |
| 213 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("float", I:Int, .Vals)   => intToF(I) |
| 214 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("float", F:Float, .Vals) => F |
| 217 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators] |
| 218-222 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete] |
| 223 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators] |
| 224-226 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete] |
| 227 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("round", F:Float, .Vals)        => roundF(F) |
| 228 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N) |
| 230 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators] |
| 231 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule sqrtF(F:Float) => sqrtFloat(F) [concrete] |
| 232 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= "#mathSqrt" |
| 233 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)] |
| 234 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k> |
| 235 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k> |
| 243 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #maxAccF(Iterable, Float) &#124; #maxContF(Float) |
| 244 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V) |
| 245 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k> |
| 246 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k> |
| 247-248 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V) |
| 250 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #minAccF(Iterable, Float) &#124; #minContF(Float) |
| 251 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V) |
| 252 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k> |
| 253 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #minContF(M:Float) => M ... </k> |
| 254-255 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V) |
| 261 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #sumAccF(Iterable, Float) &#124; #sumContF(Float) |
| 262-264 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V)) |
| 265 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k> |
| 266 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k> |
| 267-269 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V) |
| 270-272 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V) |
| 273 | endmodule | — | ASSEMBLY | endmodule |

## semantics/functions.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-FUNCTIONS |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 8-11 | syntax | — | FIXED-SUPPLIED—target/load path | syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) &#124; #bindP(ParamNames, Vals) &#124; "#pop" &#124; "#endcall" |
| 14-16 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes> |
| 18 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Expr ::= closureExpr(ParamNames, Stmts) |
| 19-20 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env> |
| 27 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map) |
| 31-32 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) &#124; #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map) |
| 33-35 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k> |
| 36-41 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires FV in_keys(M) |
| 42-45 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes> |
| 47-49 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env> |
| 50-52 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k> |
| 53-58 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires FV in_keys(M) |
| 59-60 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k> |
| 63 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #bindP(.ParamNames, .Vals) => .K ... </k> |
| 64-66 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ P <- V ], _) ... </scopes> |
| 68-75 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)] |
| 78-79 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret> |
| 80-81 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret> |
| 85-90 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc> |
| 91 | endmodule | — | ASSEMBLY | endmodule |

## semantics/int.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 4 | module | — | ASSEMBLY | module MPY-INT |
| 5 | imports | — | ASSEMBLY | imports MPY-CORE |
| 7 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyUn("-", I:Int) => 0 -Int I |
| 9 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2 |
| 11 | rule | — | FIXED-SUPPLIED—target/load path | rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi |
| 12 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I |
| 13 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2 |
| 14 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2 |
| 15 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2) |
| 16 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2 |
| 17 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0 |
| 19 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= pyMod(Int, Int) [function] |
| 20 | rule | — | FIXED-SUPPLIED—target-unreachable | rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2 |
| 22 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2 |
| 23 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2 |
| 24 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2 |
| 25 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2 |
| 26 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2 |
| 27 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2 |
| 28 | endmodule | — | ASSEMBLY | endmodule |

## semantics/iter.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 6 | module | — | ASSEMBLY | module MPY-ITER |
| 7 | imports | — | ASSEMBLY | imports MPY-CORE |
| 8 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #iterNext(Iterable) &#124; "#iterDone" &#124; #iterYield(Val, Iterable) |
| 9 | endmodule | — | ASSEMBLY | endmodule |

## semantics/list.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-LIST |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 5 | imports | — | ASSEMBLY | imports MPY-ITER |
| 6 | imports | — | ASSEMBLY | imports MPY-OPERATORS |
| 9 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k> |
| 10 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k> |
| 13 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax ApplyK ::= "toList" |
| 14 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k> |
| 15 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k> |
| 18 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total] |
| 19 | rule | — | FIXED-SUPPLIED—target-unreachable | rule valSeqConcat(.ValSeq, T:ValSeq)                => T |
| 20 | rule | — | FIXED-SUPPLIED—target-unreachable | rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T)) |
| 24-25 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)] |
| 27 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B |
| 28 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B) |
| 33 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= hasRefVS(ValSeq) [function, total] |
| 34 | rule | — | FIXED-SUPPLIED—target-unreachable | rule hasRefVS(.ValSeq)                => false |
| 35 | rule | — | FIXED-SUPPLIED—target-unreachable | rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R) |
| 37-38 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] &#124; deepEqV(Val, Val, Map)        [function] |
| 39 | rule | — | FIXED-SUPPLIED—target-unreachable | rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true |
| 40 | rule | — | FIXED-SUPPLIED—target-unreachable | rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false |
| 41 | rule | — | FIXED-SUPPLIED—target-unreachable | rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false |
| 42-43 | rule | — | FIXED-SUPPLIED—target-unreachable | rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP) |
| 45-46 | rule | — | FIXED-SUPPLIED—target-unreachable | rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP) |
| 47-48 | rule | — | FIXED-SUPPLIED—target-unreachable | rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP) |
| 49 | rule | — | FIXED-SUPPLIED—target-unreachable | rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP) |
| 50 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise] |
| 53-55 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H &#124;-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)] |
| 58 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #memberAcc(Val, Iterable) &#124; #memberCont(Val) &#124; "#notB" |
| 59 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k> |
| 60 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k> |
| 61 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k> |
| 62 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k> |
| 63-64 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V |
| 65-66 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V) |
| 67 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> B:Bool ~> #notB => notBool B ... </k> |
| 68 | endmodule | — | ASSEMBLY | endmodule |

## semantics/methods.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-METHODS |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 5 | imports | — | ASSEMBLY | imports K-EQUAL |
| 6 | imports | — | ASSEMBLY | imports MPY-STR |
| 7 | imports | — | ASSEMBLY | imports MPY-LIST |
| 10 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Val ::= applyMethod(Val, String, Vals) [function] |
| 13 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS) |
| 14 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS) |
| 15 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS) |
| 16 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS) |
| 19 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS)) |
| 20 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS)) |
| 21 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS)) |
| 26 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS)) |
| 27 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total] |
| 28 | rule | — | FIXED-SUPPLIED—target-unreachable | rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq |
| 29 | rule | — | FIXED-SUPPLIED—target-unreachable | rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS |
| 30-31 | rule | — | FIXED-SUPPLIED—target-unreachable | rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R)))) |
| 34 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC) |
| 35 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= cntSub(IntSeq, IntSeq) [function] |
| 36 | rule | — | FIXED-SUPPLIED—target-unreachable | rule cntSub(.IntSeq, _:IntSeq) => 0 |
| 37-38 | rule | — | FIXED-SUPPLIED—target-unreachable | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0 |
| 39-40 | rule | — | FIXED-SUPPLIED—target-unreachable | rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0 |
| 41 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= dropIS(IntSeq, Int) [function, total] |
| 42 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0 |
| 43 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule dropIS(.IntSeq, _:Int) => .IntSeq [owise] |
| 44 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0 |
| 47 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS))))) |
| 48 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= trimWS(IntSeq) [function, total] |
| 49 | rule | — | FIXED-SUPPLIED—target-unreachable | rule trimWS(.IntSeq) => .IntSeq |
| 50 | rule | — | FIXED-SUPPLIED—target-unreachable | rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C) |
| 51 | rule | — | FIXED-SUPPLIED—target-unreachable | rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C) |
| 52 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= revIS(IntSeq) [function, total] &#124; revISAcc(IntSeq, IntSeq) [function, total] |
| 53 | rule | — | FIXED-SUPPLIED—target-unreachable | rule revIS(S:IntSeq) => revISAcc(S, .IntSeq) |
| 54 | rule | — | FIXED-SUPPLIED—target-unreachable | rule revISAcc(.IntSeq, A:IntSeq) => A |
| 55 | rule | — | FIXED-SUPPLIED—target-unreachable | rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A)) |
| 58 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS) |
| 61 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC) |
| 64 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V) |
| 65 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= cntOccVS(ValSeq, Val) [function, total] |
| 66 | rule | — | FIXED-SUPPLIED—target-unreachable | rule cntOccVS(.ValSeq, _:Val)                => 0 |
| 67 | rule | — | FIXED-SUPPLIED—target-unreachable | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V |
| 68 | rule | — | FIXED-SUPPLIED—target-unreachable | rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V) |
| 72-74 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)] |
| 75 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function] |
| 76 | rule | — | FIXED-SUPPLIED—target-unreachable | rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR) |
| 77-78 | rule | — | FIXED-SUPPLIED—target-unreachable | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C) |
| 79-80 | rule | — | FIXED-SUPPLIED—target-unreachable | rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C) |
| 82 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function] |
| 83 | rule | — | FIXED-SUPPLIED—target-unreachable | rule flushTok(ACC:ValSeq, .IntSeq)            => ACC |
| 84 | rule | — | FIXED-SUPPLIED—target-unreachable | rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq)) |
| 85 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isWSC(Int) [function, total] |
| 86 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13 |
| 89-91 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)] |
| 94-96 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)] |
| 97 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function] |
| 98 | rule | — | FIXED-SUPPLIED—target-unreachable | rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq) |
| 99-100 | rule | — | FIXED-SUPPLIED—target-unreachable | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP |
| 101-102 | rule | — | FIXED-SUPPLIED—target-unreachable | rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP) |
| 104-105 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B)) |
| 106 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total] |
| 107 | rule | — | FIXED-SUPPLIED—target-unreachable | rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq |
| 108 | rule | — | FIXED-SUPPLIED—target-unreachable | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A |
| 109 | rule | — | FIXED-SUPPLIED—target-unreachable | rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A) |
| 112 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isUpperC(Int) [function, total] |
| 113 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90 |
| 115 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isLowerC(Int) [function, total] |
| 116 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122 |
| 118 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isAlphaC(Int) [function, total] |
| 119 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C) |
| 121 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= isDigitC(Int) [function, total] |
| 122 | rule | — | FIXED-SUPPLIED—target-unreachable | rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57 |
| 124 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= hasUpper(IntSeq) [function, total] |
| 125 | rule | — | FIXED-SUPPLIED—target-unreachable | rule hasUpper(.IntSeq) => false |
| 126 | rule | — | FIXED-SUPPLIED—target-unreachable | rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S) |
| 128 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= hasLower(IntSeq) [function, total] |
| 129 | rule | — | FIXED-SUPPLIED—target-unreachable | rule hasLower(.IntSeq) => false |
| 130 | rule | — | FIXED-SUPPLIED—target-unreachable | rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S) |
| 132 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= allAlpha(IntSeq) [function, total] |
| 133 | rule | — | FIXED-SUPPLIED—target-unreachable | rule allAlpha(.IntSeq) => true |
| 134 | rule | — | FIXED-SUPPLIED—target-unreachable | rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S) |
| 136 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= allDigit(IntSeq) [function, total] |
| 137 | rule | — | FIXED-SUPPLIED—target-unreachable | rule allDigit(.IntSeq) => true |
| 138 | rule | — | FIXED-SUPPLIED—target-unreachable | rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S) |
| 140 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= lowerC(Int) [function, total] |
| 142 | rule | — | FIXED-SUPPLIED—target-unreachable | rule lowerC(C:Int) => C +Int 32 requires isUpperC(C) |
| 143 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule lowerC(C:Int) => C         [owise] |
| 145 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= upperC(Int) [function, total] |
| 146 | rule | — | FIXED-SUPPLIED—target-unreachable | rule upperC(C:Int) => C -Int 32 requires isLowerC(C) |
| 147 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule upperC(C:Int) => C         [owise] |
| 149 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= swapC(Int) [function, total] |
| 150 | rule | — | FIXED-SUPPLIED—target-unreachable | rule swapC(C:Int) => C +Int 32 requires isUpperC(C) |
| 151 | rule | — | FIXED-SUPPLIED—target-unreachable | rule swapC(C:Int) => C -Int 32 requires isLowerC(C) |
| 152 | rule | owise | FIXED-SUPPLIED—target-unreachable | rule swapC(C:Int) => C         [owise] |
| 154 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= mapLower(IntSeq) [function, total] |
| 155 | rule | — | FIXED-SUPPLIED—target-unreachable | rule mapLower(.IntSeq) => .IntSeq |
| 156 | rule | — | FIXED-SUPPLIED—target-unreachable | rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S)) |
| 158 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= mapUpper(IntSeq) [function, total] |
| 159 | rule | — | FIXED-SUPPLIED—target-unreachable | rule mapUpper(.IntSeq) => .IntSeq |
| 160 | rule | — | FIXED-SUPPLIED—target-unreachable | rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S)) |
| 162 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= mapSwap(IntSeq) [function, total] |
| 163 | rule | — | FIXED-SUPPLIED—target-unreachable | rule mapSwap(.IntSeq) => .IntSeq |
| 164 | rule | — | FIXED-SUPPLIED—target-unreachable | rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S)) |
| 166 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total] |
| 167 | rule | — | FIXED-SUPPLIED—target-unreachable | rule startsWith(.IntSeq, _:IntSeq)               => true |
| 168 | rule | — | FIXED-SUPPLIED—target-unreachable | rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| 169 | rule | — | FIXED-SUPPLIED—target-unreachable | rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs) |
| 170 | endmodule | — | ASSEMBLY | endmodule |

## semantics/operators.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 6 | module | — | ASSEMBLY | module MPY-OPERATORS |
| 7 | imports | — | ASSEMBLY | imports MPY-CORE |
| 8 | imports | — | ASSEMBLY | imports MPY-ITER |
| 10 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k> |
| 12 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k> |
| 15 | context | — | FIXED-SUPPLIED—target/load path | context Compare(HOLE, _) |
| 16 | context | — | FIXED-SUPPLIED—target/load path | context Compare(_:Val, CmpOp(_, HOLE)) |
| 17 | rule | owise | FIXED-SUPPLIED—target/load path | rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise] |
| 19 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("is",     V:Val, noneV) => V ==K noneV |
| 20 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV) |
| 25-27 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 28-31 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)] |
| 34-37 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)] |
| 38-42 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H &#124;-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)] |
| 44-46 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 47 | endmodule | — | ASSEMBLY | endmodule |

## semantics/range.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 5 | module | — | ASSEMBLY | module MPY-RANGE |
| 6 | imports | — | ASSEMBLY | imports MPY-CORE |
| 7 | imports | — | ASSEMBLY | imports MPY-ITER |
| 9 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= inRange(Int, Int, Int) [function, total] |
| 10 | rule | — | FIXED-SUPPLIED—target-unreachable | rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI) |
| 12 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= rangeLen(Int, Int, Int) [function] |
| 13-14 | rule | — | FIXED-SUPPLIED—target-unreachable | rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO |
| 15-16 | rule | — | FIXED-SUPPLIED—target-unreachable | rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO |
| 17-18 | rule | — | FIXED-SUPPLIED—target-unreachable | rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO) |
| 20-22 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST) |
| 23-24 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST) |
| 25 | endmodule | — | ASSEMBLY | endmodule |

## semantics/set.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-SET |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 8 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Val ::= setV(IntSeq) |
| 11 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= codeIn(Int, IntSeq) [function, total] |
| 12 | rule | — | FIXED-SUPPLIED—target-unreachable | rule codeIn(_:Int, .IntSeq)                => false |
| 13 | rule | — | FIXED-SUPPLIED—target-unreachable | rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T) |
| 16-17 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] &#124; dedupFrom(IntSeq, IntSeq)  [function, total] |
| 18 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq) |
| 19 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC |
| 20-21 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC) |
| 22-23 | rule | — | FIXED-SUPPLIED—target-unreachable | rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC) |
| 25 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= snocCode(IntSeq, Int) [function, total] |
| 26 | rule | — | FIXED-SUPPLIED—target-unreachable | rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq) |
| 27 | rule | — | FIXED-SUPPLIED—target-unreachable | rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C)) |
| 31 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total] |
| 32 | rule | — | FIXED-SUPPLIED—target-unreachable | rule subsetCodes(.IntSeq, _:IntSeq)                => true |
| 33 | rule | — | FIXED-SUPPLIED—target-unreachable | rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B) |
| 35 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total] |
| 36 | rule | — | FIXED-SUPPLIED—target-unreachable | rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A) |
| 39 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B) |
| 40 | endmodule | — | ASSEMBLY | endmodule |

## semantics/sort.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 10 | module | — | ASSEMBLY | module MPY-SORT |
| 11 | imports | — | ASSEMBLY | imports MPY-BUILTINS |
| 12 | imports | — | ASSEMBLY | imports MPY-SUBSCRIPT |
| 18 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators] |
| 19 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= insVS(Int, ValSeq) [function] |
| 20 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule sortVS(.ValSeq)                => .ValSeq          [concrete] |
| 21 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete] |
| 22 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete] |
| 23 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete] |
| 24 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete] |
| 26 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function] |
| 27 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete] |
| 28 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete] |
| 29-30 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete] |
| 31-32 | rule | concrete | FIXED-SUPPLIED—target-unreachable | rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete] |
| 36-37 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k> |
| 40-42 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H &#124;-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)] |
| 49 | syntax | function, total, symbol, no-evaluators | FIXED-SUPPLIED—opaque, target-unreachable | syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators] |
| 51-52 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= revVS(ValSeq) [function, total] &#124; revVSAcc(ValSeq, ValSeq) [function, total] |
| 53 | rule | — | FIXED-SUPPLIED—target-unreachable | rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq) |
| 54 | rule | — | FIXED-SUPPLIED—target-unreachable | rule revVSAcc(.ValSeq, A:ValSeq) => A |
| 55 | rule | — | FIXED-SUPPLIED—target-unreachable | rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A)) |
| 57 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= condRev(ValSeq, Bool) [function, total] |
| 58 | rule | — | FIXED-SUPPLIED—target-unreachable | rule condRev(S:ValSeq, false) => S |
| 59 | rule | — | FIXED-SUPPLIED—target-unreachable | rule condRev(S:ValSeq, true)  => revVS(S) |
| 61-62 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k> |
| 63-64 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k> |
| 65-66 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k> |
| 72 | endmodule | — | ASSEMBLY | endmodule |

## semantics/str.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-STR |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 5 | imports | — | ASSEMBLY | imports MPY-ITER |
| 8 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k> |
| 9-10 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k> |
| 13 | syntax | function | FIXED-SUPPLIED—target/load path | syntax IntSeq ::= strToCodes(String) [function] |
| 14 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> Str(S:String) => str(strToCodes(S)) ... </k> |
| 15 | rule | — | FIXED-SUPPLIED—target/load path | rule strToCodes("") => .IntSeq |
| 16-17 | rule | — | FIXED-SUPPLIED—target/load path | rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128 |
| 20 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total] |
| 21 | rule | — | FIXED-SUPPLIED—target-unreachable | rule seqConcat(.IntSeq, T:IntSeq)                => T |
| 22 | rule | — | FIXED-SUPPLIED—target-unreachable | rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T)) |
| 24 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B)) |
| 25 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B |
| 26 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B) |
| 29 | rule | — | FIXED-SUPPLIED—target/load path | rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X) |
| 30 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X) |
| 32 | syntax | function, total | FIXED-SUPPLIED—target/load path | syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total] |
| 33 | rule | — | FIXED-SUPPLIED—target/load path | rule strPrefix(.IntSeq, _:IntSeq)               => true |
| 34 | rule | — | FIXED-SUPPLIED—target/load path | rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| 35 | rule | — | FIXED-SUPPLIED—target/load path | rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs) |
| 37 | syntax | function, total | FIXED-SUPPLIED—target/load path | syntax Bool ::= strContains(IntSeq, IntSeq) [function, total] |
| 38 | rule | — | FIXED-SUPPLIED—target/load path | rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X) |
| 39 | rule | — | FIXED-SUPPLIED—target/load path | rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq) |
| 40-41 | rule | — | FIXED-SUPPLIED—target/load path | rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs)) |
| 48 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Bool ::= strLt(IntSeq, IntSeq) [function, total] |
| 49 | rule | — | FIXED-SUPPLIED—target-unreachable | rule strLt(.IntSeq, .IntSeq)                => false |
| 50 | rule | — | FIXED-SUPPLIED—target-unreachable | rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true |
| 51 | rule | — | FIXED-SUPPLIED—target-unreachable | rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false |
| 52 | rule | — | FIXED-SUPPLIED—target-unreachable | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B |
| 53 | rule | — | FIXED-SUPPLIED—target-unreachable | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B |
| 54 | rule | — | FIXED-SUPPLIED—target-unreachable | rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B |
| 56 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B) |
| 57 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A) |
| 58 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A) |
| 59 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B) |
| 60 | endmodule | — | ASSEMBLY | endmodule |

## semantics/subscript.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-SUBSCRIPT |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 11 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Val ::= valSeqAt(ValSeq, Int) [function, total] |
| 12 | rule | — | FIXED-SUPPLIED—target-unreachable | rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V |
| 13-14 | rule | — | FIXED-SUPPLIED—target-unreachable | rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0 |
| 16 | syntax | function | FIXED-SUPPLIED—target/load path | syntax Int ::= intSeqAt(IntSeq, Int) [function] |
| 17 | rule | — | FIXED-SUPPLIED—target/load path | rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C |
| 18-19 | rule | — | FIXED-SUPPLIED—target/load path | rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0 |
| 21 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= normIdx(Int, Int) [function, total] |
| 22 | rule | — | FIXED-SUPPLIED—target-unreachable | rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0 |
| 23 | rule | — | FIXED-SUPPLIED—target-unreachable | rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0 |
| 27 | context | — | FIXED-SUPPLIED—target/load path | context Subscript(HOLE, _) |
| 28 | context | — | FIXED-SUPPLIED—target/load path | context Subscript(_:Val, HOLE:Expr) |
| 31-33 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 35 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k> |
| 37 | syntax | function | FIXED-SUPPLIED—target/load path | syntax Val ::= applyIndex(Val, Int) [function] |
| 38 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS))) |
| 39 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS))) |
| 40-41 | rule | — | FIXED-SUPPLIED—target/load path | rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq)) |
| 44-47 | syntax | — | FIXED-SUPPLIED—target/load path | syntax KItem ::= #evalB(Bound) &#124; "#toSome" &#124; #slLo(Val, Bound, Bound) &#124; #slHi(Val, OptInt, Bound) &#124; #slStep(Val, OptInt, OptInt) |
| 49 | syntax | — | FIXED-SUPPLIED—target/load path | syntax OptInt ::= "noB" &#124; someB(Int) |
| 50 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #evalB(NoBound)  => noB ... </k> |
| 51 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k> |
| 52 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> I:Int ~> #toSome => someB(I) ... </k> |
| 54 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k> |
| 55 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k> |
| 56 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k> |
| 58-60 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)] |
| 61 | rule | — | FIXED-SUPPLIED—target/load path | rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k> |
| 63 | syntax | function | FIXED-SUPPLIED—target/load path | syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function] |
| 64-65 | rule | — | FIXED-SUPPLIED—target-unreachable | rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| 66-67 | rule | — | FIXED-SUPPLIED—target-unreachable | rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST))) |
| 68-69 | rule | — | FIXED-SUPPLIED—target/load path | rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST))) |
| 72 | syntax | function, total | FIXED-SUPPLIED—target/load path | syntax Int ::= slStep(OptInt) [function, total] |
| 73 | rule | — | FIXED-SUPPLIED—target/load path | rule slStep(noB)          => 1 |
| 74 | rule | — | FIXED-SUPPLIED—target-unreachable | rule slStep(someB(S:Int)) => S |
| 76 | syntax | function | FIXED-SUPPLIED—target/load path | syntax Int ::= slStart(OptInt, OptInt, Int) [function] |
| 77-78 | rule | — | FIXED-SUPPLIED—target-unreachable | rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0 |
| 79-80 | rule | — | FIXED-SUPPLIED—target-unreachable | rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0 |
| 81 | rule | — | FIXED-SUPPLIED—target/load path | rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST)) |
| 83 | syntax | function | FIXED-SUPPLIED—target/load path | syntax Int ::= slStop(OptInt, OptInt, Int) [function] |
| 84-85 | rule | — | FIXED-SUPPLIED—target/load path | rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0 |
| 86-87 | rule | — | FIXED-SUPPLIED—target-unreachable | rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0 |
| 88 | rule | — | FIXED-SUPPLIED—target-unreachable | rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST)) |
| 90 | syntax | function, total | FIXED-SUPPLIED—target/load path | syntax Int ::= slAdjust(Int, Int, Int) [function, total] |
| 91-92 | rule | — | FIXED-SUPPLIED—target-unreachable | rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0 |
| 93-94 | rule | — | FIXED-SUPPLIED—target/load path | rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0 |
| 96 | syntax | function, total | FIXED-SUPPLIED—target-unreachable | syntax Int ::= clampLo(Int, Int) [function, total] |
| 97-98 | rule | — | FIXED-SUPPLIED—target-unreachable | rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0 |
| 99-100 | rule | — | FIXED-SUPPLIED—target-unreachable | rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0 |
| 102 | syntax | function, total | FIXED-SUPPLIED—target/load path | syntax Int ::= clampHi(Int, Int, Int) [function, total] |
| 103-104 | rule | — | FIXED-SUPPLIED—target/load path | rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN |
| 105-106 | rule | — | FIXED-SUPPLIED—target/load path | rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN |
| 109 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function] |
| 110-112 | rule | — | FIXED-SUPPLIED—target-unreachable | rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP) |
| 113-114 | rule | — | FIXED-SUPPLIED—target-unreachable | rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)) |
| 116 | syntax | function | FIXED-SUPPLIED—target/load path | syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function] |
| 117-119 | rule | — | FIXED-SUPPLIED—target/load path | rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP) |
| 120-121 | rule | — | FIXED-SUPPLIED—target/load path | rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)) |
| 122 | endmodule | — | ASSEMBLY | endmodule |

## semantics/syntax.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-SYNTAX |
| 4 | imports | — | ASSEMBLY | imports INT-SYNTAX |
| 5 | imports | — | ASSEMBLY | imports FLOAT-SYNTAX |
| 6 | imports | — | ASSEMBLY | imports BOOL-SYNTAX |
| 7 | imports | — | ASSEMBLY | imports STRING-SYNTAX |
| 9-30 | syntax | macro, strict, seqstrict | FIXED-SUPPLIED—target/load path | syntax Expr ::= "Int"      "(" Int ")" &#124; "Float"    "(" Float ")" &#124; "Bool"     "(" Bool ")" &#124; "Name"     "(" String ")" &#124; "Str"      "(" String ")" &#124; "UnaryOp"  "(" String "," Expr ")" [strict(2)] &#124; "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] &#124; "BoolOp"    "(" String "," Exprs ")" &#124; "ListExpr"  "(" Exprs ")" &#124; "DictExpr"  "(" Entries ")" &#124; "ListComp"  "(" Expr "," CompFors ")" [macro] &#124; "GenExp"    "(" Expr "," CompFors ")" [macro] &#124; "TupleExpr" "(" Exprs ")" &#124; "Subscript" "(" Expr "," Index ")" &#124; "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] &#124; "Lambda"    "(" Params "," Expr ")" &#124; "KwArg"     "(" String "," Expr ")" &#124; "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" &#124; "NoneVal" &#124; "Call"      "(" Expr "," Exprs ")" &#124; "Attribute" "(" Expr "," String ")" [strict(1)] &#124; "Compare"   "(" Expr "," CmpOp ")" |
| 32 | syntax | — | FIXED-SUPPLIED—target/load path | syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")" |
| 33 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Entry    ::= "Entry" "(" Expr "," Expr ")" |
| 34 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax Entries  ::= List{Entry, ","} |
| 35 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")" |
| 36 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax CompFors ::= List{CompFor, ""} |
| 37 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Exprs    ::= List{Expr, ","} |
| 38 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Index    ::= Expr &#124; "Slice" "(" Bound "," Bound "," Bound ")" |
| 39 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Bound    ::= Expr &#124; "NoBound" |
| 41-54 | syntax | strict | FIXED-SUPPLIED—target/load path | syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] &#124; "Import"    "(" String ")" &#124; "ImportFrom" "(" String "," ParamNames ")" &#124; "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] &#124; "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] &#124; "While"     "(" Expr "," Stmts ")" &#124; "Break" &#124; "Continue" &#124; "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] &#124; "Return"    "(" Expr ")" [strict] &#124; "Assert"    "(" Expr ")" [strict] &#124; "Expr"      "(" Expr ")" [strict] &#124; "FuncDef"   "(" String "," Params "," Stmts ")" &#124; "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")" |
| 56 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Stmts      ::= List{Stmt, ""} |
| 57 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Params     ::= "Params" "(" ParamNames ")" |
| 58 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax CellVars   ::= "CellVars" "(" ParamNames ")" |
| 59 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax FreeVars   ::= "FreeVars" "(" ParamNames ")" |
| 60 | syntax | — | FIXED-SUPPLIED—target/load path | syntax ParamNames ::= List{String, ","} |
| 61 | syntax | — | FIXED-SUPPLIED—target/load path | syntax Module     ::= "Module" "(" Stmts ")" |
| 62 | endmodule | — | ASSEMBLY | endmodule |

## semantics/tuple.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 3 | module | — | ASSEMBLY | module MPY-TUPLE |
| 4 | imports | — | ASSEMBLY | imports MPY-CORE |
| 5 | imports | — | ASSEMBLY | imports MPY-ITER |
| 6 | imports | — | ASSEMBLY | imports MPY-LIST |
| 7 | imports | — | ASSEMBLY | imports MPY-METHODS |
| 10 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k> |
| 11 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k> |
| 14 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax ApplyK ::= "toTuple" |
| 15 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k> |
| 16 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k> |
| 18 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B |
| 20 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k> |
| 21 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k> |
| 23 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0) |
| 24 | syntax | function | FIXED-SUPPLIED—target-unreachable | syntax Int ::= idxOfVS(ValSeq, Val, Int) [function] |
| 25 | rule | — | FIXED-SUPPLIED—target-unreachable | rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V |
| 26-27 | rule | — | FIXED-SUPPLIED—target-unreachable | rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V) |
| 28 | rule | — | FIXED-SUPPLIED—target-unreachable | rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B) |
| 31 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #bindTgt(Expr, Val) |
| 32-34 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map => M [ X <- V ], _) ... </scopes> |
| 35-41 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L &#124;-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)] |
| 42 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| 43 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k> |
| 44-46 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 49 | syntax | — | FIXED-SUPPLIED—target-unreachable | syntax KItem ::= #unpackSeq(Exprs, ValSeq) |
| 50 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k> |
| 51 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k> |
| 52-54 | rule | priority | FIXED-SUPPLIED—target-unreachable | rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H &#124;-> V:Val ... </heap> [priority(40)] |
| 55-56 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k> |
| 57 | rule | — | FIXED-SUPPLIED—target-unreachable | rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k> |
| 58 | endmodule | — | ASSEMBLY | endmodule |

## verification.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 1 | requires | — | PROOF-LOCAL declaration | requires "reference-semantics/semantics.k" |
| 3 | module | — | PROOF-LOCAL declaration | module VERIFICATION |
| 4 | imports | — | PROOF-LOCAL declaration | imports MPY |
| 7 | syntax | function, total | PROOF-LOCAL declaration | syntax Int ::= countUpperEven(IntSeq) [function, total] |
| 8 | rule | — | PROOF-LOCAL—review individually | rule countUpperEven(.IntSeq) => 0 |
| 9-21 | rule | simplification | PROOF-LOCAL—review individually | rule countUpperEven(CODES:IntSeq) => (#if strContains( iCons(intSeqAt(CODES, 0), .IntSeq), strToCodes("AEIOU")) #then 1 #else 0 #fi) +Int countUpperEven( buildIS( CODES, clampHi(2, isLen(CODES), 1), isLen(CODES), 1)) requires notBool (CODES ==K .IntSeq) [simplification] |
| 24-26 | rule | simplification | PROOF-LOCAL—review individually | rule (A:Int +Int B:Int) +Int C:Int => A +Int (B +Int C) [simplification] |
| 27 | endmodule | — | PROOF-LOCAL declaration | endmodule |

## spec.k

| Lines | Kind | Attributes | Disposition | Normalized declaration |
|---:|---|---|---|---|
| 1 | requires | — | TARGET CLAIM—review individually | requires "verification.k" |
| 3 | module | — | TARGET CLAIM—review individually | module SPEC |
| 4 | imports | — | TARGET CLAIM—review individually | imports VERIFICATION |
| 6-33 | claim | — | TARGET CLAIM—review individually | claim [loop-invariant]: <k> #while( Name("remaining"), AugAssign( Name("count"), "+", Compare( Subscript(Name("remaining"), Int(0)), CmpOp("in", Str("AEIOU")))) Assign( Name("remaining"), Subscript( Name("remaining"), Slice(Int(2), NoBound, NoBound)))) => .K ... </k> <env> 1 </env> <scopes> ... 1 &#124;-> scope( "s" &#124;-> str(ORIGINAL:IntSeq) "count" &#124;-> (ACC:Int => ACC +Int countUpperEven(CODES)) "remaining" &#124;-> (str(CODES) => str(.IntSeq)), parent(0)) ... </scopes> |
| 35-73 | claim | — | TARGET CLAIM—review individually | claim [count-upper]: <k> Call(Name("count_upper"), str(CODES:IntSeq)) => countUpperEven(CODES) </k> <env> 0 </env> <scopes> 0 &#124;-> scope( "count_upper" &#124;-> closureVal( ("s", .ParamNames), Assign(Name("count"), Int(0)) Assign(Name("remaining"), Name("s")) While( Name("remaining"), AugAssign( Name("count"), "+", Compare( Subscript(Name("remaining"), Int(0)), CmpOp("in", Str("AEIOU")))) Assign( Name("remaining"), Subscript( Name("remaining"), Slice(Int(2), NoBound, NoBound)))) Return(Name("count")) .Stmts, 0), parent(-1)) -1 &#124;-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> |
| 74 | endmodule | — | TARGET CLAIM—review individually | endmodule |

## Counts

Kinds: claim=2, configuration=1, context=5, endmodule=27, imports=88, module=27, requires=25, rule=698, syntax=228

Dispositions: ASSEMBLY=159, FIXED-SUPPLIED—opaque, target-unreachable=22, FIXED-SUPPLIED—target-unreachable=792, FIXED-SUPPLIED—target/load path=114, PROOF-LOCAL declaration=5, PROOF-LOCAL—review individually=3, TARGET CLAIM—review individually=6

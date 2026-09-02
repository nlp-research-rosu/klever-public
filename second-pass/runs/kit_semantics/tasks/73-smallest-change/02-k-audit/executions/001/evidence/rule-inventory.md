# Exhaustive K declaration/rule inventory

Generated from the trusted supplied-semantics tree and all proof-local source modules that contribute declarations or claims. Every source line beginning with `configuration`, `syntax`, `rule`, `claim`, `context`, or `alias` starts one inventoried block; continuation lines are retained through the next declaration.

- Files: 31
- Inventory records: 957
- Kinds: claim=7, configuration=1, context=5, rule=709, syntax=235
- Attributes: concrete=35, function=149, macro=8, owise=26, priority(39)=1, priority(40)=42, priority(45)=3, seqstrict(2, 3)=1, simplification=3, strict=1, strict(1)=2, strict(2)=2, strict(3)=1, symbol(absF)=1, symbol(addF)=1, symbol(ceilF)=1, symbol(decStrToF)=1, symbol(divF)=1, symbol(divFloatIntV)=1, symbol(divII)=1, symbol(eqF)=1, symbol(floatLt)=1, symbol(floatMod)=1, symbol(floorFI)=1, symbol(gtF)=1, symbol(intFloatDiv)=1, symbol(intToF)=1, symbol(md5hexCodes)=1, symbol(mulF)=1, symbol(powF)=1, symbol(roundF)=1, symbol(roundFN)=1, symbol(sortKeyVS)=1, symbol(sortVS)=1, symbol(sqrtF)=1, symbol(subF)=1, symbol(toF)=1, symbol(truncF)=1, total=109

## /reference/reference-semantics/semantics/assert.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 1 | 6-7 | rule | ordinary | `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)` |
| 2 | 8-12 | rule | ordinary | `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)` |
| 3 | 13-15 | rule | priority(40) | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |

## /reference/reference-semantics/semantics/bool.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 4 | 8-9 | rule | ordinary | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 5 | 10-10 | rule | ordinary | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 6 | 11-15 | rule | ordinary | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| 7 | 16-16 | context | ordinary | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 8 | 17-17 | rule | ordinary | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 9 | 18-19 | rule | ordinary | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)` |
| 10 | 20-21 | rule | ordinary | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)` |
| 11 | 22-23 | rule | ordinary | `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)` |
| 12 | 24-28 | rule | ordinary | `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)` |
| 13 | 29-30 | rule | priority(40) | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]` |
| 14 | 31-34 | rule | priority(40) | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 15 | 35-38 | rule | priority(40) | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |
| 16 | 39-42 | rule | priority(40) | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H \|-> V:Val ... </heap> requires truthy(V) [priority(40)]` |
| 17 | 43-46 | rule | priority(40) | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]` |

## /reference/reference-semantics/semantics/builtins.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 18 | 17-19 | syntax | function | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| 19 | 20-20 | syntax | function | `syntax Int ::= seqLen(Val) [function]` |
| 20 | 21-21 | rule | ordinary | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 21 | 22-22 | rule | ordinary | `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)` |
| 22 | 23-23 | rule | ordinary | `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)` |
| 23 | 24-24 | rule | ordinary | `rule seqLen(str(IS:IntSeq))                   => isLen(IS)` |
| 24 | 25-25 | rule | ordinary | `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)` |
| 25 | 26-31 | rule | ordinary | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| 26 | 32-32 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>` |
| 27 | 33-33 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 28 | 34-34 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>` |
| 29 | 35-35 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>` |
| 30 | 36-36 | syntax | function, total | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 31 | 37-37 | rule | ordinary | `rule charsOf(.IntSeq)                => .ValSeq` |
| 32 | 38-40 | rule | ordinary | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| 33 | 41-43 | rule | ordinary | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| 34 | 44-46 | rule | ordinary | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| 35 | 47-47 | syntax | ordinary | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 36 | 48-48 | rule | ordinary | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 37 | 49-49 | rule | ordinary | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 38 | 50-53 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)` |
| 39 | 54-54 | syntax | function | `syntax Int ::= intOf(Val) [function]` |
| 40 | 55-55 | rule | ordinary | `rule intOf(I:Int)  => I` |
| 41 | 56-58 | rule | ordinary | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| 42 | 59-59 | syntax | ordinary | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 43 | 60-60 | rule | ordinary | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 44 | 61-61 | rule | ordinary | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 45 | 62-63 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)` |
| 46 | 64-66 | rule | ordinary | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)` |
| 47 | 67-67 | syntax | ordinary | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 48 | 68-68 | rule | ordinary | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 49 | 69-69 | rule | ordinary | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 50 | 70-71 | rule | ordinary | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)` |
| 51 | 72-75 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)` |
| 52 | 76-76 | syntax | ordinary | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 53 | 77-77 | rule | ordinary | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 54 | 78-79 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 55 | 80-80 | rule | ordinary | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 56 | 81-81 | rule | ordinary | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 57 | 82-85 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 58 | 86-86 | syntax | ordinary | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 59 | 87-87 | rule | ordinary | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 60 | 88-89 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)` |
| 61 | 90-90 | rule | ordinary | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 62 | 91-91 | rule | ordinary | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 63 | 92-96 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)` |
| 64 | 97-97 | syntax | function | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 65 | 98-98 | rule | ordinary | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 66 | 99-99 | rule | ordinary | `rule maxVals(M:Int, .Vals)           => M` |
| 67 | 100-101 | rule | ordinary | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| 68 | 102-102 | syntax | function | `syntax Int ::= minVals(Int, Vals) [function]` |
| 69 | 103-103 | rule | ordinary | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 70 | 104-104 | rule | ordinary | `rule minVals(M:Int, .Vals)           => M` |
| 71 | 105-107 | rule | ordinary | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| 72 | 108-110 | rule | ordinary | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0` |
| 73 | 111-113 | rule | ordinary | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0` |
| 74 | 114-114 | syntax | function, total | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 75 | 115-115 | rule | ordinary | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 76 | 116-116 | rule | ordinary | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 77 | 117-117 | syntax | function, total | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 78 | 118-118 | rule | ordinary | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 79 | 119-123 | rule | ordinary | `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0` |
| 80 | 124-125 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>` |
| 81 | 126-126 | syntax | function, total | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 82 | 127-127 | rule | ordinary | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 83 | 128-131 | rule | ordinary | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))` |
| 84 | 132-133 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>` |
| 85 | 134-134 | syntax | function, total | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 86 | 135-135 | rule | ordinary | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 87 | 136-136 | rule | ordinary | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 88 | 137-139 | rule | ordinary | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| 89 | 140-142 | rule | ordinary | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| 90 | 143-143 | rule | ordinary | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 91 | 144-147 | rule | ordinary | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128` |
| 92 | 148-148 | rule | ordinary | `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))` |
| 93 | 149-151 | rule | ordinary | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| 94 | 152-155 | rule | ordinary | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57` |
| 95 | 156-157 | rule | ordinary | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2` |
| 96 | 158-158 | syntax | function, total | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 97 | 159-159 | rule | ordinary | `rule intDigAcc(.IntSeq, ACC:Int)             => ACC` |
| 98 | 160-162 | rule | ordinary | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| 99 | 163-163 | rule | ordinary | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 100 | 164-166 | rule | ordinary | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)` |
| 101 | 167-168 | rule | ordinary | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>` |
| 102 | 169-169 | rule | ordinary | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>` |
| 103 | 170-170 | rule | ordinary | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 104 | 171-172 | rule | ordinary | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>` |
| 105 | 173-173 | rule | ordinary | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>` |
| 106 | 174-176 | rule | ordinary | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| 107 | 177-177 | rule | ordinary | `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)` |
| 108 | 178-178 | rule | ordinary | `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)` |
| 109 | 179-186 | rule | ordinary | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0` |
| 110 | 187-187 | rule | ordinary | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 111 | 188-188 | syntax | function | `syntax Int ::= evalArith(IntSeq) [function]` |
| 112 | 189-191 | rule | ordinary | `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))` |
| 113 | 192-193 | syntax | ordinary | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| 114 | 194-194 | syntax | function, total | `syntax Bool ::= evDigit(Int) [function, total]` |
| 115 | 195-195 | rule | ordinary | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 116 | 196-196 | syntax | function, total | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 117 | 197-197 | rule | ordinary | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 118 | 198-198 | rule | owise | `rule evHead42(_:IntSeq)            => false [owise]` |
| 119 | 199-199 | syntax | function, total | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 120 | 200-200 | rule | ordinary | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 121 | 201-202 | rule | owise | `rule evHead47(_:IntSeq)            => false [owise]` |
| 122 | 203-203 | syntax | function, total | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 123 | 204-204 | rule | ordinary | `rule tokOps(.IntSeq)                 => .OpSeq` |
| 124 | 205-205 | rule | ordinary | `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)` |
| 125 | 206-206 | rule | ordinary | `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)` |
| 126 | 207-207 | rule | ordinary | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 127 | 208-208 | rule | ordinary | `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 128 | 209-209 | rule | ordinary | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 129 | 210-210 | rule | ordinary | `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 130 | 211-211 | rule | ordinary | `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))` |
| 131 | 212-213 | rule | ordinary | `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))` |
| 132 | 214-215 | syntax | function, total | `syntax IntSeq ::= tokNds(IntSeq) [function, total] \| tokNdAcc(Int, IntSeq) [function, total]` |
| 133 | 216-216 | rule | ordinary | `rule tokNds(.IntSeq)                => .IntSeq` |
| 134 | 217-217 | rule | ordinary | `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)` |
| 135 | 218-218 | rule | ordinary | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 136 | 219-220 | rule | ordinary | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32` |
| 137 | 221-222 | rule | ordinary | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)` |
| 138 | 223-224 | rule | owise | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 139 | 225-225 | syntax | ordinary | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 140 | 226-226 | syntax | function, total | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 141 | 227-227 | rule | ordinary | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 142 | 228-229 | rule | owise | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 143 | 230-230 | syntax | function, total | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 144 | 231-231 | rule | ordinary | `rule applyOpE("+",  A:Int, B:Int) => A +Int B` |
| 145 | 232-232 | rule | ordinary | `rule applyOpE("-",  A:Int, B:Int) => A -Int B` |
| 146 | 233-233 | rule | ordinary | `rule applyOpE("*",  A:Int, B:Int) => A *Int B` |
| 147 | 234-234 | rule | ordinary | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 148 | 235-235 | rule | ordinary | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 149 | 236-237 | rule | owise | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 150 | 238-238 | syntax | function, total | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 151 | 239-239 | rule | ordinary | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 152 | 240-240 | rule | ordinary | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 153 | 241-242 | rule | ordinary | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"` |
| 154 | 243-243 | rule | owise | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 155 | 244-244 | syntax | function, total | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 156 | 245-245 | rule | ordinary | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 157 | 246-246 | rule | ordinary | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 158 | 247-247 | syntax | function, total | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 159 | 248-249 | rule | ordinary | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 160 | 250-250 | syntax | function, total | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 161 | 251-251 | rule | ordinary | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 162 | 252-252 | rule | ordinary | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 163 | 253-253 | rule | ordinary | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 164 | 254-254 | rule | ordinary | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 165 | 255-255 | syntax | function, total | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 166 | 256-256 | rule | ordinary | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 167 | 257-259 | rule | ordinary | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)` |
| 168 | 260-262 | rule | ordinary | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)` |
| 169 | 263-264 | rule | owise | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]` |
| 170 | 265-265 | syntax | function, total | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 171 | 266-266 | rule | ordinary | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 172 | 267-267 | rule | ordinary | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 173 | 268-268 | rule | owise | `rule inLevelE(_:String, _:String) => false [owise]` |
| 174 | 269-269 | syntax | function, total | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 175 | 270-270 | rule | ordinary | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 176 | 271-271 | rule | ordinary | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 177 | 272-272 | syntax | function, total | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 178 | 273-273 | rule | ordinary | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 179 | 274-278 | rule | ordinary | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| 180 | 279-279 | syntax | ordinary | `syntax KItem ::= "#md5"` |
| 181 | 280-281 | rule | priority(40) | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]` |
| 182 | 282-282 | rule | ordinary | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 183 | 283-283 | syntax | ordinary | `syntax Val ::= md5Obj(IntSeq)` |
| 184 | 284-284 | rule | ordinary | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 185 | 285-290 | syntax | function, symbol(md5hexCodes), total | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| 186 | 291-291 | rule | ordinary | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 187 | 292-292 | rule | ordinary | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 188 | 293-293 | syntax | function | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 189 | 294-294 | rule | ordinary | `rule isIntV(_:Int)         => true` |
| 190 | 295-295 | rule | owise | `rule isIntV(_:Val)         => false [owise]` |
| 191 | 296-296 | rule | ordinary | `rule isStrV(str(_:IntSeq)) => true` |
| 192 | 297-297 | rule | owise | `rule isStrV(_:Val)         => false [owise]` |

## /reference/reference-semantics/semantics/call.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 193 | 16-18 | rule | ordinary | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| 194 | 19-19 | syntax | ordinary | `syntax KItem ::= #callee(Exprs)` |
| 195 | 20-20 | rule | owise | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 196 | 21-23 | rule | ordinary | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| 197 | 24-25 | rule | ordinary | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 198 | 26-26 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 199 | 27-27 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>` |
| 200 | 28-28 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>` |
| 201 | 29-29 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>` |
| 202 | 30-30 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>` |
| 203 | 31-31 | rule | owise | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 204 | 32-37 | rule | ordinary | `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>` |
| 205 | 38-41 | rule | priority(40) | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 206 | 42-46 | rule | priority(40) | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]` |
| 207 | 47-51 | rule | priority(40) | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 208 | 52-52 | syntax | function, total | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 209 | 53-55 | rule | ordinary | `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"` |
| 210 | 56-62 | rule | priority(40) | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]` |
| 211 | 63-68 | rule | priority(40) | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]` |
| 212 | 69-79 | rule | ordinary | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| 213 | 80-86 | rule | ordinary | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>` |
| 214 | 87-87 | syntax | ordinary | `syntax KItem ::= #allocCells(ParamNames)` |
| 215 | 88-88 | rule | ordinary | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 216 | 89-94 | rule | ordinary | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N \|-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |

## /reference/reference-semantics/semantics/comprehension.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 217 | 11-11 | rule | ordinary | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 218 | 12-13 | rule | ordinary | `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 219 | 14-14 | syntax | macro | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 220 | 15-17 | rule | ordinary | `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))` |
| 221 | 18-18 | syntax | macro | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 222 | 19-20 | rule | ordinary | `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))` |
| 223 | 21-23 | rule | ordinary | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))` |
| 224 | 24-24 | syntax | macro | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 225 | 25-25 | rule | ordinary | `rule compGuard(.Exprs)             => Bool(true)` |
| 226 | 26-26 | rule | ordinary | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |

## /reference/reference-semantics/semantics/concrete.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 227 | 13-15 | rule | ordinary | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 228 | 16-24 | rule | ordinary | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)` |
| 229 | 25-25 | syntax | ordinary | `syntax Val ::= kvP(Val, Val)` |
| 230 | 26-27 | syntax | ordinary | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) \| #ksIns(Val, ValSeq, Val, ValSeq, Bool)` |
| 231 | 28-30 | rule | priority(40) | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]` |
| 232 | 31-33 | rule | priority(40) | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]` |
| 233 | 34-35 | rule | ordinary | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>` |
| 234 | 36-37 | rule | ordinary | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>` |
| 235 | 38-41 | rule | ordinary | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)` |
| 236 | 42-42 | syntax | function | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 237 | 43-43 | rule | ordinary | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 238 | 44-46 | rule | ordinary | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)` |
| 239 | 47-50 | rule | ordinary | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)` |
| 240 | 51-51 | syntax | function | `syntax Bool ::= kLt(Val, Val) [function]` |
| 241 | 52-52 | rule | ordinary | `rule kLt(I1:Int, I2:Int)             => I1 <Int I2` |
| 242 | 53-53 | rule | ordinary | `rule kLt(F1:Float, F2:Float)         => F1 <Float F2` |
| 243 | 54-55 | rule | ordinary | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 244 | 56-56 | syntax | function, total | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 245 | 57-57 | rule | ordinary | `rule unpairVS(.ValSeq) => .ValSeq` |
| 246 | 58-58 | rule | ordinary | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 247 | 59-59 | rule | owise | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |

## /reference/reference-semantics/semantics/controls.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 248 | 9-11 | rule | ordinary | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 249 | 12-19 | rule | priority(40) | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 250 | 20-26 | rule | ordinary | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)` |
| 251 | 27-34 | rule | priority(40) | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]` |
| 252 | 35-35 | rule | ordinary | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 253 | 36-36 | rule | owise | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 254 | 37-37 | syntax | ordinary | `syntax KItem ::= #bindImports(ParamNames)` |
| 255 | 38-38 | rule | ordinary | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 256 | 39-42 | rule | ordinary | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"` |
| 257 | 43-47 | rule | ordinary | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")` |
| 258 | 48-50 | rule | ordinary | `rule <k> Expr(_:Val) => .K ... </k>` |
| 259 | 51-51 | syntax | ordinary | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 260 | 52-52 | rule | ordinary | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 261 | 53-53 | rule | ordinary | `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>` |
| 262 | 54-56 | rule | ordinary | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| 263 | 57-58 | rule | ordinary | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)` |
| 264 | 59-64 | rule | ordinary | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)` |
| 265 | 65-68 | syntax | ordinary | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts) \| #while(Expr, Stmts) \| #whileCond(Expr, Stmts) \| #loopLbl(K) \| "#cont" \| "#brk"` |
| 266 | 69-70 | rule | ordinary | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 267 | 71-71 | rule | ordinary | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 268 | 72-72 | rule | ordinary | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 269 | 73-76 | rule | ordinary | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>` |
| 270 | 77-77 | rule | ordinary | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 271 | 78-78 | rule | ordinary | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 272 | 79-80 | rule | ordinary | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)` |
| 273 | 81-84 | rule | ordinary | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)` |
| 274 | 85-85 | rule | ordinary | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 275 | 86-86 | rule | ordinary | `rule <k> Continue => #cont ... </k>` |
| 276 | 87-87 | rule | ordinary | `rule <k> Break => #brk ... </k>` |
| 277 | 88-88 | rule | ordinary | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 278 | 89-89 | rule | owise | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 279 | 90-90 | rule | ordinary | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 280 | 91-94 | rule | owise | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| 281 | 95-97 | rule | priority(40) | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 282 | 98-100 | rule | priority(40) | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 283 | 101-105 | rule | priority(40) | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 284 | 106-108 | rule | priority(40) | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |

## /reference/reference-semantics/semantics/core.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 285 | 13-13 | syntax | ordinary | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 286 | 14-14 | syntax | ordinary | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 287 | 15-17 | syntax | ordinary | `syntax Str    ::= str(IntSeq)` |
| 288 | 18-24 | syntax | ordinary | `syntax Iterable ::= list(ValSeq) \| tuple(ValSeq) \| Str \| rangeObj(Int, Int, Int) \| zipObj(ValSeq, ValSeq) \| zipObjS(IntSeq, IntSeq)` |
| 289 | 25-35 | syntax | ordinary | `syntax Val      ::= Int \| Bool \| "noneV" \| Iterable \| ref(Int) \| cellRef(Int) \| closureVal(ParamNames, Stmts, Int) \| typeV(String) \| builtinV(String) \| boundMethodV(Val, String)` |
| 290 | 36-36 | syntax | ordinary | `syntax Parent   ::= "root" \| parent(Int)` |
| 291 | 37-37 | syntax | ordinary | `syntax Scope    ::= scope(Map, Parent)` |
| 292 | 38-38 | syntax | ordinary | `syntax KResult  ::= Val` |
| 293 | 39-39 | syntax | ordinary | `syntax Expr     ::= Val` |
| 294 | 40-40 | syntax | ordinary | `syntax Vals     ::= List{Val, ","}` |
| 295 | 41-41 | syntax | ordinary | `syntax Exc      ::= "NoExc" \| "AssertionError"` |
| 296 | 42-48 | syntax | ordinary | `syntax RetState ::= "noRet" \| retV(Val)` |
| 297 | 49-67 | configuration | ordinary | `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     \|-> scope(.Map, parent(-1)) -1    \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code>` |
| 298 | 68-68 | syntax | function, total | `syntax Bool ::= isRefV(Val) [function, total]` |
| 299 | 69-69 | rule | ordinary | `rule isRefV(ref(_:Int)) => true` |
| 300 | 70-74 | rule | owise | `rule isRefV(_:Val)      => false [owise]` |
| 301 | 75-75 | syntax | ordinary | `syntax HeapVal ::= cellV(Val)` |
| 302 | 76-76 | syntax | function, total | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 303 | 77-77 | rule | ordinary | `rule isCellRef(cellRef(_:Int)) => true` |
| 304 | 78-84 | rule | owise | `rule isCellRef(_:Val)          => false [owise]` |
| 305 | 85-94 | rule | priority(40) | `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]` |
| 306 | 95-95 | syntax | ordinary | `syntax Val ::= kwV(String, Val)` |
| 307 | 96-96 | syntax | ordinary | `syntax KItem ::= #kwTag(String)` |
| 308 | 97-97 | rule | ordinary | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 309 | 98-99 | rule | ordinary | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)` |
| 310 | 100-100 | syntax | function, total | `syntax Bool ::= isKwV(Val) [function, total]` |
| 311 | 101-101 | rule | ordinary | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 312 | 102-105 | rule | owise | `rule isKwV(_:Val)                => false [owise]` |
| 313 | 106-106 | syntax | ordinary | `syntax Val ::= cellsMark(ParamNames)` |
| 314 | 107-107 | syntax | function | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 315 | 108-108 | rule | ordinary | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 316 | 109-109 | syntax | function, total | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 317 | 110-110 | rule | ordinary | `rule pnMember(_:String, .ParamNames) => false` |
| 318 | 111-112 | rule | ordinary | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 319 | 113-113 | syntax | ordinary | `syntax KItem ::= #cellW(Val, Val)` |
| 320 | 114-116 | rule | ordinary | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H \|-> cellV(_:Val => V) ... </heap>` |
| 321 | 117-117 | syntax | ordinary | `syntax KItem ::= #alloc(Val)` |
| 322 | 118-123 | rule | ordinary | `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N \|-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)` |
| 323 | 124-124 | syntax | ordinary | `syntax KItem ::= #loadAll(Module)` |
| 324 | 125-125 | rule | ordinary | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 325 | 126-126 | rule | ordinary | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 326 | 127-129 | rule | ordinary | `rule <k> .Stmts => .K ... </k>` |
| 327 | 130-130 | syntax | ordinary | `syntax KItem ::= #look(String, Int)` |
| 328 | 131-131 | rule | ordinary | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 329 | 132-144 | rule | ordinary | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)` |
| 330 | 145-151 | rule | priority(40) | `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L \|-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H \|-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]` |
| 331 | 152-156 | rule | ordinary | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L \|-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))` |
| 332 | 157-157 | syntax | function, total | `syntax Scope ::= "builtinsScope" [function, total]` |
| 333 | 158-184 | rule | ordinary | `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root)` |
| 334 | 185-185 | syntax | ordinary | `syntax ApplyK ::= toCall(Val)` |
| 335 | 186-188 | syntax | ordinary | `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) \| #evalArgCont(Exprs, Vals, ApplyK) \| #applyK(ApplyK, Vals)` |
| 336 | 189-189 | rule | ordinary | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 337 | 190-190 | rule | ordinary | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 338 | 191-193 | rule | ordinary | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| 339 | 194-194 | rule | ordinary | `rule <k> Int(I:Int)   => I ... </k>` |
| 340 | 195-195 | rule | ordinary | `rule <k> Bool(B:Bool) => B ... </k>` |
| 341 | 196-198 | rule | ordinary | `rule <k> NoneVal      => noneV ... </k>` |
| 342 | 199-199 | syntax | function | `syntax Bool ::= truthy(Val) [function]` |
| 343 | 200-200 | rule | ordinary | `rule truthy(B:Bool)          => B` |
| 344 | 201-201 | rule | ordinary | `rule truthy(noneV)           => false` |
| 345 | 202-202 | rule | ordinary | `rule truthy(I:Int)           => I =/=Int 0` |
| 346 | 203-203 | rule | ordinary | `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)` |
| 347 | 204-204 | rule | ordinary | `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)` |
| 348 | 205-207 | rule | ordinary | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 349 | 208-208 | syntax | function | `syntax Val  ::= applyUn(String, Val) [function]` |
| 350 | 209-209 | syntax | function | `syntax Val  ::= applyBin(String, Val, Val) [function]` |
| 351 | 210-212 | syntax | function | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| 352 | 213-213 | syntax | function, total | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 353 | 214-214 | rule | ordinary | `rule appendVal(.Vals, V:Val)              => V , .Vals` |
| 354 | 215-216 | rule | ordinary | `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)` |
| 355 | 217-217 | syntax | function, total | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 356 | 218-218 | rule | ordinary | `rule vals2valSeq(.Vals)            => .ValSeq` |
| 357 | 219-222 | rule | ordinary | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| 358 | 223-223 | syntax | function, total | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 359 | 224-224 | rule | ordinary | `rule vsLen(.ValSeq)                => 0` |
| 360 | 225-226 | rule | ordinary | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 361 | 227-227 | syntax | function, total | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 362 | 228-228 | rule | ordinary | `rule isLen(.IntSeq)                => 0` |
| 363 | 229-232 | rule | ordinary | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| 364 | 233-233 | syntax | function, total | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 365 | 234-234 | rule | ordinary | `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq` |
| 366 | 235-235 | rule | ordinary | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)` |
| 367 | 236-237 | rule | ordinary | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0` |
| 368 | 238-239 | rule | ordinary | `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0` |

## /reference/reference-semantics/semantics/dict.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 369 | 20-22 | syntax | ordinary | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| 370 | 23-25 | syntax | ordinary | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) \| #dictKey(Expr, Entries, ValSeq, ValSeq) \| #dictVal(Val, Entries, ValSeq, ValSeq)` |
| 371 | 26-26 | rule | ordinary | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 372 | 27-27 | rule | ordinary | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 373 | 28-29 | rule | ordinary | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>` |
| 374 | 30-31 | rule | ordinary | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>` |
| 375 | 32-36 | rule | ordinary | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>` |
| 376 | 37-37 | syntax | function, total | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 377 | 38-38 | rule | ordinary | `rule dHasKey(.ValSeq, _:Val)                => false` |
| 378 | 39-39 | rule | ordinary | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K` |
| 379 | 40-42 | rule | ordinary | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| 380 | 43-43 | syntax | function, total | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 381 | 44-44 | rule | ordinary | `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)` |
| 382 | 45-48 | rule | ordinary | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| 383 | 49-49 | syntax | function, total | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 384 | 50-51 | rule | ordinary | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K` |
| 385 | 52-53 | rule | ordinary | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)` |
| 386 | 54-57 | rule | owise | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| 387 | 58-62 | rule | priority(40) | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]` |
| 388 | 63-63 | rule | ordinary | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 389 | 64-64 | syntax | function | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 390 | 65-69 | rule | priority(45) | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]` |
| 391 | 70-70 | syntax | function | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 392 | 71-75 | rule | ordinary | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| 393 | 76-76 | syntax | ordinary | `syntax KItem ::= #dsetK(String, Val)` |
| 394 | 77-77 | rule | ordinary | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 395 | 78-81 | rule | ordinary | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)` |
| 396 | 82-85 | rule | ordinary | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)` |
| 397 | 86-86 | syntax | ordinary | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 398 | 87-89 | rule | ordinary | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H \|-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>` |
| 399 | 90-90 | syntax | function, total | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 400 | 91-91 | rule | ordinary | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 401 | 92-94 | rule | ordinary | `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0` |
| 402 | 95-96 | rule | ordinary | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)` |
| 403 | 97-97 | syntax | function | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 404 | 98-98 | rule | ordinary | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 405 | 99-100 | rule | ordinary | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)` |
| 406 | 101-101 | syntax | function | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 407 | 102-102 | rule | ordinary | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K` |
| 408 | 103-103 | rule | ordinary | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |

## /reference/reference-semantics/semantics/float.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 409 | 20-20 | syntax | ordinary | `syntax Val ::= Float` |
| 410 | 21-23 | rule | ordinary | `rule <k> Float(F:Float) => F ... </k>` |
| 411 | 24-24 | syntax | function, symbol(intFloatDiv), total | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 412 | 25-26 | rule | concrete | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 413 | 27-29 | rule | ordinary | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| 414 | 30-30 | syntax | function, symbol(divII), total | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 415 | 31-31 | rule | concrete | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 416 | 32-36 | rule | ordinary | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| 417 | 37-37 | syntax | function, symbol(floatMod), total | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 418 | 38-38 | rule | concrete | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 419 | 39-42 | rule | ordinary | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| 420 | 43-43 | rule | ordinary | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 421 | 44-49 | rule | ordinary | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| 422 | 50-50 | syntax | function, symbol(floatLt), total | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 423 | 51-51 | rule | concrete | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 424 | 52-53 | rule | ordinary | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 425 | 54-54 | syntax | function, symbol(absF), total | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 426 | 55-55 | rule | concrete | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 427 | 56-60 | rule | ordinary | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| 428 | 61-64 | rule | ordinary | `rule <k> Import(_:String) => .K ... </k>` |
| 429 | 65-65 | syntax | ordinary | `syntax KItem ::= "#mathCeil"` |
| 430 | 66-66 | rule | priority(40) | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 431 | 67-69 | rule | ordinary | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| 432 | 70-70 | syntax | ordinary | `syntax KItem ::= "#mathFloor"` |
| 433 | 71-71 | rule | priority(40) | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 434 | 72-72 | rule | ordinary | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 435 | 73-73 | syntax | function, symbol(floorFI), total | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 436 | 74-74 | rule | concrete | `rule floorFI(I:Int)   => I                        [concrete]` |
| 437 | 75-77 | rule | concrete | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| 438 | 78-78 | rule | ordinary | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 439 | 79-81 | rule | ordinary | `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)` |
| 440 | 82-82 | syntax | ordinary | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 441 | 83-83 | rule | priority(40) | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 442 | 84-84 | rule | ordinary | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 443 | 85-85 | rule | ordinary | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 444 | 86-86 | syntax | function, symbol(toF), total | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 445 | 87-87 | rule | concrete | `rule toF(F:Float) => F        [concrete]` |
| 446 | 88-92 | rule | concrete | `rule toF(I:Int)   => intToF(I) [concrete]` |
| 447 | 93-93 | syntax | function, symbol(ceilF), total | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 448 | 94-94 | rule | concrete | `rule ceilF(I:Int)   => I                       [concrete]` |
| 449 | 95-98 | rule | concrete | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| 450 | 99-102 | rule | ordinary | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| 451 | 103-103 | syntax | function, symbol(subF), total | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 452 | 104-104 | rule | concrete | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 453 | 105-106 | rule | ordinary | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 454 | 107-107 | syntax | function, symbol(divF), total | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 455 | 108-108 | rule | concrete | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 456 | 109-110 | rule | ordinary | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 457 | 111-111 | syntax | function, symbol(addF), total | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 458 | 112-112 | rule | concrete | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 459 | 113-114 | rule | ordinary | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 460 | 115-115 | syntax | function, symbol(mulF), total | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 461 | 116-116 | rule | concrete | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 462 | 117-118 | rule | ordinary | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 463 | 119-119 | syntax | function, symbol(powF), total | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 464 | 120-120 | rule | concrete | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 465 | 121-124 | rule | ordinary | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| 466 | 125-125 | syntax | function, symbol(gtF), total | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 467 | 126-126 | rule | concrete | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 468 | 127-127 | rule | ordinary | `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)` |
| 469 | 128-128 | rule | ordinary | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 470 | 129-131 | rule | ordinary | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| 471 | 132-132 | rule | ordinary | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 472 | 133-133 | rule | ordinary | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 473 | 134-134 | rule | ordinary | `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)` |
| 474 | 135-135 | rule | ordinary | `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))` |
| 475 | 136-136 | rule | ordinary | `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)` |
| 476 | 137-137 | rule | ordinary | `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))` |
| 477 | 138-138 | rule | ordinary | `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)` |
| 478 | 139-141 | rule | ordinary | `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))` |
| 479 | 142-142 | syntax | function, symbol(eqF), total | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 480 | 143-143 | rule | concrete | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 481 | 144-144 | rule | ordinary | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 482 | 145-145 | rule | ordinary | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 483 | 146-146 | rule | ordinary | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 484 | 147-147 | rule | ordinary | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 485 | 148-148 | rule | ordinary | `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)` |
| 486 | 149-149 | rule | ordinary | `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))` |
| 487 | 150-150 | rule | ordinary | `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)` |
| 488 | 151-153 | rule | ordinary | `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))` |
| 489 | 154-154 | rule | ordinary | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 490 | 155-159 | rule | ordinary | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| 491 | 160-160 | syntax | function, symbol(decStrToF), total | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 492 | 161-161 | rule | concrete | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 493 | 162-164 | rule | concrete | `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]` |
| 494 | 165-165 | syntax | function | `syntax Int ::= headIS(IntSeq) [function]` |
| 495 | 166-166 | rule | ordinary | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 496 | 167-167 | syntax | function, total | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 497 | 168-168 | rule | ordinary | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 498 | 169-169 | rule | ordinary | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 499 | 170-170 | rule | ordinary | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 500 | 171-172 | rule | ordinary | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46` |
| 501 | 173-173 | syntax | function, total | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 502 | 174-174 | rule | ordinary | `rule fracPart(.IntSeq) => 0` |
| 503 | 175-175 | rule | ordinary | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 504 | 176-176 | rule | ordinary | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 505 | 177-177 | rule | ordinary | `rule fracAcc(.IntSeq, A:Int) => A` |
| 506 | 178-178 | rule | ordinary | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 507 | 179-179 | syntax | function, total | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 508 | 180-180 | rule | ordinary | `rule fracScale(.IntSeq) => 1` |
| 509 | 181-181 | rule | ordinary | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 510 | 182-182 | rule | ordinary | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 511 | 183-183 | rule | ordinary | `rule fscAcc(.IntSeq, A:Int) => A` |
| 512 | 184-184 | rule | ordinary | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 513 | 185-185 | rule | ordinary | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 514 | 186-186 | rule | ordinary | `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)` |
| 515 | 187-189 | rule | ordinary | `rule applyBuiltin("float", F:Float, .Vals)        => F` |
| 516 | 190-190 | syntax | function, symbol(divFloatIntV), total | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 517 | 191-191 | rule | concrete | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 518 | 192-194 | rule | ordinary | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| 519 | 195-195 | syntax | function, symbol(intToF), total | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 520 | 196-196 | rule | concrete | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 521 | 197-197 | rule | ordinary | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 522 | 198-198 | rule | ordinary | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 523 | 199-199 | rule | ordinary | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 524 | 200-200 | rule | ordinary | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 525 | 201-201 | rule | ordinary | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 526 | 202-202 | rule | ordinary | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 527 | 203-203 | rule | ordinary | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 528 | 204-204 | rule | ordinary | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 529 | 205-205 | rule | ordinary | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 530 | 206-208 | rule | ordinary | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| 531 | 209-209 | syntax | function, symbol(truncF), total | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 532 | 210-210 | rule | concrete | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 533 | 211-212 | rule | ordinary | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 534 | 213-213 | rule | ordinary | `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)` |
| 535 | 214-216 | rule | ordinary | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| 536 | 217-217 | syntax | function, symbol(roundF), total | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 537 | 218-222 | rule | concrete | `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]` |
| 538 | 223-223 | syntax | function, symbol(roundFN), total | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 539 | 224-226 | rule | concrete | `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]` |
| 540 | 227-227 | rule | ordinary | `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)` |
| 541 | 228-229 | rule | ordinary | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 542 | 230-230 | syntax | function, symbol(sqrtF), total | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 543 | 231-231 | rule | concrete | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 544 | 232-232 | syntax | ordinary | `syntax KItem ::= "#mathSqrt"` |
| 545 | 233-233 | rule | priority(40) | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 546 | 234-234 | rule | ordinary | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 547 | 235-242 | rule | ordinary | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| 548 | 243-243 | syntax | ordinary | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 549 | 244-244 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 550 | 245-245 | rule | ordinary | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 551 | 246-246 | rule | ordinary | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 552 | 247-249 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 553 | 250-250 | syntax | ordinary | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 554 | 251-251 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 555 | 252-252 | rule | ordinary | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 556 | 253-253 | rule | ordinary | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 557 | 254-260 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)` |
| 558 | 261-261 | syntax | ordinary | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 559 | 262-264 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))` |
| 560 | 265-265 | rule | ordinary | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 561 | 266-266 | rule | ordinary | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 562 | 267-269 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)` |
| 563 | 270-272 | rule | ordinary | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)` |

## /reference/reference-semantics/semantics/functions.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 564 | 8-13 | syntax | ordinary | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) \| #bindP(ParamNames, Vals) \| "#pop" \| "#endcall"` |
| 565 | 14-17 | rule | ordinary | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>` |
| 566 | 18-18 | syntax | ordinary | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 567 | 19-26 | rule | ordinary | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>` |
| 568 | 27-30 | syntax | ordinary | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| 569 | 31-32 | syntax | ordinary | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) \| #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 570 | 33-35 | rule | ordinary | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>` |
| 571 | 36-41 | rule | ordinary | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 572 | 42-46 | rule | ordinary | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>` |
| 573 | 47-49 | rule | ordinary | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>` |
| 574 | 50-52 | rule | ordinary | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>` |
| 575 | 53-58 | rule | ordinary | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)` |
| 576 | 59-62 | rule | ordinary | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>` |
| 577 | 63-63 | rule | ordinary | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 578 | 64-67 | rule | ordinary | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ P <- V ], _) ... </scopes>` |
| 579 | 68-77 | rule | priority(40) | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]` |
| 580 | 78-79 | rule | ordinary | `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>` |
| 581 | 80-84 | rule | ordinary | `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>` |
| 582 | 85-90 | rule | ordinary | `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>` |

## /reference/reference-semantics/semantics/int.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 583 | 7-8 | rule | ordinary | `rule applyUn("-", I:Int) => 0 -Int I` |
| 584 | 9-10 | rule | ordinary | `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2` |
| 585 | 11-11 | rule | ordinary | `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 586 | 12-12 | rule | ordinary | `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 587 | 13-13 | rule | ordinary | `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2` |
| 588 | 14-14 | rule | ordinary | `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2` |
| 589 | 15-15 | rule | ordinary | `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)` |
| 590 | 16-16 | rule | ordinary | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 591 | 17-18 | rule | ordinary | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 592 | 19-19 | syntax | function | `syntax Int ::= pyMod(Int, Int) [function]` |
| 593 | 20-21 | rule | ordinary | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 594 | 22-22 | rule | ordinary | `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2` |
| 595 | 23-23 | rule | ordinary | `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2` |
| 596 | 24-24 | rule | ordinary | `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2` |
| 597 | 25-25 | rule | ordinary | `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2` |
| 598 | 26-26 | rule | ordinary | `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2` |
| 599 | 27-27 | rule | ordinary | `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2` |

## /reference/reference-semantics/semantics/iter.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 600 | 8-8 | syntax | ordinary | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |

## /reference/reference-semantics/semantics/list.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 601 | 9-9 | rule | ordinary | `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>` |
| 602 | 10-12 | rule | ordinary | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| 603 | 13-13 | syntax | ordinary | `syntax ApplyK ::= "toList"` |
| 604 | 14-14 | rule | ordinary | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 605 | 15-17 | rule | ordinary | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| 606 | 18-18 | syntax | function, total | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 607 | 19-19 | rule | ordinary | `rule valSeqConcat(.ValSeq, T:ValSeq)                => T` |
| 608 | 20-23 | rule | ordinary | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| 609 | 24-26 | rule | priority(45) | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]` |
| 610 | 27-27 | rule | ordinary | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 611 | 28-32 | rule | ordinary | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| 612 | 33-33 | syntax | function, total | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 613 | 34-34 | rule | ordinary | `rule hasRefVS(.ValSeq)                => false` |
| 614 | 35-36 | rule | ordinary | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 615 | 37-38 | syntax | function | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] \| deepEqV(Val, Val, Map)        [function]` |
| 616 | 39-39 | rule | ordinary | `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true` |
| 617 | 40-40 | rule | ordinary | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false` |
| 618 | 41-41 | rule | ordinary | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false` |
| 619 | 42-44 | rule | ordinary | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)` |
| 620 | 45-46 | rule | ordinary | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)` |
| 621 | 47-48 | rule | ordinary | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)` |
| 622 | 49-49 | rule | ordinary | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 623 | 50-52 | rule | owise | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| 624 | 53-57 | rule | priority(40) | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]` |
| 625 | 58-58 | syntax | ordinary | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 626 | 59-59 | rule | ordinary | `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 627 | 60-60 | rule | ordinary | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 628 | 61-61 | rule | ordinary | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 629 | 62-62 | rule | ordinary | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 630 | 63-64 | rule | ordinary | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V` |
| 631 | 65-66 | rule | ordinary | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)` |
| 632 | 67-67 | rule | ordinary | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |

## /reference/reference-semantics/semantics/methods.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 633 | 10-12 | syntax | function | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| 634 | 13-13 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 635 | 14-14 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 636 | 15-15 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 637 | 16-18 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| 638 | 19-19 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))` |
| 639 | 20-20 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))` |
| 640 | 21-25 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| 641 | 26-26 | rule | ordinary | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 642 | 27-27 | syntax | function, total | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 643 | 28-28 | rule | ordinary | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 644 | 29-29 | rule | ordinary | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 645 | 30-33 | rule | ordinary | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))` |
| 646 | 34-34 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 647 | 35-35 | syntax | function | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 648 | 36-36 | rule | ordinary | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 649 | 37-38 | rule | ordinary | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0` |
| 650 | 39-40 | rule | ordinary | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0` |
| 651 | 41-41 | syntax | function, total | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 652 | 42-42 | rule | ordinary | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 653 | 43-43 | rule | owise | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 654 | 44-46 | rule | ordinary | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| 655 | 47-47 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 656 | 48-48 | syntax | function, total | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 657 | 49-49 | rule | ordinary | `rule trimWS(.IntSeq) => .IntSeq` |
| 658 | 50-50 | rule | ordinary | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 659 | 51-51 | rule | ordinary | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 660 | 52-52 | syntax | function, total | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 661 | 53-53 | rule | ordinary | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 662 | 54-54 | rule | ordinary | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 663 | 55-57 | rule | ordinary | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| 664 | 58-60 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| 665 | 61-63 | rule | ordinary | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| 666 | 64-64 | rule | ordinary | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 667 | 65-65 | syntax | function, total | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 668 | 66-66 | rule | ordinary | `rule cntOccVS(.ValSeq, _:Val)                => 0` |
| 669 | 67-67 | rule | ordinary | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 670 | 68-71 | rule | ordinary | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)` |
| 671 | 72-74 | rule | priority(40) | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]` |
| 672 | 75-75 | syntax | function | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]` |
| 673 | 76-76 | rule | ordinary | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 674 | 77-78 | rule | ordinary | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)` |
| 675 | 79-81 | rule | ordinary | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)` |
| 676 | 82-82 | syntax | function | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 677 | 83-83 | rule | ordinary | `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC` |
| 678 | 84-84 | rule | ordinary | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 679 | 85-85 | syntax | function, total | `syntax Bool ::= isWSC(Int) [function, total]` |
| 680 | 86-88 | rule | ordinary | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| 681 | 89-93 | rule | priority(39) | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]` |
| 682 | 94-96 | rule | priority(40) | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]` |
| 683 | 97-97 | syntax | function | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]` |
| 684 | 98-98 | rule | ordinary | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)` |
| 685 | 99-100 | rule | ordinary | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP` |
| 686 | 101-103 | rule | ordinary | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)` |
| 687 | 104-105 | rule | ordinary | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))` |
| 688 | 106-106 | syntax | function, total | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 689 | 107-107 | rule | ordinary | `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq` |
| 690 | 108-108 | rule | ordinary | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 691 | 109-111 | rule | ordinary | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| 692 | 112-112 | syntax | function, total | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 693 | 113-114 | rule | ordinary | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 694 | 115-115 | syntax | function, total | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 695 | 116-117 | rule | ordinary | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 696 | 118-118 | syntax | function, total | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 697 | 119-120 | rule | ordinary | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 698 | 121-121 | syntax | function, total | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 699 | 122-123 | rule | ordinary | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 700 | 124-124 | syntax | function, total | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 701 | 125-125 | rule | ordinary | `rule hasUpper(.IntSeq) => false` |
| 702 | 126-127 | rule | ordinary | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 703 | 128-128 | syntax | function, total | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 704 | 129-129 | rule | ordinary | `rule hasLower(.IntSeq) => false` |
| 705 | 130-131 | rule | ordinary | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 706 | 132-132 | syntax | function, total | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 707 | 133-133 | rule | ordinary | `rule allAlpha(.IntSeq) => true` |
| 708 | 134-135 | rule | ordinary | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 709 | 136-136 | syntax | function, total | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 710 | 137-137 | rule | ordinary | `rule allDigit(.IntSeq) => true` |
| 711 | 138-139 | rule | ordinary | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 712 | 140-141 | syntax | function, total | `syntax Int ::= lowerC(Int) [function, total]` |
| 713 | 142-142 | rule | ordinary | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 714 | 143-144 | rule | owise | `rule lowerC(C:Int) => C         [owise]` |
| 715 | 145-145 | syntax | function, total | `syntax Int ::= upperC(Int) [function, total]` |
| 716 | 146-146 | rule | ordinary | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 717 | 147-148 | rule | owise | `rule upperC(C:Int) => C         [owise]` |
| 718 | 149-149 | syntax | function, total | `syntax Int ::= swapC(Int) [function, total]` |
| 719 | 150-150 | rule | ordinary | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 720 | 151-151 | rule | ordinary | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 721 | 152-153 | rule | owise | `rule swapC(C:Int) => C         [owise]` |
| 722 | 154-154 | syntax | function, total | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 723 | 155-155 | rule | ordinary | `rule mapLower(.IntSeq) => .IntSeq` |
| 724 | 156-157 | rule | ordinary | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 725 | 158-158 | syntax | function, total | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 726 | 159-159 | rule | ordinary | `rule mapUpper(.IntSeq) => .IntSeq` |
| 727 | 160-161 | rule | ordinary | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 728 | 162-162 | syntax | function, total | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 729 | 163-163 | rule | ordinary | `rule mapSwap(.IntSeq) => .IntSeq` |
| 730 | 164-165 | rule | ordinary | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 731 | 166-166 | syntax | function, total | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 732 | 167-167 | rule | ordinary | `rule startsWith(.IntSeq, _:IntSeq)               => true` |
| 733 | 168-168 | rule | ordinary | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 734 | 169-169 | rule | ordinary | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |

## /reference/reference-semantics/semantics/operators.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 735 | 10-11 | rule | ordinary | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 736 | 12-14 | rule | ordinary | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| 737 | 15-15 | context | ordinary | `context Compare(HOLE, _)` |
| 738 | 16-16 | context | ordinary | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 739 | 17-18 | rule | owise | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 740 | 19-19 | rule | ordinary | `rule applyCmp("is",     V:Val, noneV) => V ==K noneV` |
| 741 | 20-24 | rule | ordinary | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| 742 | 25-27 | rule | priority(40) | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 743 | 28-33 | rule | priority(40) | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]` |
| 744 | 34-37 | rule | priority(40) | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]` |
| 745 | 38-43 | rule | priority(40) | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H \|-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]` |
| 746 | 44-46 | rule | priority(40) | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |

## /reference/reference-semantics/semantics/range.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 747 | 9-9 | syntax | function, total | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 748 | 10-11 | rule | ordinary | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 749 | 12-12 | syntax | function | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 750 | 13-14 | rule | ordinary | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO` |
| 751 | 15-16 | rule | ordinary | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO` |
| 752 | 17-19 | rule | ordinary | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)` |
| 753 | 20-22 | rule | ordinary | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)` |
| 754 | 23-24 | rule | ordinary | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)` |

## /reference/reference-semantics/semantics/set.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 755 | 8-10 | syntax | ordinary | `syntax Val ::= setV(IntSeq)` |
| 756 | 11-11 | syntax | function, total | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 757 | 12-12 | rule | ordinary | `rule codeIn(_:Int, .IntSeq)                => false` |
| 758 | 13-15 | rule | ordinary | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| 759 | 16-17 | syntax | function, total | `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] \| dedupFrom(IntSeq, IntSeq)  [function, total]` |
| 760 | 18-18 | rule | ordinary | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 761 | 19-19 | rule | ordinary | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 762 | 20-21 | rule | ordinary | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)` |
| 763 | 22-24 | rule | ordinary | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)` |
| 764 | 25-25 | syntax | function, total | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 765 | 26-26 | rule | ordinary | `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)` |
| 766 | 27-30 | rule | ordinary | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| 767 | 31-31 | syntax | function, total | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 768 | 32-32 | rule | ordinary | `rule subsetCodes(.IntSeq, _:IntSeq)                => true` |
| 769 | 33-34 | rule | ordinary | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 770 | 35-35 | syntax | function, total | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 771 | 36-38 | rule | ordinary | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| 772 | 39-39 | rule | ordinary | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |

## /reference/reference-semantics/semantics/sort.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 773 | 18-18 | syntax | function, symbol(sortVS), total | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 774 | 19-19 | syntax | function | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 775 | 20-20 | rule | concrete | `rule sortVS(.ValSeq)                => .ValSeq          [concrete]` |
| 776 | 21-21 | rule | concrete | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 777 | 22-22 | rule | concrete | `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]` |
| 778 | 23-23 | rule | concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 779 | 24-25 | rule | concrete | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]` |
| 780 | 26-26 | syntax | function | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 781 | 27-27 | rule | concrete | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 782 | 28-28 | rule | concrete | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 783 | 29-30 | rule | concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]` |
| 784 | 31-35 | rule | concrete | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]` |
| 785 | 36-39 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>` |
| 786 | 40-48 | rule | priority(40) | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H \|-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]` |
| 787 | 49-50 | syntax | function, symbol(sortKeyVS), total | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 788 | 51-52 | syntax | function, total | `syntax ValSeq ::= revVS(ValSeq) [function, total] \| revVSAcc(ValSeq, ValSeq) [function, total]` |
| 789 | 53-53 | rule | ordinary | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 790 | 54-54 | rule | ordinary | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 791 | 55-56 | rule | ordinary | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 792 | 57-57 | syntax | function, total | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 793 | 58-58 | rule | ordinary | `rule condRev(S:ValSeq, false) => S` |
| 794 | 59-60 | rule | ordinary | `rule condRev(S:ValSeq, true)  => revVS(S)` |
| 795 | 61-62 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>` |
| 796 | 63-64 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>` |
| 797 | 65-71 | rule | ordinary | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>` |

## /reference/reference-semantics/semantics/str.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 798 | 8-8 | rule | ordinary | `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>` |
| 799 | 9-12 | rule | ordinary | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>` |
| 800 | 13-13 | syntax | function | `syntax IntSeq ::= strToCodes(String) [function]` |
| 801 | 14-14 | rule | ordinary | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 802 | 15-15 | rule | ordinary | `rule strToCodes("") => .IntSeq` |
| 803 | 16-19 | rule | ordinary | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128` |
| 804 | 20-20 | syntax | function, total | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 805 | 21-21 | rule | ordinary | `rule seqConcat(.IntSeq, T:IntSeq)                => T` |
| 806 | 22-23 | rule | ordinary | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 807 | 24-24 | rule | ordinary | `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 808 | 25-25 | rule | ordinary | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 809 | 26-28 | rule | ordinary | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| 810 | 29-29 | rule | ordinary | `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 811 | 30-31 | rule | ordinary | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 812 | 32-32 | syntax | function, total | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 813 | 33-33 | rule | ordinary | `rule strPrefix(.IntSeq, _:IntSeq)               => true` |
| 814 | 34-34 | rule | ordinary | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 815 | 35-36 | rule | ordinary | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 816 | 37-37 | syntax | function, total | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 817 | 38-38 | rule | ordinary | `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)` |
| 818 | 39-39 | rule | ordinary | `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)` |
| 819 | 40-47 | rule | ordinary | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))` |
| 820 | 48-48 | syntax | function, total | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 821 | 49-49 | rule | ordinary | `rule strLt(.IntSeq, .IntSeq)                => false` |
| 822 | 50-50 | rule | ordinary | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 823 | 51-51 | rule | ordinary | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 824 | 52-52 | rule | ordinary | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B` |
| 825 | 53-53 | rule | ordinary | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B` |
| 826 | 54-55 | rule | ordinary | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 827 | 56-56 | rule | ordinary | `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 828 | 57-57 | rule | ordinary | `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 829 | 58-58 | rule | ordinary | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 830 | 59-59 | rule | ordinary | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |

## /reference/reference-semantics/semantics/subscript.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 831 | 11-11 | syntax | function, total | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 832 | 12-12 | rule | ordinary | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V` |
| 833 | 13-15 | rule | ordinary | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0` |
| 834 | 16-16 | syntax | function | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 835 | 17-17 | rule | ordinary | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C` |
| 836 | 18-20 | rule | ordinary | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0` |
| 837 | 21-21 | syntax | function, total | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 838 | 22-22 | rule | ordinary | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 839 | 23-26 | rule | ordinary | `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0` |
| 840 | 27-27 | context | ordinary | `context Subscript(HOLE, _)` |
| 841 | 28-30 | context | ordinary | `context Subscript(_:Val, HOLE:Expr)` |
| 842 | 31-34 | rule | priority(40) | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 843 | 35-36 | rule | ordinary | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 844 | 37-37 | syntax | function | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 845 | 38-38 | rule | ordinary | `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 846 | 39-39 | rule | ordinary | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 847 | 40-43 | rule | ordinary | `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))` |
| 848 | 44-48 | syntax | ordinary | `syntax KItem ::= #evalB(Bound) \| "#toSome" \| #slLo(Val, Bound, Bound) \| #slHi(Val, OptInt, Bound) \| #slStep(Val, OptInt, OptInt)` |
| 849 | 49-49 | syntax | ordinary | `syntax OptInt ::= "noB" \| someB(Int)` |
| 850 | 50-50 | rule | ordinary | `rule <k> #evalB(NoBound)  => noB ... </k>` |
| 851 | 51-51 | rule | ordinary | `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>` |
| 852 | 52-53 | rule | ordinary | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 853 | 54-54 | rule | ordinary | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 854 | 55-55 | rule | ordinary | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 855 | 56-57 | rule | ordinary | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| 856 | 58-60 | rule | priority(45) | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]` |
| 857 | 61-62 | rule | ordinary | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 858 | 63-63 | syntax | function | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 859 | 64-65 | rule | ordinary | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 860 | 66-67 | rule | ordinary | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))` |
| 861 | 68-71 | rule | ordinary | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))` |
| 862 | 72-72 | syntax | function, total | `syntax Int ::= slStep(OptInt) [function, total]` |
| 863 | 73-73 | rule | ordinary | `rule slStep(noB)          => 1` |
| 864 | 74-75 | rule | ordinary | `rule slStep(someB(S:Int)) => S` |
| 865 | 76-76 | syntax | function | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 866 | 77-78 | rule | ordinary | `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0` |
| 867 | 79-80 | rule | ordinary | `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0` |
| 868 | 81-82 | rule | ordinary | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 869 | 83-83 | syntax | function | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 870 | 84-85 | rule | ordinary | `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0` |
| 871 | 86-87 | rule | ordinary | `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0` |
| 872 | 88-89 | rule | ordinary | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 873 | 90-90 | syntax | function, total | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 874 | 91-92 | rule | ordinary | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0` |
| 875 | 93-95 | rule | ordinary | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0` |
| 876 | 96-96 | syntax | function, total | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 877 | 97-98 | rule | ordinary | `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0` |
| 878 | 99-101 | rule | ordinary | `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0` |
| 879 | 102-102 | syntax | function, total | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 880 | 103-104 | rule | ordinary | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN` |
| 881 | 105-108 | rule | ordinary | `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN` |
| 882 | 109-109 | syntax | function | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 883 | 110-112 | rule | ordinary | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 884 | 113-115 | rule | ordinary | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |
| 885 | 116-116 | syntax | function | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 886 | 117-119 | rule | ordinary | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)` |
| 887 | 120-121 | rule | ordinary | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))` |

## /reference/reference-semantics/semantics/syntax.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 888 | 9-31 | syntax | macro, seqstrict(2, 3), strict(1), strict(2) | `syntax Expr ::= "Int"      "(" Int ")" \| "Float"    "(" Float ")" \| "Bool"     "(" Bool ")" \| "Name"     "(" String ")" \| "Str"      "(" String ")" \| "UnaryOp"  "(" String "," Expr ")" [strict(2)] \| "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] \| "BoolOp"    "(" String "," Exprs ")" \| "ListExpr"  "(" Exprs ")" \| "DictExpr"  "(" Entries ")" \| "ListComp"  "(" Expr "," CompFors ")" [macro] \| "GenExp"    "(" Expr "," CompFors ")" [macro] \| "TupleExpr" "(" Exprs ")" \| "Subscript" "(" Expr "," Index ")" \| "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] \| "Lambda"    "(" Params "," Expr ")" \| "KwArg"     "(" String "," Expr ")" \| "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" \| "NoneVal" \| "Call"      "(" Expr "," Exprs ")" \| "Attribute" "(" Expr "," String ")" [strict(1)] \| "Compare"   "(" Expr "," CmpOp ")"` |
| 889 | 32-32 | syntax | ordinary | `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"` |
| 890 | 33-33 | syntax | ordinary | `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"` |
| 891 | 34-34 | syntax | ordinary | `syntax Entries  ::= List{Entry, ","}` |
| 892 | 35-35 | syntax | ordinary | `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 893 | 36-36 | syntax | ordinary | `syntax CompFors ::= List{CompFor, ""}` |
| 894 | 37-37 | syntax | ordinary | `syntax Exprs    ::= List{Expr, ","}` |
| 895 | 38-38 | syntax | ordinary | `syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 896 | 39-40 | syntax | ordinary | `syntax Bound    ::= Expr \| "NoBound"` |
| 897 | 41-55 | syntax | strict, strict(1), strict(2), strict(3) | `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] \| "Import"    "(" String ")" \| "ImportFrom" "(" String "," ParamNames ")" \| "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] \| "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] \| "While"     "(" Expr "," Stmts ")" \| "Break" \| "Continue" \| "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] \| "Return"    "(" Expr ")" [strict] \| "Assert"    "(" Expr ")" [strict] \| "Expr"      "(" Expr ")" [strict] \| "FuncDef"   "(" String "," Params "," Stmts ")" \| "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"` |
| 898 | 56-56 | syntax | ordinary | `syntax Stmts      ::= List{Stmt, ""}` |
| 899 | 57-57 | syntax | ordinary | `syntax Params     ::= "Params" "(" ParamNames ")"` |
| 900 | 58-58 | syntax | ordinary | `syntax CellVars   ::= "CellVars" "(" ParamNames ")"` |
| 901 | 59-59 | syntax | ordinary | `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"` |
| 902 | 60-60 | syntax | ordinary | `syntax ParamNames ::= List{String, ","}` |
| 903 | 61-61 | syntax | ordinary | `syntax Module     ::= "Module" "(" Stmts ")"` |

## /reference/reference-semantics/semantics/tuple.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 904 | 10-10 | rule | ordinary | `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>` |
| 905 | 11-13 | rule | ordinary | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| 906 | 14-14 | syntax | ordinary | `syntax ApplyK ::= "toTuple"` |
| 907 | 15-15 | rule | ordinary | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 908 | 16-17 | rule | ordinary | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 909 | 18-19 | rule | ordinary | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| 910 | 20-20 | rule | ordinary | `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 911 | 21-22 | rule | ordinary | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| 912 | 23-23 | rule | ordinary | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 913 | 24-24 | syntax | function | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 914 | 25-25 | rule | ordinary | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 915 | 26-27 | rule | ordinary | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)` |
| 916 | 28-30 | rule | ordinary | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| 917 | 31-31 | syntax | ordinary | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 918 | 32-34 | rule | ordinary | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map => M [ X <- V ], _) ... </scopes>` |
| 919 | 35-41 | rule | priority(40) | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L \|-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]` |
| 920 | 42-42 | rule | ordinary | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 921 | 43-43 | rule | ordinary | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 922 | 44-48 | rule | priority(40) | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 923 | 49-49 | syntax | ordinary | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 924 | 50-50 | rule | ordinary | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 925 | 51-51 | rule | ordinary | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 926 | 52-54 | rule | priority(40) | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H \|-> V:Val ... </heap> [priority(40)]` |
| 927 | 55-56 | rule | ordinary | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>` |
| 928 | 57-57 | rule | ordinary | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |

## /candidate/verification-base.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 929 | 9-9 | syntax | macro | `syntax Stmts ::= "smallestLoopBody" [macro]` |
| 930 | 10-25 | rule | ordinary | `rule smallestLoopBody => If( Compare( Subscript(Name("arr"), Name("i")), CmpOp( "!=", Subscript( Name("arr"), BinOp( "-", BinOp("-", Call(Name("len"), Name("arr")), Name("i")), Int(1))))), AugAssign(Name("changes"), "+", Int(1)), .Stmts) AugAssign(Name("i"), "+", Int(1))` |
| 931 | 26-26 | syntax | macro | `syntax Stmts ::= "smallestBody" [macro]` |
| 932 | 27-41 | rule | ordinary | `rule smallestBody => Assign(Name("changes"), Int(0)) Assign(Name("i"), Int(0)) While( Compare( Name("i"), CmpOp( "<", BinOp( "//", Call(Name("len"), Name("arr")), Int(2)))), smallestLoopBody) Return(Name("changes"))` |
| 933 | 42-42 | syntax | macro | `syntax Stmt ::= "smallestDef" [macro]` |
| 934 | 43-47 | rule | ordinary | `rule smallestDef => FuncDef("smallest_change", Params("arr"), smallestBody)` |
| 935 | 48-48 | syntax | macro | `syntax Scope ::= "fixedBuiltins" [macro]` |
| 936 | 49-76 | rule | ordinary | `rule fixedBuiltins => scope("len" \|-> builtinV("len") "set" \|-> builtinV("set") "sum" \|-> builtinV("sum") "abs" \|-> builtinV("abs") "min" \|-> builtinV("min") "max" \|-> builtinV("max") "ord" \|-> builtinV("ord") "chr" \|-> builtinV("chr") "range" \|-> builtinV("range") "all" \|-> builtinV("all") "any" \|-> builtinV("any") "zip" \|-> builtinV("zip") "isinstance" \|-> builtinV("isinstance") "sorted" \|-> builtinV("sorted") "list" \|-> builtinV("list") "round" \|-> builtinV("round") "bin" \|-> builtinV("bin") "enumerate" \|-> builtinV("enumerate") "map" \|-> builtinV("map") "eval" \|-> builtinV("eval") "int" \|-> typeV("int") "str" \|-> typeV("str") "float" \|-> typeV("float"), root)` |
| 937 | 77-77 | syntax | function, total | `syntax Bool ::= allInts(ValSeq) [function, total]` |
| 938 | 78-78 | rule | ordinary | `rule allInts(.ValSeq)                => true` |
| 939 | 79-81 | rule | ordinary | `rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R)` |
| 940 | 82-82 | syntax | function, total | `syntax Int ::= halfLen(ValSeq) [function, total]` |
| 941 | 83-93 | rule | simplification | `rule halfLen(VS:ValSeq) => (vsLen(VS) -Int (((vsLen(VS) %Int 2) +Int 2) %Int 2)) /Int 2 [simplification]` |
| 942 | 94-107 | rule | simplification | `rule #Ceil( applyCmp( "!=", valSeqAt(VS:ValSeq, I:Int), valSeqAt(VS, vsLen(VS) -Int I +Int -1))) => #Top requires allInts(VS) andBool 0 <=Int I andBool I <Int halfLen(VS) [simplification]` |
| 943 | 108-130 | rule | ordinary | `rule <k> #branch( B:Bool, AugAssign(Name("changes"), "+", Int(1)), .Stmts) => .K ... </k> <env> 1 </env> <scopes> 1 \|-> scope( "arr" \|-> list(VS:ValSeq) "changes" \|-> (C:Int => C +Int (#if B #then 1 #else 0 #fi)) "i" \|-> I:Int, parent(0)) REST:Map </scopes>` |
| 944 | 131-131 | syntax | function | `syntax Int ::= pairDiff(ValSeq, Int) [function]` |
| 945 | 132-141 | rule | ordinary | `rule pairDiff(VS:ValSeq, I:Int) => #if applyCmp( "!=", valSeqAt(VS, I), valSeqAt(VS, vsLen(VS) -Int I -Int 1)) #then 1 #else 0 #fi` |
| 946 | 142-142 | syntax | function | `syntax Int ::= mismatchCount(ValSeq, Int, Int) [function]` |
| 947 | 143-144 | rule | ordinary | `rule mismatchCount(_VS:ValSeq, I:Int, STOP:Int) => 0 requires I >=Int STOP` |
| 948 | 145-148 | rule | ordinary | `rule mismatchCount(VS:ValSeq, I:Int, STOP:Int) => pairDiff(VS, I) +Int mismatchCount(VS, I +Int 1, STOP) requires I <Int STOP` |
| 949 | 149-151 | rule | simplification | `rule (A:Int +Int B:Int) +Int C:Int => A +Int (B +Int C) [simplification]` |

## /candidate/verification.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 950 | 9-56 | rule | priority(40) | `rule <k> #while( Compare( Name("i"), CmpOp( "<", BinOp( "//", Call(Name("len"), Name("arr")), Int(2)))), smallestLoopBody) ~> (Return(Name("changes")) .Stmts):Stmts ~> #endcall => mismatchCount(VS, 0, halfLen(VS)) </k> <env> 1 => 0 </env> <scopes> -1 \|-> fixedBuiltins 0 \|-> scope( "smallest_change" \|-> closureVal("arr", smallestBody, 0), parent(-1)) 1 \|-> scope( "arr" \|-> list(VS:ValSeq) "changes" \|-> 0 "i" \|-> 0, parent(0)) => -1 \|-> fixedBuiltins 0 \|-> scope( "smallest_change" \|-> closureVal("arr", smallestBody, 0), parent(-1)) </scopes> <scopeLoc> 2 => 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> ListItem(frame(.K, 0, 1)) => .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allInts(VS) [priority(40)]` |

## /candidate/spec.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 951 | 9-60 | claim | ordinary | `claim [loop-invariant]: <k> #while( Compare( Name("i"), CmpOp( "<", BinOp( "//", Call(Name("len"), Name("arr")), Int(2)))), smallestLoopBody) ~> (Return(Name("changes")) .Stmts):Stmts ~> #endcall => C +Int mismatchCount(VS, I, halfLen(VS)) </k> <env> 1 => 0 </env> <scopes> -1 \|-> builtinsScope 0 \|-> scope( "smallest_change" \|-> closureVal("arr", smallestBody, 0), parent(-1)) 1 \|-> scope( "arr" \|-> list(VS:ValSeq) "changes" \|-> C:Int "i" \|-> I:Int, parent(0)) => -1 \|-> builtinsScope 0 \|-> scope( "smallest_change" \|-> closureVal("arr", smallestBody, 0), parent(-1)) </scopes> <scopeLoc> 2 => 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> ListItem(frame(.K, 0, 1)) => .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allInts(VS) andBool 0 <=Int I` |
| 952 | 61-86 | claim | ordinary | `claim [smallest-change]: <k> #loadAll(Module(smallestDef)) ~> Call(Name("smallest_change"), list(VS:ValSeq)) => mismatchCount(VS, 0, halfLen(VS)) </k> <env> 0 </env> <scopes> 0 \|-> scope(.Map, parent(-1)) -1 \|-> builtinsScope => 0 \|-> scope( "smallest_change" \|-> closureVal("arr", smallestBody, 0), parent(-1)) -1 \|-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allInts(VS)` |

## /candidate/branch-connection-spec.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 953 | 6-9 | claim | ordinary | `claim [branch-true]: <k> #branch(B:Bool, T:Stmts, _E:Stmts) => T ... </k> requires B` |
| 954 | 10-13 | claim | ordinary | `claim [branch-false]: <k> #branch(B:Bool, _T:Stmts, E:Stmts) => E ... </k> requires notBool B` |
| 955 | 14-34 | claim | ordinary | `claim [count-branch-true]: <k> #branch( B:Bool, AugAssign(Name("changes"), "+", Int(1)), .Stmts) => .K ... </k> <env> 1 </env> <scopes> 1 \|-> scope( "arr" \|-> list(VS:ValSeq) "changes" \|-> (C:Int => C +Int 1) "i" \|-> I:Int, parent(0)) REST:Map </scopes> requires B` |
| 956 | 35-54 | claim | ordinary | `claim [count-branch-false]: <k> #branch( B:Bool, AugAssign(Name("changes"), "+", Int(1)), .Stmts) => .K ... </k> <env> 1 </env> <scopes> 1 \|-> scope( "arr" \|-> list(VS:ValSeq) "changes" \|-> C:Int "i" \|-> I:Int, parent(0)) REST:Map </scopes> requires notBool B` |

## /candidate/loop-connection-spec.k

| ID | Lines | Kind | Attributes | Declaration / rule |
|---:|:---|:---|:---|:---|
| 957 | 6-54 | claim | ordinary | `claim [loop-connection]: <k> #while( Compare( Name("i"), CmpOp( "<", BinOp( "//", Call(Name("len"), Name("arr")), Int(2)))), smallestLoopBody) ~> (Return(Name("changes")) .Stmts):Stmts ~> #endcall => C +Int mismatchCount(VS, I, halfLen(VS)) </k> <env> 1 => 0 </env> <scopes> -1 \|-> fixedBuiltins 0 \|-> scope( "smallest_change" \|-> closureVal("arr", smallestBody, 0), parent(-1)) 1 \|-> scope( "arr" \|-> list(VS:ValSeq) "changes" \|-> C:Int "i" \|-> I:Int, parent(0)) => -1 \|-> fixedBuiltins 0 \|-> scope( "smallest_change" \|-> closureVal("arr", smallestBody, 0), parent(-1)) </scopes> <scopeLoc> 2 => 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> ListItem(frame(.K, 0, 1)) => .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires allInts(VS) andBool 0 <=Int I` |


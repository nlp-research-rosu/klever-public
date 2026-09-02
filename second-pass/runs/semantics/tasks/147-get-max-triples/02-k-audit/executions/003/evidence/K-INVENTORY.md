# Exhaustive K source inventory

Each source header beginning `syntax`, `rule`, `claim`, `configuration`, or
`context` is listed once. The complete numbered source is preserved separately.

## reference-semantics/semantics/assert.k

- sha256: `4258987a261d24b02ab3abfa52b3b2e013ea6323f9d5eb9a59c8f42cbcba030b`
- headers: 3; counts: `{'rule': 3}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 6 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Assert(V:Val) => .K ... </k>` |
| 8 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Assert(V:Val) ~> _ => .K </k>` |
| 13 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>` |

## reference-semantics/semantics/bool.k

- sha256: `8d6cfa9cd1ed776e51d776e4d358c418960c57715a6f9654ef9af41aea29f4fd`
- headers: 14; counts: `{'context': 1, 'rule': 13}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 8 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| 10 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| 11 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| 16 | context | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| 17 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| 18 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>` |
| 20 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>` |
| 22 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>` |
| 24 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>` |
| 29 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>` |
| 31 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>` |
| 35 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>` |
| 39 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>` |
| 43 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>` |

## reference-semantics/semantics/builtins.k

- sha256: `fa43a855b8a4548f305f3dd210c8f6c6e7aa15b8d1cb0b8296977f061310c2dd`
- headers: 175; counts: `{'rule': 137, 'syntax': 38}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 17 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| 20 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= seqLen(Val) [function]` |
| 21 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| 22 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)` |
| 23 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)` |
| 24 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule seqLen(str(IS:IntSeq))                   => isLen(IS)` |
| 25 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)` |
| 26 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| 32 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>` |
| 33 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| 34 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>` |
| 35 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>` |
| 36 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| 37 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule charsOf(.IntSeq)                => .ValSeq` |
| 38 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| 41 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| 44 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| 47 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| 48 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| 49 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| 50 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)` |
| 54 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= intOf(Val) [function]` |
| 55 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intOf(I:Int)  => I` |
| 56 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| 59 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| 60 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| 61 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| 62 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>` |
| 64 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>` |
| 67 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| 68 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| 69 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| 70 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>` |
| 72 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>` |
| 76 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| 77 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| 78 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>` |
| 80 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| 81 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| 82 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)` |
| 86 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| 87 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| 88 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>` |
| 90 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| 91 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| 92 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)` |
| 97 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= maxVals(Int, Vals) [function]` |
| 98 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| 99 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule maxVals(M:Int, .Vals)           => M` |
| 100 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| 102 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= minVals(Int, Vals) [function]` |
| 103 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| 104 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule minVals(M:Int, .Vals)           => M` |
| 105 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| 108 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))` |
| 111 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("bin", N:Int, .Vals)` |
| 114 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| 115 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule binCodes(0) => iCons(48, .IntSeq)` |
| 116 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| 117 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| 118 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule binAcc(0, ACC:IntSeq) => ACC` |
| 119 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule binAcc(N:Int, ACC:IntSeq)` |
| 124 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))` |
| 126 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| 127 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| 128 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int)` |
| 132 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))` |
| 134 | syntax | [function, total] | UNUSED_TOTALITY_GAP | compiler-reported non-exhaustive total function; unreachable here | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| 135 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule mapStrVS(.ValSeq) => .ValSeq` |
| 136 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| 137 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| 140 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| 143 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| 144 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))` |
| 148 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))` |
| 149 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| 152 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48` |
| 156 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)` |
| 158 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| 159 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intDigAcc(.IntSeq, ACC:Int)             => ACC` |
| 160 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| 163 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| 164 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)` |
| 167 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))` |
| 169 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>` |
| 170 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| 171 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))` |
| 173 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>` |
| 174 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| 177 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)` |
| 178 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)` |
| 179 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)` |
| 187 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| 188 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= evalArith(IntSeq) [function]` |
| 189 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule evalArith(CS:IntSeq)` |
| 192 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| 194 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= evDigit(Int) [function, total]` |
| 195 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 196 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| 197 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| 198 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule evHead42(_:IntSeq)            => false [owise]` |
| 199 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| 200 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| 201 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule evHead47(_:IntSeq)            => false [owise]` |
| 203 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| 204 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokOps(.IntSeq)                 => .OpSeq` |
| 205 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)` |
| 206 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)` |
| 207 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| 208 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| 209 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| 210 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| 211 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))` |
| 212 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))` |
| 214 | syntax | [function, total], [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= tokNds(IntSeq) [function, total]` |
| 216 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokNds(.IntSeq)                => .IntSeq` |
| 217 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)` |
| 218 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| 219 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)` |
| 221 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)` |
| 223 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| 225 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| 226 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| 227 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| 228 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule firstNdE(_:EvPair) => 0 [owise]` |
| 230 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| 231 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyOpE("+",  A:Int, B:Int) => A +Int B` |
| 232 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyOpE("-",  A:Int, B:Int) => A -Int B` |
| 233 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyOpE("*",  A:Int, B:Int) => A *Int B` |
| 234 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| 235 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| 236 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| 238 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| 239 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| 240 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| 241 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))` |
| 243 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| 244 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| 245 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| 246 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| 247 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| 248 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| 250 | syntax | [function, total], [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| 251 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 252 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 253 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| 254 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| 255 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| 256 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| 257 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)` |
| 260 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)` |
| 263 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)` |
| 265 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| 266 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| 267 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| 268 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule inLevelE(_:String, _:String) => false [owise]` |
| 269 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| 270 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| 271 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| 272 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| 273 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| 274 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| 279 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= "#md5"` |
| 280 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>` |
| 282 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| 283 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= md5Obj(IntSeq)` |
| 284 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| 285 | syntax | [function, total, symbol(md5hexCodes), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| 291 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| 292 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| 293 | syntax | [function], [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| 294 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isIntV(_:Int)         => true` |
| 295 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isIntV(_:Val)         => false [owise]` |
| 296 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isStrV(str(_:IntSeq)) => true` |
| 297 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isStrV(_:Val)         => false [owise]` |

## reference-semantics/semantics/call.k

- sha256: `7e4d6c7cabe7bb4ccff52f21c5d5f30920ccb48d42864146ce53146509f736e4`
- headers: 24; counts: `{'rule': 21, 'syntax': 3}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 16 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| 19 | syntax | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax KItem ::= #callee(Exprs)` |
| 20 | rule | [owise] | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| 21 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| 24 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| 26 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| 27 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>` |
| 28 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>` |
| 29 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>` |
| 30 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>` |
| 31 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| 32 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>` |
| 38 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))` |
| 42 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))` |
| 47 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))` |
| 52 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isMutMethod(String) [function, total]` |
| 53 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isMutMethod(M:String)` |
| 56 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)` |
| 63 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))` |
| 69 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT` |
| 80 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT` |
| 87 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #allocCells(ParamNames)` |
| 88 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| 89 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>` |

## reference-semantics/semantics/comprehension.k

- sha256: `cf7c38aad5cff698ebb05ecbadf00cbf210ddb2f54ae86f22b328311c027c6a7`
- headers: 10; counts: `{'rule': 7, 'syntax': 3}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 11 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 12 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| 14 | syntax | [macro] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| 15 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule compBody(Gs:CompFors, ELT:Expr)` |
| 18 | syntax | [macro-rec] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| 19 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule compNest(.CompFors, ELT:Expr)` |
| 21 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)` |
| 24 | syntax | [macro] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Expr ::= compGuard(Exprs) [macro]` |
| 25 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule compGuard(.Exprs)             => Bool(true)` |
| 26 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |

## reference-semantics/semantics/concrete.k

- sha256: `1ffea42a32610e9116506d709e9163413aeb5f6deb7824ea554aca8341f2d305`
- headers: 21; counts: `{'rule': 16, 'syntax': 5}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 13 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>` |
| 16 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>` |
| 25 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= kvP(Val, Val)` |
| 26 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)` |
| 28 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))` |
| 31 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))` |
| 34 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)` |
| 36 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)` |
| 38 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)` |
| 42 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| 43 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| 44 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)` |
| 47 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)` |
| 51 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= kLt(Val, Val) [function]` |
| 52 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule kLt(I1:Int, I2:Int)             => I1 <Int I2` |
| 53 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule kLt(F1:Float, F2:Float)         => F1 <Float F2` |
| 54 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 56 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| 57 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule unpairVS(.ValSeq) => .ValSeq` |
| 58 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| 59 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |

## reference-semantics/semantics/controls.k

- sha256: `325c73757d5a7ccf541b93240accd590a2cee90d84470efa3a4a0a14165aafae`
- headers: 37; counts: `{'rule': 34, 'syntax': 3}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 9 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k>` |
| 12 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>` |
| 20 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>` |
| 27 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>` |
| 35 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| 36 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| 37 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #bindImports(ParamNames)` |
| 38 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| 39 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>` |
| 43 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>` |
| 48 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Expr(_:Val) => .K ... </k>` |
| 51 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| 52 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| 53 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>` |
| 54 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| 57 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>` |
| 59 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>` |
| 65 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts)` |
| 69 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| 71 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| 72 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| 73 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)` |
| 77 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| 78 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| 79 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>` |
| 81 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>` |
| 85 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 86 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Continue => #cont ... </k>` |
| 87 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Break => #brk ... </k>` |
| 88 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| 89 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| 90 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| 91 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| 95 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>` |
| 98 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>` |
| 101 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>` |
| 106 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>` |

## reference-semantics/semantics/core.k

- sha256: `e0fdc11dc2b9cd0acb18fe7c832c1ea1ac0c9e79cadf40c63f34276aca513d7e`
- headers: 84; counts: `{'configuration': 1, 'rule': 46, 'syntax': 37}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 13 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| 14 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| 15 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Str    ::= str(IntSeq)` |
| 18 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Iterable ::= list(ValSeq)` |
| 25 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val      ::= Int` |
| 36 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Parent   ::= "root" \| parent(Int)` |
| 37 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Scope    ::= scope(Map, Parent)` |
| 38 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KResult  ::= Val` |
| 39 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Expr     ::= Val   // cooling puts results back into expression holes` |
| 40 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Vals     ::= List{Val, ","}` |
| 41 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Exc      ::= "NoExc" \| "AssertionError"` |
| 42 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax RetState ::= "noRet" \| retV(Val)` |
| 49 | configuration | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `configuration` |
| 68 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isRefV(Val) [function, total]` |
| 69 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isRefV(ref(_:Int)) => true` |
| 70 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isRefV(_:Val)      => false [owise]` |
| 75 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax HeapVal ::= cellV(Val)` |
| 76 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isCellRef(Val) [function, total]` |
| 77 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isCellRef(cellRef(_:Int)) => true` |
| 78 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isCellRef(_:Val)          => false [owise]` |
| 85 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> cellRef(H:Int) => V ... </k>` |
| 95 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= kwV(String, Val)` |
| 96 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #kwTag(String)` |
| 97 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| 98 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>` |
| 100 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isKwV(Val) [function, total]` |
| 101 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isKwV(kwV(_:String, _:Val)) => true` |
| 102 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isKwV(_:Val)                => false [owise]` |
| 106 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= cellsMark(ParamNames)` |
| 107 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ParamNames ::= cellsOf(Val) [function]` |
| 108 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| 109 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| 110 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule pnMember(_:String, .ParamNames) => false` |
| 111 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| 113 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #cellW(Val, Val)` |
| 114 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>` |
| 117 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #alloc(Val)` |
| 118 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #alloc(V:Val) => ref(N) ... </k>` |
| 124 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #loadAll(Module)` |
| 125 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| 126 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| 127 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> .Stmts => .K ... </k>` |
| 130 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #look(String, Int)` |
| 131 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| 132 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>` |
| 145 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #look(X:String, L:Int) => V ... </k>` |
| 152 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>` |
| 157 | syntax | [function, total] | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax Scope ::= "builtinsScope" [function, total]` |
| 158 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule builtinsScope` |
| 185 | syntax | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax ApplyK ::= toCall(Val)` |
| 186 | syntax | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)` |
| 189 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| 190 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| 191 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| 194 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> Int(I:Int)   => I ... </k>` |
| 195 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Bool(B:Bool) => B ... </k>` |
| 196 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> NoneVal      => noneV ... </k>` |
| 199 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= truthy(Val) [function]` |
| 200 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule truthy(B:Bool)          => B` |
| 201 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule truthy(noneV)           => false` |
| 202 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule truthy(I:Int)           => I =/=Int 0` |
| 203 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)` |
| 204 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)` |
| 205 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| 208 | syntax | [function] | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax Val  ::= applyUn(String, Val) [function]` |
| 209 | syntax | [function] | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax Val  ::= applyBin(String, Val, Val) [function]` |
| 210 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| 213 | syntax | [function, total] | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| 214 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule appendVal(.Vals, V:Val)              => V , .Vals` |
| 215 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)` |
| 217 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| 218 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule vals2valSeq(.Vals)            => .ValSeq` |
| 219 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| 223 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| 224 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule vsLen(.ValSeq)                => 0` |
| 225 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| 227 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= isLen(IntSeq) [function, total]` |
| 228 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isLen(.IntSeq)                => 0` |
| 229 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| 233 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| 234 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq` |
| 235 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)` |
| 236 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))` |
| 238 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS` |

## reference-semantics/semantics/dict.k

- sha256: `779b06e18162464c8422bbd6ac35fa0b9e34ef82807d5c707c6f4552d63c0580`
- headers: 40; counts: `{'rule': 28, 'syntax': 12}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 20 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| 23 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)` |
| 26 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| 27 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| 28 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)` |
| 30 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)` |
| 32 | rule | [total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)` |
| 37 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| 38 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dHasKey(.ValSeq, _:Val)                => false` |
| 39 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K` |
| 40 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| 43 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| 44 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)` |
| 45 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| 49 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| 50 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)` |
| 52 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))` |
| 54 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| 58 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)` |
| 63 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| 64 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| 65 | rule | [priority(45)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>` |
| 70 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| 71 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| 76 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #dsetK(String, Val)` |
| 77 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| 78 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>` |
| 82 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>` |
| 86 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| 87 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>` |
| 90 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| 91 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 92 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0` |
| 95 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))` |
| 97 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| 98 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| 99 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)` |
| 101 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| 102 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K` |
| 103 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |

## reference-semantics/semantics/float.k

- sha256: `5dfeee8700c90c3aa6dc515b15b74283882845fb6cdcc3627d97ef650124b70f`
- headers: 155; counts: `{'rule': 121, 'syntax': 34}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 20 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= Float` |
| 21 | rule | — | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `rule <k> Float(F:Float) => F ... </k>` |
| 24 | syntax | [function, total, symbol(intFloatDiv), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| 25 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| 27 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| 30 | syntax | [function, total, symbol(divII), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| 31 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| 32 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| 37 | syntax | [function, total, symbol(floatMod), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| 38 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| 39 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| 43 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| 44 | rule | [no-evaluators], [concrete] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| 50 | syntax | [function, total, symbol(floatLt), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| 51 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| 52 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| 54 | syntax | [function, total, symbol(absF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| 55 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule absF(F:Float) => absFloat(F) [concrete]` |
| 56 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| 61 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Import(_:String) => .K ... </k>` |
| 65 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= "#mathCeil"` |
| 66 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| 67 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| 70 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= "#mathFloor"` |
| 71 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| 72 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| 73 | syntax | [function, total, symbol(floorFI)] | UNUSED_TOTALITY_GAP | compiler-reported non-exhaustive total function; unreachable here | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| 74 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule floorFI(I:Int)   => I                        [concrete]` |
| 75 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| 78 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| 79 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)` |
| 82 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| 83 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| 84 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| 85 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| 86 | syntax | [function, total, symbol(toF)] | UNUSED_TOTALITY_GAP | compiler-reported non-exhaustive total function; unreachable here | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| 87 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule toF(F:Float) => F        [concrete]` |
| 88 | rule | [concrete], [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule toF(I:Int)   => intToF(I) [concrete]` |
| 93 | syntax | [function, total, symbol(ceilF)] | UNUSED_TOTALITY_GAP | compiler-reported non-exhaustive total function; unreachable here | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| 94 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule ceilF(I:Int)   => I                       [concrete]` |
| 95 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| 99 | rule | [no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| 103 | syntax | [function, total, symbol(subF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| 104 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| 105 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| 107 | syntax | [function, total, symbol(divF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| 108 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| 109 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| 111 | syntax | [function, total, symbol(addF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| 112 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| 113 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| 115 | syntax | [function, total, symbol(mulF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| 116 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| 117 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| 119 | syntax | [function, total, symbol(powF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| 120 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| 121 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| 125 | syntax | [function, total, symbol(gtF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| 126 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| 127 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)` |
| 128 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| 129 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| 132 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| 133 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| 134 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)` |
| 135 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))` |
| 136 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)` |
| 137 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))` |
| 138 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)` |
| 139 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))` |
| 142 | syntax | [function, total, symbol(eqF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| 143 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| 144 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| 145 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| 146 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| 147 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| 148 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)` |
| 149 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))` |
| 150 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)` |
| 151 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))` |
| 154 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| 155 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| 160 | syntax | [function, total, symbol(decStrToF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| 161 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| 162 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule decStrToF(CS:IntSeq)` |
| 165 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= headIS(IntSeq) [function]` |
| 166 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| 167 | syntax | [function, total], [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| 168 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| 169 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intPartAcc(.IntSeq, A:Int) => A` |
| 170 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| 171 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))` |
| 173 | syntax | [function, total], [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| 174 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fracPart(.IntSeq) => 0` |
| 175 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| 176 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| 177 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fracAcc(.IntSeq, A:Int) => A` |
| 178 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| 179 | syntax | [function, total], [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| 180 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fracScale(.IntSeq) => 1` |
| 181 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| 182 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| 183 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fscAcc(.IntSeq, A:Int) => A` |
| 184 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| 185 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| 186 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)` |
| 187 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("float", F:Float, .Vals)        => F` |
| 190 | syntax | [function, total, symbol(divFloatIntV), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| 191 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| 192 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| 195 | syntax | [function, total, symbol(intToF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| 196 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| 197 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| 198 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| 199 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| 200 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| 201 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| 202 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| 203 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| 204 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| 205 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| 206 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| 209 | syntax | [function, total, symbol(truncF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| 210 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| 211 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| 213 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)` |
| 214 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| 217 | syntax | [function, total, symbol(roundF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| 218 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule roundF(F:Float)` |
| 223 | syntax | [function, total, symbol(roundFN), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| 224 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule roundFN(F:Float, N:Int)` |
| 227 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)` |
| 228 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| 230 | syntax | [function, total, symbol(sqrtF), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| 231 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| 232 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= "#mathSqrt"` |
| 233 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| 234 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| 235 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| 243 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| 244 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 245 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| 246 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| 247 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>` |
| 250 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| 251 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| 252 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| 253 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| 254 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>` |
| 261 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| 262 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)` |
| 265 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| 266 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| 267 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)` |
| 270 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)` |

## reference-semantics/semantics/functions.k

- sha256: `e4c8f67741117b29703c3c61d48a5b0f92cf7bd531e78e25c03e794a910ac193`
- headers: 19; counts: `{'rule': 15, 'syntax': 4}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 8 | syntax | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)` |
| 14 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>` |
| 18 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| 19 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>` |
| 27 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| 31 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| 33 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),` |
| 36 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,` |
| 42 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,` |
| 47 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr)` |
| 50 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),` |
| 53 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,` |
| 59 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)` |
| 63 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| 64 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>` |
| 68 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))` |
| 78 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> Return(V:Val) ~> _ => #pop </k>` |
| 80 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #endcall => #pop ... </k>` |
| 85 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> #pop => V ~> CONT </k>` |

## reference-semantics/semantics/int.k

- sha256: `dc2da7d81578370651ecb6905b69cb44443cdd8db3869441242b81420382abe5`
- headers: 17; counts: `{'rule': 16, 'syntax': 1}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 7 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyUn("-", I:Int) => 0 -Int I` |
| 9 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2` |
| 11 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| 12 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| 13 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2` |
| 14 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2` |
| 15 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)` |
| 16 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| 17 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| 19 | syntax | [function] | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax Int ::= pyMod(Int, Int) [function]` |
| 20 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| 22 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2` |
| 23 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2` |
| 24 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2` |
| 25 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2` |
| 26 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2` |
| 27 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2` |

## reference-semantics/semantics/iter.k

- sha256: `5085db2fed67b7bbd39f6289ec275905aaee742690895d7b3f843f73bd62f77f`
- headers: 1; counts: `{'syntax': 1}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 8 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |

## reference-semantics/semantics/list.k

- sha256: `870c72341c25e2c16283726191a71bf5b571ed2995c8ae12e3e2923cdce5a9aa`
- headers: 32; counts: `{'rule': 27, 'syntax': 5}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 9 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>` |
| 10 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| 13 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ApplyK ::= "toList"` |
| 14 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| 15 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| 18 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| 19 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule valSeqConcat(.ValSeq, T:ValSeq)                => T` |
| 20 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| 24 | rule | [priority(45)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>` |
| 27 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| 28 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| 33 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| 34 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule hasRefVS(.ValSeq)                => false` |
| 35 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| 37 | syntax | [function], [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]` |
| 39 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true` |
| 40 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false` |
| 41 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false` |
| 42 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)` |
| 45 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)` |
| 47 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)` |
| 49 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| 50 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| 53 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>` |
| 58 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| 59 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| 60 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| 61 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| 62 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| 63 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>` |
| 65 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>` |
| 67 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |

## reference-semantics/semantics/methods.k

- sha256: `ff9acc6dab2d1cc99ec4f2d234f27ae4526d752aae62bcfd7f9fd2a0399f7743`
- headers: 102; counts: `{'rule': 75, 'syntax': 27}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 10 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| 13 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| 14 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| 15 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| 16 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| 19 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))` |
| 20 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))` |
| 21 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| 26 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| 27 | syntax | [function, total] | UNUSED_TOTALITY_GAP | compiler-reported non-exhaustive total function; unreachable here | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| 28 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| 29 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| 30 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))` |
| 34 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| 35 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| 36 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| 37 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)` |
| 39 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)` |
| 41 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| 42 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| 43 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| 44 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| 47 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| 48 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| 49 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule trimWS(.IntSeq) => .IntSeq` |
| 50 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| 51 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| 52 | syntax | [function, total], [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| 53 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| 54 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| 55 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| 58 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| 61 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| 64 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| 65 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| 66 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule cntOccVS(.ValSeq, _:Val)                => 0` |
| 67 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| 68 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)` |
| 72 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)` |
| 75 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result` |
| 76 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| 77 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))` |
| 79 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)` |
| 82 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| 83 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC` |
| 84 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| 85 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isWSC(Int) [function, total]` |
| 86 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| 89 | rule | [priority(39)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))` |
| 94 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))` |
| 97 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token` |
| 98 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)` |
| 99 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))` |
| 101 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))` |
| 104 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)` |
| 106 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| 107 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq` |
| 108 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| 109 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| 112 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isUpperC(Int) [function, total]` |
| 113 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| 115 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isLowerC(Int) [function, total]` |
| 116 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| 118 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| 119 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| 121 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= isDigitC(Int) [function, total]` |
| 122 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| 124 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| 125 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule hasUpper(.IntSeq) => false` |
| 126 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| 128 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| 129 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule hasLower(.IntSeq) => false` |
| 130 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| 132 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| 133 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule allAlpha(.IntSeq) => true` |
| 134 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| 136 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| 137 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule allDigit(.IntSeq) => true` |
| 138 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| 140 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= lowerC(Int) [function, total]` |
| 142 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 143 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule lowerC(C:Int) => C         [owise]` |
| 145 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= upperC(Int) [function, total]` |
| 146 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 147 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule upperC(C:Int) => C         [owise]` |
| 149 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= swapC(Int) [function, total]` |
| 150 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| 151 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| 152 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule swapC(C:Int) => C         [owise]` |
| 154 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| 155 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule mapLower(.IntSeq) => .IntSeq` |
| 156 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| 158 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| 159 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule mapUpper(.IntSeq) => .IntSeq` |
| 160 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| 162 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| 163 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule mapSwap(.IntSeq) => .IntSeq` |
| 164 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| 166 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| 167 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule startsWith(.IntSeq, _:IntSeq)               => true` |
| 168 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 169 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |

## reference-semantics/semantics/operators.k

- sha256: `f3d1fd85734f5e1757307e606cbfb8d6d4bf0893ee85ce20ec99606ade910e8b`
- headers: 12; counts: `{'context': 2, 'rule': 10}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 10 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| 12 | rule | — | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| 15 | context | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `context Compare(HOLE, _)` |
| 16 | context | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `context Compare(_:Val, CmpOp(_, HOLE))` |
| 17 | rule | [owise] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| 19 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("is",     V:Val, noneV) => V ==K noneV` |
| 20 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| 25 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>` |
| 28 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>` |
| 34 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>` |
| 38 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>` |
| 44 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>` |

## reference-semantics/semantics/range.k

- sha256: `810e4c04b757445c03592aef25c97d6b2cc7c6fffa646288bc6cd15a3cae643d`
- headers: 8; counts: `{'rule': 6, 'syntax': 2}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 9 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| 10 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| 12 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| 13 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST` |
| 15 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)` |
| 17 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0` |
| 20 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))` |
| 23 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>` |

## reference-semantics/semantics/set.k

- sha256: `b822c3c6944f9940a4477fa6b7a42490c407663f2a314394e9c146e8951f1ac7`
- headers: 18; counts: `{'rule': 12, 'syntax': 6}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 8 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= setV(IntSeq)` |
| 11 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| 12 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule codeIn(_:Int, .IntSeq)                => false` |
| 13 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| 16 | syntax | [function, total], [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]` |
| 18 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| 19 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| 20 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)` |
| 22 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))` |
| 25 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| 26 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)` |
| 27 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| 31 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| 32 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule subsetCodes(.IntSeq, _:IntSeq)                => true` |
| 33 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| 35 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| 36 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| 39 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |

## reference-semantics/semantics/sort.k

- sha256: `df79670e4794a92e96ffc824857fbc34d3a65b6b6a3026d1dcf322128fbaba5a`
- headers: 25; counts: `{'rule': 19, 'syntax': 6}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 18 | syntax | [function, total, symbol(sortVS), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| 19 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| 20 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule sortVS(.ValSeq)                => .ValSeq          [concrete]` |
| 21 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| 22 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]` |
| 23 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| 24 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]` |
| 26 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| 27 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| 28 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| 29 | rule | [concrete] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))` |
| 31 | rule | [concrete], [owise] | UNUSED_CONCRETE_ONLY | concrete-only rule; absent from symbolic target path | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))` |
| 36 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))` |
| 40 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>` |
| 49 | syntax | [function, total, symbol(sortKeyVS), no-evaluators] | UNUSED_OPAQUE_BOUNDARY | explicit opaque result; unreachable here | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| 51 | syntax | [function, total], [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= revVS(ValSeq) [function, total]` |
| 53 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| 54 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| 55 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| 57 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| 58 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule condRev(S:ValSeq, false) => S` |
| 59 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule condRev(S:ValSeq, true)  => revVS(S)` |
| 61 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))` |
| 63 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))` |
| 65 | rule | [total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))` |

## reference-semantics/semantics/str.k

- sha256: `1bf0abf61d7c5df6301433a89c79d2ef4259d47a68d98385ff74618c4c310e0f`
- headers: 33; counts: `{'rule': 28, 'syntax': 5}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 8 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>` |
| 9 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))` |
| 13 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= strToCodes(String) [function]` |
| 14 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| 15 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strToCodes("") => .IntSeq` |
| 16 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))` |
| 20 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| 21 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule seqConcat(.IntSeq, T:IntSeq)                => T` |
| 22 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| 24 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| 25 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| 26 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| 29 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| 30 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| 32 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| 33 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strPrefix(.IntSeq, _:IntSeq)               => true` |
| 34 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 35 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| 37 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| 38 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)` |
| 39 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)` |
| 40 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)` |
| 48 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| 49 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strLt(.IntSeq, .IntSeq)                => false` |
| 50 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| 51 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| 52 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B` |
| 53 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B` |
| 54 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| 56 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| 57 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| 58 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| 59 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |

## reference-semantics/semantics/subscript.k

- sha256: `dba04c0acf213bef4f9f7b11243ca00a2b3ca5fa8666c544ede7d382d27d36a7`
- headers: 57; counts: `{'context': 2, 'rule': 40, 'syntax': 15}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 11 | syntax | [function, total] | UNUSED_TOTALITY_GAP | compiler-reported non-exhaustive total function; unreachable here | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| 12 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V` |
| 13 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)` |
| 16 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| 17 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C` |
| 18 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)` |
| 21 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| 22 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| 23 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0` |
| 27 | context | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `context Subscript(HOLE, _)` |
| 28 | context | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `context Subscript(_:Val, HOLE:Expr)` |
| 31 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>` |
| 35 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| 37 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= applyIndex(Val, Int) [function]` |
| 38 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 39 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| 40 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyIndex(str(IS:IntSeq),   I:Int)` |
| 44 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #evalB(Bound) \| "#toSome"` |
| 49 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax OptInt ::= "noB" \| someB(Int)` |
| 50 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #evalB(NoBound)  => noB ... </k>` |
| 51 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>` |
| 52 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| 54 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| 55 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| 56 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| 58 | rule | [priority(45)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)` |
| 61 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| 63 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| 64 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)` |
| 66 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)` |
| 68 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)` |
| 72 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= slStep(OptInt) [function, total]` |
| 73 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slStep(noB)          => 1` |
| 74 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slStep(someB(S:Int)) => S` |
| 76 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| 77 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0` |
| 79 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1` |
| 81 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 83 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| 84 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN` |
| 86 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1` |
| 88 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| 90 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| 91 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)` |
| 93 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)` |
| 96 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| 97 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule clampLo(J:Int, _STEP:Int) => J` |
| 99 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi` |
| 102 | syntax | [function, total] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| 103 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I` |
| 105 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi` |
| 109 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| 110 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)` |
| 113 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq` |
| 116 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| 117 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)` |
| 120 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq` |

## reference-semantics/semantics/syntax.k

- sha256: `1e9e629e5e6e14bdd7f4d530375e8655a89366b5ecd0c24a3c57ad3b5708f2a6`
- headers: 16; counts: `{'syntax': 16}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 9 | syntax | [strict(2)], [seqstrict(2, 3)], [macro], [macro], [strict(1)], [strict(1)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Expr ::= "Int"      "(" Int ")"` |
| 32 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"` |
| 33 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"` |
| 34 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Entries  ::= List{Entry, ","}` |
| 35 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| 36 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax CompFors ::= List{CompFor, ""}` |
| 37 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Exprs    ::= List{Expr, ","}` |
| 38 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| 39 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Bound    ::= Expr \| "NoBound"` |
| 41 | syntax | [strict(2)], [strict(3)], [strict(2)], [strict(1)], [strict], [strict], [strict] | TARGET_REACHABLE_FIXED | reviewed against this program's Python behavior | `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)]` |
| 56 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Stmts      ::= List{Stmt, ""}` |
| 57 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Params     ::= "Params" "(" ParamNames ")"` |
| 58 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax CellVars   ::= "CellVars" "(" ParamNames ")"` |
| 59 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"` |
| 60 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ParamNames ::= List{String, ","}` |
| 61 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Module     ::= "Module" "(" Stmts ")"` |

## reference-semantics/semantics/tuple.k

- sha256: `41395a1ec6a58129c78facb15b44206907c54d79e86ea363ae68cb37bfc64abb`
- headers: 25; counts: `{'rule': 21, 'syntax': 4}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 10 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>` |
| 11 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| 14 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax ApplyK ::= "toTuple"` |
| 15 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| 16 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| 18 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| 20 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| 21 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| 23 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| 24 | syntax | [function] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| 25 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| 26 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)` |
| 28 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| 31 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #bindTgt(Expr, Val)` |
| 32 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>` |
| 35 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>` |
| 42 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 43 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 44 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>` |
| 49 | syntax | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| 50 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| 51 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| 52 | rule | [priority(40)] | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>` |
| 55 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))` |
| 57 | rule | — | UNUSED_FIXED_BASELINE | reviewed; no false conclusion witness affecting target | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |

## reference-semantics/semantics.k

- sha256: `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`
- headers: 0; counts: `{}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|

## verification.k

- sha256: `856ebca2c4f37f5b0b20071ad6ebfc73ec6733bc0125e399e6ebf4bc0615f90f`
- headers: 8; counts: `{'rule': 4, 'syntax': 4}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 8 | syntax | [function] | LOCAL_PROOF_EXTENSION | reviewed: truthful terminating definition; no overlap | `syntax Stmts ::= "getMaxTriplesBody" [function]` |
| 9 | rule | — | LOCAL_PROOF_EXTENSION | reviewed: truthful terminating definition; no overlap | `rule getMaxTriplesBody` |
| 45 | syntax | [function] | LOCAL_PROOF_EXTENSION | reviewed: truthful terminating definition; no overlap | `syntax Int ::= chooseThree(Int) [function]` |
| 46 | rule | — | LOCAL_PROOF_EXTENSION | reviewed: truthful terminating definition; no overlap | `rule chooseThree(C:Int)` |
| 51 | syntax | [function] | LOCAL_PROOF_EXTENSION | reviewed: truthful terminating definition; no overlap | `syntax Int ::= zeroResidues(Int) [function]` |
| 52 | rule | — | LOCAL_PROOF_EXTENSION | reviewed: truthful terminating definition; no overlap | `rule zeroResidues(N:Int)` |
| 55 | syntax | [function] | LOCAL_PROOF_EXTENSION | reviewed: truthful terminating definition; no overlap | `syntax Int ::= tripleCount(Int) [function]` |
| 56 | rule | — | LOCAL_PROOF_EXTENSION | reviewed: truthful terminating definition; no overlap | `rule tripleCount(N:Int)` |

## spec.k

- sha256: `db06c15c7d5f65d6a531ef96576117eb8eac21ff6984ae83375075a85eae4391`
- headers: 4; counts: `{'claim': 4}`

| line | kind | attributes | target class | assessment | source header |
|---:|---|---|---|---|---|
| 7 | claim | — | TARGET_CLAIM | reviewed independently in Stages 3-6 | `claim [residue-0]:` |
| 14 | claim | — | TARGET_CLAIM | reviewed independently in Stages 3-6 | `claim [residue-1]:` |
| 21 | claim | — | TARGET_CLAIM | reviewed independently in Stages 3-6 | `claim [residue-2]:` |
| 32 | claim | — | TARGET_CLAIM | reviewed independently in Stages 3-6 | `claim [get-max-triples-correct]:` |

# Totals

- source files: 26
- inventoried headers: 940
- counts: `{'claim': 4, 'configuration': 1, 'context': 5, 'rule': 699, 'syntax': 231}`
- explicit target-reachable source headers: 53
- compiler-reported unused totality gaps: 6

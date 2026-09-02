# Exhaustive lexical K declaration inventory

Generated from the clean trusted supplied-semantics copy plus `verification.k` and `spec.k`. Each record includes the complete source block through the next top-level K declaration.

## `reference-semantics/semantics/assert.k`

### rule at line 6 (attributes: none)

```k
  rule <k> Assert(V:Val) => .K ... </k>
```

### rule at line 8 (attributes: none)

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
```

### rule at line 13 (attributes: priority)

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/bool.k`

### rule at line 8 (attributes: none)

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### rule at line 10 (attributes: none)

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### rule at line 11 (attributes: none)

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### context at line 16 (attributes: none)

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### rule at line 17 (attributes: none)

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### rule at line 18 (attributes: none)

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
```

### rule at line 20 (attributes: none)

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
```

### rule at line 22 (attributes: none)

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
```

### rule at line 24 (attributes: none)

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
```

### rule at line 29 (attributes: priority)

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### rule at line 31 (attributes: none)

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### rule at line 35 (attributes: none)

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### rule at line 39 (attributes: none)

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### rule at line 43 (attributes: none)

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

## `reference-semantics/semantics/builtins.k`

### syntax at line 17 (attributes: function)

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### syntax at line 20 (attributes: function)

```k
  syntax Int ::= seqLen(Val) [function]
```

### rule at line 21 (attributes: none)

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### rule at line 22 (attributes: none)

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### rule at line 23 (attributes: none)

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### rule at line 24 (attributes: none)

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### rule at line 25 (attributes: none)

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### rule at line 26 (attributes: none)

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### rule at line 32 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### rule at line 33 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### rule at line 34 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### rule at line 35 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### syntax at line 36 (attributes: function, total)

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### rule at line 37 (attributes: none)

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### rule at line 38 (attributes: none)

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### rule at line 41 (attributes: none)

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### rule at line 44 (attributes: none)

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### syntax at line 47 (attributes: none)

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### rule at line 48 (attributes: none)

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### rule at line 49 (attributes: none)

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### rule at line 50 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
```

### syntax at line 54 (attributes: function)

```k
  syntax Int ::= intOf(Val) [function]
```

### rule at line 55 (attributes: none)

```k
  rule intOf(I:Int)  => I
```

### rule at line 56 (attributes: none)

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### syntax at line 59 (attributes: none)

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### rule at line 60 (attributes: none)

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### rule at line 61 (attributes: none)

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### rule at line 62 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
```

### rule at line 64 (attributes: none)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
```

### syntax at line 67 (attributes: none)

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### rule at line 68 (attributes: none)

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### rule at line 69 (attributes: none)

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### rule at line 70 (attributes: none)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
```

### rule at line 72 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
```

### syntax at line 76 (attributes: none)

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### rule at line 77 (attributes: none)

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### rule at line 78 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
```

### rule at line 80 (attributes: none)

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### rule at line 81 (attributes: none)

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### rule at line 82 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
```

### syntax at line 86 (attributes: none)

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### rule at line 87 (attributes: none)

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### rule at line 88 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
```

### rule at line 90 (attributes: none)

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### rule at line 91 (attributes: none)

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### rule at line 92 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
```

### syntax at line 97 (attributes: function)

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### rule at line 98 (attributes: none)

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### rule at line 99 (attributes: none)

```k
  rule maxVals(M:Int, .Vals)           => M
```

### rule at line 100 (attributes: none)

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### syntax at line 102 (attributes: function)

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### rule at line 103 (attributes: none)

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### rule at line 104 (attributes: none)

```k
  rule minVals(M:Int, .Vals)           => M
```

### rule at line 105 (attributes: none)

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### rule at line 108 (attributes: none)

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
```

### rule at line 111 (attributes: none)

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
```

### syntax at line 114 (attributes: function, total)

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### rule at line 115 (attributes: none)

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### rule at line 116 (attributes: none)

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### syntax at line 117 (attributes: function, total)

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### rule at line 118 (attributes: none)

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### rule at line 119 (attributes: none)

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
```

### rule at line 124 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### syntax at line 126 (attributes: function, total)

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### rule at line 127 (attributes: none)

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### rule at line 128 (attributes: none)

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### rule at line 132 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### syntax at line 134 (attributes: function, total)

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### rule at line 135 (attributes: none)

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### rule at line 136 (attributes: none)

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### rule at line 137 (attributes: none)

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### rule at line 140 (attributes: none)

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### rule at line 143 (attributes: none)

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### rule at line 144 (attributes: none)

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
```

### rule at line 148 (attributes: none)

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### rule at line 149 (attributes: none)

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### rule at line 152 (attributes: none)

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
```

### rule at line 156 (attributes: none)

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
```

### syntax at line 158 (attributes: function, total)

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### rule at line 159 (attributes: none)

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### rule at line 160 (attributes: none)

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### rule at line 163 (attributes: none)

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### rule at line 164 (attributes: none)

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### rule at line 167 (attributes: none)

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### rule at line 169 (attributes: none)

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### rule at line 170 (attributes: none)

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### rule at line 171 (attributes: none)

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### rule at line 173 (attributes: none)

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### rule at line 174 (attributes: none)

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### rule at line 177 (attributes: none)

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### rule at line 178 (attributes: none)

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### rule at line 179 (attributes: none)

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
```

### rule at line 187 (attributes: none)

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### syntax at line 188 (attributes: function)

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### rule at line 189 (attributes: none)

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### syntax at line 192 (attributes: none)

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### syntax at line 194 (attributes: function, total)

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### rule at line 195 (attributes: none)

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### syntax at line 196 (attributes: function, total)

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### rule at line 197 (attributes: none)

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### rule at line 198 (attributes: owise)

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### syntax at line 199 (attributes: function, total)

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### rule at line 200 (attributes: none)

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### rule at line 201 (attributes: owise)

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### syntax at line 203 (attributes: function, total)

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### rule at line 204 (attributes: none)

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### rule at line 205 (attributes: none)

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### rule at line 206 (attributes: none)

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### rule at line 207 (attributes: none)

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### rule at line 208 (attributes: none)

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### rule at line 209 (attributes: none)

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### rule at line 210 (attributes: none)

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### rule at line 211 (attributes: none)

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### rule at line 212 (attributes: none)

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### syntax at line 214 (attributes: function, total)

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### rule at line 216 (attributes: none)

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### rule at line 217 (attributes: none)

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### rule at line 218 (attributes: none)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### rule at line 219 (attributes: none)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
```

### rule at line 221 (attributes: none)

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
```

### rule at line 223 (attributes: owise)

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### syntax at line 225 (attributes: none)

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### syntax at line 226 (attributes: function, total)

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### rule at line 227 (attributes: none)

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### rule at line 228 (attributes: owise)

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### syntax at line 230 (attributes: function, total)

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### rule at line 231 (attributes: none)

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### rule at line 232 (attributes: none)

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### rule at line 233 (attributes: none)

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### rule at line 234 (attributes: none)

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### rule at line 235 (attributes: none)

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### rule at line 236 (attributes: owise)

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### syntax at line 238 (attributes: function, total)

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### rule at line 239 (attributes: none)

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### rule at line 240 (attributes: none)

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### rule at line 241 (attributes: none)

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
```

### rule at line 243 (attributes: owise)

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### syntax at line 244 (attributes: function, total)

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### rule at line 245 (attributes: none)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### rule at line 246 (attributes: none)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### syntax at line 247 (attributes: function, total)

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### rule at line 248 (attributes: none)

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### syntax at line 250 (attributes: function, total)

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### rule at line 251 (attributes: none)

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### rule at line 252 (attributes: none)

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### rule at line 253 (attributes: none)

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### rule at line 254 (attributes: none)

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### syntax at line 255 (attributes: function, total)

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### rule at line 256 (attributes: none)

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### rule at line 257 (attributes: none)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
```

### rule at line 260 (attributes: none)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
```

### rule at line 263 (attributes: owise)

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### syntax at line 265 (attributes: function, total)

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### rule at line 266 (attributes: none)

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### rule at line 267 (attributes: none)

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### rule at line 268 (attributes: owise)

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### syntax at line 269 (attributes: function, total)

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### rule at line 270 (attributes: none)

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### rule at line 271 (attributes: none)

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### syntax at line 272 (attributes: function, total)

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### rule at line 273 (attributes: none)

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### rule at line 274 (attributes: none)

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### syntax at line 279 (attributes: none)

```k
  syntax KItem ::= "#md5"
```

### rule at line 280 (attributes: priority)

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### rule at line 282 (attributes: none)

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### syntax at line 283 (attributes: none)

```k
  syntax Val ::= md5Obj(IntSeq)
```

### rule at line 284 (attributes: none)

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### syntax at line 285 (attributes: function, total, symbol, no-evaluators)

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### rule at line 291 (attributes: none)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### rule at line 292 (attributes: none)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### syntax at line 293 (attributes: function)

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### rule at line 294 (attributes: none)

```k
  rule isIntV(_:Int)         => true
```

### rule at line 295 (attributes: owise)

```k
  rule isIntV(_:Val)         => false [owise]
```

### rule at line 296 (attributes: none)

```k
  rule isStrV(str(_:IntSeq)) => true
```

### rule at line 297 (attributes: owise)

```k
  rule isStrV(_:Val)         => false [owise]
```

## `reference-semantics/semantics/call.k`

### rule at line 16 (attributes: none)

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### syntax at line 19 (attributes: none)

```k
  syntax KItem ::= #callee(Exprs)
```

### rule at line 20 (attributes: owise)

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### rule at line 21 (attributes: none)

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### rule at line 24 (attributes: none)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### rule at line 26 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### rule at line 27 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### rule at line 28 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### rule at line 29 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### rule at line 30 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### rule at line 31 (attributes: owise)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### rule at line 32 (attributes: none)

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### rule at line 38 (attributes: priority)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at line 42 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### rule at line 47 (attributes: priority)

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### syntax at line 52 (attributes: function, total)

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### rule at line 53 (attributes: none)

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### rule at line 56 (attributes: none)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### rule at line 63 (attributes: none)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### rule at line 69 (attributes: none)

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### rule at line 80 (attributes: none)

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### syntax at line 87 (attributes: none)

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### rule at line 88 (attributes: none)

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### rule at line 89 (attributes: none)

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
```

## `reference-semantics/semantics/comprehension.k`

### rule at line 11 (attributes: none)

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### rule at line 12 (attributes: none)

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### syntax at line 14 (attributes: macro)

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### rule at line 15 (attributes: none)

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### syntax at line 18 (attributes: macro)

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### rule at line 19 (attributes: none)

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### rule at line 21 (attributes: none)

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### syntax at line 24 (attributes: macro)

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### rule at line 25 (attributes: none)

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### rule at line 26 (attributes: none)

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## `reference-semantics/semantics/concrete.k`

### rule at line 13 (attributes: none)

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
```

### rule at line 16 (attributes: none)

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
```

### syntax at line 25 (attributes: none)

```k
  syntax Val ::= kvP(Val, Val)
```

### syntax at line 26 (attributes: none)

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### rule at line 28 (attributes: priority)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### rule at line 31 (attributes: priority)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### rule at line 34 (attributes: none)

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### rule at line 36 (attributes: none)

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### rule at line 38 (attributes: none)

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
```

### syntax at line 42 (attributes: function)

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### rule at line 43 (attributes: none)

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### rule at line 44 (attributes: none)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
```

### rule at line 47 (attributes: none)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
```

### syntax at line 51 (attributes: function)

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### rule at line 52 (attributes: none)

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### rule at line 53 (attributes: none)

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### rule at line 54 (attributes: none)

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### syntax at line 56 (attributes: function, total)

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### rule at line 57 (attributes: none)

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### rule at line 58 (attributes: none)

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### rule at line 59 (attributes: owise)

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## `reference-semantics/semantics/controls.k`

### rule at line 9 (attributes: none)

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### rule at line 12 (attributes: none)

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### rule at line 20 (attributes: none)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
```

### rule at line 27 (attributes: none)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### rule at line 35 (attributes: none)

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### rule at line 36 (attributes: owise)

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### syntax at line 37 (attributes: none)

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### rule at line 38 (attributes: none)

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### rule at line 39 (attributes: none)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
```

### rule at line 43 (attributes: none)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
```

### rule at line 48 (attributes: none)

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### syntax at line 51 (attributes: none)

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### rule at line 52 (attributes: none)

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### rule at line 53 (attributes: none)

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### rule at line 54 (attributes: none)

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### rule at line 57 (attributes: none)

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
```

### rule at line 59 (attributes: none)

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
```

### syntax at line 65 (attributes: none)

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### rule at line 69 (attributes: none)

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### rule at line 71 (attributes: none)

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### rule at line 72 (attributes: none)

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### rule at line 73 (attributes: none)

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### rule at line 77 (attributes: none)

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### rule at line 78 (attributes: none)

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### rule at line 79 (attributes: none)

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
```

### rule at line 81 (attributes: none)

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
```

### rule at line 85 (attributes: none)

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### rule at line 86 (attributes: none)

```k
  rule <k> Continue => #cont ... </k>
```

### rule at line 87 (attributes: none)

```k
  rule <k> Break => #brk ... </k>
```

### rule at line 88 (attributes: none)

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### rule at line 89 (attributes: owise)

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### rule at line 90 (attributes: none)

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### rule at line 91 (attributes: owise)

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### rule at line 95 (attributes: priority)

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at line 98 (attributes: priority)

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at line 101 (attributes: priority)

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at line 106 (attributes: priority)

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/core.k`

### syntax at line 13 (attributes: none)

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### syntax at line 14 (attributes: none)

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### syntax at line 15 (attributes: none)

```k
  syntax Str    ::= str(IntSeq)
```

### syntax at line 18 (attributes: none)

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### syntax at line 25 (attributes: function)

```k
  syntax Val      ::= Int
                    | Bool
                    | "noneV"
                    | Iterable
                    | ref(Int)          // a heap object: <heap> holds its list(VS)
                    | cellRef(Int)      // a closure cell: <heap> holds cellV(V)
                    | closureVal(ParamNames, Stmts, Int)
                    | typeV(String)     // a type object (int/str), resolved from the builtins frame
                    | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough)
                    | boundMethodV(Val, String)   // a cooled Attribute: obj.method
```

### syntax at line 36 (attributes: none)

```k
  syntax Parent   ::= "root" | parent(Int)
```

### syntax at line 37 (attributes: none)

```k
  syntax Scope    ::= scope(Map, Parent)
```

### syntax at line 38 (attributes: none)

```k
  syntax KResult  ::= Val
```

### syntax at line 39 (attributes: none)

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### syntax at line 40 (attributes: none)

```k
  syntax Vals     ::= List{Val, ","}
```

### syntax at line 41 (attributes: none)

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### syntax at line 42 (attributes: none)

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### configuration at line 49 (attributes: none)

```k
  configuration
    <k>       #loadAll($PGM:Module) </k>
    <env>     0 </env>
    <scopes>   0     |-> scope(.Map, parent(-1))
              -1    |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>    .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>   .List </stack>
    <ret>     noRet </ret>
    <exc>     NoExc </exc>
    <exit-code exit=""> 0 </exit-code>
```

### syntax at line 68 (attributes: function, total)

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### rule at line 69 (attributes: none)

```k
  rule isRefV(ref(_:Int)) => true
```

### rule at line 70 (attributes: owise)

```k
  rule isRefV(_:Val)      => false [owise]
```

### syntax at line 75 (attributes: none)

```k
  syntax HeapVal ::= cellV(Val)
```

### syntax at line 76 (attributes: function, total)

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### rule at line 77 (attributes: none)

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### rule at line 78 (attributes: owise)

```k
  rule isCellRef(_:Val)          => false [owise]
```

### rule at line 85 (attributes: none)

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
```

### syntax at line 95 (attributes: none)

```k
  syntax Val ::= kwV(String, Val)
```

### syntax at line 96 (attributes: none)

```k
  syntax KItem ::= #kwTag(String)
```

### rule at line 97 (attributes: none)

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### rule at line 98 (attributes: none)

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
```

### syntax at line 100 (attributes: function, total)

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### rule at line 101 (attributes: none)

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### rule at line 102 (attributes: owise)

```k
  rule isKwV(_:Val)                => false [owise]
```

### syntax at line 106 (attributes: none)

```k
  syntax Val ::= cellsMark(ParamNames)
```

### syntax at line 107 (attributes: function)

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### rule at line 108 (attributes: none)

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### syntax at line 109 (attributes: function, total)

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### rule at line 110 (attributes: none)

```k
  rule pnMember(_:String, .ParamNames) => false
```

### rule at line 111 (attributes: none)

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### syntax at line 113 (attributes: none)

```k
  syntax KItem ::= #cellW(Val, Val)
```

### rule at line 114 (attributes: none)

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### syntax at line 117 (attributes: none)

```k
  syntax KItem ::= #alloc(Val)
```

### rule at line 118 (attributes: none)

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
```

### syntax at line 124 (attributes: none)

```k
  syntax KItem ::= #loadAll(Module)
```

### rule at line 125 (attributes: none)

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### rule at line 126 (attributes: none)

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### rule at line 127 (attributes: none)

```k
  rule <k> .Stmts => .K ... </k>
```

### syntax at line 130 (attributes: none)

```k
  syntax KItem ::= #look(String, Int)
```

### rule at line 131 (attributes: none)

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### rule at line 132 (attributes: none)

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
```

### rule at line 145 (attributes: none)

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
```

### rule at line 152 (attributes: none)

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
```

### syntax at line 157 (attributes: function, total)

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### rule at line 158 (attributes: none)

```k
  rule builtinsScope
    => scope(.Map [ "len"    <- builtinV("len")    ]
                  [ "set"    <- builtinV("set")    ]
                  [ "sum"    <- builtinV("sum")    ]
                  [ "abs"    <- builtinV("abs")    ]
                  [ "min"    <- builtinV("min")    ]
                  [ "max"    <- builtinV("max")    ]
                  [ "ord"    <- builtinV("ord")    ]
                  [ "chr"    <- builtinV("chr")    ]
                  [ "range"  <- builtinV("range")  ]
                  [ "all"    <- builtinV("all")    ]
                  [ "any"    <- builtinV("any")    ]
                  [ "zip"    <- builtinV("zip")    ]
                  [ "isinstance" <- builtinV("isinstance") ]
                  [ "sorted" <- builtinV("sorted") ]
                  [ "list"   <- builtinV("list")   ]
                  [ "round"  <- builtinV("round")  ]
                  [ "bin"    <- builtinV("bin")    ]
                  [ "enumerate" <- builtinV("enumerate") ]
                  [ "map"    <- builtinV("map")    ]
                  [ "eval"   <- builtinV("eval")   ]
                  [ "int"    <- typeV("int")       ]
                  [ "str"    <- typeV("str")       ]
                  [ "float"  <- typeV("float")     ], root)
```

### syntax at line 185 (attributes: none)

```k
  syntax ApplyK ::= toCall(Val)
```

### syntax at line 186 (attributes: none)

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### rule at line 189 (attributes: none)

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### rule at line 190 (attributes: none)

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### rule at line 191 (attributes: none)

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### rule at line 194 (attributes: none)

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### rule at line 195 (attributes: none)

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### rule at line 196 (attributes: none)

```k
  rule <k> NoneVal      => noneV ... </k>
```

### syntax at line 199 (attributes: function)

```k
  syntax Bool ::= truthy(Val) [function]
```

### rule at line 200 (attributes: none)

```k
  rule truthy(B:Bool)          => B
```

### rule at line 201 (attributes: none)

```k
  rule truthy(noneV)           => false
```

### rule at line 202 (attributes: none)

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### rule at line 203 (attributes: none)

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### rule at line 204 (attributes: none)

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### rule at line 205 (attributes: none)

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### syntax at line 208 (attributes: function)

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### syntax at line 209 (attributes: function)

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### syntax at line 210 (attributes: function)

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### syntax at line 213 (attributes: function, total)

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### rule at line 214 (attributes: none)

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### rule at line 215 (attributes: none)

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### syntax at line 217 (attributes: function, total)

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### rule at line 218 (attributes: none)

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### rule at line 219 (attributes: none)

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### syntax at line 223 (attributes: function, total)

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### rule at line 224 (attributes: none)

```k
  rule vsLen(.ValSeq)                => 0
```

### rule at line 225 (attributes: none)

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### syntax at line 227 (attributes: function, total)

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### rule at line 228 (attributes: none)

```k
  rule isLen(.IntSeq)                => 0
```

### rule at line 229 (attributes: none)

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### syntax at line 233 (attributes: function, total)

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### rule at line 234 (attributes: none)

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### rule at line 235 (attributes: none)

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### rule at line 236 (attributes: none)

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
```

### rule at line 238 (attributes: none)

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
```

## `reference-semantics/semantics/dict.k`

### syntax at line 20 (attributes: none)

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### syntax at line 23 (attributes: none)

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### rule at line 26 (attributes: none)

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### rule at line 27 (attributes: none)

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### rule at line 28 (attributes: none)

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### rule at line 30 (attributes: none)

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### rule at line 32 (attributes: none)

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### syntax at line 37 (attributes: function, total)

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### rule at line 38 (attributes: none)

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### rule at line 39 (attributes: none)

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### rule at line 40 (attributes: none)

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### syntax at line 43 (attributes: function, total)

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### rule at line 44 (attributes: none)

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### rule at line 45 (attributes: none)

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### syntax at line 49 (attributes: function, total)

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### rule at line 50 (attributes: none)

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
```

### rule at line 52 (attributes: none)

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
```

### rule at line 54 (attributes: owise)

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### rule at line 58 (attributes: priority)

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### rule at line 63 (attributes: none)

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### syntax at line 64 (attributes: function)

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### rule at line 65 (attributes: priority)

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### syntax at line 70 (attributes: function)

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### rule at line 71 (attributes: none)

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### syntax at line 76 (attributes: none)

```k
  syntax KItem ::= #dsetK(String, Val)
```

### rule at line 77 (attributes: none)

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### rule at line 78 (attributes: none)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
```

### rule at line 82 (attributes: none)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### syntax at line 86 (attributes: none)

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### rule at line 87 (attributes: none)

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### syntax at line 90 (attributes: function, total)

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### rule at line 91 (attributes: none)

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### rule at line 92 (attributes: none)

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### rule at line 95 (attributes: none)

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### syntax at line 97 (attributes: function)

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### rule at line 98 (attributes: none)

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### rule at line 99 (attributes: none)

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### syntax at line 101 (attributes: function)

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### rule at line 102 (attributes: none)

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### rule at line 103 (attributes: none)

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## `reference-semantics/semantics/float.k`

### syntax at line 20 (attributes: none)

```k
  syntax Val ::= Float
```

### rule at line 21 (attributes: none)

```k
  rule <k> Float(F:Float) => F ... </k>
```

### syntax at line 24 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### rule at line 25 (attributes: concrete)

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### rule at line 27 (attributes: none)

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### syntax at line 30 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### rule at line 31 (attributes: concrete)

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### rule at line 32 (attributes: none)

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### syntax at line 37 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### rule at line 38 (attributes: concrete)

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### rule at line 39 (attributes: none)

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### rule at line 43 (attributes: none)

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### rule at line 44 (attributes: none)

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### syntax at line 50 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### rule at line 51 (attributes: concrete)

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### rule at line 52 (attributes: none)

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### syntax at line 54 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### rule at line 55 (attributes: concrete)

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### rule at line 56 (attributes: none)

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### rule at line 61 (attributes: none)

```k
  rule <k> Import(_:String) => .K ... </k>
```

### syntax at line 65 (attributes: none)

```k
  syntax KItem ::= "#mathCeil"
```

### rule at line 66 (attributes: priority)

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### rule at line 67 (attributes: none)

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### syntax at line 70 (attributes: none)

```k
  syntax KItem ::= "#mathFloor"
```

### rule at line 71 (attributes: priority)

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### rule at line 72 (attributes: none)

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### syntax at line 73 (attributes: function, total, symbol)

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### rule at line 74 (attributes: concrete)

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### rule at line 75 (attributes: concrete)

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### rule at line 78 (attributes: none)

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### rule at line 79 (attributes: none)

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### syntax at line 82 (attributes: none)

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### rule at line 83 (attributes: priority)

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### rule at line 84 (attributes: none)

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### rule at line 85 (attributes: none)

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### syntax at line 86 (attributes: function, total, symbol)

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### rule at line 87 (attributes: concrete)

```k
  rule toF(F:Float) => F        [concrete]
```

### rule at line 88 (attributes: concrete)

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### syntax at line 93 (attributes: function, total, symbol)

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### rule at line 94 (attributes: concrete)

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### rule at line 95 (attributes: concrete)

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### rule at line 99 (attributes: none)

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### syntax at line 103 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### rule at line 104 (attributes: concrete)

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### rule at line 105 (attributes: none)

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### syntax at line 107 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### rule at line 108 (attributes: concrete)

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### rule at line 109 (attributes: none)

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### syntax at line 111 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### rule at line 112 (attributes: concrete)

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### rule at line 113 (attributes: none)

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### syntax at line 115 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### rule at line 116 (attributes: concrete)

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### rule at line 117 (attributes: none)

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### syntax at line 119 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### rule at line 120 (attributes: concrete)

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### rule at line 121 (attributes: none)

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### syntax at line 125 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### rule at line 126 (attributes: concrete)

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### rule at line 127 (attributes: none)

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### rule at line 128 (attributes: none)

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### rule at line 129 (attributes: none)

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### rule at line 132 (attributes: none)

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### rule at line 133 (attributes: none)

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### rule at line 134 (attributes: none)

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### rule at line 135 (attributes: none)

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### rule at line 136 (attributes: none)

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### rule at line 137 (attributes: none)

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### rule at line 138 (attributes: none)

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### rule at line 139 (attributes: none)

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### syntax at line 142 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### rule at line 143 (attributes: concrete)

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### rule at line 144 (attributes: none)

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### rule at line 145 (attributes: none)

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### rule at line 146 (attributes: none)

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### rule at line 147 (attributes: none)

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### rule at line 148 (attributes: none)

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### rule at line 149 (attributes: none)

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### rule at line 150 (attributes: none)

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### rule at line 151 (attributes: none)

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### rule at line 154 (attributes: none)

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### rule at line 155 (attributes: none)

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### syntax at line 160 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### rule at line 161 (attributes: concrete)

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### rule at line 162 (attributes: none)

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
```

### syntax at line 165 (attributes: function)

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### rule at line 166 (attributes: none)

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### syntax at line 167 (attributes: function, total)

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### rule at line 168 (attributes: none)

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### rule at line 169 (attributes: none)

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### rule at line 170 (attributes: none)

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### rule at line 171 (attributes: none)

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
```

### syntax at line 173 (attributes: function, total)

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### rule at line 174 (attributes: none)

```k
  rule fracPart(.IntSeq) => 0
```

### rule at line 175 (attributes: none)

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### rule at line 176 (attributes: none)

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### rule at line 177 (attributes: none)

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### rule at line 178 (attributes: none)

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### syntax at line 179 (attributes: function, total)

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### rule at line 180 (attributes: none)

```k
  rule fracScale(.IntSeq) => 1
```

### rule at line 181 (attributes: none)

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### rule at line 182 (attributes: none)

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### rule at line 183 (attributes: none)

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### rule at line 184 (attributes: none)

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### rule at line 185 (attributes: none)

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### rule at line 186 (attributes: none)

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### rule at line 187 (attributes: none)

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### syntax at line 190 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### rule at line 191 (attributes: concrete)

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### rule at line 192 (attributes: none)

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### syntax at line 195 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### rule at line 196 (attributes: concrete)

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### rule at line 197 (attributes: none)

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### rule at line 198 (attributes: none)

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### rule at line 199 (attributes: none)

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### rule at line 200 (attributes: none)

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### rule at line 201 (attributes: none)

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### rule at line 202 (attributes: none)

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### rule at line 203 (attributes: none)

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### rule at line 204 (attributes: none)

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### rule at line 205 (attributes: none)

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### rule at line 206 (attributes: none)

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### syntax at line 209 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### rule at line 210 (attributes: concrete)

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### rule at line 211 (attributes: none)

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### rule at line 213 (attributes: none)

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### rule at line 214 (attributes: none)

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### syntax at line 217 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### rule at line 218 (attributes: concrete)

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### syntax at line 223 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### rule at line 224 (attributes: concrete)

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### rule at line 227 (attributes: none)

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### rule at line 228 (attributes: none)

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### syntax at line 230 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### rule at line 231 (attributes: concrete)

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### syntax at line 232 (attributes: none)

```k
  syntax KItem ::= "#mathSqrt"
```

### rule at line 233 (attributes: priority)

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### rule at line 234 (attributes: none)

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### rule at line 235 (attributes: none)

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### syntax at line 243 (attributes: none)

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### rule at line 244 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### rule at line 245 (attributes: none)

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### rule at line 246 (attributes: none)

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### rule at line 247 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
```

### syntax at line 250 (attributes: none)

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### rule at line 251 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### rule at line 252 (attributes: none)

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### rule at line 253 (attributes: none)

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### rule at line 254 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
```

### syntax at line 261 (attributes: none)

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### rule at line 262 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
```

### rule at line 265 (attributes: none)

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### rule at line 266 (attributes: none)

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### rule at line 267 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
```

### rule at line 270 (attributes: none)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
```

## `reference-semantics/semantics/functions.k`

### syntax at line 8 (attributes: none)

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### rule at line 14 (attributes: none)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### syntax at line 18 (attributes: none)

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### rule at line 19 (attributes: none)

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### syntax at line 27 (attributes: none)

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### syntax at line 31 (attributes: none)

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### rule at line 33 (attributes: none)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### rule at line 36 (attributes: none)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### rule at line 42 (attributes: none)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### rule at line 47 (attributes: none)

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### rule at line 50 (attributes: none)

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### rule at line 53 (attributes: none)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### rule at line 59 (attributes: none)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### rule at line 63 (attributes: none)

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### rule at line 64 (attributes: none)

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### rule at line 68 (attributes: none)

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### rule at line 78 (attributes: none)

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### rule at line 80 (attributes: none)

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### rule at line 85 (attributes: none)

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## `reference-semantics/semantics/int.k`

### rule at line 7 (attributes: none)

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### rule at line 9 (attributes: none)

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### rule at line 11 (attributes: none)

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### rule at line 12 (attributes: none)

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### rule at line 13 (attributes: none)

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### rule at line 14 (attributes: none)

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### rule at line 15 (attributes: none)

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### rule at line 16 (attributes: none)

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### rule at line 17 (attributes: none)

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### syntax at line 19 (attributes: function)

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### rule at line 20 (attributes: none)

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### rule at line 22 (attributes: none)

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### rule at line 23 (attributes: none)

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### rule at line 24 (attributes: none)

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### rule at line 25 (attributes: none)

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### rule at line 26 (attributes: none)

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### rule at line 27 (attributes: none)

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## `reference-semantics/semantics/iter.k`

### syntax at line 8 (attributes: none)

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## `reference-semantics/semantics/list.k`

### rule at line 9 (attributes: none)

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### rule at line 10 (attributes: none)

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### syntax at line 13 (attributes: none)

```k
  syntax ApplyK ::= "toList"
```

### rule at line 14 (attributes: none)

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### rule at line 15 (attributes: none)

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### syntax at line 18 (attributes: function, total)

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### rule at line 19 (attributes: none)

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### rule at line 20 (attributes: none)

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### rule at line 24 (attributes: priority)

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### rule at line 27 (attributes: none)

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### rule at line 28 (attributes: none)

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### syntax at line 33 (attributes: function, total)

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### rule at line 34 (attributes: none)

```k
  rule hasRefVS(.ValSeq)                => false
```

### rule at line 35 (attributes: none)

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### syntax at line 37 (attributes: function)

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### rule at line 39 (attributes: none)

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### rule at line 40 (attributes: none)

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### rule at line 41 (attributes: none)

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### rule at line 42 (attributes: none)

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### rule at line 45 (attributes: none)

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
```

### rule at line 47 (attributes: none)

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
```

### rule at line 49 (attributes: none)

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### rule at line 50 (attributes: owise)

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### rule at line 53 (attributes: priority)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### syntax at line 58 (attributes: none)

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### rule at line 59 (attributes: none)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### rule at line 60 (attributes: none)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### rule at line 61 (attributes: none)

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### rule at line 62 (attributes: none)

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### rule at line 63 (attributes: none)

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
```

### rule at line 65 (attributes: none)

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
```

### rule at line 67 (attributes: none)

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## `reference-semantics/semantics/methods.k`

### syntax at line 10 (attributes: function)

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### rule at line 13 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### rule at line 14 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### rule at line 15 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### rule at line 16 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### rule at line 19 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### rule at line 20 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### rule at line 21 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### rule at line 26 (attributes: none)

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### syntax at line 27 (attributes: function, total)

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### rule at line 28 (attributes: none)

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### rule at line 29 (attributes: none)

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### rule at line 30 (attributes: none)

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### rule at line 34 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### syntax at line 35 (attributes: function)

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### rule at line 36 (attributes: none)

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### rule at line 37 (attributes: none)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
```

### rule at line 39 (attributes: none)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
```

### syntax at line 41 (attributes: function, total)

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### rule at line 42 (attributes: none)

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### rule at line 43 (attributes: owise)

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### rule at line 44 (attributes: none)

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### rule at line 47 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### syntax at line 48 (attributes: function, total)

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### rule at line 49 (attributes: none)

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### rule at line 50 (attributes: none)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### rule at line 51 (attributes: none)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### syntax at line 52 (attributes: function, total)

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### rule at line 53 (attributes: none)

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### rule at line 54 (attributes: none)

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### rule at line 55 (attributes: none)

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### rule at line 58 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### rule at line 61 (attributes: none)

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### rule at line 64 (attributes: none)

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### syntax at line 65 (attributes: function, total)

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### rule at line 66 (attributes: none)

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### rule at line 67 (attributes: none)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### rule at line 68 (attributes: none)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### rule at line 72 (attributes: priority)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### syntax at line 75 (attributes: function)

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### rule at line 76 (attributes: none)

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### rule at line 77 (attributes: none)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
```

### rule at line 79 (attributes: none)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
```

### syntax at line 82 (attributes: function)

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### rule at line 83 (attributes: none)

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### rule at line 84 (attributes: none)

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### syntax at line 85 (attributes: function, total)

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### rule at line 86 (attributes: none)

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### rule at line 89 (attributes: priority)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### rule at line 94 (attributes: priority)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### syntax at line 97 (attributes: function)

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### rule at line 98 (attributes: none)

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### rule at line 99 (attributes: none)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
```

### rule at line 101 (attributes: none)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
```

### rule at line 104 (attributes: none)

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### syntax at line 106 (attributes: function, total)

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### rule at line 107 (attributes: none)

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### rule at line 108 (attributes: none)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### rule at line 109 (attributes: none)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### syntax at line 112 (attributes: function, total)

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### rule at line 113 (attributes: none)

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### syntax at line 115 (attributes: function, total)

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### rule at line 116 (attributes: none)

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### syntax at line 118 (attributes: function, total)

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### rule at line 119 (attributes: none)

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### syntax at line 121 (attributes: function, total)

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### rule at line 122 (attributes: none)

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### syntax at line 124 (attributes: function, total)

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### rule at line 125 (attributes: none)

```k
  rule hasUpper(.IntSeq) => false
```

### rule at line 126 (attributes: none)

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### syntax at line 128 (attributes: function, total)

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### rule at line 129 (attributes: none)

```k
  rule hasLower(.IntSeq) => false
```

### rule at line 130 (attributes: none)

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### syntax at line 132 (attributes: function, total)

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### rule at line 133 (attributes: none)

```k
  rule allAlpha(.IntSeq) => true
```

### rule at line 134 (attributes: none)

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### syntax at line 136 (attributes: function, total)

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### rule at line 137 (attributes: none)

```k
  rule allDigit(.IntSeq) => true
```

### rule at line 138 (attributes: none)

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### syntax at line 140 (attributes: function, total)

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### rule at line 142 (attributes: none)

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### rule at line 143 (attributes: owise)

```k
  rule lowerC(C:Int) => C         [owise]
```

### syntax at line 145 (attributes: function, total)

```k
  syntax Int ::= upperC(Int) [function, total]
```

### rule at line 146 (attributes: none)

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### rule at line 147 (attributes: owise)

```k
  rule upperC(C:Int) => C         [owise]
```

### syntax at line 149 (attributes: function, total)

```k
  syntax Int ::= swapC(Int) [function, total]
```

### rule at line 150 (attributes: none)

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### rule at line 151 (attributes: none)

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### rule at line 152 (attributes: owise)

```k
  rule swapC(C:Int) => C         [owise]
```

### syntax at line 154 (attributes: function, total)

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### rule at line 155 (attributes: none)

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### rule at line 156 (attributes: none)

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### syntax at line 158 (attributes: function, total)

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### rule at line 159 (attributes: none)

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### rule at line 160 (attributes: none)

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### syntax at line 162 (attributes: function, total)

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### rule at line 163 (attributes: none)

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### rule at line 164 (attributes: none)

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### syntax at line 166 (attributes: function, total)

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### rule at line 167 (attributes: none)

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### rule at line 168 (attributes: none)

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule at line 169 (attributes: none)

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## `reference-semantics/semantics/operators.k`

### rule at line 10 (attributes: none)

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### rule at line 12 (attributes: none)

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### context at line 15 (attributes: none)

```k
  context Compare(HOLE, _)
```

### context at line 16 (attributes: none)

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### rule at line 17 (attributes: owise)

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### rule at line 19 (attributes: none)

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### rule at line 20 (attributes: none)

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### rule at line 25 (attributes: priority)

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at line 28 (attributes: none)

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### rule at line 34 (attributes: none)

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### rule at line 38 (attributes: none)

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### rule at line 44 (attributes: priority)

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/range.k`

### syntax at line 9 (attributes: function, total)

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### rule at line 10 (attributes: none)

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### syntax at line 12 (attributes: function)

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### rule at line 13 (attributes: none)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
```

### rule at line 15 (attributes: none)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
```

### rule at line 17 (attributes: none)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
```

### rule at line 20 (attributes: none)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
```

### rule at line 23 (attributes: none)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
```

## `reference-semantics/semantics/set.k`

### syntax at line 8 (attributes: none)

```k
  syntax Val ::= setV(IntSeq)
```

### syntax at line 11 (attributes: function, total)

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### rule at line 12 (attributes: none)

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### rule at line 13 (attributes: none)

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### syntax at line 16 (attributes: function, total)

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### rule at line 18 (attributes: none)

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### rule at line 19 (attributes: none)

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### rule at line 20 (attributes: none)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
```

### rule at line 22 (attributes: none)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
```

### syntax at line 25 (attributes: function, total)

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### rule at line 26 (attributes: none)

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### rule at line 27 (attributes: none)

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### syntax at line 31 (attributes: function, total)

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### rule at line 32 (attributes: none)

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### rule at line 33 (attributes: none)

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### syntax at line 35 (attributes: function, total)

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### rule at line 36 (attributes: none)

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### rule at line 39 (attributes: none)

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## `reference-semantics/semantics/sort.k`

### syntax at line 18 (attributes: function, total, symbol, no-evaluators)

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### syntax at line 19 (attributes: function)

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### rule at line 20 (attributes: concrete)

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### rule at line 21 (attributes: concrete)

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### rule at line 22 (attributes: concrete)

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### rule at line 23 (attributes: concrete)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### rule at line 24 (attributes: concrete)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### syntax at line 26 (attributes: function)

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### rule at line 27 (attributes: concrete)

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### rule at line 28 (attributes: concrete)

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### rule at line 29 (attributes: none)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
```

### rule at line 31 (attributes: none)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
```

### rule at line 36 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### rule at line 40 (attributes: priority)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### syntax at line 49 (attributes: function, total, symbol, no-evaluators)

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### syntax at line 51 (attributes: function, total)

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### rule at line 53 (attributes: none)

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### rule at line 54 (attributes: none)

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### rule at line 55 (attributes: none)

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### syntax at line 57 (attributes: function, total)

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### rule at line 58 (attributes: none)

```k
  rule condRev(S:ValSeq, false) => S
```

### rule at line 59 (attributes: none)

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### rule at line 61 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### rule at line 63 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### rule at line 65 (attributes: none)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

## `reference-semantics/semantics/str.k`

### rule at line 8 (attributes: none)

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### rule at line 9 (attributes: none)

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### syntax at line 13 (attributes: function)

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### rule at line 14 (attributes: none)

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### rule at line 15 (attributes: none)

```k
  rule strToCodes("") => .IntSeq
```

### rule at line 16 (attributes: none)

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
```

### syntax at line 20 (attributes: function, total)

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### rule at line 21 (attributes: none)

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### rule at line 22 (attributes: none)

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### rule at line 24 (attributes: none)

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### rule at line 25 (attributes: none)

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### rule at line 26 (attributes: none)

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### rule at line 29 (attributes: none)

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### rule at line 30 (attributes: none)

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### syntax at line 32 (attributes: function, total)

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### rule at line 33 (attributes: none)

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### rule at line 34 (attributes: none)

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule at line 35 (attributes: none)

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### syntax at line 37 (attributes: function, total)

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### rule at line 38 (attributes: none)

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### rule at line 39 (attributes: none)

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### rule at line 40 (attributes: none)

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
```

### syntax at line 48 (attributes: function, total)

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### rule at line 49 (attributes: none)

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### rule at line 50 (attributes: none)

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### rule at line 51 (attributes: none)

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule at line 52 (attributes: none)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### rule at line 53 (attributes: none)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### rule at line 54 (attributes: none)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### rule at line 56 (attributes: none)

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### rule at line 57 (attributes: none)

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### rule at line 58 (attributes: none)

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### rule at line 59 (attributes: none)

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## `reference-semantics/semantics/subscript.k`

### syntax at line 11 (attributes: function, total)

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### rule at line 12 (attributes: none)

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### rule at line 13 (attributes: none)

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
```

### syntax at line 16 (attributes: function)

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### rule at line 17 (attributes: none)

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### rule at line 18 (attributes: none)

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
```

### syntax at line 21 (attributes: function, total)

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### rule at line 22 (attributes: none)

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### rule at line 23 (attributes: none)

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### context at line 27 (attributes: none)

```k
  context Subscript(HOLE, _)
```

### context at line 28 (attributes: none)

```k
  context Subscript(_:Val, HOLE:Expr)
```

### rule at line 31 (attributes: priority)

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at line 35 (attributes: none)

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### syntax at line 37 (attributes: function)

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### rule at line 38 (attributes: none)

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### rule at line 39 (attributes: none)

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### rule at line 40 (attributes: none)

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### syntax at line 44 (attributes: none)

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### syntax at line 49 (attributes: none)

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### rule at line 50 (attributes: none)

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### rule at line 51 (attributes: none)

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### rule at line 52 (attributes: none)

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### rule at line 54 (attributes: none)

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### rule at line 55 (attributes: none)

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### rule at line 56 (attributes: none)

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### rule at line 58 (attributes: priority)

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### rule at line 61 (attributes: none)

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### syntax at line 63 (attributes: function)

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### rule at line 64 (attributes: none)

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### rule at line 66 (attributes: none)

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### rule at line 68 (attributes: none)

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### syntax at line 72 (attributes: function, total)

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### rule at line 73 (attributes: none)

```k
  rule slStep(noB)          => 1
```

### rule at line 74 (attributes: none)

```k
  rule slStep(someB(S:Int)) => S
```

### syntax at line 76 (attributes: function)

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### rule at line 77 (attributes: none)

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
```

### rule at line 79 (attributes: none)

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
```

### rule at line 81 (attributes: none)

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### syntax at line 83 (attributes: function)

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### rule at line 84 (attributes: none)

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
```

### rule at line 86 (attributes: none)

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
```

### rule at line 88 (attributes: none)

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### syntax at line 90 (attributes: function, total)

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### rule at line 91 (attributes: none)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
```

### rule at line 93 (attributes: none)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
```

### syntax at line 96 (attributes: function, total)

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### rule at line 97 (attributes: none)

```k
  rule clampLo(J:Int, _STEP:Int) => J
```

### rule at line 99 (attributes: none)

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
```

### syntax at line 102 (attributes: function, total)

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### rule at line 103 (attributes: none)

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
```

### rule at line 105 (attributes: none)

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
```

### syntax at line 109 (attributes: function)

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### rule at line 110 (attributes: none)

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
```

### rule at line 113 (attributes: none)

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
```

### syntax at line 116 (attributes: function)

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### rule at line 117 (attributes: none)

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
```

### rule at line 120 (attributes: none)

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
```

## `reference-semantics/semantics/syntax.k`

### syntax at line 9 (attributes: macro, strict, seqstrict)

```k
  syntax Expr ::= "Int"      "(" Int ")"
                | "Float"    "(" Float ")"
                | "Bool"     "(" Bool ")"
                | "Name"     "(" String ")"
                | "Str"      "(" String ")"
                | "UnaryOp"  "(" String "," Expr ")" [strict(2)]
                | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)]
                | "BoolOp"    "(" String "," Exprs ")"
                | "ListExpr"  "(" Exprs ")"
                | "DictExpr"  "(" Entries ")"
                | "ListComp"  "(" Expr "," CompFors ")" [macro]
                | "GenExp"    "(" Expr "," CompFors ")" [macro]
                | "TupleExpr" "(" Exprs ")"
                | "Subscript" "(" Expr "," Index ")"
                | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)]
                | "Lambda"    "(" Params "," Expr ")"
                | "KwArg"     "(" String "," Expr ")"
                | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")"
                | "NoneVal"
                | "Call"      "(" Expr "," Exprs ")"
                | "Attribute" "(" Expr "," String ")" [strict(1)]
                | "Compare"   "(" Expr "," CmpOp ")"
```

### syntax at line 32 (attributes: none)

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### syntax at line 33 (attributes: none)

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### syntax at line 34 (attributes: none)

```k
  syntax Entries  ::= List{Entry, ","}
```

### syntax at line 35 (attributes: none)

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### syntax at line 36 (attributes: none)

```k
  syntax CompFors ::= List{CompFor, ""}
```

### syntax at line 37 (attributes: none)

```k
  syntax Exprs    ::= List{Expr, ","}
```

### syntax at line 38 (attributes: none)

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### syntax at line 39 (attributes: none)

```k
  syntax Bound    ::= Expr | "NoBound"
```

### syntax at line 41 (attributes: strict)

```k
  syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)]
                | "Import"    "(" String ")"
                | "ImportFrom" "(" String "," ParamNames ")"
                | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)]
                | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)]
                | "While"     "(" Expr "," Stmts ")"
                | "Break"
                | "Continue"
                | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)]
                | "Return"    "(" Expr ")" [strict]
                | "Assert"    "(" Expr ")" [strict]
                | "Expr"      "(" Expr ")" [strict]
                | "FuncDef"   "(" String "," Params "," Stmts ")"
                | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
```

### syntax at line 56 (attributes: none)

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### syntax at line 57 (attributes: none)

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### syntax at line 58 (attributes: none)

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### syntax at line 59 (attributes: none)

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### syntax at line 60 (attributes: none)

```k
  syntax ParamNames ::= List{String, ","}
```

### syntax at line 61 (attributes: none)

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## `reference-semantics/semantics/tuple.k`

### rule at line 10 (attributes: none)

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### rule at line 11 (attributes: none)

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### syntax at line 14 (attributes: none)

```k
  syntax ApplyK ::= "toTuple"
```

### rule at line 15 (attributes: none)

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### rule at line 16 (attributes: none)

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### rule at line 18 (attributes: none)

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### rule at line 20 (attributes: none)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### rule at line 21 (attributes: none)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### rule at line 23 (attributes: none)

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### syntax at line 24 (attributes: function)

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### rule at line 25 (attributes: none)

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### rule at line 26 (attributes: none)

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
```

### rule at line 28 (attributes: none)

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### syntax at line 31 (attributes: none)

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### rule at line 32 (attributes: none)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### rule at line 35 (attributes: none)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### rule at line 42 (attributes: none)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### rule at line 43 (attributes: none)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### rule at line 44 (attributes: priority)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### syntax at line 49 (attributes: none)

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### rule at line 50 (attributes: none)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### rule at line 51 (attributes: none)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### rule at line 52 (attributes: priority)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at line 55 (attributes: none)

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### rule at line 57 (attributes: none)

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## `verification.k`

### syntax at line 9 (attributes: function, total, symbol, no-evaluators)

```k
  syntax Float ::= minVF(ValSeq) [function, total, symbol(minVF), no-evaluators]
                 | maxVF(ValSeq) [function, total, symbol(maxVF), no-evaluators]
```

### rule at line 12 (attributes: priority)

```k
  rule <k> #applyK(toCall(builtinV("min")), (list(VS:ValSeq), .Vals))
        => minVF(VS) ... </k>
       [priority(40)]
```

### rule at line 15 (attributes: priority)

```k
  rule <k> #applyK(toCall(builtinV("max")), (list(VS:ValSeq), .Vals))
        => maxVF(VS) ... </k>
       [priority(40)]
```

### syntax at line 21 (attributes: function, total, symbol)

```k
  syntax Float ::= asFloat(Val) [function, total, symbol(asFloat)]
```

### rule at line 22 (attributes: none)

```k
  rule asFloat(F:Float) => F
```

### syntax at line 24 (attributes: function, total)

```k
  syntax Float ::= scaleF(Float, Float, Float) [function, total]
```

### rule at line 25 (attributes: none)

```k
  rule scaleF(F:Float, LO:Float, HI:Float)
    => divF(subF(F, LO), subF(HI, LO))
```

### syntax at line 28 (attributes: function, total)

```k
  syntax ValSeq ::= scaleAcc(ValSeq, ValSeq, Float, Float) [function, total]
```

### rule at line 29 (attributes: none)

```k
  rule scaleAcc(ACC:ValSeq, .ValSeq, _:Float, _:Float) => ACC
```

### rule at line 30 (attributes: none)

```k
  rule scaleAcc(ACC:ValSeq, vCons(V:Val, REST:ValSeq), LO:Float, HI:Float)
    => scaleAcc(
         valSeqConcat(ACC, vCons(scaleF(asFloat(V), LO, HI), .ValSeq)),
         REST,
         LO,
         HI)
```

### syntax at line 37 (attributes: function, total)

```k
  syntax Bool ::= allFloats(ValSeq) [function, total]
```

### rule at line 38 (attributes: none)

```k
  rule allFloats(.ValSeq) => true
```

### rule at line 39 (attributes: none)

```k
  rule allFloats(vCons(V:Val, REST:ValSeq))
    => isFloat(V) andBool allFloats(REST)
```

### syntax at line 44 (attributes: none)

```k
  syntax FloatSeq ::= ".FloatSeq" | fCons(Float, FloatSeq)
```

### syntax at line 45 (attributes: function, total)

```k
  syntax ValSeq ::= injectFloats(FloatSeq) [function, total]
```

### rule at line 46 (attributes: none)

```k
  rule injectFloats(.FloatSeq) => .ValSeq
```

### rule at line 47 (attributes: none)

```k
  rule injectFloats(fCons(F:Float, REST:FloatSeq))
    => vCons(F, injectFloats(REST))
```

### rule at line 54 (attributes: none)

```k
  rule <k>
         ListComp(
           BinOp(
             "/",
             BinOp("-", Name("number"), Name("min_number")),
             BinOp("-", Name("max_number"), Name("min_number"))),
           CompFor(
             Name("number"),
             Name("numbers"),
             Bool(true)))
         => #alloc(list(scaleAcc(.ValSeq, VS, LO, HI)))
         ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap>
         ...
         MINH:Int |-> cellV(LO:Float)
         MAXH:Int |-> cellV(HI:Float)
         ...
       </heap>
```

### syntax at line 85 (attributes: none)

```k
  syntax KItem ::= "#observe"
```

### rule at line 86 (attributes: none)

```k
  rule <k> ref(H:Int) ~> #observe => V ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### syntax at line 91 (attributes: none)

```k
  syntax KItem ::= #runRescale(ValSeq)
```

### rule at line 92 (attributes: none)

```k
  rule <k> #runRescale(VS:ValSeq)
        => #loadAll(Module(
             ImportFrom("typing", "List")
             FuncDef(
               "rescale_to_unit",
               Params("numbers"),
               CellVars("max_number", "min_number"),
               FreeVars(.ParamNames),
               Assign(
                 Name("min_number"),
                 Call(Name("min"), Name("numbers")))
               Assign(
                 Name("max_number"),
                 Call(Name("max"), Name("numbers")))
               Return(
                 ListComp(
                   BinOp(
                     "/",
                     BinOp("-", Name("number"), Name("min_number")),
                     BinOp("-", Name("max_number"), Name("min_number"))),
                   CompFor(
                     Name("number"),
                     Name("numbers"),
                     Bool(true)))))))
           ~> Call(Name("rescale_to_unit"), list(VS))
           ~> #observe
           ...
       </k>
```

## `spec.k`

### claim at line 6 (attributes: none)

```k
  claim
    <k>
      #runRescale(
        vCons(FIRST:Float,
          vCons(SECOND:Float, REST:ValSeq)))
      => list(
           scaleAcc(
             .ValSeq,
             vCons(FIRST,
               vCons(SECOND, REST)),
             minVF(
               vCons(FIRST,
                 vCons(SECOND, REST))),
             maxVF(
               vCons(FIRST,
                 vCons(SECOND, REST)))))
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
```


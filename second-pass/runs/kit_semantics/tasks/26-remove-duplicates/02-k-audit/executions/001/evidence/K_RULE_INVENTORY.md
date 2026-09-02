# Exhaustive K source inventory

Files: 26
Items: 1103

## Counts by item kind

- claim: 2
- configuration: 1
- context: 5
- endmodule: 27
- imports: 88
- module: 27
- requires: 25
- rule: 699
- syntax: 229

## Counts by classification tag

- concrete: 36
- equational: 461
- function: 148
- macro: 4
- macro-rec: 1
- no-evaluators: 22
- opaque: 22
- operational: 238
- owise: 26
- priority: 45
- seqstrict: 1
- strict: 2
- symbol: 25
- total: 109

## File inventory

### `reference-semantics/semantics/assert.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-ASSERT
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 6; kind `rule`; tags `operational`

  ```k
    rule <k> Assert(V:Val) => .K ... </k>
         requires truthy(V)
  ```

- Line 8; kind `rule`; tags `operational`

  ```k
    rule <k> Assert(V:Val) ~> _ => .K </k>
         <exc> NoExc => AssertionError </exc>
         <exit-code> _ => 1 </exit-code>
         requires notBool truthy(V)
  ```

- Line 13; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 16; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/bool.k`

- Line 5; kind `module`; tags `none`

  ```k
  module MPY-BOOL
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 8; kind `rule`; tags `equational`

  ```k
    rule applyUn("not", V:Val) => notBool truthy(V)
  ```

- Line 10; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
  ```

- Line 11; kind `rule`; tags `equational`

  ```k
    rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
  ```

- Line 16; kind `context`; tags `none`

  ```k
    context BoolOp(_, (HOLE:Expr, _:Exprs))
  ```

- Line 17; kind `rule`; tags `operational`

  ```k
    rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
  ```

- Line 18; kind `rule`; tags `operational`

  ```k
    rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
         requires truthy(V)
  ```

- Line 20; kind `rule`; tags `operational`

  ```k
    rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
         requires notBool truthy(V)
  ```

- Line 22; kind `rule`; tags `operational`

  ```k
    rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
         requires truthy(V)
  ```

- Line 24; kind `rule`; tags `operational`

  ```k
    rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
         requires notBool truthy(V)
  ```

- Line 29; kind `rule`; tags `priority, operational`

  ```k
    rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
         [priority(40)]
  ```

- Line 31; kind `rule`; tags `priority, operational`

  ```k
    rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires truthy(V)
         [priority(40)]
  ```

- Line 35; kind `rule`; tags `priority, operational`

  ```k
    rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool truthy(V)
         [priority(40)]
  ```

- Line 39; kind `rule`; tags `priority, operational`

  ```k
    rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires truthy(V)
         [priority(40)]
  ```

- Line 43; kind `rule`; tags `priority, operational`

  ```k
    rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool truthy(V)
         [priority(40)]
  ```

- Line 47; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/builtins.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-BUILTINS
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports MPY-STR
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports MPY-SET
  ```

- Line 7; kind `imports`; tags `none`

  ```k
    imports MPY-ITER
  ```

- Line 8; kind `imports`; tags `none`

  ```k
    imports MPY-RANGE
  ```

- Line 9; kind `imports`; tags `none`

  ```k
    imports MPY-INT
  ```

- Line 10; kind `imports`; tags `none`

  ```k
    imports MPY-METHODS
  ```

- Line 17; kind `syntax`; tags `function`

  ```k
    syntax Val ::= applyBuiltin(String, Vals) [function]
  ```

- Line 20; kind `syntax`; tags `function`

  ```k
    syntax Int ::= seqLen(Val) [function]
  ```

- Line 21; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
  ```

- Line 22; kind `rule`; tags `equational`

  ```k
    rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
  ```

- Line 23; kind `rule`; tags `equational`

  ```k
    rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
  ```

- Line 24; kind `rule`; tags `equational`

  ```k
    rule seqLen(str(IS:IntSeq))                   => isLen(IS)
  ```

- Line 25; kind `rule`; tags `equational`

  ```k
    rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
  ```

- Line 26; kind `rule`; tags `equational`

  ```k
    rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
  ```

- Line 32; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
  ```

- Line 33; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
  ```

- Line 34; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
  ```

- Line 35; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
  ```

- Line 36; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= charsOf(IntSeq) [function, total]
  ```

- Line 37; kind `rule`; tags `equational`

  ```k
    rule charsOf(.IntSeq)                => .ValSeq
  ```

- Line 38; kind `rule`; tags `equational`

  ```k
    rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
  ```

- Line 41; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
  ```

- Line 44; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
  ```

- Line 47; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
  ```

- Line 48; kind `rule`; tags `operational`

  ```k
    rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
  ```

- Line 49; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
  ```

- Line 50; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
          => #sumAcc(R, ACC +Int intOf(V)) ... </k>
         requires isInt(V) orBool isBool(V)
  ```

- Line 54; kind `syntax`; tags `function`

  ```k
    syntax Int ::= intOf(Val) [function]
  ```

- Line 55; kind `rule`; tags `equational`

  ```k
    rule intOf(I:Int)  => I
  ```

- Line 56; kind `rule`; tags `equational`

  ```k
    rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
  ```

- Line 59; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #allAcc(Iterable) | "#allCont"
  ```

- Line 60; kind `rule`; tags `operational`

  ```k
    rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
  ```

- Line 61; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #allCont => true ... </k>
  ```

- Line 62; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
         requires truthy(V)
  ```

- Line 64; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
         requires notBool truthy(V)
  ```

- Line 67; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
  ```

- Line 68; kind `rule`; tags `operational`

  ```k
    rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
  ```

- Line 69; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #anyCont => false ... </k>
  ```

- Line 70; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
         requires truthy(V)
  ```

- Line 72; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
         requires notBool truthy(V)
  ```

- Line 76; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
  ```

- Line 77; kind `rule`; tags `operational`

  ```k
    rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
  ```

- Line 78; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
         requires isInt(V)
  ```

- Line 80; kind `rule`; tags `operational`

  ```k
    rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
  ```

- Line 81; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
  ```

- Line 82; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
          => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
         requires isInt(V)
  ```

- Line 86; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
  ```

- Line 87; kind `rule`; tags `operational`

  ```k
    rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
  ```

- Line 88; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
         requires isInt(V)
  ```

- Line 90; kind `rule`; tags `operational`

  ```k
    rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
  ```

- Line 91; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
  ```

- Line 92; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
          => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
         requires isInt(V)
  ```

- Line 97; kind `syntax`; tags `function`

  ```k
    syntax Int ::= maxVals(Int, Vals) [function]
  ```

- Line 98; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
  ```

- Line 99; kind `rule`; tags `equational`

  ```k
    rule maxVals(M:Int, .Vals)           => M
  ```

- Line 100; kind `rule`; tags `equational`

  ```k
    rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
  ```

- Line 102; kind `syntax`; tags `function`

  ```k
    syntax Int ::= minVals(Int, Vals) [function]
  ```

- Line 103; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
  ```

- Line 104; kind `rule`; tags `equational`

  ```k
    rule minVals(M:Int, .Vals)           => M
  ```

- Line 105; kind `rule`; tags `equational`

  ```k
    rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
  ```

- Line 108; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
         requires N >=Int 0
  ```

- Line 111; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("bin", N:Int, .Vals)
      => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
         requires N <Int 0
  ```

- Line 114; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= binCodes(Int) [function, total]
  ```

- Line 115; kind `rule`; tags `equational`

  ```k
    rule binCodes(0) => iCons(48, .IntSeq)
  ```

- Line 116; kind `rule`; tags `equational`

  ```k
    rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
  ```

- Line 117; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
  ```

- Line 118; kind `rule`; tags `equational`

  ```k
    rule binAcc(0, ACC:IntSeq) => ACC
  ```

- Line 119; kind `rule`; tags `equational`

  ```k
    rule binAcc(N:Int, ACC:IntSeq)
      => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
         requires N >Int 0
  ```

- Line 124; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
          => #alloc(list(enumVS(VS, 0))) ... </k>
  ```

- Line 126; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
  ```

- Line 127; kind `rule`; tags `equational`

  ```k
    rule enumVS(.ValSeq, _:Int) => .ValSeq
  ```

- Line 128; kind `rule`; tags `equational`

  ```k
    rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
      => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
  ```

- Line 132; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
          => #alloc(list(mapStrVS(VS))) ... </k>
  ```

- Line 134; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
  ```

- Line 135; kind `rule`; tags `equational`

  ```k
    rule mapStrVS(.ValSeq) => .ValSeq
  ```

- Line 136; kind `rule`; tags `equational`

  ```k
    rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
  ```

- Line 137; kind `rule`; tags `equational`

  ```k
    rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
  ```

- Line 140; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("int", I:Int, .Vals) => I
  ```

- Line 143; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
  ```

- Line 144; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
         requires 0 <=Int I andBool I <Int 128
  ```

- Line 148; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
  ```

- Line 149; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
  ```

- Line 152; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
         requires 48 <=Int C andBool C <=Int 57
  ```

- Line 156; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
         requires isLen(CS) >=Int 2
  ```

- Line 158; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
  ```

- Line 159; kind `rule`; tags `equational`

  ```k
    rule intDigAcc(.IntSeq, ACC:Int)             => ACC
  ```

- Line 160; kind `rule`; tags `equational`

  ```k
    rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
  ```

- Line 163; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
  ```

- Line 164; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
  ```

- Line 167; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
          => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
  ```

- Line 169; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
  ```

- Line 170; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
  ```

- Line 171; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
          => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
  ```

- Line 173; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
  ```

- Line 174; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
  ```

- Line 177; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
  ```

- Line 178; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
  ```

- Line 179; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
         requires S =/=Int 0
  ```

- Line 187; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
  ```

- Line 188; kind `syntax`; tags `function`

  ```k
    syntax Int ::= evalArith(IntSeq) [function]
  ```

- Line 189; kind `rule`; tags `equational`

  ```k
    rule evalArith(CS:IntSeq)
      => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
  ```

- Line 192; kind `syntax`; tags `none`

  ```k
    syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
  ```

- Line 194; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= evDigit(Int) [function, total]
  ```

- Line 195; kind `rule`; tags `equational`

  ```k
    rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
  ```

- Line 196; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= evHead42(IntSeq) [function, total]
  ```

- Line 197; kind `rule`; tags `equational`

  ```k
    rule evHead42(iCons(42, _:IntSeq)) => true
  ```

- Line 198; kind `rule`; tags `owise, equational`

  ```k
    rule evHead42(_:IntSeq)            => false [owise]
  ```

- Line 199; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= evHead47(IntSeq) [function, total]
  ```

- Line 200; kind `rule`; tags `equational`

  ```k
    rule evHead47(iCons(47, _:IntSeq)) => true
  ```

- Line 201; kind `rule`; tags `owise, equational`

  ```k
    rule evHead47(_:IntSeq)            => false [owise]
  ```

- Line 203; kind `syntax`; tags `function, total`

  ```k
    syntax OpSeq ::= tokOps(IntSeq) [function, total]
  ```

- Line 204; kind `rule`; tags `equational`

  ```k
    rule tokOps(.IntSeq)                 => .OpSeq
  ```

- Line 205; kind `rule`; tags `equational`

  ```k
    rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
  ```

- Line 206; kind `rule`; tags `equational`

  ```k
    rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
  ```

- Line 207; kind `rule`; tags `equational`

  ```k
    rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
  ```

- Line 208; kind `rule`; tags `equational`

  ```k
    rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
  ```

- Line 209; kind `rule`; tags `equational`

  ```k
    rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
  ```

- Line 210; kind `rule`; tags `equational`

  ```k
    rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
  ```

- Line 211; kind `rule`; tags `equational`

  ```k
    rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
  ```

- Line 212; kind `rule`; tags `equational`

  ```k
    rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
  ```

- Line 214; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= tokNds(IntSeq) [function, total]
                    | tokNdAcc(Int, IntSeq) [function, total]
  ```

- Line 216; kind `rule`; tags `equational`

  ```k
    rule tokNds(.IntSeq)                => .IntSeq
  ```

- Line 217; kind `rule`; tags `equational`

  ```k
    rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
  ```

- Line 218; kind `rule`; tags `equational`

  ```k
    rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
  ```

- Line 219; kind `rule`; tags `equational`

  ```k
    rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
         requires notBool evDigit(C) andBool C =/=Int 32
  ```

- Line 221; kind `rule`; tags `equational`

  ```k
    rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
         requires evDigit(C)
  ```

- Line 223; kind `rule`; tags `owise, equational`

  ```k
    rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
  ```

- Line 225; kind `syntax`; tags `none`

  ```k
    syntax EvPair ::= evp(OpSeq, IntSeq)
  ```

- Line 226; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= firstNdE(EvPair) [function, total]
  ```

- Line 227; kind `rule`; tags `equational`

  ```k
    rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
  ```

- Line 228; kind `rule`; tags `owise, equational`

  ```k
    rule firstNdE(_:EvPair) => 0 [owise]
  ```

- Line 230; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= applyOpE(String, Int, Int) [function, total]
  ```

- Line 231; kind `rule`; tags `equational`

  ```k
    rule applyOpE("+",  A:Int, B:Int) => A +Int B
  ```

- Line 232; kind `rule`; tags `equational`

  ```k
    rule applyOpE("-",  A:Int, B:Int) => A -Int B
  ```

- Line 233; kind `rule`; tags `equational`

  ```k
    rule applyOpE("*",  A:Int, B:Int) => A *Int B
  ```

- Line 234; kind `rule`; tags `equational`

  ```k
    rule applyOpE("//", A:Int, B:Int) => A divInt B
  ```

- Line 235; kind `rule`; tags `equational`

  ```k
    rule applyOpE("**", A:Int, B:Int) => A ^Int B
  ```

- Line 236; kind `rule`; tags `owise, equational`

  ```k
    rule applyOpE(_:String, A:Int, _:Int) => A [owise]
  ```

- Line 238; kind `syntax`; tags `function, total`

  ```k
    syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
  ```

- Line 239; kind `rule`; tags `equational`

  ```k
    rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
  ```

- Line 240; kind `rule`; tags `equational`

  ```k
    rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
  ```

- Line 241; kind `rule`; tags `equational`

  ```k
    rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
         requires O =/=String "**"
  ```

- Line 243; kind `rule`; tags `owise, equational`

  ```k
    rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
  ```

- Line 244; kind `syntax`; tags `function, total`

  ```k
    syntax EvPair ::= powCombE(Int, EvPair) [function, total]
  ```

- Line 245; kind `rule`; tags `equational`

  ```k
    rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
  ```

- Line 246; kind `rule`; tags `equational`

  ```k
    rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
  ```

- Line 247; kind `syntax`; tags `function, total`

  ```k
    syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
  ```

- Line 248; kind `rule`; tags `equational`

  ```k
    rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
  ```

- Line 250; kind `syntax`; tags `function, total`

  ```k
    syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
  ```

- Line 251; kind `rule`; tags `equational`

  ```k
    rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
  ```

- Line 252; kind `rule`; tags `equational`

  ```k
    rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
  ```

- Line 253; kind `rule`; tags `equational`

  ```k
    rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
  ```

- Line 254; kind `rule`; tags `equational`

  ```k
    rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
  ```

- Line 255; kind `syntax`; tags `function, total`

  ```k
    syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
  ```

- Line 256; kind `rule`; tags `equational`

  ```k
    rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
  ```

- Line 257; kind `rule`; tags `equational`

  ```k
    rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
      => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
         requires inLevelE(L, O)
  ```

- Line 260; kind `rule`; tags `equational`

  ```k
    rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
      => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
         requires notBool inLevelE(L, O)
  ```

- Line 263; kind `rule`; tags `owise, equational`

  ```k
    rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
      => evp(OO, appendIE(ON, CUR)) [owise]
  ```

- Line 265; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= inLevelE(String, String) [function, total]
  ```

- Line 266; kind `rule`; tags `equational`

  ```k
    rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
  ```

- Line 267; kind `rule`; tags `equational`

  ```k
    rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
  ```

- Line 268; kind `rule`; tags `owise, equational`

  ```k
    rule inLevelE(_:String, _:String) => false [owise]
  ```

- Line 269; kind `syntax`; tags `function, total`

  ```k
    syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
  ```

- Line 270; kind `rule`; tags `equational`

  ```k
    rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
  ```

- Line 271; kind `rule`; tags `equational`

  ```k
    rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
  ```

- Line 272; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
  ```

- Line 273; kind `rule`; tags `equational`

  ```k
    rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
  ```

- Line 274; kind `rule`; tags `equational`

  ```k
    rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
  ```

- Line 279; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= "#md5"
  ```

- Line 280; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
         [priority(40)]
  ```

- Line 282; kind `rule`; tags `operational`

  ```k
    rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
  ```

- Line 283; kind `syntax`; tags `none`

  ```k
    syntax Val ::= md5Obj(IntSeq)
  ```

- Line 284; kind `rule`; tags `equational`

  ```k
    rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
  ```

- Line 285; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
  ```

- Line 291; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
  ```

- Line 292; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
  ```

- Line 293; kind `syntax`; tags `function`

  ```k
    syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
  ```

- Line 294; kind `rule`; tags `equational`

  ```k
    rule isIntV(_:Int)         => true
  ```

- Line 295; kind `rule`; tags `owise, equational`

  ```k
    rule isIntV(_:Val)         => false [owise]
  ```

- Line 296; kind `rule`; tags `equational`

  ```k
    rule isStrV(str(_:IntSeq)) => true
  ```

- Line 297; kind `rule`; tags `owise, equational`

  ```k
    rule isStrV(_:Val)         => false [owise]
  ```

- Line 298; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/call.k`

- Line 10; kind `module`; tags `none`

  ```k
  module MPY-CALL
  ```

- Line 11; kind `imports`; tags `none`

  ```k
    imports MPY-METHODS
  ```

- Line 12; kind `imports`; tags `none`

  ```k
    imports MPY-BUILTINS
  ```

- Line 13; kind `imports`; tags `none`

  ```k
    imports MPY-FUNCTIONS
  ```

- Line 16; kind `rule`; tags `operational`

  ```k
    rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
  ```

- Line 19; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #callee(Exprs)
  ```

- Line 20; kind `rule`; tags `owise, operational`

  ```k
    rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
  ```

- Line 21; kind `rule`; tags `operational`

  ```k
    rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
  ```

- Line 24; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
  ```

- Line 26; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
  ```

- Line 27; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
  ```

- Line 28; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
  ```

- Line 29; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
  ```

- Line 30; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
  ```

- Line 31; kind `rule`; tags `owise, operational`

  ```k
    rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
  ```

- Line 32; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
  ```

- Line 38; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
          => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 42; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
          => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isRefV(A)
         [priority(40)]
  ```

- Line 47; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
          => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 52; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= isMutMethod(String) [function, total]
  ```

- Line 53; kind `rule`; tags `equational`

  ```k
    rule isMutMethod(M:String)
      => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
         orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
  ```

- Line 56; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
          => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isMutMethod(M)
         [priority(40)]
  ```

- Line 63; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
          => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
         [priority(40)]
  ```

- Line 69; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
          => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
         <env>     CALLERL:Int => NEWL </env>
         <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
         <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
         <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
  ```

- Line 80; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
          => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
         <env>     CALLERL:Int => NEWL </env>
         <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
         <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
         <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
  ```

- Line 87; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #allocCells(ParamNames)
  ```

- Line 88; kind `rule`; tags `operational`

  ```k
    rule <k> #allocCells(.ParamNames) => .K ... </k>
  ```

- Line 89; kind `rule`; tags `operational`

  ```k
    rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
         <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
         <heapLoc> N:Int => N +Int 1 </heapLoc>
         requires notBool N in_keys(H)
  ```

- Line 95; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/comprehension.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-COMPREHENSION
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports MPY-OPERATORS
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports MPY-LIST
  ```

- Line 7; kind `imports`; tags `none`

  ```k
    imports MPY-CONTROLS
  ```

- Line 8; kind `imports`; tags `none`

  ```k
    imports MPY-FUNCTIONS
  ```

- Line 11; kind `rule`; tags `equational`

  ```k
    rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
  ```

- Line 12; kind `rule`; tags `equational`

  ```k
    rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
  ```

- Line 14; kind `syntax`; tags `macro`

  ```k
    syntax Stmts ::= compBody(CompFors, Expr) [macro]
  ```

- Line 15; kind `rule`; tags `equational`

  ```k
    rule compBody(Gs:CompFors, ELT:Expr)
      => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
  ```

- Line 18; kind `syntax`; tags `macro, macro-rec`

  ```k
    syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
  ```

- Line 19; kind `rule`; tags `equational`

  ```k
    rule compNest(.CompFors, ELT:Expr)
      => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
  ```

- Line 21; kind `rule`; tags `equational`

  ```k
    rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
      => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
  ```

- Line 24; kind `syntax`; tags `macro`

  ```k
    syntax Expr ::= compGuard(Exprs) [macro]
  ```

- Line 25; kind `rule`; tags `equational`

  ```k
    rule compGuard(.Exprs)             => Bool(true)
  ```

- Line 26; kind `rule`; tags `equational`

  ```k
    rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
  ```

- Line 27; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/concrete.k`

- Line 8; kind `module`; tags `none`

  ```k
  module MPY-CONCRETE
  ```

- Line 9; kind `imports`; tags `none`

  ```k
    imports MPY
  ```

- Line 13; kind `rule`; tags `operational`

  ```k
    rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
         <heap> HP:Map </heap>
         requires hasRefVS(A) orBool hasRefVS(B)
  ```

- Line 16; kind `rule`; tags `operational`

  ```k
    rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
         <heap> HP:Map </heap>
         requires hasRefVS(A) orBool hasRefVS(B)
  ```

- Line 25; kind `syntax`; tags `none`

  ```k
    syntax Val ::= kvP(Val, Val)
  ```

- Line 26; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                   | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
  ```

- Line 28; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
          => #ksort(VS, KV, .ValSeq, false) ... </k>
         [priority(40)]
  ```

- Line 31; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
          => #ksort(VS, KV, .ValSeq, RB) ... </k>
         [priority(40)]
  ```

- Line 34; kind `rule`; tags `operational`

  ```k
    rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
          => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
  ```

- Line 36; kind `rule`; tags `operational`

  ```k
    rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
          => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
  ```

- Line 38; kind `rule`; tags `operational`

  ```k
    rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
          => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
         requires notBool isKwV(K)
  ```

- Line 42; kind `syntax`; tags `function`

  ```k
    syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
  ```

- Line 43; kind `rule`; tags `equational`

  ```k
    rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
  ```

- Line 44; kind `rule`; tags `equational`

  ```k
    rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
      => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
         requires kLt(K, K2)
  ```

- Line 47; kind `rule`; tags `equational`

  ```k
    rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
      => vCons(kvP(K2, V2), insPair(R, K, V))
         requires notBool kLt(K, K2)
  ```

- Line 51; kind `syntax`; tags `function`

  ```k
    syntax Bool ::= kLt(Val, Val) [function]
  ```

- Line 52; kind `rule`; tags `equational`

  ```k
    rule kLt(I1:Int, I2:Int)             => I1 <Int I2
  ```

- Line 53; kind `rule`; tags `equational`

  ```k
    rule kLt(F1:Float, F2:Float)         => F1 <Float F2
  ```

- Line 54; kind `rule`; tags `equational`

  ```k
    rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
  ```

- Line 56; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= unpairVS(ValSeq) [function, total]
  ```

- Line 57; kind `rule`; tags `equational`

  ```k
    rule unpairVS(.ValSeq) => .ValSeq
  ```

- Line 58; kind `rule`; tags `equational`

  ```k
    rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
  ```

- Line 59; kind `rule`; tags `owise, equational`

  ```k
    rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
  ```

- Line 60; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/controls.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-CONTROLS
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports MPY-TUPLE
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports MPY-ITER
  ```

- Line 9; kind `rule`; tags `operational`

  ```k
    rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
  ```

- Line 12; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires "$cells" in_keys(M)
          andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
          andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
         [priority(40)]
  ```

- Line 20; kind `rule`; tags `operational`

  ```k
    rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
         requires X in_keys(M)
  ```

- Line 27; kind `rule`; tags `priority, operational`

  ```k
    rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires X in_keys(M) andBool isRefV({M[X]}:>Val)
         [priority(40)]
  ```

- Line 35; kind `rule`; tags `operational`

  ```k
    rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
  ```

- Line 36; kind `rule`; tags `owise, operational`

  ```k
    rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
  ```

- Line 37; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #bindImports(ParamNames)
  ```

- Line 38; kind `rule`; tags `operational`

  ```k
    rule <k> #bindImports(.ParamNames) => .K ... </k>
  ```

- Line 39; kind `rule`; tags `operational`

  ```k
    rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
         requires N ==String "floor" orBool N ==String "ceil"
  ```

- Line 43; kind `rule`; tags `operational`

  ```k
    rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
         requires notBool (N ==String "floor" orBool N ==String "ceil")
  ```

- Line 48; kind `rule`; tags `operational`

  ```k
    rule <k> Expr(_:Val) => .K ... </k>
  ```

- Line 51; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #branch(Bool, Stmts, Stmts)
  ```

- Line 52; kind `rule`; tags `operational`

  ```k
    rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
  ```

- Line 53; kind `rule`; tags `operational`

  ```k
    rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
  ```

- Line 54; kind `rule`; tags `operational`

  ```k
    rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
  ```

- Line 57; kind `rule`; tags `operational`

  ```k
    rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
         requires truthy(V)
  ```

- Line 59; kind `rule`; tags `operational`

  ```k
    rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
         requires notBool truthy(V)
  ```

- Line 65; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                   | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                   | #loopLbl(K) | "#cont" | "#brk"
  ```

- Line 69; kind `rule`; tags `operational`

  ```k
    rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
  ```

- Line 71; kind `rule`; tags `operational`

  ```k
    rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
  ```

- Line 72; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
  ```

- Line 73; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
          => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
  ```

- Line 77; kind `rule`; tags `operational`

  ```k
    rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
  ```

- Line 78; kind `rule`; tags `operational`

  ```k
    rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
  ```

- Line 79; kind `rule`; tags `operational`

  ```k
    rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
         requires truthy(V)
  ```

- Line 81; kind `rule`; tags `operational`

  ```k
    rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
         requires notBool truthy(V)
  ```

- Line 85; kind `rule`; tags `operational`

  ```k
    rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
  ```

- Line 86; kind `rule`; tags `operational`

  ```k
    rule <k> Continue => #cont ... </k>
  ```

- Line 87; kind `rule`; tags `operational`

  ```k
    rule <k> Break => #brk ... </k>
  ```

- Line 88; kind `rule`; tags `operational`

  ```k
    rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
  ```

- Line 89; kind `rule`; tags `owise, operational`

  ```k
    rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
  ```

- Line 90; kind `rule`; tags `operational`

  ```k
    rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
  ```

- Line 91; kind `rule`; tags `owise, operational`

  ```k
    rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
  ```

- Line 95; kind `rule`; tags `priority, operational`

  ```k
    rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 98; kind `rule`; tags `priority, operational`

  ```k
    rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 101; kind `rule`; tags `priority, operational`

  ```k
    rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 106; kind `rule`; tags `priority, operational`

  ```k
    rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 109; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/core.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-CORE
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-SYNTAX
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports INT
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports BOOL
  ```

- Line 7; kind `imports`; tags `none`

  ```k
    imports STRING
  ```

- Line 8; kind `imports`; tags `none`

  ```k
    imports MAP
  ```

- Line 9; kind `imports`; tags `none`

  ```k
    imports LIST
  ```

- Line 10; kind `imports`; tags `none`

  ```k
    imports K-EQUAL
  ```

- Line 13; kind `syntax`; tags `none`

  ```k
    syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  ```

- Line 14; kind `syntax`; tags `none`

  ```k
    syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
  ```

- Line 15; kind `syntax`; tags `none`

  ```k
    syntax Str    ::= str(IntSeq)
  ```

- Line 18; kind `syntax`; tags `none`

  ```k
    syntax Iterable ::= list(ValSeq)
                      | tuple(ValSeq)
                      | Str
                      | rangeObj(Int, Int, Int)
                      | zipObj(ValSeq, ValSeq)
                      | zipObjS(IntSeq, IntSeq)
  ```

- Line 25; kind `syntax`; tags `function`

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

- Line 36; kind `syntax`; tags `none`

  ```k
    syntax Parent   ::= "root" | parent(Int)
  ```

- Line 37; kind `syntax`; tags `none`

  ```k
    syntax Scope    ::= scope(Map, Parent)
  ```

- Line 38; kind `syntax`; tags `none`

  ```k
    syntax KResult  ::= Val
  ```

- Line 39; kind `syntax`; tags `none`

  ```k
    syntax Expr     ::= Val   // cooling puts results back into expression holes
  ```

- Line 40; kind `syntax`; tags `none`

  ```k
    syntax Vals     ::= List{Val, ","}
  ```

- Line 41; kind `syntax`; tags `none`

  ```k
    syntax Exc      ::= "NoExc" | "AssertionError"
  ```

- Line 42; kind `syntax`; tags `none`

  ```k
    syntax RetState ::= "noRet" | retV(Val)
  ```

- Line 49; kind `configuration`; tags `none`

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

- Line 68; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= isRefV(Val) [function, total]
  ```

- Line 69; kind `rule`; tags `equational`

  ```k
    rule isRefV(ref(_:Int)) => true
  ```

- Line 70; kind `rule`; tags `owise, equational`

  ```k
    rule isRefV(_:Val)      => false [owise]
  ```

- Line 75; kind `syntax`; tags `none`

  ```k
    syntax HeapVal ::= cellV(Val)
  ```

- Line 76; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= isCellRef(Val) [function, total]
  ```

- Line 77; kind `rule`; tags `equational`

  ```k
    rule isCellRef(cellRef(_:Int)) => true
  ```

- Line 78; kind `rule`; tags `owise, equational`

  ```k
    rule isCellRef(_:Val)          => false [owise]
  ```

- Line 85; kind `rule`; tags `priority, operational`

  ```k
    rule <k> cellRef(H:Int) => V ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         <heap> ... H |-> cellV(V:Val) ... </heap>
         requires "$cells" in_keys(M)
         [priority(40)]
  ```

- Line 95; kind `syntax`; tags `none`

  ```k
    syntax Val ::= kwV(String, Val)
  ```

- Line 96; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #kwTag(String)
  ```

- Line 97; kind `rule`; tags `operational`

  ```k
    rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
  ```

- Line 98; kind `rule`; tags `operational`

  ```k
    rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
         requires notBool isKwV(V)
  ```

- Line 100; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= isKwV(Val) [function, total]
  ```

- Line 101; kind `rule`; tags `equational`

  ```k
    rule isKwV(kwV(_:String, _:Val)) => true
  ```

- Line 102; kind `rule`; tags `owise, equational`

  ```k
    rule isKwV(_:Val)                => false [owise]
  ```

- Line 106; kind `syntax`; tags `none`

  ```k
    syntax Val ::= cellsMark(ParamNames)
  ```

- Line 107; kind `syntax`; tags `function`

  ```k
    syntax ParamNames ::= cellsOf(Val) [function]
  ```

- Line 108; kind `rule`; tags `equational`

  ```k
    rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
  ```

- Line 109; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= pnMember(String, ParamNames) [function, total]
  ```

- Line 110; kind `rule`; tags `equational`

  ```k
    rule pnMember(_:String, .ParamNames) => false
  ```

- Line 111; kind `rule`; tags `equational`

  ```k
    rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
  ```

- Line 113; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #cellW(Val, Val)
  ```

- Line 114; kind `rule`; tags `operational`

  ```k
    rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
         <heap> ... H |-> cellV(_:Val => V) ... </heap>
  ```

- Line 117; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #alloc(Val)
  ```

- Line 118; kind `rule`; tags `operational`

  ```k
    rule <k> #alloc(V:Val) => ref(N) ... </k>
         <heap>    H:Map => (N |-> V) H </heap>
         <heapLoc> N:Int => N +Int 1 </heapLoc>
         requires notBool N in_keys(H)
  ```

- Line 124; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #loadAll(Module)
  ```

- Line 125; kind `rule`; tags `operational`

  ```k
    rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
  ```

- Line 126; kind `rule`; tags `operational`

  ```k
    rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
  ```

- Line 127; kind `rule`; tags `operational`

  ```k
    rule <k> .Stmts => .K ... </k>
  ```

- Line 130; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #look(String, Int)
  ```

- Line 131; kind `rule`; tags `operational`

  ```k
    rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
  ```

- Line 132; kind `rule`; tags `operational`

  ```k
    rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
         <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
         requires X in_keys(M)
  ```

- Line 145; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #look(X:String, L:Int) => V ... </k>
         <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
         <heap> ... H |-> cellV(V:Val) ... </heap>
         requires X in_keys(M) andBool "$cells" in_keys(M)
          andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
          andBool {M[X]}:>Val ==K cellRef(H)
         [priority(40)]
  ```

- Line 152; kind `rule`; tags `operational`

  ```k
    rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
         <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
         requires notBool (X in_keys(M))
  ```

- Line 157; kind `syntax`; tags `function, total`

  ```k
    syntax Scope ::= "builtinsScope" [function, total]
  ```

- Line 158; kind `rule`; tags `equational`

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

- Line 185; kind `syntax`; tags `none`

  ```k
    syntax ApplyK ::= toCall(Val)
  ```

- Line 186; kind `syntax`; tags `none`

  ```k
    syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                    | #evalArgCont(Exprs, Vals, ApplyK)
                    | #applyK(ApplyK, Vals)
  ```

- Line 189; kind `rule`; tags `operational`

  ```k
    rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
  ```

- Line 190; kind `rule`; tags `operational`

  ```k
    rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
  ```

- Line 191; kind `rule`; tags `operational`

  ```k
    rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
  ```

- Line 194; kind `rule`; tags `operational`

  ```k
    rule <k> Int(I:Int)   => I ... </k>
  ```

- Line 195; kind `rule`; tags `operational`

  ```k
    rule <k> Bool(B:Bool) => B ... </k>
  ```

- Line 196; kind `rule`; tags `operational`

  ```k
    rule <k> NoneVal      => noneV ... </k>
  ```

- Line 199; kind `syntax`; tags `function`

  ```k
    syntax Bool ::= truthy(Val) [function]
  ```

- Line 200; kind `rule`; tags `equational`

  ```k
    rule truthy(B:Bool)          => B
  ```

- Line 201; kind `rule`; tags `equational`

  ```k
    rule truthy(noneV)           => false
  ```

- Line 202; kind `rule`; tags `equational`

  ```k
    rule truthy(I:Int)           => I =/=Int 0
  ```

- Line 203; kind `rule`; tags `equational`

  ```k
    rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
  ```

- Line 204; kind `rule`; tags `equational`

  ```k
    rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
  ```

- Line 205; kind `rule`; tags `equational`

  ```k
    rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
  ```

- Line 208; kind `syntax`; tags `function`

  ```k
    syntax Val  ::= applyUn(String, Val) [function]
  ```

- Line 209; kind `syntax`; tags `function`

  ```k
    syntax Val  ::= applyBin(String, Val, Val) [function]
  ```

- Line 210; kind `syntax`; tags `function`

  ```k
    syntax Bool ::= applyCmp(String, Val, Val) [function]
  ```

- Line 213; kind `syntax`; tags `function, total`

  ```k
    syntax Vals ::= appendVal(Vals, Val) [function, total]
  ```

- Line 214; kind `rule`; tags `equational`

  ```k
    rule appendVal(.Vals, V:Val)              => V , .Vals
  ```

- Line 215; kind `rule`; tags `equational`

  ```k
    rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
  ```

- Line 217; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= vals2valSeq(Vals) [function, total]
  ```

- Line 218; kind `rule`; tags `equational`

  ```k
    rule vals2valSeq(.Vals)            => .ValSeq
  ```

- Line 219; kind `rule`; tags `equational`

  ```k
    rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
  ```

- Line 223; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= vsLen(ValSeq) [function, total]
  ```

- Line 224; kind `rule`; tags `equational`

  ```k
    rule vsLen(.ValSeq)                => 0
  ```

- Line 225; kind `rule`; tags `equational`

  ```k
    rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
  ```

- Line 227; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= isLen(IntSeq) [function, total]
  ```

- Line 228; kind `rule`; tags `equational`

  ```k
    rule isLen(.IntSeq)                => 0
  ```

- Line 229; kind `rule`; tags `equational`

  ```k
    rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
  ```

- Line 233; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
  ```

- Line 234; kind `rule`; tags `equational`

  ```k
    rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
  ```

- Line 235; kind `rule`; tags `equational`

  ```k
    rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
  ```

- Line 236; kind `rule`; tags `equational`

  ```k
    rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
         requires I >Int 0
  ```

- Line 238; kind `rule`; tags `equational`

  ```k
    rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
         requires I <Int 0
  ```

- Line 240; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/dict.k`

- Line 13; kind `module`; tags `none`

  ```k
  module MPY-DICT
  ```

- Line 14; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 15; kind `imports`; tags `none`

  ```k
    imports MPY-ITER
  ```

- Line 16; kind `imports`; tags `none`

  ```k
    imports MPY-METHODS
  ```

- Line 17; kind `imports`; tags `none`

  ```k
    imports MPY-LIST
  ```

- Line 20; kind `syntax`; tags `none`

  ```k
    syntax Val ::= dictV(ValSeq, ValSeq)
  ```

- Line 23; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                   | #dictKey(Expr, Entries, ValSeq, ValSeq)
                   | #dictVal(Val, Entries, ValSeq, ValSeq)
  ```

- Line 26; kind `rule`; tags `operational`

  ```k
    rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
  ```

- Line 27; kind `rule`; tags `operational`

  ```k
    rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
  ```

- Line 28; kind `rule`; tags `operational`

  ```k
    rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
          => K ~> #dictKey(V, REST, KS, VS) ... </k>
  ```

- Line 30; kind `rule`; tags `operational`

  ```k
    rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
          => V ~> #dictVal(KV, REST, KS, VS) ... </k>
  ```

- Line 32; kind `rule`; tags `operational`

  ```k
    rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
          => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
  ```

- Line 37; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
  ```

- Line 38; kind `rule`; tags `equational`

  ```k
    rule dHasKey(.ValSeq, _:Val)                => false
  ```

- Line 39; kind `rule`; tags `equational`

  ```k
    rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
  ```

- Line 40; kind `rule`; tags `equational`

  ```k
    rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
  ```

- Line 43; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
  ```

- Line 44; kind `rule`; tags `equational`

  ```k
    rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
  ```

- Line 45; kind `rule`; tags `equational`

  ```k
    rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
  ```

- Line 49; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
  ```

- Line 50; kind `rule`; tags `equational`

  ```k
    rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
         requires A ==K K
  ```

- Line 52; kind `rule`; tags `equational`

  ```k
    rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
         requires notBool (A ==K K)
  ```

- Line 54; kind `rule`; tags `owise, equational`

  ```k
    rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
  ```

- Line 58; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
          => #alloc(list(KS)) ... </k>
         [priority(40)]
  ```

- Line 63; kind `rule`; tags `equational`

  ```k
    rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
  ```

- Line 64; kind `syntax`; tags `function`

  ```k
    syntax Val ::= applyIndexD(Val, Val) [function]
  ```

- Line 65; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
         [priority(45)]
  ```

- Line 70; kind `syntax`; tags `function`

  ```k
    syntax Val ::= dictSet(Val, Val, Val) [function]
  ```

- Line 71; kind `rule`; tags `equational`

  ```k
    rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
  ```

- Line 76; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #dsetK(String, Val)
  ```

- Line 77; kind `rule`; tags `operational`

  ```k
    rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
  ```

- Line 78; kind `rule`; tags `operational`

  ```k
    rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
         requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
  ```

- Line 82; kind `rule`; tags `operational`

  ```k
    rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires X in_keys(M) andBool isRefV({M[X]}:>Val)
  ```

- Line 86; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #dsetV(Val, Val, Val)
  ```

- Line 87; kind `rule`; tags `operational`

  ```k
    rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
         <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  ```

- Line 90; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= normIdxD(Int, Int) [function, total]
  ```

- Line 91; kind `rule`; tags `equational`

  ```k
    rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
  ```

- Line 92; kind `rule`; tags `equational`

  ```k
    rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
  ```

- Line 95; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
      => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
  ```

- Line 97; kind `syntax`; tags `function`

  ```k
    syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
  ```

- Line 98; kind `rule`; tags `equational`

  ```k
    rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
  ```

- Line 99; kind `rule`; tags `equational`

  ```k
    rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
      => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
  ```

- Line 101; kind `syntax`; tags `function`

  ```k
    syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
  ```

- Line 102; kind `rule`; tags `equational`

  ```k
    rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
  ```

- Line 103; kind `rule`; tags `equational`

  ```k
    rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
  ```

- Line 104; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/float.k`

- Line 14; kind `module`; tags `none`

  ```k
  module MPY-FLOAT
  ```

- Line 15; kind `imports`; tags `none`

  ```k
    imports MPY-OPERATORS
  ```

- Line 16; kind `imports`; tags `none`

  ```k
    imports MPY-BUILTINS
  ```

- Line 17; kind `imports`; tags `none`

  ```k
    imports FLOAT
  ```

- Line 20; kind `syntax`; tags `none`

  ```k
    syntax Val ::= Float
  ```

- Line 21; kind `rule`; tags `operational`

  ```k
    rule <k> Float(F:Float) => F ... </k>
  ```

- Line 24; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
  ```

- Line 25; kind `rule`; tags `concrete, equational`

  ```k
    rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
  ```

- Line 27; kind `rule`; tags `equational`

  ```k
    rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
  ```

- Line 30; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
  ```

- Line 31; kind `rule`; tags `concrete, equational`

  ```k
    rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
  ```

- Line 32; kind `rule`; tags `equational`

  ```k
    rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
  ```

- Line 37; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
  ```

- Line 38; kind `rule`; tags `concrete, equational`

  ```k
    rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
  ```

- Line 39; kind `rule`; tags `equational`

  ```k
    rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
  ```

- Line 43; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
  ```

- Line 44; kind `rule`; tags `equational`

  ```k
    rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
  ```

- Line 50; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
  ```

- Line 51; kind `rule`; tags `concrete, equational`

  ```k
    rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
  ```

- Line 52; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
  ```

- Line 54; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
  ```

- Line 55; kind `rule`; tags `concrete, equational`

  ```k
    rule absF(F:Float) => absFloat(F) [concrete]
  ```

- Line 56; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
  ```

- Line 61; kind `rule`; tags `operational`

  ```k
    rule <k> Import(_:String) => .K ... </k>
  ```

- Line 65; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= "#mathCeil"
  ```

- Line 66; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
  ```

- Line 67; kind `rule`; tags `operational`

  ```k
    rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
  ```

- Line 70; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= "#mathFloor"
  ```

- Line 71; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
  ```

- Line 72; kind `rule`; tags `operational`

  ```k
    rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
  ```

- Line 73; kind `syntax`; tags `function, total, symbol`

  ```k
    syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
  ```

- Line 74; kind `rule`; tags `concrete, equational`

  ```k
    rule floorFI(I:Int)   => I                        [concrete]
  ```

- Line 75; kind `rule`; tags `concrete, equational`

  ```k
    rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
  ```

- Line 78; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
  ```

- Line 79; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
  ```

- Line 82; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
  ```

- Line 83; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
  ```

- Line 84; kind `rule`; tags `operational`

  ```k
    rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
  ```

- Line 85; kind `rule`; tags `operational`

  ```k
    rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
  ```

- Line 86; kind `syntax`; tags `function, total, symbol`

  ```k
    syntax Float ::= toF(Val) [function, total, symbol(toF)]
  ```

- Line 87; kind `rule`; tags `concrete, equational`

  ```k
    rule toF(F:Float) => F        [concrete]
  ```

- Line 88; kind `rule`; tags `concrete, equational`

  ```k
    rule toF(I:Int)   => intToF(I) [concrete]
  ```

- Line 93; kind `syntax`; tags `function, total, symbol`

  ```k
    syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
  ```

- Line 94; kind `rule`; tags `concrete, equational`

  ```k
    rule ceilF(I:Int)   => I                       [concrete]
  ```

- Line 95; kind `rule`; tags `concrete, equational`

  ```k
    rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
  ```

- Line 99; kind `rule`; tags `equational`

  ```k
    rule applyUn("-", F:Float) => 0.0 -Float F
  ```

- Line 103; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
  ```

- Line 104; kind `rule`; tags `concrete, equational`

  ```k
    rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
  ```

- Line 105; kind `rule`; tags `equational`

  ```k
    rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
  ```

- Line 107; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
  ```

- Line 108; kind `rule`; tags `concrete, equational`

  ```k
    rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
  ```

- Line 109; kind `rule`; tags `equational`

  ```k
    rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
  ```

- Line 111; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
  ```

- Line 112; kind `rule`; tags `concrete, equational`

  ```k
    rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
  ```

- Line 113; kind `rule`; tags `equational`

  ```k
    rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
  ```

- Line 115; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
  ```

- Line 116; kind `rule`; tags `concrete, equational`

  ```k
    rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
  ```

- Line 117; kind `rule`; tags `equational`

  ```k
    rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
  ```

- Line 119; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
  ```

- Line 120; kind `rule`; tags `concrete, equational`

  ```k
    rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
  ```

- Line 121; kind `rule`; tags `equational`

  ```k
    rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
  ```

- Line 125; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
  ```

- Line 126; kind `rule`; tags `concrete, equational`

  ```k
    rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
  ```

- Line 127; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
  ```

- Line 128; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
  ```

- Line 129; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
  ```

- Line 132; kind `rule`; tags `equational`

  ```k
    rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
  ```

- Line 133; kind `rule`; tags `equational`

  ```k
    rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
  ```

- Line 134; kind `rule`; tags `equational`

  ```k
    rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
  ```

- Line 135; kind `rule`; tags `equational`

  ```k
    rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
  ```

- Line 136; kind `rule`; tags `equational`

  ```k
    rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
  ```

- Line 137; kind `rule`; tags `equational`

  ```k
    rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
  ```

- Line 138; kind `rule`; tags `equational`

  ```k
    rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
  ```

- Line 139; kind `rule`; tags `equational`

  ```k
    rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
  ```

- Line 142; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
  ```

- Line 143; kind `rule`; tags `concrete, equational`

  ```k
    rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
  ```

- Line 144; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
  ```

- Line 145; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
  ```

- Line 146; kind `rule`; tags `equational`

  ```k
    rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
  ```

- Line 147; kind `rule`; tags `equational`

  ```k
    rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
  ```

- Line 148; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
  ```

- Line 149; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
  ```

- Line 150; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
  ```

- Line 151; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
  ```

- Line 154; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", V:Val, noneV) => V ==K noneV
  ```

- Line 155; kind `rule`; tags `equational`

  ```k
    rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
  ```

- Line 160; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
  ```

- Line 161; kind `rule`; tags `concrete, equational`

  ```k
    rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
  ```

- Line 162; kind `rule`; tags `concrete, equational`

  ```k
    rule decStrToF(CS:IntSeq)
      => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
         requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
  ```

- Line 165; kind `syntax`; tags `function`

  ```k
    syntax Int ::= headIS(IntSeq) [function]
  ```

- Line 166; kind `rule`; tags `equational`

  ```k
    rule headIS(iCons(C:Int, _:IntSeq)) => C
  ```

- Line 167; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
  ```

- Line 168; kind `rule`; tags `equational`

  ```k
    rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
  ```

- Line 169; kind `rule`; tags `equational`

  ```k
    rule intPartAcc(.IntSeq, A:Int) => A
  ```

- Line 170; kind `rule`; tags `equational`

  ```k
    rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
  ```

- Line 171; kind `rule`; tags `equational`

  ```k
    rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
         requires C =/=Int 46
  ```

- Line 173; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
  ```

- Line 174; kind `rule`; tags `equational`

  ```k
    rule fracPart(.IntSeq) => 0
  ```

- Line 175; kind `rule`; tags `equational`

  ```k
    rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
  ```

- Line 176; kind `rule`; tags `equational`

  ```k
    rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
  ```

- Line 177; kind `rule`; tags `equational`

  ```k
    rule fracAcc(.IntSeq, A:Int) => A
  ```

- Line 178; kind `rule`; tags `equational`

  ```k
    rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
  ```

- Line 179; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
  ```

- Line 180; kind `rule`; tags `equational`

  ```k
    rule fracScale(.IntSeq) => 1
  ```

- Line 181; kind `rule`; tags `equational`

  ```k
    rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
  ```

- Line 182; kind `rule`; tags `equational`

  ```k
    rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
  ```

- Line 183; kind `rule`; tags `equational`

  ```k
    rule fscAcc(.IntSeq, A:Int) => A
  ```

- Line 184; kind `rule`; tags `equational`

  ```k
    rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
  ```

- Line 185; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
  ```

- Line 186; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
  ```

- Line 187; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("float", F:Float, .Vals)        => F
  ```

- Line 190; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
  ```

- Line 191; kind `rule`; tags `concrete, equational`

  ```k
    rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
  ```

- Line 192; kind `rule`; tags `equational`

  ```k
    rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
  ```

- Line 195; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
  ```

- Line 196; kind `rule`; tags `concrete, equational`

  ```k
    rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
  ```

- Line 197; kind `rule`; tags `equational`

  ```k
    rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
  ```

- Line 198; kind `rule`; tags `equational`

  ```k
    rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
  ```

- Line 199; kind `rule`; tags `equational`

  ```k
    rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
  ```

- Line 200; kind `rule`; tags `equational`

  ```k
    rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
  ```

- Line 201; kind `rule`; tags `equational`

  ```k
    rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
  ```

- Line 202; kind `rule`; tags `equational`

  ```k
    rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
  ```

- Line 203; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
  ```

- Line 204; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
  ```

- Line 205; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
  ```

- Line 206; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
  ```

- Line 209; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
  ```

- Line 210; kind `rule`; tags `concrete, equational`

  ```k
    rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
  ```

- Line 211; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
  ```

- Line 213; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
  ```

- Line 214; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("float", F:Float, .Vals) => F
  ```

- Line 217; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
  ```

- Line 218; kind `rule`; tags `concrete, equational`

  ```k
    rule roundF(F:Float)
      => #if (F -Float floorFloat(F)) ==Float 0.5
         #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
                #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
         #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
  ```

- Line 223; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
  ```

- Line 224; kind `rule`; tags `concrete, equational`

  ```k
    rule roundFN(F:Float, N:Int)
      => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
         /Float Int2Float(10 ^Int N, 53, 11) [concrete]
  ```

- Line 227; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
  ```

- Line 228; kind `rule`; tags `equational`

  ```k
    rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
  ```

- Line 230; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
  ```

- Line 231; kind `rule`; tags `concrete, equational`

  ```k
    rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
  ```

- Line 232; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= "#mathSqrt"
  ```

- Line 233; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
  ```

- Line 234; kind `rule`; tags `operational`

  ```k
    rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
  ```

- Line 235; kind `rule`; tags `operational`

  ```k
    rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
  ```

- Line 243; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
  ```

- Line 244; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
  ```

- Line 245; kind `rule`; tags `operational`

  ```k
    rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
  ```

- Line 246; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
  ```

- Line 247; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
         requires isFloat(V)
  ```

- Line 250; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
  ```

- Line 251; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
  ```

- Line 252; kind `rule`; tags `operational`

  ```k
    rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
  ```

- Line 253; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
  ```

- Line 254; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
         requires isFloat(V)
  ```

- Line 261; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
  ```

- Line 262; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
          => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
         requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
  ```

- Line 265; kind `rule`; tags `operational`

  ```k
    rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
  ```

- Line 266; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
  ```

- Line 267; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
          => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
         requires isFloat(V)
  ```

- Line 270; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
          => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
         requires isInt(V) orBool isBool(V)
  ```

- Line 273; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/functions.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-FUNCTIONS
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 8; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                   | #bindP(ParamNames, Vals)
                   | "#pop"
                   | "#endcall"
  ```

- Line 14; kind `rule`; tags `operational`

  ```k
    rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
  ```

- Line 18; kind `syntax`; tags `none`

  ```k
    syntax Expr ::= closureExpr(ParamNames, Stmts)
  ```

- Line 19; kind `rule`; tags `operational`

  ```k
    rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
         <env> L:Int </env>
  ```

- Line 27; kind `syntax`; tags `none`

  ```k
    syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
  ```

- Line 31; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                   | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
  ```

- Line 33; kind `rule`; tags `operational`

  ```k
    rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                     FreeVars(FVS:ParamNames), BODY:Stmts)
          => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
  ```

- Line 36; kind `rule`; tags `operational`

  ```k
    rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                        (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
          => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires FV in_keys(M)
  ```

- Line 42; kind `rule`; tags `operational`

  ```k
    rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                        .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
  ```

- Line 47; kind `rule`; tags `operational`

  ```k
    rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
          => closureVal(PNS, Return(E) .Stmts, L) ... </k>
         <env> L:Int </env>
  ```

- Line 50; kind `rule`; tags `operational`

  ```k
    rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                    FreeVars(FVS:ParamNames), E:Expr)
          => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
  ```

- Line 53; kind `rule`; tags `operational`

  ```k
    rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                       (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
          => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires FV in_keys(M)
  ```

- Line 59; kind `rule`; tags `operational`

  ```k
    rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
          => closureValC(PNS, CVS, BODY, CM) ... </k>
  ```

- Line 63; kind `rule`; tags `operational`

  ```k
    rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
  ```

- Line 64; kind `rule`; tags `operational`

  ```k
    rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  ```

- Line 68; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
          => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires "$cells" in_keys(M)
          andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
          andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
         [priority(40)]
  ```

- Line 78; kind `rule`; tags `operational`

  ```k
    rule <k> Return(V:Val) ~> _ => #pop </k>
         <ret> noRet => retV(V) </ret>
  ```

- Line 80; kind `rule`; tags `operational`

  ```k
    rule <k> #endcall => #pop ... </k>
         <ret> noRet => retV(noneV) </ret>
  ```

- Line 85; kind `rule`; tags `operational`

  ```k
    rule <k> #pop => V ~> CONT </k>
         <ret>   retV(V) => noRet </ret>
         <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
         <env>   L:Int => CALLERL </env>
         <scopes> SC:Map => SC [ L <- undef ] </scopes>
         <scopeLoc> _ => SAVEDL </scopeLoc>
  ```

- Line 91; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/int.k`

- Line 4; kind `module`; tags `none`

  ```k
  module MPY-INT
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 7; kind `rule`; tags `equational`

  ```k
    rule applyUn("-", I:Int) => 0 -Int I
  ```

- Line 9; kind `rule`; tags `equational`

  ```k
    rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  ```

- Line 11; kind `rule`; tags `equational`

  ```k
    rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
  ```

- Line 12; kind `rule`; tags `equational`

  ```k
    rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
  ```

- Line 13; kind `rule`; tags `equational`

  ```k
    rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
  ```

- Line 14; kind `rule`; tags `equational`

  ```k
    rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
  ```

- Line 15; kind `rule`; tags `equational`

  ```k
    rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
  ```

- Line 16; kind `rule`; tags `equational`

  ```k
    rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
  ```

- Line 17; kind `rule`; tags `equational`

  ```k
    rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
  ```

- Line 19; kind `syntax`; tags `function`

  ```k
    syntax Int ::= pyMod(Int, Int) [function]
  ```

- Line 20; kind `rule`; tags `equational`

  ```k
    rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
  ```

- Line 22; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
  ```

- Line 23; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
  ```

- Line 24; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
  ```

- Line 25; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
  ```

- Line 26; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
  ```

- Line 27; kind `rule`; tags `equational`

  ```k
    rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
  ```

- Line 28; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/iter.k`

- Line 6; kind `module`; tags `none`

  ```k
  module MPY-ITER
  ```

- Line 7; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 8; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
  ```

- Line 9; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/list.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-LIST
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports MPY-ITER
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports MPY-OPERATORS
  ```

- Line 9; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
  ```

- Line 10; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
  ```

- Line 13; kind `syntax`; tags `none`

  ```k
    syntax ApplyK ::= "toList"
  ```

- Line 14; kind `rule`; tags `operational`

  ```k
    rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
  ```

- Line 15; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
  ```

- Line 18; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
  ```

- Line 19; kind `rule`; tags `equational`

  ```k
    rule valSeqConcat(.ValSeq, T:ValSeq)                => T
  ```

- Line 20; kind `rule`; tags `equational`

  ```k
    rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
  ```

- Line 24; kind `rule`; tags `priority, operational`

  ```k
    rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
         [priority(45)]
  ```

- Line 27; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
  ```

- Line 28; kind `rule`; tags `equational`

  ```k
    rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
  ```

- Line 33; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= hasRefVS(ValSeq) [function, total]
  ```

- Line 34; kind `rule`; tags `equational`

  ```k
    rule hasRefVS(.ValSeq)                => false
  ```

- Line 35; kind `rule`; tags `equational`

  ```k
    rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
  ```

- Line 37; kind `syntax`; tags `function`

  ```k
    syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                  | deepEqV(Val, Val, Map)        [function]
  ```

- Line 39; kind `rule`; tags `equational`

  ```k
    rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
  ```

- Line 40; kind `rule`; tags `equational`

  ```k
    rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
  ```

- Line 41; kind `rule`; tags `equational`

  ```k
    rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
  ```

- Line 42; kind `rule`; tags `equational`

  ```k
    rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
      => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
  ```

- Line 45; kind `rule`; tags `equational`

  ```k
    rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
         requires H in_keys(HP)
  ```

- Line 47; kind `rule`; tags `equational`

  ```k
    rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
         requires notBool isRefV(A) andBool H in_keys(HP)
  ```

- Line 49; kind `rule`; tags `equational`

  ```k
    rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
  ```

- Line 50; kind `rule`; tags `owise, equational`

  ```k
    rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
  ```

- Line 53; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
         <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
         [priority(40)]
  ```

- Line 58; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
  ```

- Line 59; kind `rule`; tags `operational`

  ```k
    rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
  ```

- Line 60; kind `rule`; tags `operational`

  ```k
    rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
  ```

- Line 61; kind `rule`; tags `operational`

  ```k
    rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
  ```

- Line 62; kind `rule`; tags `operational`

  ```k
    rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
  ```

- Line 63; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
         requires E ==K V
  ```

- Line 65; kind `rule`; tags `operational`

  ```k
    rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
         requires notBool (E ==K V)
  ```

- Line 67; kind `rule`; tags `operational`

  ```k
    rule <k> B:Bool ~> #notB => notBool B ... </k>
  ```

- Line 68; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/methods.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-METHODS
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports K-EQUAL
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports MPY-STR
  ```

- Line 7; kind `imports`; tags `none`

  ```k
    imports MPY-LIST
  ```

- Line 10; kind `syntax`; tags `function`

  ```k
    syntax Val ::= applyMethod(Val, String, Vals) [function]
  ```

- Line 13; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
  ```

- Line 14; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
  ```

- Line 15; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
  ```

- Line 16; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
  ```

- Line 19; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
  ```

- Line 20; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
  ```

- Line 21; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
  ```

- Line 26; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
  ```

- Line 27; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
  ```

- Line 28; kind `rule`; tags `equational`

  ```k
    rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
  ```

- Line 29; kind `rule`; tags `equational`

  ```k
    rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
  ```

- Line 30; kind `rule`; tags `equational`

  ```k
    rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
      => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
  ```

- Line 34; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
  ```

- Line 35; kind `syntax`; tags `function`

  ```k
    syntax Int ::= cntSub(IntSeq, IntSeq) [function]
  ```

- Line 36; kind `rule`; tags `equational`

  ```k
    rule cntSub(.IntSeq, _:IntSeq) => 0
  ```

- Line 37; kind `rule`; tags `equational`

  ```k
    rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
         requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
  ```

- Line 39; kind `rule`; tags `equational`

  ```k
    rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
         requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
  ```

- Line 41; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
  ```

- Line 42; kind `rule`; tags `equational`

  ```k
    rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
  ```

- Line 43; kind `rule`; tags `owise, equational`

  ```k
    rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
  ```

- Line 44; kind `rule`; tags `equational`

  ```k
    rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
  ```

- Line 47; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
  ```

- Line 48; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= trimWS(IntSeq) [function, total]
  ```

- Line 49; kind `rule`; tags `equational`

  ```k
    rule trimWS(.IntSeq) => .IntSeq
  ```

- Line 50; kind `rule`; tags `equational`

  ```k
    rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
  ```

- Line 51; kind `rule`; tags `equational`

  ```k
    rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
  ```

- Line 52; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
  ```

- Line 53; kind `rule`; tags `equational`

  ```k
    rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
  ```

- Line 54; kind `rule`; tags `equational`

  ```k
    rule revISAcc(.IntSeq, A:IntSeq) => A
  ```

- Line 55; kind `rule`; tags `equational`

  ```k
    rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
  ```

- Line 58; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
  ```

- Line 61; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
  ```

- Line 64; kind `rule`; tags `equational`

  ```k
    rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
  ```

- Line 65; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
  ```

- Line 66; kind `rule`; tags `equational`

  ```k
    rule cntOccVS(.ValSeq, _:Val)                => 0
  ```

- Line 67; kind `rule`; tags `equational`

  ```k
    rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
  ```

- Line 68; kind `rule`; tags `equational`

  ```k
    rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
  ```

- Line 72; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
          => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
         [priority(40)]
  ```

- Line 75; kind `syntax`; tags `function`

  ```k
    syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
  ```

- Line 76; kind `rule`; tags `equational`

  ```k
    rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
  ```

- Line 77; kind `rule`; tags `equational`

  ```k
    rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
         requires isWSC(C)
  ```

- Line 79; kind `rule`; tags `equational`

  ```k
    rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
         requires notBool isWSC(C)
  ```

- Line 82; kind `syntax`; tags `function`

  ```k
    syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
  ```

- Line 83; kind `rule`; tags `equational`

  ```k
    rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
  ```

- Line 84; kind `rule`; tags `equational`

  ```k
    rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
  ```

- Line 85; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= isWSC(Int) [function, total]
  ```

- Line 86; kind `rule`; tags `equational`

  ```k
    rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
  ```

- Line 89; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
          => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
         [priority(39)]
  ```

- Line 94; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
          => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
         [priority(40)]
  ```

- Line 97; kind `syntax`; tags `function`

  ```k
    syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
  ```

- Line 98; kind `rule`; tags `equational`

  ```k
    rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
  ```

- Line 99; kind `rule`; tags `equational`

  ```k
    rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
         requires C ==Int SEP
  ```

- Line 101; kind `rule`; tags `equational`

  ```k
    rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
         requires notBool (C ==Int SEP)
  ```

- Line 104; kind `rule`; tags `equational`

  ```k
    rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
      => str(replaceC(CS, A, B))
  ```

- Line 106; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
  ```

- Line 107; kind `rule`; tags `equational`

  ```k
    rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
  ```

- Line 108; kind `rule`; tags `equational`

  ```k
    rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
  ```

- Line 109; kind `rule`; tags `equational`

  ```k
    rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
  ```

- Line 112; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= isUpperC(Int) [function, total]
  ```

- Line 113; kind `rule`; tags `equational`

  ```k
    rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
  ```

- Line 115; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= isLowerC(Int) [function, total]
  ```

- Line 116; kind `rule`; tags `equational`

  ```k
    rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
  ```

- Line 118; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= isAlphaC(Int) [function, total]
  ```

- Line 119; kind `rule`; tags `equational`

  ```k
    rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
  ```

- Line 121; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= isDigitC(Int) [function, total]
  ```

- Line 122; kind `rule`; tags `equational`

  ```k
    rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
  ```

- Line 124; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= hasUpper(IntSeq) [function, total]
  ```

- Line 125; kind `rule`; tags `equational`

  ```k
    rule hasUpper(.IntSeq) => false
  ```

- Line 126; kind `rule`; tags `equational`

  ```k
    rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
  ```

- Line 128; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= hasLower(IntSeq) [function, total]
  ```

- Line 129; kind `rule`; tags `equational`

  ```k
    rule hasLower(.IntSeq) => false
  ```

- Line 130; kind `rule`; tags `equational`

  ```k
    rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
  ```

- Line 132; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= allAlpha(IntSeq) [function, total]
  ```

- Line 133; kind `rule`; tags `equational`

  ```k
    rule allAlpha(.IntSeq) => true
  ```

- Line 134; kind `rule`; tags `equational`

  ```k
    rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
  ```

- Line 136; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= allDigit(IntSeq) [function, total]
  ```

- Line 137; kind `rule`; tags `equational`

  ```k
    rule allDigit(.IntSeq) => true
  ```

- Line 138; kind `rule`; tags `equational`

  ```k
    rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
  ```

- Line 140; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= lowerC(Int) [function, total]
  ```

- Line 142; kind `rule`; tags `equational`

  ```k
    rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
  ```

- Line 143; kind `rule`; tags `owise, equational`

  ```k
    rule lowerC(C:Int) => C         [owise]
  ```

- Line 145; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= upperC(Int) [function, total]
  ```

- Line 146; kind `rule`; tags `equational`

  ```k
    rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
  ```

- Line 147; kind `rule`; tags `owise, equational`

  ```k
    rule upperC(C:Int) => C         [owise]
  ```

- Line 149; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= swapC(Int) [function, total]
  ```

- Line 150; kind `rule`; tags `equational`

  ```k
    rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
  ```

- Line 151; kind `rule`; tags `equational`

  ```k
    rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
  ```

- Line 152; kind `rule`; tags `owise, equational`

  ```k
    rule swapC(C:Int) => C         [owise]
  ```

- Line 154; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= mapLower(IntSeq) [function, total]
  ```

- Line 155; kind `rule`; tags `equational`

  ```k
    rule mapLower(.IntSeq) => .IntSeq
  ```

- Line 156; kind `rule`; tags `equational`

  ```k
    rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
  ```

- Line 158; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= mapUpper(IntSeq) [function, total]
  ```

- Line 159; kind `rule`; tags `equational`

  ```k
    rule mapUpper(.IntSeq) => .IntSeq
  ```

- Line 160; kind `rule`; tags `equational`

  ```k
    rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
  ```

- Line 162; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= mapSwap(IntSeq) [function, total]
  ```

- Line 163; kind `rule`; tags `equational`

  ```k
    rule mapSwap(.IntSeq) => .IntSeq
  ```

- Line 164; kind `rule`; tags `equational`

  ```k
    rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
  ```

- Line 166; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
  ```

- Line 167; kind `rule`; tags `equational`

  ```k
    rule startsWith(.IntSeq, _:IntSeq)               => true
  ```

- Line 168; kind `rule`; tags `equational`

  ```k
    rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
  ```

- Line 169; kind `rule`; tags `equational`

  ```k
    rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
  ```

- Line 170; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/operators.k`

- Line 6; kind `module`; tags `none`

  ```k
  module MPY-OPERATORS
  ```

- Line 7; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 8; kind `imports`; tags `none`

  ```k
    imports MPY-ITER
  ```

- Line 10; kind `rule`; tags `operational`

  ```k
    rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
  ```

- Line 12; kind `rule`; tags `operational`

  ```k
    rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
  ```

- Line 15; kind `context`; tags `none`

  ```k
    context Compare(HOLE, _)
  ```

- Line 16; kind `context`; tags `none`

  ```k
    context Compare(_:Val, CmpOp(_, HOLE))
  ```

- Line 17; kind `rule`; tags `owise, operational`

  ```k
    rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
  ```

- Line 19; kind `rule`; tags `equational`

  ```k
    rule applyCmp("is",     V:Val, noneV) => V ==K noneV
  ```

- Line 20; kind `rule`; tags `equational`

  ```k
    rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
  ```

- Line 25; kind `rule`; tags `priority, operational`

  ```k
    rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 28; kind `rule`; tags `priority, operational`

  ```k
    rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isRefV(L)
         [priority(40)]
  ```

- Line 34; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires OP =/=String "in" andBool OP =/=String "not in"
         [priority(40)]
  ```

- Line 38; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         requires notBool isRefV(L)
          orBool OP ==String "in" orBool OP ==String "not in"
         [priority(40)]
  ```

- Line 44; kind `rule`; tags `priority, operational`

  ```k
    rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 47; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/range.k`

- Line 5; kind `module`; tags `none`

  ```k
  module MPY-RANGE
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 7; kind `imports`; tags `none`

  ```k
    imports MPY-ITER
  ```

- Line 9; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= inRange(Int, Int, Int) [function, total]
  ```

- Line 10; kind `rule`; tags `equational`

  ```k
    rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
  ```

- Line 12; kind `syntax`; tags `function`

  ```k
    syntax Int ::= rangeLen(Int, Int, Int) [function]
  ```

- Line 13; kind `rule`; tags `equational`

  ```k
    rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
         requires ST >Int 0 andBool HI >Int LO
  ```

- Line 15; kind `rule`; tags `equational`

  ```k
    rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
         requires ST <Int 0 andBool HI <Int LO
  ```

- Line 17; kind `rule`; tags `equational`

  ```k
    rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
         requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
  ```

- Line 20; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
          => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
         requires inRange(I, HI, ST)
  ```

- Line 23; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
         requires notBool inRange(I, HI, ST)
  ```

- Line 25; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/set.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-SET
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 8; kind `syntax`; tags `none`

  ```k
    syntax Val ::= setV(IntSeq)
  ```

- Line 11; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= codeIn(Int, IntSeq) [function, total]
  ```

- Line 12; kind `rule`; tags `equational`

  ```k
    rule codeIn(_:Int, .IntSeq)                => false
  ```

- Line 13; kind `rule`; tags `equational`

  ```k
    rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
  ```

- Line 16; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                    | dedupFrom(IntSeq, IntSeq)  [function, total]
  ```

- Line 18; kind `rule`; tags `equational`

  ```k
    rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
  ```

- Line 19; kind `rule`; tags `equational`

  ```k
    rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
  ```

- Line 20; kind `rule`; tags `equational`

  ```k
    rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
         requires codeIn(C, ACC)
  ```

- Line 22; kind `rule`; tags `equational`

  ```k
    rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
         requires notBool codeIn(C, ACC)
  ```

- Line 25; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
  ```

- Line 26; kind `rule`; tags `equational`

  ```k
    rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
  ```

- Line 27; kind `rule`; tags `equational`

  ```k
    rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
  ```

- Line 31; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
  ```

- Line 32; kind `rule`; tags `equational`

  ```k
    rule subsetCodes(.IntSeq, _:IntSeq)                => true
  ```

- Line 33; kind `rule`; tags `equational`

  ```k
    rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
  ```

- Line 35; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
  ```

- Line 36; kind `rule`; tags `equational`

  ```k
    rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
  ```

- Line 39; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
  ```

- Line 40; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/sort.k`

- Line 10; kind `module`; tags `none`

  ```k
  module MPY-SORT
  ```

- Line 11; kind `imports`; tags `none`

  ```k
    imports MPY-BUILTINS
  ```

- Line 12; kind `imports`; tags `none`

  ```k
    imports MPY-SUBSCRIPT
  ```

- Line 18; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
  ```

- Line 19; kind `syntax`; tags `function`

  ```k
    syntax ValSeq ::= insVS(Int, ValSeq) [function]
  ```

- Line 20; kind `rule`; tags `concrete, equational`

  ```k
    rule sortVS(.ValSeq)                => .ValSeq          [concrete]
  ```

- Line 21; kind `rule`; tags `concrete, equational`

  ```k
    rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
  ```

- Line 22; kind `rule`; tags `concrete, equational`

  ```k
    rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
  ```

- Line 23; kind `rule`; tags `concrete, equational`

  ```k
    rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
  ```

- Line 24; kind `rule`; tags `concrete, equational`

  ```k
    rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  ```

- Line 26; kind `syntax`; tags `function`

  ```k
    syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
  ```

- Line 27; kind `rule`; tags `concrete, equational`

  ```k
    rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
  ```

- Line 28; kind `rule`; tags `concrete, equational`

  ```k
    rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
  ```

- Line 29; kind `rule`; tags `concrete, equational`

  ```k
    rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
         requires strLt(A, B) orBool A ==K B [concrete]
  ```

- Line 31; kind `rule`; tags `concrete, equational`

  ```k
    rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
         requires notBool (strLt(A, B) orBool A ==K B) [concrete]
  ```

- Line 36; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
          => #alloc(list(sortVS(VS))) ... </k>
  ```

- Line 40; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
         <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
         [priority(40)]
  ```

- Line 49; kind `syntax`; tags `function, total, no-evaluators, symbol, opaque`

  ```k
    syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
  ```

- Line 51; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= revVS(ValSeq) [function, total]
                    | revVSAcc(ValSeq, ValSeq) [function, total]
  ```

- Line 53; kind `rule`; tags `equational`

  ```k
    rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
  ```

- Line 54; kind `rule`; tags `equational`

  ```k
    rule revVSAcc(.ValSeq, A:ValSeq) => A
  ```

- Line 55; kind `rule`; tags `equational`

  ```k
    rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
  ```

- Line 57; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
  ```

- Line 58; kind `rule`; tags `equational`

  ```k
    rule condRev(S:ValSeq, false) => S
  ```

- Line 59; kind `rule`; tags `equational`

  ```k
    rule condRev(S:ValSeq, true)  => revVS(S)
  ```

- Line 61; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
          => #alloc(list(sortKeyVS(VS, KV))) ... </k>
  ```

- Line 63; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
          => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
  ```

- Line 65; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
          => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
  ```

- Line 72; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/str.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-STR
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports MPY-ITER
  ```

- Line 8; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
  ```

- Line 9; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
          => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
  ```

- Line 13; kind `syntax`; tags `function`

  ```k
    syntax IntSeq ::= strToCodes(String) [function]
  ```

- Line 14; kind `rule`; tags `operational`

  ```k
    rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
  ```

- Line 15; kind `rule`; tags `equational`

  ```k
    rule strToCodes("") => .IntSeq
  ```

- Line 16; kind `rule`; tags `equational`

  ```k
    rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
      requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
  ```

- Line 20; kind `syntax`; tags `function, total`

  ```k
    syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
  ```

- Line 21; kind `rule`; tags `equational`

  ```k
    rule seqConcat(.IntSeq, T:IntSeq)                => T
  ```

- Line 22; kind `rule`; tags `equational`

  ```k
    rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
  ```

- Line 24; kind `rule`; tags `equational`

  ```k
    rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
  ```

- Line 25; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
  ```

- Line 26; kind `rule`; tags `equational`

  ```k
    rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
  ```

- Line 29; kind `rule`; tags `equational`

  ```k
    rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
  ```

- Line 30; kind `rule`; tags `equational`

  ```k
    rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
  ```

- Line 32; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
  ```

- Line 33; kind `rule`; tags `equational`

  ```k
    rule strPrefix(.IntSeq, _:IntSeq)               => true
  ```

- Line 34; kind `rule`; tags `equational`

  ```k
    rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
  ```

- Line 35; kind `rule`; tags `equational`

  ```k
    rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
  ```

- Line 37; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
  ```

- Line 38; kind `rule`; tags `equational`

  ```k
    rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
  ```

- Line 39; kind `rule`; tags `equational`

  ```k
    rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
  ```

- Line 40; kind `rule`; tags `equational`

  ```k
    rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
         requires notBool strPrefix(P, iCons(C, Xs))
  ```

- Line 48; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
  ```

- Line 49; kind `rule`; tags `equational`

  ```k
    rule strLt(.IntSeq, .IntSeq)                => false
  ```

- Line 50; kind `rule`; tags `equational`

  ```k
    rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
  ```

- Line 51; kind `rule`; tags `equational`

  ```k
    rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
  ```

- Line 52; kind `rule`; tags `equational`

  ```k
    rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
  ```

- Line 53; kind `rule`; tags `equational`

  ```k
    rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
  ```

- Line 54; kind `rule`; tags `equational`

  ```k
    rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
  ```

- Line 56; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
  ```

- Line 57; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
  ```

- Line 58; kind `rule`; tags `equational`

  ```k
    rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
  ```

- Line 59; kind `rule`; tags `equational`

  ```k
    rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
  ```

- Line 60; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/subscript.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-SUBSCRIPT
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 11; kind `syntax`; tags `function, total`

  ```k
    syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
  ```

- Line 12; kind `rule`; tags `equational`

  ```k
    rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
  ```

- Line 13; kind `rule`; tags `equational`

  ```k
    rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
         requires I >Int 0
  ```

- Line 16; kind `syntax`; tags `function`

  ```k
    syntax Int ::= intSeqAt(IntSeq, Int) [function]
  ```

- Line 17; kind `rule`; tags `equational`

  ```k
    rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
  ```

- Line 18; kind `rule`; tags `equational`

  ```k
    rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
         requires I >Int 0
  ```

- Line 21; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= normIdx(Int, Int) [function, total]
  ```

- Line 22; kind `rule`; tags `equational`

  ```k
    rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
  ```

- Line 23; kind `rule`; tags `equational`

  ```k
    rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
  ```

- Line 27; kind `context`; tags `none`

  ```k
    context Subscript(HOLE, _)
  ```

- Line 28; kind `context`; tags `none`

  ```k
    context Subscript(_:Val, HOLE:Expr)
  ```

- Line 31; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 35; kind `rule`; tags `operational`

  ```k
    rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
  ```

- Line 37; kind `syntax`; tags `function`

  ```k
    syntax Val ::= applyIndex(Val, Int) [function]
  ```

- Line 38; kind `rule`; tags `equational`

  ```k
    rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
  ```

- Line 39; kind `rule`; tags `equational`

  ```k
    rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
  ```

- Line 40; kind `rule`; tags `equational`

  ```k
    rule applyIndex(str(IS:IntSeq),   I:Int)
      => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
  ```

- Line 44; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #evalB(Bound) | "#toSome"
                   | #slLo(Val, Bound, Bound)
                   | #slHi(Val, OptInt, Bound)
                   | #slStep(Val, OptInt, OptInt)
  ```

- Line 49; kind `syntax`; tags `none`

  ```k
    syntax OptInt ::= "noB" | someB(Int)
  ```

- Line 50; kind `rule`; tags `operational`

  ```k
    rule <k> #evalB(NoBound)  => noB ... </k>
  ```

- Line 51; kind `rule`; tags `operational`

  ```k
    rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
  ```

- Line 52; kind `rule`; tags `operational`

  ```k
    rule <k> I:Int ~> #toSome => someB(I) ... </k>
  ```

- Line 54; kind `rule`; tags `operational`

  ```k
    rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
  ```

- Line 55; kind `rule`; tags `operational`

  ```k
    rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
  ```

- Line 56; kind `rule`; tags `operational`

  ```k
    rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  ```

- Line 58; kind `rule`; tags `priority, operational`

  ```k
    rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
          => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
         [priority(45)]
  ```

- Line 61; kind `rule`; tags `operational`

  ```k
    rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
  ```

- Line 63; kind `syntax`; tags `function`

  ```k
    syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
  ```

- Line 64; kind `rule`; tags `equational`

  ```k
    rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
      => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
  ```

- Line 66; kind `rule`; tags `equational`

  ```k
    rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
      => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
  ```

- Line 68; kind `rule`; tags `equational`

  ```k
    rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
      => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
  ```

- Line 72; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= slStep(OptInt) [function, total]
  ```

- Line 73; kind `rule`; tags `equational`

  ```k
    rule slStep(noB)          => 1
  ```

- Line 74; kind `rule`; tags `equational`

  ```k
    rule slStep(someB(S:Int)) => S
  ```

- Line 76; kind `syntax`; tags `function`

  ```k
    syntax Int ::= slStart(OptInt, OptInt, Int) [function]
  ```

- Line 77; kind `rule`; tags `equational`

  ```k
    rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
         requires slStep(ST) >Int 0
  ```

- Line 79; kind `rule`; tags `equational`

  ```k
    rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
         requires slStep(ST) <Int 0
  ```

- Line 81; kind `rule`; tags `equational`

  ```k
    rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
  ```

- Line 83; kind `syntax`; tags `function`

  ```k
    syntax Int ::= slStop(OptInt, OptInt, Int) [function]
  ```

- Line 84; kind `rule`; tags `equational`

  ```k
    rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
         requires slStep(ST) >Int 0
  ```

- Line 86; kind `rule`; tags `equational`

  ```k
    rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
         requires slStep(ST) <Int 0
  ```

- Line 88; kind `rule`; tags `equational`

  ```k
    rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
  ```

- Line 90; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= slAdjust(Int, Int, Int) [function, total]
  ```

- Line 91; kind `rule`; tags `equational`

  ```k
    rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
         requires I  <Int 0
  ```

- Line 93; kind `rule`; tags `equational`

  ```k
    rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
         requires I >=Int 0
  ```

- Line 96; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= clampLo(Int, Int) [function, total]
  ```

- Line 97; kind `rule`; tags `equational`

  ```k
    rule clampLo(J:Int, _STEP:Int) => J
         requires J >=Int 0
  ```

- Line 99; kind `rule`; tags `equational`

  ```k
    rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
         requires J <Int 0
  ```

- Line 102; kind `syntax`; tags `function, total`

  ```k
    syntax Int ::= clampHi(Int, Int, Int) [function, total]
  ```

- Line 103; kind `rule`; tags `equational`

  ```k
    rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
         requires I  <Int LEN
  ```

- Line 105; kind `rule`; tags `equational`

  ```k
    rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
         requires I >=Int LEN
  ```

- Line 109; kind `syntax`; tags `function`

  ```k
    syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
  ```

- Line 110; kind `rule`; tags `equational`

  ```k
    rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
      => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
         requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
  ```

- Line 113; kind `rule`; tags `equational`

  ```k
    rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
         requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
  ```

- Line 116; kind `syntax`; tags `function`

  ```k
    syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
  ```

- Line 117; kind `rule`; tags `equational`

  ```k
    rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
      => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
         requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
  ```

- Line 120; kind `rule`; tags `equational`

  ```k
    rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
         requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
  ```

- Line 122; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/syntax.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-SYNTAX
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports INT-SYNTAX
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports FLOAT-SYNTAX
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports BOOL-SYNTAX
  ```

- Line 7; kind `imports`; tags `none`

  ```k
    imports STRING-SYNTAX
  ```

- Line 9; kind `syntax`; tags `macro, strict, seqstrict`

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

- Line 32; kind `syntax`; tags `none`

  ```k
    syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
  ```

- Line 33; kind `syntax`; tags `none`

  ```k
    syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
  ```

- Line 34; kind `syntax`; tags `none`

  ```k
    syntax Entries  ::= List{Entry, ","}
  ```

- Line 35; kind `syntax`; tags `none`

  ```k
    syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
  ```

- Line 36; kind `syntax`; tags `none`

  ```k
    syntax CompFors ::= List{CompFor, ""}
  ```

- Line 37; kind `syntax`; tags `none`

  ```k
    syntax Exprs    ::= List{Expr, ","}
  ```

- Line 38; kind `syntax`; tags `none`

  ```k
    syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
  ```

- Line 39; kind `syntax`; tags `none`

  ```k
    syntax Bound    ::= Expr | "NoBound"
  ```

- Line 41; kind `syntax`; tags `strict`

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

- Line 56; kind `syntax`; tags `none`

  ```k
    syntax Stmts      ::= List{Stmt, ""}
  ```

- Line 57; kind `syntax`; tags `none`

  ```k
    syntax Params     ::= "Params" "(" ParamNames ")"
  ```

- Line 58; kind `syntax`; tags `none`

  ```k
    syntax CellVars   ::= "CellVars" "(" ParamNames ")"
  ```

- Line 59; kind `syntax`; tags `none`

  ```k
    syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
  ```

- Line 60; kind `syntax`; tags `none`

  ```k
    syntax ParamNames ::= List{String, ","}
  ```

- Line 61; kind `syntax`; tags `none`

  ```k
    syntax Module     ::= "Module" "(" Stmts ")"
  ```

- Line 62; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics/tuple.k`

- Line 3; kind `module`; tags `none`

  ```k
  module MPY-TUPLE
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 5; kind `imports`; tags `none`

  ```k
    imports MPY-ITER
  ```

- Line 6; kind `imports`; tags `none`

  ```k
    imports MPY-LIST
  ```

- Line 7; kind `imports`; tags `none`

  ```k
    imports MPY-METHODS
  ```

- Line 10; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
  ```

- Line 11; kind `rule`; tags `operational`

  ```k
    rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
  ```

- Line 14; kind `syntax`; tags `none`

  ```k
    syntax ApplyK ::= "toTuple"
  ```

- Line 15; kind `rule`; tags `operational`

  ```k
    rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
  ```

- Line 16; kind `rule`; tags `operational`

  ```k
    rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
  ```

- Line 18; kind `rule`; tags `equational`

  ```k
    rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  ```

- Line 20; kind `rule`; tags `operational`

  ```k
    rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
  ```

- Line 21; kind `rule`; tags `operational`

  ```k
    rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  ```

- Line 23; kind `rule`; tags `equational`

  ```k
    rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
  ```

- Line 24; kind `syntax`; tags `function`

  ```k
    syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
  ```

- Line 25; kind `rule`; tags `equational`

  ```k
    rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
  ```

- Line 26; kind `rule`; tags `equational`

  ```k
    rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
         requires notBool (A ==K V)
  ```

- Line 28; kind `rule`; tags `equational`

  ```k
    rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
  ```

- Line 31; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #bindTgt(Expr, Val)
  ```

- Line 32; kind `rule`; tags `operational`

  ```k
    rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
  ```

- Line 35; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
         <env> L:Int </env>
         <scopes> ... L |-> scope(M:Map, _) ... </scopes>
         requires "$cells" in_keys(M)
          andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
          andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
         [priority(40)]
  ```

- Line 42; kind `rule`; tags `operational`

  ```k
    rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
  ```

- Line 43; kind `rule`; tags `operational`

  ```k
    rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
  ```

- Line 44; kind `rule`; tags `priority, operational`

  ```k
    rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 49; kind `syntax`; tags `none`

  ```k
    syntax KItem ::= #unpackSeq(Exprs, ValSeq)
  ```

- Line 50; kind `rule`; tags `operational`

  ```k
    rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
  ```

- Line 51; kind `rule`; tags `operational`

  ```k
    rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
  ```

- Line 52; kind `rule`; tags `priority, operational`

  ```k
    rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
         <heap> ... H |-> V:Val ... </heap>
         [priority(40)]
  ```

- Line 55; kind `rule`; tags `operational`

  ```k
    rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
          => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
  ```

- Line 57; kind `rule`; tags `operational`

  ```k
    rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
  ```

- Line 58; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `reference-semantics/semantics.k`

- Line 34; kind `requires`; tags `none`

  ```k
  requires "semantics/syntax.k"
  ```

- Line 35; kind `requires`; tags `none`

  ```k
  requires "semantics/core.k"
  ```

- Line 36; kind `requires`; tags `none`

  ```k
  requires "semantics/iter.k"
  ```

- Line 37; kind `requires`; tags `none`

  ```k
  requires "semantics/range.k"
  ```

- Line 38; kind `requires`; tags `none`

  ```k
  requires "semantics/operators.k"
  ```

- Line 39; kind `requires`; tags `none`

  ```k
  requires "semantics/int.k"
  ```

- Line 40; kind `requires`; tags `none`

  ```k
  requires "semantics/bool.k"
  ```

- Line 41; kind `requires`; tags `none`

  ```k
  requires "semantics/float.k"
  ```

- Line 42; kind `requires`; tags `none`

  ```k
  requires "semantics/str.k"
  ```

- Line 43; kind `requires`; tags `none`

  ```k
  requires "semantics/set.k"
  ```

- Line 44; kind `requires`; tags `none`

  ```k
  requires "semantics/list.k"
  ```

- Line 45; kind `requires`; tags `none`

  ```k
  requires "semantics/tuple.k"
  ```

- Line 46; kind `requires`; tags `none`

  ```k
  requires "semantics/subscript.k"
  ```

- Line 47; kind `requires`; tags `none`

  ```k
  requires "semantics/comprehension.k"
  ```

- Line 48; kind `requires`; tags `none`

  ```k
  requires "semantics/methods.k"
  ```

- Line 49; kind `requires`; tags `none`

  ```k
  requires "semantics/controls.k"
  ```

- Line 50; kind `requires`; tags `none`

  ```k
  requires "semantics/functions.k"
  ```

- Line 51; kind `requires`; tags `none`

  ```k
  requires "semantics/builtins.k"
  ```

- Line 52; kind `requires`; tags `none`

  ```k
  requires "semantics/call.k"
  ```

- Line 53; kind `requires`; tags `none`

  ```k
  requires "semantics/sort.k"
  ```

- Line 54; kind `requires`; tags `none`

  ```k
  requires "semantics/assert.k"
  ```

- Line 55; kind `requires`; tags `none`

  ```k
  requires "semantics/dict.k"
  ```

- Line 56; kind `requires`; tags `concrete`

  ```k
  requires "semantics/concrete.k"
  ```

- Line 58; kind `module`; tags `none`

  ```k
  module MPY
  ```

- Line 59; kind `imports`; tags `none`

  ```k
    imports MPY-CORE
  ```

- Line 60; kind `imports`; tags `none`

  ```k
    imports MPY-ITER
  ```

- Line 61; kind `imports`; tags `none`

  ```k
    imports MPY-RANGE
  ```

- Line 62; kind `imports`; tags `none`

  ```k
    imports MPY-OPERATORS
  ```

- Line 63; kind `imports`; tags `none`

  ```k
    imports MPY-INT
  ```

- Line 64; kind `imports`; tags `none`

  ```k
    imports MPY-BOOL
  ```

- Line 65; kind `imports`; tags `none`

  ```k
    imports MPY-FLOAT
  ```

- Line 66; kind `imports`; tags `none`

  ```k
    imports MPY-STR
  ```

- Line 67; kind `imports`; tags `none`

  ```k
    imports MPY-SET
  ```

- Line 68; kind `imports`; tags `none`

  ```k
    imports MPY-LIST
  ```

- Line 69; kind `imports`; tags `none`

  ```k
    imports MPY-TUPLE
  ```

- Line 70; kind `imports`; tags `none`

  ```k
    imports MPY-SUBSCRIPT
  ```

- Line 71; kind `imports`; tags `none`

  ```k
    imports MPY-COMPREHENSION
  ```

- Line 72; kind `imports`; tags `none`

  ```k
    imports MPY-METHODS
  ```

- Line 73; kind `imports`; tags `none`

  ```k
    imports MPY-CONTROLS
  ```

- Line 74; kind `imports`; tags `none`

  ```k
    imports MPY-FUNCTIONS
  ```

- Line 75; kind `imports`; tags `none`

  ```k
    imports MPY-BUILTINS
  ```

- Line 76; kind `imports`; tags `none`

  ```k
    imports MPY-CALL
  ```

- Line 77; kind `imports`; tags `none`

  ```k
    imports MPY-SORT
  ```

- Line 78; kind `imports`; tags `none`

  ```k
    imports MPY-ASSERT
  ```

- Line 79; kind `imports`; tags `none`

  ```k
    imports MPY-DICT
  ```

- Line 80; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

- Line 87; kind `module`; tags `none`

  ```k
  module MPY-KRUN
  ```

- Line 88; kind `imports`; tags `none`

  ```k
    imports MPY
  ```

- Line 89; kind `imports`; tags `none`

  ```k
    imports MPY-CONCRETE
  ```

- Line 90; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `/candidate/verification.k`

- Line 1; kind `requires`; tags `none`

  ```k
  requires "reference-semantics/semantics.k"
  ```

- Line 3; kind `module`; tags `none`

  ```k
  module VERIFICATION
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports MPY
  ```

- Line 7; kind `syntax`; tags `function, total`

  ```k
    syntax Bool ::= allInts(ValSeq) [function, total]
  ```

- Line 8; kind `rule`; tags `equational`

  ```k
    rule allInts(.ValSeq)                => true
  ```

- Line 9; kind `rule`; tags `equational`

  ```k
    rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R)
  ```

- Line 13; kind `syntax`; tags `function, total`

  ```k
    syntax ValSeq ::= rdAcc(ValSeq, ValSeq, ValSeq) [function, total]
  ```

- Line 14; kind `rule`; tags `equational`

  ```k
    rule rdAcc(ACC:ValSeq, .ValSeq, _ALL:ValSeq) => ACC
  ```

- Line 15; kind `rule`; tags `equational`

  ```k
    rule rdAcc(ACC:ValSeq, vCons(V:Val, R:ValSeq), ALL:ValSeq)
      => #if 1 ==Int cntOccVS(ALL, V)
         #then rdAcc(valSeqConcat(ACC, vCons(V, .ValSeq)), R, ALL)
         #else rdAcc(ACC, R, ALL)
         #fi
  ```

- Line 20; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

### `/candidate/spec.k`

- Line 1; kind `requires`; tags `none`

  ```k
  requires "verification.k"
  ```

- Line 3; kind `module`; tags `none`

  ```k
  module SPEC
  ```

- Line 4; kind `imports`; tags `none`

  ```k
    imports VERIFICATION
  ```

- Line 6; kind `claim`; tags `none`

  ```k
    claim [remove-duplicates-loop]:
      <k>
        #loop(
          list(REST:ValSeq),
          Name("number"),
          If(
            Compare(
              Call(
                Attribute(Name("numbers"), "count"),
                (Name("number"), .Exprs)),
              CmpOp("==", Int(1))),
            Expr(
              Call(
                Attribute(Name("result"), "append"),
                (Name("number"), .Exprs))),
            .Stmts))
        => .K
        ...
      </k>
      <env> L:Int </env>
      <scopes>
        ...
        L |-> scope(
          "numbers" |-> list(ALL:ValSeq)
          "result"  |-> ref(H:Int)
          "number"  |-> (N:Val => ?N:Val),
          parent(0))
        ...
      </scopes>
      <heap>
        ...
        H |-> list(ACC:ValSeq => rdAcc(ACC, REST, ALL))
        ...
      </heap>
      requires allInts(REST) andBool allInts(ALL)
  ```

- Line 42; kind `claim`; tags `none`

  ```k
    claim [remove-duplicates]:
      <k>
        #loadAll(
          Module(
            ImportFrom("typing", "List")
            FuncDef(
              "remove_duplicates",
              Params("numbers"),
              Assign(Name("result"), ListExpr(.Exprs))
              Assign(Name("number"), Int(0))
              For(
                Name("number"),
                Name("numbers"),
                If(
                  Compare(
                    Call(
                      Attribute(Name("numbers"), "count"),
                      (Name("number"), .Exprs)),
                    CmpOp("==", Int(1))),
                  Expr(
                    Call(
                      Attribute(Name("result"), "append"),
                      (Name("number"), .Exprs))),
                  .Stmts))
              Return(Name("result")))))
        ~> Call(
             Name("remove_duplicates"),
             (list(INPUT:ValSeq), .Exprs))
        => ref(0)
      </k>
      <env> 0 </env>
      <scopes>
        0  |-> (scope(.Map, parent(-1))
                => scope(
                     "remove_duplicates" |->
                       closureVal(
                         ("numbers", .ParamNames),
                         Assign(Name("result"), ListExpr(.Exprs))
                         Assign(Name("number"), Int(0))
                         For(
                           Name("number"),
                           Name("numbers"),
                           If(
                             Compare(
                               Call(
                                 Attribute(Name("numbers"), "count"),
                                 (Name("number"), .Exprs)),
                               CmpOp("==", Int(1))),
                             Expr(
                               Call(
                                 Attribute(Name("result"), "append"),
                                 (Name("number"), .Exprs))),
                             .Stmts))
                         Return(Name("result")),
                         0),
                     parent(-1)))
        -1 |-> builtinsScope
      </scopes>
      <scopeLoc> 1 </scopeLoc>
      <heap>
        .Map => 0 |-> list(rdAcc(.ValSeq, INPUT, INPUT))
      </heap>
      <heapLoc> 0 => 1 </heapLoc>
      <stack> .List </stack>
      <ret> noRet </ret>
      <exc> NoExc </exc>
      <exit-code> 0 </exit-code>
      requires allInts(INPUT)
  ```

- Line 110; kind `endmodule`; tags `none`

  ```k
  endmodule
  ```

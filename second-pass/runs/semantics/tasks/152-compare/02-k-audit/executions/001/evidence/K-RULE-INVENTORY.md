# Exhaustive K declaration and rule inventory

Scope: the byte-verified supplied `reference-semantics/**/*.k`, `verification.k`, `spec.k`, and `operational-spec.k` in the clean scratch copy.

## `reference-semantics/semantics/assert.k`

SHA-256: `4258987a261d24b02ab3abfa52b3b2e013ea6323f9d5eb9a59c8f42cbcba030b`. Inventoried items: 3.

### reference-semantics/semantics/assert.k:6 — item 1 (`rule`, `rule/ordinary`)

```k
  rule <k> Assert(V:Val) => .K ... </k>
```

### reference-semantics/semantics/assert.k:8-10 — item 2 (`rule`, `rule/ordinary`)

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
```

### reference-semantics/semantics/assert.k:13-15 — item 3 (`rule`, `rule/priority`)

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/bool.k`

SHA-256: `8d6cfa9cd1ed776e51d776e4d358c418960c57715a6f9654ef9af41aea29f4fd`. Inventoried items: 14.

### reference-semantics/semantics/bool.k:8 — item 1 (`rule`, `rule/ordinary`)

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### reference-semantics/semantics/bool.k:10 — item 2 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### reference-semantics/semantics/bool.k:11 — item 3 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### reference-semantics/semantics/bool.k:16 — item 4 (`context`, `context`)

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### reference-semantics/semantics/bool.k:17 — item 5 (`rule`, `rule/ordinary`)

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### reference-semantics/semantics/bool.k:18 — item 6 (`rule`, `rule/ordinary`)

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
```

### reference-semantics/semantics/bool.k:20 — item 7 (`rule`, `rule/ordinary`)

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
```

### reference-semantics/semantics/bool.k:22 — item 8 (`rule`, `rule/ordinary`)

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
```

### reference-semantics/semantics/bool.k:24 — item 9 (`rule`, `rule/ordinary`)

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
```

### reference-semantics/semantics/bool.k:29-30 — item 10 (`rule`, `rule/priority`)

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/bool.k:31-32 — item 11 (`rule`, `rule/ordinary`)

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/bool.k:35-36 — item 12 (`rule`, `rule/ordinary`)

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/bool.k:39-40 — item 13 (`rule`, `rule/ordinary`)

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/bool.k:43-44 — item 14 (`rule`, `rule/ordinary`)

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

## `reference-semantics/semantics/builtins.k`

SHA-256: `fa43a855b8a4548f305f3dd210c8f6c6e7aa15b8d1cb0b8296977f061310c2dd`. Inventoried items: 175.

### reference-semantics/semantics/builtins.k:17 — item 1 (`syntax`, `syntax/function`)

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

### reference-semantics/semantics/builtins.k:20 — item 2 (`syntax`, `syntax/function`)

```k
  syntax Int ::= seqLen(Val) [function]
```

### reference-semantics/semantics/builtins.k:21 — item 3 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### reference-semantics/semantics/builtins.k:22 — item 4 (`rule`, `rule/ordinary`)

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### reference-semantics/semantics/builtins.k:23 — item 5 (`rule`, `rule/ordinary`)

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### reference-semantics/semantics/builtins.k:24 — item 6 (`rule`, `rule/ordinary`)

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### reference-semantics/semantics/builtins.k:25 — item 7 (`rule`, `rule/ordinary`)

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### reference-semantics/semantics/builtins.k:26 — item 8 (`rule`, `rule/ordinary`)

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### reference-semantics/semantics/builtins.k:32 — item 9 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### reference-semantics/semantics/builtins.k:33 — item 10 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### reference-semantics/semantics/builtins.k:34 — item 11 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### reference-semantics/semantics/builtins.k:35 — item 12 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### reference-semantics/semantics/builtins.k:36 — item 13 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:37 — item 14 (`rule`, `rule/ordinary`)

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### reference-semantics/semantics/builtins.k:38 — item 15 (`rule`, `rule/ordinary`)

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### reference-semantics/semantics/builtins.k:41 — item 16 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### reference-semantics/semantics/builtins.k:44 — item 17 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### reference-semantics/semantics/builtins.k:47 — item 18 (`syntax`, `syntax`)

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### reference-semantics/semantics/builtins.k:48 — item 19 (`rule`, `rule/ordinary`)

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### reference-semantics/semantics/builtins.k:49 — item 20 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### reference-semantics/semantics/builtins.k:50-51 — item 21 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
```

### reference-semantics/semantics/builtins.k:54 — item 22 (`syntax`, `syntax/function`)

```k
  syntax Int ::= intOf(Val) [function]
```

### reference-semantics/semantics/builtins.k:55 — item 23 (`rule`, `rule/ordinary`)

```k
  rule intOf(I:Int)  => I
```

### reference-semantics/semantics/builtins.k:56 — item 24 (`rule`, `rule/ordinary`)

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### reference-semantics/semantics/builtins.k:59 — item 25 (`syntax`, `syntax`)

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### reference-semantics/semantics/builtins.k:60 — item 26 (`rule`, `rule/ordinary`)

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### reference-semantics/semantics/builtins.k:61 — item 27 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### reference-semantics/semantics/builtins.k:62 — item 28 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
```

### reference-semantics/semantics/builtins.k:64 — item 29 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
```

### reference-semantics/semantics/builtins.k:67 — item 30 (`syntax`, `syntax`)

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### reference-semantics/semantics/builtins.k:68 — item 31 (`rule`, `rule/ordinary`)

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### reference-semantics/semantics/builtins.k:69 — item 32 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### reference-semantics/semantics/builtins.k:70 — item 33 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
```

### reference-semantics/semantics/builtins.k:72 — item 34 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
```

### reference-semantics/semantics/builtins.k:76 — item 35 (`syntax`, `syntax`)

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### reference-semantics/semantics/builtins.k:77 — item 36 (`rule`, `rule/ordinary`)

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### reference-semantics/semantics/builtins.k:78 — item 37 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
```

### reference-semantics/semantics/builtins.k:80 — item 38 (`rule`, `rule/ordinary`)

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### reference-semantics/semantics/builtins.k:81 — item 39 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### reference-semantics/semantics/builtins.k:82-83 — item 40 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
```

### reference-semantics/semantics/builtins.k:86 — item 41 (`syntax`, `syntax`)

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### reference-semantics/semantics/builtins.k:87 — item 42 (`rule`, `rule/ordinary`)

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### reference-semantics/semantics/builtins.k:88 — item 43 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
```

### reference-semantics/semantics/builtins.k:90 — item 44 (`rule`, `rule/ordinary`)

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### reference-semantics/semantics/builtins.k:91 — item 45 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### reference-semantics/semantics/builtins.k:92-93 — item 46 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
```

### reference-semantics/semantics/builtins.k:97 — item 47 (`syntax`, `syntax/function`)

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### reference-semantics/semantics/builtins.k:98 — item 48 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### reference-semantics/semantics/builtins.k:99 — item 49 (`rule`, `rule/ordinary`)

```k
  rule maxVals(M:Int, .Vals)           => M
```

### reference-semantics/semantics/builtins.k:100 — item 50 (`rule`, `rule/ordinary`)

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### reference-semantics/semantics/builtins.k:102 — item 51 (`syntax`, `syntax/function`)

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### reference-semantics/semantics/builtins.k:103 — item 52 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### reference-semantics/semantics/builtins.k:104 — item 53 (`rule`, `rule/ordinary`)

```k
  rule minVals(M:Int, .Vals)           => M
```

### reference-semantics/semantics/builtins.k:105 — item 54 (`rule`, `rule/ordinary`)

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### reference-semantics/semantics/builtins.k:108 — item 55 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
```

### reference-semantics/semantics/builtins.k:111-112 — item 56 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
```

### reference-semantics/semantics/builtins.k:114 — item 57 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### reference-semantics/semantics/builtins.k:115 — item 58 (`rule`, `rule/ordinary`)

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### reference-semantics/semantics/builtins.k:116 — item 59 (`rule`, `rule/ordinary`)

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### reference-semantics/semantics/builtins.k:117 — item 60 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:118 — item 61 (`rule`, `rule/ordinary`)

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### reference-semantics/semantics/builtins.k:119-120 — item 62 (`rule`, `rule/ordinary`)

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
```

### reference-semantics/semantics/builtins.k:124-125 — item 63 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### reference-semantics/semantics/builtins.k:126 — item 64 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:127 — item 65 (`rule`, `rule/ordinary`)

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### reference-semantics/semantics/builtins.k:128-129 — item 66 (`rule`, `rule/ordinary`)

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### reference-semantics/semantics/builtins.k:132-133 — item 67 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### reference-semantics/semantics/builtins.k:134 — item 68 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:135 — item 69 (`rule`, `rule/ordinary`)

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### reference-semantics/semantics/builtins.k:136 — item 70 (`rule`, `rule/ordinary`)

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### reference-semantics/semantics/builtins.k:137 — item 71 (`rule`, `rule/ordinary`)

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### reference-semantics/semantics/builtins.k:140 — item 72 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

### reference-semantics/semantics/builtins.k:143 — item 73 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### reference-semantics/semantics/builtins.k:144 — item 74 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
```

### reference-semantics/semantics/builtins.k:148 — item 75 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### reference-semantics/semantics/builtins.k:149 — item 76 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### reference-semantics/semantics/builtins.k:152 — item 77 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
```

### reference-semantics/semantics/builtins.k:156 — item 78 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
```

### reference-semantics/semantics/builtins.k:158 — item 79 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:159 — item 80 (`rule`, `rule/ordinary`)

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### reference-semantics/semantics/builtins.k:160 — item 81 (`rule`, `rule/ordinary`)

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### reference-semantics/semantics/builtins.k:163 — item 82 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### reference-semantics/semantics/builtins.k:164 — item 83 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### reference-semantics/semantics/builtins.k:167-168 — item 84 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### reference-semantics/semantics/builtins.k:169 — item 85 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:170 — item 86 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:171-172 — item 87 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### reference-semantics/semantics/builtins.k:173 — item 88 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:174 — item 89 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### reference-semantics/semantics/builtins.k:177 — item 90 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### reference-semantics/semantics/builtins.k:178 — item 91 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### reference-semantics/semantics/builtins.k:179 — item 92 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
```

### reference-semantics/semantics/builtins.k:187 — item 93 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### reference-semantics/semantics/builtins.k:188 — item 94 (`syntax`, `syntax/function`)

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### reference-semantics/semantics/builtins.k:189-190 — item 95 (`rule`, `rule/ordinary`)

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### reference-semantics/semantics/builtins.k:192 — item 96 (`syntax`, `syntax`)

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### reference-semantics/semantics/builtins.k:194 — item 97 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### reference-semantics/semantics/builtins.k:195 — item 98 (`rule`, `rule/ordinary`)

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### reference-semantics/semantics/builtins.k:196 — item 99 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:197 — item 100 (`rule`, `rule/ordinary`)

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### reference-semantics/semantics/builtins.k:198 — item 101 (`rule`, `rule/owise`)

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### reference-semantics/semantics/builtins.k:199 — item 102 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:200 — item 103 (`rule`, `rule/ordinary`)

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### reference-semantics/semantics/builtins.k:201 — item 104 (`rule`, `rule/owise`)

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### reference-semantics/semantics/builtins.k:203 — item 105 (`syntax`, `syntax/function,total`)

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:204 — item 106 (`rule`, `rule/ordinary`)

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### reference-semantics/semantics/builtins.k:205 — item 107 (`rule`, `rule/ordinary`)

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### reference-semantics/semantics/builtins.k:206 — item 108 (`rule`, `rule/ordinary`)

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### reference-semantics/semantics/builtins.k:207 — item 109 (`rule`, `rule/ordinary`)

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### reference-semantics/semantics/builtins.k:208 — item 110 (`rule`, `rule/ordinary`)

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### reference-semantics/semantics/builtins.k:209 — item 111 (`rule`, `rule/ordinary`)

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### reference-semantics/semantics/builtins.k:210 — item 112 (`rule`, `rule/ordinary`)

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### reference-semantics/semantics/builtins.k:211 — item 113 (`rule`, `rule/ordinary`)

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### reference-semantics/semantics/builtins.k:212 — item 114 (`rule`, `rule/ordinary`)

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### reference-semantics/semantics/builtins.k:214-215 — item 115 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:216 — item 116 (`rule`, `rule/ordinary`)

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### reference-semantics/semantics/builtins.k:217 — item 117 (`rule`, `rule/ordinary`)

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### reference-semantics/semantics/builtins.k:218 — item 118 (`rule`, `rule/ordinary`)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### reference-semantics/semantics/builtins.k:219 — item 119 (`rule`, `rule/ordinary`)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
```

### reference-semantics/semantics/builtins.k:221 — item 120 (`rule`, `rule/ordinary`)

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
```

### reference-semantics/semantics/builtins.k:223 — item 121 (`rule`, `rule/owise`)

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### reference-semantics/semantics/builtins.k:225 — item 122 (`syntax`, `syntax`)

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### reference-semantics/semantics/builtins.k:226 — item 123 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:227 — item 124 (`rule`, `rule/ordinary`)

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### reference-semantics/semantics/builtins.k:228 — item 125 (`rule`, `rule/owise`)

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### reference-semantics/semantics/builtins.k:230 — item 126 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:231 — item 127 (`rule`, `rule/ordinary`)

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### reference-semantics/semantics/builtins.k:232 — item 128 (`rule`, `rule/ordinary`)

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### reference-semantics/semantics/builtins.k:233 — item 129 (`rule`, `rule/ordinary`)

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### reference-semantics/semantics/builtins.k:234 — item 130 (`rule`, `rule/ordinary`)

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### reference-semantics/semantics/builtins.k:235 — item 131 (`rule`, `rule/ordinary`)

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### reference-semantics/semantics/builtins.k:236 — item 132 (`rule`, `rule/owise`)

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### reference-semantics/semantics/builtins.k:238 — item 133 (`syntax`, `syntax/function,total`)

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:239 — item 134 (`rule`, `rule/ordinary`)

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### reference-semantics/semantics/builtins.k:240 — item 135 (`rule`, `rule/ordinary`)

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### reference-semantics/semantics/builtins.k:241 — item 136 (`rule`, `rule/ordinary`)

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
```

### reference-semantics/semantics/builtins.k:243 — item 137 (`rule`, `rule/owise`)

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### reference-semantics/semantics/builtins.k:244 — item 138 (`syntax`, `syntax/function,total`)

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:245 — item 139 (`rule`, `rule/ordinary`)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### reference-semantics/semantics/builtins.k:246 — item 140 (`rule`, `rule/ordinary`)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### reference-semantics/semantics/builtins.k:247 — item 141 (`syntax`, `syntax/function,total`)

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:248 — item 142 (`rule`, `rule/ordinary`)

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### reference-semantics/semantics/builtins.k:250 — item 143 (`syntax`, `syntax/function,total`)

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### reference-semantics/semantics/builtins.k:251 — item 144 (`rule`, `rule/ordinary`)

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### reference-semantics/semantics/builtins.k:252 — item 145 (`rule`, `rule/ordinary`)

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### reference-semantics/semantics/builtins.k:253 — item 146 (`rule`, `rule/ordinary`)

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### reference-semantics/semantics/builtins.k:254 — item 147 (`rule`, `rule/ordinary`)

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### reference-semantics/semantics/builtins.k:255 — item 148 (`syntax`, `syntax/function,total`)

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/builtins.k:256 — item 149 (`rule`, `rule/ordinary`)

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### reference-semantics/semantics/builtins.k:257-258 — item 150 (`rule`, `rule/ordinary`)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
```

### reference-semantics/semantics/builtins.k:260-261 — item 151 (`rule`, `rule/ordinary`)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
```

### reference-semantics/semantics/builtins.k:263-264 — item 152 (`rule`, `rule/owise`)

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### reference-semantics/semantics/builtins.k:265 — item 153 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### reference-semantics/semantics/builtins.k:266 — item 154 (`rule`, `rule/ordinary`)

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### reference-semantics/semantics/builtins.k:267 — item 155 (`rule`, `rule/ordinary`)

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### reference-semantics/semantics/builtins.k:268 — item 156 (`rule`, `rule/owise`)

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### reference-semantics/semantics/builtins.k:269 — item 157 (`syntax`, `syntax/function,total`)

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### reference-semantics/semantics/builtins.k:270 — item 158 (`rule`, `rule/ordinary`)

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### reference-semantics/semantics/builtins.k:271 — item 159 (`rule`, `rule/ordinary`)

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### reference-semantics/semantics/builtins.k:272 — item 160 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/builtins.k:273 — item 161 (`rule`, `rule/ordinary`)

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### reference-semantics/semantics/builtins.k:274 — item 162 (`rule`, `rule/ordinary`)

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### reference-semantics/semantics/builtins.k:279 — item 163 (`syntax`, `syntax`)

```k
  syntax KItem ::= "#md5"
```

### reference-semantics/semantics/builtins.k:280-281 — item 164 (`rule`, `rule/priority`)

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### reference-semantics/semantics/builtins.k:282 — item 165 (`rule`, `rule/ordinary`)

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### reference-semantics/semantics/builtins.k:283 — item 166 (`syntax`, `syntax`)

```k
  syntax Val ::= md5Obj(IntSeq)
```

### reference-semantics/semantics/builtins.k:284 — item 167 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### reference-semantics/semantics/builtins.k:285 — item 168 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### reference-semantics/semantics/builtins.k:291 — item 169 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### reference-semantics/semantics/builtins.k:292 — item 170 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### reference-semantics/semantics/builtins.k:293 — item 171 (`syntax`, `syntax/function`)

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### reference-semantics/semantics/builtins.k:294 — item 172 (`rule`, `rule/ordinary`)

```k
  rule isIntV(_:Int)         => true
```

### reference-semantics/semantics/builtins.k:295 — item 173 (`rule`, `rule/owise`)

```k
  rule isIntV(_:Val)         => false [owise]
```

### reference-semantics/semantics/builtins.k:296 — item 174 (`rule`, `rule/ordinary`)

```k
  rule isStrV(str(_:IntSeq)) => true
```

### reference-semantics/semantics/builtins.k:297 — item 175 (`rule`, `rule/owise`)

```k
  rule isStrV(_:Val)         => false [owise]
```

## `reference-semantics/semantics/call.k`

SHA-256: `7e4d6c7cabe7bb4ccff52f21c5d5f30920ccb48d42864146ce53146509f736e4`. Inventoried items: 24.

### reference-semantics/semantics/call.k:16 — item 1 (`rule`, `rule/ordinary`)

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### reference-semantics/semantics/call.k:19 — item 2 (`syntax`, `syntax`)

```k
  syntax KItem ::= #callee(Exprs)
```

### reference-semantics/semantics/call.k:20 — item 3 (`rule`, `rule/owise`)

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### reference-semantics/semantics/call.k:21 — item 4 (`rule`, `rule/ordinary`)

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### reference-semantics/semantics/call.k:24 — item 5 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### reference-semantics/semantics/call.k:26 — item 6 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### reference-semantics/semantics/call.k:27 — item 7 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### reference-semantics/semantics/call.k:28 — item 8 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### reference-semantics/semantics/call.k:29 — item 9 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### reference-semantics/semantics/call.k:30 — item 10 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### reference-semantics/semantics/call.k:31 — item 11 (`rule`, `rule/owise`)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### reference-semantics/semantics/call.k:32 — item 12 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### reference-semantics/semantics/call.k:38-41 — item 13 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/call.k:42-44 — item 14 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/call.k:47-50 — item 15 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/call.k:52 — item 16 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### reference-semantics/semantics/call.k:53-55 — item 17 (`rule`, `rule/ordinary`)

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### reference-semantics/semantics/call.k:56-58 — item 18 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/call.k:63-65 — item 19 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/call.k:69-74 — item 20 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### reference-semantics/semantics/call.k:80-85 — item 21 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### reference-semantics/semantics/call.k:87 — item 22 (`syntax`, `syntax`)

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### reference-semantics/semantics/call.k:88 — item 23 (`rule`, `rule/ordinary`)

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### reference-semantics/semantics/call.k:89-93 — item 24 (`rule`, `rule/ordinary`)

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
```

## `reference-semantics/semantics/comprehension.k`

SHA-256: `cf7c38aad5cff698ebb05ecbadf00cbf210ddb2f54ae86f22b328311c027c6a7`. Inventoried items: 10.

### reference-semantics/semantics/comprehension.k:11 — item 1 (`rule`, `rule/ordinary`)

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### reference-semantics/semantics/comprehension.k:12 — item 2 (`rule`, `rule/ordinary`)

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### reference-semantics/semantics/comprehension.k:14 — item 3 (`syntax`, `syntax/macro`)

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### reference-semantics/semantics/comprehension.k:15-16 — item 4 (`rule`, `rule/ordinary`)

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### reference-semantics/semantics/comprehension.k:18 — item 5 (`syntax`, `syntax/macro-rec,macro`)

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### reference-semantics/semantics/comprehension.k:19-20 — item 6 (`rule`, `rule/ordinary`)

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### reference-semantics/semantics/comprehension.k:21-22 — item 7 (`rule`, `rule/ordinary`)

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### reference-semantics/semantics/comprehension.k:24 — item 8 (`syntax`, `syntax/macro`)

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### reference-semantics/semantics/comprehension.k:25 — item 9 (`rule`, `rule/ordinary`)

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### reference-semantics/semantics/comprehension.k:26 — item 10 (`rule`, `rule/ordinary`)

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## `reference-semantics/semantics/concrete.k`

SHA-256: `1ffea42a32610e9116506d709e9163413aeb5f6deb7824ea554aca8341f2d305`. Inventoried items: 21.

### reference-semantics/semantics/concrete.k:13-14 — item 1 (`rule`, `rule/ordinary`)

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
```

### reference-semantics/semantics/concrete.k:16-17 — item 2 (`rule`, `rule/ordinary`)

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
```

### reference-semantics/semantics/concrete.k:25 — item 3 (`syntax`, `syntax`)

```k
  syntax Val ::= kvP(Val, Val)
```

### reference-semantics/semantics/concrete.k:26-27 — item 4 (`syntax`, `syntax`)

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### reference-semantics/semantics/concrete.k:28-30 — item 5 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/concrete.k:31-33 — item 6 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/concrete.k:34-35 — item 7 (`rule`, `rule/ordinary`)

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### reference-semantics/semantics/concrete.k:36-37 — item 8 (`rule`, `rule/ordinary`)

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### reference-semantics/semantics/concrete.k:38-39 — item 9 (`rule`, `rule/ordinary`)

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
```

### reference-semantics/semantics/concrete.k:42 — item 10 (`syntax`, `syntax/function`)

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### reference-semantics/semantics/concrete.k:43 — item 11 (`rule`, `rule/ordinary`)

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### reference-semantics/semantics/concrete.k:44-45 — item 12 (`rule`, `rule/ordinary`)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
```

### reference-semantics/semantics/concrete.k:47-48 — item 13 (`rule`, `rule/ordinary`)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
```

### reference-semantics/semantics/concrete.k:51 — item 14 (`syntax`, `syntax/function`)

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### reference-semantics/semantics/concrete.k:52 — item 15 (`rule`, `rule/ordinary`)

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### reference-semantics/semantics/concrete.k:53 — item 16 (`rule`, `rule/ordinary`)

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### reference-semantics/semantics/concrete.k:54 — item 17 (`rule`, `rule/ordinary`)

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### reference-semantics/semantics/concrete.k:56 — item 18 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### reference-semantics/semantics/concrete.k:57 — item 19 (`rule`, `rule/ordinary`)

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### reference-semantics/semantics/concrete.k:58 — item 20 (`rule`, `rule/ordinary`)

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### reference-semantics/semantics/concrete.k:59 — item 21 (`rule`, `rule/owise`)

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## `reference-semantics/semantics/controls.k`

SHA-256: `325c73757d5a7ccf541b93240accd590a2cee90d84470efa3a4a0a14165aafae`. Inventoried items: 37.

### reference-semantics/semantics/controls.k:9-11 — item 1 (`rule`, `rule/ordinary`)

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### reference-semantics/semantics/controls.k:12-14 — item 2 (`rule`, `rule/ordinary`)

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/controls.k:20-22 — item 3 (`rule`, `rule/ordinary`)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
```

### reference-semantics/semantics/controls.k:27-29 — item 4 (`rule`, `rule/ordinary`)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/controls.k:35 — item 5 (`rule`, `rule/ordinary`)

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### reference-semantics/semantics/controls.k:36 — item 6 (`rule`, `rule/owise`)

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### reference-semantics/semantics/controls.k:37 — item 7 (`syntax`, `syntax`)

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### reference-semantics/semantics/controls.k:38 — item 8 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### reference-semantics/semantics/controls.k:39-41 — item 9 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
```

### reference-semantics/semantics/controls.k:43 — item 10 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
```

### reference-semantics/semantics/controls.k:48 — item 11 (`rule`, `rule/ordinary`)

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

### reference-semantics/semantics/controls.k:51 — item 12 (`syntax`, `syntax`)

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### reference-semantics/semantics/controls.k:52 — item 13 (`rule`, `rule/ordinary`)

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### reference-semantics/semantics/controls.k:53 — item 14 (`rule`, `rule/ordinary`)

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### reference-semantics/semantics/controls.k:54 — item 15 (`rule`, `rule/ordinary`)

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### reference-semantics/semantics/controls.k:57 — item 16 (`rule`, `rule/ordinary`)

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
```

### reference-semantics/semantics/controls.k:59 — item 17 (`rule`, `rule/ordinary`)

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
```

### reference-semantics/semantics/controls.k:65-67 — item 18 (`syntax`, `syntax`)

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### reference-semantics/semantics/controls.k:69 — item 19 (`rule`, `rule/ordinary`)

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### reference-semantics/semantics/controls.k:71 — item 20 (`rule`, `rule/ordinary`)

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### reference-semantics/semantics/controls.k:72 — item 21 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### reference-semantics/semantics/controls.k:73-74 — item 22 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### reference-semantics/semantics/controls.k:77 — item 23 (`rule`, `rule/ordinary`)

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### reference-semantics/semantics/controls.k:78 — item 24 (`rule`, `rule/ordinary`)

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### reference-semantics/semantics/controls.k:79 — item 25 (`rule`, `rule/ordinary`)

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
```

### reference-semantics/semantics/controls.k:81 — item 26 (`rule`, `rule/ordinary`)

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
```

### reference-semantics/semantics/controls.k:85 — item 27 (`rule`, `rule/ordinary`)

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### reference-semantics/semantics/controls.k:86 — item 28 (`rule`, `rule/ordinary`)

```k
  rule <k> Continue => #cont ... </k>
```

### reference-semantics/semantics/controls.k:87 — item 29 (`rule`, `rule/ordinary`)

```k
  rule <k> Break => #brk ... </k>
```

### reference-semantics/semantics/controls.k:88 — item 30 (`rule`, `rule/ordinary`)

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### reference-semantics/semantics/controls.k:89 — item 31 (`rule`, `rule/owise`)

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### reference-semantics/semantics/controls.k:90 — item 32 (`rule`, `rule/ordinary`)

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### reference-semantics/semantics/controls.k:91 — item 33 (`rule`, `rule/owise`)

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### reference-semantics/semantics/controls.k:95-97 — item 34 (`rule`, `rule/priority`)

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/controls.k:98-100 — item 35 (`rule`, `rule/priority`)

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/controls.k:101-103 — item 36 (`rule`, `rule/priority`)

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/controls.k:106-108 — item 37 (`rule`, `rule/priority`)

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/core.k`

SHA-256: `e0fdc11dc2b9cd0acb18fe7c832c1ea1ac0c9e79cadf40c63f34276aca513d7e`. Inventoried items: 84.

### reference-semantics/semantics/core.k:13 — item 1 (`syntax`, `syntax`)

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### reference-semantics/semantics/core.k:14 — item 2 (`syntax`, `syntax`)

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### reference-semantics/semantics/core.k:15 — item 3 (`syntax`, `syntax`)

```k
  syntax Str    ::= str(IntSeq)
```

### reference-semantics/semantics/core.k:18-23 — item 4 (`syntax`, `syntax`)

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### reference-semantics/semantics/core.k:25-34 — item 5 (`syntax`, `syntax/function`)

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

### reference-semantics/semantics/core.k:36 — item 6 (`syntax`, `syntax`)

```k
  syntax Parent   ::= "root" | parent(Int)
```

### reference-semantics/semantics/core.k:37 — item 7 (`syntax`, `syntax`)

```k
  syntax Scope    ::= scope(Map, Parent)
```

### reference-semantics/semantics/core.k:38 — item 8 (`syntax`, `syntax`)

```k
  syntax KResult  ::= Val
```

### reference-semantics/semantics/core.k:39 — item 9 (`syntax`, `syntax`)

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### reference-semantics/semantics/core.k:40 — item 10 (`syntax`, `syntax`)

```k
  syntax Vals     ::= List{Val, ","}
```

### reference-semantics/semantics/core.k:41 — item 11 (`syntax`, `syntax`)

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### reference-semantics/semantics/core.k:42 — item 12 (`syntax`, `syntax`)

```k
  syntax RetState ::= "noRet" | retV(Val)
```

### reference-semantics/semantics/core.k:49-60 — item 13 (`configuration`, `configuration`)

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

### reference-semantics/semantics/core.k:68 — item 14 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### reference-semantics/semantics/core.k:69 — item 15 (`rule`, `rule/ordinary`)

```k
  rule isRefV(ref(_:Int)) => true
```

### reference-semantics/semantics/core.k:70 — item 16 (`rule`, `rule/owise`)

```k
  rule isRefV(_:Val)      => false [owise]
```

### reference-semantics/semantics/core.k:75 — item 17 (`syntax`, `syntax`)

```k
  syntax HeapVal ::= cellV(Val)
```

### reference-semantics/semantics/core.k:76 — item 18 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### reference-semantics/semantics/core.k:77 — item 19 (`rule`, `rule/ordinary`)

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### reference-semantics/semantics/core.k:78 — item 20 (`rule`, `rule/owise`)

```k
  rule isCellRef(_:Val)          => false [owise]
```

### reference-semantics/semantics/core.k:85-88 — item 21 (`rule`, `rule/ordinary`)

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
```

### reference-semantics/semantics/core.k:95 — item 22 (`syntax`, `syntax`)

```k
  syntax Val ::= kwV(String, Val)
```

### reference-semantics/semantics/core.k:96 — item 23 (`syntax`, `syntax`)

```k
  syntax KItem ::= #kwTag(String)
```

### reference-semantics/semantics/core.k:97 — item 24 (`rule`, `rule/ordinary`)

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### reference-semantics/semantics/core.k:98 — item 25 (`rule`, `rule/ordinary`)

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
```

### reference-semantics/semantics/core.k:100 — item 26 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### reference-semantics/semantics/core.k:101 — item 27 (`rule`, `rule/ordinary`)

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### reference-semantics/semantics/core.k:102 — item 28 (`rule`, `rule/owise`)

```k
  rule isKwV(_:Val)                => false [owise]
```

### reference-semantics/semantics/core.k:106 — item 29 (`syntax`, `syntax`)

```k
  syntax Val ::= cellsMark(ParamNames)
```

### reference-semantics/semantics/core.k:107 — item 30 (`syntax`, `syntax/function`)

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### reference-semantics/semantics/core.k:108 — item 31 (`rule`, `rule/ordinary`)

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### reference-semantics/semantics/core.k:109 — item 32 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### reference-semantics/semantics/core.k:110 — item 33 (`rule`, `rule/ordinary`)

```k
  rule pnMember(_:String, .ParamNames) => false
```

### reference-semantics/semantics/core.k:111 — item 34 (`rule`, `rule/ordinary`)

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### reference-semantics/semantics/core.k:113 — item 35 (`syntax`, `syntax`)

```k
  syntax KItem ::= #cellW(Val, Val)
```

### reference-semantics/semantics/core.k:114-115 — item 36 (`rule`, `rule/ordinary`)

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### reference-semantics/semantics/core.k:117 — item 37 (`syntax`, `syntax`)

```k
  syntax KItem ::= #alloc(Val)
```

### reference-semantics/semantics/core.k:118-120 — item 38 (`rule`, `rule/ordinary`)

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
```

### reference-semantics/semantics/core.k:124 — item 39 (`syntax`, `syntax`)

```k
  syntax KItem ::= #loadAll(Module)
```

### reference-semantics/semantics/core.k:125 — item 40 (`rule`, `rule/ordinary`)

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### reference-semantics/semantics/core.k:126 — item 41 (`rule`, `rule/ordinary`)

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### reference-semantics/semantics/core.k:127 — item 42 (`rule`, `rule/ordinary`)

```k
  rule <k> .Stmts => .K ... </k>
```

### reference-semantics/semantics/core.k:130 — item 43 (`syntax`, `syntax`)

```k
  syntax KItem ::= #look(String, Int)
```

### reference-semantics/semantics/core.k:131 — item 44 (`rule`, `rule/ordinary`)

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### reference-semantics/semantics/core.k:132-133 — item 45 (`rule`, `rule/ordinary`)

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
```

### reference-semantics/semantics/core.k:145-147 — item 46 (`rule`, `rule/ordinary`)

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
```

### reference-semantics/semantics/core.k:152-153 — item 47 (`rule`, `rule/ordinary`)

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
```

### reference-semantics/semantics/core.k:157 — item 48 (`syntax`, `syntax/function,total`)

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### reference-semantics/semantics/core.k:158-181 — item 49 (`rule`, `rule/ordinary`)

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

### reference-semantics/semantics/core.k:185 — item 50 (`syntax`, `syntax`)

```k
  syntax ApplyK ::= toCall(Val)
```

### reference-semantics/semantics/core.k:186-188 — item 51 (`syntax`, `syntax`)

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### reference-semantics/semantics/core.k:189 — item 52 (`rule`, `rule/ordinary`)

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### reference-semantics/semantics/core.k:190 — item 53 (`rule`, `rule/ordinary`)

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### reference-semantics/semantics/core.k:191 — item 54 (`rule`, `rule/ordinary`)

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### reference-semantics/semantics/core.k:194 — item 55 (`rule`, `rule/ordinary`)

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### reference-semantics/semantics/core.k:195 — item 56 (`rule`, `rule/ordinary`)

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### reference-semantics/semantics/core.k:196 — item 57 (`rule`, `rule/ordinary`)

```k
  rule <k> NoneVal      => noneV ... </k>
```

### reference-semantics/semantics/core.k:199 — item 58 (`syntax`, `syntax/function`)

```k
  syntax Bool ::= truthy(Val) [function]
```

### reference-semantics/semantics/core.k:200 — item 59 (`rule`, `rule/ordinary`)

```k
  rule truthy(B:Bool)          => B
```

### reference-semantics/semantics/core.k:201 — item 60 (`rule`, `rule/ordinary`)

```k
  rule truthy(noneV)           => false
```

### reference-semantics/semantics/core.k:202 — item 61 (`rule`, `rule/ordinary`)

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### reference-semantics/semantics/core.k:203 — item 62 (`rule`, `rule/ordinary`)

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### reference-semantics/semantics/core.k:204 — item 63 (`rule`, `rule/ordinary`)

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### reference-semantics/semantics/core.k:205 — item 64 (`rule`, `rule/ordinary`)

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### reference-semantics/semantics/core.k:208 — item 65 (`syntax`, `syntax/function`)

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### reference-semantics/semantics/core.k:209 — item 66 (`syntax`, `syntax/function`)

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### reference-semantics/semantics/core.k:210 — item 67 (`syntax`, `syntax/function`)

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### reference-semantics/semantics/core.k:213 — item 68 (`syntax`, `syntax/function,total`)

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### reference-semantics/semantics/core.k:214 — item 69 (`rule`, `rule/ordinary`)

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### reference-semantics/semantics/core.k:215 — item 70 (`rule`, `rule/ordinary`)

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### reference-semantics/semantics/core.k:217 — item 71 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### reference-semantics/semantics/core.k:218 — item 72 (`rule`, `rule/ordinary`)

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### reference-semantics/semantics/core.k:219 — item 73 (`rule`, `rule/ordinary`)

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### reference-semantics/semantics/core.k:223 — item 74 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### reference-semantics/semantics/core.k:224 — item 75 (`rule`, `rule/ordinary`)

```k
  rule vsLen(.ValSeq)                => 0
```

### reference-semantics/semantics/core.k:225 — item 76 (`rule`, `rule/ordinary`)

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### reference-semantics/semantics/core.k:227 — item 77 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### reference-semantics/semantics/core.k:228 — item 78 (`rule`, `rule/ordinary`)

```k
  rule isLen(.IntSeq)                => 0
```

### reference-semantics/semantics/core.k:229 — item 79 (`rule`, `rule/ordinary`)

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### reference-semantics/semantics/core.k:233 — item 80 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### reference-semantics/semantics/core.k:234 — item 81 (`rule`, `rule/ordinary`)

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### reference-semantics/semantics/core.k:235 — item 82 (`rule`, `rule/ordinary`)

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### reference-semantics/semantics/core.k:236 — item 83 (`rule`, `rule/ordinary`)

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
```

### reference-semantics/semantics/core.k:238 — item 84 (`rule`, `rule/ordinary`)

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
```

## `reference-semantics/semantics/dict.k`

SHA-256: `779b06e18162464c8422bbd6ac35fa0b9e34ef82807d5c707c6f4552d63c0580`. Inventoried items: 40.

### reference-semantics/semantics/dict.k:20 — item 1 (`syntax`, `syntax`)

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

### reference-semantics/semantics/dict.k:23-25 — item 2 (`syntax`, `syntax`)

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### reference-semantics/semantics/dict.k:26 — item 3 (`rule`, `rule/ordinary`)

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### reference-semantics/semantics/dict.k:27 — item 4 (`rule`, `rule/ordinary`)

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### reference-semantics/semantics/dict.k:28-29 — item 5 (`rule`, `rule/ordinary`)

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### reference-semantics/semantics/dict.k:30-31 — item 6 (`rule`, `rule/ordinary`)

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### reference-semantics/semantics/dict.k:32-33 — item 7 (`rule`, `rule/ordinary`)

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### reference-semantics/semantics/dict.k:37 — item 8 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### reference-semantics/semantics/dict.k:38 — item 9 (`rule`, `rule/ordinary`)

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### reference-semantics/semantics/dict.k:39 — item 10 (`rule`, `rule/ordinary`)

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### reference-semantics/semantics/dict.k:40 — item 11 (`rule`, `rule/ordinary`)

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### reference-semantics/semantics/dict.k:43 — item 12 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### reference-semantics/semantics/dict.k:44 — item 13 (`rule`, `rule/ordinary`)

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### reference-semantics/semantics/dict.k:45 — item 14 (`rule`, `rule/ordinary`)

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### reference-semantics/semantics/dict.k:49 — item 15 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### reference-semantics/semantics/dict.k:50 — item 16 (`rule`, `rule/ordinary`)

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
```

### reference-semantics/semantics/dict.k:52 — item 17 (`rule`, `rule/ordinary`)

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
```

### reference-semantics/semantics/dict.k:54 — item 18 (`rule`, `rule/owise`)

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### reference-semantics/semantics/dict.k:58-60 — item 19 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/dict.k:63 — item 20 (`rule`, `rule/ordinary`)

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### reference-semantics/semantics/dict.k:64 — item 21 (`syntax`, `syntax/function`)

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### reference-semantics/semantics/dict.k:65-66 — item 22 (`rule`, `rule/priority`)

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

### reference-semantics/semantics/dict.k:70 — item 23 (`syntax`, `syntax/function`)

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### reference-semantics/semantics/dict.k:71 — item 24 (`rule`, `rule/ordinary`)

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### reference-semantics/semantics/dict.k:76 — item 25 (`syntax`, `syntax`)

```k
  syntax KItem ::= #dsetK(String, Val)
```

### reference-semantics/semantics/dict.k:77 — item 26 (`rule`, `rule/ordinary`)

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### reference-semantics/semantics/dict.k:78-80 — item 27 (`rule`, `rule/ordinary`)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
```

### reference-semantics/semantics/dict.k:82-84 — item 28 (`rule`, `rule/ordinary`)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/dict.k:86 — item 29 (`syntax`, `syntax`)

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### reference-semantics/semantics/dict.k:87-88 — item 30 (`rule`, `rule/ordinary`)

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### reference-semantics/semantics/dict.k:90 — item 31 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### reference-semantics/semantics/dict.k:91 — item 32 (`rule`, `rule/ordinary`)

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### reference-semantics/semantics/dict.k:92 — item 33 (`rule`, `rule/ordinary`)

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### reference-semantics/semantics/dict.k:95-96 — item 34 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### reference-semantics/semantics/dict.k:97 — item 35 (`syntax`, `syntax/function`)

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### reference-semantics/semantics/dict.k:98 — item 36 (`rule`, `rule/ordinary`)

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### reference-semantics/semantics/dict.k:99-100 — item 37 (`rule`, `rule/ordinary`)

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### reference-semantics/semantics/dict.k:101 — item 38 (`syntax`, `syntax/function`)

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### reference-semantics/semantics/dict.k:102 — item 39 (`rule`, `rule/ordinary`)

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### reference-semantics/semantics/dict.k:103 — item 40 (`rule`, `rule/ordinary`)

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## `reference-semantics/semantics/float.k`

SHA-256: `5dfeee8700c90c3aa6dc515b15b74283882845fb6cdcc3627d97ef650124b70f`. Inventoried items: 155.

### reference-semantics/semantics/float.k:20 — item 1 (`syntax`, `syntax`)

```k
  syntax Val ::= Float
```

### reference-semantics/semantics/float.k:21 — item 2 (`rule`, `rule/ordinary`)

```k
  rule <k> Float(F:Float) => F ... </k>
```

### reference-semantics/semantics/float.k:24 — item 3 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### reference-semantics/semantics/float.k:25 — item 4 (`rule`, `rule/concrete`)

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### reference-semantics/semantics/float.k:27 — item 5 (`rule`, `rule/ordinary`)

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### reference-semantics/semantics/float.k:30 — item 6 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### reference-semantics/semantics/float.k:31 — item 7 (`rule`, `rule/concrete`)

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:32 — item 8 (`rule`, `rule/ordinary`)

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### reference-semantics/semantics/float.k:37 — item 9 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### reference-semantics/semantics/float.k:38 — item 10 (`rule`, `rule/concrete`)

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### reference-semantics/semantics/float.k:39 — item 11 (`rule`, `rule/ordinary`)

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### reference-semantics/semantics/float.k:43 — item 12 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### reference-semantics/semantics/float.k:44 — item 13 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### reference-semantics/semantics/float.k:50 — item 14 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### reference-semantics/semantics/float.k:51 — item 15 (`rule`, `rule/concrete`)

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### reference-semantics/semantics/float.k:52 — item 16 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### reference-semantics/semantics/float.k:54 — item 17 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### reference-semantics/semantics/float.k:55 — item 18 (`rule`, `rule/concrete`)

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### reference-semantics/semantics/float.k:56 — item 19 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### reference-semantics/semantics/float.k:61 — item 20 (`rule`, `rule/ordinary`)

```k
  rule <k> Import(_:String) => .K ... </k>
```

### reference-semantics/semantics/float.k:65 — item 21 (`syntax`, `syntax`)

```k
  syntax KItem ::= "#mathCeil"
```

### reference-semantics/semantics/float.k:66 — item 22 (`rule`, `rule/priority`)

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:67 — item 23 (`rule`, `rule/ordinary`)

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### reference-semantics/semantics/float.k:70 — item 24 (`syntax`, `syntax`)

```k
  syntax KItem ::= "#mathFloor"
```

### reference-semantics/semantics/float.k:71 — item 25 (`rule`, `rule/priority`)

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:72 — item 26 (`rule`, `rule/ordinary`)

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### reference-semantics/semantics/float.k:73 — item 27 (`syntax`, `syntax/function,total,symbol`)

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### reference-semantics/semantics/float.k:74 — item 28 (`rule`, `rule/concrete`)

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### reference-semantics/semantics/float.k:75 — item 29 (`rule`, `rule/concrete`)

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### reference-semantics/semantics/float.k:78 — item 30 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### reference-semantics/semantics/float.k:79 — item 31 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### reference-semantics/semantics/float.k:82 — item 32 (`syntax`, `syntax`)

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### reference-semantics/semantics/float.k:83 — item 33 (`rule`, `rule/priority`)

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:84 — item 34 (`rule`, `rule/ordinary`)

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### reference-semantics/semantics/float.k:85 — item 35 (`rule`, `rule/ordinary`)

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### reference-semantics/semantics/float.k:86 — item 36 (`syntax`, `syntax/function,total,symbol`)

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### reference-semantics/semantics/float.k:87 — item 37 (`rule`, `rule/concrete`)

```k
  rule toF(F:Float) => F        [concrete]
```

### reference-semantics/semantics/float.k:88 — item 38 (`rule`, `rule/concrete`)

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

### reference-semantics/semantics/float.k:93 — item 39 (`syntax`, `syntax/function,total,symbol`)

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### reference-semantics/semantics/float.k:94 — item 40 (`rule`, `rule/concrete`)

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### reference-semantics/semantics/float.k:95 — item 41 (`rule`, `rule/concrete`)

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### reference-semantics/semantics/float.k:99 — item 42 (`rule`, `rule/ordinary`)

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

### reference-semantics/semantics/float.k:103 — item 43 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### reference-semantics/semantics/float.k:104 — item 44 (`rule`, `rule/concrete`)

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### reference-semantics/semantics/float.k:105 — item 45 (`rule`, `rule/ordinary`)

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### reference-semantics/semantics/float.k:107 — item 46 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### reference-semantics/semantics/float.k:108 — item 47 (`rule`, `rule/concrete`)

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### reference-semantics/semantics/float.k:109 — item 48 (`rule`, `rule/ordinary`)

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### reference-semantics/semantics/float.k:111 — item 49 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### reference-semantics/semantics/float.k:112 — item 50 (`rule`, `rule/concrete`)

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### reference-semantics/semantics/float.k:113 — item 51 (`rule`, `rule/ordinary`)

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### reference-semantics/semantics/float.k:115 — item 52 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### reference-semantics/semantics/float.k:116 — item 53 (`rule`, `rule/concrete`)

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### reference-semantics/semantics/float.k:117 — item 54 (`rule`, `rule/ordinary`)

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### reference-semantics/semantics/float.k:119 — item 55 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### reference-semantics/semantics/float.k:120 — item 56 (`rule`, `rule/concrete`)

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### reference-semantics/semantics/float.k:121 — item 57 (`rule`, `rule/ordinary`)

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### reference-semantics/semantics/float.k:125 — item 58 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### reference-semantics/semantics/float.k:126 — item 59 (`rule`, `rule/concrete`)

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### reference-semantics/semantics/float.k:127 — item 60 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### reference-semantics/semantics/float.k:128 — item 61 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### reference-semantics/semantics/float.k:129 — item 62 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### reference-semantics/semantics/float.k:132 — item 63 (`rule`, `rule/ordinary`)

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### reference-semantics/semantics/float.k:133 — item 64 (`rule`, `rule/ordinary`)

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### reference-semantics/semantics/float.k:134 — item 65 (`rule`, `rule/ordinary`)

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### reference-semantics/semantics/float.k:135 — item 66 (`rule`, `rule/ordinary`)

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### reference-semantics/semantics/float.k:136 — item 67 (`rule`, `rule/ordinary`)

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### reference-semantics/semantics/float.k:137 — item 68 (`rule`, `rule/ordinary`)

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### reference-semantics/semantics/float.k:138 — item 69 (`rule`, `rule/ordinary`)

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### reference-semantics/semantics/float.k:139 — item 70 (`rule`, `rule/ordinary`)

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### reference-semantics/semantics/float.k:142 — item 71 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### reference-semantics/semantics/float.k:143 — item 72 (`rule`, `rule/concrete`)

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### reference-semantics/semantics/float.k:144 — item 73 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### reference-semantics/semantics/float.k:145 — item 74 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### reference-semantics/semantics/float.k:146 — item 75 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### reference-semantics/semantics/float.k:147 — item 76 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### reference-semantics/semantics/float.k:148 — item 77 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### reference-semantics/semantics/float.k:149 — item 78 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### reference-semantics/semantics/float.k:150 — item 79 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### reference-semantics/semantics/float.k:151 — item 80 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### reference-semantics/semantics/float.k:154 — item 81 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### reference-semantics/semantics/float.k:155 — item 82 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### reference-semantics/semantics/float.k:160 — item 83 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### reference-semantics/semantics/float.k:161 — item 84 (`rule`, `rule/concrete`)

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### reference-semantics/semantics/float.k:162-163 — item 85 (`rule`, `rule/ordinary`)

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
```

### reference-semantics/semantics/float.k:165 — item 86 (`syntax`, `syntax/function`)

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### reference-semantics/semantics/float.k:166 — item 87 (`rule`, `rule/ordinary`)

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### reference-semantics/semantics/float.k:167 — item 88 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/float.k:168 — item 89 (`rule`, `rule/ordinary`)

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### reference-semantics/semantics/float.k:169 — item 90 (`rule`, `rule/ordinary`)

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### reference-semantics/semantics/float.k:170 — item 91 (`rule`, `rule/ordinary`)

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### reference-semantics/semantics/float.k:171 — item 92 (`rule`, `rule/ordinary`)

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
```

### reference-semantics/semantics/float.k:173 — item 93 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/float.k:174 — item 94 (`rule`, `rule/ordinary`)

```k
  rule fracPart(.IntSeq) => 0
```

### reference-semantics/semantics/float.k:175 — item 95 (`rule`, `rule/ordinary`)

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### reference-semantics/semantics/float.k:176 — item 96 (`rule`, `rule/ordinary`)

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### reference-semantics/semantics/float.k:177 — item 97 (`rule`, `rule/ordinary`)

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### reference-semantics/semantics/float.k:178 — item 98 (`rule`, `rule/ordinary`)

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### reference-semantics/semantics/float.k:179 — item 99 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/float.k:180 — item 100 (`rule`, `rule/ordinary`)

```k
  rule fracScale(.IntSeq) => 1
```

### reference-semantics/semantics/float.k:181 — item 101 (`rule`, `rule/ordinary`)

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### reference-semantics/semantics/float.k:182 — item 102 (`rule`, `rule/ordinary`)

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### reference-semantics/semantics/float.k:183 — item 103 (`rule`, `rule/ordinary`)

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### reference-semantics/semantics/float.k:184 — item 104 (`rule`, `rule/ordinary`)

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### reference-semantics/semantics/float.k:185 — item 105 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### reference-semantics/semantics/float.k:186 — item 106 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### reference-semantics/semantics/float.k:187 — item 107 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

### reference-semantics/semantics/float.k:190 — item 108 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### reference-semantics/semantics/float.k:191 — item 109 (`rule`, `rule/concrete`)

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:192 — item 110 (`rule`, `rule/ordinary`)

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### reference-semantics/semantics/float.k:195 — item 111 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### reference-semantics/semantics/float.k:196 — item 112 (`rule`, `rule/concrete`)

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:197 — item 113 (`rule`, `rule/ordinary`)

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### reference-semantics/semantics/float.k:198 — item 114 (`rule`, `rule/ordinary`)

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### reference-semantics/semantics/float.k:199 — item 115 (`rule`, `rule/ordinary`)

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### reference-semantics/semantics/float.k:200 — item 116 (`rule`, `rule/ordinary`)

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### reference-semantics/semantics/float.k:201 — item 117 (`rule`, `rule/ordinary`)

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### reference-semantics/semantics/float.k:202 — item 118 (`rule`, `rule/ordinary`)

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### reference-semantics/semantics/float.k:203 — item 119 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### reference-semantics/semantics/float.k:204 — item 120 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### reference-semantics/semantics/float.k:205 — item 121 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### reference-semantics/semantics/float.k:206 — item 122 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### reference-semantics/semantics/float.k:209 — item 123 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### reference-semantics/semantics/float.k:210 — item 124 (`rule`, `rule/concrete`)

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### reference-semantics/semantics/float.k:211 — item 125 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### reference-semantics/semantics/float.k:213 — item 126 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### reference-semantics/semantics/float.k:214 — item 127 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

### reference-semantics/semantics/float.k:217 — item 128 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### reference-semantics/semantics/float.k:218-222 — item 129 (`rule`, `rule/concrete`)

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### reference-semantics/semantics/float.k:223 — item 130 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### reference-semantics/semantics/float.k:224-226 — item 131 (`rule`, `rule/concrete`)

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### reference-semantics/semantics/float.k:227 — item 132 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### reference-semantics/semantics/float.k:228 — item 133 (`rule`, `rule/ordinary`)

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### reference-semantics/semantics/float.k:230 — item 134 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### reference-semantics/semantics/float.k:231 — item 135 (`rule`, `rule/concrete`)

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### reference-semantics/semantics/float.k:232 — item 136 (`syntax`, `syntax`)

```k
  syntax KItem ::= "#mathSqrt"
```

### reference-semantics/semantics/float.k:233 — item 137 (`rule`, `rule/priority`)

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### reference-semantics/semantics/float.k:234 — item 138 (`rule`, `rule/ordinary`)

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### reference-semantics/semantics/float.k:235 — item 139 (`rule`, `rule/ordinary`)

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### reference-semantics/semantics/float.k:243 — item 140 (`syntax`, `syntax`)

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### reference-semantics/semantics/float.k:244 — item 141 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### reference-semantics/semantics/float.k:245 — item 142 (`rule`, `rule/ordinary`)

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### reference-semantics/semantics/float.k:246 — item 143 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### reference-semantics/semantics/float.k:247 — item 144 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
```

### reference-semantics/semantics/float.k:250 — item 145 (`syntax`, `syntax`)

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### reference-semantics/semantics/float.k:251 — item 146 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### reference-semantics/semantics/float.k:252 — item 147 (`rule`, `rule/ordinary`)

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### reference-semantics/semantics/float.k:253 — item 148 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### reference-semantics/semantics/float.k:254 — item 149 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
```

### reference-semantics/semantics/float.k:261 — item 150 (`syntax`, `syntax`)

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### reference-semantics/semantics/float.k:262-263 — item 151 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
```

### reference-semantics/semantics/float.k:265 — item 152 (`rule`, `rule/ordinary`)

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### reference-semantics/semantics/float.k:266 — item 153 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### reference-semantics/semantics/float.k:267-268 — item 154 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
```

### reference-semantics/semantics/float.k:270-271 — item 155 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
```

## `reference-semantics/semantics/functions.k`

SHA-256: `e4c8f67741117b29703c3c61d48a5b0f92cf7bd531e78e25c03e794a910ac193`. Inventoried items: 19.

### reference-semantics/semantics/functions.k:8-11 — item 1 (`syntax`, `syntax`)

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

### reference-semantics/semantics/functions.k:14-16 — item 2 (`rule`, `rule/ordinary`)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### reference-semantics/semantics/functions.k:18 — item 3 (`syntax`, `syntax`)

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### reference-semantics/semantics/functions.k:19-20 — item 4 (`rule`, `rule/ordinary`)

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

### reference-semantics/semantics/functions.k:27 — item 5 (`syntax`, `syntax`)

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### reference-semantics/semantics/functions.k:31-32 — item 6 (`syntax`, `syntax`)

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### reference-semantics/semantics/functions.k:33-35 — item 7 (`rule`, `rule/ordinary`)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### reference-semantics/semantics/functions.k:36-40 — item 8 (`rule`, `rule/ordinary`)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/functions.k:42-45 — item 9 (`rule`, `rule/ordinary`)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### reference-semantics/semantics/functions.k:47-49 — item 10 (`rule`, `rule/ordinary`)

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### reference-semantics/semantics/functions.k:50-52 — item 11 (`rule`, `rule/ordinary`)

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### reference-semantics/semantics/functions.k:53-57 — item 12 (`rule`, `rule/ordinary`)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/functions.k:59-60 — item 13 (`rule`, `rule/ordinary`)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### reference-semantics/semantics/functions.k:63 — item 14 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### reference-semantics/semantics/functions.k:64-66 — item 15 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### reference-semantics/semantics/functions.k:68-71 — item 16 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/functions.k:78-79 — item 17 (`rule`, `rule/ordinary`)

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### reference-semantics/semantics/functions.k:80-81 — item 18 (`rule`, `rule/ordinary`)

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

### reference-semantics/semantics/functions.k:85-90 — item 19 (`rule`, `rule/ordinary`)

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## `reference-semantics/semantics/int.k`

SHA-256: `dc2da7d81578370651ecb6905b69cb44443cdd8db3869441242b81420382abe5`. Inventoried items: 17.

### reference-semantics/semantics/int.k:7 — item 1 (`rule`, `rule/ordinary`)

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### reference-semantics/semantics/int.k:9 — item 2 (`rule`, `rule/ordinary`)

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### reference-semantics/semantics/int.k:11 — item 3 (`rule`, `rule/ordinary`)

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### reference-semantics/semantics/int.k:12 — item 4 (`rule`, `rule/ordinary`)

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### reference-semantics/semantics/int.k:13 — item 5 (`rule`, `rule/ordinary`)

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### reference-semantics/semantics/int.k:14 — item 6 (`rule`, `rule/ordinary`)

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### reference-semantics/semantics/int.k:15 — item 7 (`rule`, `rule/ordinary`)

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### reference-semantics/semantics/int.k:16 — item 8 (`rule`, `rule/ordinary`)

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### reference-semantics/semantics/int.k:17 — item 9 (`rule`, `rule/ordinary`)

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### reference-semantics/semantics/int.k:19 — item 10 (`syntax`, `syntax/function`)

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### reference-semantics/semantics/int.k:20 — item 11 (`rule`, `rule/ordinary`)

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### reference-semantics/semantics/int.k:22 — item 12 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### reference-semantics/semantics/int.k:23 — item 13 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### reference-semantics/semantics/int.k:24 — item 14 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### reference-semantics/semantics/int.k:25 — item 15 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### reference-semantics/semantics/int.k:26 — item 16 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### reference-semantics/semantics/int.k:27 — item 17 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## `reference-semantics/semantics/iter.k`

SHA-256: `5085db2fed67b7bbd39f6289ec275905aaee742690895d7b3f843f73bd62f77f`. Inventoried items: 1.

### reference-semantics/semantics/iter.k:8 — item 1 (`syntax`, `syntax`)

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## `reference-semantics/semantics/list.k`

SHA-256: `870c72341c25e2c16283726191a71bf5b571ed2995c8ae12e3e2923cdce5a9aa`. Inventoried items: 32.

### reference-semantics/semantics/list.k:9 — item 1 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### reference-semantics/semantics/list.k:10 — item 2 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### reference-semantics/semantics/list.k:13 — item 3 (`syntax`, `syntax`)

```k
  syntax ApplyK ::= "toList"
```

### reference-semantics/semantics/list.k:14 — item 4 (`rule`, `rule/ordinary`)

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### reference-semantics/semantics/list.k:15 — item 5 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### reference-semantics/semantics/list.k:18 — item 6 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### reference-semantics/semantics/list.k:19 — item 7 (`rule`, `rule/ordinary`)

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### reference-semantics/semantics/list.k:20 — item 8 (`rule`, `rule/ordinary`)

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### reference-semantics/semantics/list.k:24-25 — item 9 (`rule`, `rule/priority`)

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### reference-semantics/semantics/list.k:27 — item 10 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### reference-semantics/semantics/list.k:28 — item 11 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### reference-semantics/semantics/list.k:33 — item 12 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### reference-semantics/semantics/list.k:34 — item 13 (`rule`, `rule/ordinary`)

```k
  rule hasRefVS(.ValSeq)                => false
```

### reference-semantics/semantics/list.k:35 — item 14 (`rule`, `rule/ordinary`)

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### reference-semantics/semantics/list.k:37-38 — item 15 (`syntax`, `syntax/function`)

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### reference-semantics/semantics/list.k:39 — item 16 (`rule`, `rule/ordinary`)

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### reference-semantics/semantics/list.k:40 — item 17 (`rule`, `rule/ordinary`)

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### reference-semantics/semantics/list.k:41 — item 18 (`rule`, `rule/ordinary`)

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### reference-semantics/semantics/list.k:42-43 — item 19 (`rule`, `rule/ordinary`)

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### reference-semantics/semantics/list.k:45 — item 20 (`rule`, `rule/ordinary`)

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
```

### reference-semantics/semantics/list.k:47 — item 21 (`rule`, `rule/ordinary`)

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
```

### reference-semantics/semantics/list.k:49 — item 22 (`rule`, `rule/ordinary`)

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### reference-semantics/semantics/list.k:50 — item 23 (`rule`, `rule/owise`)

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### reference-semantics/semantics/list.k:53-55 — item 24 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/list.k:58 — item 25 (`syntax`, `syntax`)

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### reference-semantics/semantics/list.k:59 — item 26 (`rule`, `rule/ordinary`)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### reference-semantics/semantics/list.k:60 — item 27 (`rule`, `rule/ordinary`)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### reference-semantics/semantics/list.k:61 — item 28 (`rule`, `rule/ordinary`)

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### reference-semantics/semantics/list.k:62 — item 29 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### reference-semantics/semantics/list.k:63 — item 30 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
```

### reference-semantics/semantics/list.k:65 — item 31 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
```

### reference-semantics/semantics/list.k:67 — item 32 (`rule`, `rule/ordinary`)

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## `reference-semantics/semantics/methods.k`

SHA-256: `ff9acc6dab2d1cc99ec4f2d234f27ae4526d752aae62bcfd7f9fd2a0399f7743`. Inventoried items: 102.

### reference-semantics/semantics/methods.k:10 — item 1 (`syntax`, `syntax/function`)

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### reference-semantics/semantics/methods.k:13 — item 2 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### reference-semantics/semantics/methods.k:14 — item 3 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### reference-semantics/semantics/methods.k:15 — item 4 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### reference-semantics/semantics/methods.k:16 — item 5 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### reference-semantics/semantics/methods.k:19 — item 6 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### reference-semantics/semantics/methods.k:20 — item 7 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### reference-semantics/semantics/methods.k:21 — item 8 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### reference-semantics/semantics/methods.k:26 — item 9 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### reference-semantics/semantics/methods.k:27 — item 10 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### reference-semantics/semantics/methods.k:28 — item 11 (`rule`, `rule/ordinary`)

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:29 — item 12 (`rule`, `rule/ordinary`)

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### reference-semantics/semantics/methods.k:30-31 — item 13 (`rule`, `rule/ordinary`)

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### reference-semantics/semantics/methods.k:34 — item 14 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### reference-semantics/semantics/methods.k:35 — item 15 (`syntax`, `syntax/function`)

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### reference-semantics/semantics/methods.k:36 — item 16 (`rule`, `rule/ordinary`)

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### reference-semantics/semantics/methods.k:37 — item 17 (`rule`, `rule/ordinary`)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
```

### reference-semantics/semantics/methods.k:39 — item 18 (`rule`, `rule/ordinary`)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
```

### reference-semantics/semantics/methods.k:41 — item 19 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/methods.k:42 — item 20 (`rule`, `rule/ordinary`)

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### reference-semantics/semantics/methods.k:43 — item 21 (`rule`, `rule/owise`)

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### reference-semantics/semantics/methods.k:44 — item 22 (`rule`, `rule/ordinary`)

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### reference-semantics/semantics/methods.k:47 — item 23 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### reference-semantics/semantics/methods.k:48 — item 24 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:49 — item 25 (`rule`, `rule/ordinary`)

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:50 — item 26 (`rule`, `rule/ordinary`)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### reference-semantics/semantics/methods.k:51 — item 27 (`rule`, `rule/ordinary`)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### reference-semantics/semantics/methods.k:52 — item 28 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:53 — item 29 (`rule`, `rule/ordinary`)

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### reference-semantics/semantics/methods.k:54 — item 30 (`rule`, `rule/ordinary`)

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### reference-semantics/semantics/methods.k:55 — item 31 (`rule`, `rule/ordinary`)

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### reference-semantics/semantics/methods.k:58 — item 32 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### reference-semantics/semantics/methods.k:61 — item 33 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### reference-semantics/semantics/methods.k:64 — item 34 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### reference-semantics/semantics/methods.k:65 — item 35 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### reference-semantics/semantics/methods.k:66 — item 36 (`rule`, `rule/ordinary`)

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### reference-semantics/semantics/methods.k:67 — item 37 (`rule`, `rule/ordinary`)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### reference-semantics/semantics/methods.k:68 — item 38 (`rule`, `rule/ordinary`)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### reference-semantics/semantics/methods.k:72-74 — item 39 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/methods.k:75 — item 40 (`syntax`, `syntax/function,token`)

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### reference-semantics/semantics/methods.k:76 — item 41 (`rule`, `rule/ordinary`)

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### reference-semantics/semantics/methods.k:77 — item 42 (`rule`, `rule/ordinary`)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
```

### reference-semantics/semantics/methods.k:79 — item 43 (`rule`, `rule/ordinary`)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
```

### reference-semantics/semantics/methods.k:82 — item 44 (`syntax`, `syntax/function`)

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### reference-semantics/semantics/methods.k:83 — item 45 (`rule`, `rule/ordinary`)

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### reference-semantics/semantics/methods.k:84 — item 46 (`rule`, `rule/ordinary`)

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### reference-semantics/semantics/methods.k:85 — item 47 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:86 — item 48 (`rule`, `rule/ordinary`)

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### reference-semantics/semantics/methods.k:89-91 — item 49 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

### reference-semantics/semantics/methods.k:94-96 — item 50 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### reference-semantics/semantics/methods.k:97 — item 51 (`syntax`, `syntax/function,token`)

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### reference-semantics/semantics/methods.k:98 — item 52 (`rule`, `rule/ordinary`)

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### reference-semantics/semantics/methods.k:99 — item 53 (`rule`, `rule/ordinary`)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
```

### reference-semantics/semantics/methods.k:101 — item 54 (`rule`, `rule/ordinary`)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
```

### reference-semantics/semantics/methods.k:104-105 — item 55 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### reference-semantics/semantics/methods.k:106 — item 56 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### reference-semantics/semantics/methods.k:107 — item 57 (`rule`, `rule/ordinary`)

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### reference-semantics/semantics/methods.k:108 — item 58 (`rule`, `rule/ordinary`)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### reference-semantics/semantics/methods.k:109 — item 59 (`rule`, `rule/ordinary`)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### reference-semantics/semantics/methods.k:112 — item 60 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:113 — item 61 (`rule`, `rule/ordinary`)

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### reference-semantics/semantics/methods.k:115 — item 62 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:116 — item 63 (`rule`, `rule/ordinary`)

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### reference-semantics/semantics/methods.k:118 — item 64 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:119 — item 65 (`rule`, `rule/ordinary`)

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### reference-semantics/semantics/methods.k:121 — item 66 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:122 — item 67 (`rule`, `rule/ordinary`)

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### reference-semantics/semantics/methods.k:124 — item 68 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:125 — item 69 (`rule`, `rule/ordinary`)

```k
  rule hasUpper(.IntSeq) => false
```

### reference-semantics/semantics/methods.k:126 — item 70 (`rule`, `rule/ordinary`)

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### reference-semantics/semantics/methods.k:128 — item 71 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:129 — item 72 (`rule`, `rule/ordinary`)

```k
  rule hasLower(.IntSeq) => false
```

### reference-semantics/semantics/methods.k:130 — item 73 (`rule`, `rule/ordinary`)

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### reference-semantics/semantics/methods.k:132 — item 74 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:133 — item 75 (`rule`, `rule/ordinary`)

```k
  rule allAlpha(.IntSeq) => true
```

### reference-semantics/semantics/methods.k:134 — item 76 (`rule`, `rule/ordinary`)

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### reference-semantics/semantics/methods.k:136 — item 77 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:137 — item 78 (`rule`, `rule/ordinary`)

```k
  rule allDigit(.IntSeq) => true
```

### reference-semantics/semantics/methods.k:138 — item 79 (`rule`, `rule/ordinary`)

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### reference-semantics/semantics/methods.k:140 — item 80 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:142 — item 81 (`rule`, `rule/ordinary`)

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### reference-semantics/semantics/methods.k:143 — item 82 (`rule`, `rule/owise`)

```k
  rule lowerC(C:Int) => C         [owise]
```

### reference-semantics/semantics/methods.k:145 — item 83 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= upperC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:146 — item 84 (`rule`, `rule/ordinary`)

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### reference-semantics/semantics/methods.k:147 — item 85 (`rule`, `rule/owise`)

```k
  rule upperC(C:Int) => C         [owise]
```

### reference-semantics/semantics/methods.k:149 — item 86 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= swapC(Int) [function, total]
```

### reference-semantics/semantics/methods.k:150 — item 87 (`rule`, `rule/ordinary`)

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### reference-semantics/semantics/methods.k:151 — item 88 (`rule`, `rule/ordinary`)

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### reference-semantics/semantics/methods.k:152 — item 89 (`rule`, `rule/owise`)

```k
  rule swapC(C:Int) => C         [owise]
```

### reference-semantics/semantics/methods.k:154 — item 90 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:155 — item 91 (`rule`, `rule/ordinary`)

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:156 — item 92 (`rule`, `rule/ordinary`)

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### reference-semantics/semantics/methods.k:158 — item 93 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:159 — item 94 (`rule`, `rule/ordinary`)

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:160 — item 95 (`rule`, `rule/ordinary`)

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### reference-semantics/semantics/methods.k:162 — item 96 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:163 — item 97 (`rule`, `rule/ordinary`)

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### reference-semantics/semantics/methods.k:164 — item 98 (`rule`, `rule/ordinary`)

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### reference-semantics/semantics/methods.k:166 — item 99 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/methods.k:167 — item 100 (`rule`, `rule/ordinary`)

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### reference-semantics/semantics/methods.k:168 — item 101 (`rule`, `rule/ordinary`)

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### reference-semantics/semantics/methods.k:169 — item 102 (`rule`, `rule/ordinary`)

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## `reference-semantics/semantics/operators.k`

SHA-256: `f3d1fd85734f5e1757307e606cbfb8d6d4bf0893ee85ce20ec99606ade910e8b`. Inventoried items: 12.

### reference-semantics/semantics/operators.k:10 — item 1 (`rule`, `rule/ordinary`)

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### reference-semantics/semantics/operators.k:12 — item 2 (`rule`, `rule/ordinary`)

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### reference-semantics/semantics/operators.k:15 — item 3 (`context`, `context`)

```k
  context Compare(HOLE, _)
```

### reference-semantics/semantics/operators.k:16 — item 4 (`context`, `context`)

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### reference-semantics/semantics/operators.k:17 — item 5 (`rule`, `rule/owise`)

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### reference-semantics/semantics/operators.k:19 — item 6 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### reference-semantics/semantics/operators.k:20 — item 7 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### reference-semantics/semantics/operators.k:25-27 — item 8 (`rule`, `rule/priority`)

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/operators.k:28-29 — item 9 (`rule`, `rule/ordinary`)

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/operators.k:34-35 — item 10 (`rule`, `rule/ordinary`)

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/operators.k:38-39 — item 11 (`rule`, `rule/ordinary`)

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
```

### reference-semantics/semantics/operators.k:44-46 — item 12 (`rule`, `rule/priority`)

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/range.k`

SHA-256: `810e4c04b757445c03592aef25c97d6b2cc7c6fffa646288bc6cd15a3cae643d`. Inventoried items: 8.

### reference-semantics/semantics/range.k:9 — item 1 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### reference-semantics/semantics/range.k:10 — item 2 (`rule`, `rule/ordinary`)

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### reference-semantics/semantics/range.k:12 — item 3 (`syntax`, `syntax/function`)

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### reference-semantics/semantics/range.k:13 — item 4 (`rule`, `rule/ordinary`)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
```

### reference-semantics/semantics/range.k:15 — item 5 (`rule`, `rule/ordinary`)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
```

### reference-semantics/semantics/range.k:17 — item 6 (`rule`, `rule/ordinary`)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
```

### reference-semantics/semantics/range.k:20-21 — item 7 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
```

### reference-semantics/semantics/range.k:23 — item 8 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
```

## `reference-semantics/semantics/set.k`

SHA-256: `b822c3c6944f9940a4477fa6b7a42490c407663f2a314394e9c146e8951f1ac7`. Inventoried items: 18.

### reference-semantics/semantics/set.k:8 — item 1 (`syntax`, `syntax`)

```k
  syntax Val ::= setV(IntSeq)
```

### reference-semantics/semantics/set.k:11 — item 2 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### reference-semantics/semantics/set.k:12 — item 3 (`rule`, `rule/ordinary`)

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### reference-semantics/semantics/set.k:13 — item 4 (`rule`, `rule/ordinary`)

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### reference-semantics/semantics/set.k:16-17 — item 5 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### reference-semantics/semantics/set.k:18 — item 6 (`rule`, `rule/ordinary`)

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### reference-semantics/semantics/set.k:19 — item 7 (`rule`, `rule/ordinary`)

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### reference-semantics/semantics/set.k:20 — item 8 (`rule`, `rule/ordinary`)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
```

### reference-semantics/semantics/set.k:22 — item 9 (`rule`, `rule/ordinary`)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
```

### reference-semantics/semantics/set.k:25 — item 10 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### reference-semantics/semantics/set.k:26 — item 11 (`rule`, `rule/ordinary`)

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### reference-semantics/semantics/set.k:27 — item 12 (`rule`, `rule/ordinary`)

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### reference-semantics/semantics/set.k:31 — item 13 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/set.k:32 — item 14 (`rule`, `rule/ordinary`)

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### reference-semantics/semantics/set.k:33 — item 15 (`rule`, `rule/ordinary`)

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### reference-semantics/semantics/set.k:35 — item 16 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/set.k:36 — item 17 (`rule`, `rule/ordinary`)

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### reference-semantics/semantics/set.k:39 — item 18 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## `reference-semantics/semantics/sort.k`

SHA-256: `df79670e4794a92e96ffc824857fbc34d3a65b6b6a3026d1dcf322128fbaba5a`. Inventoried items: 25.

### reference-semantics/semantics/sort.k:18 — item 1 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### reference-semantics/semantics/sort.k:19 — item 2 (`syntax`, `syntax/function`)

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### reference-semantics/semantics/sort.k:20 — item 3 (`rule`, `rule/concrete`)

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### reference-semantics/semantics/sort.k:21 — item 4 (`rule`, `rule/concrete`)

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### reference-semantics/semantics/sort.k:22 — item 5 (`rule`, `rule/concrete`)

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### reference-semantics/semantics/sort.k:23 — item 6 (`rule`, `rule/concrete`)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### reference-semantics/semantics/sort.k:24 — item 7 (`rule`, `rule/concrete`)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### reference-semantics/semantics/sort.k:26 — item 8 (`syntax`, `syntax/function`)

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### reference-semantics/semantics/sort.k:27 — item 9 (`rule`, `rule/concrete`)

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### reference-semantics/semantics/sort.k:28 — item 10 (`rule`, `rule/concrete`)

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### reference-semantics/semantics/sort.k:29 — item 11 (`rule`, `rule/ordinary`)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
```

### reference-semantics/semantics/sort.k:31 — item 12 (`rule`, `rule/ordinary`)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
```

### reference-semantics/semantics/sort.k:36-37 — item 13 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

### reference-semantics/semantics/sort.k:40-42 — item 14 (`rule`, `rule/priority`)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/sort.k:49 — item 15 (`syntax`, `syntax/function,total,symbol,no-evaluators`)

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### reference-semantics/semantics/sort.k:51-52 — item 16 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### reference-semantics/semantics/sort.k:53 — item 17 (`rule`, `rule/ordinary`)

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### reference-semantics/semantics/sort.k:54 — item 18 (`rule`, `rule/ordinary`)

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### reference-semantics/semantics/sort.k:55 — item 19 (`rule`, `rule/ordinary`)

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### reference-semantics/semantics/sort.k:57 — item 20 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### reference-semantics/semantics/sort.k:58 — item 21 (`rule`, `rule/ordinary`)

```k
  rule condRev(S:ValSeq, false) => S
```

### reference-semantics/semantics/sort.k:59 — item 22 (`rule`, `rule/ordinary`)

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### reference-semantics/semantics/sort.k:61-62 — item 23 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### reference-semantics/semantics/sort.k:63-64 — item 24 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### reference-semantics/semantics/sort.k:65-66 — item 25 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

## `reference-semantics/semantics/str.k`

SHA-256: `1bf0abf61d7c5df6301433a89c79d2ef4259d47a68d98385ff74618c4c310e0f`. Inventoried items: 33.

### reference-semantics/semantics/str.k:8 — item 1 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### reference-semantics/semantics/str.k:9-10 — item 2 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### reference-semantics/semantics/str.k:13 — item 3 (`syntax`, `syntax/function`)

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### reference-semantics/semantics/str.k:14 — item 4 (`rule`, `rule/ordinary`)

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### reference-semantics/semantics/str.k:15 — item 5 (`rule`, `rule/ordinary`)

```k
  rule strToCodes("") => .IntSeq
```

### reference-semantics/semantics/str.k:16 — item 6 (`rule`, `rule/ordinary`)

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
```

### reference-semantics/semantics/str.k:20 — item 7 (`syntax`, `syntax/function,total`)

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:21 — item 8 (`rule`, `rule/ordinary`)

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### reference-semantics/semantics/str.k:22 — item 9 (`rule`, `rule/ordinary`)

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### reference-semantics/semantics/str.k:24 — item 10 (`rule`, `rule/ordinary`)

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### reference-semantics/semantics/str.k:25 — item 11 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### reference-semantics/semantics/str.k:26 — item 12 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### reference-semantics/semantics/str.k:29 — item 13 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### reference-semantics/semantics/str.k:30 — item 14 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### reference-semantics/semantics/str.k:32 — item 15 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:33 — item 16 (`rule`, `rule/ordinary`)

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### reference-semantics/semantics/str.k:34 — item 17 (`rule`, `rule/ordinary`)

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### reference-semantics/semantics/str.k:35 — item 18 (`rule`, `rule/ordinary`)

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### reference-semantics/semantics/str.k:37 — item 19 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:38 — item 20 (`rule`, `rule/ordinary`)

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### reference-semantics/semantics/str.k:39 — item 21 (`rule`, `rule/ordinary`)

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### reference-semantics/semantics/str.k:40 — item 22 (`rule`, `rule/ordinary`)

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
```

### reference-semantics/semantics/str.k:48 — item 23 (`syntax`, `syntax/function,total`)

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### reference-semantics/semantics/str.k:49 — item 24 (`rule`, `rule/ordinary`)

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### reference-semantics/semantics/str.k:50 — item 25 (`rule`, `rule/ordinary`)

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### reference-semantics/semantics/str.k:51 — item 26 (`rule`, `rule/ordinary`)

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### reference-semantics/semantics/str.k:52 — item 27 (`rule`, `rule/ordinary`)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### reference-semantics/semantics/str.k:53 — item 28 (`rule`, `rule/ordinary`)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### reference-semantics/semantics/str.k:54 — item 29 (`rule`, `rule/ordinary`)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### reference-semantics/semantics/str.k:56 — item 30 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### reference-semantics/semantics/str.k:57 — item 31 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### reference-semantics/semantics/str.k:58 — item 32 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### reference-semantics/semantics/str.k:59 — item 33 (`rule`, `rule/ordinary`)

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## `reference-semantics/semantics/subscript.k`

SHA-256: `dba04c0acf213bef4f9f7b11243ca00a2b3ca5fa8666c544ede7d382d27d36a7`. Inventoried items: 57.

### reference-semantics/semantics/subscript.k:11 — item 1 (`syntax`, `syntax/function,total`)

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:12 — item 2 (`rule`, `rule/ordinary`)

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### reference-semantics/semantics/subscript.k:13 — item 3 (`rule`, `rule/ordinary`)

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
```

### reference-semantics/semantics/subscript.k:16 — item 4 (`syntax`, `syntax/function`)

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### reference-semantics/semantics/subscript.k:17 — item 5 (`rule`, `rule/ordinary`)

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### reference-semantics/semantics/subscript.k:18 — item 6 (`rule`, `rule/ordinary`)

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
```

### reference-semantics/semantics/subscript.k:21 — item 7 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:22 — item 8 (`rule`, `rule/ordinary`)

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### reference-semantics/semantics/subscript.k:23 — item 9 (`rule`, `rule/ordinary`)

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### reference-semantics/semantics/subscript.k:27 — item 10 (`context`, `context`)

```k
  context Subscript(HOLE, _)
```

### reference-semantics/semantics/subscript.k:28 — item 11 (`context`, `context`)

```k
  context Subscript(_:Val, HOLE:Expr)
```

### reference-semantics/semantics/subscript.k:31-33 — item 12 (`rule`, `rule/priority`)

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/subscript.k:35 — item 13 (`rule`, `rule/ordinary`)

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### reference-semantics/semantics/subscript.k:37 — item 14 (`syntax`, `syntax/function`)

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### reference-semantics/semantics/subscript.k:38 — item 15 (`rule`, `rule/ordinary`)

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### reference-semantics/semantics/subscript.k:39 — item 16 (`rule`, `rule/ordinary`)

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### reference-semantics/semantics/subscript.k:40-41 — item 17 (`rule`, `rule/ordinary`)

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### reference-semantics/semantics/subscript.k:44-47 — item 18 (`syntax`, `syntax`)

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### reference-semantics/semantics/subscript.k:49 — item 19 (`syntax`, `syntax`)

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### reference-semantics/semantics/subscript.k:50 — item 20 (`rule`, `rule/ordinary`)

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### reference-semantics/semantics/subscript.k:51 — item 21 (`rule`, `rule/ordinary`)

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### reference-semantics/semantics/subscript.k:52 — item 22 (`rule`, `rule/ordinary`)

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### reference-semantics/semantics/subscript.k:54 — item 23 (`rule`, `rule/ordinary`)

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### reference-semantics/semantics/subscript.k:55 — item 24 (`rule`, `rule/ordinary`)

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### reference-semantics/semantics/subscript.k:56 — item 25 (`rule`, `rule/ordinary`)

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### reference-semantics/semantics/subscript.k:58-60 — item 26 (`rule`, `rule/priority`)

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### reference-semantics/semantics/subscript.k:61 — item 27 (`rule`, `rule/ordinary`)

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### reference-semantics/semantics/subscript.k:63 — item 28 (`syntax`, `syntax/function`)

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### reference-semantics/semantics/subscript.k:64-65 — item 29 (`rule`, `rule/ordinary`)

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### reference-semantics/semantics/subscript.k:66-67 — item 30 (`rule`, `rule/ordinary`)

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### reference-semantics/semantics/subscript.k:68-69 — item 31 (`rule`, `rule/ordinary`)

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### reference-semantics/semantics/subscript.k:72 — item 32 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### reference-semantics/semantics/subscript.k:73 — item 33 (`rule`, `rule/ordinary`)

```k
  rule slStep(noB)          => 1
```

### reference-semantics/semantics/subscript.k:74 — item 34 (`rule`, `rule/ordinary`)

```k
  rule slStep(someB(S:Int)) => S
```

### reference-semantics/semantics/subscript.k:76 — item 35 (`syntax`, `syntax/function`)

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### reference-semantics/semantics/subscript.k:77 — item 36 (`rule`, `rule/ordinary`)

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
```

### reference-semantics/semantics/subscript.k:79 — item 37 (`rule`, `rule/ordinary`)

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
```

### reference-semantics/semantics/subscript.k:81 — item 38 (`rule`, `rule/ordinary`)

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### reference-semantics/semantics/subscript.k:83 — item 39 (`syntax`, `syntax/function`)

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### reference-semantics/semantics/subscript.k:84 — item 40 (`rule`, `rule/ordinary`)

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
```

### reference-semantics/semantics/subscript.k:86 — item 41 (`rule`, `rule/ordinary`)

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
```

### reference-semantics/semantics/subscript.k:88 — item 42 (`rule`, `rule/ordinary`)

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### reference-semantics/semantics/subscript.k:90 — item 43 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:91 — item 44 (`rule`, `rule/ordinary`)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
```

### reference-semantics/semantics/subscript.k:93 — item 45 (`rule`, `rule/ordinary`)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
```

### reference-semantics/semantics/subscript.k:96 — item 46 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:97 — item 47 (`rule`, `rule/ordinary`)

```k
  rule clampLo(J:Int, _STEP:Int) => J
```

### reference-semantics/semantics/subscript.k:99 — item 48 (`rule`, `rule/ordinary`)

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
```

### reference-semantics/semantics/subscript.k:102 — item 49 (`syntax`, `syntax/function,total`)

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### reference-semantics/semantics/subscript.k:103 — item 50 (`rule`, `rule/ordinary`)

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
```

### reference-semantics/semantics/subscript.k:105 — item 51 (`rule`, `rule/ordinary`)

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
```

### reference-semantics/semantics/subscript.k:109 — item 52 (`syntax`, `syntax/function`)

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### reference-semantics/semantics/subscript.k:110-111 — item 53 (`rule`, `rule/ordinary`)

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
```

### reference-semantics/semantics/subscript.k:113 — item 54 (`rule`, `rule/ordinary`)

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
```

### reference-semantics/semantics/subscript.k:116 — item 55 (`syntax`, `syntax/function`)

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### reference-semantics/semantics/subscript.k:117-118 — item 56 (`rule`, `rule/ordinary`)

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
```

### reference-semantics/semantics/subscript.k:120 — item 57 (`rule`, `rule/ordinary`)

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
```

## `reference-semantics/semantics/syntax.k`

SHA-256: `1e9e629e5e6e14bdd7f4d530375e8655a89366b5ecd0c24a3c57ad3b5708f2a6`. Inventoried items: 16.

### reference-semantics/semantics/syntax.k:9-30 — item 1 (`syntax`, `syntax/macro,strict,seqstrict`)

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

### reference-semantics/semantics/syntax.k:32 — item 2 (`syntax`, `syntax`)

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### reference-semantics/semantics/syntax.k:33 — item 3 (`syntax`, `syntax`)

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### reference-semantics/semantics/syntax.k:34 — item 4 (`syntax`, `syntax`)

```k
  syntax Entries  ::= List{Entry, ","}
```

### reference-semantics/semantics/syntax.k:35 — item 5 (`syntax`, `syntax`)

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### reference-semantics/semantics/syntax.k:36 — item 6 (`syntax`, `syntax`)

```k
  syntax CompFors ::= List{CompFor, ""}
```

### reference-semantics/semantics/syntax.k:37 — item 7 (`syntax`, `syntax`)

```k
  syntax Exprs    ::= List{Expr, ","}
```

### reference-semantics/semantics/syntax.k:38 — item 8 (`syntax`, `syntax`)

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### reference-semantics/semantics/syntax.k:39 — item 9 (`syntax`, `syntax`)

```k
  syntax Bound    ::= Expr | "NoBound"
```

### reference-semantics/semantics/syntax.k:41-54 — item 10 (`syntax`, `syntax/strict`)

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

### reference-semantics/semantics/syntax.k:56 — item 11 (`syntax`, `syntax`)

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### reference-semantics/semantics/syntax.k:57 — item 12 (`syntax`, `syntax`)

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### reference-semantics/semantics/syntax.k:58 — item 13 (`syntax`, `syntax`)

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### reference-semantics/semantics/syntax.k:59 — item 14 (`syntax`, `syntax`)

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### reference-semantics/semantics/syntax.k:60 — item 15 (`syntax`, `syntax`)

```k
  syntax ParamNames ::= List{String, ","}
```

### reference-semantics/semantics/syntax.k:61 — item 16 (`syntax`, `syntax`)

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## `reference-semantics/semantics/tuple.k`

SHA-256: `41395a1ec6a58129c78facb15b44206907c54d79e86ea363ae68cb37bfc64abb`. Inventoried items: 25.

### reference-semantics/semantics/tuple.k:10 — item 1 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### reference-semantics/semantics/tuple.k:11 — item 2 (`rule`, `rule/ordinary`)

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### reference-semantics/semantics/tuple.k:14 — item 3 (`syntax`, `syntax`)

```k
  syntax ApplyK ::= "toTuple"
```

### reference-semantics/semantics/tuple.k:15 — item 4 (`rule`, `rule/ordinary`)

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### reference-semantics/semantics/tuple.k:16 — item 5 (`rule`, `rule/ordinary`)

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### reference-semantics/semantics/tuple.k:18 — item 6 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### reference-semantics/semantics/tuple.k:20 — item 7 (`rule`, `rule/ordinary`)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### reference-semantics/semantics/tuple.k:21 — item 8 (`rule`, `rule/ordinary`)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### reference-semantics/semantics/tuple.k:23 — item 9 (`rule`, `rule/ordinary`)

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### reference-semantics/semantics/tuple.k:24 — item 10 (`syntax`, `syntax/function`)

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### reference-semantics/semantics/tuple.k:25 — item 11 (`rule`, `rule/ordinary`)

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### reference-semantics/semantics/tuple.k:26 — item 12 (`rule`, `rule/ordinary`)

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
```

### reference-semantics/semantics/tuple.k:28 — item 13 (`rule`, `rule/ordinary`)

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### reference-semantics/semantics/tuple.k:31 — item 14 (`syntax`, `syntax`)

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### reference-semantics/semantics/tuple.k:32-34 — item 15 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### reference-semantics/semantics/tuple.k:35-37 — item 16 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
```

### reference-semantics/semantics/tuple.k:42 — item 17 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:43 — item 18 (`rule`, `rule/ordinary`)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:44-46 — item 19 (`rule`, `rule/priority`)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/tuple.k:49 — item 20 (`syntax`, `syntax`)

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### reference-semantics/semantics/tuple.k:50 — item 21 (`rule`, `rule/ordinary`)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:51 — item 22 (`rule`, `rule/ordinary`)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:52-54 — item 23 (`rule`, `rule/priority`)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### reference-semantics/semantics/tuple.k:55-56 — item 24 (`rule`, `rule/ordinary`)

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### reference-semantics/semantics/tuple.k:57 — item 25 (`rule`, `rule/ordinary`)

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## `reference-semantics/semantics.k`

SHA-256: `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`. Inventoried items: 0.

## `verification.k`

SHA-256: `592016f3ca06f1bf04f938cf3505227b1d1aa08f121bde55e6134547ae5a9b4d`. Inventoried items: 14.

### verification.k:8 — item 1 (`syntax`, `syntax/function,total`)

```k
  syntax ValSeq ::= intVals(IntSeq) [function, total]
```

### verification.k:9 — item 2 (`rule`, `rule/ordinary`)

```k
  rule intVals(.IntSeq)                => .ValSeq
```

### verification.k:10 — item 3 (`rule`, `rule/ordinary`)

```k
  rule intVals(iCons(I:Int, R:IntSeq)) => vCons(I, intVals(R))
```

### verification.k:14 — item 4 (`syntax`, `syntax/function`)

```k
  syntax ValSeq ::= absDiffs(ValSeq, ValSeq) [function]
```

### verification.k:15 — item 5 (`rule`, `rule/ordinary`)

```k
  rule absDiffs(.ValSeq, _:ValSeq) => .ValSeq
```

### verification.k:16 — item 6 (`rule`, `rule/ordinary`)

```k
  rule absDiffs(vCons(_:Int, _:ValSeq), .ValSeq) => .ValSeq
```

### verification.k:17-18 — item 7 (`rule`, `rule/ordinary`)

```k
  rule absDiffs(vCons(A:Int, AS:ValSeq), vCons(B:Int, BS:ValSeq))
    => vCons(absInt(A -Int B), absDiffs(AS, BS))
```

### verification.k:21 — item 8 (`syntax`, `syntax/macro`)

```k
  syntax Stmts ::= "appendBody" [macro]
```

### verification.k:22-26 — item 9 (`rule`, `rule/ordinary`)

```k
  rule appendBody
    => Expr(
         Call(
           Attribute(Name("result"), "append"),
           Call(Name("abs"), BinOp("-", Name("score"), Name("prediction")))))
```

### verification.k:28 — item 10 (`syntax`, `syntax/macro`)

```k
  syntax Stmts ::= "compareBody" [macro]
```

### verification.k:29-36 — item 11 (`rule`, `rule/ordinary`)

```k
  rule compareBody
    => Expr(Str("Return the absolute error for each corresponding score and guess."))
       Assign(Name("result"), ListExpr(.Exprs))
       For(
         TupleExpr(Name("score"), Name("prediction")),
         Call(Name("zip"), Name("game"), Name("guess")),
         appendBody)
       Return(Name("result"))
```

### verification.k:38 — item 12 (`syntax`, `syntax/macro`)

```k
  syntax Stmt ::= "compareDef" [macro]
```

### verification.k:39-40 — item 13 (`rule`, `rule/ordinary`)

```k
  rule compareDef
    => FuncDef("compare", Params("game", "guess"), compareBody)
```

### verification.k:50-64 — item 14 (`rule`, `rule/ordinary`)

```k
  rule <k>
         #loop(
           zipObj(GAME:ValSeq, GUESS:ValSeq),
           TupleExpr(Name("score"), Name("prediction")),
           appendBody)
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap>
         ... H:Int |-> list(
              ACC:ValSeq
              => valSeqConcat(ACC, absDiffs(GAME, GUESS))) ...
       </heap>
```

## `spec.k`

SHA-256: `81b43a7920c7cf8f396ba2b67682dcdc3a146cbbe467be89f03b68a140da14e8`. Inventoried items: 3.

### spec.k:9-40 — item 1 (`claim`, `claim`)

```k
  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(intVals(GAME:IntSeq)),
           list(intVals(GUESS:IntSeq)))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(absDiffs(intVals(GAME), intVals(GUESS)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### spec.k:43-74 — item 2 (`claim`, `claim`)

```k
  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(vCons(1, vCons(2, vCons(3, vCons(4, vCons(5, vCons(1, .ValSeq))))))),
           list(vCons(1, vCons(2, vCons(3, vCons(4, vCons(2, vCons(-2, .ValSeq))))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(0, vCons(0, vCons(0, vCons(0, vCons(3, vCons(3, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### spec.k:76-107 — item 3 (`claim`, `claim`)

```k
  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(vCons(0, vCons(5, vCons(0, vCons(0, vCons(0, vCons(4, .ValSeq))))))),
           list(vCons(4, vCons(1, vCons(1, vCons(0, vCons(0, vCons(-2, .ValSeq))))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(4, vCons(4, vCons(1, vCons(0, vCons(0, vCons(6, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

## `operational-spec.k`

SHA-256: `08534b9872ff4faad2cc600fb98fa74c0d208308953cc85f0b8bdc09e190d834`. Inventoried items: 4.

### operational-spec.k:9-40 — item 1 (`claim`, `claim`)

```k
  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(vCons(1, vCons(2, vCons(3, vCons(4, vCons(5, vCons(1, .ValSeq))))))),
           list(vCons(1, vCons(2, vCons(3, vCons(4, vCons(2, vCons(-2, .ValSeq))))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(0, vCons(0, vCons(0, vCons(0, vCons(3, vCons(3, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### operational-spec.k:42-73 — item 2 (`claim`, `claim`)

```k
  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(vCons(0, vCons(5, vCons(0, vCons(0, vCons(0, vCons(4, .ValSeq))))))),
           list(vCons(4, vCons(1, vCons(1, vCons(0, vCons(0, vCons(-2, .ValSeq))))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(4, vCons(4, vCons(1, vCons(0, vCons(0, vCons(6, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### operational-spec.k:75-99 — item 3 (`claim`, `claim`)

```k
  claim
    <k>
      compareDef
      ~> Call(Name("compare"), list(.ValSeq), list(.ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### operational-spec.k:101-132 — item 4 (`claim`, `claim`)

```k
  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(vCons(-7, vCons(9, .ValSeq))),
           list(vCons(5, vCons(-4, .ValSeq))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(12, vCons(13, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

## Inventory totals

Files: 27

- `claim`: 7
- `configuration`: 1
- `context`: 5
- `rule/concrete`: 32
- `rule/ordinary`: 617
- `rule/owise`: 26
- `rule/priority`: 29
- `syntax`: 76
- `syntax/function`: 38
- `syntax/function,token`: 2
- `syntax/function,total`: 83
- `syntax/function,total,symbol`: 3
- `syntax/function,total,symbol,no-evaluators`: 22
- `syntax/macro`: 5
- `syntax/macro,strict,seqstrict`: 1
- `syntax/macro-rec,macro`: 1
- `syntax/strict`: 1

# Exhaustive K source inventory

Generated from fresh trusted-semantics scratch sources. Each top-level K declaration,
configuration, context, rule, and claim is reproduced with its source line span.

## `reference-semantics/semantics.k`

## `reference-semantics/semantics/assert.k`

### rule at `reference-semantics/semantics/assert.k:6` (through line 7)

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### rule at `reference-semantics/semantics/assert.k:8` (through line 11)

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### rule at `reference-semantics/semantics/assert.k:13` (through line 15)

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/bool.k`

### rule at `reference-semantics/semantics/bool.k:8` (through line 8)

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### rule at `reference-semantics/semantics/bool.k:10` (through line 10)

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### rule at `reference-semantics/semantics/bool.k:11` (through line 15)

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### context at `reference-semantics/semantics/bool.k:16` (through line 16)

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### rule at `reference-semantics/semantics/bool.k:17` (through line 17)

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### rule at `reference-semantics/semantics/bool.k:18` (through line 19)

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### rule at `reference-semantics/semantics/bool.k:20` (through line 21)

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### rule at `reference-semantics/semantics/bool.k:22` (through line 23)

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### rule at `reference-semantics/semantics/bool.k:24` (through line 28)

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

### rule at `reference-semantics/semantics/bool.k:29` (through line 30)

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### rule at `reference-semantics/semantics/bool.k:31` (through line 34)

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### rule at `reference-semantics/semantics/bool.k:35` (through line 38)

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### rule at `reference-semantics/semantics/bool.k:39` (through line 42)

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### rule at `reference-semantics/semantics/bool.k:43` (through line 46)

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## `reference-semantics/semantics/builtins.k`

### syntax at `reference-semantics/semantics/builtins.k:17` (through line 19)

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### syntax at `reference-semantics/semantics/builtins.k:20` (through line 20)

```k
  syntax Int ::= seqLen(Val) [function]
```

### rule at `reference-semantics/semantics/builtins.k:21` (through line 21)

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### rule at `reference-semantics/semantics/builtins.k:22` (through line 22)

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### rule at `reference-semantics/semantics/builtins.k:23` (through line 23)

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### rule at `reference-semantics/semantics/builtins.k:24` (through line 24)

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### rule at `reference-semantics/semantics/builtins.k:25` (through line 25)

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### rule at `reference-semantics/semantics/builtins.k:26` (through line 31)

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### rule at `reference-semantics/semantics/builtins.k:32` (through line 32)

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:33` (through line 33)

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:34` (through line 34)

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:35` (through line 35)

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### syntax at `reference-semantics/semantics/builtins.k:36` (through line 36)

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:37` (through line 37)

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### rule at `reference-semantics/semantics/builtins.k:38` (through line 40)

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### rule at `reference-semantics/semantics/builtins.k:41` (through line 43)

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### rule at `reference-semantics/semantics/builtins.k:44` (through line 46)

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### syntax at `reference-semantics/semantics/builtins.k:47` (through line 47)

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### rule at `reference-semantics/semantics/builtins.k:48` (through line 48)

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:49` (through line 49)

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:50` (through line 52)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### syntax at `reference-semantics/semantics/builtins.k:54` (through line 54)

```k
  syntax Int ::= intOf(Val) [function]
```

### rule at `reference-semantics/semantics/builtins.k:55` (through line 55)

```k
  rule intOf(I:Int)  => I
```

### rule at `reference-semantics/semantics/builtins.k:56` (through line 58)

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### syntax at `reference-semantics/semantics/builtins.k:59` (through line 59)

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### rule at `reference-semantics/semantics/builtins.k:60` (through line 60)

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:61` (through line 61)

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:62` (through line 63)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### rule at `reference-semantics/semantics/builtins.k:64` (through line 65)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### syntax at `reference-semantics/semantics/builtins.k:67` (through line 67)

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### rule at `reference-semantics/semantics/builtins.k:68` (through line 68)

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:69` (through line 69)

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:70` (through line 71)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### rule at `reference-semantics/semantics/builtins.k:72` (through line 75)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

### syntax at `reference-semantics/semantics/builtins.k:76` (through line 76)

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### rule at `reference-semantics/semantics/builtins.k:77` (through line 77)

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:78` (through line 79)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### rule at `reference-semantics/semantics/builtins.k:80` (through line 80)

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:81` (through line 81)

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:82` (through line 84)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### syntax at `reference-semantics/semantics/builtins.k:86` (through line 86)

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### rule at `reference-semantics/semantics/builtins.k:87` (through line 87)

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:88` (through line 89)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### rule at `reference-semantics/semantics/builtins.k:90` (through line 90)

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:91` (through line 91)

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:92` (through line 96)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

### syntax at `reference-semantics/semantics/builtins.k:97` (through line 97)

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### rule at `reference-semantics/semantics/builtins.k:98` (through line 98)

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### rule at `reference-semantics/semantics/builtins.k:99` (through line 99)

```k
  rule maxVals(M:Int, .Vals)           => M
```

### rule at `reference-semantics/semantics/builtins.k:100` (through line 100)

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### syntax at `reference-semantics/semantics/builtins.k:102` (through line 102)

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### rule at `reference-semantics/semantics/builtins.k:103` (through line 103)

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### rule at `reference-semantics/semantics/builtins.k:104` (through line 104)

```k
  rule minVals(M:Int, .Vals)           => M
```

### rule at `reference-semantics/semantics/builtins.k:105` (through line 107)

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### rule at `reference-semantics/semantics/builtins.k:108` (through line 110)

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

### rule at `reference-semantics/semantics/builtins.k:111` (through line 113)

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### syntax at `reference-semantics/semantics/builtins.k:114` (through line 114)

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:115` (through line 115)

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### rule at `reference-semantics/semantics/builtins.k:116` (through line 116)

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### syntax at `reference-semantics/semantics/builtins.k:117` (through line 117)

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:118` (through line 118)

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### rule at `reference-semantics/semantics/builtins.k:119` (through line 123)

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

### rule at `reference-semantics/semantics/builtins.k:124` (through line 125)

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### syntax at `reference-semantics/semantics/builtins.k:126` (through line 126)

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:127` (through line 127)

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### rule at `reference-semantics/semantics/builtins.k:128` (through line 131)

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### rule at `reference-semantics/semantics/builtins.k:132` (through line 133)

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### syntax at `reference-semantics/semantics/builtins.k:134` (through line 134)

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:135` (through line 135)

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### rule at `reference-semantics/semantics/builtins.k:136` (through line 136)

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### rule at `reference-semantics/semantics/builtins.k:137` (through line 139)

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### rule at `reference-semantics/semantics/builtins.k:140` (through line 142)

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### rule at `reference-semantics/semantics/builtins.k:143` (through line 143)

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### rule at `reference-semantics/semantics/builtins.k:144` (through line 147)

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

### rule at `reference-semantics/semantics/builtins.k:148` (through line 148)

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### rule at `reference-semantics/semantics/builtins.k:149` (through line 151)

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### rule at `reference-semantics/semantics/builtins.k:152` (through line 155)

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

### rule at `reference-semantics/semantics/builtins.k:156` (through line 157)

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### syntax at `reference-semantics/semantics/builtins.k:158` (through line 158)

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:159` (through line 159)

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### rule at `reference-semantics/semantics/builtins.k:160` (through line 162)

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### rule at `reference-semantics/semantics/builtins.k:163` (through line 163)

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### rule at `reference-semantics/semantics/builtins.k:164` (through line 166)

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### rule at `reference-semantics/semantics/builtins.k:167` (through line 168)

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:169` (through line 169)

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:170` (through line 170)

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:171` (through line 172)

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:173` (through line 173)

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### rule at `reference-semantics/semantics/builtins.k:174` (through line 176)

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### rule at `reference-semantics/semantics/builtins.k:177` (through line 177)

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### rule at `reference-semantics/semantics/builtins.k:178` (through line 178)

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### rule at `reference-semantics/semantics/builtins.k:179` (through line 186)

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0

  // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
  // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
  // trusted pass evaluator, now DEFINED in the reference and driven by a
  // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
  // argument leaves the call unevaluated for problem-level folds.
```

### rule at `reference-semantics/semantics/builtins.k:187` (through line 187)

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### syntax at `reference-semantics/semantics/builtins.k:188` (through line 188)

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### rule at `reference-semantics/semantics/builtins.k:189` (through line 190)

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### syntax at `reference-semantics/semantics/builtins.k:192` (through line 192)

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### syntax at `reference-semantics/semantics/builtins.k:194` (through line 194)

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:195` (through line 195)

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### syntax at `reference-semantics/semantics/builtins.k:196` (through line 196)

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:197` (through line 197)

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### rule at `reference-semantics/semantics/builtins.k:198` (through line 198)

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### syntax at `reference-semantics/semantics/builtins.k:199` (through line 199)

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:200` (through line 200)

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### rule at `reference-semantics/semantics/builtins.k:201` (through line 201)

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### syntax at `reference-semantics/semantics/builtins.k:203` (through line 203)

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:204` (through line 204)

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### rule at `reference-semantics/semantics/builtins.k:205` (through line 205)

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### rule at `reference-semantics/semantics/builtins.k:206` (through line 206)

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### rule at `reference-semantics/semantics/builtins.k:207` (through line 207)

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### rule at `reference-semantics/semantics/builtins.k:208` (through line 208)

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### rule at `reference-semantics/semantics/builtins.k:209` (through line 209)

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### rule at `reference-semantics/semantics/builtins.k:210` (through line 210)

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### rule at `reference-semantics/semantics/builtins.k:211` (through line 211)

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### rule at `reference-semantics/semantics/builtins.k:212` (through line 212)

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### syntax at `reference-semantics/semantics/builtins.k:214` (through line 215)

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:216` (through line 216)

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### rule at `reference-semantics/semantics/builtins.k:217` (through line 217)

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### rule at `reference-semantics/semantics/builtins.k:218` (through line 218)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### rule at `reference-semantics/semantics/builtins.k:219` (through line 220)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### rule at `reference-semantics/semantics/builtins.k:221` (through line 222)

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### rule at `reference-semantics/semantics/builtins.k:223` (through line 223)

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### syntax at `reference-semantics/semantics/builtins.k:225` (through line 225)

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### syntax at `reference-semantics/semantics/builtins.k:226` (through line 226)

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:227` (through line 227)

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### rule at `reference-semantics/semantics/builtins.k:228` (through line 228)

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### syntax at `reference-semantics/semantics/builtins.k:230` (through line 230)

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:231` (through line 231)

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### rule at `reference-semantics/semantics/builtins.k:232` (through line 232)

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### rule at `reference-semantics/semantics/builtins.k:233` (through line 233)

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### rule at `reference-semantics/semantics/builtins.k:234` (through line 234)

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### rule at `reference-semantics/semantics/builtins.k:235` (through line 235)

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### rule at `reference-semantics/semantics/builtins.k:236` (through line 236)

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### syntax at `reference-semantics/semantics/builtins.k:238` (through line 238)

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:239` (through line 239)

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### rule at `reference-semantics/semantics/builtins.k:240` (through line 240)

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### rule at `reference-semantics/semantics/builtins.k:241` (through line 242)

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### rule at `reference-semantics/semantics/builtins.k:243` (through line 243)

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### syntax at `reference-semantics/semantics/builtins.k:244` (through line 244)

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:245` (through line 245)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### rule at `reference-semantics/semantics/builtins.k:246` (through line 246)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### syntax at `reference-semantics/semantics/builtins.k:247` (through line 247)

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:248` (through line 248)

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### syntax at `reference-semantics/semantics/builtins.k:250` (through line 250)

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:251` (through line 251)

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### rule at `reference-semantics/semantics/builtins.k:252` (through line 252)

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### rule at `reference-semantics/semantics/builtins.k:253` (through line 253)

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### rule at `reference-semantics/semantics/builtins.k:254` (through line 254)

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### syntax at `reference-semantics/semantics/builtins.k:255` (through line 255)

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:256` (through line 256)

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### rule at `reference-semantics/semantics/builtins.k:257` (through line 259)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### rule at `reference-semantics/semantics/builtins.k:260` (through line 262)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### rule at `reference-semantics/semantics/builtins.k:263` (through line 264)

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### syntax at `reference-semantics/semantics/builtins.k:265` (through line 265)

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:266` (through line 266)

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### rule at `reference-semantics/semantics/builtins.k:267` (through line 267)

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### rule at `reference-semantics/semantics/builtins.k:268` (through line 268)

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### syntax at `reference-semantics/semantics/builtins.k:269` (through line 269)

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:270` (through line 270)

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### rule at `reference-semantics/semantics/builtins.k:271` (through line 271)

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### syntax at `reference-semantics/semantics/builtins.k:272` (through line 272)

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### rule at `reference-semantics/semantics/builtins.k:273` (through line 273)

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### rule at `reference-semantics/semantics/builtins.k:274` (through line 278)

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### syntax at `reference-semantics/semantics/builtins.k:279` (through line 279)

```k
  syntax KItem ::= "#md5"
```

### rule at `reference-semantics/semantics/builtins.k:280` (through line 281)

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### rule at `reference-semantics/semantics/builtins.k:282` (through line 282)

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### syntax at `reference-semantics/semantics/builtins.k:283` (through line 283)

```k
  syntax Val ::= md5Obj(IntSeq)
```

### rule at `reference-semantics/semantics/builtins.k:284` (through line 284)

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### syntax at `reference-semantics/semantics/builtins.k:285` (through line 290)

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### rule at `reference-semantics/semantics/builtins.k:291` (through line 291)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### rule at `reference-semantics/semantics/builtins.k:292` (through line 292)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### syntax at `reference-semantics/semantics/builtins.k:293` (through line 293)

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### rule at `reference-semantics/semantics/builtins.k:294` (through line 294)

```k
  rule isIntV(_:Int)         => true
```

### rule at `reference-semantics/semantics/builtins.k:295` (through line 295)

```k
  rule isIntV(_:Val)         => false [owise]
```

### rule at `reference-semantics/semantics/builtins.k:296` (through line 296)

```k
  rule isStrV(str(_:IntSeq)) => true
```

### rule at `reference-semantics/semantics/builtins.k:297` (through line 297)

```k
  rule isStrV(_:Val)         => false [owise]
```

## `reference-semantics/semantics/call.k`

### rule at `reference-semantics/semantics/call.k:16` (through line 18)

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### syntax at `reference-semantics/semantics/call.k:19` (through line 19)

```k
  syntax KItem ::= #callee(Exprs)
```

### rule at `reference-semantics/semantics/call.k:20` (through line 20)

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### rule at `reference-semantics/semantics/call.k:21` (through line 23)

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### rule at `reference-semantics/semantics/call.k:24` (through line 24)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### rule at `reference-semantics/semantics/call.k:26` (through line 26)

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### rule at `reference-semantics/semantics/call.k:27` (through line 27)

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### rule at `reference-semantics/semantics/call.k:28` (through line 28)

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### rule at `reference-semantics/semantics/call.k:29` (through line 29)

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### rule at `reference-semantics/semantics/call.k:30` (through line 30)

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### rule at `reference-semantics/semantics/call.k:31` (through line 31)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### rule at `reference-semantics/semantics/call.k:32` (through line 37)

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### rule at `reference-semantics/semantics/call.k:38` (through line 41)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at `reference-semantics/semantics/call.k:42` (through line 46)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### rule at `reference-semantics/semantics/call.k:47` (through line 50)

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### syntax at `reference-semantics/semantics/call.k:52` (through line 52)

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### rule at `reference-semantics/semantics/call.k:53` (through line 55)

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### rule at `reference-semantics/semantics/call.k:56` (through line 62)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
  // non-mutating methods READ their heap-object arguments too (join's list);
  // mutators keep refs (append of a list into a list-of-lists stays aliased)
```

### rule at `reference-semantics/semantics/call.k:63` (through line 67)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### rule at `reference-semantics/semantics/call.k:69` (through line 79)

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>

  // annotated closure: the frame starts with the captured freevar cells, its
  // parent is the module scope (all enclosing-local reads go through cells),
  // and the cellvars' fresh cells allocate before params bind (a cellvar param
  // then writes through its cell in #bindP).
```

### rule at `reference-semantics/semantics/call.k:80` (through line 85)

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### syntax at `reference-semantics/semantics/call.k:87` (through line 87)

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### rule at `reference-semantics/semantics/call.k:88` (through line 88)

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### rule at `reference-semantics/semantics/call.k:89` (through line 94)

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

## `reference-semantics/semantics/comprehension.k`

### rule at `reference-semantics/semantics/comprehension.k:11` (through line 11)

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### rule at `reference-semantics/semantics/comprehension.k:12` (through line 12)

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### syntax at `reference-semantics/semantics/comprehension.k:14` (through line 14)

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### rule at `reference-semantics/semantics/comprehension.k:15` (through line 16)

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### syntax at `reference-semantics/semantics/comprehension.k:18` (through line 18)

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### rule at `reference-semantics/semantics/comprehension.k:19` (through line 20)

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### rule at `reference-semantics/semantics/comprehension.k:21` (through line 22)

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### syntax at `reference-semantics/semantics/comprehension.k:24` (through line 24)

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### rule at `reference-semantics/semantics/comprehension.k:25` (through line 25)

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### rule at `reference-semantics/semantics/comprehension.k:26` (through line 26)

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## `reference-semantics/semantics/concrete.k`

### rule at `reference-semantics/semantics/concrete.k:13` (through line 15)

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### rule at `reference-semantics/semantics/concrete.k:16` (through line 24)

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)

  // ==== keyed sort, concrete leg ============================================
  // Computes each key by a REAL call through the uniform #callee machinery
  // (closures, len, type objects all work), stable-inserts on the key, and
  // allocates the result. priority(40) beats sort.k's opaque rules, so krun
  // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.
```

### syntax at `reference-semantics/semantics/concrete.k:25` (through line 25)

```k
  syntax Val ::= kvP(Val, Val)
```

### syntax at `reference-semantics/semantics/concrete.k:26` (through line 27)

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### rule at `reference-semantics/semantics/concrete.k:28` (through line 30)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### rule at `reference-semantics/semantics/concrete.k:31` (through line 33)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### rule at `reference-semantics/semantics/concrete.k:34` (through line 35)

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### rule at `reference-semantics/semantics/concrete.k:36` (through line 37)

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### rule at `reference-semantics/semantics/concrete.k:38` (through line 40)

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### syntax at `reference-semantics/semantics/concrete.k:42` (through line 42)

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### rule at `reference-semantics/semantics/concrete.k:43` (through line 43)

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### rule at `reference-semantics/semantics/concrete.k:44` (through line 46)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### rule at `reference-semantics/semantics/concrete.k:47` (through line 49)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### syntax at `reference-semantics/semantics/concrete.k:51` (through line 51)

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### rule at `reference-semantics/semantics/concrete.k:52` (through line 52)

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### rule at `reference-semantics/semantics/concrete.k:53` (through line 53)

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### rule at `reference-semantics/semantics/concrete.k:54` (through line 54)

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### syntax at `reference-semantics/semantics/concrete.k:56` (through line 56)

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### rule at `reference-semantics/semantics/concrete.k:57` (through line 57)

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### rule at `reference-semantics/semantics/concrete.k:58` (through line 58)

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### rule at `reference-semantics/semantics/concrete.k:59` (through line 59)

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## `reference-semantics/semantics/controls.k`

### rule at `reference-semantics/semantics/controls.k:9` (through line 11)

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### rule at `reference-semantics/semantics/controls.k:12` (through line 18)

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### rule at `reference-semantics/semantics/controls.k:20` (through line 26)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
  // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
  // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
  // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
```

### rule at `reference-semantics/semantics/controls.k:27` (through line 34)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]

  // ==== import trivia: `from math import floor, ceil` binds the supported
  // names as builtins in the current scope; every other import is a no-op
```

### rule at `reference-semantics/semantics/controls.k:35` (through line 35)

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### rule at `reference-semantics/semantics/controls.k:36` (through line 36)

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### syntax at `reference-semantics/semantics/controls.k:37` (through line 37)

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### rule at `reference-semantics/semantics/controls.k:38` (through line 38)

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### rule at `reference-semantics/semantics/controls.k:39` (through line 42)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### rule at `reference-semantics/semantics/controls.k:43` (through line 47)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

### rule at `reference-semantics/semantics/controls.k:48` (through line 50)

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### syntax at `reference-semantics/semantics/controls.k:51` (through line 51)

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### rule at `reference-semantics/semantics/controls.k:52` (through line 52)

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### rule at `reference-semantics/semantics/controls.k:53` (through line 53)

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### rule at `reference-semantics/semantics/controls.k:54` (through line 56)

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### rule at `reference-semantics/semantics/controls.k:57` (through line 58)

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### rule at `reference-semantics/semantics/controls.k:59` (through line 64)

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

### syntax at `reference-semantics/semantics/controls.k:65` (through line 67)

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### rule at `reference-semantics/semantics/controls.k:69` (through line 69)

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### rule at `reference-semantics/semantics/controls.k:71` (through line 71)

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### rule at `reference-semantics/semantics/controls.k:72` (through line 72)

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### rule at `reference-semantics/semantics/controls.k:73` (through line 76)

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### rule at `reference-semantics/semantics/controls.k:77` (through line 77)

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### rule at `reference-semantics/semantics/controls.k:78` (through line 78)

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### rule at `reference-semantics/semantics/controls.k:79` (through line 80)

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### rule at `reference-semantics/semantics/controls.k:81` (through line 84)

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

### rule at `reference-semantics/semantics/controls.k:85` (through line 85)

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### rule at `reference-semantics/semantics/controls.k:86` (through line 86)

```k
  rule <k> Continue => #cont ... </k>
```

### rule at `reference-semantics/semantics/controls.k:87` (through line 87)

```k
  rule <k> Break => #brk ... </k>
```

### rule at `reference-semantics/semantics/controls.k:88` (through line 88)

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### rule at `reference-semantics/semantics/controls.k:89` (through line 89)

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### rule at `reference-semantics/semantics/controls.k:90` (through line 90)

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### rule at `reference-semantics/semantics/controls.k:91` (through line 94)

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### rule at `reference-semantics/semantics/controls.k:95` (through line 97)

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at `reference-semantics/semantics/controls.k:98` (through line 100)

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at `reference-semantics/semantics/controls.k:101` (through line 105)

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### rule at `reference-semantics/semantics/controls.k:106` (through line 108)

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/core.k`

### syntax at `reference-semantics/semantics/core.k:13` (through line 13)

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### syntax at `reference-semantics/semantics/core.k:14` (through line 14)

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### syntax at `reference-semantics/semantics/core.k:15` (through line 17)

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### syntax at `reference-semantics/semantics/core.k:18` (through line 23)

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### syntax at `reference-semantics/semantics/core.k:25` (through line 34)

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

### syntax at `reference-semantics/semantics/core.k:36` (through line 36)

```k
  syntax Parent   ::= "root" | parent(Int)
```

### syntax at `reference-semantics/semantics/core.k:37` (through line 37)

```k
  syntax Scope    ::= scope(Map, Parent)
```

### syntax at `reference-semantics/semantics/core.k:38` (through line 38)

```k
  syntax KResult  ::= Val
```

### syntax at `reference-semantics/semantics/core.k:39` (through line 39)

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### syntax at `reference-semantics/semantics/core.k:40` (through line 40)

```k
  syntax Vals     ::= List{Val, ","}
```

### syntax at `reference-semantics/semantics/core.k:41` (through line 41)

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### syntax at `reference-semantics/semantics/core.k:42` (through line 48)

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### configuration at `reference-semantics/semantics/core.k:49` (through line 67)

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

  // ==== heap allocation (constructed lists become objects) ==================
  // Cons-form emission with a freshness guard (the heap-list-probe discipline:
  // an update-form H[N <- _] never re-normalizes symbolically). heapLoc is
  // monotonic — it does NOT wind back at #pop: returned lists escape by ref.
  // A bare list(VS) Val stays legal (read-only inputs in claims flow unboxed);
  // only CONSTRUCTORS in program syntax allocate.
```

### syntax at `reference-semantics/semantics/core.k:68` (through line 68)

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### rule at `reference-semantics/semantics/core.k:69` (through line 69)

```k
  rule isRefV(ref(_:Int)) => true
```

### rule at `reference-semantics/semantics/core.k:70` (through line 74)

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### syntax at `reference-semantics/semantics/core.k:75` (through line 75)

```k
  syntax HeapVal ::= cellV(Val)
```

### syntax at `reference-semantics/semantics/core.k:76` (through line 76)

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### rule at `reference-semantics/semantics/core.k:77` (through line 77)

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### rule at `reference-semantics/semantics/core.k:78` (through line 84)

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

### rule at `reference-semantics/semantics/core.k:85` (through line 94)

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]

  // write through a cell (Assign / #bindP / #bindTgt dispatch here on
  // cell-bound names)
  // a keyword argument cools to a TAGGED value (consumed by kw-aware builtins)
```

### syntax at `reference-semantics/semantics/core.k:95` (through line 95)

```k
  syntax Val ::= kwV(String, Val)
```

### syntax at `reference-semantics/semantics/core.k:96` (through line 96)

```k
  syntax KItem ::= #kwTag(String)
```

### rule at `reference-semantics/semantics/core.k:97` (through line 97)

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### rule at `reference-semantics/semantics/core.k:98` (through line 99)

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### syntax at `reference-semantics/semantics/core.k:100` (through line 100)

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### rule at `reference-semantics/semantics/core.k:101` (through line 101)

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### rule at `reference-semantics/semantics/core.k:102` (through line 105)

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### syntax at `reference-semantics/semantics/core.k:106` (through line 106)

```k
  syntax Val ::= cellsMark(ParamNames)
```

### syntax at `reference-semantics/semantics/core.k:107` (through line 107)

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### rule at `reference-semantics/semantics/core.k:108` (through line 108)

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### syntax at `reference-semantics/semantics/core.k:109` (through line 109)

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### rule at `reference-semantics/semantics/core.k:110` (through line 110)

```k
  rule pnMember(_:String, .ParamNames) => false
```

### rule at `reference-semantics/semantics/core.k:111` (through line 111)

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### syntax at `reference-semantics/semantics/core.k:113` (through line 113)

```k
  syntax KItem ::= #cellW(Val, Val)
```

### rule at `reference-semantics/semantics/core.k:114` (through line 115)

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### syntax at `reference-semantics/semantics/core.k:117` (through line 117)

```k
  syntax KItem ::= #alloc(Val)
```

### rule at `reference-semantics/semantics/core.k:118` (through line 123)

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

### syntax at `reference-semantics/semantics/core.k:124` (through line 124)

```k
  syntax KItem ::= #loadAll(Module)
```

### rule at `reference-semantics/semantics/core.k:125` (through line 125)

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### rule at `reference-semantics/semantics/core.k:126` (through line 126)

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### rule at `reference-semantics/semantics/core.k:127` (through line 129)

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### syntax at `reference-semantics/semantics/core.k:130` (through line 130)

```k
  syntax KItem ::= #look(String, Int)
```

### rule at `reference-semantics/semantics/core.k:131` (through line 131)

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### rule at `reference-semantics/semantics/core.k:132` (through line 144)

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
  // a SYNTACTICALLY cell-bound name reads through the heap cell AT THE
  // LOOKUP (higher priority beats the plain return above on concrete cell
  // bindings; abstract claim values take the plain rule unchanged) — this
  // covers cross-frame cell reads (a comprehension closure reading the
  // enclosing function's cellvar) without a narrowing-prone k-top redex
  // guarded on the FOUND frame's DECLARED cellvars (pnMember over the
  // cellsMark): decidable for every concrete frame pin — plain frames and
  // non-cell names prune outright, so an abstract looked-up value never
  // drags a narrowing cellV heap match along (probed on 5-intersperse and
  // Q4's abstract `numbers` in the annotated frame)
```

### rule at `reference-semantics/semantics/core.k:145` (through line 151)

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### rule at `reference-semantics/semantics/core.k:152` (through line 156)

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

### syntax at `reference-semantics/semantics/core.k:157` (through line 157)

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### rule at `reference-semantics/semantics/core.k:158` (through line 184)

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

  // ==== argument/element evaluation: ONE left-to-right loop, tagged by destination ==
  // (list/tuple literals and calls all use it; modules extend ApplyK with their tags)
```

### syntax at `reference-semantics/semantics/core.k:185` (through line 185)

```k
  syntax ApplyK ::= toCall(Val)
```

### syntax at `reference-semantics/semantics/core.k:186` (through line 188)

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### rule at `reference-semantics/semantics/core.k:189` (through line 189)

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### rule at `reference-semantics/semantics/core.k:190` (through line 190)

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### rule at `reference-semantics/semantics/core.k:191` (through line 193)

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### rule at `reference-semantics/semantics/core.k:194` (through line 194)

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### rule at `reference-semantics/semantics/core.k:195` (through line 195)

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### rule at `reference-semantics/semantics/core.k:196` (through line 198)

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### syntax at `reference-semantics/semantics/core.k:199` (through line 199)

```k
  syntax Bool ::= truthy(Val) [function]
```

### rule at `reference-semantics/semantics/core.k:200` (through line 200)

```k
  rule truthy(B:Bool)          => B
```

### rule at `reference-semantics/semantics/core.k:201` (through line 201)

```k
  rule truthy(noneV)           => false
```

### rule at `reference-semantics/semantics/core.k:202` (through line 202)

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### rule at `reference-semantics/semantics/core.k:203` (through line 203)

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### rule at `reference-semantics/semantics/core.k:204` (through line 204)

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### rule at `reference-semantics/semantics/core.k:205` (through line 207)

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### syntax at `reference-semantics/semantics/core.k:208` (through line 208)

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### syntax at `reference-semantics/semantics/core.k:209` (through line 209)

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### syntax at `reference-semantics/semantics/core.k:210` (through line 212)

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### syntax at `reference-semantics/semantics/core.k:213` (through line 213)

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### rule at `reference-semantics/semantics/core.k:214` (through line 214)

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### rule at `reference-semantics/semantics/core.k:215` (through line 215)

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### syntax at `reference-semantics/semantics/core.k:217` (through line 217)

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### rule at `reference-semantics/semantics/core.k:218` (through line 218)

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### rule at `reference-semantics/semantics/core.k:219` (through line 222)

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### syntax at `reference-semantics/semantics/core.k:223` (through line 223)

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### rule at `reference-semantics/semantics/core.k:224` (through line 224)

```k
  rule vsLen(.ValSeq)                => 0
```

### rule at `reference-semantics/semantics/core.k:225` (through line 225)

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### syntax at `reference-semantics/semantics/core.k:227` (through line 227)

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/core.k:228` (through line 228)

```k
  rule isLen(.IntSeq)                => 0
```

### rule at `reference-semantics/semantics/core.k:229` (through line 232)

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### syntax at `reference-semantics/semantics/core.k:233` (through line 233)

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### rule at `reference-semantics/semantics/core.k:234` (through line 234)

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### rule at `reference-semantics/semantics/core.k:235` (through line 235)

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### rule at `reference-semantics/semantics/core.k:236` (through line 237)

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### rule at `reference-semantics/semantics/core.k:238` (through line 239)

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

## `reference-semantics/semantics/dict.k`

### syntax at `reference-semantics/semantics/dict.k:20` (through line 22)

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### syntax at `reference-semantics/semantics/dict.k:23` (through line 25)

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### rule at `reference-semantics/semantics/dict.k:26` (through line 26)

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### rule at `reference-semantics/semantics/dict.k:27` (through line 27)

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### rule at `reference-semantics/semantics/dict.k:28` (through line 29)

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### rule at `reference-semantics/semantics/dict.k:30` (through line 31)

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### rule at `reference-semantics/semantics/dict.k:32` (through line 36)

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### syntax at `reference-semantics/semantics/dict.k:37` (through line 37)

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### rule at `reference-semantics/semantics/dict.k:38` (through line 38)

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### rule at `reference-semantics/semantics/dict.k:39` (through line 39)

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### rule at `reference-semantics/semantics/dict.k:40` (through line 42)

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### syntax at `reference-semantics/semantics/dict.k:43` (through line 43)

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### rule at `reference-semantics/semantics/dict.k:44` (through line 44)

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### rule at `reference-semantics/semantics/dict.k:45` (through line 48)

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### syntax at `reference-semantics/semantics/dict.k:49` (through line 49)

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### rule at `reference-semantics/semantics/dict.k:50` (through line 51)

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### rule at `reference-semantics/semantics/dict.k:52` (through line 53)

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### rule at `reference-semantics/semantics/dict.k:54` (through line 57)

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### rule at `reference-semantics/semantics/dict.k:58` (through line 62)

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### rule at `reference-semantics/semantics/dict.k:63` (through line 63)

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### syntax at `reference-semantics/semantics/dict.k:64` (through line 64)

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### rule at `reference-semantics/semantics/dict.k:65` (through line 69)

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### syntax at `reference-semantics/semantics/dict.k:70` (through line 70)

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### rule at `reference-semantics/semantics/dict.k:71` (through line 75)

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### syntax at `reference-semantics/semantics/dict.k:76` (through line 76)

```k
  syntax KItem ::= #dsetK(String, Val)
```

### rule at `reference-semantics/semantics/dict.k:77` (through line 77)

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### rule at `reference-semantics/semantics/dict.k:78` (through line 81)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### rule at `reference-semantics/semantics/dict.k:82` (through line 85)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### syntax at `reference-semantics/semantics/dict.k:86` (through line 86)

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### rule at `reference-semantics/semantics/dict.k:87` (through line 89)

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### syntax at `reference-semantics/semantics/dict.k:90` (through line 90)

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### rule at `reference-semantics/semantics/dict.k:91` (through line 91)

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### rule at `reference-semantics/semantics/dict.k:92` (through line 94)

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### rule at `reference-semantics/semantics/dict.k:95` (through line 96)

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### syntax at `reference-semantics/semantics/dict.k:97` (through line 97)

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### rule at `reference-semantics/semantics/dict.k:98` (through line 98)

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### rule at `reference-semantics/semantics/dict.k:99` (through line 100)

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### syntax at `reference-semantics/semantics/dict.k:101` (through line 101)

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### rule at `reference-semantics/semantics/dict.k:102` (through line 102)

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### rule at `reference-semantics/semantics/dict.k:103` (through line 103)

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## `reference-semantics/semantics/float.k`

### syntax at `reference-semantics/semantics/float.k:20` (through line 20)

```k
  syntax Val ::= Float
```

### rule at `reference-semantics/semantics/float.k:21` (through line 23)

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### syntax at `reference-semantics/semantics/float.k:24` (through line 24)

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:25` (through line 25)

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### rule at `reference-semantics/semantics/float.k:27` (through line 29)

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### syntax at `reference-semantics/semantics/float.k:30` (through line 30)

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:31` (through line 31)

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### rule at `reference-semantics/semantics/float.k:32` (through line 36)

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### syntax at `reference-semantics/semantics/float.k:37` (through line 37)

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:38` (through line 38)

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### rule at `reference-semantics/semantics/float.k:39` (through line 42)

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### rule at `reference-semantics/semantics/float.k:43` (through line 43)

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### rule at `reference-semantics/semantics/float.k:44` (through line 49)

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### syntax at `reference-semantics/semantics/float.k:50` (through line 50)

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:51` (through line 51)

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### rule at `reference-semantics/semantics/float.k:52` (through line 52)

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### syntax at `reference-semantics/semantics/float.k:54` (through line 54)

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:55` (through line 55)

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### rule at `reference-semantics/semantics/float.k:56` (through line 60)

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### rule at `reference-semantics/semantics/float.k:61` (through line 64)

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### syntax at `reference-semantics/semantics/float.k:65` (through line 65)

```k
  syntax KItem ::= "#mathCeil"
```

### rule at `reference-semantics/semantics/float.k:66` (through line 66)

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### rule at `reference-semantics/semantics/float.k:67` (through line 69)

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### syntax at `reference-semantics/semantics/float.k:70` (through line 70)

```k
  syntax KItem ::= "#mathFloor"
```

### rule at `reference-semantics/semantics/float.k:71` (through line 71)

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### rule at `reference-semantics/semantics/float.k:72` (through line 72)

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### syntax at `reference-semantics/semantics/float.k:73` (through line 73)

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### rule at `reference-semantics/semantics/float.k:74` (through line 74)

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### rule at `reference-semantics/semantics/float.k:75` (through line 77)

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### rule at `reference-semantics/semantics/float.k:78` (through line 78)

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### rule at `reference-semantics/semantics/float.k:79` (through line 81)

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### syntax at `reference-semantics/semantics/float.k:82` (through line 82)

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### rule at `reference-semantics/semantics/float.k:83` (through line 83)

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### rule at `reference-semantics/semantics/float.k:84` (through line 84)

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### rule at `reference-semantics/semantics/float.k:85` (through line 85)

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### syntax at `reference-semantics/semantics/float.k:86` (through line 86)

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### rule at `reference-semantics/semantics/float.k:87` (through line 87)

```k
  rule toF(F:Float) => F        [concrete]
```

### rule at `reference-semantics/semantics/float.k:88` (through line 92)

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### syntax at `reference-semantics/semantics/float.k:93` (through line 93)

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### rule at `reference-semantics/semantics/float.k:94` (through line 94)

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### rule at `reference-semantics/semantics/float.k:95` (through line 98)

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### rule at `reference-semantics/semantics/float.k:99` (through line 102)

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### syntax at `reference-semantics/semantics/float.k:103` (through line 103)

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:104` (through line 104)

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### rule at `reference-semantics/semantics/float.k:105` (through line 105)

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### syntax at `reference-semantics/semantics/float.k:107` (through line 107)

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:108` (through line 108)

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### rule at `reference-semantics/semantics/float.k:109` (through line 109)

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### syntax at `reference-semantics/semantics/float.k:111` (through line 111)

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:112` (through line 112)

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### rule at `reference-semantics/semantics/float.k:113` (through line 113)

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### syntax at `reference-semantics/semantics/float.k:115` (through line 115)

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:116` (through line 116)

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### rule at `reference-semantics/semantics/float.k:117` (through line 117)

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### syntax at `reference-semantics/semantics/float.k:119` (through line 119)

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:120` (through line 120)

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### rule at `reference-semantics/semantics/float.k:121` (through line 124)

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### syntax at `reference-semantics/semantics/float.k:125` (through line 125)

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:126` (through line 126)

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### rule at `reference-semantics/semantics/float.k:127` (through line 127)

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### rule at `reference-semantics/semantics/float.k:128` (through line 128)

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### rule at `reference-semantics/semantics/float.k:129` (through line 131)

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### rule at `reference-semantics/semantics/float.k:132` (through line 132)

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:133` (through line 133)

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:134` (through line 134)

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:135` (through line 135)

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:136` (through line 136)

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:137` (through line 137)

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:138` (through line 138)

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:139` (through line 141)

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### syntax at `reference-semantics/semantics/float.k:142` (through line 142)

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:143` (through line 143)

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### rule at `reference-semantics/semantics/float.k:144` (through line 144)

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:145` (through line 145)

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:146` (through line 146)

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:147` (through line 147)

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:148` (through line 148)

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:149` (through line 149)

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:150` (through line 150)

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:151` (through line 153)

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### rule at `reference-semantics/semantics/float.k:154` (through line 154)

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### rule at `reference-semantics/semantics/float.k:155` (through line 159)

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### syntax at `reference-semantics/semantics/float.k:160` (through line 160)

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:161` (through line 161)

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### rule at `reference-semantics/semantics/float.k:162` (through line 164)

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### syntax at `reference-semantics/semantics/float.k:165` (through line 165)

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### rule at `reference-semantics/semantics/float.k:166` (through line 166)

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### syntax at `reference-semantics/semantics/float.k:167` (through line 167)

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### rule at `reference-semantics/semantics/float.k:168` (through line 168)

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### rule at `reference-semantics/semantics/float.k:169` (through line 169)

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### rule at `reference-semantics/semantics/float.k:170` (through line 170)

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### rule at `reference-semantics/semantics/float.k:171` (through line 172)

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### syntax at `reference-semantics/semantics/float.k:173` (through line 173)

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### rule at `reference-semantics/semantics/float.k:174` (through line 174)

```k
  rule fracPart(.IntSeq) => 0
```

### rule at `reference-semantics/semantics/float.k:175` (through line 175)

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### rule at `reference-semantics/semantics/float.k:176` (through line 176)

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### rule at `reference-semantics/semantics/float.k:177` (through line 177)

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### rule at `reference-semantics/semantics/float.k:178` (through line 178)

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### syntax at `reference-semantics/semantics/float.k:179` (through line 179)

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### rule at `reference-semantics/semantics/float.k:180` (through line 180)

```k
  rule fracScale(.IntSeq) => 1
```

### rule at `reference-semantics/semantics/float.k:181` (through line 181)

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### rule at `reference-semantics/semantics/float.k:182` (through line 182)

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### rule at `reference-semantics/semantics/float.k:183` (through line 183)

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### rule at `reference-semantics/semantics/float.k:184` (through line 184)

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### rule at `reference-semantics/semantics/float.k:185` (through line 185)

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### rule at `reference-semantics/semantics/float.k:186` (through line 186)

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### rule at `reference-semantics/semantics/float.k:187` (through line 189)

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### syntax at `reference-semantics/semantics/float.k:190` (through line 190)

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:191` (through line 191)

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### rule at `reference-semantics/semantics/float.k:192` (through line 194)

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### syntax at `reference-semantics/semantics/float.k:195` (through line 195)

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:196` (through line 196)

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### rule at `reference-semantics/semantics/float.k:197` (through line 197)

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:198` (through line 198)

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:199` (through line 199)

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:200` (through line 200)

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:201` (through line 201)

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:202` (through line 202)

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:203` (through line 203)

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:204` (through line 204)

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### rule at `reference-semantics/semantics/float.k:205` (through line 205)

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### rule at `reference-semantics/semantics/float.k:206` (through line 208)

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### syntax at `reference-semantics/semantics/float.k:209` (through line 209)

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:210` (through line 210)

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### rule at `reference-semantics/semantics/float.k:211` (through line 211)

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### rule at `reference-semantics/semantics/float.k:213` (through line 213)

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### rule at `reference-semantics/semantics/float.k:214` (through line 216)

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### syntax at `reference-semantics/semantics/float.k:217` (through line 217)

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:218` (through line 222)

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### syntax at `reference-semantics/semantics/float.k:223` (through line 223)

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:224` (through line 226)

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### rule at `reference-semantics/semantics/float.k:227` (through line 227)

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### rule at `reference-semantics/semantics/float.k:228` (through line 228)

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### syntax at `reference-semantics/semantics/float.k:230` (through line 230)

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### rule at `reference-semantics/semantics/float.k:231` (through line 231)

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### syntax at `reference-semantics/semantics/float.k:232` (through line 232)

```k
  syntax KItem ::= "#mathSqrt"
```

### rule at `reference-semantics/semantics/float.k:233` (through line 233)

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### rule at `reference-semantics/semantics/float.k:234` (through line 234)

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### rule at `reference-semantics/semantics/float.k:235` (through line 242)

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

### syntax at `reference-semantics/semantics/float.k:243` (through line 243)

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### rule at `reference-semantics/semantics/float.k:244` (through line 244)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### rule at `reference-semantics/semantics/float.k:245` (through line 245)

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### rule at `reference-semantics/semantics/float.k:246` (through line 246)

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### rule at `reference-semantics/semantics/float.k:247` (through line 248)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### syntax at `reference-semantics/semantics/float.k:250` (through line 250)

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### rule at `reference-semantics/semantics/float.k:251` (through line 251)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### rule at `reference-semantics/semantics/float.k:252` (through line 252)

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### rule at `reference-semantics/semantics/float.k:253` (through line 253)

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### rule at `reference-semantics/semantics/float.k:254` (through line 260)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

### syntax at `reference-semantics/semantics/float.k:261` (through line 261)

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### rule at `reference-semantics/semantics/float.k:262` (through line 264)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### rule at `reference-semantics/semantics/float.k:265` (through line 265)

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### rule at `reference-semantics/semantics/float.k:266` (through line 266)

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### rule at `reference-semantics/semantics/float.k:267` (through line 269)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### rule at `reference-semantics/semantics/float.k:270` (through line 272)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

## `reference-semantics/semantics/functions.k`

### syntax at `reference-semantics/semantics/functions.k:8` (through line 13)

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### rule at `reference-semantics/semantics/functions.k:14` (through line 16)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### syntax at `reference-semantics/semantics/functions.k:18` (through line 18)

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### rule at `reference-semantics/semantics/functions.k:19` (through line 26)

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

### syntax at `reference-semantics/semantics/functions.k:27` (through line 30)

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### syntax at `reference-semantics/semantics/functions.k:31` (through line 32)

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### rule at `reference-semantics/semantics/functions.k:33` (through line 35)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### rule at `reference-semantics/semantics/functions.k:36` (through line 41)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### rule at `reference-semantics/semantics/functions.k:42` (through line 45)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### rule at `reference-semantics/semantics/functions.k:47` (through line 49)

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### rule at `reference-semantics/semantics/functions.k:50` (through line 52)

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### rule at `reference-semantics/semantics/functions.k:53` (through line 58)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### rule at `reference-semantics/semantics/functions.k:59` (through line 62)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### rule at `reference-semantics/semantics/functions.k:63` (through line 63)

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### rule at `reference-semantics/semantics/functions.k:64` (through line 67)

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### rule at `reference-semantics/semantics/functions.k:68` (through line 77)

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
        andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
       [priority(40)]

  // ==== return / pop the frame (the returned expr evaluates by strictness) ==
```

### rule at `reference-semantics/semantics/functions.k:78` (through line 79)

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### rule at `reference-semantics/semantics/functions.k:80` (through line 84)

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### rule at `reference-semantics/semantics/functions.k:85` (through line 90)

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## `reference-semantics/semantics/int.k`

### rule at `reference-semantics/semantics/int.k:7` (through line 7)

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### rule at `reference-semantics/semantics/int.k:9` (through line 10)

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### rule at `reference-semantics/semantics/int.k:11` (through line 11)

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### rule at `reference-semantics/semantics/int.k:12` (through line 12)

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### rule at `reference-semantics/semantics/int.k:13` (through line 13)

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### rule at `reference-semantics/semantics/int.k:14` (through line 14)

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### rule at `reference-semantics/semantics/int.k:15` (through line 15)

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### rule at `reference-semantics/semantics/int.k:16` (through line 16)

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### rule at `reference-semantics/semantics/int.k:17` (through line 17)

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### syntax at `reference-semantics/semantics/int.k:19` (through line 19)

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### rule at `reference-semantics/semantics/int.k:20` (through line 20)

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### rule at `reference-semantics/semantics/int.k:22` (through line 22)

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### rule at `reference-semantics/semantics/int.k:23` (through line 23)

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### rule at `reference-semantics/semantics/int.k:24` (through line 24)

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### rule at `reference-semantics/semantics/int.k:25` (through line 25)

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### rule at `reference-semantics/semantics/int.k:26` (through line 26)

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### rule at `reference-semantics/semantics/int.k:27` (through line 27)

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## `reference-semantics/semantics/iter.k`

### syntax at `reference-semantics/semantics/iter.k:8` (through line 8)

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## `reference-semantics/semantics/list.k`

### rule at `reference-semantics/semantics/list.k:9` (through line 9)

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### rule at `reference-semantics/semantics/list.k:10` (through line 12)

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### syntax at `reference-semantics/semantics/list.k:13` (through line 13)

```k
  syntax ApplyK ::= "toList"
```

### rule at `reference-semantics/semantics/list.k:14` (through line 14)

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### rule at `reference-semantics/semantics/list.k:15` (through line 17)

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### syntax at `reference-semantics/semantics/list.k:18` (through line 18)

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### rule at `reference-semantics/semantics/list.k:19` (through line 19)

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### rule at `reference-semantics/semantics/list.k:20` (through line 23)

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### rule at `reference-semantics/semantics/list.k:24` (through line 25)

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### rule at `reference-semantics/semantics/list.k:27` (through line 27)

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### rule at `reference-semantics/semantics/list.k:28` (through line 32)

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### syntax at `reference-semantics/semantics/list.k:33` (through line 33)

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### rule at `reference-semantics/semantics/list.k:34` (through line 34)

```k
  rule hasRefVS(.ValSeq)                => false
```

### rule at `reference-semantics/semantics/list.k:35` (through line 35)

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### syntax at `reference-semantics/semantics/list.k:37` (through line 38)

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### rule at `reference-semantics/semantics/list.k:39` (through line 39)

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### rule at `reference-semantics/semantics/list.k:40` (through line 40)

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### rule at `reference-semantics/semantics/list.k:41` (through line 41)

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### rule at `reference-semantics/semantics/list.k:42` (through line 43)

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### rule at `reference-semantics/semantics/list.k:45` (through line 46)

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### rule at `reference-semantics/semantics/list.k:47` (through line 48)

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### rule at `reference-semantics/semantics/list.k:49` (through line 49)

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### rule at `reference-semantics/semantics/list.k:50` (through line 52)

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### rule at `reference-semantics/semantics/list.k:53` (through line 57)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### syntax at `reference-semantics/semantics/list.k:58` (through line 58)

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### rule at `reference-semantics/semantics/list.k:59` (through line 59)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### rule at `reference-semantics/semantics/list.k:60` (through line 60)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### rule at `reference-semantics/semantics/list.k:61` (through line 61)

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### rule at `reference-semantics/semantics/list.k:62` (through line 62)

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### rule at `reference-semantics/semantics/list.k:63` (through line 64)

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### rule at `reference-semantics/semantics/list.k:65` (through line 66)

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### rule at `reference-semantics/semantics/list.k:67` (through line 67)

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## `reference-semantics/semantics/methods.k`

### syntax at `reference-semantics/semantics/methods.k:10` (through line 12)

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### rule at `reference-semantics/semantics/methods.k:13` (through line 13)

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### rule at `reference-semantics/semantics/methods.k:14` (through line 14)

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### rule at `reference-semantics/semantics/methods.k:15` (through line 15)

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### rule at `reference-semantics/semantics/methods.k:16` (through line 18)

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### rule at `reference-semantics/semantics/methods.k:19` (through line 19)

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### rule at `reference-semantics/semantics/methods.k:20` (through line 20)

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### rule at `reference-semantics/semantics/methods.k:21` (through line 25)

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### rule at `reference-semantics/semantics/methods.k:26` (through line 26)

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### syntax at `reference-semantics/semantics/methods.k:27` (through line 27)

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:28` (through line 28)

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### rule at `reference-semantics/semantics/methods.k:29` (through line 29)

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### rule at `reference-semantics/semantics/methods.k:30` (through line 33)

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### rule at `reference-semantics/semantics/methods.k:34` (through line 34)

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### syntax at `reference-semantics/semantics/methods.k:35` (through line 35)

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### rule at `reference-semantics/semantics/methods.k:36` (through line 36)

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### rule at `reference-semantics/semantics/methods.k:37` (through line 38)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### rule at `reference-semantics/semantics/methods.k:39` (through line 40)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### syntax at `reference-semantics/semantics/methods.k:41` (through line 41)

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:42` (through line 42)

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### rule at `reference-semantics/semantics/methods.k:43` (through line 43)

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### rule at `reference-semantics/semantics/methods.k:44` (through line 46)

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### rule at `reference-semantics/semantics/methods.k:47` (through line 47)

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### syntax at `reference-semantics/semantics/methods.k:48` (through line 48)

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:49` (through line 49)

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### rule at `reference-semantics/semantics/methods.k:50` (through line 50)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### rule at `reference-semantics/semantics/methods.k:51` (through line 51)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### syntax at `reference-semantics/semantics/methods.k:52` (through line 52)

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:53` (through line 53)

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### rule at `reference-semantics/semantics/methods.k:54` (through line 54)

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### rule at `reference-semantics/semantics/methods.k:55` (through line 57)

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### rule at `reference-semantics/semantics/methods.k:58` (through line 60)

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### rule at `reference-semantics/semantics/methods.k:61` (through line 63)

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### rule at `reference-semantics/semantics/methods.k:64` (through line 64)

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### syntax at `reference-semantics/semantics/methods.k:65` (through line 65)

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:66` (through line 66)

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### rule at `reference-semantics/semantics/methods.k:67` (through line 67)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### rule at `reference-semantics/semantics/methods.k:68` (through line 71)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### rule at `reference-semantics/semantics/methods.k:72` (through line 74)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### syntax at `reference-semantics/semantics/methods.k:75` (through line 75)

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### rule at `reference-semantics/semantics/methods.k:76` (through line 76)

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### rule at `reference-semantics/semantics/methods.k:77` (through line 78)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### rule at `reference-semantics/semantics/methods.k:79` (through line 81)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

### syntax at `reference-semantics/semantics/methods.k:82` (through line 82)

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### rule at `reference-semantics/semantics/methods.k:83` (through line 83)

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### rule at `reference-semantics/semantics/methods.k:84` (through line 84)

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### syntax at `reference-semantics/semantics/methods.k:85` (through line 85)

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:86` (through line 88)

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### rule at `reference-semantics/semantics/methods.k:89` (through line 93)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### rule at `reference-semantics/semantics/methods.k:94` (through line 96)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### syntax at `reference-semantics/semantics/methods.k:97` (through line 97)

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### rule at `reference-semantics/semantics/methods.k:98` (through line 98)

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### rule at `reference-semantics/semantics/methods.k:99` (through line 100)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### rule at `reference-semantics/semantics/methods.k:101` (through line 102)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### rule at `reference-semantics/semantics/methods.k:104` (through line 105)

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### syntax at `reference-semantics/semantics/methods.k:106` (through line 106)

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:107` (through line 107)

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### rule at `reference-semantics/semantics/methods.k:108` (through line 108)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### rule at `reference-semantics/semantics/methods.k:109` (through line 111)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### syntax at `reference-semantics/semantics/methods.k:112` (through line 112)

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:113` (through line 113)

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### syntax at `reference-semantics/semantics/methods.k:115` (through line 115)

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:116` (through line 116)

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### syntax at `reference-semantics/semantics/methods.k:118` (through line 118)

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:119` (through line 119)

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### syntax at `reference-semantics/semantics/methods.k:121` (through line 121)

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:122` (through line 122)

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### syntax at `reference-semantics/semantics/methods.k:124` (through line 124)

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:125` (through line 125)

```k
  rule hasUpper(.IntSeq) => false
```

### rule at `reference-semantics/semantics/methods.k:126` (through line 126)

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### syntax at `reference-semantics/semantics/methods.k:128` (through line 128)

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:129` (through line 129)

```k
  rule hasLower(.IntSeq) => false
```

### rule at `reference-semantics/semantics/methods.k:130` (through line 130)

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### syntax at `reference-semantics/semantics/methods.k:132` (through line 132)

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:133` (through line 133)

```k
  rule allAlpha(.IntSeq) => true
```

### rule at `reference-semantics/semantics/methods.k:134` (through line 134)

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### syntax at `reference-semantics/semantics/methods.k:136` (through line 136)

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:137` (through line 137)

```k
  rule allDigit(.IntSeq) => true
```

### rule at `reference-semantics/semantics/methods.k:138` (through line 138)

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### syntax at `reference-semantics/semantics/methods.k:140` (through line 140)

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:142` (through line 142)

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### rule at `reference-semantics/semantics/methods.k:143` (through line 143)

```k
  rule lowerC(C:Int) => C         [owise]
```

### syntax at `reference-semantics/semantics/methods.k:145` (through line 145)

```k
  syntax Int ::= upperC(Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:146` (through line 146)

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### rule at `reference-semantics/semantics/methods.k:147` (through line 147)

```k
  rule upperC(C:Int) => C         [owise]
```

### syntax at `reference-semantics/semantics/methods.k:149` (through line 149)

```k
  syntax Int ::= swapC(Int) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:150` (through line 150)

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### rule at `reference-semantics/semantics/methods.k:151` (through line 151)

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### rule at `reference-semantics/semantics/methods.k:152` (through line 152)

```k
  rule swapC(C:Int) => C         [owise]
```

### syntax at `reference-semantics/semantics/methods.k:154` (through line 154)

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:155` (through line 155)

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### rule at `reference-semantics/semantics/methods.k:156` (through line 156)

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### syntax at `reference-semantics/semantics/methods.k:158` (through line 158)

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:159` (through line 159)

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### rule at `reference-semantics/semantics/methods.k:160` (through line 160)

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### syntax at `reference-semantics/semantics/methods.k:162` (through line 162)

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:163` (through line 163)

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### rule at `reference-semantics/semantics/methods.k:164` (through line 164)

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### syntax at `reference-semantics/semantics/methods.k:166` (through line 166)

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/methods.k:167` (through line 167)

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### rule at `reference-semantics/semantics/methods.k:168` (through line 168)

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule at `reference-semantics/semantics/methods.k:169` (through line 169)

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## `reference-semantics/semantics/operators.k`

### rule at `reference-semantics/semantics/operators.k:10` (through line 10)

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### rule at `reference-semantics/semantics/operators.k:12` (through line 14)

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### context at `reference-semantics/semantics/operators.k:15` (through line 15)

```k
  context Compare(HOLE, _)
```

### context at `reference-semantics/semantics/operators.k:16` (through line 16)

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### rule at `reference-semantics/semantics/operators.k:17` (through line 17)

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### rule at `reference-semantics/semantics/operators.k:19` (through line 19)

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### rule at `reference-semantics/semantics/operators.k:20` (through line 24)

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### rule at `reference-semantics/semantics/operators.k:25` (through line 27)

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at `reference-semantics/semantics/operators.k:28` (through line 33)

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

### rule at `reference-semantics/semantics/operators.k:34` (through line 37)

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### rule at `reference-semantics/semantics/operators.k:38` (through line 42)

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### rule at `reference-semantics/semantics/operators.k:44` (through line 46)

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## `reference-semantics/semantics/range.k`

### syntax at `reference-semantics/semantics/range.k:9` (through line 9)

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### rule at `reference-semantics/semantics/range.k:10` (through line 10)

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### syntax at `reference-semantics/semantics/range.k:12` (through line 12)

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### rule at `reference-semantics/semantics/range.k:13` (through line 14)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### rule at `reference-semantics/semantics/range.k:15` (through line 16)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### rule at `reference-semantics/semantics/range.k:17` (through line 18)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### rule at `reference-semantics/semantics/range.k:20` (through line 22)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### rule at `reference-semantics/semantics/range.k:23` (through line 24)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

## `reference-semantics/semantics/set.k`

### syntax at `reference-semantics/semantics/set.k:8` (through line 10)

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### syntax at `reference-semantics/semantics/set.k:11` (through line 11)

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/set.k:12` (through line 12)

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### rule at `reference-semantics/semantics/set.k:13` (through line 15)

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### syntax at `reference-semantics/semantics/set.k:16` (through line 17)

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### rule at `reference-semantics/semantics/set.k:18` (through line 18)

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### rule at `reference-semantics/semantics/set.k:19` (through line 19)

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### rule at `reference-semantics/semantics/set.k:20` (through line 21)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### rule at `reference-semantics/semantics/set.k:22` (through line 23)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### syntax at `reference-semantics/semantics/set.k:25` (through line 25)

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### rule at `reference-semantics/semantics/set.k:26` (through line 26)

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### rule at `reference-semantics/semantics/set.k:27` (through line 30)

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### syntax at `reference-semantics/semantics/set.k:31` (through line 31)

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/set.k:32` (through line 32)

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### rule at `reference-semantics/semantics/set.k:33` (through line 33)

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### syntax at `reference-semantics/semantics/set.k:35` (through line 35)

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/set.k:36` (through line 38)

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### rule at `reference-semantics/semantics/set.k:39` (through line 39)

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## `reference-semantics/semantics/sort.k`

### syntax at `reference-semantics/semantics/sort.k:18` (through line 18)

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### syntax at `reference-semantics/semantics/sort.k:19` (through line 19)

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### rule at `reference-semantics/semantics/sort.k:20` (through line 20)

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### rule at `reference-semantics/semantics/sort.k:21` (through line 21)

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### rule at `reference-semantics/semantics/sort.k:22` (through line 22)

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### rule at `reference-semantics/semantics/sort.k:23` (through line 23)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### rule at `reference-semantics/semantics/sort.k:24` (through line 25)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### syntax at `reference-semantics/semantics/sort.k:26` (through line 26)

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### rule at `reference-semantics/semantics/sort.k:27` (through line 27)

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### rule at `reference-semantics/semantics/sort.k:28` (through line 28)

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### rule at `reference-semantics/semantics/sort.k:29` (through line 30)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### rule at `reference-semantics/semantics/sort.k:31` (through line 35)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

### rule at `reference-semantics/semantics/sort.k:36` (through line 39)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### rule at `reference-semantics/semantics/sort.k:40` (through line 48)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]

  // ==== keyed / reversed sorted() (WP2) =====================================
  // sortKeyVS(VS, KV): the stable ascending sort of VS by the key value KV
  // (a closure/builtin/type — anything callable). OPAQUE here; the concrete
  // leg (MPY-CONCRETE, llvm only) computes keys by REAL calls and stable-
  // inserts, at priority(40) over these.
```

### syntax at `reference-semantics/semantics/sort.k:49` (through line 49)

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### syntax at `reference-semantics/semantics/sort.k:51` (through line 52)

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### rule at `reference-semantics/semantics/sort.k:53` (through line 53)

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### rule at `reference-semantics/semantics/sort.k:54` (through line 54)

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### rule at `reference-semantics/semantics/sort.k:55` (through line 55)

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### syntax at `reference-semantics/semantics/sort.k:57` (through line 57)

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### rule at `reference-semantics/semantics/sort.k:58` (through line 58)

```k
  rule condRev(S:ValSeq, false) => S
```

### rule at `reference-semantics/semantics/sort.k:59` (through line 59)

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### rule at `reference-semantics/semantics/sort.k:61` (through line 62)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### rule at `reference-semantics/semantics/sort.k:63` (through line 64)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### rule at `reference-semantics/semantics/sort.k:65` (through line 71)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
```

## `reference-semantics/semantics/str.k`

### rule at `reference-semantics/semantics/str.k:8` (through line 8)

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### rule at `reference-semantics/semantics/str.k:9` (through line 12)

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### syntax at `reference-semantics/semantics/str.k:13` (through line 13)

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### rule at `reference-semantics/semantics/str.k:14` (through line 14)

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### rule at `reference-semantics/semantics/str.k:15` (through line 15)

```k
  rule strToCodes("") => .IntSeq
```

### rule at `reference-semantics/semantics/str.k:16` (through line 19)

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

### syntax at `reference-semantics/semantics/str.k:20` (through line 20)

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/str.k:21` (through line 21)

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### rule at `reference-semantics/semantics/str.k:22` (through line 22)

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### rule at `reference-semantics/semantics/str.k:24` (through line 24)

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### rule at `reference-semantics/semantics/str.k:25` (through line 25)

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### rule at `reference-semantics/semantics/str.k:26` (through line 28)

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### rule at `reference-semantics/semantics/str.k:29` (through line 29)

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### rule at `reference-semantics/semantics/str.k:30` (through line 30)

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### syntax at `reference-semantics/semantics/str.k:32` (through line 32)

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/str.k:33` (through line 33)

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### rule at `reference-semantics/semantics/str.k:34` (through line 34)

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule at `reference-semantics/semantics/str.k:35` (through line 35)

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### syntax at `reference-semantics/semantics/str.k:37` (through line 37)

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/str.k:38` (through line 38)

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### rule at `reference-semantics/semantics/str.k:39` (through line 39)

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### rule at `reference-semantics/semantics/str.k:40` (through line 47)

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))

  // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
  // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
  // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
  // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
  // str </<=/>/>= comparisons.
```

### syntax at `reference-semantics/semantics/str.k:48` (through line 48)

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### rule at `reference-semantics/semantics/str.k:49` (through line 49)

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### rule at `reference-semantics/semantics/str.k:50` (through line 50)

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### rule at `reference-semantics/semantics/str.k:51` (through line 51)

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule at `reference-semantics/semantics/str.k:52` (through line 52)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### rule at `reference-semantics/semantics/str.k:53` (through line 53)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### rule at `reference-semantics/semantics/str.k:54` (through line 54)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### rule at `reference-semantics/semantics/str.k:56` (through line 56)

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### rule at `reference-semantics/semantics/str.k:57` (through line 57)

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### rule at `reference-semantics/semantics/str.k:58` (through line 58)

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### rule at `reference-semantics/semantics/str.k:59` (through line 59)

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## `reference-semantics/semantics/subscript.k`

### syntax at `reference-semantics/semantics/subscript.k:11` (through line 11)

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### rule at `reference-semantics/semantics/subscript.k:12` (through line 12)

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### rule at `reference-semantics/semantics/subscript.k:13` (through line 14)

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### syntax at `reference-semantics/semantics/subscript.k:16` (through line 16)

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### rule at `reference-semantics/semantics/subscript.k:17` (through line 17)

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### rule at `reference-semantics/semantics/subscript.k:18` (through line 19)

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### syntax at `reference-semantics/semantics/subscript.k:21` (through line 21)

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### rule at `reference-semantics/semantics/subscript.k:22` (through line 22)

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### rule at `reference-semantics/semantics/subscript.k:23` (through line 26)

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### context at `reference-semantics/semantics/subscript.k:27` (through line 27)

```k
  context Subscript(HOLE, _)
```

### context at `reference-semantics/semantics/subscript.k:28` (through line 30)

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### rule at `reference-semantics/semantics/subscript.k:31` (through line 33)

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at `reference-semantics/semantics/subscript.k:35` (through line 35)

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### syntax at `reference-semantics/semantics/subscript.k:37` (through line 37)

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### rule at `reference-semantics/semantics/subscript.k:38` (through line 38)

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### rule at `reference-semantics/semantics/subscript.k:39` (through line 39)

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### rule at `reference-semantics/semantics/subscript.k:40` (through line 43)

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### syntax at `reference-semantics/semantics/subscript.k:44` (through line 47)

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### syntax at `reference-semantics/semantics/subscript.k:49` (through line 49)

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### rule at `reference-semantics/semantics/subscript.k:50` (through line 50)

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### rule at `reference-semantics/semantics/subscript.k:51` (through line 51)

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### rule at `reference-semantics/semantics/subscript.k:52` (through line 52)

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### rule at `reference-semantics/semantics/subscript.k:54` (through line 54)

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### rule at `reference-semantics/semantics/subscript.k:55` (through line 55)

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### rule at `reference-semantics/semantics/subscript.k:56` (through line 57)

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### rule at `reference-semantics/semantics/subscript.k:58` (through line 60)

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### rule at `reference-semantics/semantics/subscript.k:61` (through line 61)

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### syntax at `reference-semantics/semantics/subscript.k:63` (through line 63)

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### rule at `reference-semantics/semantics/subscript.k:64` (through line 65)

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### rule at `reference-semantics/semantics/subscript.k:66` (through line 67)

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### rule at `reference-semantics/semantics/subscript.k:68` (through line 71)

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### syntax at `reference-semantics/semantics/subscript.k:72` (through line 72)

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### rule at `reference-semantics/semantics/subscript.k:73` (through line 73)

```k
  rule slStep(noB)          => 1
```

### rule at `reference-semantics/semantics/subscript.k:74` (through line 74)

```k
  rule slStep(someB(S:Int)) => S
```

### syntax at `reference-semantics/semantics/subscript.k:76` (through line 76)

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### rule at `reference-semantics/semantics/subscript.k:77` (through line 78)

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### rule at `reference-semantics/semantics/subscript.k:79` (through line 80)

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### rule at `reference-semantics/semantics/subscript.k:81` (through line 81)

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### syntax at `reference-semantics/semantics/subscript.k:83` (through line 83)

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### rule at `reference-semantics/semantics/subscript.k:84` (through line 85)

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### rule at `reference-semantics/semantics/subscript.k:86` (through line 87)

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### rule at `reference-semantics/semantics/subscript.k:88` (through line 88)

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### syntax at `reference-semantics/semantics/subscript.k:90` (through line 90)

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### rule at `reference-semantics/semantics/subscript.k:91` (through line 92)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### rule at `reference-semantics/semantics/subscript.k:93` (through line 94)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### syntax at `reference-semantics/semantics/subscript.k:96` (through line 96)

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### rule at `reference-semantics/semantics/subscript.k:97` (through line 98)

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### rule at `reference-semantics/semantics/subscript.k:99` (through line 100)

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### syntax at `reference-semantics/semantics/subscript.k:102` (through line 102)

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### rule at `reference-semantics/semantics/subscript.k:103` (through line 104)

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### rule at `reference-semantics/semantics/subscript.k:105` (through line 108)

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

### syntax at `reference-semantics/semantics/subscript.k:109` (through line 109)

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### rule at `reference-semantics/semantics/subscript.k:110` (through line 112)

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### rule at `reference-semantics/semantics/subscript.k:113` (through line 114)

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### syntax at `reference-semantics/semantics/subscript.k:116` (through line 116)

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### rule at `reference-semantics/semantics/subscript.k:117` (through line 119)

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### rule at `reference-semantics/semantics/subscript.k:120` (through line 121)

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## `reference-semantics/semantics/syntax.k`

### syntax at `reference-semantics/semantics/syntax.k:9` (through line 30)

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

### syntax at `reference-semantics/semantics/syntax.k:32` (through line 32)

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### syntax at `reference-semantics/semantics/syntax.k:33` (through line 33)

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### syntax at `reference-semantics/semantics/syntax.k:34` (through line 34)

```k
  syntax Entries  ::= List{Entry, ","}
```

### syntax at `reference-semantics/semantics/syntax.k:35` (through line 35)

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### syntax at `reference-semantics/semantics/syntax.k:36` (through line 36)

```k
  syntax CompFors ::= List{CompFor, ""}
```

### syntax at `reference-semantics/semantics/syntax.k:37` (through line 37)

```k
  syntax Exprs    ::= List{Expr, ","}
```

### syntax at `reference-semantics/semantics/syntax.k:38` (through line 38)

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### syntax at `reference-semantics/semantics/syntax.k:39` (through line 39)

```k
  syntax Bound    ::= Expr | "NoBound"
```

### syntax at `reference-semantics/semantics/syntax.k:41` (through line 54)

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

### syntax at `reference-semantics/semantics/syntax.k:56` (through line 56)

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### syntax at `reference-semantics/semantics/syntax.k:57` (through line 57)

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### syntax at `reference-semantics/semantics/syntax.k:58` (through line 58)

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### syntax at `reference-semantics/semantics/syntax.k:59` (through line 59)

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### syntax at `reference-semantics/semantics/syntax.k:60` (through line 60)

```k
  syntax ParamNames ::= List{String, ","}
```

### syntax at `reference-semantics/semantics/syntax.k:61` (through line 61)

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## `reference-semantics/semantics/tuple.k`

### rule at `reference-semantics/semantics/tuple.k:10` (through line 10)

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### rule at `reference-semantics/semantics/tuple.k:11` (through line 13)

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### syntax at `reference-semantics/semantics/tuple.k:14` (through line 14)

```k
  syntax ApplyK ::= "toTuple"
```

### rule at `reference-semantics/semantics/tuple.k:15` (through line 15)

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### rule at `reference-semantics/semantics/tuple.k:16` (through line 16)

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### rule at `reference-semantics/semantics/tuple.k:18` (through line 19)

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### rule at `reference-semantics/semantics/tuple.k:20` (through line 20)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### rule at `reference-semantics/semantics/tuple.k:21` (through line 22)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### rule at `reference-semantics/semantics/tuple.k:23` (through line 23)

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### syntax at `reference-semantics/semantics/tuple.k:24` (through line 24)

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### rule at `reference-semantics/semantics/tuple.k:25` (through line 25)

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### rule at `reference-semantics/semantics/tuple.k:26` (through line 27)

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### rule at `reference-semantics/semantics/tuple.k:28` (through line 30)

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### syntax at `reference-semantics/semantics/tuple.k:31` (through line 31)

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### rule at `reference-semantics/semantics/tuple.k:32` (through line 34)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### rule at `reference-semantics/semantics/tuple.k:35` (through line 41)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### rule at `reference-semantics/semantics/tuple.k:42` (through line 42)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### rule at `reference-semantics/semantics/tuple.k:43` (through line 43)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### rule at `reference-semantics/semantics/tuple.k:44` (through line 48)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### syntax at `reference-semantics/semantics/tuple.k:49` (through line 49)

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### rule at `reference-semantics/semantics/tuple.k:50` (through line 50)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### rule at `reference-semantics/semantics/tuple.k:51` (through line 51)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### rule at `reference-semantics/semantics/tuple.k:52` (through line 54)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### rule at `reference-semantics/semantics/tuple.k:55` (through line 56)

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### rule at `reference-semantics/semantics/tuple.k:57` (through line 57)

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## `verification.k`

### syntax at `verification.k:7` (through line 7)

```k
  syntax KItem ::= "#runSumToN" "(" Int ")"
```

### rule at `verification.k:8` (through line 23)

```k
  rule #runSumToN(N:Int)
    => #loadAll(
         Module(
           FuncDef(
             "sum_to_n",
             Params("n"),
             Return(
               BinOp(
                 "//",
                 BinOp("*", Name("n"), BinOp("+", Name("n"), Int(1))),
                 Int(2))))))
       ~> Call(Name("sum_to_n"), Int(N), .Exprs)

  // Mathematical triangular number.  This spells floor division exactly as
  // the supplied Python semantics does.  For N >= 0, N * (N + 1) is even, so
  // this is the standard N * (N + 1) / 2 closed form.
```

### syntax at `verification.k:24` (through line 24)

```k
  syntax Int ::= triangular(Int) [function, total]
```

### rule at `verification.k:25` (through line 26)

```k
  rule triangular(N:Int)
    => (N *Int (N +Int 1) -Int pyMod(N *Int (N +Int 1), 2)) /Int 2
```

## `spec.k`

### claim at `spec.k:6` (through line 34)

```k
  claim
    <k> #runSumToN(N) => triangular(N) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "sum_to_n"
               |-> closureVal(
                     "n",
                     Return(
                       BinOp(
                         "//",
                         BinOp("*", Name("n"), BinOp("+", Name("n"), Int(1))),
                         Int(2)))
                     .Stmts,
                     0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
```

## Counts

- claim: 1
- configuration: 1
- context: 5
- endmodule: 27
- imports: 88
- module: 27
- requires: 25
- rule: 697
- syntax: 229

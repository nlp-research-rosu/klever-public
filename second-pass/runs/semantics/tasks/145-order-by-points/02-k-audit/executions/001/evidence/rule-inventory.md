# Exhaustive K declaration and rule inventory

Sources are the trusted supplied semantics plus candidate proof sources.

## /reference/reference-semantics/semantics.k

Entries: 0

## /reference/reference-semantics/semantics/assert.k

Entries: 3

### 1. lines 6-7: rule

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### 2. lines 8-12: rule

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### 3. lines 13-15: rule, priority

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## /reference/reference-semantics/semantics/bool.k

Entries: 14

### 1. lines 8-9: rule

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### 2. lines 10-10: rule

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### 3. lines 11-15: rule

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### 4. lines 16-16: context

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### 5. lines 17-17: rule

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### 6. lines 18-19: rule

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### 7. lines 20-21: rule

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### 8. lines 22-23: rule

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### 9. lines 24-28: rule

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

### 10. lines 29-30: rule, priority

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### 11. lines 31-34: rule, priority

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### 12. lines 35-38: rule, priority

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### 13. lines 39-42: rule, priority

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### 14. lines 43-46: rule, priority

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## /reference/reference-semantics/semantics/builtins.k

Entries: 175

### 1. lines 17-19: syntax, function

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### 2. lines 20-20: syntax, function

```k
  syntax Int ::= seqLen(Val) [function]
```

### 3. lines 21-21: rule

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### 4. lines 22-22: rule

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### 5. lines 23-23: rule

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### 6. lines 24-24: rule

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### 7. lines 25-25: rule

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### 8. lines 26-31: rule

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### 9. lines 32-32: rule

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### 10. lines 33-33: rule

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### 11. lines 34-34: rule

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### 12. lines 35-35: rule

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### 13. lines 36-36: syntax, function, total

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### 14. lines 37-37: rule

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### 15. lines 38-40: rule

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### 16. lines 41-43: rule

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### 17. lines 44-46: rule

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### 18. lines 47-47: syntax

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### 19. lines 48-48: rule

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### 20. lines 49-49: rule

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### 21. lines 50-53: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### 22. lines 54-54: syntax, function

```k
  syntax Int ::= intOf(Val) [function]
```

### 23. lines 55-55: rule

```k
  rule intOf(I:Int)  => I
```

### 24. lines 56-58: rule

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### 25. lines 59-59: syntax

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### 26. lines 60-60: rule

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### 27. lines 61-61: rule

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### 28. lines 62-63: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### 29. lines 64-66: rule

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### 30. lines 67-67: syntax

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### 31. lines 68-68: rule

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### 32. lines 69-69: rule

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### 33. lines 70-71: rule

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### 34. lines 72-75: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

### 35. lines 76-76: syntax

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### 36. lines 77-77: rule

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### 37. lines 78-79: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### 38. lines 80-80: rule

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### 39. lines 81-81: rule

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### 40. lines 82-85: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### 41. lines 86-86: syntax

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### 42. lines 87-87: rule

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### 43. lines 88-89: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### 44. lines 90-90: rule

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### 45. lines 91-91: rule

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### 46. lines 92-96: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

### 47. lines 97-97: syntax, function

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### 48. lines 98-98: rule

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### 49. lines 99-99: rule

```k
  rule maxVals(M:Int, .Vals)           => M
```

### 50. lines 100-101: rule

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### 51. lines 102-102: syntax, function

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### 52. lines 103-103: rule

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### 53. lines 104-104: rule

```k
  rule minVals(M:Int, .Vals)           => M
```

### 54. lines 105-107: rule

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### 55. lines 108-110: rule

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

### 56. lines 111-113: rule

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### 57. lines 114-114: syntax, function, total

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### 58. lines 115-115: rule

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### 59. lines 116-116: rule

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### 60. lines 117-117: syntax, function, total

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### 61. lines 118-118: rule

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### 62. lines 119-123: rule

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

### 63. lines 124-125: rule

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### 64. lines 126-126: syntax, function, total

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### 65. lines 127-127: rule

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### 66. lines 128-131: rule

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### 67. lines 132-133: rule

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### 68. lines 134-134: syntax, function, total

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### 69. lines 135-135: rule

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### 70. lines 136-136: rule

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### 71. lines 137-139: rule

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### 72. lines 140-142: rule

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### 73. lines 143-143: rule

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### 74. lines 144-147: rule

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

### 75. lines 148-148: rule

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### 76. lines 149-151: rule

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### 77. lines 152-155: rule

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

### 78. lines 156-157: rule

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### 79. lines 158-158: syntax, function, total

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### 80. lines 159-159: rule

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### 81. lines 160-162: rule

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### 82. lines 163-163: rule

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### 83. lines 164-166: rule

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### 84. lines 167-168: rule

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### 85. lines 169-169: rule

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### 86. lines 170-170: rule

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### 87. lines 171-172: rule

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### 88. lines 173-173: rule

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### 89. lines 174-176: rule

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### 90. lines 177-177: rule

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### 91. lines 178-178: rule

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### 92. lines 179-186: rule, concrete

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0

  // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
  // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
  // trusted pass evaluator, now DEFINED in the reference and driven by a
  // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
  // argument leaves the call unevaluated for problem-level folds.
```

### 93. lines 187-187: rule

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### 94. lines 188-188: syntax, function

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### 95. lines 189-191: rule

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### 96. lines 192-193: syntax

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### 97. lines 194-194: syntax, function, total

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### 98. lines 195-195: rule

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### 99. lines 196-196: syntax, function, total

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### 100. lines 197-197: rule

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### 101. lines 198-198: rule, owise

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### 102. lines 199-199: syntax, function, total

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### 103. lines 200-200: rule

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### 104. lines 201-202: rule, owise

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### 105. lines 203-203: syntax, function, total

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### 106. lines 204-204: rule

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### 107. lines 205-205: rule

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### 108. lines 206-206: rule

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### 109. lines 207-207: rule

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### 110. lines 208-208: rule

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### 111. lines 209-209: rule

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### 112. lines 210-210: rule

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### 113. lines 211-211: rule

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### 114. lines 212-213: rule

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### 115. lines 214-215: syntax, function, total

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### 116. lines 216-216: rule

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### 117. lines 217-217: rule

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### 118. lines 218-218: rule

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### 119. lines 219-220: rule

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### 120. lines 221-222: rule

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### 121. lines 223-224: rule, owise

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### 122. lines 225-225: syntax

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### 123. lines 226-226: syntax, function, total

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### 124. lines 227-227: rule

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### 125. lines 228-229: rule, owise

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### 126. lines 230-230: syntax, function, total

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### 127. lines 231-231: rule

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### 128. lines 232-232: rule

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### 129. lines 233-233: rule

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### 130. lines 234-234: rule

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### 131. lines 235-235: rule

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### 132. lines 236-237: rule, owise

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### 133. lines 238-238: syntax, function, total

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### 134. lines 239-239: rule

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### 135. lines 240-240: rule

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### 136. lines 241-242: rule

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### 137. lines 243-243: rule, owise

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### 138. lines 244-244: syntax, function, total

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### 139. lines 245-245: rule

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### 140. lines 246-246: rule

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### 141. lines 247-247: syntax, function, total

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### 142. lines 248-249: rule

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### 143. lines 250-250: syntax, function, total

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### 144. lines 251-251: rule

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### 145. lines 252-252: rule

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### 146. lines 253-253: rule

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### 147. lines 254-254: rule

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### 148. lines 255-255: syntax, function, total

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### 149. lines 256-256: rule

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### 150. lines 257-259: rule

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### 151. lines 260-262: rule

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### 152. lines 263-264: rule, owise

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### 153. lines 265-265: syntax, function, total

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### 154. lines 266-266: rule

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### 155. lines 267-267: rule

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### 156. lines 268-268: rule, owise

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### 157. lines 269-269: syntax, function, total

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### 158. lines 270-270: rule

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### 159. lines 271-271: rule

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### 160. lines 272-272: syntax, function, total

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### 161. lines 273-273: rule

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### 162. lines 274-278: rule, concrete

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### 163. lines 279-279: syntax

```k
  syntax KItem ::= "#md5"
```

### 164. lines 280-281: rule, priority

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### 165. lines 282-282: rule

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### 166. lines 283-283: syntax

```k
  syntax Val ::= md5Obj(IntSeq)
```

### 167. lines 284-284: rule

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### 168. lines 285-290: syntax, function, total, concrete, owise, symbol, no-evaluators, opaque

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### 169. lines 291-291: rule

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### 170. lines 292-292: rule

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### 171. lines 293-293: syntax, function

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### 172. lines 294-294: rule

```k
  rule isIntV(_:Int)         => true
```

### 173. lines 295-295: rule, owise

```k
  rule isIntV(_:Val)         => false [owise]
```

### 174. lines 296-296: rule

```k
  rule isStrV(str(_:IntSeq)) => true
```

### 175. lines 297-297: rule, owise

```k
  rule isStrV(_:Val)         => false [owise]
```

## /reference/reference-semantics/semantics/call.k

Entries: 24

### 1. lines 16-18: rule, owise

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### 2. lines 19-19: syntax

```k
  syntax KItem ::= #callee(Exprs)
```

### 3. lines 20-20: rule, owise

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### 4. lines 21-23: rule

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### 5. lines 24-25: rule

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### 6. lines 26-26: rule

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### 7. lines 27-27: rule

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### 8. lines 28-28: rule

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### 9. lines 29-29: rule

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### 10. lines 30-30: rule

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### 11. lines 31-31: rule, owise

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### 12. lines 32-37: rule

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### 13. lines 38-41: rule, priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 14. lines 42-46: rule, priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### 15. lines 47-51: rule, priority

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 16. lines 52-52: syntax, function, total

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### 17. lines 53-55: rule

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### 18. lines 56-62: rule, priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
  // non-mutating methods READ their heap-object arguments too (join's list);
  // mutators keep refs (append of a list into a list-of-lists stays aliased)
```

### 19. lines 63-68: rule, priority

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### 20. lines 69-79: rule

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

### 21. lines 80-86: rule

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### 22. lines 87-87: syntax

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### 23. lines 88-88: rule

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### 24. lines 89-94: rule

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

## /reference/reference-semantics/semantics/comprehension.k

Entries: 10

### 1. lines 11-11: rule

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### 2. lines 12-13: rule

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### 3. lines 14-14: syntax, macro

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### 4. lines 15-17: rule

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### 5. lines 18-18: syntax, macro, macro-rec

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### 6. lines 19-20: rule

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### 7. lines 21-23: rule

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### 8. lines 24-24: syntax, macro

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### 9. lines 25-25: rule

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### 10. lines 26-26: rule

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## /reference/reference-semantics/semantics/concrete.k

Entries: 21

### 1. lines 13-15: rule

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### 2. lines 16-24: rule, concrete, priority

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

### 3. lines 25-25: syntax

```k
  syntax Val ::= kvP(Val, Val)
```

### 4. lines 26-27: syntax

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### 5. lines 28-30: rule, priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### 6. lines 31-33: rule, priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### 7. lines 34-35: rule

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### 8. lines 36-37: rule

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### 9. lines 38-41: rule

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### 10. lines 42-42: syntax, function

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### 11. lines 43-43: rule

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### 12. lines 44-46: rule

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### 13. lines 47-50: rule

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### 14. lines 51-51: syntax, function

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### 15. lines 52-52: rule

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### 16. lines 53-53: rule

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### 17. lines 54-55: rule

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### 18. lines 56-56: syntax, function, total

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### 19. lines 57-57: rule

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### 20. lines 58-58: rule

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### 21. lines 59-59: rule, owise

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## /reference/reference-semantics/semantics/controls.k

Entries: 37

### 1. lines 9-11: rule

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### 2. lines 12-19: rule, priority

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### 3. lines 20-26: rule

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
  // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
  // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
  // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
```

### 4. lines 27-34: rule, priority

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]

  // ==== import trivia: `from math import floor, ceil` binds the supported
  // names as builtins in the current scope; every other import is a no-op
```

### 5. lines 35-35: rule

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### 6. lines 36-36: rule, owise

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### 7. lines 37-37: syntax

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### 8. lines 38-38: rule

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### 9. lines 39-42: rule

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### 10. lines 43-47: rule

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

### 11. lines 48-50: rule

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### 12. lines 51-51: syntax

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### 13. lines 52-52: rule

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### 14. lines 53-53: rule

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### 15. lines 54-56: rule

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### 16. lines 57-58: rule

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### 17. lines 59-64: rule

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

### 18. lines 65-68: syntax

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### 19. lines 69-70: rule

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### 20. lines 71-71: rule

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### 21. lines 72-72: rule

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### 22. lines 73-76: rule

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### 23. lines 77-77: rule

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### 24. lines 78-78: rule

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### 25. lines 79-80: rule

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### 26. lines 81-84: rule

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

### 27. lines 85-85: rule

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### 28. lines 86-86: rule

```k
  rule <k> Continue => #cont ... </k>
```

### 29. lines 87-87: rule

```k
  rule <k> Break => #brk ... </k>
```

### 30. lines 88-88: rule

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### 31. lines 89-89: rule, owise

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### 32. lines 90-90: rule

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### 33. lines 91-94: rule, owise, priority

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### 34. lines 95-97: rule, priority

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 35. lines 98-100: rule, priority

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 36. lines 101-105: rule, priority

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### 37. lines 106-108: rule, priority

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## /reference/reference-semantics/semantics/core.k

Entries: 84

### 1. lines 13-13: syntax

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### 2. lines 14-14: syntax

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### 3. lines 15-17: syntax

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### 4. lines 18-24: syntax

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### 5. lines 25-35: syntax, function

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

### 6. lines 36-36: syntax

```k
  syntax Parent   ::= "root" | parent(Int)
```

### 7. lines 37-37: syntax

```k
  syntax Scope    ::= scope(Map, Parent)
```

### 8. lines 38-38: syntax

```k
  syntax KResult  ::= Val
```

### 9. lines 39-39: syntax

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### 10. lines 40-40: syntax

```k
  syntax Vals     ::= List{Val, ","}
```

### 11. lines 41-41: syntax

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### 12. lines 42-48: syntax

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### 13. lines 49-67: configuration

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

### 14. lines 68-68: syntax, function, total

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### 15. lines 69-69: rule

```k
  rule isRefV(ref(_:Int)) => true
```

### 16. lines 70-74: rule, owise

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### 17. lines 75-75: syntax

```k
  syntax HeapVal ::= cellV(Val)
```

### 18. lines 76-76: syntax, function, total

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### 19. lines 77-77: rule

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### 20. lines 78-84: rule, function, owise

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

### 21. lines 85-94: rule, priority

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

### 22. lines 95-95: syntax

```k
  syntax Val ::= kwV(String, Val)
```

### 23. lines 96-96: syntax

```k
  syntax KItem ::= #kwTag(String)
```

### 24. lines 97-97: rule

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### 25. lines 98-99: rule

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### 26. lines 100-100: syntax, function, total

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### 27. lines 101-101: rule

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### 28. lines 102-105: rule, owise

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### 29. lines 106-106: syntax

```k
  syntax Val ::= cellsMark(ParamNames)
```

### 30. lines 107-107: syntax, function

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### 31. lines 108-108: rule

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### 32. lines 109-109: syntax, function, total

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### 33. lines 110-110: rule

```k
  rule pnMember(_:String, .ParamNames) => false
```

### 34. lines 111-112: rule

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### 35. lines 113-113: syntax

```k
  syntax KItem ::= #cellW(Val, Val)
```

### 36. lines 114-116: rule

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### 37. lines 117-117: syntax

```k
  syntax KItem ::= #alloc(Val)
```

### 38. lines 118-123: rule

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

### 39. lines 124-124: syntax

```k
  syntax KItem ::= #loadAll(Module)
```

### 40. lines 125-125: rule

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### 41. lines 126-126: rule

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### 42. lines 127-129: rule

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### 43. lines 130-130: syntax

```k
  syntax KItem ::= #look(String, Int)
```

### 44. lines 131-131: rule

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### 45. lines 132-144: rule, function, concrete, priority

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

### 46. lines 145-151: rule, priority

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### 47. lines 152-156: rule

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

### 48. lines 157-157: syntax, function, total

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### 49. lines 158-184: rule

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

### 50. lines 185-185: syntax

```k
  syntax ApplyK ::= toCall(Val)
```

### 51. lines 186-188: syntax

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### 52. lines 189-189: rule

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### 53. lines 190-190: rule

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### 54. lines 191-193: rule

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### 55. lines 194-194: rule

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### 56. lines 195-195: rule

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### 57. lines 196-198: rule

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### 58. lines 199-199: syntax, function

```k
  syntax Bool ::= truthy(Val) [function]
```

### 59. lines 200-200: rule

```k
  rule truthy(B:Bool)          => B
```

### 60. lines 201-201: rule

```k
  rule truthy(noneV)           => false
```

### 61. lines 202-202: rule

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### 62. lines 203-203: rule

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### 63. lines 204-204: rule

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### 64. lines 205-207: rule

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### 65. lines 208-208: syntax, function

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### 66. lines 209-209: syntax, function

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### 67. lines 210-212: syntax, function

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### 68. lines 213-213: syntax, function, total

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### 69. lines 214-214: rule

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### 70. lines 215-216: rule

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### 71. lines 217-217: syntax, function, total

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### 72. lines 218-218: rule

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### 73. lines 219-222: rule

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### 74. lines 223-223: syntax, function, total

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### 75. lines 224-224: rule

```k
  rule vsLen(.ValSeq)                => 0
```

### 76. lines 225-226: rule

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### 77. lines 227-227: syntax, function, total

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### 78. lines 228-228: rule

```k
  rule isLen(.IntSeq)                => 0
```

### 79. lines 229-232: rule, total

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### 80. lines 233-233: syntax, function, total

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### 81. lines 234-234: rule

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### 82. lines 235-235: rule

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### 83. lines 236-237: rule

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### 84. lines 238-239: rule

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

## /reference/reference-semantics/semantics/dict.k

Entries: 40

### 1. lines 20-22: syntax

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### 2. lines 23-25: syntax

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### 3. lines 26-26: rule

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### 4. lines 27-27: rule

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### 5. lines 28-29: rule

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### 6. lines 30-31: rule

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### 7. lines 32-36: rule, total, concrete

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### 8. lines 37-37: syntax, function, total

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### 9. lines 38-38: rule

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### 10. lines 39-39: rule

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### 11. lines 40-42: rule

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### 12. lines 43-43: syntax, function, total

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### 13. lines 44-44: rule

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### 14. lines 45-48: rule, owise

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### 15. lines 49-49: syntax, function, total

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### 16. lines 50-51: rule

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### 17. lines 52-53: rule

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### 18. lines 54-57: rule, owise

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### 19. lines 58-62: rule, priority

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### 20. lines 63-63: rule

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### 21. lines 64-64: syntax, function

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### 22. lines 65-69: rule, priority

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### 23. lines 70-70: syntax, function

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### 24. lines 71-75: rule

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### 25. lines 76-76: syntax

```k
  syntax KItem ::= #dsetK(String, Val)
```

### 26. lines 77-77: rule

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### 27. lines 78-81: rule

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### 28. lines 82-85: rule

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### 29. lines 86-86: syntax

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### 30. lines 87-89: rule

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### 31. lines 90-90: syntax, function, total

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### 32. lines 91-91: rule

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### 33. lines 92-94: rule

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### 34. lines 95-96: rule

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### 35. lines 97-97: syntax, function

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### 36. lines 98-98: rule

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### 37. lines 99-100: rule

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### 38. lines 101-101: syntax, function

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### 39. lines 102-102: rule

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### 40. lines 103-103: rule

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## /reference/reference-semantics/semantics/float.k

Entries: 155

### 1. lines 20-20: syntax

```k
  syntax Val ::= Float
```

### 2. lines 21-23: rule, concrete, no-evaluators

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### 3. lines 24-24: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### 4. lines 25-26: rule, concrete

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### 5. lines 27-29: rule, concrete

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### 6. lines 30-30: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### 7. lines 31-31: rule, concrete

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### 8. lines 32-36: rule, concrete

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### 9. lines 37-37: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### 10. lines 38-38: rule, concrete

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### 11. lines 39-42: rule, concrete

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### 12. lines 43-43: rule

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### 13. lines 44-49: rule, concrete, no-evaluators

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### 14. lines 50-50: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### 15. lines 51-51: rule, concrete

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### 16. lines 52-53: rule

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### 17. lines 54-54: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### 18. lines 55-55: rule, concrete

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### 19. lines 56-60: rule

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### 20. lines 61-64: rule, priority

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### 21. lines 65-65: syntax

```k
  syntax KItem ::= "#mathCeil"
```

### 22. lines 66-66: rule, priority

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### 23. lines 67-69: rule

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### 24. lines 70-70: syntax

```k
  syntax KItem ::= "#mathFloor"
```

### 25. lines 71-71: rule, priority

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### 26. lines 72-72: rule

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### 27. lines 73-73: syntax, function, total, symbol

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### 28. lines 74-74: rule, concrete

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### 29. lines 75-77: rule, concrete

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### 30. lines 78-78: rule

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### 31. lines 79-81: rule

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### 32. lines 82-82: syntax

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### 33. lines 83-83: rule, priority

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### 34. lines 84-84: rule

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### 35. lines 85-85: rule

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### 36. lines 86-86: syntax, function, total, symbol

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### 37. lines 87-87: rule, concrete

```k
  rule toF(F:Float) => F        [concrete]
```

### 38. lines 88-92: rule, concrete

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### 39. lines 93-93: syntax, function, total, symbol

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### 40. lines 94-94: rule, concrete

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### 41. lines 95-98: rule, concrete

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### 42. lines 99-102: rule, concrete, no-evaluators

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### 43. lines 103-103: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### 44. lines 104-104: rule, concrete

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### 45. lines 105-106: rule

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### 46. lines 107-107: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### 47. lines 108-108: rule, concrete

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### 48. lines 109-110: rule

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### 49. lines 111-111: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### 50. lines 112-112: rule, concrete

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### 51. lines 113-114: rule

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### 52. lines 115-115: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### 53. lines 116-116: rule, concrete

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### 54. lines 117-118: rule

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### 55. lines 119-119: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### 56. lines 120-120: rule, concrete

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### 57. lines 121-124: rule

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### 58. lines 125-125: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### 59. lines 126-126: rule, concrete

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### 60. lines 127-127: rule

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### 61. lines 128-128: rule

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### 62. lines 129-131: rule

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### 63. lines 132-132: rule

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### 64. lines 133-133: rule

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### 65. lines 134-134: rule

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### 66. lines 135-135: rule

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### 67. lines 136-136: rule

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### 68. lines 137-137: rule

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### 69. lines 138-138: rule

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### 70. lines 139-141: rule, concrete

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### 71. lines 142-142: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### 72. lines 143-143: rule, concrete

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### 73. lines 144-144: rule

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### 74. lines 145-145: rule

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### 75. lines 146-146: rule

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### 76. lines 147-147: rule

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### 77. lines 148-148: rule

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### 78. lines 149-149: rule

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### 79. lines 150-150: rule

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### 80. lines 151-153: rule

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### 81. lines 154-154: rule

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### 82. lines 155-159: rule, concrete

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### 83. lines 160-160: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### 84. lines 161-161: rule, concrete

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### 85. lines 162-164: rule, concrete

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### 86. lines 165-165: syntax, function

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### 87. lines 166-166: rule

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### 88. lines 167-167: syntax, function, total

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### 89. lines 168-168: rule

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### 90. lines 169-169: rule

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### 91. lines 170-170: rule

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### 92. lines 171-172: rule

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### 93. lines 173-173: syntax, function, total

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### 94. lines 174-174: rule

```k
  rule fracPart(.IntSeq) => 0
```

### 95. lines 175-175: rule

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### 96. lines 176-176: rule

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### 97. lines 177-177: rule

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### 98. lines 178-178: rule

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### 99. lines 179-179: syntax, function, total

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### 100. lines 180-180: rule

```k
  rule fracScale(.IntSeq) => 1
```

### 101. lines 181-181: rule

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### 102. lines 182-182: rule

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### 103. lines 183-183: rule

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### 104. lines 184-184: rule

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### 105. lines 185-185: rule

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### 106. lines 186-186: rule

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### 107. lines 187-189: rule

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### 108. lines 190-190: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### 109. lines 191-191: rule, concrete

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### 110. lines 192-194: rule

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### 111. lines 195-195: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### 112. lines 196-196: rule, concrete

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### 113. lines 197-197: rule

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### 114. lines 198-198: rule

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### 115. lines 199-199: rule

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### 116. lines 200-200: rule

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### 117. lines 201-201: rule

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### 118. lines 202-202: rule

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### 119. lines 203-203: rule

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### 120. lines 204-204: rule

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### 121. lines 205-205: rule

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### 122. lines 206-208: rule

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### 123. lines 209-209: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### 124. lines 210-210: rule, concrete

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### 125. lines 211-212: rule

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### 126. lines 213-213: rule

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### 127. lines 214-216: rule

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### 128. lines 217-217: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### 129. lines 218-222: rule, concrete

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### 130. lines 223-223: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### 131. lines 224-226: rule, concrete

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### 132. lines 227-227: rule

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### 133. lines 228-229: rule

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### 134. lines 230-230: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### 135. lines 231-231: rule, concrete

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### 136. lines 232-232: syntax

```k
  syntax KItem ::= "#mathSqrt"
```

### 137. lines 233-233: rule, priority

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### 138. lines 234-234: rule

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### 139. lines 235-242: rule, concrete, priority

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

### 140. lines 243-243: syntax

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### 141. lines 244-244: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### 142. lines 245-245: rule

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### 143. lines 246-246: rule

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### 144. lines 247-249: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### 145. lines 250-250: syntax

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### 146. lines 251-251: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### 147. lines 252-252: rule

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### 148. lines 253-253: rule

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### 149. lines 254-260: rule, concrete

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

### 150. lines 261-261: syntax

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### 151. lines 262-264: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### 152. lines 265-265: rule

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### 153. lines 266-266: rule

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### 154. lines 267-269: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### 155. lines 270-272: rule

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

## /reference/reference-semantics/semantics/functions.k

Entries: 19

### 1. lines 8-13: syntax

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### 2. lines 14-17: rule

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### 3. lines 18-18: syntax

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### 4. lines 19-26: rule

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

### 5. lines 27-30: syntax

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### 6. lines 31-32: syntax

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### 7. lines 33-35: rule

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### 8. lines 36-41: rule

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### 9. lines 42-46: rule

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### 10. lines 47-49: rule

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### 11. lines 50-52: rule

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### 12. lines 53-58: rule

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### 13. lines 59-62: rule

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### 14. lines 63-63: rule

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### 15. lines 64-67: rule

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### 16. lines 68-77: rule, priority

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

### 17. lines 78-79: rule

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### 18. lines 80-84: rule

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### 19. lines 85-90: rule

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## /reference/reference-semantics/semantics/int.k

Entries: 17

### 1. lines 7-8: rule

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### 2. lines 9-10: rule

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### 3. lines 11-11: rule

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### 4. lines 12-12: rule

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### 5. lines 13-13: rule

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### 6. lines 14-14: rule

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### 7. lines 15-15: rule

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### 8. lines 16-16: rule

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### 9. lines 17-18: rule

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### 10. lines 19-19: syntax, function

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### 11. lines 20-21: rule

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### 12. lines 22-22: rule

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### 13. lines 23-23: rule

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### 14. lines 24-24: rule

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### 15. lines 25-25: rule

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### 16. lines 26-26: rule

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### 17. lines 27-27: rule

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## /reference/reference-semantics/semantics/iter.k

Entries: 1

### 1. lines 8-8: syntax

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## /reference/reference-semantics/semantics/list.k

Entries: 32

### 1. lines 9-9: rule

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### 2. lines 10-12: rule

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### 3. lines 13-13: syntax

```k
  syntax ApplyK ::= "toList"
```

### 4. lines 14-14: rule

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### 5. lines 15-17: rule

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### 6. lines 18-18: syntax, function, total

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### 7. lines 19-19: rule

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### 8. lines 20-23: rule, priority

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### 9. lines 24-26: rule, priority

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### 10. lines 27-27: rule

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### 11. lines 28-32: rule, concrete

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### 12. lines 33-33: syntax, function, total

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### 13. lines 34-34: rule

```k
  rule hasRefVS(.ValSeq)                => false
```

### 14. lines 35-36: rule

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### 15. lines 37-38: syntax, function

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### 16. lines 39-39: rule

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### 17. lines 40-40: rule

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### 18. lines 41-41: rule

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### 19. lines 42-44: rule

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### 20. lines 45-46: rule

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### 21. lines 47-48: rule

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### 22. lines 49-49: rule

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### 23. lines 50-52: rule, owise

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### 24. lines 53-57: rule, priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### 25. lines 58-58: syntax

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### 26. lines 59-59: rule

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### 27. lines 60-60: rule

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### 28. lines 61-61: rule

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### 29. lines 62-62: rule

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### 30. lines 63-64: rule

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### 31. lines 65-66: rule

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### 32. lines 67-67: rule

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## /reference/reference-semantics/semantics/methods.k

Entries: 102

### 1. lines 10-12: syntax, function

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### 2. lines 13-13: rule

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### 3. lines 14-14: rule

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### 4. lines 15-15: rule

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### 5. lines 16-18: rule

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### 6. lines 19-19: rule

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### 7. lines 20-20: rule

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### 8. lines 21-25: rule

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### 9. lines 26-26: rule

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### 10. lines 27-27: syntax, function, total

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### 11. lines 28-28: rule

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### 12. lines 29-29: rule

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### 13. lines 30-33: rule

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### 14. lines 34-34: rule

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### 15. lines 35-35: syntax, function

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### 16. lines 36-36: rule

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### 17. lines 37-38: rule

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### 18. lines 39-40: rule

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### 19. lines 41-41: syntax, function, total

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### 20. lines 42-42: rule

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### 21. lines 43-43: rule, owise

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### 22. lines 44-46: rule

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### 23. lines 47-47: rule

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### 24. lines 48-48: syntax, function, total

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### 25. lines 49-49: rule

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### 26. lines 50-50: rule

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### 27. lines 51-51: rule

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### 28. lines 52-52: syntax, function, total

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### 29. lines 53-53: rule

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### 30. lines 54-54: rule

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### 31. lines 55-57: rule

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### 32. lines 58-60: rule

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### 33. lines 61-63: rule, concrete

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### 34. lines 64-64: rule

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### 35. lines 65-65: syntax, function, total

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### 36. lines 66-66: rule

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### 37. lines 67-67: rule

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### 38. lines 68-71: rule

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### 39. lines 72-74: rule, priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### 40. lines 75-75: syntax, function

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### 41. lines 76-76: rule

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### 42. lines 77-78: rule

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### 43. lines 79-81: rule

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

### 44. lines 82-82: syntax, function

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### 45. lines 83-83: rule

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### 46. lines 84-84: rule

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### 47. lines 85-85: syntax, function, total

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### 48. lines 86-88: rule

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### 49. lines 89-93: rule, priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### 50. lines 94-96: rule, priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### 51. lines 97-97: syntax, function

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### 52. lines 98-98: rule

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### 53. lines 99-100: rule

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### 54. lines 101-103: rule

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### 55. lines 104-105: rule

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### 56. lines 106-106: syntax, function, total

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### 57. lines 107-107: rule

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### 58. lines 108-108: rule

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### 59. lines 109-111: rule

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### 60. lines 112-112: syntax, function, total

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### 61. lines 113-114: rule

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### 62. lines 115-115: syntax, function, total

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### 63. lines 116-117: rule

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### 64. lines 118-118: syntax, function, total

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### 65. lines 119-120: rule

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### 66. lines 121-121: syntax, function, total

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### 67. lines 122-123: rule

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### 68. lines 124-124: syntax, function, total

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### 69. lines 125-125: rule

```k
  rule hasUpper(.IntSeq) => false
```

### 70. lines 126-127: rule

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### 71. lines 128-128: syntax, function, total

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### 72. lines 129-129: rule

```k
  rule hasLower(.IntSeq) => false
```

### 73. lines 130-131: rule

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### 74. lines 132-132: syntax, function, total

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### 75. lines 133-133: rule

```k
  rule allAlpha(.IntSeq) => true
```

### 76. lines 134-135: rule

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### 77. lines 136-136: syntax, function, total

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### 78. lines 137-137: rule

```k
  rule allDigit(.IntSeq) => true
```

### 79. lines 138-139: rule

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### 80. lines 140-141: syntax, function, total

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### 81. lines 142-142: rule

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### 82. lines 143-144: rule, owise

```k
  rule lowerC(C:Int) => C         [owise]
```

### 83. lines 145-145: syntax, function, total

```k
  syntax Int ::= upperC(Int) [function, total]
```

### 84. lines 146-146: rule

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### 85. lines 147-148: rule, owise

```k
  rule upperC(C:Int) => C         [owise]
```

### 86. lines 149-149: syntax, function, total

```k
  syntax Int ::= swapC(Int) [function, total]
```

### 87. lines 150-150: rule

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### 88. lines 151-151: rule

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### 89. lines 152-153: rule, owise

```k
  rule swapC(C:Int) => C         [owise]
```

### 90. lines 154-154: syntax, function, total

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### 91. lines 155-155: rule

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### 92. lines 156-157: rule

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### 93. lines 158-158: syntax, function, total

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### 94. lines 159-159: rule

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### 95. lines 160-161: rule

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### 96. lines 162-162: syntax, function, total

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### 97. lines 163-163: rule

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### 98. lines 164-165: rule

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### 99. lines 166-166: syntax, function, total

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### 100. lines 167-167: rule

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### 101. lines 168-168: rule

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### 102. lines 169-169: rule

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## /reference/reference-semantics/semantics/operators.k

Entries: 12

### 1. lines 10-11: rule

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### 2. lines 12-14: rule

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### 3. lines 15-15: context

```k
  context Compare(HOLE, _)
```

### 4. lines 16-16: context

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### 5. lines 17-18: rule, owise

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### 6. lines 19-19: rule

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### 7. lines 20-24: rule, priority

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### 8. lines 25-27: rule, priority

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 9. lines 28-33: rule, priority

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

### 10. lines 34-37: rule, priority

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### 11. lines 38-43: rule, priority

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### 12. lines 44-46: rule, priority

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## /reference/reference-semantics/semantics/range.k

Entries: 8

### 1. lines 9-9: syntax, function, total

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### 2. lines 10-11: rule

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### 3. lines 12-12: syntax, function

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### 4. lines 13-14: rule

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### 5. lines 15-16: rule

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### 6. lines 17-19: rule

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### 7. lines 20-22: rule

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### 8. lines 23-24: rule

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

## /reference/reference-semantics/semantics/set.k

Entries: 18

### 1. lines 8-10: syntax

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### 2. lines 11-11: syntax, function, total

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### 3. lines 12-12: rule

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### 4. lines 13-15: rule

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### 5. lines 16-17: syntax, function, total

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### 6. lines 18-18: rule

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### 7. lines 19-19: rule

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### 8. lines 20-21: rule

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### 9. lines 22-24: rule

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### 10. lines 25-25: syntax, function, total

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### 11. lines 26-26: rule

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### 12. lines 27-30: rule

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### 13. lines 31-31: syntax, function, total

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### 14. lines 32-32: rule

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### 15. lines 33-34: rule

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### 16. lines 35-35: syntax, function, total

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### 17. lines 36-38: rule

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### 18. lines 39-39: rule

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## /reference/reference-semantics/semantics/sort.k

Entries: 25

### 1. lines 18-18: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### 2. lines 19-19: syntax, function

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### 3. lines 20-20: rule, concrete

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### 4. lines 21-21: rule, concrete

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### 5. lines 22-22: rule, concrete

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### 6. lines 23-23: rule, concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### 7. lines 24-25: rule, concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### 8. lines 26-26: syntax, function

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### 9. lines 27-27: rule, concrete

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### 10. lines 28-28: rule, concrete

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### 11. lines 29-30: rule, concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### 12. lines 31-35: rule, concrete, owise

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

### 13. lines 36-39: rule

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### 14. lines 40-48: rule, concrete, priority

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

### 15. lines 49-50: syntax, function, total, symbol, no-evaluators, opaque

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### 16. lines 51-52: syntax, function, total

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### 17. lines 53-53: rule

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### 18. lines 54-54: rule

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### 19. lines 55-56: rule

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### 20. lines 57-57: syntax, function, total

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### 21. lines 58-58: rule

```k
  rule condRev(S:ValSeq, false) => S
```

### 22. lines 59-60: rule

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### 23. lines 61-62: rule

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### 24. lines 63-64: rule

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### 25. lines 65-71: rule, total, concrete

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
```

## /reference/reference-semantics/semantics/str.k

Entries: 33

### 1. lines 8-8: rule

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### 2. lines 9-12: rule

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### 3. lines 13-13: syntax, function

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### 4. lines 14-14: rule

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### 5. lines 15-15: rule

```k
  rule strToCodes("") => .IntSeq
```

### 6. lines 16-19: rule

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

### 7. lines 20-20: syntax, function, total

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### 8. lines 21-21: rule

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### 9. lines 22-23: rule

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### 10. lines 24-24: rule

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### 11. lines 25-25: rule

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### 12. lines 26-28: rule

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### 13. lines 29-29: rule

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### 14. lines 30-31: rule

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### 15. lines 32-32: syntax, function, total

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### 16. lines 33-33: rule

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### 17. lines 34-34: rule

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### 18. lines 35-36: rule

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### 19. lines 37-37: syntax, function, total

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### 20. lines 38-38: rule

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### 21. lines 39-39: rule

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### 22. lines 40-47: rule

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))

  // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
  // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
  // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
  // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
  // str </<=/>/>= comparisons.
```

### 23. lines 48-48: syntax, function, total

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### 24. lines 49-49: rule

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### 25. lines 50-50: rule

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### 26. lines 51-51: rule

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### 27. lines 52-52: rule

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### 28. lines 53-53: rule

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### 29. lines 54-55: rule

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### 30. lines 56-56: rule

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### 31. lines 57-57: rule

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### 32. lines 58-58: rule

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### 33. lines 59-59: rule

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## /reference/reference-semantics/semantics/subscript.k

Entries: 57

### 1. lines 11-11: syntax, function, total

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### 2. lines 12-12: rule

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### 3. lines 13-15: rule

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### 4. lines 16-16: syntax, function

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### 5. lines 17-17: rule

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### 6. lines 18-20: rule

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### 7. lines 21-21: syntax, function, total

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### 8. lines 22-22: rule

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### 9. lines 23-26: rule, strict

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### 10. lines 27-27: context

```k
  context Subscript(HOLE, _)
```

### 11. lines 28-30: context

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### 12. lines 31-34: rule, priority

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 13. lines 35-36: rule

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### 14. lines 37-37: syntax, function

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### 15. lines 38-38: rule

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### 16. lines 39-39: rule

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### 17. lines 40-43: rule

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### 18. lines 44-48: syntax

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### 19. lines 49-49: syntax

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### 20. lines 50-50: rule

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### 21. lines 51-51: rule

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### 22. lines 52-53: rule

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### 23. lines 54-54: rule

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### 24. lines 55-55: rule

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### 25. lines 56-57: rule

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### 26. lines 58-60: rule, priority

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### 27. lines 61-62: rule

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### 28. lines 63-63: syntax, function

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### 29. lines 64-65: rule

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### 30. lines 66-67: rule

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### 31. lines 68-71: rule

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### 32. lines 72-72: syntax, function, total

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### 33. lines 73-73: rule

```k
  rule slStep(noB)          => 1
```

### 34. lines 74-75: rule

```k
  rule slStep(someB(S:Int)) => S
```

### 35. lines 76-76: syntax, function

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### 36. lines 77-78: rule

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### 37. lines 79-80: rule

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### 38. lines 81-82: rule

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### 39. lines 83-83: syntax, function

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### 40. lines 84-85: rule

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### 41. lines 86-87: rule

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### 42. lines 88-89: rule

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### 43. lines 90-90: syntax, function, total

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### 44. lines 91-92: rule

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### 45. lines 93-95: rule

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### 46. lines 96-96: syntax, function, total

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### 47. lines 97-98: rule

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### 48. lines 99-101: rule

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### 49. lines 102-102: syntax, function, total

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### 50. lines 103-104: rule

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### 51. lines 105-108: rule

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

### 52. lines 109-109: syntax, function

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### 53. lines 110-112: rule

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### 54. lines 113-115: rule

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### 55. lines 116-116: syntax, function

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### 56. lines 117-119: rule

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### 57. lines 120-121: rule

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## /reference/reference-semantics/semantics/syntax.k

Entries: 16

### 1. lines 9-31: syntax, macro, strict, seqstrict

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

### 2. lines 32-32: syntax

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### 3. lines 33-33: syntax

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### 4. lines 34-34: syntax

```k
  syntax Entries  ::= List{Entry, ","}
```

### 5. lines 35-35: syntax

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### 6. lines 36-36: syntax

```k
  syntax CompFors ::= List{CompFor, ""}
```

### 7. lines 37-37: syntax

```k
  syntax Exprs    ::= List{Expr, ","}
```

### 8. lines 38-38: syntax

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### 9. lines 39-40: syntax

```k
  syntax Bound    ::= Expr | "NoBound"
```

### 10. lines 41-55: syntax, strict

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

### 11. lines 56-56: syntax

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### 12. lines 57-57: syntax

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### 13. lines 58-58: syntax

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### 14. lines 59-59: syntax

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### 15. lines 60-60: syntax

```k
  syntax ParamNames ::= List{String, ","}
```

### 16. lines 61-61: syntax

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## /reference/reference-semantics/semantics/tuple.k

Entries: 25

### 1. lines 10-10: rule

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### 2. lines 11-13: rule

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### 3. lines 14-14: syntax

```k
  syntax ApplyK ::= "toTuple"
```

### 4. lines 15-15: rule

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### 5. lines 16-17: rule

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### 6. lines 18-19: rule

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### 7. lines 20-20: rule

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### 8. lines 21-22: rule

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### 9. lines 23-23: rule

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### 10. lines 24-24: syntax, function

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### 11. lines 25-25: rule

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### 12. lines 26-27: rule

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### 13. lines 28-30: rule

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### 14. lines 31-31: syntax

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### 15. lines 32-34: rule

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### 16. lines 35-41: rule, priority

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### 17. lines 42-42: rule

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### 18. lines 43-43: rule

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### 19. lines 44-48: rule, priority

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### 20. lines 49-49: syntax

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### 21. lines 50-50: rule

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### 22. lines 51-51: rule

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### 23. lines 52-54: rule, priority

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 24. lines 55-56: rule

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### 25. lines 57-57: rule

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## /candidate/verification.k

Entries: 15

### 1. lines 6-6: syntax, function, total

```k
  syntax Stmts ::= "digitSumBody" [function, total]
```

### 2. lines 7-26: rule, total

```k
  rule digitSumBody =>
    Assign(Name("negative"), Compare(Name("n"), CmpOp("<", Int(0))))
    Assign(Name("n"), Call(Name("abs"), (Name("n"), .Exprs)))
    Assign(Name("total"), Int(0))
    Assign(Name("most_significant"), Int(0))
    While(Name("n"),
      Assign(Name("most_significant"), BinOp("%", Name("n"), Int(10)))
      AugAssign(Name("total"), "+", Name("most_significant"))
      AugAssign(Name("n"), "//", Int(10))
      .Stmts)
    If(Name("negative"),
      AugAssign(
        Name("total"),
        "-",
        BinOp("*", Int(2), Name("most_significant")))
      .Stmts,
      .Stmts)
    Return(Name("total"))
    .Stmts
```

### 3. lines 27-27: syntax, function, total

```k
  syntax Stmts ::= "orderByPointsBody" [function, total]
```

### 4. lines 28-36: rule

```k
  rule orderByPointsBody =>
    Return(
      Call(
        Name("sorted"),
        (Name("nums"),
         KwArg("key", Name("digit_sum")),
         .Exprs)))
    .Stmts
```

### 5. lines 37-38: syntax, function, total

```k
  syntax Val ::= "digitSumClosure" [function, total]
               | "orderByPointsClosure" [function, total]
```

### 6. lines 39-40: rule

```k
  rule digitSumClosure =>
    closureVal(("n", .ParamNames), digitSumBody, 0)
```

### 7. lines 41-43: rule

```k
  rule orderByPointsClosure =>
    closureVal(("nums", .ParamNames), orderByPointsBody, 0)
```

### 8. lines 44-44: syntax, function, total

```k
  syntax Module ::= "solutionModule" [function, total]
```

### 9. lines 45-53: rule

```k
  rule solutionModule =>
    Module(
      FuncDef("digit_sum", Params(("n", .ParamNames)), digitSumBody)
      FuncDef(
        "order_by_points",
        Params(("nums", .ParamNames)),
        orderByPointsBody)
      .Stmts)
```

### 10. lines 54-55: syntax, function, total

```k
  syntax Map ::= "initialScopes" [function, total]
               | "loadedScopes" [function, total]
```

### 11. lines 56-58: rule

```k
  rule initialScopes =>
    (0 |-> scope(.Map, parent(-1)))
    (-1 |-> builtinsScope)
```

### 12. lines 59-66: rule

```k
  rule loadedScopes =>
    (0 |-> scope(
      .Map
        [ "digit_sum" <- digitSumClosure ]
        [ "order_by_points" <- orderByPointsClosure ],
      parent(-1)))
    (-1 |-> builtinsScope)
```

### 13. lines 67-68: syntax

```k
  syntax KItem ::= "#runDigitSum" "(" Int ")"
                 | "#runOrderByPoints" "(" Val ")"
```

### 14. lines 69-72: rule

```k
  rule <k> #runDigitSum(N:Int)
        => #loadAll(solutionModule)
        ~> Call(Name("digit_sum"), (N, .Exprs))
        ... </k>
```

### 15. lines 73-76: rule

```k
  rule <k> #runOrderByPoints(V:Val)
        => #loadAll(solutionModule)
        ~> Call(Name("order_by_points"), (V, .Exprs))
        ... </k>
```

## /candidate/spec.k

Entries: 8

### 1. lines 6-16: claim

```k
  claim
    <k> #runDigitSum(0) => 0 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### 2. lines 17-27: claim

```k
  claim
    <k> #runDigitSum(1) => 1 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### 3. lines 28-38: claim

```k
  claim
    <k> #runDigitSum(11) => 2 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### 4. lines 39-49: claim

```k
  claim
    <k> #runDigitSum(-1) => -1 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### 5. lines 50-60: claim

```k
  claim
    <k> #runDigitSum(-11) => 0 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### 6. lines 61-71: claim

```k
  claim
    <k> #runDigitSum(-12) => 1 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### 7. lines 72-82: claim

```k
  claim
    <k> #runDigitSum(-123) => 4 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

### 8. lines 83-96: claim

```k
  claim
    <k> #runOrderByPoints(list(VS:ValSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortKeyVS(VS, digitSumClosure))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
```

# Totals

All entries: 951
- claim: 8
- configuration: 1
- context: 5
- rule: 704
- syntax: 233

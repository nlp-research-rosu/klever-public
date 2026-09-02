# Exhaustive K declaration and rule inventory

Generated from every `.k` source in the freshly copied supplied-semantics tree plus candidate `verification.k` and `spec.k`. Blocks begin at every top-level K directive and retain the complete multiline declaration/rule.

Files: 26

Directive counts: `{'claim': 2, 'configuration': 1, 'context': 5, 'endmodule': 27, 'imports': 88, 'module': 27, 'requires': 25, 'rule': 719, 'syntax': 235}`

Attribute/class counts: `{'equational-rule': 475, 'function': 153, 'macro': 4, 'opaque/no-evaluators': 26, 'operational-k-rule': 244, 'owise': 32, 'priority(30)': 6, 'priority(39)': 1, 'priority(40)': 45, 'priority(45)': 4, 'total': 119}`

## `/tmp/audit-work/work/reference-semantics/semantics/assert.k`

### 1. module at lines 3-3 (attributes/classes: none)

```k
module MPY-ASSERT
```

### 2. imports at lines 4-5 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 3. rule at lines 6-7 (attributes/classes: operational-k-rule)

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

### 4. rule at lines 8-12 (attributes/classes: operational-k-rule)

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

### 5. rule at lines 13-15 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 6. endmodule at lines 16-16 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/bool.k`

### 7. module at lines 5-5 (attributes/classes: none)

```k
module MPY-BOOL
```

### 8. imports at lines 6-7 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 9. rule at lines 8-9 (attributes/classes: equational-rule)

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

### 10. rule at lines 10-10 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### 11. rule at lines 11-15 (attributes/classes: equational-rule)

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

  // ==== BoolOp: short-circuit, value-returning and / or =====================
  // the node is its own accumulator: heat the HEAD element only, then either return it
  // (short-circuit) or drop it and continue
```

### 12. context at lines 16-16 (attributes/classes: none)

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### 13. rule at lines 17-17 (attributes/classes: operational-k-rule)

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### 14. rule at lines 18-19 (attributes/classes: operational-k-rule)

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

### 15. rule at lines 20-21 (attributes/classes: operational-k-rule)

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

### 16. rule at lines 22-23 (attributes/classes: operational-k-rule)

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

### 17. rule at lines 24-28 (attributes/classes: operational-k-rule)

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)

  // ==== heap-object head: decide truthiness THROUGH the heap, never rewrite the
  // operand — and/or return the OBJECT itself (Python identity), not its structure
```

### 18. rule at lines 29-30 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

### 19. rule at lines 31-34 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### 20. rule at lines 35-38 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### 21. rule at lines 39-42 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

### 22. rule at lines 43-46 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

### 23. endmodule at lines 47-47 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/builtins.k`

### 24. module at lines 3-3 (attributes/classes: none)

```k
module MPY-BUILTINS
```

### 25. imports at lines 4-4 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 26. imports at lines 5-5 (attributes/classes: none)

```k
  imports MPY-STR
```

### 27. imports at lines 6-6 (attributes/classes: none)

```k
  imports MPY-SET
```

### 28. imports at lines 7-7 (attributes/classes: none)

```k
  imports MPY-ITER
```

### 29. imports at lines 8-8 (attributes/classes: none)

```k
  imports MPY-RANGE
```

### 30. imports at lines 9-9 (attributes/classes: none)

```k
  imports MPY-INT
```

### 31. imports at lines 10-16 (attributes/classes: none)

```k
  imports MPY-METHODS

  // the builtins REGISTRY is core.k's builtinsScope (the -1 frame); names resolve by lookup

  // Call routing + argument evaluation live in call.k, which also routes the fold
  // builtins (sum/all/any/max/min) to the #_Acc folds below and everything else to
  // applyBuiltin. This module owns applyBuiltin + the fold implementations.
```

### 32. syntax at lines 17-19 (attributes/classes: function)

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]

  // ==== len(obj) — O(1) per kind ============================================
```

### 33. syntax at lines 20-20 (attributes/classes: function)

```k
  syntax Int ::= seqLen(Val) [function]
```

### 34. rule at lines 21-21 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### 35. rule at lines 22-22 (attributes/classes: equational-rule)

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### 36. rule at lines 23-23 (attributes/classes: equational-rule)

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### 37. rule at lines 24-24 (attributes/classes: equational-rule)

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### 38. rule at lines 25-25 (attributes/classes: equational-rule)

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### 39. rule at lines 26-31 (attributes/classes: equational-rule)

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

  // ==== list(seq) — materialize a list/tuple into a list (e.g. list(d.keys())) ==
  // Minimal: the "copy a sequence" case (list of a list is itself; list of a tuple keeps order).
  // list() of other iterables (str/range/set/zip) is added via the iterator fold when needed.
  // (k-cell — list() constructs a NEW object)
```

### 40. rule at lines 32-32 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### 41. rule at lines 33-33 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### 42. rule at lines 34-34 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### 43. rule at lines 35-35 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### 44. syntax at lines 36-36 (attributes/classes: function, total)

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### 45. rule at lines 37-37 (attributes/classes: equational-rule)

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

### 46. rule at lines 38-40 (attributes/classes: equational-rule)

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

  // ==== set(str) — distinct character codes =================================
```

### 47. rule at lines 41-43 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

  // ==== abs(int) ============================================================
```

### 48. rule at lines 44-46 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

  // ==== sum(iterable) — one #iterNext fold; intOf = int value of an int/bool ==
```

### 49. syntax at lines 47-47 (attributes/classes: none)

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### 50. rule at lines 48-48 (attributes/classes: operational-k-rule)

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### 51. rule at lines 49-49 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### 52. rule at lines 50-53 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

### 53. syntax at lines 54-54 (attributes/classes: function)

```k
  syntax Int ::= intOf(Val) [function]
```

### 54. rule at lines 55-55 (attributes/classes: equational-rule)

```k
  rule intOf(I:Int)  => I
```

### 55. rule at lines 56-58 (attributes/classes: equational-rule)

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

  // ==== all / any (short-circuiting #iterNext folds) ========================
```

### 56. syntax at lines 59-59 (attributes/classes: none)

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### 57. rule at lines 60-60 (attributes/classes: operational-k-rule)

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### 58. rule at lines 61-61 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

### 59. rule at lines 62-63 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

### 60. rule at lines 64-66 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

### 61. syntax at lines 67-67 (attributes/classes: none)

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### 62. rule at lines 68-68 (attributes/classes: operational-k-rule)

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### 63. rule at lines 69-69 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

### 64. rule at lines 70-71 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

### 65. rule at lines 72-75 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)

  // ==== max / min over an iterable (#iterNext folds; first element seeds) ====
```

### 66. syntax at lines 76-76 (attributes/classes: none)

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### 67. rule at lines 77-77 (attributes/classes: operational-k-rule)

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### 68. rule at lines 78-79 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### 69. rule at lines 80-80 (attributes/classes: operational-k-rule)

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### 70. rule at lines 81-81 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### 71. rule at lines 82-85 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

### 72. syntax at lines 86-86 (attributes/classes: none)

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### 73. rule at lines 87-87 (attributes/classes: operational-k-rule)

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### 74. rule at lines 88-89 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

### 75. rule at lines 90-90 (attributes/classes: operational-k-rule)

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### 76. rule at lines 91-91 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### 77. rule at lines 92-96 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)

  // ==== variadic max / min (a Vals fold) ====================================
```

### 78. syntax at lines 97-97 (attributes/classes: function)

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

### 79. rule at lines 98-98 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### 80. rule at lines 99-99 (attributes/classes: equational-rule)

```k
  rule maxVals(M:Int, .Vals)           => M
```

### 81. rule at lines 100-101 (attributes/classes: equational-rule)

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### 82. syntax at lines 102-102 (attributes/classes: function)

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

### 83. rule at lines 103-103 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### 84. rule at lines 104-104 (attributes/classes: equational-rule)

```k
  rule minVals(M:Int, .Vals)           => M
```

### 85. rule at lines 105-107 (attributes/classes: equational-rule)

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

  // ==== bin(n) — "0b" + binary digit codes (promoted from 103's defined fold) ==
```

### 86. rule at lines 108-110 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
  // negative operand: the '-' sign prefixes the magnitude's digits
```

### 87. rule at lines 111-113 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

### 88. syntax at lines 114-114 (attributes/classes: function, total)

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

### 89. rule at lines 115-115 (attributes/classes: equational-rule)

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

### 90. rule at lines 116-116 (attributes/classes: equational-rule)

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### 91. syntax at lines 117-117 (attributes/classes: function, total)

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### 92. rule at lines 118-118 (attributes/classes: equational-rule)

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

### 93. rule at lines 119-123 (attributes/classes: equational-rule)

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0

  // ==== enumerate(xs) — pairs (i, v); materialized eagerly over a list =========
```

### 94. rule at lines 124-125 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

### 95. syntax at lines 126-126 (attributes/classes: function, total)

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### 96. rule at lines 127-127 (attributes/classes: equational-rule)

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### 97. rule at lines 128-131 (attributes/classes: equational-rule)

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

  // ==== map(str, xs) — eager (only the str case is in the subset) =============
```

### 98. rule at lines 132-133 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

### 99. syntax at lines 134-134 (attributes/classes: function, total)

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### 100. rule at lines 135-135 (attributes/classes: equational-rule)

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

### 101. rule at lines 136-136 (attributes/classes: equational-rule)

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### 102. rule at lines 137-139 (attributes/classes: equational-rule)

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

  // ==== int(x) identities (int(round(x)) composes through) ====================
```

### 103. rule at lines 140-142 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("int", I:Int, .Vals) => I

  // ==== ord / chr ===========================================================
```

### 104. rule at lines 143-143 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### 105. rule at lines 144-147 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128

  // ==== str(int) / str(str) =================================================
```

### 106. rule at lines 148-148 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### 107. rule at lines 149-151 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

  // ==== int(str) — a single digit char ('0'..'9', code 48..57) to its value =====
```

### 108. rule at lines 152-155 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57

  // ==== int(str) — a multi-digit non-negative numeral (Horner fold; the single-char rule covers len 1)
```

### 109. rule at lines 156-157 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

### 110. syntax at lines 158-158 (attributes/classes: function, total)

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### 111. rule at lines 159-159 (attributes/classes: equational-rule)

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### 112. rule at lines 160-162 (attributes/classes: equational-rule)

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

  // ==== zip(a, b) — parallel iterable of pairs, truncating to the shorter =====
```

### 113. rule at lines 163-163 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### 114. rule at lines 164-166 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

  // zip's iterator-protocol cases (zip is created here, so its #iterNext lives here)
```

### 115. rule at lines 167-168 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### 116. rule at lines 169-169 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### 117. rule at lines 170-170 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### 118. rule at lines 171-172 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### 119. rule at lines 173-173 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### 120. rule at lines 174-176 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

  // ==== range(stop) / range(start, stop) / range(start, stop, step) =========
```

### 121. rule at lines 177-177 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### 122. rule at lines 178-178 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### 123. rule at lines 179-186 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0

  // ==== eval(str) — arithmetic expressions (ints, + - * // **, spaces) ========
  // Python precedence: ** right-assoc, then * //, then + -. Promoted from 160's
  // trusted pass evaluator, now DEFINED in the reference and driven by a
  // code-level tokenizer. Reduces on concrete strings (krun); a symbolic
  // argument leaves the call unevaluated for problem-level folds.
```

### 124. rule at lines 187-187 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### 125. syntax at lines 188-188 (attributes/classes: function)

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

### 126. rule at lines 189-191 (attributes/classes: equational-rule)

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### 127. syntax at lines 192-193 (attributes/classes: none)

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### 128. syntax at lines 194-194 (attributes/classes: function, total)

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

### 129. rule at lines 195-195 (attributes/classes: equational-rule)

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### 130. syntax at lines 196-196 (attributes/classes: function, total)

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

### 131. rule at lines 197-197 (attributes/classes: equational-rule)

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

### 132. rule at lines 198-198 (attributes/classes: owise, equational-rule)

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

### 133. syntax at lines 199-199 (attributes/classes: function, total)

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

### 134. rule at lines 200-200 (attributes/classes: equational-rule)

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

### 135. rule at lines 201-202 (attributes/classes: owise, equational-rule)

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

### 136. syntax at lines 203-203 (attributes/classes: function, total)

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### 137. rule at lines 204-204 (attributes/classes: equational-rule)

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

### 138. rule at lines 205-205 (attributes/classes: equational-rule)

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### 139. rule at lines 206-206 (attributes/classes: equational-rule)

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### 140. rule at lines 207-207 (attributes/classes: equational-rule)

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### 141. rule at lines 208-208 (attributes/classes: equational-rule)

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### 142. rule at lines 209-209 (attributes/classes: equational-rule)

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### 143. rule at lines 210-210 (attributes/classes: equational-rule)

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### 144. rule at lines 211-211 (attributes/classes: equational-rule)

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### 145. rule at lines 212-213 (attributes/classes: equational-rule)

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### 146. syntax at lines 214-215 (attributes/classes: function, total)

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

### 147. rule at lines 216-216 (attributes/classes: equational-rule)

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

### 148. rule at lines 217-217 (attributes/classes: equational-rule)

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### 149. rule at lines 218-218 (attributes/classes: equational-rule)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### 150. rule at lines 219-220 (attributes/classes: equational-rule)

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

### 151. rule at lines 221-222 (attributes/classes: equational-rule)

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

### 152. rule at lines 223-224 (attributes/classes: owise, equational-rule)

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### 153. syntax at lines 225-225 (attributes/classes: none)

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

### 154. syntax at lines 226-226 (attributes/classes: function, total)

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

### 155. rule at lines 227-227 (attributes/classes: equational-rule)

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### 156. rule at lines 228-229 (attributes/classes: owise, equational-rule)

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

### 157. syntax at lines 230-230 (attributes/classes: function, total)

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### 158. rule at lines 231-231 (attributes/classes: equational-rule)

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### 159. rule at lines 232-232 (attributes/classes: equational-rule)

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### 160. rule at lines 233-233 (attributes/classes: equational-rule)

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### 161. rule at lines 234-234 (attributes/classes: equational-rule)

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### 162. rule at lines 235-235 (attributes/classes: equational-rule)

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### 163. rule at lines 236-237 (attributes/classes: owise, equational-rule)

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### 164. syntax at lines 238-238 (attributes/classes: function, total)

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### 165. rule at lines 239-239 (attributes/classes: equational-rule)

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### 166. rule at lines 240-240 (attributes/classes: equational-rule)

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### 167. rule at lines 241-242 (attributes/classes: equational-rule)

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

### 168. rule at lines 243-243 (attributes/classes: owise, equational-rule)

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### 169. syntax at lines 244-244 (attributes/classes: function, total)

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### 170. rule at lines 245-245 (attributes/classes: equational-rule)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### 171. rule at lines 246-246 (attributes/classes: equational-rule)

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### 172. syntax at lines 247-247 (attributes/classes: function, total)

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### 173. rule at lines 248-249 (attributes/classes: equational-rule)

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### 174. syntax at lines 250-250 (attributes/classes: function, total)

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### 175. rule at lines 251-251 (attributes/classes: equational-rule)

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### 176. rule at lines 252-252 (attributes/classes: equational-rule)

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### 177. rule at lines 253-253 (attributes/classes: equational-rule)

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### 178. rule at lines 254-254 (attributes/classes: equational-rule)

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### 179. syntax at lines 255-255 (attributes/classes: function, total)

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### 180. rule at lines 256-256 (attributes/classes: equational-rule)

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### 181. rule at lines 257-259 (attributes/classes: equational-rule)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

### 182. rule at lines 260-262 (attributes/classes: equational-rule)

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

### 183. rule at lines 263-264 (attributes/classes: owise, equational-rule)

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

### 184. syntax at lines 265-265 (attributes/classes: function, total)

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

### 185. rule at lines 266-266 (attributes/classes: equational-rule)

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### 186. rule at lines 267-267 (attributes/classes: equational-rule)

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### 187. rule at lines 268-268 (attributes/classes: owise, equational-rule)

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

### 188. syntax at lines 269-269 (attributes/classes: function, total)

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### 189. rule at lines 270-270 (attributes/classes: equational-rule)

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### 190. rule at lines 271-271 (attributes/classes: equational-rule)

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### 191. syntax at lines 272-272 (attributes/classes: function, total)

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### 192. rule at lines 273-273 (attributes/classes: equational-rule)

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### 193. rule at lines 274-278 (attributes/classes: equational-rule)

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

  // ==== hashlib.md5(S).hexdigest() — a trusted opaque digest ==================
  // The md5 value itself is a named shared trust (sortVS-style, no concrete
  // twin); proofs use the length/hex-charset lemmas (lemmas/builtins.k).
```

### 194. syntax at lines 279-279 (attributes/classes: none)

```k
  syntax KItem ::= "#md5"
```

### 195. rule at lines 280-281 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

### 196. rule at lines 282-282 (attributes/classes: operational-k-rule)

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### 197. syntax at lines 283-283 (attributes/classes: none)

```k
  syntax Val ::= md5Obj(IntSeq)
```

### 198. rule at lines 284-284 (attributes/classes: equational-rule)

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### 199. syntax at lines 285-290 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

  // ==== isinstance(V, int|str) — an ordinary 2-arg builtin ===================
  // The type argument (int/str) is an ordinary name that resolves via the builtins frame to
  // typeV (see core.k's config); no Call-level special case. isIntV/isStrV mirror the old
  // owise-on-Val test (concrete-sort args decide; a symbolic Val stays owise, as before).
```

### 200. rule at lines 291-291 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### 201. rule at lines 292-292 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### 202. syntax at lines 293-293 (attributes/classes: function)

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### 203. rule at lines 294-294 (attributes/classes: equational-rule)

```k
  rule isIntV(_:Int)         => true
```

### 204. rule at lines 295-295 (attributes/classes: owise, equational-rule)

```k
  rule isIntV(_:Val)         => false [owise]
```

### 205. rule at lines 296-296 (attributes/classes: equational-rule)

```k
  rule isStrV(str(_:IntSeq)) => true
```

### 206. rule at lines 297-297 (attributes/classes: owise, equational-rule)

```k
  rule isStrV(_:Val)         => false [owise]
```

### 207. endmodule at lines 298-298 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/call.k`

### 208. module at lines 10-10 (attributes/classes: none)

```k
module MPY-CALL
```

### 209. imports at lines 11-11 (attributes/classes: none)

```k
  imports MPY-METHODS
```

### 210. imports at lines 12-12 (attributes/classes: none)

```k
  imports MPY-BUILTINS
```

### 211. imports at lines 13-15 (attributes/classes: none)

```k
  imports MPY-FUNCTIONS

  // a cooled attribute is a bound method value
```

### 212. rule at lines 16-18 (attributes/classes: owise, operational-k-rule)

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

  // evaluate callee, then args ([owise]: problem-local Call interceptions beat this)
```

### 213. syntax at lines 19-19 (attributes/classes: none)

```k
  syntax KItem ::= #callee(Exprs)
```

### 214. rule at lines 20-20 (attributes/classes: owise, operational-k-rule)

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### 215. rule at lines 21-23 (attributes/classes: operational-k-rule)

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

  // ==== dispatch on the callee value ========================================
```

### 216. rule at lines 24-25 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### 217. rule at lines 26-26 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### 218. rule at lines 27-27 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### 219. rule at lines 28-28 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### 220. rule at lines 29-29 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### 221. rule at lines 30-30 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### 222. rule at lines 31-31 (attributes/classes: owise, operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### 223. rule at lines 32-37 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

  // ==== heap-object arguments/receivers =====================================
  // Builtins and type calls READ structure — deref the first two arg positions
  // (covers len/sum/all/any/max/min/sorted/list/set + zip's pair). Mutating list
  // methods take the ref itself; every other method receiver is deref'd.
```

### 224. rule at lines 38-41 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 225. rule at lines 42-46 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

### 226. rule at lines 47-51 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 227. syntax at lines 52-52 (attributes/classes: function, total)

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

### 228. rule at lines 53-55 (attributes/classes: equational-rule)

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### 229. rule at lines 56-62 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
  // non-mutating methods READ their heap-object arguments too (join's list);
  // mutators keep refs (append of a list into a list-of-lists stays aliased)
```

### 230. rule at lines 63-68 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

### 231. rule at lines 69-79 (attributes/classes: operational-k-rule)

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

### 232. rule at lines 80-86 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### 233. syntax at lines 87-87 (attributes/classes: none)

```k
  syntax KItem ::= #allocCells(ParamNames)
```

### 234. rule at lines 88-88 (attributes/classes: operational-k-rule)

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### 235. rule at lines 89-94 (attributes/classes: operational-k-rule)

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

### 236. endmodule at lines 95-95 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/comprehension.k`

### 237. module at lines 3-3 (attributes/classes: none)

```k
module MPY-COMPREHENSION
```

### 238. imports at lines 4-4 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 239. imports at lines 5-5 (attributes/classes: none)

```k
  imports MPY-OPERATORS
```

### 240. imports at lines 6-6 (attributes/classes: none)

```k
  imports MPY-LIST
```

### 241. imports at lines 7-7 (attributes/classes: none)

```k
  imports MPY-CONTROLS
```

### 242. imports at lines 8-10 (attributes/classes: none)

```k
  imports MPY-FUNCTIONS

  // A comprehension is pure syntactic sugar
```

### 243. rule at lines 11-11 (attributes/classes: equational-rule)

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### 244. rule at lines 12-13 (attributes/classes: equational-rule)

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### 245. syntax at lines 14-14 (attributes/classes: macro)

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### 246. rule at lines 15-17 (attributes/classes: equational-rule)

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### 247. syntax at lines 18-18 (attributes/classes: macro)

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### 248. rule at lines 19-20 (attributes/classes: equational-rule)

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### 249. rule at lines 21-23 (attributes/classes: equational-rule)

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### 250. syntax at lines 24-24 (attributes/classes: macro)

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

### 251. rule at lines 25-25 (attributes/classes: equational-rule)

```k
  rule compGuard(.Exprs)             => Bool(true)
```

### 252. rule at lines 26-26 (attributes/classes: equational-rule)

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### 253. endmodule at lines 27-27 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/concrete.k`

### 254. module at lines 8-8 (attributes/classes: none)

```k
module MPY-CONCRETE
```

### 255. imports at lines 9-12 (attributes/classes: none)

```k
  imports MPY

  // deep equality for list compares whose elements are heap objects
  // (list-of-lists): Python == is structural at every depth.
```

### 256. rule at lines 13-15 (attributes/classes: operational-k-rule)

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

### 257. rule at lines 16-24 (attributes/classes: priority(40), operational-k-rule)

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

### 258. syntax at lines 25-25 (attributes/classes: none)

```k
  syntax Val ::= kvP(Val, Val)
```

### 259. syntax at lines 26-27 (attributes/classes: none)

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### 260. rule at lines 28-30 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

### 261. rule at lines 31-33 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

### 262. rule at lines 34-35 (attributes/classes: operational-k-rule)

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### 263. rule at lines 36-37 (attributes/classes: operational-k-rule)

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### 264. rule at lines 38-41 (attributes/classes: operational-k-rule)

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

### 265. syntax at lines 42-42 (attributes/classes: function)

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### 266. rule at lines 43-43 (attributes/classes: equational-rule)

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### 267. rule at lines 44-46 (attributes/classes: equational-rule)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

### 268. rule at lines 47-50 (attributes/classes: equational-rule)

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

### 269. syntax at lines 51-51 (attributes/classes: function)

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

### 270. rule at lines 52-52 (attributes/classes: equational-rule)

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### 271. rule at lines 53-53 (attributes/classes: equational-rule)

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### 272. rule at lines 54-55 (attributes/classes: equational-rule)

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### 273. syntax at lines 56-56 (attributes/classes: function, total)

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### 274. rule at lines 57-57 (attributes/classes: equational-rule)

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

### 275. rule at lines 58-58 (attributes/classes: equational-rule)

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### 276. rule at lines 59-59 (attributes/classes: owise, equational-rule)

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### 277. endmodule at lines 60-60 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/controls.k`

### 278. module at lines 3-3 (attributes/classes: none)

```k
module MPY-CONTROLS
```

### 279. imports at lines 4-4 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 280. imports at lines 5-5 (attributes/classes: none)

```k
  imports MPY-TUPLE
```

### 281. imports at lines 6-8 (attributes/classes: none)

```k
  imports MPY-ITER

  // ==== Assign / AugAssign (write the current scope; RHS evaluated by strictness) ==
```

### 282. rule at lines 9-11 (attributes/classes: operational-k-rule)

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### 283. rule at lines 12-19 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### 284. rule at lines 20-26 (attributes/classes: operational-k-rule)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
  // `lst += [..]` where lst is a heap ref: the generic rule leaves applyBin(OP, ref, V) — but the
  // ref-deref preemption is BinOp-level (operators.k), so applyBin never derefs and it sticks. Route
  // the ref case through BinOp so the deref + list-concat + #alloc path fires (result is a fresh ref).
```

### 285. rule at lines 27-34 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]

  // ==== import trivia: `from math import floor, ceil` binds the supported
  // names as builtins in the current scope; every other import is a no-op
```

### 286. rule at lines 35-35 (attributes/classes: operational-k-rule)

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### 287. rule at lines 36-36 (attributes/classes: owise, operational-k-rule)

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### 288. syntax at lines 37-37 (attributes/classes: none)

```k
  syntax KItem ::= #bindImports(ParamNames)
```

### 289. rule at lines 38-38 (attributes/classes: operational-k-rule)

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### 290. rule at lines 39-42 (attributes/classes: operational-k-rule)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

### 291. rule at lines 43-47 (attributes/classes: operational-k-rule)

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")

  // ==== Expr statement: evaluate for effect, discard the value ===============
  // (bare calls — mutator methods, docstrings; the WP0 statement-trivia rung)
```

### 292. rule at lines 48-50 (attributes/classes: operational-k-rule)

```k
  rule <k> Expr(_:Val) => .K ... </k>

  // ==== If (condition evaluated by strictness) ==============================
```

### 293. syntax at lines 51-51 (attributes/classes: none)

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### 294. rule at lines 52-52 (attributes/classes: operational-k-rule)

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### 295. rule at lines 53-53 (attributes/classes: operational-k-rule)

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### 296. rule at lines 54-56 (attributes/classes: operational-k-rule)

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

  // ==== IfExp: ternary T if C else E ========================================
```

### 297. rule at lines 57-58 (attributes/classes: operational-k-rule)

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

### 298. rule at lines 59-64 (attributes/classes: operational-k-rule)

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)

  // ==== For: one loop, in-cell continuation, over #iterNext =================
  // (the iterable is evaluated once, by strictness; the protocol stays rewrites —
  // circularities anchor on #loop and narrowing substitutes the structure)
```

### 299. syntax at lines 65-68 (attributes/classes: none)

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

### 300. rule at lines 69-70 (attributes/classes: operational-k-rule)

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### 301. rule at lines 71-71 (attributes/classes: operational-k-rule)

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### 302. rule at lines 72-72 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### 303. rule at lines 73-76 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

  // ==== While ==============================================================
```

### 304. rule at lines 77-77 (attributes/classes: operational-k-rule)

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### 305. rule at lines 78-78 (attributes/classes: operational-k-rule)

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### 306. rule at lines 79-80 (attributes/classes: operational-k-rule)

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

### 307. rule at lines 81-84 (attributes/classes: operational-k-rule)

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)

  // ==== loop control (break / continue) =====================================
```

### 308. rule at lines 85-85 (attributes/classes: operational-k-rule)

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### 309. rule at lines 86-86 (attributes/classes: operational-k-rule)

```k
  rule <k> Continue => #cont ... </k>
```

### 310. rule at lines 87-87 (attributes/classes: operational-k-rule)

```k
  rule <k> Break => #brk ... </k>
```

### 311. rule at lines 88-88 (attributes/classes: operational-k-rule)

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### 312. rule at lines 89-89 (attributes/classes: owise, operational-k-rule)

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### 313. rule at lines 90-90 (attributes/classes: operational-k-rule)

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### 314. rule at lines 91-94 (attributes/classes: owise, priority(40), operational-k-rule)

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

  // ==== heap-object deref at the truthiness/iteration consumers ==============
  // (priority(40) preempts the generic Val rules so truthy/#loop never see a ref)
```

### 315. rule at lines 95-97 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 316. rule at lines 98-100 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 317. rule at lines 101-105 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  // For derefs its iterable ONCE at loop start (iteration is over the snapshot;
  // mutating the iterated list inside its own loop is outside the subset)
```

### 318. rule at lines 106-108 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 319. endmodule at lines 109-109 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/core.k`

### 320. module at lines 3-3 (attributes/classes: none)

```k
module MPY-CORE
```

### 321. imports at lines 4-4 (attributes/classes: none)

```k
  imports MPY-SYNTAX
```

### 322. imports at lines 5-5 (attributes/classes: none)

```k
  imports INT
```

### 323. imports at lines 6-6 (attributes/classes: none)

```k
  imports BOOL
```

### 324. imports at lines 7-7 (attributes/classes: none)

```k
  imports STRING
```

### 325. imports at lines 8-8 (attributes/classes: none)

```k
  imports MAP
```

### 326. imports at lines 9-9 (attributes/classes: none)

```k
  imports LIST
```

### 327. imports at lines 10-12 (attributes/classes: none)

```k
  imports K-EQUAL

  // ==== values, the algebraic lists, and the scope heap =====================
```

### 328. syntax at lines 13-13 (attributes/classes: none)

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### 329. syntax at lines 14-14 (attributes/classes: none)

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### 330. syntax at lines 15-17 (attributes/classes: none)

```k
  syntax Str    ::= str(IntSeq)

  // the iterable values, grouped under one sort (typing only — dispatch is <k>-cell)
```

### 331. syntax at lines 18-24 (attributes/classes: none)

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

### 332. syntax at lines 25-35 (attributes/classes: none)

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

### 333. syntax at lines 36-36 (attributes/classes: none)

```k
  syntax Parent   ::= "root" | parent(Int)
```

### 334. syntax at lines 37-37 (attributes/classes: none)

```k
  syntax Scope    ::= scope(Map, Parent)
```

### 335. syntax at lines 38-38 (attributes/classes: none)

```k
  syntax KResult  ::= Val
```

### 336. syntax at lines 39-39 (attributes/classes: none)

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### 337. syntax at lines 40-40 (attributes/classes: none)

```k
  syntax Vals     ::= List{Val, ","}
```

### 338. syntax at lines 41-41 (attributes/classes: none)

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

### 339. syntax at lines 42-48 (attributes/classes: none)

```k
  syntax RetState ::= "noRet" | retV(Val)

  // ==== configuration =======================================================
  // The builtins namespace is a real scope at reserved location -1 (the bottom of every
  // chain; scopeLoc only allocates >=1, so -1 never collides). The module scope (loc 0)
  // has it as parent, so an unbound name resolves there last — exactly LEGB. `int`/`str`
  // resolve to their type objects; any local/global binding shadows them via normal lookup.
```

### 340. configuration at lines 49-67 (attributes/classes: none)

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

### 341. syntax at lines 68-68 (attributes/classes: function, total)

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

### 342. rule at lines 69-69 (attributes/classes: equational-rule)

```k
  rule isRefV(ref(_:Int)) => true
```

### 343. rule at lines 70-74 (attributes/classes: owise, equational-rule)

```k
  rule isRefV(_:Val)      => false [owise]

  // closure cells (Python-faithful capture): the heap holds cellV(V); a
  // cellRef surfacing as the k-redex reads through (lookup is the only use —
  // cellRefs never escape to user-visible values)
```

### 344. syntax at lines 75-75 (attributes/classes: none)

```k
  syntax HeapVal ::= cellV(Val)
```

### 345. syntax at lines 76-76 (attributes/classes: function, total)

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

### 346. rule at lines 77-77 (attributes/classes: equational-rule)

```k
  rule isCellRef(cellRef(_:Int)) => true
```

### 347. rule at lines 78-84 (attributes/classes: owise, equational-rule)

```k
  rule isCellRef(_:Val)          => false [owise]
  // k-top deref for cell-bound reads surfacing INSIDE the annotated frame
  // (AugAssign's in-place read and friends). The "$cells" guard keeps this
  // DECIDABLY inapplicable in plain frames — an unguarded rule lets the
  // prover narrow abstract k-top values into cellRef junk (probed on
  // 26-remove-duplicates). Cross-frame reads (a comprehension closure
  // reading the enclosing function's cellvar) deref inside #look instead.
```

### 348. rule at lines 85-94 (attributes/classes: priority(40), operational-k-rule)

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

### 349. syntax at lines 95-95 (attributes/classes: none)

```k
  syntax Val ::= kwV(String, Val)
```

### 350. syntax at lines 96-96 (attributes/classes: none)

```k
  syntax KItem ::= #kwTag(String)
```

### 351. rule at lines 97-97 (attributes/classes: operational-k-rule)

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### 352. rule at lines 98-99 (attributes/classes: operational-k-rule)

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

### 353. syntax at lines 100-100 (attributes/classes: function, total)

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

### 354. rule at lines 101-101 (attributes/classes: equational-rule)

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

### 355. rule at lines 102-105 (attributes/classes: owise, equational-rule)

```k
  rule isKwV(_:Val)                => false [owise]

  // the frame marker carries the CONCRETE cellvar list, so cell-write dispatch
  // decides by pnMember even over an abstract frame rest (no prover branching)
```

### 356. syntax at lines 106-106 (attributes/classes: none)

```k
  syntax Val ::= cellsMark(ParamNames)
```

### 357. syntax at lines 107-107 (attributes/classes: function)

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

### 358. rule at lines 108-108 (attributes/classes: equational-rule)

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### 359. syntax at lines 109-109 (attributes/classes: function, total)

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### 360. rule at lines 110-110 (attributes/classes: equational-rule)

```k
  rule pnMember(_:String, .ParamNames) => false
```

### 361. rule at lines 111-112 (attributes/classes: equational-rule)

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### 362. syntax at lines 113-113 (attributes/classes: none)

```k
  syntax KItem ::= #cellW(Val, Val)
```

### 363. rule at lines 114-116 (attributes/classes: operational-k-rule)

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### 364. syntax at lines 117-117 (attributes/classes: none)

```k
  syntax KItem ::= #alloc(Val)
```

### 365. rule at lines 118-123 (attributes/classes: operational-k-rule)

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)

  // ==== module load + statement sequencing ==================================
```

### 366. syntax at lines 124-124 (attributes/classes: none)

```k
  syntax KItem ::= #loadAll(Module)
```

### 367. rule at lines 125-125 (attributes/classes: operational-k-rule)

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### 368. rule at lines 126-126 (attributes/classes: operational-k-rule)

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### 369. rule at lines 127-129 (attributes/classes: operational-k-rule)

```k
  rule <k> .Stmts => .K ... </k>

  // ==== Name lookup (walk the scope chain; builtins live in the -1 scope) ====
```

### 370. syntax at lines 130-130 (attributes/classes: none)

```k
  syntax KItem ::= #look(String, Int)
```

### 371. rule at lines 131-131 (attributes/classes: operational-k-rule)

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### 372. rule at lines 132-144 (attributes/classes: operational-k-rule)

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

### 373. rule at lines 145-151 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

### 374. rule at lines 152-156 (attributes/classes: operational-k-rule)

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))

  // the ONE predefined builtins scope (the -1 frame; claims write `-1 |-> builtinsScope`)
```

### 375. syntax at lines 157-157 (attributes/classes: function, total)

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

### 376. rule at lines 158-184 (attributes/classes: equational-rule)

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

### 377. syntax at lines 185-185 (attributes/classes: none)

```k
  syntax ApplyK ::= toCall(Val)
```

### 378. syntax at lines 186-188 (attributes/classes: none)

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

### 379. rule at lines 189-189 (attributes/classes: operational-k-rule)

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### 380. rule at lines 190-190 (attributes/classes: operational-k-rule)

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### 381. rule at lines 191-193 (attributes/classes: operational-k-rule)

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

  // ==== Int / Bool / None literals ==========================================
```

### 382. rule at lines 194-194 (attributes/classes: operational-k-rule)

```k
  rule <k> Int(I:Int)   => I ... </k>
```

### 383. rule at lines 195-195 (attributes/classes: operational-k-rule)

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

### 384. rule at lines 196-198 (attributes/classes: operational-k-rule)

```k
  rule <k> NoneVal      => noneV ... </k>

  // ==== truthy (If, Assert, BoolOp, IfExp, not, While) ======================
```

### 385. syntax at lines 199-199 (attributes/classes: function)

```k
  syntax Bool ::= truthy(Val) [function]
```

### 386. rule at lines 200-200 (attributes/classes: equational-rule)

```k
  rule truthy(B:Bool)          => B
```

### 387. rule at lines 201-201 (attributes/classes: equational-rule)

```k
  rule truthy(noneV)           => false
```

### 388. rule at lines 202-202 (attributes/classes: equational-rule)

```k
  rule truthy(I:Int)           => I =/=Int 0
```

### 389. rule at lines 203-203 (attributes/classes: equational-rule)

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### 390. rule at lines 204-204 (attributes/classes: equational-rule)

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### 391. rule at lines 205-207 (attributes/classes: equational-rule)

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

  // ==== extensible operator dispatch (cases added by the construct modules) ==
```

### 392. syntax at lines 208-208 (attributes/classes: function)

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

### 393. syntax at lines 209-209 (attributes/classes: function)

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

### 394. syntax at lines 210-212 (attributes/classes: function)

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]

  // ==== shared list helpers =================================================
```

### 395. syntax at lines 213-213 (attributes/classes: function, total)

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### 396. rule at lines 214-214 (attributes/classes: equational-rule)

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

### 397. rule at lines 215-216 (attributes/classes: equational-rule)

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### 398. syntax at lines 217-217 (attributes/classes: function, total)

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### 399. rule at lines 218-218 (attributes/classes: equational-rule)

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

### 400. rule at lines 219-222 (attributes/classes: equational-rule)

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

  // ==== shared sequence length (len / summaries across many modules) ========
  // (positional access valSeqAt/intSeqAt + normIdx live in subscript.k)
```

### 401. syntax at lines 223-223 (attributes/classes: function, total)

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

### 402. rule at lines 224-224 (attributes/classes: equational-rule)

```k
  rule vsLen(.ValSeq)                => 0
```

### 403. rule at lines 225-226 (attributes/classes: equational-rule)

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### 404. syntax at lines 227-227 (attributes/classes: function, total)

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

### 405. rule at lines 228-228 (attributes/classes: equational-rule)

```k
  rule isLen(.IntSeq)                => 0
```

### 406. rule at lines 229-232 (attributes/classes: total, equational-rule)

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

  // in-bounds positional write (list subscript-assign); OOB leaves the seq unchanged
  // (valid programs write in-bounds — mirrors valSeqAt's total-but-underspecified stance)
```

### 407. syntax at lines 233-233 (attributes/classes: function, total)

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### 408. rule at lines 234-234 (attributes/classes: equational-rule)

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### 409. rule at lines 235-235 (attributes/classes: equational-rule)

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### 410. rule at lines 236-237 (attributes/classes: equational-rule)

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

### 411. rule at lines 238-239 (attributes/classes: equational-rule)

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

### 412. endmodule at lines 240-240 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/dict.k`

### 413. module at lines 13-13 (attributes/classes: none)

```k
module MPY-DICT
```

### 414. imports at lines 14-14 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 415. imports at lines 15-15 (attributes/classes: none)

```k
  imports MPY-ITER
```

### 416. imports at lines 16-16 (attributes/classes: none)

```k
  imports MPY-METHODS
```

### 417. imports at lines 17-19 (attributes/classes: none)

```k
  imports MPY-LIST

  // dict as PARALLEL ordered key/value ValSeqs (same length; keys distinct).
```

### 418. syntax at lines 20-22 (attributes/classes: none)

```k
  syntax Val ::= dictV(ValSeq, ValSeq)

  // ==== DictExpr: {k: v, ...} literal. Eval each key then value, left to right, insert-with-dedup.
```

### 419. syntax at lines 23-25 (attributes/classes: none)

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### 420. rule at lines 26-26 (attributes/classes: operational-k-rule)

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### 421. rule at lines 27-27 (attributes/classes: operational-k-rule)

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### 422. rule at lines 28-29 (attributes/classes: operational-k-rule)

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### 423. rule at lines 30-31 (attributes/classes: operational-k-rule)

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### 424. rule at lines 32-36 (attributes/classes: total, operational-k-rule)

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

  // insert-with-dedup helpers (concrete Val key equality via ==K). [total] so buildFold over a dict is
  // total (its #Ceil is #Top) — needed when a symbolic proof carries a built dict as a config value.
```

### 425. syntax at lines 37-37 (attributes/classes: function, total)

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### 426. rule at lines 38-38 (attributes/classes: equational-rule)

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

### 427. rule at lines 39-39 (attributes/classes: equational-rule)

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### 428. rule at lines 40-42 (attributes/classes: equational-rule)

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

  // dPutK: KS unchanged if K already present, else append K (keep-first-position).
```

### 429. syntax at lines 43-43 (attributes/classes: function, total)

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### 430. rule at lines 44-44 (attributes/classes: equational-rule)

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### 431. rule at lines 45-48 (attributes/classes: owise, equational-rule)

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

  // dPutV: parallel to KS — set the value at K's position if present, else append V at the end. The
  // [owise] catch-all covers the degenerate mismatched-length case (never reached for a well-formed dict).
```

### 432. syntax at lines 49-49 (attributes/classes: function, total)

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### 433. rule at lines 50-51 (attributes/classes: equational-rule)

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

### 434. rule at lines 52-53 (attributes/classes: equational-rule)

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

### 435. rule at lines 54-57 (attributes/classes: owise, equational-rule)

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

  // ==== dict methods ========================================================
  // d.keys() -> a FRESH list object of the ordered keys (k-cell: it allocates).
```

### 436. rule at lines 58-62 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]

  // ==== dict subscript READ: d[k] (assoc lookup; KeyError is out of subset) ==
```

### 437. rule at lines 63-63 (attributes/classes: equational-rule)

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### 438. syntax at lines 64-64 (attributes/classes: function)

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

### 439. rule at lines 65-69 (attributes/classes: priority(45), operational-k-rule)

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]

  // ==== dict subscript-assign: d[k] = v (insert/update in place) =============
  // Only for a LOCAL dict variable X (the current scope holds it). Reuses dPutK/dPutV.
```

### 440. syntax at lines 70-70 (attributes/classes: function)

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

### 441. rule at lines 71-75 (attributes/classes: equational-rule)

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

  // RHS evaluates first (Assign strictness), then the key. Dispatch on the scope
  // value: a bare dict updates in the scope (dicts stay values); a ref (a heap
  // list — or a heap dict later) writes the heap in place.
```

### 442. syntax at lines 76-76 (attributes/classes: none)

```k
  syntax KItem ::= #dsetK(String, Val)
```

### 443. rule at lines 77-77 (attributes/classes: operational-k-rule)

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### 444. rule at lines 78-81 (attributes/classes: operational-k-rule)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### 445. rule at lines 82-85 (attributes/classes: operational-k-rule)

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### 446. syntax at lines 86-86 (attributes/classes: none)

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

### 447. rule at lines 87-89 (attributes/classes: operational-k-rule)

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
  // negative-index normalization local to the write (subscript.k's is not imported here)
```

### 448. syntax at lines 90-90 (attributes/classes: function, total)

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

### 449. rule at lines 91-91 (attributes/classes: equational-rule)

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### 450. rule at lines 92-94 (attributes/classes: equational-rule)

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== dict == (order-insensitive: same size + same key->value pairs) =======
```

### 451. rule at lines 95-96 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### 452. syntax at lines 97-97 (attributes/classes: function)

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### 453. rule at lines 98-98 (attributes/classes: equational-rule)

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### 454. rule at lines 99-100 (attributes/classes: equational-rule)

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### 455. syntax at lines 101-101 (attributes/classes: function)

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### 456. rule at lines 102-102 (attributes/classes: equational-rule)

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### 457. rule at lines 103-103 (attributes/classes: equational-rule)

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### 458. endmodule at lines 104-104 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/float.k`

### 459. module at lines 14-14 (attributes/classes: none)

```k
module MPY-FLOAT
```

### 460. imports at lines 15-15 (attributes/classes: none)

```k
  imports MPY-OPERATORS
```

### 461. imports at lines 16-16 (attributes/classes: none)

```k
  imports MPY-BUILTINS
```

### 462. imports at lines 17-19 (attributes/classes: none)

```k
  imports FLOAT

  // Float is a value; the float literal evaluates to the K Float.
```

### 463. syntax at lines 20-20 (attributes/classes: none)

```k
  syntax Val ::= Float
```

### 464. rule at lines 21-23 (attributes/classes: opaque/no-evaluators, operational-k-rule)

```k
  rule <k> Float(F:Float) => F ... </k>

  // Int / float true division. OPAQUE for kprove (no-evaluators); concrete for krun.
```

### 465. syntax at lines 24-24 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### 466. rule at lines 25-26 (attributes/classes: equational-rule)

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### 467. rule at lines 27-29 (attributes/classes: equational-rule)

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

  // Int / Int true division (Python: always a float). OPAQUE for kprove; concrete for krun.
```

### 468. syntax at lines 30-30 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### 469. rule at lines 31-31 (attributes/classes: equational-rule)

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### 470. rule at lines 32-36 (attributes/classes: equational-rule)

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

  // float % float (e.g. `number % 1.0` = the fractional part). OPAQUE for kprove, concrete for
  // krun. Python's float `%` is floor-based: a % b = a - floor(a/b)*b (K's %Float is IEEE
  // remainder, which differs — 3.5 %Float 1.0 = -0.5 vs Python 0.5 — so it is NOT used).
```

### 471. syntax at lines 37-37 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### 472. rule at lines 38-38 (attributes/classes: equational-rule)

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### 473. rule at lines 39-42 (attributes/classes: equational-rule)

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

  // float equality — for concrete krun asserts (e.g. `area == 7.5`); the FLOAT.eq hook is fine on
  // concrete floats. kprove proofs return floats structurally and do not compare them.
```

### 474. rule at lines 43-43 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### 475. rule at lines 44-49 (attributes/classes: opaque/no-evaluators, equational-rule)

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

  // float `<` and abs — OPAQUE for kprove ([no-evaluators], so a SYMBOLIC float compare stays an
  // uninterpreted Bool a proof case-splits on — a SINGLE compare per branch, not a nonlinear cascade),
  // [concrete] for krun. Additive, sort-disjoint from the Int rules. (has_close_elements: the pairwise
  // `abs(a-b) < t` proximity test.)
```

### 476. syntax at lines 50-50 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### 477. rule at lines 51-51 (attributes/classes: equational-rule)

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### 478. rule at lines 52-53 (attributes/classes: equational-rule)

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### 479. syntax at lines 54-54 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### 480. rule at lines 55-55 (attributes/classes: equational-rule)

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

### 481. rule at lines 56-60 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

  // ==== math.ceil ===========================================================
  // `import X` is a no-op (we intercept the specific math functions syntactically; `math` itself is
  // never bound as a value).
```

### 482. rule at lines 61-64 (attributes/classes: operational-k-rule)

```k
  rule <k> Import(_:String) => .K ... </k>

  // math.ceil(x): ceiling to an int. Intercepted at the Call BEFORE `math` is looked up (higher
  // priority than the generic Attribute/method dispatch in call.k).
```

### 483. syntax at lines 65-65 (attributes/classes: none)

```k
  syntax KItem ::= "#mathCeil"
```

### 484. rule at lines 66-66 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### 485. rule at lines 67-69 (attributes/classes: operational-k-rule)

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

  // math.floor(x) — same interception shape as math.ceil
```

### 486. syntax at lines 70-70 (attributes/classes: none)

```k
  syntax KItem ::= "#mathFloor"
```

### 487. rule at lines 71-71 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### 488. rule at lines 72-72 (attributes/classes: operational-k-rule)

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### 489. syntax at lines 73-73 (attributes/classes: function, total)

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### 490. rule at lines 74-74 (attributes/classes: equational-rule)

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

### 491. rule at lines 75-77 (attributes/classes: equational-rule)

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

  // bare floor/ceil (bound by `from math import floor, ceil`)
```

### 492. rule at lines 78-78 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### 493. rule at lines 79-81 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

  // math.pow(x, y) — a two-arg interception onto powF (ints promote)
```

### 494. syntax at lines 82-82 (attributes/classes: none)

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### 495. rule at lines 83-83 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### 496. rule at lines 84-84 (attributes/classes: operational-k-rule)

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### 497. rule at lines 85-85 (attributes/classes: operational-k-rule)

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### 498. syntax at lines 86-86 (attributes/classes: function, total)

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### 499. rule at lines 87-87 (attributes/classes: equational-rule)

```k
  rule toF(F:Float) => F        [concrete]
```

### 500. rule at lines 88-92 (attributes/classes: equational-rule)

```k
  rule toF(I:Int)   => intToF(I) [concrete]

  // ceilF: math.ceil as an Int. TOTAL (K trusts it; a symbolic list element stays opaque for
  // kprove — structural). [concrete] so the Int2Float/ceilFloat hooks only run for krun (llvm).
  // Matches Python incl. negatives: ceil(-2.4) = -2 = Float2Int(ceilFloat(-2.4)).
```

### 501. syntax at lines 93-93 (attributes/classes: function, total)

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### 502. rule at lines 94-94 (attributes/classes: equational-rule)

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

### 503. rule at lines 95-98 (attributes/classes: equational-rule)

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

  // unary minus on a float (e.g. the literal -2.4 = UnaryOp("-", Float(2.4))). Concrete for krun;
  // proofs use symbolic elements, never a float literal.
```

### 504. rule at lines 99-102 (attributes/classes: opaque/no-evaluators, equational-rule)

```k
  rule applyUn("-", F:Float) => 0.0 -Float F

  // ---- float - / / / + (OPAQUE for kprove [no-evaluators], concrete for krun) — for float-list
  // element maps (x - lo) / (hi - lo). Mirror intFloatDiv: additive, sort-disjoint from the Int rules.
```

### 505. syntax at lines 103-103 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### 506. rule at lines 104-104 (attributes/classes: equational-rule)

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### 507. rule at lines 105-106 (attributes/classes: equational-rule)

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### 508. syntax at lines 107-107 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### 509. rule at lines 108-108 (attributes/classes: equational-rule)

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### 510. rule at lines 109-110 (attributes/classes: equational-rule)

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### 511. syntax at lines 111-111 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### 512. rule at lines 112-112 (attributes/classes: equational-rule)

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### 513. rule at lines 113-114 (attributes/classes: equational-rule)

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### 514. syntax at lines 115-115 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### 515. rule at lines 116-116 (attributes/classes: equational-rule)

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### 516. rule at lines 117-118 (attributes/classes: equational-rule)

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### 517. syntax at lines 119-119 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### 518. rule at lines 120-120 (attributes/classes: equational-rule)

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### 519. rule at lines 121-124 (attributes/classes: equational-rule)

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

  // ---- the remaining comparisons (gtF promoted from find_zero — its summaries
  //      case-split on the atom; >= / <= derive from the two opaque compares) ----
```

### 520. syntax at lines 125-125 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### 521. rule at lines 126-126 (attributes/classes: equational-rule)

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### 522. rule at lines 127-127 (attributes/classes: equational-rule)

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### 523. rule at lines 128-128 (attributes/classes: equational-rule)

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### 524. rule at lines 129-131 (attributes/classes: equational-rule)

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

  // ---- mixed Int/Float operators promote the Int side (n ** 0.5 etc.) ----
```

### 525. rule at lines 132-132 (attributes/classes: equational-rule)

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### 526. rule at lines 133-133 (attributes/classes: equational-rule)

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### 527. rule at lines 134-134 (attributes/classes: equational-rule)

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### 528. rule at lines 135-135 (attributes/classes: equational-rule)

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### 529. rule at lines 136-136 (attributes/classes: equational-rule)

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### 530. rule at lines 137-137 (attributes/classes: equational-rule)

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### 531. rule at lines 138-138 (attributes/classes: equational-rule)

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### 532. rule at lines 139-141 (attributes/classes: equational-rule)

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

  // ---- mixed Int == Float (shared eqF; opaque symbolic / concrete twin) ----
```

### 533. syntax at lines 142-142 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### 534. rule at lines 143-143 (attributes/classes: equational-rule)

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### 535. rule at lines 144-144 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### 536. rule at lines 145-145 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### 537. rule at lines 146-146 (attributes/classes: equational-rule)

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### 538. rule at lines 147-147 (attributes/classes: equational-rule)

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### 539. rule at lines 148-148 (attributes/classes: equational-rule)

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### 540. rule at lines 149-149 (attributes/classes: equational-rule)

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### 541. rule at lines 150-150 (attributes/classes: equational-rule)

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### 542. rule at lines 151-153 (attributes/classes: equational-rule)

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

  // ---- x == None (promoted from 137; `is` cases live in operators.k) ----
```

### 543. rule at lines 154-154 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### 544. rule at lines 155-159 (attributes/classes: equational-rule)

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

  // ---- float(str): decimal parse (promoted from 137's defined chain) ----
  // digits '.' digits, optional leading '-'; concrete evaluation only (the
  // symbolic side stays an opaque decStrToF term a proof case-splits on).
```

### 545. syntax at lines 160-160 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### 546. rule at lines 161-161 (attributes/classes: equational-rule)

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### 547. rule at lines 162-164 (attributes/classes: equational-rule)

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### 548. syntax at lines 165-165 (attributes/classes: function)

```k
  syntax Int ::= headIS(IntSeq) [function]
```

### 549. rule at lines 166-166 (attributes/classes: equational-rule)

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### 550. syntax at lines 167-167 (attributes/classes: function, total)

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### 551. rule at lines 168-168 (attributes/classes: equational-rule)

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### 552. rule at lines 169-169 (attributes/classes: equational-rule)

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

### 553. rule at lines 170-170 (attributes/classes: equational-rule)

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### 554. rule at lines 171-172 (attributes/classes: equational-rule)

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

### 555. syntax at lines 173-173 (attributes/classes: function, total)

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### 556. rule at lines 174-174 (attributes/classes: equational-rule)

```k
  rule fracPart(.IntSeq) => 0
```

### 557. rule at lines 175-175 (attributes/classes: equational-rule)

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### 558. rule at lines 176-176 (attributes/classes: equational-rule)

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### 559. rule at lines 177-177 (attributes/classes: equational-rule)

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

### 560. rule at lines 178-178 (attributes/classes: equational-rule)

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### 561. syntax at lines 179-179 (attributes/classes: function, total)

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### 562. rule at lines 180-180 (attributes/classes: equational-rule)

```k
  rule fracScale(.IntSeq) => 1
```

### 563. rule at lines 181-181 (attributes/classes: equational-rule)

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### 564. rule at lines 182-182 (attributes/classes: equational-rule)

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### 565. rule at lines 183-183 (attributes/classes: equational-rule)

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

### 566. rule at lines 184-184 (attributes/classes: equational-rule)

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### 567. rule at lines 185-185 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### 568. rule at lines 186-186 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### 569. rule at lines 187-189 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F

  // ---- float / int division (promoted from mean_absolute_deviation) ----
```

### 570. syntax at lines 190-190 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### 571. rule at lines 191-191 (attributes/classes: equational-rule)

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### 572. rule at lines 192-194 (attributes/classes: equational-rule)

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

  // ---- int -> float promotion for the remaining mixed arithmetic/compares ----
```

### 573. syntax at lines 195-195 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### 574. rule at lines 196-196 (attributes/classes: equational-rule)

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### 575. rule at lines 197-197 (attributes/classes: equational-rule)

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### 576. rule at lines 198-198 (attributes/classes: equational-rule)

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### 577. rule at lines 199-199 (attributes/classes: equational-rule)

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### 578. rule at lines 200-200 (attributes/classes: equational-rule)

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### 579. rule at lines 201-201 (attributes/classes: equational-rule)

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### 580. rule at lines 202-202 (attributes/classes: equational-rule)

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### 581. rule at lines 203-203 (attributes/classes: equational-rule)

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### 582. rule at lines 204-204 (attributes/classes: equational-rule)

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### 583. rule at lines 205-205 (attributes/classes: equational-rule)

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### 584. rule at lines 206-208 (attributes/classes: equational-rule)

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

  // ---- conversions: int(float) truncates toward zero; float(int); round; math.sqrt ----
```

### 585. syntax at lines 209-209 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### 586. rule at lines 210-210 (attributes/classes: equational-rule)

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### 587. rule at lines 211-212 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### 588. rule at lines 213-213 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### 589. rule at lines 214-216 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("float", F:Float, .Vals) => F

  // round: Python half-even (banker's); round(F, N) scales by 10^N
```

### 590. syntax at lines 217-217 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### 591. rule at lines 218-222 (attributes/classes: equational-rule)

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### 592. syntax at lines 223-223 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### 593. rule at lines 224-226 (attributes/classes: equational-rule)

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### 594. rule at lines 227-227 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### 595. rule at lines 228-229 (attributes/classes: equational-rule)

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### 596. syntax at lines 230-230 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### 597. rule at lines 231-231 (attributes/classes: equational-rule)

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### 598. syntax at lines 232-232 (attributes/classes: none)

```k
  syntax KItem ::= "#mathSqrt"
```

### 599. rule at lines 233-233 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### 600. rule at lines 234-234 (attributes/classes: operational-k-rule)

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### 601. rule at lines 235-242 (attributes/classes: operational-k-rule)

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

  // ---- min / max over a FLOAT list — FLOAT branch of the shared #minCont0/#maxCont0 folds (which
  // seed/step with `requires isInt(V)`, so they are STUCK on floats). These add the `requires
  // isFloat(V)` seed + a Float-accumulator fold via K's minFloat/maxFloat — concrete for krun. A proof
  // over a SYMBOLIC float list intercepts min/max problem-locally to an opaque minVF/maxVF (at
  // #applyK, priority 40, in its verification.k) BEFORE #minAcc0, so this fold is krun-only. Additive:
  // the isFloat guard is disjoint from the existing isInt one.
```

### 602. syntax at lines 243-243 (attributes/classes: none)

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### 603. rule at lines 244-244 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### 604. rule at lines 245-245 (attributes/classes: operational-k-rule)

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### 605. rule at lines 246-246 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### 606. rule at lines 247-249 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### 607. syntax at lines 250-250 (attributes/classes: none)

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### 608. rule at lines 251-251 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### 609. rule at lines 252-252 (attributes/classes: operational-k-rule)

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### 610. rule at lines 253-253 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### 611. rule at lines 254-260 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)

  // ---- sum over a float list (krun; mirrors the min/max float paths). The Int-only shared
  // #sumCont sticks on a Float yield; switch to a Float-headed fold via addF (concrete twin).
  // The switch guard carries the SYNTACTIC negation of the Int rule's guard so a symbolic proof
  // with isInt(V) in its path condition refutes this branch without sort reasoning.
```

### 612. syntax at lines 261-261 (attributes/classes: none)

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### 613. rule at lines 262-264 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### 614. rule at lines 265-265 (attributes/classes: operational-k-rule)

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### 615. rule at lines 266-266 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### 616. rule at lines 267-269 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

### 617. rule at lines 270-272 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

### 618. endmodule at lines 273-273 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/functions.k`

### 619. module at lines 3-3 (attributes/classes: none)

```k
module MPY-FUNCTIONS
```

### 620. imports at lines 4-7 (attributes/classes: none)

```k
  imports MPY-CORE

  // call routing + callee/arg evaluation (#callee/#args/#argCont) live in call.k;
  // this module owns the frame lifecycle (bind params, return, pop).
```

### 621. syntax at lines 8-13 (attributes/classes: none)

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"

  // ==== def / anonymous closure =============================================
```

### 622. rule at lines 14-17 (attributes/classes: operational-k-rule)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### 623. syntax at lines 18-18 (attributes/classes: none)

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### 624. rule at lines 19-26 (attributes/classes: operational-k-rule)

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>

  // ==== annotated def/lambda (closure cells; spec 2.3) ======================
  // closureValC(params, cellvars, body, captured-cells). No frame anchor: all
  // enclosing-local reads are freevars (symtable-complete) and go through the
  // captured cells; everything else is global/builtin, so the callee frame's
  // parent is the module scope (0) — sound after the defining frame dies.
```

### 625. syntax at lines 27-30 (attributes/classes: none)

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

  // capture: resolve each freevar to the enclosing frame's cellRef, then bind
  // (FuncDef) or yield (Lambda) the closure value.
```

### 626. syntax at lines 31-32 (attributes/classes: none)

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### 627. rule at lines 33-35 (attributes/classes: operational-k-rule)

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### 628. rule at lines 36-41 (attributes/classes: operational-k-rule)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### 629. rule at lines 42-46 (attributes/classes: operational-k-rule)

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### 630. rule at lines 47-49 (attributes/classes: operational-k-rule)

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

### 631. rule at lines 50-52 (attributes/classes: operational-k-rule)

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### 632. rule at lines 53-58 (attributes/classes: operational-k-rule)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

### 633. rule at lines 59-62 (attributes/classes: operational-k-rule)

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>

  // ==== bind params ========================================================
```

### 634. rule at lines 63-63 (attributes/classes: operational-k-rule)

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### 635. rule at lines 64-67 (attributes/classes: operational-k-rule)

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
  // a param that is a cellvar was pre-bound to its cell at frame entry
```

### 636. rule at lines 68-77 (attributes/classes: priority(40), operational-k-rule)

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

### 637. rule at lines 78-79 (attributes/classes: operational-k-rule)

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

### 638. rule at lines 80-84 (attributes/classes: operational-k-rule)

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
  // pop: restore env, DEALLOCATE the callee frame, and wind scopeLoc back (LIFO allocation
  // makes the saved loc the callee frame's own loc). Sound because no closureVal outlives its
  // defining frame (frontend subset: no returned/stored closures; module defs live in loc 0).
```

### 639. rule at lines 85-90 (attributes/classes: operational-k-rule)

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

### 640. endmodule at lines 91-91 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/int.k`

### 641. module at lines 4-4 (attributes/classes: none)

```k
module MPY-INT
```

### 642. imports at lines 5-6 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 643. rule at lines 7-8 (attributes/classes: equational-rule)

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

### 644. rule at lines 9-10 (attributes/classes: equational-rule)

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
  // Bool participates in int arithmetic (x += (a == b))
```

### 645. rule at lines 11-11 (attributes/classes: equational-rule)

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### 646. rule at lines 12-12 (attributes/classes: equational-rule)

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### 647. rule at lines 13-13 (attributes/classes: equational-rule)

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### 648. rule at lines 14-14 (attributes/classes: equational-rule)

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### 649. rule at lines 15-15 (attributes/classes: equational-rule)

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### 650. rule at lines 16-16 (attributes/classes: equational-rule)

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### 651. rule at lines 17-18 (attributes/classes: equational-rule)

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### 652. syntax at lines 19-19 (attributes/classes: function)

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

### 653. rule at lines 20-21 (attributes/classes: equational-rule)

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### 654. rule at lines 22-22 (attributes/classes: equational-rule)

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### 655. rule at lines 23-23 (attributes/classes: equational-rule)

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### 656. rule at lines 24-24 (attributes/classes: equational-rule)

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### 657. rule at lines 25-25 (attributes/classes: equational-rule)

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### 658. rule at lines 26-26 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### 659. rule at lines 27-27 (attributes/classes: equational-rule)

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### 660. endmodule at lines 28-28 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/iter.k`

### 661. module at lines 6-6 (attributes/classes: none)

```k
module MPY-ITER
```

### 662. imports at lines 7-7 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 663. syntax at lines 8-8 (attributes/classes: none)

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### 664. endmodule at lines 9-9 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/list.k`

### 665. module at lines 3-3 (attributes/classes: none)

```k
module MPY-LIST
```

### 666. imports at lines 4-4 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 667. imports at lines 5-5 (attributes/classes: none)

```k
  imports MPY-ITER
```

### 668. imports at lines 6-8 (attributes/classes: none)

```k
  imports MPY-OPERATORS

  // ==== iteration (the iterator protocol's list case) =======================
```

### 669. rule at lines 9-9 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### 670. rule at lines 10-12 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

  // ==== ListExpr: [...] literal -> a fresh heap object =======================
```

### 671. syntax at lines 13-13 (attributes/classes: none)

```k
  syntax ApplyK ::= "toList"
```

### 672. rule at lines 14-14 (attributes/classes: operational-k-rule)

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### 673. rule at lines 15-17 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

  // ==== list ops: + / == / != ===============================================
```

### 674. syntax at lines 18-18 (attributes/classes: function, total)

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### 675. rule at lines 19-19 (attributes/classes: equational-rule)

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### 676. rule at lines 20-23 (attributes/classes: priority(45), equational-rule)

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

  // list + list constructs a NEW object (k-cell — it allocates; operands land here
  // already deref'd). priority(45) beats the generic BinOp dispatch.
```

### 677. rule at lines 24-26 (attributes/classes: priority(45), operational-k-rule)

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

### 678. rule at lines 27-27 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### 679. rule at lines 28-32 (attributes/classes: equational-rule)

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

  // ==== deep equality when elements are heap objects (list-of-lists) ========
  // Python == is structural at every depth. Fires ONLY when a ref is present
  // (the guard decides on concrete seqs); the plain ==K path above is unchanged.
```

### 680. syntax at lines 33-33 (attributes/classes: function, total)

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### 681. rule at lines 34-34 (attributes/classes: equational-rule)

```k
  rule hasRefVS(.ValSeq)                => false
```

### 682. rule at lines 35-36 (attributes/classes: equational-rule)

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### 683. syntax at lines 37-38 (attributes/classes: function)

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

### 684. rule at lines 39-39 (attributes/classes: equational-rule)

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### 685. rule at lines 40-40 (attributes/classes: equational-rule)

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### 686. rule at lines 41-41 (attributes/classes: equational-rule)

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### 687. rule at lines 42-44 (attributes/classes: equational-rule)

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### 688. rule at lines 45-46 (attributes/classes: equational-rule)

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

### 689. rule at lines 47-48 (attributes/classes: equational-rule)

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

### 690. rule at lines 49-49 (attributes/classes: equational-rule)

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### 691. rule at lines 50-52 (attributes/classes: owise, equational-rule)

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

  // ==== mutator: xs.append(v) — an in-place heap write ======================
```

### 692. rule at lines 53-57 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]

  // ==== `x in list` — a <k>-cell fold over #iterNext ========================
```

### 693. syntax at lines 58-58 (attributes/classes: none)

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### 694. rule at lines 59-59 (attributes/classes: operational-k-rule)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### 695. rule at lines 60-60 (attributes/classes: operational-k-rule)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### 696. rule at lines 61-61 (attributes/classes: operational-k-rule)

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### 697. rule at lines 62-62 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### 698. rule at lines 63-64 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

### 699. rule at lines 65-66 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

### 700. rule at lines 67-67 (attributes/classes: operational-k-rule)

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### 701. endmodule at lines 68-68 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/methods.k`

### 702. module at lines 3-3 (attributes/classes: none)

```k
module MPY-METHODS
```

### 703. imports at lines 4-4 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 704. imports at lines 5-5 (attributes/classes: none)

```k
  imports K-EQUAL
```

### 705. imports at lines 6-6 (attributes/classes: none)

```k
  imports MPY-STR
```

### 706. imports at lines 7-9 (attributes/classes: none)

```k
  imports MPY-LIST

  // method-call routing + arg-eval live in call.k; this module owns applyMethod.
```

### 707. syntax at lines 10-12 (attributes/classes: function)

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]

  // ==== string predicates (Python semantics) =================================
```

### 708. rule at lines 13-13 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### 709. rule at lines 14-14 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### 710. rule at lines 15-15 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### 711. rule at lines 16-18 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

  // ==== case maps ============================================================
```

### 712. rule at lines 19-19 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### 713. rule at lines 20-20 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### 714. rule at lines 21-25 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

  // ==== join / count / strip / encode ========================================
  // S.join(list-of-str): fold with separator codes (receiver + arg deref'd by
  // the call layer; the result str is a value)
```

### 715. rule at lines 26-26 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### 716. syntax at lines 27-27 (attributes/classes: function, total)

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### 717. rule at lines 28-28 (attributes/classes: equational-rule)

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### 718. rule at lines 29-29 (attributes/classes: equational-rule)

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### 719. rule at lines 30-33 (attributes/classes: equational-rule)

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

  // S.count(sub): non-overlapping window scan (Python str.count)
```

### 720. rule at lines 34-34 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### 721. syntax at lines 35-35 (attributes/classes: function)

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### 722. rule at lines 36-36 (attributes/classes: equational-rule)

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

### 723. rule at lines 37-38 (attributes/classes: equational-rule)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### 724. rule at lines 39-40 (attributes/classes: equational-rule)

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### 725. syntax at lines 41-41 (attributes/classes: function, total)

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### 726. rule at lines 42-42 (attributes/classes: equational-rule)

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### 727. rule at lines 43-43 (attributes/classes: owise, equational-rule)

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### 728. rule at lines 44-46 (attributes/classes: equational-rule)

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

  // S.strip(): trim whitespace runs from both ends
```

### 729. rule at lines 47-47 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### 730. syntax at lines 48-48 (attributes/classes: function, total)

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### 731. rule at lines 49-49 (attributes/classes: equational-rule)

```k
  rule trimWS(.IntSeq) => .IntSeq
```

### 732. rule at lines 50-50 (attributes/classes: equational-rule)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### 733. rule at lines 51-51 (attributes/classes: equational-rule)

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### 734. syntax at lines 52-52 (attributes/classes: function, total)

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### 735. rule at lines 53-53 (attributes/classes: equational-rule)

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### 736. rule at lines 54-54 (attributes/classes: equational-rule)

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

### 737. rule at lines 55-57 (attributes/classes: equational-rule)

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

  // S.encode('ascii'): identity on the code-sequence model (bytes == codes)
```

### 738. rule at lines 58-60 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

  // ==== prefix ===============================================================
```

### 739. rule at lines 61-63 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

  // ==== list.count(v) — number of occurrences of v in the list (concrete for krun) ==========
```

### 740. rule at lines 64-64 (attributes/classes: equational-rule)

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### 741. syntax at lines 65-65 (attributes/classes: function, total)

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### 742. rule at lines 66-66 (attributes/classes: equational-rule)

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

### 743. rule at lines 67-67 (attributes/classes: equational-rule)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### 744. rule at lines 68-71 (attributes/classes: equational-rule)

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

  // ==== split (no-arg: on whitespace runs, dropping empty tokens) + replace (single char) ==========
  // Concrete string ops for krun. A proof over a symbolic string intercepts the split problem-locally.
```

### 745. rule at lines 72-74 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

### 746. syntax at lines 75-75 (attributes/classes: function)

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### 747. rule at lines 76-76 (attributes/classes: equational-rule)

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### 748. rule at lines 77-78 (attributes/classes: equational-rule)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

### 749. rule at lines 79-81 (attributes/classes: equational-rule)

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
  // flush the current token to the result list iff non-empty.
```

### 750. syntax at lines 82-82 (attributes/classes: function)

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### 751. rule at lines 83-83 (attributes/classes: equational-rule)

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### 752. rule at lines 84-84 (attributes/classes: equational-rule)

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### 753. syntax at lines 85-85 (attributes/classes: function, total)

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

### 754. rule at lines 86-88 (attributes/classes: equational-rule)

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

  // split(sep='x') keyword form delegates to the positional k-cell rule
```

### 755. rule at lines 89-93 (attributes/classes: priority(39), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]

  // str.split(sep) — single-char separator, KEEPING empty parts (Python's sep-split; len == #sep + 1).
```

### 756. rule at lines 94-96 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

### 757. syntax at lines 97-97 (attributes/classes: function)

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### 758. rule at lines 98-98 (attributes/classes: equational-rule)

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### 759. rule at lines 99-100 (attributes/classes: equational-rule)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

### 760. rule at lines 101-103 (attributes/classes: equational-rule)

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

### 761. rule at lines 104-105 (attributes/classes: equational-rule)

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

### 762. syntax at lines 106-106 (attributes/classes: function, total)

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### 763. rule at lines 107-107 (attributes/classes: equational-rule)

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### 764. rule at lines 108-108 (attributes/classes: equational-rule)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### 765. rule at lines 109-111 (attributes/classes: equational-rule)

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

  // ==== char helpers =========================================================
```

### 766. syntax at lines 112-112 (attributes/classes: function, total)

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

### 767. rule at lines 113-114 (attributes/classes: equational-rule)

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### 768. syntax at lines 115-115 (attributes/classes: function, total)

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

### 769. rule at lines 116-117 (attributes/classes: equational-rule)

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### 770. syntax at lines 118-118 (attributes/classes: function, total)

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

### 771. rule at lines 119-120 (attributes/classes: equational-rule)

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### 772. syntax at lines 121-121 (attributes/classes: function, total)

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

### 773. rule at lines 122-123 (attributes/classes: equational-rule)

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### 774. syntax at lines 124-124 (attributes/classes: function, total)

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### 775. rule at lines 125-125 (attributes/classes: equational-rule)

```k
  rule hasUpper(.IntSeq) => false
```

### 776. rule at lines 126-127 (attributes/classes: equational-rule)

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### 777. syntax at lines 128-128 (attributes/classes: function, total)

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

### 778. rule at lines 129-129 (attributes/classes: equational-rule)

```k
  rule hasLower(.IntSeq) => false
```

### 779. rule at lines 130-131 (attributes/classes: equational-rule)

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### 780. syntax at lines 132-132 (attributes/classes: function, total)

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### 781. rule at lines 133-133 (attributes/classes: equational-rule)

```k
  rule allAlpha(.IntSeq) => true
```

### 782. rule at lines 134-135 (attributes/classes: equational-rule)

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### 783. syntax at lines 136-136 (attributes/classes: function, total)

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

### 784. rule at lines 137-137 (attributes/classes: equational-rule)

```k
  rule allDigit(.IntSeq) => true
```

### 785. rule at lines 138-139 (attributes/classes: equational-rule)

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### 786. syntax at lines 140-141 (attributes/classes: function, total)

```k
  syntax Int ::= lowerC(Int) [function, total]
```

### 787. rule at lines 142-142 (attributes/classes: equational-rule)

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### 788. rule at lines 143-144 (attributes/classes: owise, equational-rule)

```k
  rule lowerC(C:Int) => C         [owise]
```

### 789. syntax at lines 145-145 (attributes/classes: function, total)

```k
  syntax Int ::= upperC(Int) [function, total]
```

### 790. rule at lines 146-146 (attributes/classes: equational-rule)

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### 791. rule at lines 147-148 (attributes/classes: owise, equational-rule)

```k
  rule upperC(C:Int) => C         [owise]
```

### 792. syntax at lines 149-149 (attributes/classes: function, total)

```k
  syntax Int ::= swapC(Int) [function, total]
```

### 793. rule at lines 150-150 (attributes/classes: equational-rule)

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### 794. rule at lines 151-151 (attributes/classes: equational-rule)

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### 795. rule at lines 152-153 (attributes/classes: owise, equational-rule)

```k
  rule swapC(C:Int) => C         [owise]
```

### 796. syntax at lines 154-154 (attributes/classes: function, total)

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### 797. rule at lines 155-155 (attributes/classes: equational-rule)

```k
  rule mapLower(.IntSeq) => .IntSeq
```

### 798. rule at lines 156-157 (attributes/classes: equational-rule)

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### 799. syntax at lines 158-158 (attributes/classes: function, total)

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### 800. rule at lines 159-159 (attributes/classes: equational-rule)

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

### 801. rule at lines 160-161 (attributes/classes: equational-rule)

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### 802. syntax at lines 162-162 (attributes/classes: function, total)

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### 803. rule at lines 163-163 (attributes/classes: equational-rule)

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

### 804. rule at lines 164-165 (attributes/classes: equational-rule)

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### 805. syntax at lines 166-166 (attributes/classes: function, total)

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### 806. rule at lines 167-167 (attributes/classes: equational-rule)

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

### 807. rule at lines 168-168 (attributes/classes: equational-rule)

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### 808. rule at lines 169-169 (attributes/classes: equational-rule)

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### 809. endmodule at lines 170-170 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/operators.k`

### 810. module at lines 6-6 (attributes/classes: none)

```k
module MPY-OPERATORS
```

### 811. imports at lines 7-7 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 812. imports at lines 8-9 (attributes/classes: none)

```k
  imports MPY-ITER
```

### 813. rule at lines 10-11 (attributes/classes: operational-k-rule)

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### 814. rule at lines 12-14 (attributes/classes: operational-k-rule)

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

  // Compare's right operand sits under the CmpOp wrapper — contexts instead of attributes
```

### 815. context at lines 15-15 (attributes/classes: none)

```k
  context Compare(HOLE, _)
```

### 816. context at lines 16-16 (attributes/classes: none)

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

### 817. rule at lines 17-18 (attributes/classes: owise, operational-k-rule)

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### 818. rule at lines 19-19 (attributes/classes: equational-rule)

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### 819. rule at lines 20-24 (attributes/classes: priority(40), equational-rule)

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

  // ==== operand deref: heap objects combine/compare by STRUCTURE ============
  // (Python: list == is structural; identity only via `is`.) priority(40)
  // preempts the generic dispatch so applyUn/applyBin/applyCmp never see a ref.
```

### 820. rule at lines 25-27 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 821. rule at lines 28-33 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]

  // the left operand of `in`/`not in` is an ELEMENT (compares by ==K) — never deref'd
```

### 822. rule at lines 34-37 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

### 823. rule at lines 38-43 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

### 824. rule at lines 44-46 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 825. endmodule at lines 47-47 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/range.k`

### 826. module at lines 5-5 (attributes/classes: none)

```k
module MPY-RANGE
```

### 827. imports at lines 6-6 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 828. imports at lines 7-8 (attributes/classes: none)

```k
  imports MPY-ITER
```

### 829. syntax at lines 9-9 (attributes/classes: function, total)

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### 830. rule at lines 10-11 (attributes/classes: equational-rule)

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### 831. syntax at lines 12-12 (attributes/classes: function)

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### 832. rule at lines 13-14 (attributes/classes: equational-rule)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

### 833. rule at lines 15-16 (attributes/classes: equational-rule)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

### 834. rule at lines 17-19 (attributes/classes: equational-rule)

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### 835. rule at lines 20-22 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

### 836. rule at lines 23-24 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

### 837. endmodule at lines 25-25 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/set.k`

### 838. module at lines 3-3 (attributes/classes: none)

```k
module MPY-SET
```

### 839. imports at lines 4-7 (attributes/classes: none)

```k
  imports MPY-CORE

  // a set value, carried as its distinct codes in first-seen order (order is irrelevant
  // to membership/cardinality — the two observations sets support here).
```

### 840. syntax at lines 8-10 (attributes/classes: none)

```k
  syntax Val ::= setV(IntSeq)

  // membership of a code in the accumulated distinct-code sequence
```

### 841. syntax at lines 11-11 (attributes/classes: function, total)

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### 842. rule at lines 12-12 (attributes/classes: equational-rule)

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

### 843. rule at lines 13-15 (attributes/classes: equational-rule)

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

  // the distinct codes of CS (insert-if-absent fold, first-seen order)
```

### 844. syntax at lines 16-17 (attributes/classes: function, total)

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### 845. rule at lines 18-18 (attributes/classes: equational-rule)

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### 846. rule at lines 19-19 (attributes/classes: equational-rule)

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### 847. rule at lines 20-21 (attributes/classes: equational-rule)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

### 848. rule at lines 22-24 (attributes/classes: equational-rule)

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

### 849. syntax at lines 25-25 (attributes/classes: function, total)

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### 850. rule at lines 26-26 (attributes/classes: equational-rule)

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### 851. rule at lines 27-30 (attributes/classes: equational-rule)

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

  // ==== set equality: two sets are equal iff mutually subsuming ==============
  // subsetCodes(A, B) — every code of A occurs in B (duplicates in A are harmless).
```

### 852. syntax at lines 31-31 (attributes/classes: function, total)

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### 853. rule at lines 32-32 (attributes/classes: equational-rule)

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### 854. rule at lines 33-34 (attributes/classes: equational-rule)

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### 855. syntax at lines 35-35 (attributes/classes: function, total)

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### 856. rule at lines 36-38 (attributes/classes: equational-rule)

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

  // set == set  (the only comparison sets support here)
```

### 857. rule at lines 39-39 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### 858. endmodule at lines 40-40 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/sort.k`

### 859. module at lines 10-10 (attributes/classes: none)

```k
module MPY-SORT
```

### 860. imports at lines 11-11 (attributes/classes: none)

```k
  imports MPY-BUILTINS
```

### 861. imports at lines 12-17 (attributes/classes: opaque/no-evaluators)

```k
  imports MPY-SUBSCRIPT

  // sortVS(VS): the ascending sort of the Val list VS. Opaque for symbolic VS (no-evaluators);
  // concrete insertion sort for krun.
  // Concrete sort matches Int-sorted elements directly (an int Val IS an Int); projectIntTotal
  // (lemmas-only) is not available in the semantics. Int and str lists.
```

### 862. syntax at lines 18-18 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### 863. syntax at lines 19-19 (attributes/classes: function)

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### 864. rule at lines 20-20 (attributes/classes: equational-rule)

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### 865. rule at lines 21-21 (attributes/classes: equational-rule)

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### 866. rule at lines 22-22 (attributes/classes: equational-rule)

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### 867. rule at lines 23-23 (attributes/classes: equational-rule)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### 868. rule at lines 24-25 (attributes/classes: equational-rule)

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
  // str elements insert by the shared lexicographic strLt (methods.k)
```

### 869. syntax at lines 26-26 (attributes/classes: function)

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### 870. rule at lines 27-27 (attributes/classes: equational-rule)

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### 871. rule at lines 28-28 (attributes/classes: equational-rule)

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### 872. rule at lines 29-30 (attributes/classes: equational-rule)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

### 873. rule at lines 31-35 (attributes/classes: owise, equational-rule)

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]

  // sorted(list) constructs a NEW object: k-cell pre-dispatch (beats the [owise]
  // applyBuiltin routing in call.k) so the result allocates.
```

### 874. rule at lines 36-39 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>

  // mutator: xs.sort() — the in-place heap write over the same trusted sortVS
```

### 875. rule at lines 40-48 (attributes/classes: priority(40), priority(40), operational-k-rule)

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

### 876. syntax at lines 49-50 (attributes/classes: function, total, opaque/no-evaluators)

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### 877. syntax at lines 51-52 (attributes/classes: function, total)

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

### 878. rule at lines 53-53 (attributes/classes: equational-rule)

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### 879. rule at lines 54-54 (attributes/classes: equational-rule)

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### 880. rule at lines 55-56 (attributes/classes: equational-rule)

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### 881. syntax at lines 57-57 (attributes/classes: function, total)

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### 882. rule at lines 58-58 (attributes/classes: equational-rule)

```k
  rule condRev(S:ValSeq, false) => S
```

### 883. rule at lines 59-60 (attributes/classes: equational-rule)

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

### 884. rule at lines 61-62 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### 885. rule at lines 63-64 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### 886. rule at lines 65-71 (attributes/classes: total, operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

  // Indexing the opaque sorted list: `valSeqAt(sortVS(VS), I)` is DEFINED because valSeqAt is
  // [total] (subscript.k) — it stays an abstract total value for a symbolic sort and reduces
  // over the concrete sort for krun. No separate sortedAt indirection is needed; wrappers write
  // their postcondition directly as valSeqAt(sortVS(VS), …).
```

### 887. endmodule at lines 72-72 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/str.k`

### 888. module at lines 3-3 (attributes/classes: none)

```k
module MPY-STR
```

### 889. imports at lines 4-4 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 890. imports at lines 5-7 (attributes/classes: none)

```k
  imports MPY-ITER

  // ==== iteration (the iterator protocol's str case; yields 1-char strings) ==
```

### 891. rule at lines 8-8 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### 892. rule at lines 9-12 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

  // ==== str literal (ASCII-only) ============================================
```

### 893. syntax at lines 13-13 (attributes/classes: function)

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

### 894. rule at lines 14-14 (attributes/classes: operational-k-rule)

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### 895. rule at lines 15-15 (attributes/classes: equational-rule)

```k
  rule strToCodes("") => .IntSeq
```

### 896. rule at lines 16-19 (attributes/classes: equational-rule)

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

  // ==== operators: + / == / != / in =========================================
```

### 897. syntax at lines 20-20 (attributes/classes: function, total)

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### 898. rule at lines 21-21 (attributes/classes: equational-rule)

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### 899. rule at lines 22-23 (attributes/classes: equational-rule)

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### 900. rule at lines 24-24 (attributes/classes: equational-rule)

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### 901. rule at lines 25-25 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### 902. rule at lines 26-28 (attributes/classes: equational-rule)

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

  // substring membership: `P in X` iff the code-seq P occurs contiguously in X
```

### 903. rule at lines 29-29 (attributes/classes: equational-rule)

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### 904. rule at lines 30-31 (attributes/classes: equational-rule)

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### 905. syntax at lines 32-32 (attributes/classes: function, total)

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### 906. rule at lines 33-33 (attributes/classes: equational-rule)

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### 907. rule at lines 34-34 (attributes/classes: equational-rule)

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### 908. rule at lines 35-36 (attributes/classes: equational-rule)

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### 909. syntax at lines 37-37 (attributes/classes: function, total)

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### 910. rule at lines 38-38 (attributes/classes: equational-rule)

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### 911. rule at lines 39-39 (attributes/classes: equational-rule)

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### 912. rule at lines 40-47 (attributes/classes: equational-rule)

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))

  // ==== lexicographic order: < / <= / > / >= by code point (= Python str order on the code
  // model). strLt reduces on GROUND code-seqs (krun) but is inert/OPAQUE on symbolic ones
  // (a proof's codesProj(V) is an abstract IntSeq — no constructor rule matches), so a symbolic
  // str `<` stays a trusted opaque term the way sortVS / intFloatDiv do. Additive: fires only on
  // str </<=/>/>= comparisons.
```

### 913. syntax at lines 48-48 (attributes/classes: function, total)

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### 914. rule at lines 49-49 (attributes/classes: equational-rule)

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

### 915. rule at lines 50-50 (attributes/classes: equational-rule)

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### 916. rule at lines 51-51 (attributes/classes: equational-rule)

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### 917. rule at lines 52-52 (attributes/classes: equational-rule)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### 918. rule at lines 53-53 (attributes/classes: equational-rule)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### 919. rule at lines 54-55 (attributes/classes: equational-rule)

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### 920. rule at lines 56-56 (attributes/classes: equational-rule)

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### 921. rule at lines 57-57 (attributes/classes: equational-rule)

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### 922. rule at lines 58-58 (attributes/classes: equational-rule)

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### 923. rule at lines 59-59 (attributes/classes: equational-rule)

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### 924. endmodule at lines 60-60 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/subscript.k`

### 925. module at lines 3-3 (attributes/classes: none)

```k
module MPY-SUBSCRIPT
```

### 926. imports at lines 4-10 (attributes/classes: total)

```k
  imports MPY-CORE

  // ==== positional access + negative-index normalization (used only here) ===
  // valSeqAt is [total]: in-bounds vCons access reduces as usual; on an OPAQUE sequence (e.g.
  // a trusted sort's sortVS(VS)) or OOB it stays an abstract total value — so indexing the
  // opaque sorted list is DEFINED (no undischarged #Ceil), matching the old semantics' total
  // atK. K trusts the [total] annotation; valid programs index in-bounds.
```

### 927. syntax at lines 11-11 (attributes/classes: function, total)

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### 928. rule at lines 12-12 (attributes/classes: equational-rule)

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### 929. rule at lines 13-15 (attributes/classes: equational-rule)

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

### 930. syntax at lines 16-16 (attributes/classes: function)

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### 931. rule at lines 17-17 (attributes/classes: equational-rule)

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### 932. rule at lines 18-20 (attributes/classes: equational-rule)

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

### 933. syntax at lines 21-21 (attributes/classes: function, total)

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

### 934. rule at lines 22-22 (attributes/classes: equational-rule)

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### 935. rule at lines 23-26 (attributes/classes: equational-rule)

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

  // ==== Subscript: indexing obj[i] (list / tuple / str) =====================
  // contexts (not strict attrs): the Index slot's Slice alternative must never heat
```

### 936. context at lines 27-27 (attributes/classes: none)

```k
  context Subscript(HOLE, _)
```

### 937. context at lines 28-30 (attributes/classes: none)

```k
  context Subscript(_:Val, HOLE:Expr)

  // heap-object deref (covers both the index and slice forms via the Index slot)
```

### 938. rule at lines 31-34 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 939. rule at lines 35-36 (attributes/classes: operational-k-rule)

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### 940. syntax at lines 37-37 (attributes/classes: function)

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

### 941. rule at lines 38-38 (attributes/classes: equational-rule)

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### 942. rule at lines 39-39 (attributes/classes: equational-rule)

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### 943. rule at lines 40-43 (attributes/classes: equational-rule)

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

  // ==== Slice: obj[lo:hi:step] (list / str) — CPython slice.indices ==========
```

### 944. syntax at lines 44-48 (attributes/classes: none)

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

### 945. syntax at lines 49-49 (attributes/classes: none)

```k
  syntax OptInt ::= "noB" | someB(Int)
```

### 946. rule at lines 50-50 (attributes/classes: operational-k-rule)

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

### 947. rule at lines 51-51 (attributes/classes: operational-k-rule)

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### 948. rule at lines 52-53 (attributes/classes: operational-k-rule)

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### 949. rule at lines 54-54 (attributes/classes: operational-k-rule)

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### 950. rule at lines 55-55 (attributes/classes: operational-k-rule)

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### 951. rule at lines 56-57 (attributes/classes: operational-k-rule)

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
  // a list slice constructs a NEW object; a str slice stays a value
```

### 952. rule at lines 58-60 (attributes/classes: priority(45), operational-k-rule)

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

### 953. rule at lines 61-62 (attributes/classes: operational-k-rule)

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### 954. syntax at lines 63-63 (attributes/classes: function)

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### 955. rule at lines 64-65 (attributes/classes: equational-rule)

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### 956. rule at lines 66-67 (attributes/classes: equational-rule)

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### 957. rule at lines 68-71 (attributes/classes: equational-rule)

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

  // ==== slice.indices: step / start / stop / clamp ==========================
```

### 958. syntax at lines 72-72 (attributes/classes: function, total)

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

### 959. rule at lines 73-73 (attributes/classes: equational-rule)

```k
  rule slStep(noB)          => 1
```

### 960. rule at lines 74-75 (attributes/classes: equational-rule)

```k
  rule slStep(someB(S:Int)) => S
```

### 961. syntax at lines 76-76 (attributes/classes: function)

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### 962. rule at lines 77-78 (attributes/classes: equational-rule)

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

### 963. rule at lines 79-80 (attributes/classes: equational-rule)

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

### 964. rule at lines 81-82 (attributes/classes: equational-rule)

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### 965. syntax at lines 83-83 (attributes/classes: function)

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### 966. rule at lines 84-85 (attributes/classes: equational-rule)

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

### 967. rule at lines 86-87 (attributes/classes: equational-rule)

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

### 968. rule at lines 88-89 (attributes/classes: equational-rule)

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### 969. syntax at lines 90-90 (attributes/classes: function, total)

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### 970. rule at lines 91-92 (attributes/classes: equational-rule)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

### 971. rule at lines 93-95 (attributes/classes: equational-rule)

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

### 972. syntax at lines 96-96 (attributes/classes: function, total)

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

### 973. rule at lines 97-98 (attributes/classes: equational-rule)

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

### 974. rule at lines 99-101 (attributes/classes: equational-rule)

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

### 975. syntax at lines 102-102 (attributes/classes: function, total)

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### 976. rule at lines 103-104 (attributes/classes: equational-rule)

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

### 977. rule at lines 105-108 (attributes/classes: equational-rule)

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN

  // ==== build the strided sub-sequence (indices in range by construction) ====
```

### 978. syntax at lines 109-109 (attributes/classes: function)

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### 979. rule at lines 110-112 (attributes/classes: equational-rule)

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### 980. rule at lines 113-115 (attributes/classes: equational-rule)

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### 981. syntax at lines 116-116 (attributes/classes: function)

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### 982. rule at lines 117-119 (attributes/classes: equational-rule)

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### 983. rule at lines 120-121 (attributes/classes: equational-rule)

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### 984. endmodule at lines 122-122 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/syntax.k`

### 985. module at lines 3-3 (attributes/classes: none)

```k
module MPY-SYNTAX
```

### 986. imports at lines 4-4 (attributes/classes: none)

```k
  imports INT-SYNTAX
```

### 987. imports at lines 5-5 (attributes/classes: none)

```k
  imports FLOAT-SYNTAX
```

### 988. imports at lines 6-6 (attributes/classes: none)

```k
  imports BOOL-SYNTAX
```

### 989. imports at lines 7-8 (attributes/classes: none)

```k
  imports STRING-SYNTAX
```

### 990. syntax at lines 9-31 (attributes/classes: macro)

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

### 991. syntax at lines 32-32 (attributes/classes: none)

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### 992. syntax at lines 33-33 (attributes/classes: none)

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### 993. syntax at lines 34-34 (attributes/classes: none)

```k
  syntax Entries  ::= List{Entry, ","}
```

### 994. syntax at lines 35-35 (attributes/classes: none)

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### 995. syntax at lines 36-36 (attributes/classes: none)

```k
  syntax CompFors ::= List{CompFor, ""}
```

### 996. syntax at lines 37-37 (attributes/classes: none)

```k
  syntax Exprs    ::= List{Expr, ","}
```

### 997. syntax at lines 38-38 (attributes/classes: none)

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### 998. syntax at lines 39-40 (attributes/classes: none)

```k
  syntax Bound    ::= Expr | "NoBound"
```

### 999. syntax at lines 41-55 (attributes/classes: none)

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

### 1000. syntax at lines 56-56 (attributes/classes: none)

```k
  syntax Stmts      ::= List{Stmt, ""}
```

### 1001. syntax at lines 57-57 (attributes/classes: none)

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

### 1002. syntax at lines 58-58 (attributes/classes: none)

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### 1003. syntax at lines 59-59 (attributes/classes: none)

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### 1004. syntax at lines 60-60 (attributes/classes: none)

```k
  syntax ParamNames ::= List{String, ","}
```

### 1005. syntax at lines 61-61 (attributes/classes: none)

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

### 1006. endmodule at lines 62-62 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics/tuple.k`

### 1007. module at lines 3-3 (attributes/classes: none)

```k
module MPY-TUPLE
```

### 1008. imports at lines 4-4 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 1009. imports at lines 5-5 (attributes/classes: none)

```k
  imports MPY-ITER
```

### 1010. imports at lines 6-6 (attributes/classes: none)

```k
  imports MPY-LIST
```

### 1011. imports at lines 7-9 (attributes/classes: none)

```k
  imports MPY-METHODS

  // ==== iteration (the iterator protocol's tuple case) ======================
```

### 1012. rule at lines 10-10 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### 1013. rule at lines 11-13 (attributes/classes: operational-k-rule)

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

  // ==== TupleExpr: tuple(ValSeq) literal + == != ===========================
```

### 1014. syntax at lines 14-14 (attributes/classes: none)

```k
  syntax ApplyK ::= "toTuple"
```

### 1015. rule at lines 15-15 (attributes/classes: operational-k-rule)

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### 1016. rule at lines 16-17 (attributes/classes: operational-k-rule)

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### 1017. rule at lines 18-19 (attributes/classes: equational-rule)

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
  // membership routes through the same k-cell fold as lists (list.k)
```

### 1018. rule at lines 20-20 (attributes/classes: operational-k-rule)

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### 1019. rule at lines 21-22 (attributes/classes: operational-k-rule)

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
  // t.index(v): first index of v (ValueError out of subset)
```

### 1020. rule at lines 23-23 (attributes/classes: equational-rule)

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### 1021. syntax at lines 24-24 (attributes/classes: function)

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### 1022. rule at lines 25-25 (attributes/classes: equational-rule)

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### 1023. rule at lines 26-27 (attributes/classes: equational-rule)

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

### 1024. rule at lines 28-30 (attributes/classes: equational-rule)

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

  // ==== target binding: bind a Name or a TupleExpr target to a value ========
```

### 1025. syntax at lines 31-31 (attributes/classes: none)

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

### 1026. rule at lines 32-34 (attributes/classes: operational-k-rule)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### 1027. rule at lines 35-41 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

### 1028. rule at lines 42-42 (attributes/classes: operational-k-rule)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### 1029. rule at lines 43-43 (attributes/classes: operational-k-rule)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### 1030. rule at lines 44-48 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]

  // ==== unpacking: a, b = <tuple|list> (RHS evaluated by strictness) ========
```

### 1031. syntax at lines 49-49 (attributes/classes: none)

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### 1032. rule at lines 50-50 (attributes/classes: operational-k-rule)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### 1033. rule at lines 51-51 (attributes/classes: operational-k-rule)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### 1034. rule at lines 52-54 (attributes/classes: priority(40), operational-k-rule)

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

### 1035. rule at lines 55-56 (attributes/classes: operational-k-rule)

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### 1036. rule at lines 57-57 (attributes/classes: operational-k-rule)

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### 1037. endmodule at lines 58-58 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/reference-semantics/semantics.k`

### 1038. requires at lines 34-34 (attributes/classes: none)

```k
requires "semantics/syntax.k"
```

### 1039. requires at lines 35-35 (attributes/classes: none)

```k
requires "semantics/core.k"
```

### 1040. requires at lines 36-36 (attributes/classes: none)

```k
requires "semantics/iter.k"
```

### 1041. requires at lines 37-37 (attributes/classes: none)

```k
requires "semantics/range.k"
```

### 1042. requires at lines 38-38 (attributes/classes: none)

```k
requires "semantics/operators.k"
```

### 1043. requires at lines 39-39 (attributes/classes: none)

```k
requires "semantics/int.k"
```

### 1044. requires at lines 40-40 (attributes/classes: none)

```k
requires "semantics/bool.k"
```

### 1045. requires at lines 41-41 (attributes/classes: none)

```k
requires "semantics/float.k"
```

### 1046. requires at lines 42-42 (attributes/classes: none)

```k
requires "semantics/str.k"
```

### 1047. requires at lines 43-43 (attributes/classes: none)

```k
requires "semantics/set.k"
```

### 1048. requires at lines 44-44 (attributes/classes: none)

```k
requires "semantics/list.k"
```

### 1049. requires at lines 45-45 (attributes/classes: none)

```k
requires "semantics/tuple.k"
```

### 1050. requires at lines 46-46 (attributes/classes: none)

```k
requires "semantics/subscript.k"
```

### 1051. requires at lines 47-47 (attributes/classes: none)

```k
requires "semantics/comprehension.k"
```

### 1052. requires at lines 48-48 (attributes/classes: none)

```k
requires "semantics/methods.k"
```

### 1053. requires at lines 49-49 (attributes/classes: none)

```k
requires "semantics/controls.k"
```

### 1054. requires at lines 50-50 (attributes/classes: none)

```k
requires "semantics/functions.k"
```

### 1055. requires at lines 51-51 (attributes/classes: none)

```k
requires "semantics/builtins.k"
```

### 1056. requires at lines 52-52 (attributes/classes: none)

```k
requires "semantics/call.k"
```

### 1057. requires at lines 53-53 (attributes/classes: none)

```k
requires "semantics/sort.k"
```

### 1058. requires at lines 54-54 (attributes/classes: none)

```k
requires "semantics/assert.k"
```

### 1059. requires at lines 55-55 (attributes/classes: none)

```k
requires "semantics/dict.k"
```

### 1060. requires at lines 56-57 (attributes/classes: none)

```k
requires "semantics/concrete.k"
```

### 1061. module at lines 58-58 (attributes/classes: none)

```k
module MPY
```

### 1062. imports at lines 59-59 (attributes/classes: none)

```k
  imports MPY-CORE
```

### 1063. imports at lines 60-60 (attributes/classes: none)

```k
  imports MPY-ITER
```

### 1064. imports at lines 61-61 (attributes/classes: none)

```k
  imports MPY-RANGE
```

### 1065. imports at lines 62-62 (attributes/classes: none)

```k
  imports MPY-OPERATORS
```

### 1066. imports at lines 63-63 (attributes/classes: none)

```k
  imports MPY-INT
```

### 1067. imports at lines 64-64 (attributes/classes: none)

```k
  imports MPY-BOOL
```

### 1068. imports at lines 65-65 (attributes/classes: none)

```k
  imports MPY-FLOAT
```

### 1069. imports at lines 66-66 (attributes/classes: none)

```k
  imports MPY-STR
```

### 1070. imports at lines 67-67 (attributes/classes: none)

```k
  imports MPY-SET
```

### 1071. imports at lines 68-68 (attributes/classes: none)

```k
  imports MPY-LIST
```

### 1072. imports at lines 69-69 (attributes/classes: none)

```k
  imports MPY-TUPLE
```

### 1073. imports at lines 70-70 (attributes/classes: none)

```k
  imports MPY-SUBSCRIPT
```

### 1074. imports at lines 71-71 (attributes/classes: none)

```k
  imports MPY-COMPREHENSION
```

### 1075. imports at lines 72-72 (attributes/classes: none)

```k
  imports MPY-METHODS
```

### 1076. imports at lines 73-73 (attributes/classes: none)

```k
  imports MPY-CONTROLS
```

### 1077. imports at lines 74-74 (attributes/classes: none)

```k
  imports MPY-FUNCTIONS
```

### 1078. imports at lines 75-75 (attributes/classes: none)

```k
  imports MPY-BUILTINS
```

### 1079. imports at lines 76-76 (attributes/classes: none)

```k
  imports MPY-CALL
```

### 1080. imports at lines 77-77 (attributes/classes: none)

```k
  imports MPY-SORT
```

### 1081. imports at lines 78-78 (attributes/classes: none)

```k
  imports MPY-ASSERT
```

### 1082. imports at lines 79-79 (attributes/classes: none)

```k
  imports MPY-DICT
```

### 1083. endmodule at lines 80-86 (attributes/classes: none)

```k
endmodule

// The krun (llvm) main module: MPY plus the concrete-only legs (keyed sort's
// real key calls, deep list equality). Verification builds import MPY and
// never see MPY-CONCRETE. The llvm kompile MUST use --main-module MPY-KRUN —
// with plain MPY the concrete legs are silently absent (this was live for a
// while: sorted-key stuck and comprehension asserted wrong under krun).
```

### 1084. module at lines 87-87 (attributes/classes: none)

```k
module MPY-KRUN
```

### 1085. imports at lines 88-88 (attributes/classes: none)

```k
  imports MPY
```

### 1086. imports at lines 89-89 (attributes/classes: none)

```k
  imports MPY-CONCRETE
```

### 1087. endmodule at lines 90-90 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/verification.k`

### 1088. requires at lines 1-2 (attributes/classes: none)

```k
requires "reference-semantics/semantics.k"
```

### 1089. module at lines 3-3 (attributes/classes: none)

```k
module CHECK-DICT-CASE-VERIFICATION
```

### 1090. imports at lines 4-7 (attributes/classes: none)

```k
  imports MPY

  // These constructors are the exact AST emitted in solution.mpy, factored
  // into named terms so that the reachability claims remain readable.
```

### 1091. syntax at lines 8-8 (attributes/classes: function, total)

```k
  syntax Stmts ::= checkDictLoopBody() [function, total]
```

### 1092. rule at lines 9-20 (attributes/classes: equational-rule)

```k
  rule checkDictLoopBody()
    => Assign(Name("has_key"), Bool(true))
       If(UnaryOp("not", Call(Name("isinstance"), (Name("key"), Name("str"), .Exprs))),
          Assign(Name("all_lower"), Bool(false))
          Assign(Name("all_upper"), Bool(false)),
          If(UnaryOp("not", Call(Attribute(Name("key"), "islower"), .Exprs)),
             Assign(Name("all_lower"), Bool(false)),
             .Stmts)
          If(UnaryOp("not", Call(Attribute(Name("key"), "isupper"), .Exprs)),
             Assign(Name("all_upper"), Bool(false)),
             .Stmts))
```

### 1093. syntax at lines 21-21 (attributes/classes: function, total)

```k
  syntax Expr ::= checkDictResultExpr() [function, total]
```

### 1094. rule at lines 22-27 (attributes/classes: equational-rule)

```k
  rule checkDictResultExpr()
    => BoolOp("and",
         (Name("has_key"),
          BoolOp("or", (Name("all_lower"), Name("all_upper"), .Exprs)),
          .Exprs))
```

### 1095. syntax at lines 28-28 (attributes/classes: function, total)

```k
  syntax Stmts ::= checkDictBody() [function, total]
```

### 1096. rule at lines 29-38 (attributes/classes: equational-rule)

```k
  rule checkDictBody()
    => Assign(Name("has_key"), Bool(false))
       Assign(Name("all_lower"), Bool(true))
       Assign(Name("all_upper"), Bool(true))
       Assign(Name("key"), NoneVal)
       For(Name("key"),
           Call(Attribute(Name("dict"), "keys"), .Exprs),
           checkDictLoopBody())
       Return(checkDictResultExpr())
```

### 1097. syntax at lines 39-39 (attributes/classes: function, total)

```k
  syntax Module ::= checkDictCaseModule() [function, total]
```

### 1098. rule at lines 40-45 (attributes/classes: equational-rule)

```k
  rule checkDictCaseModule()
    => Module(
         FuncDef("check_dict_case", Params("dict"), checkDictBody()))

  // Mathematical specification. A key counts as lower/upper exactly when it
  // is a string and Python's corresponding case predicate is true.
```

### 1099. syntax at lines 46-48 (attributes/classes: function, total)

```k
  syntax Bool ::= stringCaseKey(Val) [function, total]
                | lowerCaseKey(Val) [function, total]
                | upperCaseKey(Val) [function, total]
```

### 1100. rule at lines 49-49 (attributes/classes: equational-rule)

```k
  rule stringCaseKey(str(_:IntSeq)) => true
```

### 1101. rule at lines 50-50 (attributes/classes: owise, equational-rule)

```k
  rule stringCaseKey(_:Val) => false [owise]
```

### 1102. rule at lines 51-52 (attributes/classes: equational-rule)

```k
  rule lowerCaseKey(str(CS:IntSeq))
    => hasLower(CS) andBool notBool hasUpper(CS)
```

### 1103. rule at lines 53-53 (attributes/classes: owise, equational-rule)

```k
  rule lowerCaseKey(_:Val) => false [owise]
```

### 1104. rule at lines 54-55 (attributes/classes: equational-rule)

```k
  rule upperCaseKey(str(CS:IntSeq))
    => hasUpper(CS) andBool notBool hasLower(CS)
```

### 1105. rule at lines 56-61 (attributes/classes: owise, equational-rule)

```k
  rule upperCaseKey(_:Val) => false [owise]

  // Proof-only observation splitters. The reference functions intentionally
  // leave an abstract Val opaque; these guarded rules expose the two exhaustive
  // Boolean outcomes without choosing either one. On concrete values their
  // guards reduce to exactly the reference isinstance/string-method results.
```

### 1106. rule at lines 62-66 (attributes/classes: priority(30), operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("isinstance")),
                   (V:Val, typeV("str"), .Vals))
        => true ... </k>
       requires stringCaseKey(V)
       [priority(30)]
```

### 1107. rule at lines 67-72 (attributes/classes: priority(30), operational-k-rule)

```k
  rule <k> #applyK(toCall(builtinV("isinstance")),
                   (V:Val, typeV("str"), .Vals))
        => false ... </k>
       requires notBool stringCaseKey(V)
       [priority(30)]
```

### 1108. rule at lines 73-76 (attributes/classes: priority(30), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(V:Val, "islower")), .Vals)
        => true ... </k>
       requires stringCaseKey(V) andBool lowerCaseKey(V)
       [priority(30)]
```

### 1109. rule at lines 77-81 (attributes/classes: priority(30), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(V:Val, "islower")), .Vals)
        => false ... </k>
       requires stringCaseKey(V) andBool notBool lowerCaseKey(V)
       [priority(30)]
```

### 1110. rule at lines 82-85 (attributes/classes: priority(30), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(V:Val, "isupper")), .Vals)
        => true ... </k>
       requires stringCaseKey(V) andBool upperCaseKey(V)
       [priority(30)]
```

### 1111. rule at lines 86-90 (attributes/classes: priority(30), operational-k-rule)

```k
  rule <k> #applyK(toCall(boundMethodV(V:Val, "isupper")), .Vals)
        => false ... </k>
       requires stringCaseKey(V) andBool notBool upperCaseKey(V)
       [priority(30)]
```

### 1112. syntax at lines 91-92 (attributes/classes: function, total)

```k
  syntax Bool ::= allLowerKeys(ValSeq) [function, total]
                | allUpperKeys(ValSeq) [function, total]
```

### 1113. rule at lines 93-93 (attributes/classes: equational-rule)

```k
  rule allLowerKeys(.ValSeq) => true
```

### 1114. rule at lines 94-97 (attributes/classes: equational-rule)

```k
  rule allLowerKeys(vCons(K:Val, KS:ValSeq))
    => stringCaseKey(K)
       andBool lowerCaseKey(K)
       andBool allLowerKeys(KS)
```

### 1115. rule at lines 98-98 (attributes/classes: equational-rule)

```k
  rule allUpperKeys(.ValSeq) => true
```

### 1116. rule at lines 99-103 (attributes/classes: equational-rule)

```k
  rule allUpperKeys(vCons(K:Val, KS:ValSeq))
    => stringCaseKey(K)
       andBool upperCaseKey(K)
       andBool allUpperKeys(KS)
```

### 1117. syntax at lines 104-104 (attributes/classes: function, total)

```k
  syntax Bool ::= keySeenAfter(ValSeq, Bool) [function, total]
```

### 1118. rule at lines 105-105 (attributes/classes: equational-rule)

```k
  rule keySeenAfter(_:ValSeq, true) => true
```

### 1119. rule at lines 106-106 (attributes/classes: equational-rule)

```k
  rule keySeenAfter(.ValSeq, false) => false
```

### 1120. rule at lines 107-110 (attributes/classes: equational-rule)

```k
  rule keySeenAfter(vCons(_:Val, _:ValSeq), _:Bool) => true

  // The generalized postcondition used as the loop invariant: prior state is
  // conjoined with the classification of every remaining dictionary key.
```

### 1121. syntax at lines 111-112 (attributes/classes: function, total)

```k
  syntax Bool ::= checkDictCaseResult(ValSeq, Bool, Bool, Bool)
                  [function, total]
```

### 1122. rule at lines 113-116 (attributes/classes: equational-rule)

```k
  rule checkDictCaseResult(KS:ValSeq, SEEN:Bool, LOWER:Bool, UPPER:Bool)
    => keySeenAfter(KS, SEEN)
       andBool ((LOWER andBool allLowerKeys(KS))
                orBool (UPPER andBool allUpperKeys(KS)))
```

### 1123. endmodule at lines 117-117 (attributes/classes: none)

```k
endmodule
```

## `/tmp/audit-work/work/spec.k`

### 1124. requires at lines 1-2 (attributes/classes: none)

```k
requires "verification.k"
```

### 1125. module at lines 3-3 (attributes/classes: none)

```k
module CHECK-DICT-CASE-SPEC
```

### 1126. imports at lines 4-7 (attributes/classes: none)

```k
  imports CHECK-DICT-CASE-VERIFICATION

  // The entry point, parameter binding, flag initialization, d.keys(), and
  // For setup reach the generalized loop state over exactly the dict key list.
```

### 1127. claim at lines 8-46 (attributes/classes: none)

```k
  claim [entry-reaches-loop]:
    <k> #loadAll(checkDictCaseModule())
         ~> Call(Name("check_dict_case"),
                 (dictV(KS:ValSeq, VS:ValSeq), .Exprs))
        =>
         #loop(list(KS), Name("key"), checkDictLoopBody())
         ~> (Return(checkDictResultExpr()) .Stmts)
         ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "check_dict_case"
                 |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
               parent(-1))
      -1 |-> builtinsScope
      1  |-> scope(
               "dict"      |-> dictV(KS, VS)
               "has_key"   |-> false
               "all_lower" |-> true
               "all_upper" |-> true
               "key"       |-> noneV,
               parent(0))
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map => 0 |-> list(KS) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack>
      .List => ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Inductive loop theorem. OLDKEY generalizes the loop target binding, while
  // the exact local map makes this a decidable non-closure frame.
```

### 1128. claim at lines 47-83 (attributes/classes: none)

```k
  claim [loop-and-return]:
    <k> #loop(list(KS:ValSeq), Name("key"), checkDictLoopBody())
         ~> (Return(checkDictResultExpr()) .Stmts)
         ~> #endcall
        =>
         checkDictCaseResult(KS, SEEN, LOWER, UPPER)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0  |-> scope(
               "check_dict_case"
                 |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
               parent(-1))
      -1 |-> builtinsScope
      1  |-> scope(
               "has_key"   |-> SEEN:Bool
               "all_lower" |-> LOWER:Bool
               "all_upper" |-> UPPER:Bool
               "dict"      |-> DICT:Val
               "key"       |-> OLDKEY:Val,
               parent(0))
      =>
      0  |-> scope(
               "check_dict_case"
                 |-> closureVal(("dict", .ParamNames), checkDictBody(), 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXTHEAP:Int </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1)) => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
```

### 1129. endmodule at lines 84-84 (attributes/classes: none)

```k
endmodule
```


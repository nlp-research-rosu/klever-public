# Exhaustive K source inventory

Files: 26
Anchored entries: 1119
Counts: claim=2, configuration=1, context=5, endmodule=29, imports=90, module=29, requires=25, rule=706, syntax=232

## 1. /tmp/audit-work/reconstruction/reference-semantics/semantics/assert.k:3 — module; attributes: -

```k
module MPY-ASSERT
```

## 2. /tmp/audit-work/reconstruction/reference-semantics/semantics/assert.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 3. /tmp/audit-work/reconstruction/reference-semantics/semantics/assert.k:6 — rule; attributes: -

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

## 4. /tmp/audit-work/reconstruction/reference-semantics/semantics/assert.k:8 — rule; attributes: -

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

## 5. /tmp/audit-work/reconstruction/reference-semantics/semantics/assert.k:13 — rule; attributes: priority

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 6. /tmp/audit-work/reconstruction/reference-semantics/semantics/assert.k:16 — endmodule; attributes: -

```k
endmodule
```

## 7. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:5 — module; attributes: -

```k
module MPY-BOOL
```

## 8. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:6 — imports; attributes: -

```k
  imports MPY-CORE
```

## 9. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:8 — rule; attributes: -

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

## 10. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:10 — rule; attributes: -

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

## 11. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:11 — rule; attributes: -

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

## 12. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:16 — context; attributes: -

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

## 13. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:17 — rule; attributes: -

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

## 14. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:18 — rule; attributes: -

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

## 15. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:20 — rule; attributes: -

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

## 16. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:22 — rule; attributes: -

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

## 17. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:24 — rule; attributes: -

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

## 18. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:29 — rule; attributes: priority

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

## 19. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:31 — rule; attributes: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

## 20. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:35 — rule; attributes: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## 21. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:39 — rule; attributes: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

## 22. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:43 — rule; attributes: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## 23. /tmp/audit-work/reconstruction/reference-semantics/semantics/bool.k:47 — endmodule; attributes: -

```k
endmodule
```

## 24. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:3 — module; attributes: -

```k
module MPY-BUILTINS
```

## 25. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 26. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:5 — imports; attributes: -

```k
  imports MPY-STR
```

## 27. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:6 — imports; attributes: -

```k
  imports MPY-SET
```

## 28. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:7 — imports; attributes: -

```k
  imports MPY-ITER
```

## 29. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:8 — imports; attributes: -

```k
  imports MPY-RANGE
```

## 30. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:9 — imports; attributes: -

```k
  imports MPY-INT
```

## 31. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:10 — imports; attributes: -

```k
  imports MPY-METHODS
```

## 32. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:17 — syntax; attributes: function

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

## 33. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:20 — syntax; attributes: function

```k
  syntax Int ::= seqLen(Val) [function]
```

## 34. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:21 — rule; attributes: -

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

## 35. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:22 — rule; attributes: -

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

## 36. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:23 — rule; attributes: -

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

## 37. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:24 — rule; attributes: -

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

## 38. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:25 — rule; attributes: -

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

## 39. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:26 — rule; attributes: -

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

## 40. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:32 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

## 41. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:33 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

## 42. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:34 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

## 43. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:35 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

## 44. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:36 — syntax; attributes: function, total

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

## 45. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:37 — rule; attributes: -

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

## 46. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:38 — rule; attributes: -

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

## 47. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:41 — rule; attributes: -

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

## 48. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:44 — rule; attributes: -

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

## 49. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:47 — syntax; attributes: -

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

## 50. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:48 — rule; attributes: -

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

## 51. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:49 — rule; attributes: -

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

## 52. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:50 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

## 53. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:54 — syntax; attributes: function

```k
  syntax Int ::= intOf(Val) [function]
```

## 54. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:55 — rule; attributes: -

```k
  rule intOf(I:Int)  => I
```

## 55. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:56 — rule; attributes: -

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

## 56. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:59 — syntax; attributes: -

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

## 57. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:60 — rule; attributes: -

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

## 58. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:61 — rule; attributes: -

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

## 59. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:62 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

## 60. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:64 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

## 61. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:67 — syntax; attributes: -

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

## 62. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:68 — rule; attributes: -

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

## 63. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:69 — rule; attributes: -

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

## 64. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:70 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

## 65. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:72 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

## 66. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:76 — syntax; attributes: -

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

## 67. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:77 — rule; attributes: -

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

## 68. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:78 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

## 69. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:80 — rule; attributes: -

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

## 70. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:81 — rule; attributes: -

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

## 71. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:82 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

## 72. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:86 — syntax; attributes: -

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

## 73. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:87 — rule; attributes: -

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

## 74. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:88 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

## 75. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:90 — rule; attributes: -

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

## 76. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:91 — rule; attributes: -

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

## 77. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:92 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

## 78. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:97 — syntax; attributes: function

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

## 79. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:98 — rule; attributes: -

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

## 80. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:99 — rule; attributes: -

```k
  rule maxVals(M:Int, .Vals)           => M
```

## 81. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:100 — rule; attributes: -

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

## 82. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:102 — syntax; attributes: function

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

## 83. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:103 — rule; attributes: -

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

## 84. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:104 — rule; attributes: -

```k
  rule minVals(M:Int, .Vals)           => M
```

## 85. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:105 — rule; attributes: -

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

## 86. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:108 — rule; attributes: -

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

## 87. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:111 — rule; attributes: -

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

## 88. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:114 — syntax; attributes: function, total

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

## 89. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:115 — rule; attributes: -

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

## 90. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:116 — rule; attributes: -

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

## 91. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:117 — syntax; attributes: function, total

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

## 92. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:118 — rule; attributes: -

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

## 93. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:119 — rule; attributes: -

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

## 94. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:124 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

## 95. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:126 — syntax; attributes: function, total

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

## 96. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:127 — rule; attributes: -

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

## 97. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:128 — rule; attributes: -

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

## 98. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:132 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

## 99. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:134 — syntax; attributes: function, total

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

## 100. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:135 — rule; attributes: -

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

## 101. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:136 — rule; attributes: -

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

## 102. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:137 — rule; attributes: -

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

## 103. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:140 — rule; attributes: -

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

## 104. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:143 — rule; attributes: -

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

## 105. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:144 — rule; attributes: -

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

## 106. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:148 — rule; attributes: -

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

## 107. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:149 — rule; attributes: -

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

## 108. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:152 — rule; attributes: -

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

## 109. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:156 — rule; attributes: -

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

## 110. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:158 — syntax; attributes: function, total

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

## 111. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:159 — rule; attributes: -

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

## 112. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:160 — rule; attributes: -

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

## 113. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:163 — rule; attributes: -

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

## 114. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:164 — rule; attributes: -

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

## 115. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:167 — rule; attributes: -

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

## 116. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:169 — rule; attributes: -

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

## 117. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:170 — rule; attributes: -

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

## 118. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:171 — rule; attributes: -

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

## 119. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:173 — rule; attributes: -

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

## 120. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:174 — rule; attributes: -

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

## 121. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:177 — rule; attributes: -

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

## 122. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:178 — rule; attributes: -

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

## 123. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:179 — rule; attributes: -

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

## 124. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:187 — rule; attributes: -

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

## 125. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:188 — syntax; attributes: function

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

## 126. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:189 — rule; attributes: -

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

## 127. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:192 — syntax; attributes: -

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

## 128. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:194 — syntax; attributes: function, total

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

## 129. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:195 — rule; attributes: -

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

## 130. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:196 — syntax; attributes: function, total

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

## 131. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:197 — rule; attributes: -

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

## 132. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:198 — rule; attributes: owise

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

## 133. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:199 — syntax; attributes: function, total

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

## 134. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:200 — rule; attributes: -

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

## 135. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:201 — rule; attributes: owise

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

## 136. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:203 — syntax; attributes: function, total

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

## 137. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:204 — rule; attributes: -

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

## 138. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:205 — rule; attributes: -

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

## 139. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:206 — rule; attributes: -

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

## 140. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:207 — rule; attributes: -

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

## 141. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:208 — rule; attributes: -

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

## 142. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:209 — rule; attributes: -

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

## 143. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:210 — rule; attributes: -

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

## 144. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:211 — rule; attributes: -

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

## 145. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:212 — rule; attributes: -

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

## 146. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:214 — syntax; attributes: function, total

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

## 147. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:216 — rule; attributes: -

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

## 148. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:217 — rule; attributes: -

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

## 149. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:218 — rule; attributes: -

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

## 150. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:219 — rule; attributes: -

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

## 151. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:221 — rule; attributes: -

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

## 152. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:223 — rule; attributes: owise

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

## 153. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:225 — syntax; attributes: -

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

## 154. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:226 — syntax; attributes: function, total

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

## 155. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:227 — rule; attributes: -

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

## 156. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:228 — rule; attributes: owise

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

## 157. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:230 — syntax; attributes: function, total

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

## 158. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:231 — rule; attributes: -

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

## 159. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:232 — rule; attributes: -

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

## 160. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:233 — rule; attributes: -

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

## 161. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:234 — rule; attributes: -

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

## 162. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:235 — rule; attributes: -

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

## 163. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:236 — rule; attributes: owise

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

## 164. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:238 — syntax; attributes: function, total

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

## 165. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:239 — rule; attributes: -

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

## 166. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:240 — rule; attributes: -

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

## 167. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:241 — rule; attributes: -

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

## 168. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:243 — rule; attributes: owise

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

## 169. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:244 — syntax; attributes: function, total

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

## 170. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:245 — rule; attributes: -

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

## 171. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:246 — rule; attributes: -

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

## 172. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:247 — syntax; attributes: function, total

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

## 173. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:248 — rule; attributes: -

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

## 174. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:250 — syntax; attributes: function, total

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

## 175. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:251 — rule; attributes: -

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

## 176. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:252 — rule; attributes: -

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

## 177. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:253 — rule; attributes: -

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

## 178. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:254 — rule; attributes: -

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

## 179. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:255 — syntax; attributes: function, total

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

## 180. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:256 — rule; attributes: -

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

## 181. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:257 — rule; attributes: -

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

## 182. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:260 — rule; attributes: -

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

## 183. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:263 — rule; attributes: owise

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

## 184. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:265 — syntax; attributes: function, total

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

## 185. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:266 — rule; attributes: -

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

## 186. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:267 — rule; attributes: -

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

## 187. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:268 — rule; attributes: owise

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

## 188. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:269 — syntax; attributes: function, total

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

## 189. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:270 — rule; attributes: -

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

## 190. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:271 — rule; attributes: -

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

## 191. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:272 — syntax; attributes: function, total

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

## 192. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:273 — rule; attributes: -

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

## 193. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:274 — rule; attributes: -

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

## 194. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:279 — syntax; attributes: -

```k
  syntax KItem ::= "#md5"
```

## 195. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:280 — rule; attributes: priority

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

## 196. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:282 — rule; attributes: -

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

## 197. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:283 — syntax; attributes: -

```k
  syntax Val ::= md5Obj(IntSeq)
```

## 198. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:284 — rule; attributes: -

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

## 199. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:285 — syntax; attributes: function, total, symbol

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

## 200. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:291 — rule; attributes: -

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

## 201. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:292 — rule; attributes: -

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

## 202. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:293 — syntax; attributes: function

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

## 203. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:294 — rule; attributes: -

```k
  rule isIntV(_:Int)         => true
```

## 204. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:295 — rule; attributes: owise

```k
  rule isIntV(_:Val)         => false [owise]
```

## 205. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:296 — rule; attributes: -

```k
  rule isStrV(str(_:IntSeq)) => true
```

## 206. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:297 — rule; attributes: owise

```k
  rule isStrV(_:Val)         => false [owise]
```

## 207. /tmp/audit-work/reconstruction/reference-semantics/semantics/builtins.k:298 — endmodule; attributes: -

```k
endmodule
```

## 208. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:10 — module; attributes: -

```k
module MPY-CALL
```

## 209. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:11 — imports; attributes: -

```k
  imports MPY-METHODS
```

## 210. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:12 — imports; attributes: -

```k
  imports MPY-BUILTINS
```

## 211. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:13 — imports; attributes: -

```k
  imports MPY-FUNCTIONS
```

## 212. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:16 — rule; attributes: -

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

## 213. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:19 — syntax; attributes: -

```k
  syntax KItem ::= #callee(Exprs)
```

## 214. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:20 — rule; attributes: owise

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

## 215. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:21 — rule; attributes: -

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

## 216. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:24 — rule; attributes: -

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

## 217. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:26 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

## 218. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:27 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

## 219. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:28 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

## 220. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:29 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

## 221. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:30 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

## 222. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:31 — rule; attributes: owise

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

## 223. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:32 — rule; attributes: -

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

## 224. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:38 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 225. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:42 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

## 226. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:47 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 227. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:52 — syntax; attributes: function, total

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

## 228. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:53 — rule; attributes: -

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

## 229. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:56 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

## 230. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:63 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

## 231. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:69 — rule; attributes: -

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

## 232. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:80 — rule; attributes: -

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

## 233. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:87 — syntax; attributes: -

```k
  syntax KItem ::= #allocCells(ParamNames)
```

## 234. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:88 — rule; attributes: -

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

## 235. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:89 — rule; attributes: -

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

## 236. /tmp/audit-work/reconstruction/reference-semantics/semantics/call.k:95 — endmodule; attributes: -

```k
endmodule
```

## 237. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:3 — module; attributes: -

```k
module MPY-COMPREHENSION
```

## 238. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 239. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:5 — imports; attributes: -

```k
  imports MPY-OPERATORS
```

## 240. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:6 — imports; attributes: -

```k
  imports MPY-LIST
```

## 241. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:7 — imports; attributes: -

```k
  imports MPY-CONTROLS
```

## 242. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:8 — imports; attributes: -

```k
  imports MPY-FUNCTIONS
```

## 243. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:11 — rule; attributes: -

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

## 244. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:12 — rule; attributes: -

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

## 245. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:14 — syntax; attributes: macro

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

## 246. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:15 — rule; attributes: -

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

## 247. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:18 — syntax; attributes: macro

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

## 248. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:19 — rule; attributes: -

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

## 249. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:21 — rule; attributes: -

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

## 250. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:24 — syntax; attributes: macro

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

## 251. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:25 — rule; attributes: -

```k
  rule compGuard(.Exprs)             => Bool(true)
```

## 252. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:26 — rule; attributes: -

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## 253. /tmp/audit-work/reconstruction/reference-semantics/semantics/comprehension.k:27 — endmodule; attributes: -

```k
endmodule
```

## 254. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:8 — module; attributes: -

```k
module MPY-CONCRETE
```

## 255. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:9 — imports; attributes: -

```k
  imports MPY
```

## 256. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:13 — rule; attributes: -

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

## 257. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:16 — rule; attributes: -

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

## 258. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:25 — syntax; attributes: -

```k
  syntax Val ::= kvP(Val, Val)
```

## 259. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:26 — syntax; attributes: -

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

## 260. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:28 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

## 261. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:31 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

## 262. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:34 — rule; attributes: -

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

## 263. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:36 — rule; attributes: -

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

## 264. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:38 — rule; attributes: -

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

## 265. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:42 — syntax; attributes: function

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

## 266. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:43 — rule; attributes: -

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

## 267. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:44 — rule; attributes: -

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

## 268. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:47 — rule; attributes: -

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

## 269. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:51 — syntax; attributes: function

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

## 270. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:52 — rule; attributes: -

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

## 271. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:53 — rule; attributes: -

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

## 272. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:54 — rule; attributes: -

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

## 273. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:56 — syntax; attributes: function, total

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

## 274. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:57 — rule; attributes: -

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

## 275. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:58 — rule; attributes: -

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

## 276. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:59 — rule; attributes: owise

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## 277. /tmp/audit-work/reconstruction/reference-semantics/semantics/concrete.k:60 — endmodule; attributes: -

```k
endmodule
```

## 278. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:3 — module; attributes: -

```k
module MPY-CONTROLS
```

## 279. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 280. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:5 — imports; attributes: -

```k
  imports MPY-TUPLE
```

## 281. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:6 — imports; attributes: -

```k
  imports MPY-ITER
```

## 282. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:9 — rule; attributes: -

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

## 283. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:12 — rule; attributes: priority

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

## 284. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:20 — rule; attributes: -

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

## 285. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:27 — rule; attributes: priority

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

## 286. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:35 — rule; attributes: -

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

## 287. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:36 — rule; attributes: owise

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

## 288. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:37 — syntax; attributes: -

```k
  syntax KItem ::= #bindImports(ParamNames)
```

## 289. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:38 — rule; attributes: -

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

## 290. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:39 — rule; attributes: -

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

## 291. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:43 — rule; attributes: -

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

## 292. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:48 — rule; attributes: -

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

## 293. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:51 — syntax; attributes: -

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

## 294. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:52 — rule; attributes: -

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

## 295. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:53 — rule; attributes: -

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

## 296. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:54 — rule; attributes: -

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

## 297. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:57 — rule; attributes: -

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

## 298. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:59 — rule; attributes: -

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

## 299. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:65 — syntax; attributes: -

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

## 300. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:69 — rule; attributes: -

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

## 301. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:71 — rule; attributes: -

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

## 302. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:72 — rule; attributes: -

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

## 303. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:73 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

## 304. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:77 — rule; attributes: -

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

## 305. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:78 — rule; attributes: -

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

## 306. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:79 — rule; attributes: -

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

## 307. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:81 — rule; attributes: -

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

## 308. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:85 — rule; attributes: -

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

## 309. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:86 — rule; attributes: -

```k
  rule <k> Continue => #cont ... </k>
```

## 310. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:87 — rule; attributes: -

```k
  rule <k> Break => #brk ... </k>
```

## 311. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:88 — rule; attributes: -

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

## 312. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:89 — rule; attributes: owise

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

## 313. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:90 — rule; attributes: -

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

## 314. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:91 — rule; attributes: owise

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

## 315. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:95 — rule; attributes: priority

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 316. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:98 — rule; attributes: priority

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 317. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:101 — rule; attributes: priority

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 318. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:106 — rule; attributes: priority

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 319. /tmp/audit-work/reconstruction/reference-semantics/semantics/controls.k:109 — endmodule; attributes: -

```k
endmodule
```

## 320. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:3 — module; attributes: -

```k
module MPY-CORE
```

## 321. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:4 — imports; attributes: -

```k
  imports MPY-SYNTAX
```

## 322. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:5 — imports; attributes: -

```k
  imports INT
```

## 323. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:6 — imports; attributes: -

```k
  imports BOOL
```

## 324. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:7 — imports; attributes: -

```k
  imports STRING
```

## 325. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:8 — imports; attributes: -

```k
  imports MAP
```

## 326. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:9 — imports; attributes: -

```k
  imports LIST
```

## 327. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:10 — imports; attributes: -

```k
  imports K-EQUAL
```

## 328. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:13 — syntax; attributes: -

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

## 329. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:14 — syntax; attributes: -

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

## 330. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:15 — syntax; attributes: -

```k
  syntax Str    ::= str(IntSeq)
```

## 331. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:18 — syntax; attributes: -

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

## 332. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:25 — syntax; attributes: function

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

## 333. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:36 — syntax; attributes: -

```k
  syntax Parent   ::= "root" | parent(Int)
```

## 334. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:37 — syntax; attributes: -

```k
  syntax Scope    ::= scope(Map, Parent)
```

## 335. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:38 — syntax; attributes: -

```k
  syntax KResult  ::= Val
```

## 336. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:39 — syntax; attributes: -

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

## 337. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:40 — syntax; attributes: -

```k
  syntax Vals     ::= List{Val, ","}
```

## 338. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:41 — syntax; attributes: -

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

## 339. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:42 — syntax; attributes: -

```k
  syntax RetState ::= "noRet" | retV(Val)
```

## 340. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:49 — configuration; attributes: -

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

## 341. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:68 — syntax; attributes: function, total

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

## 342. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:69 — rule; attributes: -

```k
  rule isRefV(ref(_:Int)) => true
```

## 343. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:70 — rule; attributes: owise

```k
  rule isRefV(_:Val)      => false [owise]
```

## 344. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:75 — syntax; attributes: -

```k
  syntax HeapVal ::= cellV(Val)
```

## 345. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:76 — syntax; attributes: function, total

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

## 346. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:77 — rule; attributes: -

```k
  rule isCellRef(cellRef(_:Int)) => true
```

## 347. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:78 — rule; attributes: owise

```k
  rule isCellRef(_:Val)          => false [owise]
```

## 348. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:85 — rule; attributes: priority

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

## 349. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:95 — syntax; attributes: -

```k
  syntax Val ::= kwV(String, Val)
```

## 350. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:96 — syntax; attributes: -

```k
  syntax KItem ::= #kwTag(String)
```

## 351. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:97 — rule; attributes: -

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

## 352. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:98 — rule; attributes: -

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

## 353. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:100 — syntax; attributes: function, total

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

## 354. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:101 — rule; attributes: -

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

## 355. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:102 — rule; attributes: owise

```k
  rule isKwV(_:Val)                => false [owise]
```

## 356. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:106 — syntax; attributes: -

```k
  syntax Val ::= cellsMark(ParamNames)
```

## 357. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:107 — syntax; attributes: function

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

## 358. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:108 — rule; attributes: -

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

## 359. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:109 — syntax; attributes: function, total

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

## 360. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:110 — rule; attributes: -

```k
  rule pnMember(_:String, .ParamNames) => false
```

## 361. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:111 — rule; attributes: -

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

## 362. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:113 — syntax; attributes: -

```k
  syntax KItem ::= #cellW(Val, Val)
```

## 363. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:114 — rule; attributes: -

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

## 364. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:117 — syntax; attributes: -

```k
  syntax KItem ::= #alloc(Val)
```

## 365. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:118 — rule; attributes: -

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

## 366. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:124 — syntax; attributes: -

```k
  syntax KItem ::= #loadAll(Module)
```

## 367. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:125 — rule; attributes: -

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

## 368. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:126 — rule; attributes: -

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

## 369. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:127 — rule; attributes: -

```k
  rule <k> .Stmts => .K ... </k>
```

## 370. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:130 — syntax; attributes: -

```k
  syntax KItem ::= #look(String, Int)
```

## 371. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:131 — rule; attributes: -

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

## 372. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:132 — rule; attributes: -

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

## 373. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:145 — rule; attributes: priority

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

## 374. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:152 — rule; attributes: -

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

## 375. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:157 — syntax; attributes: function, total

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

## 376. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:158 — rule; attributes: -

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

## 377. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:185 — syntax; attributes: -

```k
  syntax ApplyK ::= toCall(Val)
```

## 378. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:186 — syntax; attributes: -

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

## 379. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:189 — rule; attributes: -

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

## 380. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:190 — rule; attributes: -

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

## 381. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:191 — rule; attributes: -

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

## 382. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:194 — rule; attributes: -

```k
  rule <k> Int(I:Int)   => I ... </k>
```

## 383. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:195 — rule; attributes: -

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

## 384. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:196 — rule; attributes: -

```k
  rule <k> NoneVal      => noneV ... </k>
```

## 385. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:199 — syntax; attributes: function

```k
  syntax Bool ::= truthy(Val) [function]
```

## 386. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:200 — rule; attributes: -

```k
  rule truthy(B:Bool)          => B
```

## 387. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:201 — rule; attributes: -

```k
  rule truthy(noneV)           => false
```

## 388. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:202 — rule; attributes: -

```k
  rule truthy(I:Int)           => I =/=Int 0
```

## 389. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:203 — rule; attributes: -

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

## 390. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:204 — rule; attributes: -

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

## 391. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:205 — rule; attributes: -

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

## 392. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:208 — syntax; attributes: function

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

## 393. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:209 — syntax; attributes: function

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

## 394. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:210 — syntax; attributes: function

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

## 395. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:213 — syntax; attributes: function, total

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

## 396. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:214 — rule; attributes: -

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

## 397. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:215 — rule; attributes: -

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

## 398. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:217 — syntax; attributes: function, total

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

## 399. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:218 — rule; attributes: -

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

## 400. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:219 — rule; attributes: -

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

## 401. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:223 — syntax; attributes: function, total

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

## 402. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:224 — rule; attributes: -

```k
  rule vsLen(.ValSeq)                => 0
```

## 403. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:225 — rule; attributes: -

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

## 404. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:227 — syntax; attributes: function, total

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

## 405. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:228 — rule; attributes: -

```k
  rule isLen(.IntSeq)                => 0
```

## 406. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:229 — rule; attributes: -

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

## 407. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:233 — syntax; attributes: function, total

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

## 408. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:234 — rule; attributes: -

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

## 409. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:235 — rule; attributes: -

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

## 410. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:236 — rule; attributes: -

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

## 411. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:238 — rule; attributes: -

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

## 412. /tmp/audit-work/reconstruction/reference-semantics/semantics/core.k:240 — endmodule; attributes: -

```k
endmodule
```

## 413. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:13 — module; attributes: -

```k
module MPY-DICT
```

## 414. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:14 — imports; attributes: -

```k
  imports MPY-CORE
```

## 415. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:15 — imports; attributes: -

```k
  imports MPY-ITER
```

## 416. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:16 — imports; attributes: -

```k
  imports MPY-METHODS
```

## 417. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:17 — imports; attributes: -

```k
  imports MPY-LIST
```

## 418. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:20 — syntax; attributes: -

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

## 419. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:23 — syntax; attributes: -

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

## 420. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:26 — rule; attributes: -

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

## 421. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:27 — rule; attributes: -

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

## 422. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:28 — rule; attributes: -

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

## 423. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:30 — rule; attributes: -

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

## 424. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:32 — rule; attributes: -

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

## 425. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:37 — syntax; attributes: function, total

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

## 426. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:38 — rule; attributes: -

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

## 427. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:39 — rule; attributes: -

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

## 428. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:40 — rule; attributes: -

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

## 429. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:43 — syntax; attributes: function, total

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

## 430. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:44 — rule; attributes: -

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

## 431. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:45 — rule; attributes: -

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

## 432. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:49 — syntax; attributes: function, total

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

## 433. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:50 — rule; attributes: -

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

## 434. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:52 — rule; attributes: -

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

## 435. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:54 — rule; attributes: owise

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

## 436. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:58 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

## 437. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:63 — rule; attributes: -

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

## 438. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:64 — syntax; attributes: function

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

## 439. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:65 — rule; attributes: priority

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

## 440. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:70 — syntax; attributes: function

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

## 441. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:71 — rule; attributes: -

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

## 442. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:76 — syntax; attributes: -

```k
  syntax KItem ::= #dsetK(String, Val)
```

## 443. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:77 — rule; attributes: -

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

## 444. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:78 — rule; attributes: -

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

## 445. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:82 — rule; attributes: -

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

## 446. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:86 — syntax; attributes: -

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

## 447. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:87 — rule; attributes: -

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

## 448. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:90 — syntax; attributes: function, total

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

## 449. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:91 — rule; attributes: -

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

## 450. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:92 — rule; attributes: -

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

## 451. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:95 — rule; attributes: -

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

## 452. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:97 — syntax; attributes: function

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

## 453. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:98 — rule; attributes: -

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

## 454. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:99 — rule; attributes: -

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

## 455. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:101 — syntax; attributes: function

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

## 456. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:102 — rule; attributes: -

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

## 457. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:103 — rule; attributes: -

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## 458. /tmp/audit-work/reconstruction/reference-semantics/semantics/dict.k:104 — endmodule; attributes: -

```k
endmodule
```

## 459. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:14 — module; attributes: -

```k
module MPY-FLOAT
```

## 460. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:15 — imports; attributes: -

```k
  imports MPY-OPERATORS
```

## 461. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:16 — imports; attributes: -

```k
  imports MPY-BUILTINS
```

## 462. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:17 — imports; attributes: -

```k
  imports FLOAT
```

## 463. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:20 — syntax; attributes: -

```k
  syntax Val ::= Float
```

## 464. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:21 — rule; attributes: -

```k
  rule <k> Float(F:Float) => F ... </k>
```

## 465. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:24 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

## 466. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:25 — rule; attributes: concrete

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

## 467. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:27 — rule; attributes: -

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

## 468. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:30 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

## 469. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:31 — rule; attributes: concrete

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

## 470. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:32 — rule; attributes: -

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

## 471. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:37 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

## 472. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:38 — rule; attributes: concrete

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

## 473. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:39 — rule; attributes: -

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

## 474. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:43 — rule; attributes: -

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

## 475. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:44 — rule; attributes: -

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

## 476. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:50 — syntax; attributes: function, total, symbol

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

## 477. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:51 — rule; attributes: concrete

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

## 478. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:52 — rule; attributes: -

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

## 479. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:54 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

## 480. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:55 — rule; attributes: concrete

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

## 481. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:56 — rule; attributes: -

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

## 482. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:61 — rule; attributes: -

```k
  rule <k> Import(_:String) => .K ... </k>
```

## 483. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:65 — syntax; attributes: -

```k
  syntax KItem ::= "#mathCeil"
```

## 484. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:66 — rule; attributes: priority

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

## 485. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:67 — rule; attributes: -

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

## 486. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:70 — syntax; attributes: -

```k
  syntax KItem ::= "#mathFloor"
```

## 487. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:71 — rule; attributes: priority

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

## 488. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:72 — rule; attributes: -

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

## 489. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:73 — syntax; attributes: function, total, symbol

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

## 490. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:74 — rule; attributes: concrete

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

## 491. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:75 — rule; attributes: concrete

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

## 492. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:78 — rule; attributes: -

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

## 493. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:79 — rule; attributes: -

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

## 494. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:82 — syntax; attributes: -

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

## 495. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:83 — rule; attributes: priority

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

## 496. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:84 — rule; attributes: -

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

## 497. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:85 — rule; attributes: -

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

## 498. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:86 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

## 499. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:87 — rule; attributes: concrete

```k
  rule toF(F:Float) => F        [concrete]
```

## 500. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:88 — rule; attributes: concrete

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

## 501. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:93 — syntax; attributes: function, total, symbol

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

## 502. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:94 — rule; attributes: concrete

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

## 503. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:95 — rule; attributes: concrete

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

## 504. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:99 — rule; attributes: -

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

## 505. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:103 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

## 506. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:104 — rule; attributes: concrete

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

## 507. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:105 — rule; attributes: -

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

## 508. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:107 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

## 509. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:108 — rule; attributes: concrete

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

## 510. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:109 — rule; attributes: -

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

## 511. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:111 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

## 512. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:112 — rule; attributes: concrete

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

## 513. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:113 — rule; attributes: -

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

## 514. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:115 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

## 515. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:116 — rule; attributes: concrete

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

## 516. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:117 — rule; attributes: -

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

## 517. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:119 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

## 518. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:120 — rule; attributes: concrete

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

## 519. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:121 — rule; attributes: -

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

## 520. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:125 — syntax; attributes: function, total, symbol

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

## 521. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:126 — rule; attributes: concrete

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

## 522. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:127 — rule; attributes: -

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

## 523. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:128 — rule; attributes: -

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

## 524. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:129 — rule; attributes: -

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

## 525. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:132 — rule; attributes: -

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

## 526. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:133 — rule; attributes: -

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

## 527. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:134 — rule; attributes: -

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

## 528. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:135 — rule; attributes: -

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

## 529. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:136 — rule; attributes: -

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

## 530. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:137 — rule; attributes: -

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

## 531. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:138 — rule; attributes: -

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

## 532. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:139 — rule; attributes: -

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

## 533. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:142 — syntax; attributes: function, total, symbol

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

## 534. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:143 — rule; attributes: concrete

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

## 535. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:144 — rule; attributes: -

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

## 536. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:145 — rule; attributes: -

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

## 537. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:146 — rule; attributes: -

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

## 538. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:147 — rule; attributes: -

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

## 539. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:148 — rule; attributes: -

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

## 540. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:149 — rule; attributes: -

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

## 541. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:150 — rule; attributes: -

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

## 542. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:151 — rule; attributes: -

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

## 543. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:154 — rule; attributes: -

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

## 544. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:155 — rule; attributes: -

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

## 545. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:160 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

## 546. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:161 — rule; attributes: concrete

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

## 547. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:162 — rule; attributes: concrete

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

## 548. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:165 — syntax; attributes: function

```k
  syntax Int ::= headIS(IntSeq) [function]
```

## 549. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:166 — rule; attributes: -

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

## 550. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:167 — syntax; attributes: function, total

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

## 551. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:168 — rule; attributes: -

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

## 552. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:169 — rule; attributes: -

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

## 553. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:170 — rule; attributes: -

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

## 554. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:171 — rule; attributes: -

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

## 555. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:173 — syntax; attributes: function, total

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

## 556. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:174 — rule; attributes: -

```k
  rule fracPart(.IntSeq) => 0
```

## 557. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:175 — rule; attributes: -

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

## 558. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:176 — rule; attributes: -

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

## 559. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:177 — rule; attributes: -

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

## 560. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:178 — rule; attributes: -

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

## 561. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:179 — syntax; attributes: function, total

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

## 562. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:180 — rule; attributes: -

```k
  rule fracScale(.IntSeq) => 1
```

## 563. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:181 — rule; attributes: -

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

## 564. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:182 — rule; attributes: -

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

## 565. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:183 — rule; attributes: -

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

## 566. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:184 — rule; attributes: -

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

## 567. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:185 — rule; attributes: -

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

## 568. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:186 — rule; attributes: -

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

## 569. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:187 — rule; attributes: -

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

## 570. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:190 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

## 571. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:191 — rule; attributes: concrete

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

## 572. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:192 — rule; attributes: -

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

## 573. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:195 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

## 574. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:196 — rule; attributes: concrete

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

## 575. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:197 — rule; attributes: -

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

## 576. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:198 — rule; attributes: -

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

## 577. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:199 — rule; attributes: -

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

## 578. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:200 — rule; attributes: -

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

## 579. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:201 — rule; attributes: -

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

## 580. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:202 — rule; attributes: -

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

## 581. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:203 — rule; attributes: -

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

## 582. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:204 — rule; attributes: -

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

## 583. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:205 — rule; attributes: -

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

## 584. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:206 — rule; attributes: -

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

## 585. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:209 — syntax; attributes: function, total, symbol

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

## 586. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:210 — rule; attributes: concrete

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

## 587. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:211 — rule; attributes: -

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

## 588. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:213 — rule; attributes: -

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

## 589. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:214 — rule; attributes: -

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

## 590. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:217 — syntax; attributes: function, total, symbol

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

## 591. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:218 — rule; attributes: concrete

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

## 592. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:223 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

## 593. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:224 — rule; attributes: concrete

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

## 594. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:227 — rule; attributes: -

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

## 595. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:228 — rule; attributes: -

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

## 596. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:230 — syntax; attributes: function, total, symbol

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

## 597. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:231 — rule; attributes: concrete

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

## 598. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:232 — syntax; attributes: -

```k
  syntax KItem ::= "#mathSqrt"
```

## 599. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:233 — rule; attributes: priority

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

## 600. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:234 — rule; attributes: -

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

## 601. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:235 — rule; attributes: -

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

## 602. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:243 — syntax; attributes: -

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

## 603. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:244 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

## 604. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:245 — rule; attributes: -

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

## 605. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:246 — rule; attributes: -

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

## 606. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:247 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## 607. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:250 — syntax; attributes: -

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

## 608. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:251 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

## 609. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:252 — rule; attributes: -

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

## 610. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:253 — rule; attributes: -

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

## 611. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:254 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## 612. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:261 — syntax; attributes: -

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

## 613. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:262 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

## 614. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:265 — rule; attributes: -

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

## 615. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:266 — rule; attributes: -

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

## 616. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:267 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## 617. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:270 — rule; attributes: -

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

## 618. /tmp/audit-work/reconstruction/reference-semantics/semantics/float.k:273 — endmodule; attributes: -

```k
endmodule
```

## 619. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:3 — module; attributes: -

```k
module MPY-FUNCTIONS
```

## 620. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 621. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:8 — syntax; attributes: -

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

## 622. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:14 — rule; attributes: -

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

## 623. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:18 — syntax; attributes: -

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

## 624. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:19 — rule; attributes: -

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

## 625. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:27 — syntax; attributes: -

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

## 626. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:31 — syntax; attributes: -

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

## 627. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:33 — rule; attributes: -

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

## 628. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:36 — rule; attributes: -

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

## 629. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:42 — rule; attributes: -

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

## 630. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:47 — rule; attributes: -

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

## 631. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:50 — rule; attributes: -

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

## 632. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:53 — rule; attributes: -

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

## 633. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:59 — rule; attributes: -

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

## 634. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:63 — rule; attributes: -

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

## 635. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:64 — rule; attributes: -

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

## 636. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:68 — rule; attributes: priority

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

## 637. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:78 — rule; attributes: -

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

## 638. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:80 — rule; attributes: -

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

## 639. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:85 — rule; attributes: -

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## 640. /tmp/audit-work/reconstruction/reference-semantics/semantics/functions.k:91 — endmodule; attributes: -

```k
endmodule
```

## 641. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:4 — module; attributes: -

```k
module MPY-INT
```

## 642. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:5 — imports; attributes: -

```k
  imports MPY-CORE
```

## 643. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:7 — rule; attributes: -

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

## 644. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:9 — rule; attributes: -

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

## 645. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:11 — rule; attributes: -

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

## 646. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:12 — rule; attributes: -

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

## 647. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:13 — rule; attributes: -

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

## 648. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:14 — rule; attributes: -

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

## 649. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:15 — rule; attributes: -

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

## 650. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:16 — rule; attributes: -

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

## 651. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:17 — rule; attributes: -

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

## 652. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:19 — syntax; attributes: function

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

## 653. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:20 — rule; attributes: -

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

## 654. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:22 — rule; attributes: -

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

## 655. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:23 — rule; attributes: -

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

## 656. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:24 — rule; attributes: -

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

## 657. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:25 — rule; attributes: -

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

## 658. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:26 — rule; attributes: -

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

## 659. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:27 — rule; attributes: -

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## 660. /tmp/audit-work/reconstruction/reference-semantics/semantics/int.k:28 — endmodule; attributes: -

```k
endmodule
```

## 661. /tmp/audit-work/reconstruction/reference-semantics/semantics/iter.k:6 — module; attributes: -

```k
module MPY-ITER
```

## 662. /tmp/audit-work/reconstruction/reference-semantics/semantics/iter.k:7 — imports; attributes: -

```k
  imports MPY-CORE
```

## 663. /tmp/audit-work/reconstruction/reference-semantics/semantics/iter.k:8 — syntax; attributes: -

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## 664. /tmp/audit-work/reconstruction/reference-semantics/semantics/iter.k:9 — endmodule; attributes: -

```k
endmodule
```

## 665. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:3 — module; attributes: -

```k
module MPY-LIST
```

## 666. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 667. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:5 — imports; attributes: -

```k
  imports MPY-ITER
```

## 668. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:6 — imports; attributes: -

```k
  imports MPY-OPERATORS
```

## 669. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:9 — rule; attributes: -

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

## 670. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:10 — rule; attributes: -

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

## 671. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:13 — syntax; attributes: -

```k
  syntax ApplyK ::= "toList"
```

## 672. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:14 — rule; attributes: -

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

## 673. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:15 — rule; attributes: -

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

## 674. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:18 — syntax; attributes: function, total

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

## 675. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:19 — rule; attributes: -

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

## 676. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:20 — rule; attributes: -

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

## 677. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:24 — rule; attributes: priority

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

## 678. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:27 — rule; attributes: -

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

## 679. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:28 — rule; attributes: -

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

## 680. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:33 — syntax; attributes: function, total

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

## 681. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:34 — rule; attributes: -

```k
  rule hasRefVS(.ValSeq)                => false
```

## 682. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:35 — rule; attributes: -

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

## 683. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:37 — syntax; attributes: function

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

## 684. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:39 — rule; attributes: -

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

## 685. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:40 — rule; attributes: -

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

## 686. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:41 — rule; attributes: -

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

## 687. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:42 — rule; attributes: -

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

## 688. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:45 — rule; attributes: -

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

## 689. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:47 — rule; attributes: -

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

## 690. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:49 — rule; attributes: -

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

## 691. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:50 — rule; attributes: owise

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

## 692. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:53 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

## 693. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:58 — syntax; attributes: -

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

## 694. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:59 — rule; attributes: -

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

## 695. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:60 — rule; attributes: -

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

## 696. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:61 — rule; attributes: -

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

## 697. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:62 — rule; attributes: -

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

## 698. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:63 — rule; attributes: -

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

## 699. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:65 — rule; attributes: -

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

## 700. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:67 — rule; attributes: -

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## 701. /tmp/audit-work/reconstruction/reference-semantics/semantics/list.k:68 — endmodule; attributes: -

```k
endmodule
```

## 702. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:3 — module; attributes: -

```k
module MPY-METHODS
```

## 703. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 704. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:5 — imports; attributes: -

```k
  imports K-EQUAL
```

## 705. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:6 — imports; attributes: -

```k
  imports MPY-STR
```

## 706. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:7 — imports; attributes: -

```k
  imports MPY-LIST
```

## 707. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:10 — syntax; attributes: function

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

## 708. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:13 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

## 709. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:14 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

## 710. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:15 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

## 711. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:16 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

## 712. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:19 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

## 713. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:20 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

## 714. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:21 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

## 715. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:26 — rule; attributes: -

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

## 716. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:27 — syntax; attributes: function, total

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

## 717. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:28 — rule; attributes: -

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

## 718. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:29 — rule; attributes: -

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

## 719. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:30 — rule; attributes: -

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

## 720. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:34 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

## 721. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:35 — syntax; attributes: function

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

## 722. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:36 — rule; attributes: -

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

## 723. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:37 — rule; attributes: -

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

## 724. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:39 — rule; attributes: -

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

## 725. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:41 — syntax; attributes: function, total

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

## 726. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:42 — rule; attributes: -

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

## 727. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:43 — rule; attributes: owise

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

## 728. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:44 — rule; attributes: -

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

## 729. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:47 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

## 730. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:48 — syntax; attributes: function, total

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

## 731. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:49 — rule; attributes: -

```k
  rule trimWS(.IntSeq) => .IntSeq
```

## 732. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:50 — rule; attributes: -

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

## 733. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:51 — rule; attributes: -

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

## 734. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:52 — syntax; attributes: function, total

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

## 735. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:53 — rule; attributes: -

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

## 736. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:54 — rule; attributes: -

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

## 737. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:55 — rule; attributes: -

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

## 738. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:58 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

## 739. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:61 — rule; attributes: -

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

## 740. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:64 — rule; attributes: -

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

## 741. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:65 — syntax; attributes: function, total

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

## 742. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:66 — rule; attributes: -

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

## 743. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:67 — rule; attributes: -

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

## 744. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:68 — rule; attributes: -

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

## 745. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:72 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

## 746. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:75 — syntax; attributes: function

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

## 747. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:76 — rule; attributes: -

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

## 748. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:77 — rule; attributes: -

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

## 749. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:79 — rule; attributes: -

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

## 750. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:82 — syntax; attributes: function

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

## 751. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:83 — rule; attributes: -

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

## 752. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:84 — rule; attributes: -

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

## 753. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:85 — syntax; attributes: function, total

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

## 754. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:86 — rule; attributes: -

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

## 755. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:89 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

## 756. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:94 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

## 757. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:97 — syntax; attributes: function

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

## 758. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:98 — rule; attributes: -

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

## 759. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:99 — rule; attributes: -

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

## 760. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:101 — rule; attributes: -

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

## 761. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:104 — rule; attributes: -

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

## 762. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:106 — syntax; attributes: function, total

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

## 763. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:107 — rule; attributes: -

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

## 764. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:108 — rule; attributes: -

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

## 765. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:109 — rule; attributes: -

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

## 766. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:112 — syntax; attributes: function, total

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

## 767. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:113 — rule; attributes: -

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

## 768. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:115 — syntax; attributes: function, total

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

## 769. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:116 — rule; attributes: -

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

## 770. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:118 — syntax; attributes: function, total

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

## 771. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:119 — rule; attributes: -

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

## 772. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:121 — syntax; attributes: function, total

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

## 773. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:122 — rule; attributes: -

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

## 774. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:124 — syntax; attributes: function, total

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

## 775. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:125 — rule; attributes: -

```k
  rule hasUpper(.IntSeq) => false
```

## 776. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:126 — rule; attributes: -

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

## 777. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:128 — syntax; attributes: function, total

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

## 778. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:129 — rule; attributes: -

```k
  rule hasLower(.IntSeq) => false
```

## 779. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:130 — rule; attributes: -

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

## 780. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:132 — syntax; attributes: function, total

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

## 781. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:133 — rule; attributes: -

```k
  rule allAlpha(.IntSeq) => true
```

## 782. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:134 — rule; attributes: -

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

## 783. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:136 — syntax; attributes: function, total

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

## 784. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:137 — rule; attributes: -

```k
  rule allDigit(.IntSeq) => true
```

## 785. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:138 — rule; attributes: -

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

## 786. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:140 — syntax; attributes: function, total

```k
  syntax Int ::= lowerC(Int) [function, total]
```

## 787. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:142 — rule; attributes: -

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

## 788. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:143 — rule; attributes: owise

```k
  rule lowerC(C:Int) => C         [owise]
```

## 789. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:145 — syntax; attributes: function, total

```k
  syntax Int ::= upperC(Int) [function, total]
```

## 790. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:146 — rule; attributes: -

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

## 791. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:147 — rule; attributes: owise

```k
  rule upperC(C:Int) => C         [owise]
```

## 792. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:149 — syntax; attributes: function, total

```k
  syntax Int ::= swapC(Int) [function, total]
```

## 793. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:150 — rule; attributes: -

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

## 794. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:151 — rule; attributes: -

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

## 795. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:152 — rule; attributes: owise

```k
  rule swapC(C:Int) => C         [owise]
```

## 796. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:154 — syntax; attributes: function, total

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

## 797. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:155 — rule; attributes: -

```k
  rule mapLower(.IntSeq) => .IntSeq
```

## 798. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:156 — rule; attributes: -

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

## 799. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:158 — syntax; attributes: function, total

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

## 800. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:159 — rule; attributes: -

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

## 801. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:160 — rule; attributes: -

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

## 802. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:162 — syntax; attributes: function, total

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

## 803. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:163 — rule; attributes: -

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

## 804. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:164 — rule; attributes: -

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

## 805. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:166 — syntax; attributes: function, total

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

## 806. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:167 — rule; attributes: -

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

## 807. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:168 — rule; attributes: -

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## 808. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:169 — rule; attributes: -

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## 809. /tmp/audit-work/reconstruction/reference-semantics/semantics/methods.k:170 — endmodule; attributes: -

```k
endmodule
```

## 810. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:6 — module; attributes: -

```k
module MPY-OPERATORS
```

## 811. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:7 — imports; attributes: -

```k
  imports MPY-CORE
```

## 812. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:8 — imports; attributes: -

```k
  imports MPY-ITER
```

## 813. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:10 — rule; attributes: -

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

## 814. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:12 — rule; attributes: -

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

## 815. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:15 — context; attributes: -

```k
  context Compare(HOLE, _)
```

## 816. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:16 — context; attributes: -

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

## 817. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:17 — rule; attributes: owise

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

## 818. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:19 — rule; attributes: -

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

## 819. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:20 — rule; attributes: -

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

## 820. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:25 — rule; attributes: priority

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 821. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:28 — rule; attributes: priority

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

## 822. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:34 — rule; attributes: priority

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

## 823. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:38 — rule; attributes: priority

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

## 824. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:44 — rule; attributes: priority

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 825. /tmp/audit-work/reconstruction/reference-semantics/semantics/operators.k:47 — endmodule; attributes: -

```k
endmodule
```

## 826. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:5 — module; attributes: -

```k
module MPY-RANGE
```

## 827. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:6 — imports; attributes: -

```k
  imports MPY-CORE
```

## 828. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:7 — imports; attributes: -

```k
  imports MPY-ITER
```

## 829. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:9 — syntax; attributes: function, total

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

## 830. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:10 — rule; attributes: -

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

## 831. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:12 — syntax; attributes: function

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

## 832. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:13 — rule; attributes: -

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

## 833. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:15 — rule; attributes: -

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

## 834. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:17 — rule; attributes: -

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

## 835. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:20 — rule; attributes: -

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

## 836. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:23 — rule; attributes: -

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

## 837. /tmp/audit-work/reconstruction/reference-semantics/semantics/range.k:25 — endmodule; attributes: -

```k
endmodule
```

## 838. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:3 — module; attributes: -

```k
module MPY-SET
```

## 839. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 840. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:8 — syntax; attributes: -

```k
  syntax Val ::= setV(IntSeq)
```

## 841. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:11 — syntax; attributes: function, total

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

## 842. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:12 — rule; attributes: -

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

## 843. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:13 — rule; attributes: -

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

## 844. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:16 — syntax; attributes: function, total

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

## 845. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:18 — rule; attributes: -

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

## 846. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:19 — rule; attributes: -

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

## 847. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:20 — rule; attributes: -

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

## 848. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:22 — rule; attributes: -

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

## 849. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:25 — syntax; attributes: function, total

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

## 850. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:26 — rule; attributes: -

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

## 851. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:27 — rule; attributes: -

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

## 852. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:31 — syntax; attributes: function, total

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

## 853. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:32 — rule; attributes: -

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

## 854. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:33 — rule; attributes: -

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

## 855. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:35 — syntax; attributes: function, total

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

## 856. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:36 — rule; attributes: -

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

## 857. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:39 — rule; attributes: -

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## 858. /tmp/audit-work/reconstruction/reference-semantics/semantics/set.k:40 — endmodule; attributes: -

```k
endmodule
```

## 859. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:10 — module; attributes: -

```k
module MPY-SORT
```

## 860. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:11 — imports; attributes: -

```k
  imports MPY-BUILTINS
```

## 861. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:12 — imports; attributes: -

```k
  imports MPY-SUBSCRIPT
```

## 862. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:18 — syntax; attributes: function, total, symbol

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

## 863. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:19 — syntax; attributes: function

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

## 864. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:20 — rule; attributes: concrete

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

## 865. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:21 — rule; attributes: concrete

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

## 866. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:22 — rule; attributes: concrete

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

## 867. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:23 — rule; attributes: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

## 868. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:24 — rule; attributes: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

## 869. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:26 — syntax; attributes: function

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

## 870. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:27 — rule; attributes: concrete

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

## 871. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:28 — rule; attributes: concrete

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

## 872. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:29 — rule; attributes: concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

## 873. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:31 — rule; attributes: concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

## 874. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:36 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

## 875. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:40 — rule; attributes: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

## 876. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:49 — syntax; attributes: function, total, symbol

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

## 877. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:51 — syntax; attributes: function, total

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

## 878. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:53 — rule; attributes: -

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

## 879. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:54 — rule; attributes: -

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

## 880. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:55 — rule; attributes: -

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

## 881. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:57 — syntax; attributes: function, total

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

## 882. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:58 — rule; attributes: -

```k
  rule condRev(S:ValSeq, false) => S
```

## 883. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:59 — rule; attributes: -

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

## 884. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:61 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

## 885. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:63 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

## 886. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:65 — rule; attributes: -

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

## 887. /tmp/audit-work/reconstruction/reference-semantics/semantics/sort.k:72 — endmodule; attributes: -

```k
endmodule
```

## 888. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:3 — module; attributes: -

```k
module MPY-STR
```

## 889. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 890. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:5 — imports; attributes: -

```k
  imports MPY-ITER
```

## 891. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:8 — rule; attributes: -

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

## 892. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:9 — rule; attributes: -

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

## 893. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:13 — syntax; attributes: function

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

## 894. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:14 — rule; attributes: -

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

## 895. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:15 — rule; attributes: -

```k
  rule strToCodes("") => .IntSeq
```

## 896. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:16 — rule; attributes: -

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

## 897. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:20 — syntax; attributes: function, total

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

## 898. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:21 — rule; attributes: -

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

## 899. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:22 — rule; attributes: -

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

## 900. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:24 — rule; attributes: -

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

## 901. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:25 — rule; attributes: -

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

## 902. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:26 — rule; attributes: -

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

## 903. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:29 — rule; attributes: -

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

## 904. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:30 — rule; attributes: -

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

## 905. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:32 — syntax; attributes: function, total

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

## 906. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:33 — rule; attributes: -

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

## 907. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:34 — rule; attributes: -

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## 908. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:35 — rule; attributes: -

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

## 909. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:37 — syntax; attributes: function, total

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

## 910. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:38 — rule; attributes: -

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

## 911. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:39 — rule; attributes: -

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

## 912. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:40 — rule; attributes: -

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

## 913. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:48 — syntax; attributes: function, total

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

## 914. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:49 — rule; attributes: -

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

## 915. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:50 — rule; attributes: -

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

## 916. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:51 — rule; attributes: -

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## 917. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:52 — rule; attributes: -

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

## 918. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:53 — rule; attributes: -

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

## 919. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:54 — rule; attributes: -

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

## 920. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:56 — rule; attributes: -

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

## 921. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:57 — rule; attributes: -

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

## 922. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:58 — rule; attributes: -

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

## 923. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:59 — rule; attributes: -

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## 924. /tmp/audit-work/reconstruction/reference-semantics/semantics/str.k:60 — endmodule; attributes: -

```k
endmodule
```

## 925. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:3 — module; attributes: -

```k
module MPY-SUBSCRIPT
```

## 926. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 927. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:11 — syntax; attributes: function, total

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

## 928. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:12 — rule; attributes: -

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

## 929. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:13 — rule; attributes: -

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

## 930. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:16 — syntax; attributes: function

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

## 931. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:17 — rule; attributes: -

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

## 932. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:18 — rule; attributes: -

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

## 933. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:21 — syntax; attributes: function, total

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

## 934. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:22 — rule; attributes: -

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

## 935. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:23 — rule; attributes: -

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

## 936. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:27 — context; attributes: -

```k
  context Subscript(HOLE, _)
```

## 937. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:28 — context; attributes: -

```k
  context Subscript(_:Val, HOLE:Expr)
```

## 938. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:31 — rule; attributes: priority

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 939. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:35 — rule; attributes: -

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

## 940. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:37 — syntax; attributes: function

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

## 941. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:38 — rule; attributes: -

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

## 942. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:39 — rule; attributes: -

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

## 943. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:40 — rule; attributes: -

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

## 944. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:44 — syntax; attributes: -

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

## 945. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:49 — syntax; attributes: -

```k
  syntax OptInt ::= "noB" | someB(Int)
```

## 946. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:50 — rule; attributes: -

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

## 947. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:51 — rule; attributes: -

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

## 948. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:52 — rule; attributes: -

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

## 949. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:54 — rule; attributes: -

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

## 950. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:55 — rule; attributes: -

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

## 951. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:56 — rule; attributes: -

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

## 952. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:58 — rule; attributes: priority

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

## 953. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:61 — rule; attributes: -

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

## 954. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:63 — syntax; attributes: function

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

## 955. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:64 — rule; attributes: -

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

## 956. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:66 — rule; attributes: -

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

## 957. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:68 — rule; attributes: -

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

## 958. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:72 — syntax; attributes: function, total

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

## 959. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:73 — rule; attributes: -

```k
  rule slStep(noB)          => 1
```

## 960. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:74 — rule; attributes: -

```k
  rule slStep(someB(S:Int)) => S
```

## 961. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:76 — syntax; attributes: function

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

## 962. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:77 — rule; attributes: -

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

## 963. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:79 — rule; attributes: -

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

## 964. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:81 — rule; attributes: -

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

## 965. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:83 — syntax; attributes: function

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

## 966. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:84 — rule; attributes: -

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

## 967. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:86 — rule; attributes: -

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

## 968. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:88 — rule; attributes: -

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

## 969. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:90 — syntax; attributes: function, total

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

## 970. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:91 — rule; attributes: -

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

## 971. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:93 — rule; attributes: -

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

## 972. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:96 — syntax; attributes: function, total

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

## 973. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:97 — rule; attributes: -

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

## 974. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:99 — rule; attributes: -

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

## 975. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:102 — syntax; attributes: function, total

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

## 976. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:103 — rule; attributes: -

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

## 977. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:105 — rule; attributes: -

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

## 978. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:109 — syntax; attributes: function

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

## 979. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:110 — rule; attributes: -

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

## 980. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:113 — rule; attributes: -

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## 981. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:116 — syntax; attributes: function

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

## 982. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:117 — rule; attributes: -

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

## 983. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:120 — rule; attributes: -

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## 984. /tmp/audit-work/reconstruction/reference-semantics/semantics/subscript.k:122 — endmodule; attributes: -

```k
endmodule
```

## 985. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:3 — module; attributes: -

```k
module MPY-SYNTAX
```

## 986. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:4 — imports; attributes: -

```k
  imports INT-SYNTAX
```

## 987. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:5 — imports; attributes: -

```k
  imports FLOAT-SYNTAX
```

## 988. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:6 — imports; attributes: -

```k
  imports BOOL-SYNTAX
```

## 989. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:7 — imports; attributes: -

```k
  imports STRING-SYNTAX
```

## 990. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:9 — syntax; attributes: macro, strict, seqstrict

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

## 991. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:32 — syntax; attributes: -

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

## 992. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:33 — syntax; attributes: -

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

## 993. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:34 — syntax; attributes: -

```k
  syntax Entries  ::= List{Entry, ","}
```

## 994. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:35 — syntax; attributes: -

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

## 995. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:36 — syntax; attributes: -

```k
  syntax CompFors ::= List{CompFor, ""}
```

## 996. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:37 — syntax; attributes: -

```k
  syntax Exprs    ::= List{Expr, ","}
```

## 997. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:38 — syntax; attributes: -

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

## 998. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:39 — syntax; attributes: -

```k
  syntax Bound    ::= Expr | "NoBound"
```

## 999. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:41 — syntax; attributes: strict

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

## 1000. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:56 — syntax; attributes: -

```k
  syntax Stmts      ::= List{Stmt, ""}
```

## 1001. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:57 — syntax; attributes: -

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

## 1002. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:58 — syntax; attributes: -

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

## 1003. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:59 — syntax; attributes: -

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

## 1004. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:60 — syntax; attributes: -

```k
  syntax ParamNames ::= List{String, ","}
```

## 1005. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:61 — syntax; attributes: -

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## 1006. /tmp/audit-work/reconstruction/reference-semantics/semantics/syntax.k:62 — endmodule; attributes: -

```k
endmodule
```

## 1007. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:3 — module; attributes: -

```k
module MPY-TUPLE
```

## 1008. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:4 — imports; attributes: -

```k
  imports MPY-CORE
```

## 1009. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:5 — imports; attributes: -

```k
  imports MPY-ITER
```

## 1010. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:6 — imports; attributes: -

```k
  imports MPY-LIST
```

## 1011. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:7 — imports; attributes: -

```k
  imports MPY-METHODS
```

## 1012. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:10 — rule; attributes: -

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

## 1013. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:11 — rule; attributes: -

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

## 1014. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:14 — syntax; attributes: -

```k
  syntax ApplyK ::= "toTuple"
```

## 1015. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:15 — rule; attributes: -

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

## 1016. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:16 — rule; attributes: -

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

## 1017. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:18 — rule; attributes: -

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

## 1018. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:20 — rule; attributes: -

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

## 1019. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:21 — rule; attributes: -

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

## 1020. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:23 — rule; attributes: -

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

## 1021. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:24 — syntax; attributes: function

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

## 1022. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:25 — rule; attributes: -

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

## 1023. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:26 — rule; attributes: -

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

## 1024. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:28 — rule; attributes: -

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

## 1025. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:31 — syntax; attributes: -

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

## 1026. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:32 — rule; attributes: -

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

## 1027. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:35 — rule; attributes: priority

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

## 1028. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:42 — rule; attributes: -

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

## 1029. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:43 — rule; attributes: -

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

## 1030. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:44 — rule; attributes: priority

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 1031. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:49 — syntax; attributes: -

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

## 1032. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:50 — rule; attributes: -

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

## 1033. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:51 — rule; attributes: -

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

## 1034. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:52 — rule; attributes: priority

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 1035. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:55 — rule; attributes: -

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

## 1036. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:57 — rule; attributes: -

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## 1037. /tmp/audit-work/reconstruction/reference-semantics/semantics/tuple.k:58 — endmodule; attributes: -

```k
endmodule
```

## 1038. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:34 — requires; attributes: -

```k
requires "semantics/syntax.k"
```

## 1039. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:35 — requires; attributes: -

```k
requires "semantics/core.k"
```

## 1040. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:36 — requires; attributes: -

```k
requires "semantics/iter.k"
```

## 1041. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:37 — requires; attributes: -

```k
requires "semantics/range.k"
```

## 1042. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:38 — requires; attributes: -

```k
requires "semantics/operators.k"
```

## 1043. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:39 — requires; attributes: -

```k
requires "semantics/int.k"
```

## 1044. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:40 — requires; attributes: -

```k
requires "semantics/bool.k"
```

## 1045. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:41 — requires; attributes: -

```k
requires "semantics/float.k"
```

## 1046. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:42 — requires; attributes: -

```k
requires "semantics/str.k"
```

## 1047. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:43 — requires; attributes: -

```k
requires "semantics/set.k"
```

## 1048. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:44 — requires; attributes: -

```k
requires "semantics/list.k"
```

## 1049. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:45 — requires; attributes: -

```k
requires "semantics/tuple.k"
```

## 1050. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:46 — requires; attributes: -

```k
requires "semantics/subscript.k"
```

## 1051. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:47 — requires; attributes: -

```k
requires "semantics/comprehension.k"
```

## 1052. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:48 — requires; attributes: -

```k
requires "semantics/methods.k"
```

## 1053. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:49 — requires; attributes: -

```k
requires "semantics/controls.k"
```

## 1054. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:50 — requires; attributes: -

```k
requires "semantics/functions.k"
```

## 1055. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:51 — requires; attributes: -

```k
requires "semantics/builtins.k"
```

## 1056. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:52 — requires; attributes: -

```k
requires "semantics/call.k"
```

## 1057. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:53 — requires; attributes: -

```k
requires "semantics/sort.k"
```

## 1058. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:54 — requires; attributes: -

```k
requires "semantics/assert.k"
```

## 1059. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:55 — requires; attributes: -

```k
requires "semantics/dict.k"
```

## 1060. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:56 — requires; attributes: concrete

```k
requires "semantics/concrete.k"
```

## 1061. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:58 — module; attributes: -

```k
module MPY
```

## 1062. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:59 — imports; attributes: -

```k
  imports MPY-CORE
```

## 1063. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:60 — imports; attributes: -

```k
  imports MPY-ITER
```

## 1064. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:61 — imports; attributes: -

```k
  imports MPY-RANGE
```

## 1065. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:62 — imports; attributes: -

```k
  imports MPY-OPERATORS
```

## 1066. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:63 — imports; attributes: -

```k
  imports MPY-INT
```

## 1067. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:64 — imports; attributes: -

```k
  imports MPY-BOOL
```

## 1068. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:65 — imports; attributes: -

```k
  imports MPY-FLOAT
```

## 1069. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:66 — imports; attributes: -

```k
  imports MPY-STR
```

## 1070. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:67 — imports; attributes: -

```k
  imports MPY-SET
```

## 1071. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:68 — imports; attributes: -

```k
  imports MPY-LIST
```

## 1072. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:69 — imports; attributes: -

```k
  imports MPY-TUPLE
```

## 1073. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:70 — imports; attributes: -

```k
  imports MPY-SUBSCRIPT
```

## 1074. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:71 — imports; attributes: -

```k
  imports MPY-COMPREHENSION
```

## 1075. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:72 — imports; attributes: -

```k
  imports MPY-METHODS
```

## 1076. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:73 — imports; attributes: -

```k
  imports MPY-CONTROLS
```

## 1077. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:74 — imports; attributes: -

```k
  imports MPY-FUNCTIONS
```

## 1078. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:75 — imports; attributes: -

```k
  imports MPY-BUILTINS
```

## 1079. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:76 — imports; attributes: -

```k
  imports MPY-CALL
```

## 1080. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:77 — imports; attributes: -

```k
  imports MPY-SORT
```

## 1081. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:78 — imports; attributes: -

```k
  imports MPY-ASSERT
```

## 1082. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:79 — imports; attributes: -

```k
  imports MPY-DICT
```

## 1083. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:80 — endmodule; attributes: -

```k
endmodule
```

## 1084. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:87 — module; attributes: -

```k
module MPY-KRUN
```

## 1085. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:88 — imports; attributes: -

```k
  imports MPY
```

## 1086. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:89 — imports; attributes: -

```k
  imports MPY-CONCRETE
```

## 1087. /tmp/audit-work/reconstruction/reference-semantics/semantics.k:90 — endmodule; attributes: -

```k
endmodule
```

## 1088. /tmp/audit-work/reconstruction/spec.k:1 — requires; attributes: -

```k
requires "verification.k"
```

## 1089. /tmp/audit-work/reconstruction/spec.k:3 — module; attributes: -

```k
module X-OR-Y-LOOP-SPEC
```

## 1090. /tmp/audit-work/reconstruction/spec.k:4 — imports; attributes: -

```k
  imports X-OR-Y-VERIFICATION
```

## 1091. /tmp/audit-work/reconstruction/spec.k:9 — claim; attributes: -

```k
  claim
    <k>
      #loop(rangeObj(D:Int, N:Int, 1), Name("divisor"), xOrYLoopBody)
      ~> (Return(Name("x")) .Stmts)
      ~> #endcall
      => #pop
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> BS:Scope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "divisor" |-> (OLD:Int => scanLast(N, D, OLD))
        "n" |-> N:Int
        "x" |-> X:Val
        "y" |-> Y:Val,
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet => retV(primeSelect(N, D, X:Val, Y:Val)) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2
      andBool D >=Int 2
    [label(loop_correct)]
```

## 1092. /tmp/audit-work/reconstruction/spec.k:37 — endmodule; attributes: -

```k
endmodule
```

## 1093. /tmp/audit-work/reconstruction/spec.k:39 — module; attributes: -

```k
module X-OR-Y-MAIN-SPEC
```

## 1094. /tmp/audit-work/reconstruction/spec.k:40 — imports; attributes: -

```k
  imports X-OR-Y-SUMMARY
```

## 1095. /tmp/audit-work/reconstruction/spec.k:44 — claim; attributes: -

```k
  claim
    <k> #xOrY(N:Int, X:Val, Y:Val) => primeSelect(N, 2, X, Y) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(main_correct)]
```

## 1096. /tmp/audit-work/reconstruction/spec.k:59 — endmodule; attributes: -

```k
endmodule
```

## 1097. /tmp/audit-work/reconstruction/verification.k:1 — requires; attributes: -

```k
requires "reference-semantics/semantics.k"
```

## 1098. /tmp/audit-work/reconstruction/verification.k:3 — module; attributes: -

```k
module X-OR-Y-VERIFICATION
```

## 1099. /tmp/audit-work/reconstruction/verification.k:4 — imports; attributes: -

```k
  imports MPY
```

## 1100. /tmp/audit-work/reconstruction/verification.k:8 — syntax; attributes: macro

```k
  syntax Stmts ::= "xOrYLoopBody" [macro]
```

## 1101. /tmp/audit-work/reconstruction/verification.k:9 — rule; attributes: -

```k
  rule xOrYLoopBody
    => If(
         Compare(BinOp("%", Name("n"), Name("divisor")),
                 CmpOp("==", Int(0))),
         Return(Name("y")),
         .Stmts)
```

## 1102. /tmp/audit-work/reconstruction/verification.k:16 — syntax; attributes: macro

```k
  syntax Stmts ::= "xOrYBody" [macro]
```

## 1103. /tmp/audit-work/reconstruction/verification.k:17 — rule; attributes: -

```k
  rule xOrYBody
    => If(Compare(Name("n"), CmpOp("<", Int(2))),
          Return(Name("y")),
          .Stmts)
       For(Name("divisor"), Call(Name("range"), (Int(2), Name("n"))),
           xOrYLoopBody)
       Return(Name("x"))
```

## 1104. /tmp/audit-work/reconstruction/verification.k:26 — syntax; attributes: macro

```k
  syntax KItem ::= "#xOrY" "(" Int "," Val "," Val ")" [macro]
```

## 1105. /tmp/audit-work/reconstruction/verification.k:27 — rule; attributes: -

```k
  rule #xOrY(N:Int, X:Val, Y:Val)
    => Call(closureVal(("n", "x", "y"), xOrYBody, 0), (N, X, Y))
```

## 1106. /tmp/audit-work/reconstruction/verification.k:33 — syntax; attributes: function

```k
  syntax Val ::= primeSelect(Int, Int, Val, Val) [function]
```

## 1107. /tmp/audit-work/reconstruction/verification.k:35 — rule; attributes: -

```k
  rule primeSelect(N:Int, D:Int, X:Val, Y:Val) => Y
    requires D >=Int 2 andBool N <Int 2
```

## 1108. /tmp/audit-work/reconstruction/verification.k:38 — rule; attributes: -

```k
  rule primeSelect(N:Int, D:Int, X:Val, Y:Val) => X
    requires D >=Int 2 andBool N >=Int 2 andBool D >=Int N
```

## 1109. /tmp/audit-work/reconstruction/verification.k:41 — rule; attributes: -

```k
  rule primeSelect(N:Int, D:Int, X:Val, Y:Val) => Y
    requires D >=Int 2 andBool N >=Int 2 andBool D <Int N
      andBool pyMod(N, D) ==Int 0
```

## 1110. /tmp/audit-work/reconstruction/verification.k:45 — rule; attributes: -

```k
  rule primeSelect(N:Int, D:Int, X:Val, Y:Val)
    => primeSelect(N, D +Int 1, X, Y)
    requires D >=Int 2 andBool N >=Int 2 andBool D <Int N
      andBool pyMod(N, D) =/=Int 0
```

## 1111. /tmp/audit-work/reconstruction/verification.k:52 — syntax; attributes: function

```k
  syntax Int ::= scanLast(Int, Int, Int) [function]
```

## 1112. /tmp/audit-work/reconstruction/verification.k:54 — rule; attributes: -

```k
  rule scanLast(N:Int, D:Int, OLD:Int) => OLD
    requires N >=Int 2 andBool D >=Int 2 andBool D >=Int N
```

## 1113. /tmp/audit-work/reconstruction/verification.k:57 — rule; attributes: -

```k
  rule scanLast(N:Int, D:Int, OLD:Int) => D
    requires N >=Int 2 andBool D >=Int 2 andBool D <Int N
      andBool pyMod(N, D) ==Int 0
```

## 1114. /tmp/audit-work/reconstruction/verification.k:61 — rule; attributes: -

```k
  rule scanLast(N:Int, D:Int, OLD:Int)
    => scanLast(N, D +Int 1, D)
    requires N >=Int 2 andBool D >=Int 2 andBool D <Int N
      andBool pyMod(N, D) =/=Int 0
```

## 1115. /tmp/audit-work/reconstruction/verification.k:65 — endmodule; attributes: -

```k
endmodule
```

## 1116. /tmp/audit-work/reconstruction/verification.k:70 — module; attributes: -

```k
module X-OR-Y-SUMMARY
```

## 1117. /tmp/audit-work/reconstruction/verification.k:71 — imports; attributes: -

```k
  imports X-OR-Y-VERIFICATION
```

## 1118. /tmp/audit-work/reconstruction/verification.k:73 — rule; attributes: priority

```k
  rule
    <k>
      #loop(rangeObj(D:Int, N:Int, 1), Name("divisor"), xOrYLoopBody)
      ~> (Return(Name("x")) .Stmts)
      ~> #endcall
      => #pop
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> BS:Scope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "divisor" |-> (OLD:Int => scanLast(N, D, OLD))
        "n" |-> N:Int
        "x" |-> X:Val
        "y" |-> Y:Val,
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet => retV(primeSelect(N, D, X:Val, Y:Val)) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2
      andBool D >=Int 2
    [priority(40)]
```

## 1119. /tmp/audit-work/reconstruction/verification.k:101 — endmodule; attributes: -

```k
endmodule
```


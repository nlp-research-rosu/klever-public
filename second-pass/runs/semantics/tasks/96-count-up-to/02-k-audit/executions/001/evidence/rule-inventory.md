# Exhaustive K declaration and rule inventory

Source root: `/tmp/audit-work/96-count-up-to/source`

Files: 26
Inventoried blocks: 944
Block counts: {'claim': 4, 'configuration': 1, 'context': 5, 'rule': 704, 'syntax': 230}
Attribute-bearing block counts: {'concrete': 35, 'function': 148, 'macro': 4, 'no-evaluators': 25, 'owise': 26, 'priority': 47, 'seqstrict': 1, 'strict': 2, 'symbol': 28, 'total': 110}
Per-file block counts:
- `reference-semantics/semantics/assert.k`: 3
- `reference-semantics/semantics/bool.k`: 14
- `reference-semantics/semantics/builtins.k`: 175
- `reference-semantics/semantics/call.k`: 24
- `reference-semantics/semantics/comprehension.k`: 10
- `reference-semantics/semantics/concrete.k`: 21
- `reference-semantics/semantics/controls.k`: 37
- `reference-semantics/semantics/core.k`: 84
- `reference-semantics/semantics/dict.k`: 40
- `reference-semantics/semantics/float.k`: 155
- `reference-semantics/semantics/functions.k`: 19
- `reference-semantics/semantics/int.k`: 17
- `reference-semantics/semantics/iter.k`: 1
- `reference-semantics/semantics/list.k`: 32
- `reference-semantics/semantics/methods.k`: 102
- `reference-semantics/semantics/operators.k`: 12
- `reference-semantics/semantics/range.k`: 8
- `reference-semantics/semantics/set.k`: 18
- `reference-semantics/semantics/sort.k`: 25
- `reference-semantics/semantics/str.k`: 33
- `reference-semantics/semantics/subscript.k`: 57
- `reference-semantics/semantics/syntax.k`: 16
- `reference-semantics/semantics/tuple.k`: 25
- `spec.k`: 4
- `verification.k`: 12

## 1. rule — `reference-semantics/semantics/assert.k:6` (module `MPY-ASSERT`)

Attributes/classifiers: none

```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

## 2. rule — `reference-semantics/semantics/assert.k:8` (module `MPY-ASSERT`)

Attributes/classifiers: none

```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

## 3. rule — `reference-semantics/semantics/assert.k:13` (module `MPY-ASSERT`)

Attributes/classifiers: priority

```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 4. rule — `reference-semantics/semantics/bool.k:8` (module `MPY-BOOL`)

Attributes/classifiers: none

```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

## 5. rule — `reference-semantics/semantics/bool.k:10` (module `MPY-BOOL`)

Attributes/classifiers: none

```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

## 6. rule — `reference-semantics/semantics/bool.k:11` (module `MPY-BOOL`)

Attributes/classifiers: none

```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

## 7. context — `reference-semantics/semantics/bool.k:16` (module `MPY-BOOL`)

Attributes/classifiers: none

```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

## 8. rule — `reference-semantics/semantics/bool.k:17` (module `MPY-BOOL`)

Attributes/classifiers: none

```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

## 9. rule — `reference-semantics/semantics/bool.k:18` (module `MPY-BOOL`)

Attributes/classifiers: none

```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

## 10. rule — `reference-semantics/semantics/bool.k:20` (module `MPY-BOOL`)

Attributes/classifiers: none

```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

## 11. rule — `reference-semantics/semantics/bool.k:22` (module `MPY-BOOL`)

Attributes/classifiers: none

```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

## 12. rule — `reference-semantics/semantics/bool.k:24` (module `MPY-BOOL`)

Attributes/classifiers: none

```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

## 13. rule — `reference-semantics/semantics/bool.k:29` (module `MPY-BOOL`)

Attributes/classifiers: priority

```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

## 14. rule — `reference-semantics/semantics/bool.k:31` (module `MPY-BOOL`)

Attributes/classifiers: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

## 15. rule — `reference-semantics/semantics/bool.k:35` (module `MPY-BOOL`)

Attributes/classifiers: priority

```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## 16. rule — `reference-semantics/semantics/bool.k:39` (module `MPY-BOOL`)

Attributes/classifiers: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

## 17. rule — `reference-semantics/semantics/bool.k:43` (module `MPY-BOOL`)

Attributes/classifiers: priority

```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## 18. syntax — `reference-semantics/semantics/builtins.k:17` (module `MPY-BUILTINS`)

Attributes/classifiers: function

```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

## 19. syntax — `reference-semantics/semantics/builtins.k:20` (module `MPY-BUILTINS`)

Attributes/classifiers: function

```k
  syntax Int ::= seqLen(Val) [function]
```

## 20. rule — `reference-semantics/semantics/builtins.k:21` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

## 21. rule — `reference-semantics/semantics/builtins.k:22` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

## 22. rule — `reference-semantics/semantics/builtins.k:23` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

## 23. rule — `reference-semantics/semantics/builtins.k:24` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

## 24. rule — `reference-semantics/semantics/builtins.k:25` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

## 25. rule — `reference-semantics/semantics/builtins.k:26` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

## 26. rule — `reference-semantics/semantics/builtins.k:32` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

## 27. rule — `reference-semantics/semantics/builtins.k:33` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

## 28. rule — `reference-semantics/semantics/builtins.k:34` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

## 29. rule — `reference-semantics/semantics/builtins.k:35` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

## 30. syntax — `reference-semantics/semantics/builtins.k:36` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

## 31. rule — `reference-semantics/semantics/builtins.k:37` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule charsOf(.IntSeq)                => .ValSeq
```

## 32. rule — `reference-semantics/semantics/builtins.k:38` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

## 33. rule — `reference-semantics/semantics/builtins.k:41` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

## 34. rule — `reference-semantics/semantics/builtins.k:44` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

## 35. syntax — `reference-semantics/semantics/builtins.k:47` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

## 36. rule — `reference-semantics/semantics/builtins.k:48` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

## 37. rule — `reference-semantics/semantics/builtins.k:49` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

## 38. rule — `reference-semantics/semantics/builtins.k:50` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

## 39. syntax — `reference-semantics/semantics/builtins.k:54` (module `MPY-BUILTINS`)

Attributes/classifiers: function

```k
  syntax Int ::= intOf(Val) [function]
```

## 40. rule — `reference-semantics/semantics/builtins.k:55` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule intOf(I:Int)  => I
```

## 41. rule — `reference-semantics/semantics/builtins.k:56` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

## 42. syntax — `reference-semantics/semantics/builtins.k:59` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

## 43. rule — `reference-semantics/semantics/builtins.k:60` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

## 44. rule — `reference-semantics/semantics/builtins.k:61` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

## 45. rule — `reference-semantics/semantics/builtins.k:62` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

## 46. rule — `reference-semantics/semantics/builtins.k:64` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

## 47. syntax — `reference-semantics/semantics/builtins.k:67` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

## 48. rule — `reference-semantics/semantics/builtins.k:68` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

## 49. rule — `reference-semantics/semantics/builtins.k:69` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

## 50. rule — `reference-semantics/semantics/builtins.k:70` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

## 51. rule — `reference-semantics/semantics/builtins.k:72` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

## 52. syntax — `reference-semantics/semantics/builtins.k:76` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

## 53. rule — `reference-semantics/semantics/builtins.k:77` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

## 54. rule — `reference-semantics/semantics/builtins.k:78` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

## 55. rule — `reference-semantics/semantics/builtins.k:80` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

## 56. rule — `reference-semantics/semantics/builtins.k:81` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

## 57. rule — `reference-semantics/semantics/builtins.k:82` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

## 58. syntax — `reference-semantics/semantics/builtins.k:86` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

## 59. rule — `reference-semantics/semantics/builtins.k:87` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

## 60. rule — `reference-semantics/semantics/builtins.k:88` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

## 61. rule — `reference-semantics/semantics/builtins.k:90` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

## 62. rule — `reference-semantics/semantics/builtins.k:91` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

## 63. rule — `reference-semantics/semantics/builtins.k:92` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

## 64. syntax — `reference-semantics/semantics/builtins.k:97` (module `MPY-BUILTINS`)

Attributes/classifiers: function

```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

## 65. rule — `reference-semantics/semantics/builtins.k:98` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

## 66. rule — `reference-semantics/semantics/builtins.k:99` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule maxVals(M:Int, .Vals)           => M
```

## 67. rule — `reference-semantics/semantics/builtins.k:100` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

## 68. syntax — `reference-semantics/semantics/builtins.k:102` (module `MPY-BUILTINS`)

Attributes/classifiers: function

```k
  syntax Int ::= minVals(Int, Vals) [function]
```

## 69. rule — `reference-semantics/semantics/builtins.k:103` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

## 70. rule — `reference-semantics/semantics/builtins.k:104` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule minVals(M:Int, .Vals)           => M
```

## 71. rule — `reference-semantics/semantics/builtins.k:105` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

## 72. rule — `reference-semantics/semantics/builtins.k:108` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

## 73. rule — `reference-semantics/semantics/builtins.k:111` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

## 74. syntax — `reference-semantics/semantics/builtins.k:114` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

## 75. rule — `reference-semantics/semantics/builtins.k:115` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

## 76. rule — `reference-semantics/semantics/builtins.k:116` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

## 77. syntax — `reference-semantics/semantics/builtins.k:117` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

## 78. rule — `reference-semantics/semantics/builtins.k:118` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

## 79. rule — `reference-semantics/semantics/builtins.k:119` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

## 80. rule — `reference-semantics/semantics/builtins.k:124` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

## 81. syntax — `reference-semantics/semantics/builtins.k:126` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

## 82. rule — `reference-semantics/semantics/builtins.k:127` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

## 83. rule — `reference-semantics/semantics/builtins.k:128` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

## 84. rule — `reference-semantics/semantics/builtins.k:132` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

## 85. syntax — `reference-semantics/semantics/builtins.k:134` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

## 86. rule — `reference-semantics/semantics/builtins.k:135` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

## 87. rule — `reference-semantics/semantics/builtins.k:136` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

## 88. rule — `reference-semantics/semantics/builtins.k:137` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

## 89. rule — `reference-semantics/semantics/builtins.k:140` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

## 90. rule — `reference-semantics/semantics/builtins.k:143` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

## 91. rule — `reference-semantics/semantics/builtins.k:144` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

## 92. rule — `reference-semantics/semantics/builtins.k:148` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

## 93. rule — `reference-semantics/semantics/builtins.k:149` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

## 94. rule — `reference-semantics/semantics/builtins.k:152` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

## 95. rule — `reference-semantics/semantics/builtins.k:156` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

## 96. syntax — `reference-semantics/semantics/builtins.k:158` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

## 97. rule — `reference-semantics/semantics/builtins.k:159` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

## 98. rule — `reference-semantics/semantics/builtins.k:160` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

## 99. rule — `reference-semantics/semantics/builtins.k:163` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

## 100. rule — `reference-semantics/semantics/builtins.k:164` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

## 101. rule — `reference-semantics/semantics/builtins.k:167` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

## 102. rule — `reference-semantics/semantics/builtins.k:169` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

## 103. rule — `reference-semantics/semantics/builtins.k:170` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

## 104. rule — `reference-semantics/semantics/builtins.k:171` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

## 105. rule — `reference-semantics/semantics/builtins.k:173` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

## 106. rule — `reference-semantics/semantics/builtins.k:174` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

## 107. rule — `reference-semantics/semantics/builtins.k:177` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

## 108. rule — `reference-semantics/semantics/builtins.k:178` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

## 109. rule — `reference-semantics/semantics/builtins.k:179` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

## 110. rule — `reference-semantics/semantics/builtins.k:187` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

## 111. syntax — `reference-semantics/semantics/builtins.k:188` (module `MPY-BUILTINS`)

Attributes/classifiers: function

```k
  syntax Int ::= evalArith(IntSeq) [function]
```

## 112. rule — `reference-semantics/semantics/builtins.k:189` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

## 113. syntax — `reference-semantics/semantics/builtins.k:192` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

## 114. syntax — `reference-semantics/semantics/builtins.k:194` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= evDigit(Int) [function, total]
```

## 115. rule — `reference-semantics/semantics/builtins.k:195` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

## 116. syntax — `reference-semantics/semantics/builtins.k:196` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

## 117. rule — `reference-semantics/semantics/builtins.k:197` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

## 118. rule — `reference-semantics/semantics/builtins.k:198` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule evHead42(_:IntSeq)            => false [owise]
```

## 119. syntax — `reference-semantics/semantics/builtins.k:199` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

## 120. rule — `reference-semantics/semantics/builtins.k:200` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

## 121. rule — `reference-semantics/semantics/builtins.k:201` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule evHead47(_:IntSeq)            => false [owise]
```

## 122. syntax — `reference-semantics/semantics/builtins.k:203` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

## 123. rule — `reference-semantics/semantics/builtins.k:204` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

## 124. rule — `reference-semantics/semantics/builtins.k:205` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

## 125. rule — `reference-semantics/semantics/builtins.k:206` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

## 126. rule — `reference-semantics/semantics/builtins.k:207` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

## 127. rule — `reference-semantics/semantics/builtins.k:208` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

## 128. rule — `reference-semantics/semantics/builtins.k:209` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

## 129. rule — `reference-semantics/semantics/builtins.k:210` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

## 130. rule — `reference-semantics/semantics/builtins.k:211` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

## 131. rule — `reference-semantics/semantics/builtins.k:212` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

## 132. syntax — `reference-semantics/semantics/builtins.k:214` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

## 133. rule — `reference-semantics/semantics/builtins.k:216` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokNds(.IntSeq)                => .IntSeq
```

## 134. rule — `reference-semantics/semantics/builtins.k:217` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

## 135. rule — `reference-semantics/semantics/builtins.k:218` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

## 136. rule — `reference-semantics/semantics/builtins.k:219` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

## 137. rule — `reference-semantics/semantics/builtins.k:221` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

## 138. rule — `reference-semantics/semantics/builtins.k:223` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

## 139. syntax — `reference-semantics/semantics/builtins.k:225` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

## 140. syntax — `reference-semantics/semantics/builtins.k:226` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

## 141. rule — `reference-semantics/semantics/builtins.k:227` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

## 142. rule — `reference-semantics/semantics/builtins.k:228` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

## 143. syntax — `reference-semantics/semantics/builtins.k:230` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

## 144. rule — `reference-semantics/semantics/builtins.k:231` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

## 145. rule — `reference-semantics/semantics/builtins.k:232` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

## 146. rule — `reference-semantics/semantics/builtins.k:233` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

## 147. rule — `reference-semantics/semantics/builtins.k:234` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

## 148. rule — `reference-semantics/semantics/builtins.k:235` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

## 149. rule — `reference-semantics/semantics/builtins.k:236` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

## 150. syntax — `reference-semantics/semantics/builtins.k:238` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

## 151. rule — `reference-semantics/semantics/builtins.k:239` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

## 152. rule — `reference-semantics/semantics/builtins.k:240` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

## 153. rule — `reference-semantics/semantics/builtins.k:241` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

## 154. rule — `reference-semantics/semantics/builtins.k:243` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

## 155. syntax — `reference-semantics/semantics/builtins.k:244` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

## 156. rule — `reference-semantics/semantics/builtins.k:245` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

## 157. rule — `reference-semantics/semantics/builtins.k:246` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

## 158. syntax — `reference-semantics/semantics/builtins.k:247` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

## 159. rule — `reference-semantics/semantics/builtins.k:248` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

## 160. syntax — `reference-semantics/semantics/builtins.k:250` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

## 161. rule — `reference-semantics/semantics/builtins.k:251` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

## 162. rule — `reference-semantics/semantics/builtins.k:252` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

## 163. rule — `reference-semantics/semantics/builtins.k:253` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

## 164. rule — `reference-semantics/semantics/builtins.k:254` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

## 165. syntax — `reference-semantics/semantics/builtins.k:255` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

## 166. rule — `reference-semantics/semantics/builtins.k:256` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

## 167. rule — `reference-semantics/semantics/builtins.k:257` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

## 168. rule — `reference-semantics/semantics/builtins.k:260` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

## 169. rule — `reference-semantics/semantics/builtins.k:263` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

## 170. syntax — `reference-semantics/semantics/builtins.k:265` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

## 171. rule — `reference-semantics/semantics/builtins.k:266` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

## 172. rule — `reference-semantics/semantics/builtins.k:267` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

## 173. rule — `reference-semantics/semantics/builtins.k:268` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule inLevelE(_:String, _:String) => false [owise]
```

## 174. syntax — `reference-semantics/semantics/builtins.k:269` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

## 175. rule — `reference-semantics/semantics/builtins.k:270` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

## 176. rule — `reference-semantics/semantics/builtins.k:271` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

## 177. syntax — `reference-semantics/semantics/builtins.k:272` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

## 178. rule — `reference-semantics/semantics/builtins.k:273` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

## 179. rule — `reference-semantics/semantics/builtins.k:274` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

## 180. syntax — `reference-semantics/semantics/builtins.k:279` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  syntax KItem ::= "#md5"
```

## 181. rule — `reference-semantics/semantics/builtins.k:280` (module `MPY-BUILTINS`)

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

## 182. rule — `reference-semantics/semantics/builtins.k:282` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

## 183. syntax — `reference-semantics/semantics/builtins.k:283` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  syntax Val ::= md5Obj(IntSeq)
```

## 184. rule — `reference-semantics/semantics/builtins.k:284` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

## 185. syntax — `reference-semantics/semantics/builtins.k:285` (module `MPY-BUILTINS`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

## 186. rule — `reference-semantics/semantics/builtins.k:291` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

## 187. rule — `reference-semantics/semantics/builtins.k:292` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

## 188. syntax — `reference-semantics/semantics/builtins.k:293` (module `MPY-BUILTINS`)

Attributes/classifiers: function

```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

## 189. rule — `reference-semantics/semantics/builtins.k:294` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule isIntV(_:Int)         => true
```

## 190. rule — `reference-semantics/semantics/builtins.k:295` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule isIntV(_:Val)         => false [owise]
```

## 191. rule — `reference-semantics/semantics/builtins.k:296` (module `MPY-BUILTINS`)

Attributes/classifiers: none

```k
  rule isStrV(str(_:IntSeq)) => true
```

## 192. rule — `reference-semantics/semantics/builtins.k:297` (module `MPY-BUILTINS`)

Attributes/classifiers: owise

```k
  rule isStrV(_:Val)         => false [owise]
```

## 193. rule — `reference-semantics/semantics/call.k:16` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

## 194. syntax — `reference-semantics/semantics/call.k:19` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  syntax KItem ::= #callee(Exprs)
```

## 195. rule — `reference-semantics/semantics/call.k:20` (module `MPY-CALL`)

Attributes/classifiers: owise

```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

## 196. rule — `reference-semantics/semantics/call.k:21` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

## 197. rule — `reference-semantics/semantics/call.k:24` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

## 198. rule — `reference-semantics/semantics/call.k:26` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

## 199. rule — `reference-semantics/semantics/call.k:27` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

## 200. rule — `reference-semantics/semantics/call.k:28` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

## 201. rule — `reference-semantics/semantics/call.k:29` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

## 202. rule — `reference-semantics/semantics/call.k:30` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

## 203. rule — `reference-semantics/semantics/call.k:31` (module `MPY-CALL`)

Attributes/classifiers: owise

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

## 204. rule — `reference-semantics/semantics/call.k:32` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

## 205. rule — `reference-semantics/semantics/call.k:38` (module `MPY-CALL`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 206. rule — `reference-semantics/semantics/call.k:42` (module `MPY-CALL`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

## 207. rule — `reference-semantics/semantics/call.k:47` (module `MPY-CALL`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 208. syntax — `reference-semantics/semantics/call.k:52` (module `MPY-CALL`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

## 209. rule — `reference-semantics/semantics/call.k:53` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

## 210. rule — `reference-semantics/semantics/call.k:56` (module `MPY-CALL`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

## 211. rule — `reference-semantics/semantics/call.k:63` (module `MPY-CALL`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

## 212. rule — `reference-semantics/semantics/call.k:69` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

## 213. rule — `reference-semantics/semantics/call.k:80` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

## 214. syntax — `reference-semantics/semantics/call.k:87` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  syntax KItem ::= #allocCells(ParamNames)
```

## 215. rule — `reference-semantics/semantics/call.k:88` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

## 216. rule — `reference-semantics/semantics/call.k:89` (module `MPY-CALL`)

Attributes/classifiers: none

```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

## 217. rule — `reference-semantics/semantics/comprehension.k:11` (module `MPY-COMPREHENSION`)

Attributes/classifiers: none

```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

## 218. rule — `reference-semantics/semantics/comprehension.k:12` (module `MPY-COMPREHENSION`)

Attributes/classifiers: none

```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

## 219. syntax — `reference-semantics/semantics/comprehension.k:14` (module `MPY-COMPREHENSION`)

Attributes/classifiers: macro

```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

## 220. rule — `reference-semantics/semantics/comprehension.k:15` (module `MPY-COMPREHENSION`)

Attributes/classifiers: none

```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

## 221. syntax — `reference-semantics/semantics/comprehension.k:18` (module `MPY-COMPREHENSION`)

Attributes/classifiers: macro

```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

## 222. rule — `reference-semantics/semantics/comprehension.k:19` (module `MPY-COMPREHENSION`)

Attributes/classifiers: none

```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

## 223. rule — `reference-semantics/semantics/comprehension.k:21` (module `MPY-COMPREHENSION`)

Attributes/classifiers: none

```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

## 224. syntax — `reference-semantics/semantics/comprehension.k:24` (module `MPY-COMPREHENSION`)

Attributes/classifiers: macro

```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

## 225. rule — `reference-semantics/semantics/comprehension.k:25` (module `MPY-COMPREHENSION`)

Attributes/classifiers: none

```k
  rule compGuard(.Exprs)             => Bool(true)
```

## 226. rule — `reference-semantics/semantics/comprehension.k:26` (module `MPY-COMPREHENSION`)

Attributes/classifiers: none

```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## 227. rule — `reference-semantics/semantics/concrete.k:13` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

## 228. rule — `reference-semantics/semantics/concrete.k:16` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

## 229. syntax — `reference-semantics/semantics/concrete.k:25` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  syntax Val ::= kvP(Val, Val)
```

## 230. syntax — `reference-semantics/semantics/concrete.k:26` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

## 231. rule — `reference-semantics/semantics/concrete.k:28` (module `MPY-CONCRETE`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

## 232. rule — `reference-semantics/semantics/concrete.k:31` (module `MPY-CONCRETE`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

## 233. rule — `reference-semantics/semantics/concrete.k:34` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

## 234. rule — `reference-semantics/semantics/concrete.k:36` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

## 235. rule — `reference-semantics/semantics/concrete.k:38` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

## 236. syntax — `reference-semantics/semantics/concrete.k:42` (module `MPY-CONCRETE`)

Attributes/classifiers: function

```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

## 237. rule — `reference-semantics/semantics/concrete.k:43` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

## 238. rule — `reference-semantics/semantics/concrete.k:44` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

## 239. rule — `reference-semantics/semantics/concrete.k:47` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

## 240. syntax — `reference-semantics/semantics/concrete.k:51` (module `MPY-CONCRETE`)

Attributes/classifiers: function

```k
  syntax Bool ::= kLt(Val, Val) [function]
```

## 241. rule — `reference-semantics/semantics/concrete.k:52` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

## 242. rule — `reference-semantics/semantics/concrete.k:53` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

## 243. rule — `reference-semantics/semantics/concrete.k:54` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

## 244. syntax — `reference-semantics/semantics/concrete.k:56` (module `MPY-CONCRETE`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

## 245. rule — `reference-semantics/semantics/concrete.k:57` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule unpairVS(.ValSeq) => .ValSeq
```

## 246. rule — `reference-semantics/semantics/concrete.k:58` (module `MPY-CONCRETE`)

Attributes/classifiers: none

```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

## 247. rule — `reference-semantics/semantics/concrete.k:59` (module `MPY-CONCRETE`)

Attributes/classifiers: owise

```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## 248. rule — `reference-semantics/semantics/controls.k:9` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

## 249. rule — `reference-semantics/semantics/controls.k:12` (module `MPY-CONTROLS`)

Attributes/classifiers: priority

```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

## 250. rule — `reference-semantics/semantics/controls.k:20` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

## 251. rule — `reference-semantics/semantics/controls.k:27` (module `MPY-CONTROLS`)

Attributes/classifiers: priority

```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

## 252. rule — `reference-semantics/semantics/controls.k:35` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

## 253. rule — `reference-semantics/semantics/controls.k:36` (module `MPY-CONTROLS`)

Attributes/classifiers: owise

```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

## 254. syntax — `reference-semantics/semantics/controls.k:37` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  syntax KItem ::= #bindImports(ParamNames)
```

## 255. rule — `reference-semantics/semantics/controls.k:38` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

## 256. rule — `reference-semantics/semantics/controls.k:39` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

## 257. rule — `reference-semantics/semantics/controls.k:43` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

## 258. rule — `reference-semantics/semantics/controls.k:48` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> Expr(_:Val) => .K ... </k>
```

## 259. syntax — `reference-semantics/semantics/controls.k:51` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

## 260. rule — `reference-semantics/semantics/controls.k:52` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

## 261. rule — `reference-semantics/semantics/controls.k:53` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

## 262. rule — `reference-semantics/semantics/controls.k:54` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

## 263. rule — `reference-semantics/semantics/controls.k:57` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

## 264. rule — `reference-semantics/semantics/controls.k:59` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

## 265. syntax — `reference-semantics/semantics/controls.k:65` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

## 266. rule — `reference-semantics/semantics/controls.k:69` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

## 267. rule — `reference-semantics/semantics/controls.k:71` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

## 268. rule — `reference-semantics/semantics/controls.k:72` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

## 269. rule — `reference-semantics/semantics/controls.k:73` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

## 270. rule — `reference-semantics/semantics/controls.k:77` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

## 271. rule — `reference-semantics/semantics/controls.k:78` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

## 272. rule — `reference-semantics/semantics/controls.k:79` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

## 273. rule — `reference-semantics/semantics/controls.k:81` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

## 274. rule — `reference-semantics/semantics/controls.k:85` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

## 275. rule — `reference-semantics/semantics/controls.k:86` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> Continue => #cont ... </k>
```

## 276. rule — `reference-semantics/semantics/controls.k:87` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> Break => #brk ... </k>
```

## 277. rule — `reference-semantics/semantics/controls.k:88` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

## 278. rule — `reference-semantics/semantics/controls.k:89` (module `MPY-CONTROLS`)

Attributes/classifiers: owise

```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

## 279. rule — `reference-semantics/semantics/controls.k:90` (module `MPY-CONTROLS`)

Attributes/classifiers: none

```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

## 280. rule — `reference-semantics/semantics/controls.k:91` (module `MPY-CONTROLS`)

Attributes/classifiers: owise

```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

## 281. rule — `reference-semantics/semantics/controls.k:95` (module `MPY-CONTROLS`)

Attributes/classifiers: priority

```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 282. rule — `reference-semantics/semantics/controls.k:98` (module `MPY-CONTROLS`)

Attributes/classifiers: priority

```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 283. rule — `reference-semantics/semantics/controls.k:101` (module `MPY-CONTROLS`)

Attributes/classifiers: priority

```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 284. rule — `reference-semantics/semantics/controls.k:106` (module `MPY-CONTROLS`)

Attributes/classifiers: priority

```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 285. syntax — `reference-semantics/semantics/core.k:13` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

## 286. syntax — `reference-semantics/semantics/core.k:14` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

## 287. syntax — `reference-semantics/semantics/core.k:15` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax Str    ::= str(IntSeq)
```

## 288. syntax — `reference-semantics/semantics/core.k:18` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

## 289. syntax — `reference-semantics/semantics/core.k:25` (module `MPY-CORE`)

Attributes/classifiers: none

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

## 290. syntax — `reference-semantics/semantics/core.k:36` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax Parent   ::= "root" | parent(Int)
```

## 291. syntax — `reference-semantics/semantics/core.k:37` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax Scope    ::= scope(Map, Parent)
```

## 292. syntax — `reference-semantics/semantics/core.k:38` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax KResult  ::= Val
```

## 293. syntax — `reference-semantics/semantics/core.k:39` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

## 294. syntax — `reference-semantics/semantics/core.k:40` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax Vals     ::= List{Val, ","}
```

## 295. syntax — `reference-semantics/semantics/core.k:41` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

## 296. syntax — `reference-semantics/semantics/core.k:42` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax RetState ::= "noRet" | retV(Val)
```

## 297. configuration — `reference-semantics/semantics/core.k:49` (module `MPY-CORE`)

Attributes/classifiers: none

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

## 298. syntax — `reference-semantics/semantics/core.k:68` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= isRefV(Val) [function, total]
```

## 299. rule — `reference-semantics/semantics/core.k:69` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule isRefV(ref(_:Int)) => true
```

## 300. rule — `reference-semantics/semantics/core.k:70` (module `MPY-CORE`)

Attributes/classifiers: owise

```k
  rule isRefV(_:Val)      => false [owise]
```

## 301. syntax — `reference-semantics/semantics/core.k:75` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax HeapVal ::= cellV(Val)
```

## 302. syntax — `reference-semantics/semantics/core.k:76` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

## 303. rule — `reference-semantics/semantics/core.k:77` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule isCellRef(cellRef(_:Int)) => true
```

## 304. rule — `reference-semantics/semantics/core.k:78` (module `MPY-CORE`)

Attributes/classifiers: owise

```k
  rule isCellRef(_:Val)          => false [owise]
```

## 305. rule — `reference-semantics/semantics/core.k:85` (module `MPY-CORE`)

Attributes/classifiers: priority

```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

## 306. syntax — `reference-semantics/semantics/core.k:95` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax Val ::= kwV(String, Val)
```

## 307. syntax — `reference-semantics/semantics/core.k:96` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax KItem ::= #kwTag(String)
```

## 308. rule — `reference-semantics/semantics/core.k:97` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

## 309. rule — `reference-semantics/semantics/core.k:98` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

## 310. syntax — `reference-semantics/semantics/core.k:100` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= isKwV(Val) [function, total]
```

## 311. rule — `reference-semantics/semantics/core.k:101` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

## 312. rule — `reference-semantics/semantics/core.k:102` (module `MPY-CORE`)

Attributes/classifiers: owise

```k
  rule isKwV(_:Val)                => false [owise]
```

## 313. syntax — `reference-semantics/semantics/core.k:106` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax Val ::= cellsMark(ParamNames)
```

## 314. syntax — `reference-semantics/semantics/core.k:107` (module `MPY-CORE`)

Attributes/classifiers: function

```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

## 315. rule — `reference-semantics/semantics/core.k:108` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

## 316. syntax — `reference-semantics/semantics/core.k:109` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

## 317. rule — `reference-semantics/semantics/core.k:110` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule pnMember(_:String, .ParamNames) => false
```

## 318. rule — `reference-semantics/semantics/core.k:111` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

## 319. syntax — `reference-semantics/semantics/core.k:113` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax KItem ::= #cellW(Val, Val)
```

## 320. rule — `reference-semantics/semantics/core.k:114` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

## 321. syntax — `reference-semantics/semantics/core.k:117` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax KItem ::= #alloc(Val)
```

## 322. rule — `reference-semantics/semantics/core.k:118` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

## 323. syntax — `reference-semantics/semantics/core.k:124` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax KItem ::= #loadAll(Module)
```

## 324. rule — `reference-semantics/semantics/core.k:125` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

## 325. rule — `reference-semantics/semantics/core.k:126` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

## 326. rule — `reference-semantics/semantics/core.k:127` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> .Stmts => .K ... </k>
```

## 327. syntax — `reference-semantics/semantics/core.k:130` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax KItem ::= #look(String, Int)
```

## 328. rule — `reference-semantics/semantics/core.k:131` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

## 329. rule — `reference-semantics/semantics/core.k:132` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

## 330. rule — `reference-semantics/semantics/core.k:145` (module `MPY-CORE`)

Attributes/classifiers: priority

```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

## 331. rule — `reference-semantics/semantics/core.k:152` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

## 332. syntax — `reference-semantics/semantics/core.k:157` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax Scope ::= "builtinsScope" [function, total]
```

## 333. rule — `reference-semantics/semantics/core.k:158` (module `MPY-CORE`)

Attributes/classifiers: none

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

## 334. syntax — `reference-semantics/semantics/core.k:185` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax ApplyK ::= toCall(Val)
```

## 335. syntax — `reference-semantics/semantics/core.k:186` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

## 336. rule — `reference-semantics/semantics/core.k:189` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

## 337. rule — `reference-semantics/semantics/core.k:190` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

## 338. rule — `reference-semantics/semantics/core.k:191` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

## 339. rule — `reference-semantics/semantics/core.k:194` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> Int(I:Int)   => I ... </k>
```

## 340. rule — `reference-semantics/semantics/core.k:195` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> Bool(B:Bool) => B ... </k>
```

## 341. rule — `reference-semantics/semantics/core.k:196` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule <k> NoneVal      => noneV ... </k>
```

## 342. syntax — `reference-semantics/semantics/core.k:199` (module `MPY-CORE`)

Attributes/classifiers: function

```k
  syntax Bool ::= truthy(Val) [function]
```

## 343. rule — `reference-semantics/semantics/core.k:200` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule truthy(B:Bool)          => B
```

## 344. rule — `reference-semantics/semantics/core.k:201` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule truthy(noneV)           => false
```

## 345. rule — `reference-semantics/semantics/core.k:202` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule truthy(I:Int)           => I =/=Int 0
```

## 346. rule — `reference-semantics/semantics/core.k:203` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

## 347. rule — `reference-semantics/semantics/core.k:204` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

## 348. rule — `reference-semantics/semantics/core.k:205` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

## 349. syntax — `reference-semantics/semantics/core.k:208` (module `MPY-CORE`)

Attributes/classifiers: function

```k
  syntax Val  ::= applyUn(String, Val) [function]
```

## 350. syntax — `reference-semantics/semantics/core.k:209` (module `MPY-CORE`)

Attributes/classifiers: function

```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

## 351. syntax — `reference-semantics/semantics/core.k:210` (module `MPY-CORE`)

Attributes/classifiers: function

```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

## 352. syntax — `reference-semantics/semantics/core.k:213` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

## 353. rule — `reference-semantics/semantics/core.k:214` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

## 354. rule — `reference-semantics/semantics/core.k:215` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

## 355. syntax — `reference-semantics/semantics/core.k:217` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

## 356. rule — `reference-semantics/semantics/core.k:218` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

## 357. rule — `reference-semantics/semantics/core.k:219` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

## 358. syntax — `reference-semantics/semantics/core.k:223` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

## 359. rule — `reference-semantics/semantics/core.k:224` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule vsLen(.ValSeq)                => 0
```

## 360. rule — `reference-semantics/semantics/core.k:225` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

## 361. syntax — `reference-semantics/semantics/core.k:227` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

## 362. rule — `reference-semantics/semantics/core.k:228` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule isLen(.IntSeq)                => 0
```

## 363. rule — `reference-semantics/semantics/core.k:229` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

## 364. syntax — `reference-semantics/semantics/core.k:233` (module `MPY-CORE`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

## 365. rule — `reference-semantics/semantics/core.k:234` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

## 366. rule — `reference-semantics/semantics/core.k:235` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

## 367. rule — `reference-semantics/semantics/core.k:236` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

## 368. rule — `reference-semantics/semantics/core.k:238` (module `MPY-CORE`)

Attributes/classifiers: none

```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

## 369. syntax — `reference-semantics/semantics/dict.k:20` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

## 370. syntax — `reference-semantics/semantics/dict.k:23` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

## 371. rule — `reference-semantics/semantics/dict.k:26` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

## 372. rule — `reference-semantics/semantics/dict.k:27` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

## 373. rule — `reference-semantics/semantics/dict.k:28` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

## 374. rule — `reference-semantics/semantics/dict.k:30` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

## 375. rule — `reference-semantics/semantics/dict.k:32` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

## 376. syntax — `reference-semantics/semantics/dict.k:37` (module `MPY-DICT`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

## 377. rule — `reference-semantics/semantics/dict.k:38` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

## 378. rule — `reference-semantics/semantics/dict.k:39` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

## 379. rule — `reference-semantics/semantics/dict.k:40` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

## 380. syntax — `reference-semantics/semantics/dict.k:43` (module `MPY-DICT`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

## 381. rule — `reference-semantics/semantics/dict.k:44` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

## 382. rule — `reference-semantics/semantics/dict.k:45` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

## 383. syntax — `reference-semantics/semantics/dict.k:49` (module `MPY-DICT`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

## 384. rule — `reference-semantics/semantics/dict.k:50` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

## 385. rule — `reference-semantics/semantics/dict.k:52` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

## 386. rule — `reference-semantics/semantics/dict.k:54` (module `MPY-DICT`)

Attributes/classifiers: owise

```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

## 387. rule — `reference-semantics/semantics/dict.k:58` (module `MPY-DICT`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

## 388. rule — `reference-semantics/semantics/dict.k:63` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

## 389. syntax — `reference-semantics/semantics/dict.k:64` (module `MPY-DICT`)

Attributes/classifiers: function

```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

## 390. rule — `reference-semantics/semantics/dict.k:65` (module `MPY-DICT`)

Attributes/classifiers: priority

```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

## 391. syntax — `reference-semantics/semantics/dict.k:70` (module `MPY-DICT`)

Attributes/classifiers: function

```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

## 392. rule — `reference-semantics/semantics/dict.k:71` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

## 393. syntax — `reference-semantics/semantics/dict.k:76` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  syntax KItem ::= #dsetK(String, Val)
```

## 394. rule — `reference-semantics/semantics/dict.k:77` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

## 395. rule — `reference-semantics/semantics/dict.k:78` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

## 396. rule — `reference-semantics/semantics/dict.k:82` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

## 397. syntax — `reference-semantics/semantics/dict.k:86` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

## 398. rule — `reference-semantics/semantics/dict.k:87` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

## 399. syntax — `reference-semantics/semantics/dict.k:90` (module `MPY-DICT`)

Attributes/classifiers: function, total

```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

## 400. rule — `reference-semantics/semantics/dict.k:91` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

## 401. rule — `reference-semantics/semantics/dict.k:92` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

## 402. rule — `reference-semantics/semantics/dict.k:95` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

## 403. syntax — `reference-semantics/semantics/dict.k:97` (module `MPY-DICT`)

Attributes/classifiers: function

```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

## 404. rule — `reference-semantics/semantics/dict.k:98` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

## 405. rule — `reference-semantics/semantics/dict.k:99` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

## 406. syntax — `reference-semantics/semantics/dict.k:101` (module `MPY-DICT`)

Attributes/classifiers: function

```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

## 407. rule — `reference-semantics/semantics/dict.k:102` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

## 408. rule — `reference-semantics/semantics/dict.k:103` (module `MPY-DICT`)

Attributes/classifiers: none

```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## 409. syntax — `reference-semantics/semantics/float.k:20` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  syntax Val ::= Float
```

## 410. rule — `reference-semantics/semantics/float.k:21` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> Float(F:Float) => F ... </k>
```

## 411. syntax — `reference-semantics/semantics/float.k:24` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

## 412. rule — `reference-semantics/semantics/float.k:25` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

## 413. rule — `reference-semantics/semantics/float.k:27` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

## 414. syntax — `reference-semantics/semantics/float.k:30` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

## 415. rule — `reference-semantics/semantics/float.k:31` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

## 416. rule — `reference-semantics/semantics/float.k:32` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

## 417. syntax — `reference-semantics/semantics/float.k:37` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

## 418. rule — `reference-semantics/semantics/float.k:38` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

## 419. rule — `reference-semantics/semantics/float.k:39` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

## 420. rule — `reference-semantics/semantics/float.k:43` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

## 421. rule — `reference-semantics/semantics/float.k:44` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

## 422. syntax — `reference-semantics/semantics/float.k:50` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

## 423. rule — `reference-semantics/semantics/float.k:51` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

## 424. rule — `reference-semantics/semantics/float.k:52` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

## 425. syntax — `reference-semantics/semantics/float.k:54` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

## 426. rule — `reference-semantics/semantics/float.k:55` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

## 427. rule — `reference-semantics/semantics/float.k:56` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

## 428. rule — `reference-semantics/semantics/float.k:61` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> Import(_:String) => .K ... </k>
```

## 429. syntax — `reference-semantics/semantics/float.k:65` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  syntax KItem ::= "#mathCeil"
```

## 430. rule — `reference-semantics/semantics/float.k:66` (module `MPY-FLOAT`)

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

## 431. rule — `reference-semantics/semantics/float.k:67` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

## 432. syntax — `reference-semantics/semantics/float.k:70` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  syntax KItem ::= "#mathFloor"
```

## 433. rule — `reference-semantics/semantics/float.k:71` (module `MPY-FLOAT`)

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

## 434. rule — `reference-semantics/semantics/float.k:72` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

## 435. syntax — `reference-semantics/semantics/float.k:73` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol

```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

## 436. rule — `reference-semantics/semantics/float.k:74` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule floorFI(I:Int)   => I                        [concrete]
```

## 437. rule — `reference-semantics/semantics/float.k:75` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

## 438. rule — `reference-semantics/semantics/float.k:78` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

## 439. rule — `reference-semantics/semantics/float.k:79` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

## 440. syntax — `reference-semantics/semantics/float.k:82` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

## 441. rule — `reference-semantics/semantics/float.k:83` (module `MPY-FLOAT`)

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

## 442. rule — `reference-semantics/semantics/float.k:84` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

## 443. rule — `reference-semantics/semantics/float.k:85` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

## 444. syntax — `reference-semantics/semantics/float.k:86` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol

```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

## 445. rule — `reference-semantics/semantics/float.k:87` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule toF(F:Float) => F        [concrete]
```

## 446. rule — `reference-semantics/semantics/float.k:88` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

## 447. syntax — `reference-semantics/semantics/float.k:93` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol

```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

## 448. rule — `reference-semantics/semantics/float.k:94` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule ceilF(I:Int)   => I                       [concrete]
```

## 449. rule — `reference-semantics/semantics/float.k:95` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

## 450. rule — `reference-semantics/semantics/float.k:99` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

## 451. syntax — `reference-semantics/semantics/float.k:103` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

## 452. rule — `reference-semantics/semantics/float.k:104` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

## 453. rule — `reference-semantics/semantics/float.k:105` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

## 454. syntax — `reference-semantics/semantics/float.k:107` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

## 455. rule — `reference-semantics/semantics/float.k:108` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

## 456. rule — `reference-semantics/semantics/float.k:109` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

## 457. syntax — `reference-semantics/semantics/float.k:111` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

## 458. rule — `reference-semantics/semantics/float.k:112` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

## 459. rule — `reference-semantics/semantics/float.k:113` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

## 460. syntax — `reference-semantics/semantics/float.k:115` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

## 461. rule — `reference-semantics/semantics/float.k:116` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

## 462. rule — `reference-semantics/semantics/float.k:117` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

## 463. syntax — `reference-semantics/semantics/float.k:119` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

## 464. rule — `reference-semantics/semantics/float.k:120` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

## 465. rule — `reference-semantics/semantics/float.k:121` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

## 466. syntax — `reference-semantics/semantics/float.k:125` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

## 467. rule — `reference-semantics/semantics/float.k:126` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

## 468. rule — `reference-semantics/semantics/float.k:127` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

## 469. rule — `reference-semantics/semantics/float.k:128` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

## 470. rule — `reference-semantics/semantics/float.k:129` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

## 471. rule — `reference-semantics/semantics/float.k:132` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

## 472. rule — `reference-semantics/semantics/float.k:133` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

## 473. rule — `reference-semantics/semantics/float.k:134` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

## 474. rule — `reference-semantics/semantics/float.k:135` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

## 475. rule — `reference-semantics/semantics/float.k:136` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

## 476. rule — `reference-semantics/semantics/float.k:137` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

## 477. rule — `reference-semantics/semantics/float.k:138` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

## 478. rule — `reference-semantics/semantics/float.k:139` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

## 479. syntax — `reference-semantics/semantics/float.k:142` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

## 480. rule — `reference-semantics/semantics/float.k:143` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

## 481. rule — `reference-semantics/semantics/float.k:144` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

## 482. rule — `reference-semantics/semantics/float.k:145` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

## 483. rule — `reference-semantics/semantics/float.k:146` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

## 484. rule — `reference-semantics/semantics/float.k:147` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

## 485. rule — `reference-semantics/semantics/float.k:148` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

## 486. rule — `reference-semantics/semantics/float.k:149` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

## 487. rule — `reference-semantics/semantics/float.k:150` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

## 488. rule — `reference-semantics/semantics/float.k:151` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

## 489. rule — `reference-semantics/semantics/float.k:154` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

## 490. rule — `reference-semantics/semantics/float.k:155` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

## 491. syntax — `reference-semantics/semantics/float.k:160` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

## 492. rule — `reference-semantics/semantics/float.k:161` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

## 493. rule — `reference-semantics/semantics/float.k:162` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

## 494. syntax — `reference-semantics/semantics/float.k:165` (module `MPY-FLOAT`)

Attributes/classifiers: function

```k
  syntax Int ::= headIS(IntSeq) [function]
```

## 495. rule — `reference-semantics/semantics/float.k:166` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

## 496. syntax — `reference-semantics/semantics/float.k:167` (module `MPY-FLOAT`)

Attributes/classifiers: function, total

```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

## 497. rule — `reference-semantics/semantics/float.k:168` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

## 498. rule — `reference-semantics/semantics/float.k:169` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

## 499. rule — `reference-semantics/semantics/float.k:170` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

## 500. rule — `reference-semantics/semantics/float.k:171` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

## 501. syntax — `reference-semantics/semantics/float.k:173` (module `MPY-FLOAT`)

Attributes/classifiers: function, total

```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

## 502. rule — `reference-semantics/semantics/float.k:174` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fracPart(.IntSeq) => 0
```

## 503. rule — `reference-semantics/semantics/float.k:175` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

## 504. rule — `reference-semantics/semantics/float.k:176` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

## 505. rule — `reference-semantics/semantics/float.k:177` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fracAcc(.IntSeq, A:Int) => A
```

## 506. rule — `reference-semantics/semantics/float.k:178` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

## 507. syntax — `reference-semantics/semantics/float.k:179` (module `MPY-FLOAT`)

Attributes/classifiers: function, total

```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

## 508. rule — `reference-semantics/semantics/float.k:180` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fracScale(.IntSeq) => 1
```

## 509. rule — `reference-semantics/semantics/float.k:181` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

## 510. rule — `reference-semantics/semantics/float.k:182` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

## 511. rule — `reference-semantics/semantics/float.k:183` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fscAcc(.IntSeq, A:Int) => A
```

## 512. rule — `reference-semantics/semantics/float.k:184` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

## 513. rule — `reference-semantics/semantics/float.k:185` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

## 514. rule — `reference-semantics/semantics/float.k:186` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

## 515. rule — `reference-semantics/semantics/float.k:187` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

## 516. syntax — `reference-semantics/semantics/float.k:190` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

## 517. rule — `reference-semantics/semantics/float.k:191` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

## 518. rule — `reference-semantics/semantics/float.k:192` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

## 519. syntax — `reference-semantics/semantics/float.k:195` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

## 520. rule — `reference-semantics/semantics/float.k:196` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

## 521. rule — `reference-semantics/semantics/float.k:197` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

## 522. rule — `reference-semantics/semantics/float.k:198` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

## 523. rule — `reference-semantics/semantics/float.k:199` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

## 524. rule — `reference-semantics/semantics/float.k:200` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

## 525. rule — `reference-semantics/semantics/float.k:201` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

## 526. rule — `reference-semantics/semantics/float.k:202` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

## 527. rule — `reference-semantics/semantics/float.k:203` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

## 528. rule — `reference-semantics/semantics/float.k:204` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

## 529. rule — `reference-semantics/semantics/float.k:205` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

## 530. rule — `reference-semantics/semantics/float.k:206` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

## 531. syntax — `reference-semantics/semantics/float.k:209` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

## 532. rule — `reference-semantics/semantics/float.k:210` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

## 533. rule — `reference-semantics/semantics/float.k:211` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

## 534. rule — `reference-semantics/semantics/float.k:213` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

## 535. rule — `reference-semantics/semantics/float.k:214` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

## 536. syntax — `reference-semantics/semantics/float.k:217` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

## 537. rule — `reference-semantics/semantics/float.k:218` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

## 538. syntax — `reference-semantics/semantics/float.k:223` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

## 539. rule — `reference-semantics/semantics/float.k:224` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

## 540. rule — `reference-semantics/semantics/float.k:227` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

## 541. rule — `reference-semantics/semantics/float.k:228` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

## 542. syntax — `reference-semantics/semantics/float.k:230` (module `MPY-FLOAT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

## 543. rule — `reference-semantics/semantics/float.k:231` (module `MPY-FLOAT`)

Attributes/classifiers: concrete

```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

## 544. syntax — `reference-semantics/semantics/float.k:232` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  syntax KItem ::= "#mathSqrt"
```

## 545. rule — `reference-semantics/semantics/float.k:233` (module `MPY-FLOAT`)

Attributes/classifiers: priority

```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

## 546. rule — `reference-semantics/semantics/float.k:234` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

## 547. rule — `reference-semantics/semantics/float.k:235` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

## 548. syntax — `reference-semantics/semantics/float.k:243` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

## 549. rule — `reference-semantics/semantics/float.k:244` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

## 550. rule — `reference-semantics/semantics/float.k:245` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

## 551. rule — `reference-semantics/semantics/float.k:246` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

## 552. rule — `reference-semantics/semantics/float.k:247` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## 553. syntax — `reference-semantics/semantics/float.k:250` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

## 554. rule — `reference-semantics/semantics/float.k:251` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

## 555. rule — `reference-semantics/semantics/float.k:252` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

## 556. rule — `reference-semantics/semantics/float.k:253` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

## 557. rule — `reference-semantics/semantics/float.k:254` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## 558. syntax — `reference-semantics/semantics/float.k:261` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

## 559. rule — `reference-semantics/semantics/float.k:262` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

## 560. rule — `reference-semantics/semantics/float.k:265` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

## 561. rule — `reference-semantics/semantics/float.k:266` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

## 562. rule — `reference-semantics/semantics/float.k:267` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## 563. rule — `reference-semantics/semantics/float.k:270` (module `MPY-FLOAT`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

## 564. syntax — `reference-semantics/semantics/functions.k:8` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

## 565. rule — `reference-semantics/semantics/functions.k:14` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

## 566. syntax — `reference-semantics/semantics/functions.k:18` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

## 567. rule — `reference-semantics/semantics/functions.k:19` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

## 568. syntax — `reference-semantics/semantics/functions.k:27` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

## 569. syntax — `reference-semantics/semantics/functions.k:31` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

## 570. rule — `reference-semantics/semantics/functions.k:33` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

## 571. rule — `reference-semantics/semantics/functions.k:36` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

## 572. rule — `reference-semantics/semantics/functions.k:42` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

## 573. rule — `reference-semantics/semantics/functions.k:47` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

## 574. rule — `reference-semantics/semantics/functions.k:50` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

## 575. rule — `reference-semantics/semantics/functions.k:53` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

## 576. rule — `reference-semantics/semantics/functions.k:59` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

## 577. rule — `reference-semantics/semantics/functions.k:63` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

## 578. rule — `reference-semantics/semantics/functions.k:64` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

## 579. rule — `reference-semantics/semantics/functions.k:68` (module `MPY-FUNCTIONS`)

Attributes/classifiers: priority

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

## 580. rule — `reference-semantics/semantics/functions.k:78` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

## 581. rule — `reference-semantics/semantics/functions.k:80` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

## 582. rule — `reference-semantics/semantics/functions.k:85` (module `MPY-FUNCTIONS`)

Attributes/classifiers: none

```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## 583. rule — `reference-semantics/semantics/int.k:7` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyUn("-", I:Int) => 0 -Int I
```

## 584. rule — `reference-semantics/semantics/int.k:9` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

## 585. rule — `reference-semantics/semantics/int.k:11` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

## 586. rule — `reference-semantics/semantics/int.k:12` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

## 587. rule — `reference-semantics/semantics/int.k:13` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

## 588. rule — `reference-semantics/semantics/int.k:14` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

## 589. rule — `reference-semantics/semantics/int.k:15` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

## 590. rule — `reference-semantics/semantics/int.k:16` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

## 591. rule — `reference-semantics/semantics/int.k:17` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

## 592. syntax — `reference-semantics/semantics/int.k:19` (module `MPY-INT`)

Attributes/classifiers: function

```k
  syntax Int ::= pyMod(Int, Int) [function]
```

## 593. rule — `reference-semantics/semantics/int.k:20` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

## 594. rule — `reference-semantics/semantics/int.k:22` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

## 595. rule — `reference-semantics/semantics/int.k:23` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

## 596. rule — `reference-semantics/semantics/int.k:24` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

## 597. rule — `reference-semantics/semantics/int.k:25` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

## 598. rule — `reference-semantics/semantics/int.k:26` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

## 599. rule — `reference-semantics/semantics/int.k:27` (module `MPY-INT`)

Attributes/classifiers: none

```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## 600. syntax — `reference-semantics/semantics/iter.k:8` (module `MPY-ITER`)

Attributes/classifiers: none

```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## 601. rule — `reference-semantics/semantics/list.k:9` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

## 602. rule — `reference-semantics/semantics/list.k:10` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

## 603. syntax — `reference-semantics/semantics/list.k:13` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  syntax ApplyK ::= "toList"
```

## 604. rule — `reference-semantics/semantics/list.k:14` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

## 605. rule — `reference-semantics/semantics/list.k:15` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

## 606. syntax — `reference-semantics/semantics/list.k:18` (module `MPY-LIST`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

## 607. rule — `reference-semantics/semantics/list.k:19` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

## 608. rule — `reference-semantics/semantics/list.k:20` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

## 609. rule — `reference-semantics/semantics/list.k:24` (module `MPY-LIST`)

Attributes/classifiers: priority

```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

## 610. rule — `reference-semantics/semantics/list.k:27` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

## 611. rule — `reference-semantics/semantics/list.k:28` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

## 612. syntax — `reference-semantics/semantics/list.k:33` (module `MPY-LIST`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

## 613. rule — `reference-semantics/semantics/list.k:34` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule hasRefVS(.ValSeq)                => false
```

## 614. rule — `reference-semantics/semantics/list.k:35` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

## 615. syntax — `reference-semantics/semantics/list.k:37` (module `MPY-LIST`)

Attributes/classifiers: function

```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

## 616. rule — `reference-semantics/semantics/list.k:39` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

## 617. rule — `reference-semantics/semantics/list.k:40` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

## 618. rule — `reference-semantics/semantics/list.k:41` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

## 619. rule — `reference-semantics/semantics/list.k:42` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

## 620. rule — `reference-semantics/semantics/list.k:45` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

## 621. rule — `reference-semantics/semantics/list.k:47` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

## 622. rule — `reference-semantics/semantics/list.k:49` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

## 623. rule — `reference-semantics/semantics/list.k:50` (module `MPY-LIST`)

Attributes/classifiers: owise

```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

## 624. rule — `reference-semantics/semantics/list.k:53` (module `MPY-LIST`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

## 625. syntax — `reference-semantics/semantics/list.k:58` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

## 626. rule — `reference-semantics/semantics/list.k:59` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

## 627. rule — `reference-semantics/semantics/list.k:60` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

## 628. rule — `reference-semantics/semantics/list.k:61` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

## 629. rule — `reference-semantics/semantics/list.k:62` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

## 630. rule — `reference-semantics/semantics/list.k:63` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

## 631. rule — `reference-semantics/semantics/list.k:65` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

## 632. rule — `reference-semantics/semantics/list.k:67` (module `MPY-LIST`)

Attributes/classifiers: none

```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## 633. syntax — `reference-semantics/semantics/methods.k:10` (module `MPY-METHODS`)

Attributes/classifiers: function

```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

## 634. rule — `reference-semantics/semantics/methods.k:13` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

## 635. rule — `reference-semantics/semantics/methods.k:14` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

## 636. rule — `reference-semantics/semantics/methods.k:15` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

## 637. rule — `reference-semantics/semantics/methods.k:16` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

## 638. rule — `reference-semantics/semantics/methods.k:19` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

## 639. rule — `reference-semantics/semantics/methods.k:20` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

## 640. rule — `reference-semantics/semantics/methods.k:21` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

## 641. rule — `reference-semantics/semantics/methods.k:26` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

## 642. syntax — `reference-semantics/semantics/methods.k:27` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

## 643. rule — `reference-semantics/semantics/methods.k:28` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

## 644. rule — `reference-semantics/semantics/methods.k:29` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

## 645. rule — `reference-semantics/semantics/methods.k:30` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

## 646. rule — `reference-semantics/semantics/methods.k:34` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

## 647. syntax — `reference-semantics/semantics/methods.k:35` (module `MPY-METHODS`)

Attributes/classifiers: function

```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

## 648. rule — `reference-semantics/semantics/methods.k:36` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

## 649. rule — `reference-semantics/semantics/methods.k:37` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

## 650. rule — `reference-semantics/semantics/methods.k:39` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

## 651. syntax — `reference-semantics/semantics/methods.k:41` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

## 652. rule — `reference-semantics/semantics/methods.k:42` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

## 653. rule — `reference-semantics/semantics/methods.k:43` (module `MPY-METHODS`)

Attributes/classifiers: owise

```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

## 654. rule — `reference-semantics/semantics/methods.k:44` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

## 655. rule — `reference-semantics/semantics/methods.k:47` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

## 656. syntax — `reference-semantics/semantics/methods.k:48` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

## 657. rule — `reference-semantics/semantics/methods.k:49` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule trimWS(.IntSeq) => .IntSeq
```

## 658. rule — `reference-semantics/semantics/methods.k:50` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

## 659. rule — `reference-semantics/semantics/methods.k:51` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

## 660. syntax — `reference-semantics/semantics/methods.k:52` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

## 661. rule — `reference-semantics/semantics/methods.k:53` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

## 662. rule — `reference-semantics/semantics/methods.k:54` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

## 663. rule — `reference-semantics/semantics/methods.k:55` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

## 664. rule — `reference-semantics/semantics/methods.k:58` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

## 665. rule — `reference-semantics/semantics/methods.k:61` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

## 666. rule — `reference-semantics/semantics/methods.k:64` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

## 667. syntax — `reference-semantics/semantics/methods.k:65` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

## 668. rule — `reference-semantics/semantics/methods.k:66` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

## 669. rule — `reference-semantics/semantics/methods.k:67` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

## 670. rule — `reference-semantics/semantics/methods.k:68` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

## 671. rule — `reference-semantics/semantics/methods.k:72` (module `MPY-METHODS`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

## 672. syntax — `reference-semantics/semantics/methods.k:75` (module `MPY-METHODS`)

Attributes/classifiers: function

```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

## 673. rule — `reference-semantics/semantics/methods.k:76` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

## 674. rule — `reference-semantics/semantics/methods.k:77` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

## 675. rule — `reference-semantics/semantics/methods.k:79` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

## 676. syntax — `reference-semantics/semantics/methods.k:82` (module `MPY-METHODS`)

Attributes/classifiers: function

```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

## 677. rule — `reference-semantics/semantics/methods.k:83` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

## 678. rule — `reference-semantics/semantics/methods.k:84` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

## 679. syntax — `reference-semantics/semantics/methods.k:85` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= isWSC(Int) [function, total]
```

## 680. rule — `reference-semantics/semantics/methods.k:86` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

## 681. rule — `reference-semantics/semantics/methods.k:89` (module `MPY-METHODS`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

## 682. rule — `reference-semantics/semantics/methods.k:94` (module `MPY-METHODS`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

## 683. syntax — `reference-semantics/semantics/methods.k:97` (module `MPY-METHODS`)

Attributes/classifiers: function

```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

## 684. rule — `reference-semantics/semantics/methods.k:98` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

## 685. rule — `reference-semantics/semantics/methods.k:99` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

## 686. rule — `reference-semantics/semantics/methods.k:101` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

## 687. rule — `reference-semantics/semantics/methods.k:104` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

## 688. syntax — `reference-semantics/semantics/methods.k:106` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

## 689. rule — `reference-semantics/semantics/methods.k:107` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

## 690. rule — `reference-semantics/semantics/methods.k:108` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

## 691. rule — `reference-semantics/semantics/methods.k:109` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

## 692. syntax — `reference-semantics/semantics/methods.k:112` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

## 693. rule — `reference-semantics/semantics/methods.k:113` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

## 694. syntax — `reference-semantics/semantics/methods.k:115` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

## 695. rule — `reference-semantics/semantics/methods.k:116` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

## 696. syntax — `reference-semantics/semantics/methods.k:118` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

## 697. rule — `reference-semantics/semantics/methods.k:119` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

## 698. syntax — `reference-semantics/semantics/methods.k:121` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

## 699. rule — `reference-semantics/semantics/methods.k:122` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

## 700. syntax — `reference-semantics/semantics/methods.k:124` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

## 701. rule — `reference-semantics/semantics/methods.k:125` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule hasUpper(.IntSeq) => false
```

## 702. rule — `reference-semantics/semantics/methods.k:126` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

## 703. syntax — `reference-semantics/semantics/methods.k:128` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

## 704. rule — `reference-semantics/semantics/methods.k:129` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule hasLower(.IntSeq) => false
```

## 705. rule — `reference-semantics/semantics/methods.k:130` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

## 706. syntax — `reference-semantics/semantics/methods.k:132` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

## 707. rule — `reference-semantics/semantics/methods.k:133` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule allAlpha(.IntSeq) => true
```

## 708. rule — `reference-semantics/semantics/methods.k:134` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

## 709. syntax — `reference-semantics/semantics/methods.k:136` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

## 710. rule — `reference-semantics/semantics/methods.k:137` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule allDigit(.IntSeq) => true
```

## 711. rule — `reference-semantics/semantics/methods.k:138` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

## 712. syntax — `reference-semantics/semantics/methods.k:140` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Int ::= lowerC(Int) [function, total]
```

## 713. rule — `reference-semantics/semantics/methods.k:142` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

## 714. rule — `reference-semantics/semantics/methods.k:143` (module `MPY-METHODS`)

Attributes/classifiers: owise

```k
  rule lowerC(C:Int) => C         [owise]
```

## 715. syntax — `reference-semantics/semantics/methods.k:145` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Int ::= upperC(Int) [function, total]
```

## 716. rule — `reference-semantics/semantics/methods.k:146` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

## 717. rule — `reference-semantics/semantics/methods.k:147` (module `MPY-METHODS`)

Attributes/classifiers: owise

```k
  rule upperC(C:Int) => C         [owise]
```

## 718. syntax — `reference-semantics/semantics/methods.k:149` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Int ::= swapC(Int) [function, total]
```

## 719. rule — `reference-semantics/semantics/methods.k:150` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

## 720. rule — `reference-semantics/semantics/methods.k:151` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

## 721. rule — `reference-semantics/semantics/methods.k:152` (module `MPY-METHODS`)

Attributes/classifiers: owise

```k
  rule swapC(C:Int) => C         [owise]
```

## 722. syntax — `reference-semantics/semantics/methods.k:154` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

## 723. rule — `reference-semantics/semantics/methods.k:155` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule mapLower(.IntSeq) => .IntSeq
```

## 724. rule — `reference-semantics/semantics/methods.k:156` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

## 725. syntax — `reference-semantics/semantics/methods.k:158` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

## 726. rule — `reference-semantics/semantics/methods.k:159` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule mapUpper(.IntSeq) => .IntSeq
```

## 727. rule — `reference-semantics/semantics/methods.k:160` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

## 728. syntax — `reference-semantics/semantics/methods.k:162` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

## 729. rule — `reference-semantics/semantics/methods.k:163` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule mapSwap(.IntSeq) => .IntSeq
```

## 730. rule — `reference-semantics/semantics/methods.k:164` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

## 731. syntax — `reference-semantics/semantics/methods.k:166` (module `MPY-METHODS`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

## 732. rule — `reference-semantics/semantics/methods.k:167` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

## 733. rule — `reference-semantics/semantics/methods.k:168` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## 734. rule — `reference-semantics/semantics/methods.k:169` (module `MPY-METHODS`)

Attributes/classifiers: none

```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## 735. rule — `reference-semantics/semantics/operators.k:10` (module `MPY-OPERATORS`)

Attributes/classifiers: none

```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

## 736. rule — `reference-semantics/semantics/operators.k:12` (module `MPY-OPERATORS`)

Attributes/classifiers: none

```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

## 737. context — `reference-semantics/semantics/operators.k:15` (module `MPY-OPERATORS`)

Attributes/classifiers: none

```k
  context Compare(HOLE, _)
```

## 738. context — `reference-semantics/semantics/operators.k:16` (module `MPY-OPERATORS`)

Attributes/classifiers: none

```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

## 739. rule — `reference-semantics/semantics/operators.k:17` (module `MPY-OPERATORS`)

Attributes/classifiers: owise

```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

## 740. rule — `reference-semantics/semantics/operators.k:19` (module `MPY-OPERATORS`)

Attributes/classifiers: none

```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

## 741. rule — `reference-semantics/semantics/operators.k:20` (module `MPY-OPERATORS`)

Attributes/classifiers: none

```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

## 742. rule — `reference-semantics/semantics/operators.k:25` (module `MPY-OPERATORS`)

Attributes/classifiers: priority

```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 743. rule — `reference-semantics/semantics/operators.k:28` (module `MPY-OPERATORS`)

Attributes/classifiers: priority

```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

## 744. rule — `reference-semantics/semantics/operators.k:34` (module `MPY-OPERATORS`)

Attributes/classifiers: priority

```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

## 745. rule — `reference-semantics/semantics/operators.k:38` (module `MPY-OPERATORS`)

Attributes/classifiers: priority

```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

## 746. rule — `reference-semantics/semantics/operators.k:44` (module `MPY-OPERATORS`)

Attributes/classifiers: priority

```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 747. syntax — `reference-semantics/semantics/range.k:9` (module `MPY-RANGE`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

## 748. rule — `reference-semantics/semantics/range.k:10` (module `MPY-RANGE`)

Attributes/classifiers: none

```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

## 749. syntax — `reference-semantics/semantics/range.k:12` (module `MPY-RANGE`)

Attributes/classifiers: function

```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

## 750. rule — `reference-semantics/semantics/range.k:13` (module `MPY-RANGE`)

Attributes/classifiers: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

## 751. rule — `reference-semantics/semantics/range.k:15` (module `MPY-RANGE`)

Attributes/classifiers: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

## 752. rule — `reference-semantics/semantics/range.k:17` (module `MPY-RANGE`)

Attributes/classifiers: none

```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

## 753. rule — `reference-semantics/semantics/range.k:20` (module `MPY-RANGE`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

## 754. rule — `reference-semantics/semantics/range.k:23` (module `MPY-RANGE`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

## 755. syntax — `reference-semantics/semantics/set.k:8` (module `MPY-SET`)

Attributes/classifiers: none

```k
  syntax Val ::= setV(IntSeq)
```

## 756. syntax — `reference-semantics/semantics/set.k:11` (module `MPY-SET`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

## 757. rule — `reference-semantics/semantics/set.k:12` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule codeIn(_:Int, .IntSeq)                => false
```

## 758. rule — `reference-semantics/semantics/set.k:13` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

## 759. syntax — `reference-semantics/semantics/set.k:16` (module `MPY-SET`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

## 760. rule — `reference-semantics/semantics/set.k:18` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

## 761. rule — `reference-semantics/semantics/set.k:19` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

## 762. rule — `reference-semantics/semantics/set.k:20` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

## 763. rule — `reference-semantics/semantics/set.k:22` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

## 764. syntax — `reference-semantics/semantics/set.k:25` (module `MPY-SET`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

## 765. rule — `reference-semantics/semantics/set.k:26` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

## 766. rule — `reference-semantics/semantics/set.k:27` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

## 767. syntax — `reference-semantics/semantics/set.k:31` (module `MPY-SET`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

## 768. rule — `reference-semantics/semantics/set.k:32` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

## 769. rule — `reference-semantics/semantics/set.k:33` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

## 770. syntax — `reference-semantics/semantics/set.k:35` (module `MPY-SET`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

## 771. rule — `reference-semantics/semantics/set.k:36` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

## 772. rule — `reference-semantics/semantics/set.k:39` (module `MPY-SET`)

Attributes/classifiers: none

```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## 773. syntax — `reference-semantics/semantics/sort.k:18` (module `MPY-SORT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

## 774. syntax — `reference-semantics/semantics/sort.k:19` (module `MPY-SORT`)

Attributes/classifiers: function

```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

## 775. rule — `reference-semantics/semantics/sort.k:20` (module `MPY-SORT`)

Attributes/classifiers: concrete

```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

## 776. rule — `reference-semantics/semantics/sort.k:21` (module `MPY-SORT`)

Attributes/classifiers: concrete

```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

## 777. rule — `reference-semantics/semantics/sort.k:22` (module `MPY-SORT`)

Attributes/classifiers: concrete

```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

## 778. rule — `reference-semantics/semantics/sort.k:23` (module `MPY-SORT`)

Attributes/classifiers: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

## 779. rule — `reference-semantics/semantics/sort.k:24` (module `MPY-SORT`)

Attributes/classifiers: concrete

```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

## 780. syntax — `reference-semantics/semantics/sort.k:26` (module `MPY-SORT`)

Attributes/classifiers: function

```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

## 781. rule — `reference-semantics/semantics/sort.k:27` (module `MPY-SORT`)

Attributes/classifiers: concrete

```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

## 782. rule — `reference-semantics/semantics/sort.k:28` (module `MPY-SORT`)

Attributes/classifiers: concrete

```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

## 783. rule — `reference-semantics/semantics/sort.k:29` (module `MPY-SORT`)

Attributes/classifiers: concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

## 784. rule — `reference-semantics/semantics/sort.k:31` (module `MPY-SORT`)

Attributes/classifiers: concrete

```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

## 785. rule — `reference-semantics/semantics/sort.k:36` (module `MPY-SORT`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

## 786. rule — `reference-semantics/semantics/sort.k:40` (module `MPY-SORT`)

Attributes/classifiers: priority

```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

## 787. syntax — `reference-semantics/semantics/sort.k:49` (module `MPY-SORT`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

## 788. syntax — `reference-semantics/semantics/sort.k:51` (module `MPY-SORT`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

## 789. rule — `reference-semantics/semantics/sort.k:53` (module `MPY-SORT`)

Attributes/classifiers: none

```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

## 790. rule — `reference-semantics/semantics/sort.k:54` (module `MPY-SORT`)

Attributes/classifiers: none

```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

## 791. rule — `reference-semantics/semantics/sort.k:55` (module `MPY-SORT`)

Attributes/classifiers: none

```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

## 792. syntax — `reference-semantics/semantics/sort.k:57` (module `MPY-SORT`)

Attributes/classifiers: function, total

```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

## 793. rule — `reference-semantics/semantics/sort.k:58` (module `MPY-SORT`)

Attributes/classifiers: none

```k
  rule condRev(S:ValSeq, false) => S
```

## 794. rule — `reference-semantics/semantics/sort.k:59` (module `MPY-SORT`)

Attributes/classifiers: none

```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

## 795. rule — `reference-semantics/semantics/sort.k:61` (module `MPY-SORT`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

## 796. rule — `reference-semantics/semantics/sort.k:63` (module `MPY-SORT`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

## 797. rule — `reference-semantics/semantics/sort.k:65` (module `MPY-SORT`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

## 798. rule — `reference-semantics/semantics/str.k:8` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

## 799. rule — `reference-semantics/semantics/str.k:9` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

## 800. syntax — `reference-semantics/semantics/str.k:13` (module `MPY-STR`)

Attributes/classifiers: function

```k
  syntax IntSeq ::= strToCodes(String) [function]
```

## 801. rule — `reference-semantics/semantics/str.k:14` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

## 802. rule — `reference-semantics/semantics/str.k:15` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strToCodes("") => .IntSeq
```

## 803. rule — `reference-semantics/semantics/str.k:16` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

## 804. syntax — `reference-semantics/semantics/str.k:20` (module `MPY-STR`)

Attributes/classifiers: function, total

```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

## 805. rule — `reference-semantics/semantics/str.k:21` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

## 806. rule — `reference-semantics/semantics/str.k:22` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

## 807. rule — `reference-semantics/semantics/str.k:24` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

## 808. rule — `reference-semantics/semantics/str.k:25` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

## 809. rule — `reference-semantics/semantics/str.k:26` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

## 810. rule — `reference-semantics/semantics/str.k:29` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

## 811. rule — `reference-semantics/semantics/str.k:30` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

## 812. syntax — `reference-semantics/semantics/str.k:32` (module `MPY-STR`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

## 813. rule — `reference-semantics/semantics/str.k:33` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

## 814. rule — `reference-semantics/semantics/str.k:34` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## 815. rule — `reference-semantics/semantics/str.k:35` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

## 816. syntax — `reference-semantics/semantics/str.k:37` (module `MPY-STR`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

## 817. rule — `reference-semantics/semantics/str.k:38` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

## 818. rule — `reference-semantics/semantics/str.k:39` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

## 819. rule — `reference-semantics/semantics/str.k:40` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

## 820. syntax — `reference-semantics/semantics/str.k:48` (module `MPY-STR`)

Attributes/classifiers: function, total

```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

## 821. rule — `reference-semantics/semantics/str.k:49` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

## 822. rule — `reference-semantics/semantics/str.k:50` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

## 823. rule — `reference-semantics/semantics/str.k:51` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## 824. rule — `reference-semantics/semantics/str.k:52` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

## 825. rule — `reference-semantics/semantics/str.k:53` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

## 826. rule — `reference-semantics/semantics/str.k:54` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

## 827. rule — `reference-semantics/semantics/str.k:56` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

## 828. rule — `reference-semantics/semantics/str.k:57` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

## 829. rule — `reference-semantics/semantics/str.k:58` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

## 830. rule — `reference-semantics/semantics/str.k:59` (module `MPY-STR`)

Attributes/classifiers: none

```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## 831. syntax — `reference-semantics/semantics/subscript.k:11` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function, total

```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

## 832. rule — `reference-semantics/semantics/subscript.k:12` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

## 833. rule — `reference-semantics/semantics/subscript.k:13` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

## 834. syntax — `reference-semantics/semantics/subscript.k:16` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function

```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

## 835. rule — `reference-semantics/semantics/subscript.k:17` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

## 836. rule — `reference-semantics/semantics/subscript.k:18` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

## 837. syntax — `reference-semantics/semantics/subscript.k:21` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function, total

```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

## 838. rule — `reference-semantics/semantics/subscript.k:22` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

## 839. rule — `reference-semantics/semantics/subscript.k:23` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

## 840. context — `reference-semantics/semantics/subscript.k:27` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  context Subscript(HOLE, _)
```

## 841. context — `reference-semantics/semantics/subscript.k:28` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  context Subscript(_:Val, HOLE:Expr)
```

## 842. rule — `reference-semantics/semantics/subscript.k:31` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: priority

```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 843. rule — `reference-semantics/semantics/subscript.k:35` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

## 844. syntax — `reference-semantics/semantics/subscript.k:37` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function

```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

## 845. rule — `reference-semantics/semantics/subscript.k:38` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

## 846. rule — `reference-semantics/semantics/subscript.k:39` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

## 847. rule — `reference-semantics/semantics/subscript.k:40` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

## 848. syntax — `reference-semantics/semantics/subscript.k:44` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

## 849. syntax — `reference-semantics/semantics/subscript.k:49` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  syntax OptInt ::= "noB" | someB(Int)
```

## 850. rule — `reference-semantics/semantics/subscript.k:50` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

## 851. rule — `reference-semantics/semantics/subscript.k:51` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

## 852. rule — `reference-semantics/semantics/subscript.k:52` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

## 853. rule — `reference-semantics/semantics/subscript.k:54` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

## 854. rule — `reference-semantics/semantics/subscript.k:55` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

## 855. rule — `reference-semantics/semantics/subscript.k:56` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

## 856. rule — `reference-semantics/semantics/subscript.k:58` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: priority

```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

## 857. rule — `reference-semantics/semantics/subscript.k:61` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

## 858. syntax — `reference-semantics/semantics/subscript.k:63` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function

```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

## 859. rule — `reference-semantics/semantics/subscript.k:64` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

## 860. rule — `reference-semantics/semantics/subscript.k:66` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

## 861. rule — `reference-semantics/semantics/subscript.k:68` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

## 862. syntax — `reference-semantics/semantics/subscript.k:72` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function, total

```k
  syntax Int ::= slStep(OptInt) [function, total]
```

## 863. rule — `reference-semantics/semantics/subscript.k:73` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slStep(noB)          => 1
```

## 864. rule — `reference-semantics/semantics/subscript.k:74` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slStep(someB(S:Int)) => S
```

## 865. syntax — `reference-semantics/semantics/subscript.k:76` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function

```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

## 866. rule — `reference-semantics/semantics/subscript.k:77` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

## 867. rule — `reference-semantics/semantics/subscript.k:79` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

## 868. rule — `reference-semantics/semantics/subscript.k:81` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

## 869. syntax — `reference-semantics/semantics/subscript.k:83` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function

```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

## 870. rule — `reference-semantics/semantics/subscript.k:84` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

## 871. rule — `reference-semantics/semantics/subscript.k:86` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

## 872. rule — `reference-semantics/semantics/subscript.k:88` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

## 873. syntax — `reference-semantics/semantics/subscript.k:90` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function, total

```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

## 874. rule — `reference-semantics/semantics/subscript.k:91` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

## 875. rule — `reference-semantics/semantics/subscript.k:93` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

## 876. syntax — `reference-semantics/semantics/subscript.k:96` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function, total

```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

## 877. rule — `reference-semantics/semantics/subscript.k:97` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

## 878. rule — `reference-semantics/semantics/subscript.k:99` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

## 879. syntax — `reference-semantics/semantics/subscript.k:102` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function, total

```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

## 880. rule — `reference-semantics/semantics/subscript.k:103` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

## 881. rule — `reference-semantics/semantics/subscript.k:105` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

## 882. syntax — `reference-semantics/semantics/subscript.k:109` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function

```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

## 883. rule — `reference-semantics/semantics/subscript.k:110` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

## 884. rule — `reference-semantics/semantics/subscript.k:113` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## 885. syntax — `reference-semantics/semantics/subscript.k:116` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: function

```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

## 886. rule — `reference-semantics/semantics/subscript.k:117` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

## 887. rule — `reference-semantics/semantics/subscript.k:120` (module `MPY-SUBSCRIPT`)

Attributes/classifiers: none

```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## 888. syntax — `reference-semantics/semantics/syntax.k:9` (module `MPY-SYNTAX`)

Attributes/classifiers: strict, seqstrict, macro

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

## 889. syntax — `reference-semantics/semantics/syntax.k:32` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

## 890. syntax — `reference-semantics/semantics/syntax.k:33` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

## 891. syntax — `reference-semantics/semantics/syntax.k:34` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax Entries  ::= List{Entry, ","}
```

## 892. syntax — `reference-semantics/semantics/syntax.k:35` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

## 893. syntax — `reference-semantics/semantics/syntax.k:36` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax CompFors ::= List{CompFor, ""}
```

## 894. syntax — `reference-semantics/semantics/syntax.k:37` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax Exprs    ::= List{Expr, ","}
```

## 895. syntax — `reference-semantics/semantics/syntax.k:38` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

## 896. syntax — `reference-semantics/semantics/syntax.k:39` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax Bound    ::= Expr | "NoBound"
```

## 897. syntax — `reference-semantics/semantics/syntax.k:41` (module `MPY-SYNTAX`)

Attributes/classifiers: strict

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

## 898. syntax — `reference-semantics/semantics/syntax.k:56` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax Stmts      ::= List{Stmt, ""}
```

## 899. syntax — `reference-semantics/semantics/syntax.k:57` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

## 900. syntax — `reference-semantics/semantics/syntax.k:58` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

## 901. syntax — `reference-semantics/semantics/syntax.k:59` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

## 902. syntax — `reference-semantics/semantics/syntax.k:60` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax ParamNames ::= List{String, ","}
```

## 903. syntax — `reference-semantics/semantics/syntax.k:61` (module `MPY-SYNTAX`)

Attributes/classifiers: none

```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## 904. rule — `reference-semantics/semantics/tuple.k:10` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

## 905. rule — `reference-semantics/semantics/tuple.k:11` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

## 906. syntax — `reference-semantics/semantics/tuple.k:14` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  syntax ApplyK ::= "toTuple"
```

## 907. rule — `reference-semantics/semantics/tuple.k:15` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

## 908. rule — `reference-semantics/semantics/tuple.k:16` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

## 909. rule — `reference-semantics/semantics/tuple.k:18` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

## 910. rule — `reference-semantics/semantics/tuple.k:20` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

## 911. rule — `reference-semantics/semantics/tuple.k:21` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

## 912. rule — `reference-semantics/semantics/tuple.k:23` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

## 913. syntax — `reference-semantics/semantics/tuple.k:24` (module `MPY-TUPLE`)

Attributes/classifiers: function

```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

## 914. rule — `reference-semantics/semantics/tuple.k:25` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

## 915. rule — `reference-semantics/semantics/tuple.k:26` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

## 916. rule — `reference-semantics/semantics/tuple.k:28` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

## 917. syntax — `reference-semantics/semantics/tuple.k:31` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

## 918. rule — `reference-semantics/semantics/tuple.k:32` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

## 919. rule — `reference-semantics/semantics/tuple.k:35` (module `MPY-TUPLE`)

Attributes/classifiers: priority

```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

## 920. rule — `reference-semantics/semantics/tuple.k:42` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

## 921. rule — `reference-semantics/semantics/tuple.k:43` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

## 922. rule — `reference-semantics/semantics/tuple.k:44` (module `MPY-TUPLE`)

Attributes/classifiers: priority

```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 923. syntax — `reference-semantics/semantics/tuple.k:49` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

## 924. rule — `reference-semantics/semantics/tuple.k:50` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

## 925. rule — `reference-semantics/semantics/tuple.k:51` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

## 926. rule — `reference-semantics/semantics/tuple.k:52` (module `MPY-TUPLE`)

Attributes/classifiers: priority

```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 927. rule — `reference-semantics/semantics/tuple.k:55` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

## 928. rule — `reference-semantics/semantics/tuple.k:57` (module `MPY-TUPLE`)

Attributes/classifiers: none

```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## 929. syntax — `verification.k:9` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax Bool ::= noDivisor(Int, Int, Int)
    [function, total, symbol(noDivisor), no-evaluators]
```

## 930. rule — `verification.k:11` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: none

```k
  rule noDivisor(_:Int, D:Int, HI:Int) => true
    requires D >=Int HI
```

## 931. rule — `verification.k:13` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: none

```k
  rule noDivisor(C:Int, D:Int, HI:Int) => false
    requires D <Int HI andBool pyMod(C, D) ==Int 0
```

## 932. rule — `verification.k:15` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: none

```k
  rule noDivisor(C:Int, D:Int, HI:Int)
    => noDivisor(C, D +Int 1, HI)
    requires D <Int HI andBool pyMod(C, D) =/=Int 0
```

## 933. syntax — `verification.k:20` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= appendIfPrime(ValSeq, Int, Bool)
    [function, total, symbol(appendIfPrime), no-evaluators]
```

## 934. rule — `verification.k:22` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: none

```k
  rule appendIfPrime(VS:ValSeq, _:Int, false) => VS
```

## 935. rule — `verification.k:23` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: none

```k
  rule appendIfPrime(VS:ValSeq, I:Int, true)
    => valSeqConcat(VS, vCons(I, .ValSeq))
```

## 936. syntax — `verification.k:29` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: function, total, symbol, no-evaluators

```k
  syntax ValSeq ::= primesAcc(ValSeq, Int, Int)
    [function, total, symbol(primesAcc), no-evaluators]
```

## 937. rule — `verification.k:31` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: none

```k
  rule primesAcc(VS:ValSeq, I:Int, N:Int) => VS
    requires I >=Int N
```

## 938. rule — `verification.k:33` (module `COUNT-UP-TO-BASE`)

Attributes/classifiers: none

```k
  rule primesAcc(VS:ValSeq, I:Int, N:Int)
    => primesAcc(
         appendIfPrime(VS, I, noDivisor(I, 2, I)),
         I +Int 1,
         N)
    requires I <Int N
```

## 939. rule — `verification.k:46` (module `COUNT-UP-TO-WITH-INNER`)

Attributes/classifiers: priority

```k
  rule <k>
         #while(
           Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
           If(
             Compare(
               BinOp("%", Name("candidate"), Name("divisor")),
               CmpOp("==", Int(0))),
             Assign(Name("is_prime"), Bool(false)),
             .Stmts)
           AugAssign(Name("divisor"), "+", Int(1)))
         => .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         0 |-> scope(MOD:Map, parent(-1))
         -1 |-> scope(BI:Map, root)
         1 |-> scope(
           ("candidate" |-> C:Int
            "divisor" |-> (D:Int => C)
            "is_prime" |-> (B:Bool => B andBool noDivisor(C, D, C))
            "n" |-> N:Int
            "result" |-> ref(0)),
           parent(0))
       </scopes>
       <heap> 0 |-> list(VS:ValSeq) </heap>
       requires 2 <=Int D andBool D <=Int C
       [priority(40)]
```

## 940. rule — `verification.k:82` (module `COUNT-UP-TO-WITH-OUTER`)

Attributes/classifiers: priority

```k
  rule <k>
         #while(
           Compare(Name("candidate"), CmpOp("<", Name("n"))),
           While(
             Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
             If(
               Compare(
                 BinOp("%", Name("candidate"), Name("divisor")),
                 CmpOp("==", Int(0))),
               Assign(Name("is_prime"), Bool(false)),
               .Stmts)
             AugAssign(Name("divisor"), "+", Int(1)))
           If(
             Name("is_prime"),
             Expr(Call(
               Attribute(Name("result"), "append"),
               Name("candidate"))),
             .Stmts)
           AugAssign(Name("candidate"), "+", Int(1))
           Assign(Name("is_prime"), Bool(true))
           Assign(Name("divisor"), Int(2)))
         => .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         0 |-> scope(MOD:Map, parent(-1))
         -1 |-> scope(BI:Map, root)
         1 |-> scope(
           ("n" |-> N:Int
            "candidate" |-> (I:Int => N)
            "is_prime" |-> true
            "divisor" |-> 2
            "result" |-> ref(0)),
           parent(0))
       </scopes>
       <heap>
         0 |-> (list(VS:ValSeq) => list(primesAcc(VS, I, N)))
       </heap>
       requires 2 <=Int I andBool I <=Int N
       [priority(40)]
```

## 941. claim — `spec.k:8` (module `COUNT-UP-TO-INNER-LOOP-SPEC`)

Attributes/classifiers: none

```k
  claim
    <k>
      #while(
        Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
        If(
          Compare(
            BinOp("%", Name("candidate"), Name("divisor")),
            CmpOp("==", Int(0))),
          Assign(Name("is_prime"), Bool(false)),
          .Stmts)
        AugAssign(Name("divisor"), "+", Int(1)))
    => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(MOD:Map, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        ("candidate" |-> C:Int
         "divisor" |-> (D:Int => C)
         "is_prime" |-> (B:Bool => B andBool noDivisor(C, D, C))
         "n" |-> N:Int
         "result" |-> ref(0)),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(VS:ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ST:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires 2 <=Int D andBool D <=Int C
```

## 942. claim — `spec.k:48` (module `COUNT-UP-TO-OUTER-LOOP-SPEC`)

Attributes/classifiers: none

```k
  claim
    <k>
      #while(
        Compare(Name("candidate"), CmpOp("<", Name("n"))),
        While(
          Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
          If(
            Compare(
              BinOp("%", Name("candidate"), Name("divisor")),
              CmpOp("==", Int(0))),
            Assign(Name("is_prime"), Bool(false)),
            .Stmts)
          AugAssign(Name("divisor"), "+", Int(1)))
        If(
          Name("is_prime"),
          Expr(Call(
            Attribute(Name("result"), "append"),
            Name("candidate"))),
          .Stmts)
        AugAssign(Name("candidate"), "+", Int(1))
        Assign(Name("is_prime"), Bool(true))
        Assign(Name("divisor"), Int(2)))
    => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(MOD:Map, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        ("n" |-> N:Int
         "candidate" |-> (I:Int => N)
         "is_prime" |-> true
         "divisor" |-> 2
         "result" |-> ref(0)),
        parent(0))
    </scopes>
    <heap>
      0 |-> (list(VS:ValSeq) => list(primesAcc(VS, I, N)))
    </heap>
    <scopeLoc> 2 </scopeLoc>
    <heapLoc> 1 </heapLoc>
    <stack> ST:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires 2 <=Int I andBool I <=Int N
```

## 943. claim — `spec.k:101` (module `COUNT-UP-TO-ENTRY-SPEC`)

Attributes/classifiers: none

```k
  claim
    <k>
      Assign(Name("result"), ListExpr(.Exprs))
      Assign(Name("candidate"), Int(2))
      Assign(Name("is_prime"), Bool(true))
      Assign(Name("divisor"), Int(2))
      While(
        Compare(Name("candidate"), CmpOp("<", Name("n"))),
        While(
          Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
          If(
            Compare(
              BinOp("%", Name("candidate"), Name("divisor")),
              CmpOp("==", Int(0))),
            Assign(Name("is_prime"), Bool(false)),
            .Stmts)
          AugAssign(Name("divisor"), "+", Int(1)))
        If(
          Name("is_prime"),
          Expr(Call(
            Attribute(Name("result"), "append"),
            Name("candidate"))),
          .Stmts)
        AugAssign(Name("candidate"), "+", Int(1))
        Assign(Name("is_prime"), Bool(true))
        Assign(Name("divisor"), Int(2)))
      Return(Name("result"))
      ~> #endcall
    => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope("n" |-> N:Int, parent(0)))
    =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map => 0 |-> list(primesAcc(.ValSeq, 2, N)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires N >=Int 2
```

## 944. claim — `spec.k:154` (module `COUNT-UP-TO-BOUNDARY-SPEC`)

Attributes/classifiers: none

```k
  claim
    <k>
      Assign(Name("result"), ListExpr(.Exprs))
      Assign(Name("candidate"), Int(2))
      Assign(Name("is_prime"), Bool(true))
      Assign(Name("divisor"), Int(2))
      While(
        Compare(Name("candidate"), CmpOp("<", Name("n"))),
        While(
          Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
          If(
            Compare(
              BinOp("%", Name("candidate"), Name("divisor")),
              CmpOp("==", Int(0))),
            Assign(Name("is_prime"), Bool(false)),
            .Stmts)
          AugAssign(Name("divisor"), "+", Int(1)))
        If(
          Name("is_prime"),
          Expr(Call(
            Attribute(Name("result"), "append"),
            Name("candidate"))),
          .Stmts)
        AugAssign(Name("candidate"), "+", Int(1))
        Assign(Name("is_prime"), Bool(true))
        Assign(Name("divisor"), Int(2)))
      Return(Name("result"))
      ~> #endcall
    => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope("n" |-> N:Int, parent(0)))
    =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires 0 <=Int N andBool N <Int 2
```


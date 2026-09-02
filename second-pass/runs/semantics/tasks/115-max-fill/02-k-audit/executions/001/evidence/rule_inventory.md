# Exhaustive local K declaration inventory

Files: 26
Declarations: 967
Counts: claim=7, configuration=1, context=5, rule=718, syntax=236
Attribute-bearing declaration counts: concrete=32, function=150, macro=5, no-evaluators=22, owise=26, priority=31, seqstrict=1, strict=2, symbol=25, total=111

Per-file declaration counts:
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
- `spec.k`: 7
- `verification.k`: 32

Extraction rule: every source line beginning with `configuration`, `syntax`, `context`, `rule`, `claim`, or `alias`; continuations run to the next declaration/module boundary. Attributes are lexically classified.

1. `rule` — `reference-semantics/semantics/assert.k:6` — attributes: none

   `rule <k> Assert(V:Val) => .K ... </k>`

2. `rule` — `reference-semantics/semantics/assert.k:8-10` — attributes: none

   `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code>`

3. `rule` — `reference-semantics/semantics/assert.k:13-15` — attributes: priority

   `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

4. `rule` — `reference-semantics/semantics/bool.k:8` — attributes: none

   `rule applyUn("not", V:Val) => notBool truthy(V)`

5. `rule` — `reference-semantics/semantics/bool.k:10` — attributes: none

   `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`

6. `rule` — `reference-semantics/semantics/bool.k:11` — attributes: none

   `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2`

7. `context` — `reference-semantics/semantics/bool.k:16` — attributes: none

   `context BoolOp(_, (HOLE:Expr, _:Exprs))`

8. `rule` — `reference-semantics/semantics/bool.k:17` — attributes: none

   `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`

9. `rule` — `reference-semantics/semantics/bool.k:18` — attributes: none

   `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>`

10. `rule` — `reference-semantics/semantics/bool.k:20` — attributes: none

   `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>`

11. `rule` — `reference-semantics/semantics/bool.k:22` — attributes: none

   `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>`

12. `rule` — `reference-semantics/semantics/bool.k:24` — attributes: none

   `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>`

13. `rule` — `reference-semantics/semantics/bool.k:29-30` — attributes: priority

   `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`

14. `rule` — `reference-semantics/semantics/bool.k:31-32` — attributes: none

   `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`

15. `rule` — `reference-semantics/semantics/bool.k:35-36` — attributes: none

   `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap>`

16. `rule` — `reference-semantics/semantics/bool.k:39-40` — attributes: none

   `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap>`

17. `rule` — `reference-semantics/semantics/bool.k:43-44` — attributes: none

   `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`

18. `syntax` — `reference-semantics/semantics/builtins.k:17` — attributes: function

   `syntax Val ::= applyBuiltin(String, Vals) [function]`

19. `syntax` — `reference-semantics/semantics/builtins.k:20` — attributes: function

   `syntax Int ::= seqLen(Val) [function]`

20. `rule` — `reference-semantics/semantics/builtins.k:21` — attributes: none

   `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`

21. `rule` — `reference-semantics/semantics/builtins.k:22` — attributes: none

   `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)`

22. `rule` — `reference-semantics/semantics/builtins.k:23` — attributes: none

   `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)`

23. `rule` — `reference-semantics/semantics/builtins.k:24` — attributes: none

   `rule seqLen(str(IS:IntSeq))                   => isLen(IS)`

24. `rule` — `reference-semantics/semantics/builtins.k:25` — attributes: none

   `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)`

25. `rule` — `reference-semantics/semantics/builtins.k:26` — attributes: none

   `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)`

26. `rule` — `reference-semantics/semantics/builtins.k:32` — attributes: none

   `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>`

27. `rule` — `reference-semantics/semantics/builtins.k:33` — attributes: none

   `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`

28. `rule` — `reference-semantics/semantics/builtins.k:34` — attributes: none

   `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>`

29. `rule` — `reference-semantics/semantics/builtins.k:35` — attributes: none

   `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>`

30. `syntax` — `reference-semantics/semantics/builtins.k:36` — attributes: function, total

   `syntax ValSeq ::= charsOf(IntSeq) [function, total]`

31. `rule` — `reference-semantics/semantics/builtins.k:37` — attributes: none

   `rule charsOf(.IntSeq)                => .ValSeq`

32. `rule` — `reference-semantics/semantics/builtins.k:38` — attributes: none

   `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))`

33. `rule` — `reference-semantics/semantics/builtins.k:41` — attributes: none

   `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))`

34. `rule` — `reference-semantics/semantics/builtins.k:44` — attributes: none

   `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)`

35. `syntax` — `reference-semantics/semantics/builtins.k:47` — attributes: none

   `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`

36. `rule` — `reference-semantics/semantics/builtins.k:48` — attributes: none

   `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`

37. `rule` — `reference-semantics/semantics/builtins.k:49` — attributes: none

   `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`

38. `rule` — `reference-semantics/semantics/builtins.k:50-51` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k>`

39. `syntax` — `reference-semantics/semantics/builtins.k:54` — attributes: function

   `syntax Int ::= intOf(Val) [function]`

40. `rule` — `reference-semantics/semantics/builtins.k:55` — attributes: none

   `rule intOf(I:Int)  => I`

41. `rule` — `reference-semantics/semantics/builtins.k:56` — attributes: none

   `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi`

42. `syntax` — `reference-semantics/semantics/builtins.k:59` — attributes: none

   `syntax KItem ::= #allAcc(Iterable) | "#allCont"`

43. `rule` — `reference-semantics/semantics/builtins.k:60` — attributes: none

   `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`

44. `rule` — `reference-semantics/semantics/builtins.k:61` — attributes: none

   `rule <k> #iterDone ~> #allCont => true ... </k>`

45. `rule` — `reference-semantics/semantics/builtins.k:62` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>`

46. `rule` — `reference-semantics/semantics/builtins.k:64` — attributes: none

   `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>`

47. `syntax` — `reference-semantics/semantics/builtins.k:67` — attributes: none

   `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`

48. `rule` — `reference-semantics/semantics/builtins.k:68` — attributes: none

   `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`

49. `rule` — `reference-semantics/semantics/builtins.k:69` — attributes: none

   `rule <k> #iterDone ~> #anyCont => false ... </k>`

50. `rule` — `reference-semantics/semantics/builtins.k:70` — attributes: none

   `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>`

51. `rule` — `reference-semantics/semantics/builtins.k:72` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>`

52. `syntax` — `reference-semantics/semantics/builtins.k:76` — attributes: none

   `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`

53. `rule` — `reference-semantics/semantics/builtins.k:77` — attributes: none

   `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`

54. `rule` — `reference-semantics/semantics/builtins.k:78` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>`

55. `rule` — `reference-semantics/semantics/builtins.k:80` — attributes: none

   `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`

56. `rule` — `reference-semantics/semantics/builtins.k:81` — attributes: none

   `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`

57. `rule` — `reference-semantics/semantics/builtins.k:82-83` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>`

58. `syntax` — `reference-semantics/semantics/builtins.k:86` — attributes: none

   `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`

59. `rule` — `reference-semantics/semantics/builtins.k:87` — attributes: none

   `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`

60. `rule` — `reference-semantics/semantics/builtins.k:88` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>`

61. `rule` — `reference-semantics/semantics/builtins.k:90` — attributes: none

   `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`

62. `rule` — `reference-semantics/semantics/builtins.k:91` — attributes: none

   `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`

63. `rule` — `reference-semantics/semantics/builtins.k:92-93` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k>`

64. `syntax` — `reference-semantics/semantics/builtins.k:97` — attributes: function

   `syntax Int ::= maxVals(Int, Vals) [function]`

65. `rule` — `reference-semantics/semantics/builtins.k:98` — attributes: none

   `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`

66. `rule` — `reference-semantics/semantics/builtins.k:99` — attributes: none

   `rule maxVals(M:Int, .Vals)           => M`

67. `rule` — `reference-semantics/semantics/builtins.k:100` — attributes: none

   `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`

68. `syntax` — `reference-semantics/semantics/builtins.k:102` — attributes: function

   `syntax Int ::= minVals(Int, Vals) [function]`

69. `rule` — `reference-semantics/semantics/builtins.k:103` — attributes: none

   `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`

70. `rule` — `reference-semantics/semantics/builtins.k:104` — attributes: none

   `rule minVals(M:Int, .Vals)           => M`

71. `rule` — `reference-semantics/semantics/builtins.k:105` — attributes: none

   `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)`

72. `rule` — `reference-semantics/semantics/builtins.k:108` — attributes: none

   `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))`

73. `rule` — `reference-semantics/semantics/builtins.k:111-112` — attributes: none

   `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))`

74. `syntax` — `reference-semantics/semantics/builtins.k:114` — attributes: function, total

   `syntax IntSeq ::= binCodes(Int) [function, total]`

75. `rule` — `reference-semantics/semantics/builtins.k:115` — attributes: none

   `rule binCodes(0) => iCons(48, .IntSeq)`

76. `rule` — `reference-semantics/semantics/builtins.k:116` — attributes: none

   `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`

77. `syntax` — `reference-semantics/semantics/builtins.k:117` — attributes: function, total

   `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`

78. `rule` — `reference-semantics/semantics/builtins.k:118` — attributes: none

   `rule binAcc(0, ACC:IntSeq) => ACC`

79. `rule` — `reference-semantics/semantics/builtins.k:119-120` — attributes: none

   `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))`

80. `rule` — `reference-semantics/semantics/builtins.k:124-125` — attributes: none

   `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`

81. `syntax` — `reference-semantics/semantics/builtins.k:126` — attributes: function, total

   `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`

82. `rule` — `reference-semantics/semantics/builtins.k:127` — attributes: none

   `rule enumVS(.ValSeq, _:Int) => .ValSeq`

83. `rule` — `reference-semantics/semantics/builtins.k:128-129` — attributes: none

   `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))`

84. `rule` — `reference-semantics/semantics/builtins.k:132-133` — attributes: none

   `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`

85. `syntax` — `reference-semantics/semantics/builtins.k:134` — attributes: function, total

   `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`

86. `rule` — `reference-semantics/semantics/builtins.k:135` — attributes: none

   `rule mapStrVS(.ValSeq) => .ValSeq`

87. `rule` — `reference-semantics/semantics/builtins.k:136` — attributes: none

   `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`

88. `rule` — `reference-semantics/semantics/builtins.k:137` — attributes: none

   `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))`

89. `rule` — `reference-semantics/semantics/builtins.k:140` — attributes: none

   `rule applyBuiltin("int", I:Int, .Vals) => I`

90. `rule` — `reference-semantics/semantics/builtins.k:143` — attributes: none

   `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`

91. `rule` — `reference-semantics/semantics/builtins.k:144` — attributes: none

   `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))`

92. `rule` — `reference-semantics/semantics/builtins.k:148` — attributes: none

   `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))`

93. `rule` — `reference-semantics/semantics/builtins.k:149` — attributes: none

   `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)`

94. `rule` — `reference-semantics/semantics/builtins.k:152` — attributes: none

   `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48`

95. `rule` — `reference-semantics/semantics/builtins.k:156` — attributes: none

   `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)`

96. `syntax` — `reference-semantics/semantics/builtins.k:158` — attributes: function, total

   `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`

97. `rule` — `reference-semantics/semantics/builtins.k:159` — attributes: none

   `rule intDigAcc(.IntSeq, ACC:Int)             => ACC`

98. `rule` — `reference-semantics/semantics/builtins.k:160` — attributes: none

   `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))`

99. `rule` — `reference-semantics/semantics/builtins.k:163` — attributes: none

   `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`

100. `rule` — `reference-semantics/semantics/builtins.k:164` — attributes: none

   `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)`

101. `rule` — `reference-semantics/semantics/builtins.k:167-168` — attributes: none

   `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`

102. `rule` — `reference-semantics/semantics/builtins.k:169` — attributes: none

   `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>`

103. `rule` — `reference-semantics/semantics/builtins.k:170` — attributes: none

   `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`

104. `rule` — `reference-semantics/semantics/builtins.k:171-172` — attributes: none

   `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`

105. `rule` — `reference-semantics/semantics/builtins.k:173` — attributes: none

   `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>`

106. `rule` — `reference-semantics/semantics/builtins.k:174` — attributes: none

   `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>`

107. `rule` — `reference-semantics/semantics/builtins.k:177` — attributes: none

   `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)`

108. `rule` — `reference-semantics/semantics/builtins.k:178` — attributes: none

   `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)`

109. `rule` — `reference-semantics/semantics/builtins.k:179` — attributes: none

   `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)`

110. `rule` — `reference-semantics/semantics/builtins.k:187` — attributes: none

   `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`

111. `syntax` — `reference-semantics/semantics/builtins.k:188` — attributes: function

   `syntax Int ::= evalArith(IntSeq) [function]`

112. `rule` — `reference-semantics/semantics/builtins.k:189-190` — attributes: none

   `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`

113. `syntax` — `reference-semantics/semantics/builtins.k:192` — attributes: none

   `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`

114. `syntax` — `reference-semantics/semantics/builtins.k:194` — attributes: function, total

   `syntax Bool ::= evDigit(Int) [function, total]`

115. `rule` — `reference-semantics/semantics/builtins.k:195` — attributes: none

   `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`

116. `syntax` — `reference-semantics/semantics/builtins.k:196` — attributes: function, total

   `syntax Bool ::= evHead42(IntSeq) [function, total]`

117. `rule` — `reference-semantics/semantics/builtins.k:197` — attributes: none

   `rule evHead42(iCons(42, _:IntSeq)) => true`

118. `rule` — `reference-semantics/semantics/builtins.k:198` — attributes: owise

   `rule evHead42(_:IntSeq)            => false [owise]`

119. `syntax` — `reference-semantics/semantics/builtins.k:199` — attributes: function, total

   `syntax Bool ::= evHead47(IntSeq) [function, total]`

120. `rule` — `reference-semantics/semantics/builtins.k:200` — attributes: none

   `rule evHead47(iCons(47, _:IntSeq)) => true`

121. `rule` — `reference-semantics/semantics/builtins.k:201` — attributes: owise

   `rule evHead47(_:IntSeq)            => false [owise]`

122. `syntax` — `reference-semantics/semantics/builtins.k:203` — attributes: function, total

   `syntax OpSeq ::= tokOps(IntSeq) [function, total]`

123. `rule` — `reference-semantics/semantics/builtins.k:204` — attributes: none

   `rule tokOps(.IntSeq)                 => .OpSeq`

124. `rule` — `reference-semantics/semantics/builtins.k:205` — attributes: none

   `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)`

125. `rule` — `reference-semantics/semantics/builtins.k:206` — attributes: none

   `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)`

126. `rule` — `reference-semantics/semantics/builtins.k:207` — attributes: none

   `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`

127. `rule` — `reference-semantics/semantics/builtins.k:208` — attributes: none

   `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)`

128. `rule` — `reference-semantics/semantics/builtins.k:209` — attributes: none

   `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))`

129. `rule` — `reference-semantics/semantics/builtins.k:210` — attributes: none

   `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)`

130. `rule` — `reference-semantics/semantics/builtins.k:211` — attributes: none

   `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))`

131. `rule` — `reference-semantics/semantics/builtins.k:212` — attributes: none

   `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))`

132. `syntax` — `reference-semantics/semantics/builtins.k:214-215` — attributes: function, total

   `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`

133. `rule` — `reference-semantics/semantics/builtins.k:216` — attributes: none

   `rule tokNds(.IntSeq)                => .IntSeq`

134. `rule` — `reference-semantics/semantics/builtins.k:217` — attributes: none

   `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)`

135. `rule` — `reference-semantics/semantics/builtins.k:218` — attributes: none

   `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`

136. `rule` — `reference-semantics/semantics/builtins.k:219` — attributes: none

   `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)`

137. `rule` — `reference-semantics/semantics/builtins.k:221` — attributes: none

   `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)`

138. `rule` — `reference-semantics/semantics/builtins.k:223` — attributes: owise

   `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`

139. `syntax` — `reference-semantics/semantics/builtins.k:225` — attributes: none

   `syntax EvPair ::= evp(OpSeq, IntSeq)`

140. `syntax` — `reference-semantics/semantics/builtins.k:226` — attributes: function, total

   `syntax Int ::= firstNdE(EvPair) [function, total]`

141. `rule` — `reference-semantics/semantics/builtins.k:227` — attributes: none

   `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`

142. `rule` — `reference-semantics/semantics/builtins.k:228` — attributes: owise

   `rule firstNdE(_:EvPair) => 0 [owise]`

143. `syntax` — `reference-semantics/semantics/builtins.k:230` — attributes: function, total

   `syntax Int ::= applyOpE(String, Int, Int) [function, total]`

144. `rule` — `reference-semantics/semantics/builtins.k:231` — attributes: none

   `rule applyOpE("+",  A:Int, B:Int) => A +Int B`

145. `rule` — `reference-semantics/semantics/builtins.k:232` — attributes: none

   `rule applyOpE("-",  A:Int, B:Int) => A -Int B`

146. `rule` — `reference-semantics/semantics/builtins.k:233` — attributes: none

   `rule applyOpE("*",  A:Int, B:Int) => A *Int B`

147. `rule` — `reference-semantics/semantics/builtins.k:234` — attributes: none

   `rule applyOpE("//", A:Int, B:Int) => A divInt B`

148. `rule` — `reference-semantics/semantics/builtins.k:235` — attributes: none

   `rule applyOpE("**", A:Int, B:Int) => A ^Int B`

149. `rule` — `reference-semantics/semantics/builtins.k:236` — attributes: owise

   `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`

150. `syntax` — `reference-semantics/semantics/builtins.k:238` — attributes: function, total

   `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`

151. `rule` — `reference-semantics/semantics/builtins.k:239` — attributes: none

   `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`

152. `rule` — `reference-semantics/semantics/builtins.k:240` — attributes: none

   `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`

153. `rule` — `reference-semantics/semantics/builtins.k:241` — attributes: none

   `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))`

154. `rule` — `reference-semantics/semantics/builtins.k:243` — attributes: owise

   `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`

155. `syntax` — `reference-semantics/semantics/builtins.k:244` — attributes: function, total

   `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`

156. `rule` — `reference-semantics/semantics/builtins.k:245` — attributes: none

   `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`

157. `rule` — `reference-semantics/semantics/builtins.k:246` — attributes: none

   `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`

158. `syntax` — `reference-semantics/semantics/builtins.k:247` — attributes: function, total

   `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`

159. `rule` — `reference-semantics/semantics/builtins.k:248` — attributes: none

   `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`

160. `syntax` — `reference-semantics/semantics/builtins.k:250` — attributes: function, total

   `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`

161. `rule` — `reference-semantics/semantics/builtins.k:251` — attributes: none

   `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`

162. `rule` — `reference-semantics/semantics/builtins.k:252` — attributes: none

   `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`

163. `rule` — `reference-semantics/semantics/builtins.k:253` — attributes: none

   `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`

164. `rule` — `reference-semantics/semantics/builtins.k:254` — attributes: none

   `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`

165. `syntax` — `reference-semantics/semantics/builtins.k:255` — attributes: function, total

   `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`

166. `rule` — `reference-semantics/semantics/builtins.k:256` — attributes: none

   `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`

167. `rule` — `reference-semantics/semantics/builtins.k:257-258` — attributes: none

   `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)`

168. `rule` — `reference-semantics/semantics/builtins.k:260-261` — attributes: none

   `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))`

169. `rule` — `reference-semantics/semantics/builtins.k:263-264` — attributes: owise

   `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`

170. `syntax` — `reference-semantics/semantics/builtins.k:265` — attributes: function, total

   `syntax Bool ::= inLevelE(String, String) [function, total]`

171. `rule` — `reference-semantics/semantics/builtins.k:266` — attributes: none

   `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"`

172. `rule` — `reference-semantics/semantics/builtins.k:267` — attributes: none

   `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`

173. `rule` — `reference-semantics/semantics/builtins.k:268` — attributes: owise

   `rule inLevelE(_:String, _:String) => false [owise]`

174. `syntax` — `reference-semantics/semantics/builtins.k:269` — attributes: function, total

   `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`

175. `rule` — `reference-semantics/semantics/builtins.k:270` — attributes: none

   `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`

176. `rule` — `reference-semantics/semantics/builtins.k:271` — attributes: none

   `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`

177. `syntax` — `reference-semantics/semantics/builtins.k:272` — attributes: function, total

   `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`

178. `rule` — `reference-semantics/semantics/builtins.k:273` — attributes: none

   `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`

179. `rule` — `reference-semantics/semantics/builtins.k:274` — attributes: none

   `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))`

180. `syntax` — `reference-semantics/semantics/builtins.k:279` — attributes: none

   `syntax KItem ::= "#md5"`

181. `rule` — `reference-semantics/semantics/builtins.k:280-281` — attributes: priority

   `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`

182. `rule` — `reference-semantics/semantics/builtins.k:282` — attributes: none

   `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`

183. `syntax` — `reference-semantics/semantics/builtins.k:283` — attributes: none

   `syntax Val ::= md5Obj(IntSeq)`

184. `rule` — `reference-semantics/semantics/builtins.k:284` — attributes: none

   `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`

185. `syntax` — `reference-semantics/semantics/builtins.k:285` — attributes: function, no-evaluators, symbol, total

   `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`

186. `rule` — `reference-semantics/semantics/builtins.k:291` — attributes: none

   `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`

187. `rule` — `reference-semantics/semantics/builtins.k:292` — attributes: none

   `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`

188. `syntax` — `reference-semantics/semantics/builtins.k:293` — attributes: function

   `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`

189. `rule` — `reference-semantics/semantics/builtins.k:294` — attributes: none

   `rule isIntV(_:Int)         => true`

190. `rule` — `reference-semantics/semantics/builtins.k:295` — attributes: owise

   `rule isIntV(_:Val)         => false [owise]`

191. `rule` — `reference-semantics/semantics/builtins.k:296` — attributes: none

   `rule isStrV(str(_:IntSeq)) => true`

192. `rule` — `reference-semantics/semantics/builtins.k:297` — attributes: owise

   `rule isStrV(_:Val)         => false [owise]`

193. `rule` — `reference-semantics/semantics/call.k:16` — attributes: none

   `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>`

194. `syntax` — `reference-semantics/semantics/call.k:19` — attributes: none

   `syntax KItem ::= #callee(Exprs)`

195. `rule` — `reference-semantics/semantics/call.k:20` — attributes: owise

   `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`

196. `rule` — `reference-semantics/semantics/call.k:21` — attributes: none

   `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>`

197. `rule` — `reference-semantics/semantics/call.k:24` — attributes: none

   `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`

198. `rule` — `reference-semantics/semantics/call.k:26` — attributes: none

   `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`

199. `rule` — `reference-semantics/semantics/call.k:27` — attributes: none

   `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>`

200. `rule` — `reference-semantics/semantics/call.k:28` — attributes: none

   `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>`

201. `rule` — `reference-semantics/semantics/call.k:29` — attributes: none

   `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>`

202. `rule` — `reference-semantics/semantics/call.k:30` — attributes: none

   `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>`

203. `rule` — `reference-semantics/semantics/call.k:31` — attributes: owise

   `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`

204. `rule` — `reference-semantics/semantics/call.k:32` — attributes: none

   `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>`

205. `rule` — `reference-semantics/semantics/call.k:38-41` — attributes: priority

   `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

206. `rule` — `reference-semantics/semantics/call.k:42-44` — attributes: none

   `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`

207. `rule` — `reference-semantics/semantics/call.k:47-50` — attributes: priority

   `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

208. `syntax` — `reference-semantics/semantics/call.k:52` — attributes: function, total

   `syntax Bool ::= isMutMethod(String) [function, total]`

209. `rule` — `reference-semantics/semantics/call.k:53-55` — attributes: none

   `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`

210. `rule` — `reference-semantics/semantics/call.k:56-58` — attributes: none

   `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap>`

211. `rule` — `reference-semantics/semantics/call.k:63-65` — attributes: none

   `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`

212. `rule` — `reference-semantics/semantics/call.k:69-74` — attributes: none

   `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`

213. `rule` — `reference-semantics/semantics/call.k:80-85` — attributes: none

   `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`

214. `syntax` — `reference-semantics/semantics/call.k:87` — attributes: none

   `syntax KItem ::= #allocCells(ParamNames)`

215. `rule` — `reference-semantics/semantics/call.k:88` — attributes: none

   `rule <k> #allocCells(.ParamNames) => .K ... </k>`

216. `rule` — `reference-semantics/semantics/call.k:89-93` — attributes: none

   `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc>`

217. `rule` — `reference-semantics/semantics/comprehension.k:11` — attributes: none

   `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`

218. `rule` — `reference-semantics/semantics/comprehension.k:12` — attributes: none

   `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`

219. `syntax` — `reference-semantics/semantics/comprehension.k:14` — attributes: macro

   `syntax Stmts ::= compBody(CompFors, Expr) [macro]`

220. `rule` — `reference-semantics/semantics/comprehension.k:15-16` — attributes: none

   `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`

221. `syntax` — `reference-semantics/semantics/comprehension.k:18` — attributes: macro

   `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`

222. `rule` — `reference-semantics/semantics/comprehension.k:19-20` — attributes: none

   `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`

223. `rule` — `reference-semantics/semantics/comprehension.k:21-22` — attributes: none

   `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`

224. `syntax` — `reference-semantics/semantics/comprehension.k:24` — attributes: macro

   `syntax Expr ::= compGuard(Exprs) [macro]`

225. `rule` — `reference-semantics/semantics/comprehension.k:25` — attributes: none

   `rule compGuard(.Exprs)             => Bool(true)`

226. `rule` — `reference-semantics/semantics/comprehension.k:26` — attributes: none

   `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`

227. `rule` — `reference-semantics/semantics/concrete.k:13-14` — attributes: none

   `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap>`

228. `rule` — `reference-semantics/semantics/concrete.k:16-17` — attributes: none

   `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap>`

229. `syntax` — `reference-semantics/semantics/concrete.k:25` — attributes: none

   `syntax Val ::= kvP(Val, Val)`

230. `syntax` — `reference-semantics/semantics/concrete.k:26-27` — attributes: none

   `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`

231. `rule` — `reference-semantics/semantics/concrete.k:28-30` — attributes: priority

   `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`

232. `rule` — `reference-semantics/semantics/concrete.k:31-33` — attributes: priority

   `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`

233. `rule` — `reference-semantics/semantics/concrete.k:34-35` — attributes: none

   `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`

234. `rule` — `reference-semantics/semantics/concrete.k:36-37` — attributes: none

   `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`

235. `rule` — `reference-semantics/semantics/concrete.k:38-39` — attributes: none

   `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>`

236. `syntax` — `reference-semantics/semantics/concrete.k:42` — attributes: function

   `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`

237. `rule` — `reference-semantics/semantics/concrete.k:43` — attributes: none

   `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`

238. `rule` — `reference-semantics/semantics/concrete.k:44-45` — attributes: none

   `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R))`

239. `rule` — `reference-semantics/semantics/concrete.k:47-48` — attributes: none

   `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V))`

240. `syntax` — `reference-semantics/semantics/concrete.k:51` — attributes: function

   `syntax Bool ::= kLt(Val, Val) [function]`

241. `rule` — `reference-semantics/semantics/concrete.k:52` — attributes: none

   `rule kLt(I1:Int, I2:Int)             => I1 <Int I2`

242. `rule` — `reference-semantics/semantics/concrete.k:53` — attributes: none

   `rule kLt(F1:Float, F2:Float)         => F1 <Float F2`

243. `rule` — `reference-semantics/semantics/concrete.k:54` — attributes: none

   `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`

244. `syntax` — `reference-semantics/semantics/concrete.k:56` — attributes: function, total

   `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`

245. `rule` — `reference-semantics/semantics/concrete.k:57` — attributes: none

   `rule unpairVS(.ValSeq) => .ValSeq`

246. `rule` — `reference-semantics/semantics/concrete.k:58` — attributes: none

   `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`

247. `rule` — `reference-semantics/semantics/concrete.k:59` — attributes: owise

   `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`

248. `rule` — `reference-semantics/semantics/controls.k:9-11` — attributes: none

   `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`

249. `rule` — `reference-semantics/semantics/controls.k:12-14` — attributes: none

   `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`

250. `rule` — `reference-semantics/semantics/controls.k:20-22` — attributes: none

   `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>`

251. `rule` — `reference-semantics/semantics/controls.k:27-29` — attributes: none

   `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`

252. `rule` — `reference-semantics/semantics/controls.k:35` — attributes: none

   `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`

253. `rule` — `reference-semantics/semantics/controls.k:36` — attributes: owise

   `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`

254. `syntax` — `reference-semantics/semantics/controls.k:37` — attributes: none

   `syntax KItem ::= #bindImports(ParamNames)`

255. `rule` — `reference-semantics/semantics/controls.k:38` — attributes: none

   `rule <k> #bindImports(.ParamNames) => .K ... </k>`

256. `rule` — `reference-semantics/semantics/controls.k:39-41` — attributes: none

   `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>`

257. `rule` — `reference-semantics/semantics/controls.k:43` — attributes: none

   `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>`

258. `rule` — `reference-semantics/semantics/controls.k:48` — attributes: none

   `rule <k> Expr(_:Val) => .K ... </k>`

259. `syntax` — `reference-semantics/semantics/controls.k:51` — attributes: none

   `syntax KItem ::= #branch(Bool, Stmts, Stmts)`

260. `rule` — `reference-semantics/semantics/controls.k:52` — attributes: none

   `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`

261. `rule` — `reference-semantics/semantics/controls.k:53` — attributes: none

   `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>`

262. `rule` — `reference-semantics/semantics/controls.k:54` — attributes: none

   `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>`

263. `rule` — `reference-semantics/semantics/controls.k:57` — attributes: none

   `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>`

264. `rule` — `reference-semantics/semantics/controls.k:59` — attributes: none

   `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>`

265. `syntax` — `reference-semantics/semantics/controls.k:65-67` — attributes: none

   `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`

266. `rule` — `reference-semantics/semantics/controls.k:69` — attributes: none

   `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`

267. `rule` — `reference-semantics/semantics/controls.k:71` — attributes: none

   `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`

268. `rule` — `reference-semantics/semantics/controls.k:72` — attributes: none

   `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`

269. `rule` — `reference-semantics/semantics/controls.k:73-74` — attributes: none

   `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>`

270. `rule` — `reference-semantics/semantics/controls.k:77` — attributes: none

   `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`

271. `rule` — `reference-semantics/semantics/controls.k:78` — attributes: none

   `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`

272. `rule` — `reference-semantics/semantics/controls.k:79` — attributes: none

   `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>`

273. `rule` — `reference-semantics/semantics/controls.k:81` — attributes: none

   `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>`

274. `rule` — `reference-semantics/semantics/controls.k:85` — attributes: none

   `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`

275. `rule` — `reference-semantics/semantics/controls.k:86` — attributes: none

   `rule <k> Continue => #cont ... </k>`

276. `rule` — `reference-semantics/semantics/controls.k:87` — attributes: none

   `rule <k> Break => #brk ... </k>`

277. `rule` — `reference-semantics/semantics/controls.k:88` — attributes: none

   `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`

278. `rule` — `reference-semantics/semantics/controls.k:89` — attributes: owise

   `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`

279. `rule` — `reference-semantics/semantics/controls.k:90` — attributes: none

   `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`

280. `rule` — `reference-semantics/semantics/controls.k:91` — attributes: owise

   `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]`

281. `rule` — `reference-semantics/semantics/controls.k:95-97` — attributes: priority

   `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

282. `rule` — `reference-semantics/semantics/controls.k:98-100` — attributes: priority

   `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

283. `rule` — `reference-semantics/semantics/controls.k:101-103` — attributes: priority

   `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

284. `rule` — `reference-semantics/semantics/controls.k:106-108` — attributes: priority

   `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

285. `syntax` — `reference-semantics/semantics/core.k:13` — attributes: none

   `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`

286. `syntax` — `reference-semantics/semantics/core.k:14` — attributes: none

   `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`

287. `syntax` — `reference-semantics/semantics/core.k:15` — attributes: none

   `syntax Str    ::= str(IntSeq)`

288. `syntax` — `reference-semantics/semantics/core.k:18-23` — attributes: none

   `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`

289. `syntax` — `reference-semantics/semantics/core.k:25-34` — attributes: function

   `syntax Val      ::= Int | Bool | "noneV" | Iterable | ref(Int)          // a heap object: <heap> holds its list(VS) | cellRef(Int)      // a closure cell: <heap> holds cellV(V) | closureVal(ParamNames, Stmts, Int) | typeV(String)     // a type object (int/str), resolved from the builtins frame | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough) | boundMethodV(Val, String)   // a cooled Attribute: obj.method`

290. `syntax` — `reference-semantics/semantics/core.k:36` — attributes: none

   `syntax Parent   ::= "root" | parent(Int)`

291. `syntax` — `reference-semantics/semantics/core.k:37` — attributes: none

   `syntax Scope    ::= scope(Map, Parent)`

292. `syntax` — `reference-semantics/semantics/core.k:38` — attributes: none

   `syntax KResult  ::= Val`

293. `syntax` — `reference-semantics/semantics/core.k:39` — attributes: none

   `syntax Expr     ::= Val   // cooling puts results back into expression holes`

294. `syntax` — `reference-semantics/semantics/core.k:40` — attributes: none

   `syntax Vals     ::= List{Val, ","}`

295. `syntax` — `reference-semantics/semantics/core.k:41` — attributes: none

   `syntax Exc      ::= "NoExc" | "AssertionError"`

296. `syntax` — `reference-semantics/semantics/core.k:42` — attributes: none

   `syntax RetState ::= "noRet" | retV(Val)`

297. `configuration` — `reference-semantics/semantics/core.k:49-60` — attributes: none

   `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     |-> scope(.Map, parent(-1)) -1    |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code>`

298. `syntax` — `reference-semantics/semantics/core.k:68` — attributes: function, total

   `syntax Bool ::= isRefV(Val) [function, total]`

299. `rule` — `reference-semantics/semantics/core.k:69` — attributes: none

   `rule isRefV(ref(_:Int)) => true`

300. `rule` — `reference-semantics/semantics/core.k:70` — attributes: owise

   `rule isRefV(_:Val)      => false [owise]`

301. `syntax` — `reference-semantics/semantics/core.k:75` — attributes: none

   `syntax HeapVal ::= cellV(Val)`

302. `syntax` — `reference-semantics/semantics/core.k:76` — attributes: function, total

   `syntax Bool ::= isCellRef(Val) [function, total]`

303. `rule` — `reference-semantics/semantics/core.k:77` — attributes: none

   `rule isCellRef(cellRef(_:Int)) => true`

304. `rule` — `reference-semantics/semantics/core.k:78` — attributes: owise

   `rule isCellRef(_:Val)          => false [owise]`

305. `rule` — `reference-semantics/semantics/core.k:85-88` — attributes: none

   `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap>`

306. `syntax` — `reference-semantics/semantics/core.k:95` — attributes: none

   `syntax Val ::= kwV(String, Val)`

307. `syntax` — `reference-semantics/semantics/core.k:96` — attributes: none

   `syntax KItem ::= #kwTag(String)`

308. `rule` — `reference-semantics/semantics/core.k:97` — attributes: none

   `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`

309. `rule` — `reference-semantics/semantics/core.k:98` — attributes: none

   `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>`

310. `syntax` — `reference-semantics/semantics/core.k:100` — attributes: function, total

   `syntax Bool ::= isKwV(Val) [function, total]`

311. `rule` — `reference-semantics/semantics/core.k:101` — attributes: none

   `rule isKwV(kwV(_:String, _:Val)) => true`

312. `rule` — `reference-semantics/semantics/core.k:102` — attributes: owise

   `rule isKwV(_:Val)                => false [owise]`

313. `syntax` — `reference-semantics/semantics/core.k:106` — attributes: none

   `syntax Val ::= cellsMark(ParamNames)`

314. `syntax` — `reference-semantics/semantics/core.k:107` — attributes: function

   `syntax ParamNames ::= cellsOf(Val) [function]`

315. `rule` — `reference-semantics/semantics/core.k:108` — attributes: none

   `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`

316. `syntax` — `reference-semantics/semantics/core.k:109` — attributes: function, total

   `syntax Bool ::= pnMember(String, ParamNames) [function, total]`

317. `rule` — `reference-semantics/semantics/core.k:110` — attributes: none

   `rule pnMember(_:String, .ParamNames) => false`

318. `rule` — `reference-semantics/semantics/core.k:111` — attributes: none

   `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`

319. `syntax` — `reference-semantics/semantics/core.k:113` — attributes: none

   `syntax KItem ::= #cellW(Val, Val)`

320. `rule` — `reference-semantics/semantics/core.k:114-115` — attributes: none

   `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`

321. `syntax` — `reference-semantics/semantics/core.k:117` — attributes: none

   `syntax KItem ::= #alloc(Val)`

322. `rule` — `reference-semantics/semantics/core.k:118-120` — attributes: none

   `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc>`

323. `syntax` — `reference-semantics/semantics/core.k:124` — attributes: none

   `syntax KItem ::= #loadAll(Module)`

324. `rule` — `reference-semantics/semantics/core.k:125` — attributes: none

   `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`

325. `rule` — `reference-semantics/semantics/core.k:126` — attributes: none

   `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`

326. `rule` — `reference-semantics/semantics/core.k:127` — attributes: none

   `rule <k> .Stmts => .K ... </k>`

327. `syntax` — `reference-semantics/semantics/core.k:130` — attributes: none

   `syntax KItem ::= #look(String, Int)`

328. `rule` — `reference-semantics/semantics/core.k:131` — attributes: none

   `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`

329. `rule` — `reference-semantics/semantics/core.k:132-133` — attributes: none

   `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>`

330. `rule` — `reference-semantics/semantics/core.k:145-147` — attributes: none

   `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap>`

331. `rule` — `reference-semantics/semantics/core.k:152-153` — attributes: none

   `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>`

332. `syntax` — `reference-semantics/semantics/core.k:157` — attributes: function, total

   `syntax Scope ::= "builtinsScope" [function, total]`

333. `rule` — `reference-semantics/semantics/core.k:158-181` — attributes: none

   `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root)`

334. `syntax` — `reference-semantics/semantics/core.k:185` — attributes: none

   `syntax ApplyK ::= toCall(Val)`

335. `syntax` — `reference-semantics/semantics/core.k:186-188` — attributes: none

   `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`

336. `rule` — `reference-semantics/semantics/core.k:189` — attributes: none

   `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`

337. `rule` — `reference-semantics/semantics/core.k:190` — attributes: none

   `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`

338. `rule` — `reference-semantics/semantics/core.k:191` — attributes: none

   `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>`

339. `rule` — `reference-semantics/semantics/core.k:194` — attributes: none

   `rule <k> Int(I:Int)   => I ... </k>`

340. `rule` — `reference-semantics/semantics/core.k:195` — attributes: none

   `rule <k> Bool(B:Bool) => B ... </k>`

341. `rule` — `reference-semantics/semantics/core.k:196` — attributes: none

   `rule <k> NoneVal      => noneV ... </k>`

342. `syntax` — `reference-semantics/semantics/core.k:199` — attributes: function

   `syntax Bool ::= truthy(Val) [function]`

343. `rule` — `reference-semantics/semantics/core.k:200` — attributes: none

   `rule truthy(B:Bool)          => B`

344. `rule` — `reference-semantics/semantics/core.k:201` — attributes: none

   `rule truthy(noneV)           => false`

345. `rule` — `reference-semantics/semantics/core.k:202` — attributes: none

   `rule truthy(I:Int)           => I =/=Int 0`

346. `rule` — `reference-semantics/semantics/core.k:203` — attributes: none

   `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)`

347. `rule` — `reference-semantics/semantics/core.k:204` — attributes: none

   `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)`

348. `rule` — `reference-semantics/semantics/core.k:205` — attributes: none

   `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)`

349. `syntax` — `reference-semantics/semantics/core.k:208` — attributes: function

   `syntax Val  ::= applyUn(String, Val) [function]`

350. `syntax` — `reference-semantics/semantics/core.k:209` — attributes: function

   `syntax Val  ::= applyBin(String, Val, Val) [function]`

351. `syntax` — `reference-semantics/semantics/core.k:210` — attributes: function

   `syntax Bool ::= applyCmp(String, Val, Val) [function]`

352. `syntax` — `reference-semantics/semantics/core.k:213` — attributes: function, total

   `syntax Vals ::= appendVal(Vals, Val) [function, total]`

353. `rule` — `reference-semantics/semantics/core.k:214` — attributes: none

   `rule appendVal(.Vals, V:Val)              => V , .Vals`

354. `rule` — `reference-semantics/semantics/core.k:215` — attributes: none

   `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)`

355. `syntax` — `reference-semantics/semantics/core.k:217` — attributes: function, total

   `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`

356. `rule` — `reference-semantics/semantics/core.k:218` — attributes: none

   `rule vals2valSeq(.Vals)            => .ValSeq`

357. `rule` — `reference-semantics/semantics/core.k:219` — attributes: none

   `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))`

358. `syntax` — `reference-semantics/semantics/core.k:223` — attributes: function, total

   `syntax Int ::= vsLen(ValSeq) [function, total]`

359. `rule` — `reference-semantics/semantics/core.k:224` — attributes: none

   `rule vsLen(.ValSeq)                => 0`

360. `rule` — `reference-semantics/semantics/core.k:225` — attributes: none

   `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`

361. `syntax` — `reference-semantics/semantics/core.k:227` — attributes: function, total

   `syntax Int ::= isLen(IntSeq) [function, total]`

362. `rule` — `reference-semantics/semantics/core.k:228` — attributes: none

   `rule isLen(.IntSeq)                => 0`

363. `rule` — `reference-semantics/semantics/core.k:229` — attributes: none

   `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)`

364. `syntax` — `reference-semantics/semantics/core.k:233` — attributes: function, total

   `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`

365. `rule` — `reference-semantics/semantics/core.k:234` — attributes: none

   `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq`

366. `rule` — `reference-semantics/semantics/core.k:235` — attributes: none

   `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)`

367. `rule` — `reference-semantics/semantics/core.k:236` — attributes: none

   `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))`

368. `rule` — `reference-semantics/semantics/core.k:238` — attributes: none

   `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS`

369. `syntax` — `reference-semantics/semantics/dict.k:20` — attributes: none

   `syntax Val ::= dictV(ValSeq, ValSeq)`

370. `syntax` — `reference-semantics/semantics/dict.k:23-25` — attributes: none

   `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`

371. `rule` — `reference-semantics/semantics/dict.k:26` — attributes: none

   `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`

372. `rule` — `reference-semantics/semantics/dict.k:27` — attributes: none

   `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`

373. `rule` — `reference-semantics/semantics/dict.k:28-29` — attributes: none

   `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`

374. `rule` — `reference-semantics/semantics/dict.k:30-31` — attributes: none

   `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`

375. `rule` — `reference-semantics/semantics/dict.k:32-33` — attributes: none

   `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>`

376. `syntax` — `reference-semantics/semantics/dict.k:37` — attributes: function, total

   `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`

377. `rule` — `reference-semantics/semantics/dict.k:38` — attributes: none

   `rule dHasKey(.ValSeq, _:Val)                => false`

378. `rule` — `reference-semantics/semantics/dict.k:39` — attributes: none

   `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K`

379. `rule` — `reference-semantics/semantics/dict.k:40` — attributes: none

   `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)`

380. `syntax` — `reference-semantics/semantics/dict.k:43` — attributes: function, total

   `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`

381. `rule` — `reference-semantics/semantics/dict.k:44` — attributes: none

   `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)`

382. `rule` — `reference-semantics/semantics/dict.k:45` — attributes: none

   `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)`

383. `syntax` — `reference-semantics/semantics/dict.k:49` — attributes: function, total

   `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`

384. `rule` — `reference-semantics/semantics/dict.k:50` — attributes: none

   `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)`

385. `rule` — `reference-semantics/semantics/dict.k:52` — attributes: none

   `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))`

386. `rule` — `reference-semantics/semantics/dict.k:54` — attributes: owise

   `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]`

387. `rule` — `reference-semantics/semantics/dict.k:58-60` — attributes: priority

   `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]`

388. `rule` — `reference-semantics/semantics/dict.k:63` — attributes: none

   `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`

389. `syntax` — `reference-semantics/semantics/dict.k:64` — attributes: function

   `syntax Val ::= applyIndexD(Val, Val) [function]`

390. `rule` — `reference-semantics/semantics/dict.k:65-66` — attributes: priority

   `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]`

391. `syntax` — `reference-semantics/semantics/dict.k:70` — attributes: function

   `syntax Val ::= dictSet(Val, Val, Val) [function]`

392. `rule` — `reference-semantics/semantics/dict.k:71` — attributes: none

   `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))`

393. `syntax` — `reference-semantics/semantics/dict.k:76` — attributes: none

   `syntax KItem ::= #dsetK(String, Val)`

394. `rule` — `reference-semantics/semantics/dict.k:77` — attributes: none

   `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`

395. `rule` — `reference-semantics/semantics/dict.k:78-80` — attributes: none

   `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>`

396. `rule` — `reference-semantics/semantics/dict.k:82-84` — attributes: none

   `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`

397. `syntax` — `reference-semantics/semantics/dict.k:86` — attributes: none

   `syntax KItem ::= #dsetV(Val, Val, Val)`

398. `rule` — `reference-semantics/semantics/dict.k:87-88` — attributes: none

   `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>`

399. `syntax` — `reference-semantics/semantics/dict.k:90` — attributes: function, total

   `syntax Int ::= normIdxD(Int, Int) [function, total]`

400. `rule` — `reference-semantics/semantics/dict.k:91` — attributes: none

   `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`

401. `rule` — `reference-semantics/semantics/dict.k:92` — attributes: none

   `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0`

402. `rule` — `reference-semantics/semantics/dict.k:95-96` — attributes: none

   `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`

403. `syntax` — `reference-semantics/semantics/dict.k:97` — attributes: function

   `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`

404. `rule` — `reference-semantics/semantics/dict.k:98` — attributes: none

   `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`

405. `rule` — `reference-semantics/semantics/dict.k:99-100` — attributes: none

   `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`

406. `syntax` — `reference-semantics/semantics/dict.k:101` — attributes: function

   `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`

407. `rule` — `reference-semantics/semantics/dict.k:102` — attributes: none

   `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K`

408. `rule` — `reference-semantics/semantics/dict.k:103` — attributes: none

   `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`

409. `syntax` — `reference-semantics/semantics/float.k:20` — attributes: none

   `syntax Val ::= Float`

410. `rule` — `reference-semantics/semantics/float.k:21` — attributes: none

   `rule <k> Float(F:Float) => F ... </k>`

411. `syntax` — `reference-semantics/semantics/float.k:24` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`

412. `rule` — `reference-semantics/semantics/float.k:25` — attributes: concrete

   `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`

413. `rule` — `reference-semantics/semantics/float.k:27` — attributes: none

   `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)`

414. `syntax` — `reference-semantics/semantics/float.k:30` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`

415. `rule` — `reference-semantics/semantics/float.k:31` — attributes: concrete

   `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`

416. `rule` — `reference-semantics/semantics/float.k:32` — attributes: none

   `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)`

417. `syntax` — `reference-semantics/semantics/float.k:37` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`

418. `rule` — `reference-semantics/semantics/float.k:38` — attributes: concrete

   `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`

419. `rule` — `reference-semantics/semantics/float.k:39` — attributes: none

   `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)`

420. `rule` — `reference-semantics/semantics/float.k:43` — attributes: none

   `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`

421. `rule` — `reference-semantics/semantics/float.k:44` — attributes: none

   `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)`

422. `syntax` — `reference-semantics/semantics/float.k:50` — attributes: function, no-evaluators, symbol, total

   `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`

423. `rule` — `reference-semantics/semantics/float.k:51` — attributes: concrete

   `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`

424. `rule` — `reference-semantics/semantics/float.k:52` — attributes: none

   `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`

425. `syntax` — `reference-semantics/semantics/float.k:54` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`

426. `rule` — `reference-semantics/semantics/float.k:55` — attributes: concrete

   `rule absF(F:Float) => absFloat(F) [concrete]`

427. `rule` — `reference-semantics/semantics/float.k:56` — attributes: none

   `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)`

428. `rule` — `reference-semantics/semantics/float.k:61` — attributes: none

   `rule <k> Import(_:String) => .K ... </k>`

429. `syntax` — `reference-semantics/semantics/float.k:65` — attributes: none

   `syntax KItem ::= "#mathCeil"`

430. `rule` — `reference-semantics/semantics/float.k:66` — attributes: priority

   `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`

431. `rule` — `reference-semantics/semantics/float.k:67` — attributes: none

   `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>`

432. `syntax` — `reference-semantics/semantics/float.k:70` — attributes: none

   `syntax KItem ::= "#mathFloor"`

433. `rule` — `reference-semantics/semantics/float.k:71` — attributes: priority

   `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`

434. `rule` — `reference-semantics/semantics/float.k:72` — attributes: none

   `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`

435. `syntax` — `reference-semantics/semantics/float.k:73` — attributes: function, symbol, total

   `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`

436. `rule` — `reference-semantics/semantics/float.k:74` — attributes: concrete

   `rule floorFI(I:Int)   => I                        [concrete]`

437. `rule` — `reference-semantics/semantics/float.k:75` — attributes: concrete

   `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]`

438. `rule` — `reference-semantics/semantics/float.k:78` — attributes: none

   `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`

439. `rule` — `reference-semantics/semantics/float.k:79` — attributes: none

   `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)`

440. `syntax` — `reference-semantics/semantics/float.k:82` — attributes: none

   `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`

441. `rule` — `reference-semantics/semantics/float.k:83` — attributes: priority

   `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`

442. `rule` — `reference-semantics/semantics/float.k:84` — attributes: none

   `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`

443. `rule` — `reference-semantics/semantics/float.k:85` — attributes: none

   `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`

444. `syntax` — `reference-semantics/semantics/float.k:86` — attributes: function, symbol, total

   `syntax Float ::= toF(Val) [function, total, symbol(toF)]`

445. `rule` — `reference-semantics/semantics/float.k:87` — attributes: concrete

   `rule toF(F:Float) => F        [concrete]`

446. `rule` — `reference-semantics/semantics/float.k:88` — attributes: concrete

   `rule toF(I:Int)   => intToF(I) [concrete]`

447. `syntax` — `reference-semantics/semantics/float.k:93` — attributes: function, symbol, total

   `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`

448. `rule` — `reference-semantics/semantics/float.k:94` — attributes: concrete

   `rule ceilF(I:Int)   => I                       [concrete]`

449. `rule` — `reference-semantics/semantics/float.k:95` — attributes: concrete

   `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]`

450. `rule` — `reference-semantics/semantics/float.k:99` — attributes: none

   `rule applyUn("-", F:Float) => 0.0 -Float F`

451. `syntax` — `reference-semantics/semantics/float.k:103` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`

452. `rule` — `reference-semantics/semantics/float.k:104` — attributes: concrete

   `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`

453. `rule` — `reference-semantics/semantics/float.k:105` — attributes: none

   `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`

454. `syntax` — `reference-semantics/semantics/float.k:107` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`

455. `rule` — `reference-semantics/semantics/float.k:108` — attributes: concrete

   `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`

456. `rule` — `reference-semantics/semantics/float.k:109` — attributes: none

   `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`

457. `syntax` — `reference-semantics/semantics/float.k:111` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`

458. `rule` — `reference-semantics/semantics/float.k:112` — attributes: concrete

   `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`

459. `rule` — `reference-semantics/semantics/float.k:113` — attributes: none

   `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`

460. `syntax` — `reference-semantics/semantics/float.k:115` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`

461. `rule` — `reference-semantics/semantics/float.k:116` — attributes: concrete

   `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`

462. `rule` — `reference-semantics/semantics/float.k:117` — attributes: none

   `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`

463. `syntax` — `reference-semantics/semantics/float.k:119` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`

464. `rule` — `reference-semantics/semantics/float.k:120` — attributes: concrete

   `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`

465. `rule` — `reference-semantics/semantics/float.k:121` — attributes: none

   `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)`

466. `syntax` — `reference-semantics/semantics/float.k:125` — attributes: function, no-evaluators, symbol, total

   `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`

467. `rule` — `reference-semantics/semantics/float.k:126` — attributes: concrete

   `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`

468. `rule` — `reference-semantics/semantics/float.k:127` — attributes: none

   `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)`

469. `rule` — `reference-semantics/semantics/float.k:128` — attributes: none

   `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`

470. `rule` — `reference-semantics/semantics/float.k:129` — attributes: none

   `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)`

471. `rule` — `reference-semantics/semantics/float.k:132` — attributes: none

   `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`

472. `rule` — `reference-semantics/semantics/float.k:133` — attributes: none

   `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`

473. `rule` — `reference-semantics/semantics/float.k:134` — attributes: none

   `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)`

474. `rule` — `reference-semantics/semantics/float.k:135` — attributes: none

   `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))`

475. `rule` — `reference-semantics/semantics/float.k:136` — attributes: none

   `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)`

476. `rule` — `reference-semantics/semantics/float.k:137` — attributes: none

   `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))`

477. `rule` — `reference-semantics/semantics/float.k:138` — attributes: none

   `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)`

478. `rule` — `reference-semantics/semantics/float.k:139` — attributes: none

   `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))`

479. `syntax` — `reference-semantics/semantics/float.k:142` — attributes: function, no-evaluators, symbol, total

   `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`

480. `rule` — `reference-semantics/semantics/float.k:143` — attributes: concrete

   `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`

481. `rule` — `reference-semantics/semantics/float.k:144` — attributes: none

   `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`

482. `rule` — `reference-semantics/semantics/float.k:145` — attributes: none

   `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`

483. `rule` — `reference-semantics/semantics/float.k:146` — attributes: none

   `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`

484. `rule` — `reference-semantics/semantics/float.k:147` — attributes: none

   `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`

485. `rule` — `reference-semantics/semantics/float.k:148` — attributes: none

   `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)`

486. `rule` — `reference-semantics/semantics/float.k:149` — attributes: none

   `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))`

487. `rule` — `reference-semantics/semantics/float.k:150` — attributes: none

   `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)`

488. `rule` — `reference-semantics/semantics/float.k:151` — attributes: none

   `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))`

489. `rule` — `reference-semantics/semantics/float.k:154` — attributes: none

   `rule applyCmp("==", V:Val, noneV) => V ==K noneV`

490. `rule` — `reference-semantics/semantics/float.k:155` — attributes: none

   `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)`

491. `syntax` — `reference-semantics/semantics/float.k:160` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`

492. `rule` — `reference-semantics/semantics/float.k:161` — attributes: concrete

   `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`

493. `rule` — `reference-semantics/semantics/float.k:162-163` — attributes: none

   `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))`

494. `syntax` — `reference-semantics/semantics/float.k:165` — attributes: function

   `syntax Int ::= headIS(IntSeq) [function]`

495. `rule` — `reference-semantics/semantics/float.k:166` — attributes: none

   `rule headIS(iCons(C:Int, _:IntSeq)) => C`

496. `syntax` — `reference-semantics/semantics/float.k:167` — attributes: function, total

   `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`

497. `rule` — `reference-semantics/semantics/float.k:168` — attributes: none

   `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`

498. `rule` — `reference-semantics/semantics/float.k:169` — attributes: none

   `rule intPartAcc(.IntSeq, A:Int) => A`

499. `rule` — `reference-semantics/semantics/float.k:170` — attributes: none

   `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`

500. `rule` — `reference-semantics/semantics/float.k:171` — attributes: none

   `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))`

501. `syntax` — `reference-semantics/semantics/float.k:173` — attributes: function, total

   `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`

502. `rule` — `reference-semantics/semantics/float.k:174` — attributes: none

   `rule fracPart(.IntSeq) => 0`

503. `rule` — `reference-semantics/semantics/float.k:175` — attributes: none

   `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`

504. `rule` — `reference-semantics/semantics/float.k:176` — attributes: none

   `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`

505. `rule` — `reference-semantics/semantics/float.k:177` — attributes: none

   `rule fracAcc(.IntSeq, A:Int) => A`

506. `rule` — `reference-semantics/semantics/float.k:178` — attributes: none

   `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`

507. `syntax` — `reference-semantics/semantics/float.k:179` — attributes: function, total

   `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`

508. `rule` — `reference-semantics/semantics/float.k:180` — attributes: none

   `rule fracScale(.IntSeq) => 1`

509. `rule` — `reference-semantics/semantics/float.k:181` — attributes: none

   `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`

510. `rule` — `reference-semantics/semantics/float.k:182` — attributes: none

   `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`

511. `rule` — `reference-semantics/semantics/float.k:183` — attributes: none

   `rule fscAcc(.IntSeq, A:Int) => A`

512. `rule` — `reference-semantics/semantics/float.k:184` — attributes: none

   `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`

513. `rule` — `reference-semantics/semantics/float.k:185` — attributes: none

   `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`

514. `rule` — `reference-semantics/semantics/float.k:186` — attributes: none

   `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)`

515. `rule` — `reference-semantics/semantics/float.k:187` — attributes: none

   `rule applyBuiltin("float", F:Float, .Vals)        => F`

516. `syntax` — `reference-semantics/semantics/float.k:190` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`

517. `rule` — `reference-semantics/semantics/float.k:191` — attributes: concrete

   `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`

518. `rule` — `reference-semantics/semantics/float.k:192` — attributes: none

   `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)`

519. `syntax` — `reference-semantics/semantics/float.k:195` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`

520. `rule` — `reference-semantics/semantics/float.k:196` — attributes: concrete

   `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`

521. `rule` — `reference-semantics/semantics/float.k:197` — attributes: none

   `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`

522. `rule` — `reference-semantics/semantics/float.k:198` — attributes: none

   `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`

523. `rule` — `reference-semantics/semantics/float.k:199` — attributes: none

   `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`

524. `rule` — `reference-semantics/semantics/float.k:200` — attributes: none

   `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`

525. `rule` — `reference-semantics/semantics/float.k:201` — attributes: none

   `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`

526. `rule` — `reference-semantics/semantics/float.k:202` — attributes: none

   `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`

527. `rule` — `reference-semantics/semantics/float.k:203` — attributes: none

   `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`

528. `rule` — `reference-semantics/semantics/float.k:204` — attributes: none

   `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`

529. `rule` — `reference-semantics/semantics/float.k:205` — attributes: none

   `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`

530. `rule` — `reference-semantics/semantics/float.k:206` — attributes: none

   `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`

531. `syntax` — `reference-semantics/semantics/float.k:209` — attributes: function, no-evaluators, symbol, total

   `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`

532. `rule` — `reference-semantics/semantics/float.k:210` — attributes: concrete

   `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`

533. `rule` — `reference-semantics/semantics/float.k:211` — attributes: none

   `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`

534. `rule` — `reference-semantics/semantics/float.k:213` — attributes: none

   `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)`

535. `rule` — `reference-semantics/semantics/float.k:214` — attributes: none

   `rule applyBuiltin("float", F:Float, .Vals) => F`

536. `syntax` — `reference-semantics/semantics/float.k:217` — attributes: function, no-evaluators, symbol, total

   `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`

537. `rule` — `reference-semantics/semantics/float.k:218-222` — attributes: concrete

   `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`

538. `syntax` — `reference-semantics/semantics/float.k:223` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`

539. `rule` — `reference-semantics/semantics/float.k:224-226` — attributes: concrete

   `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`

540. `rule` — `reference-semantics/semantics/float.k:227` — attributes: none

   `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)`

541. `rule` — `reference-semantics/semantics/float.k:228` — attributes: none

   `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`

542. `syntax` — `reference-semantics/semantics/float.k:230` — attributes: function, no-evaluators, symbol, total

   `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`

543. `rule` — `reference-semantics/semantics/float.k:231` — attributes: concrete

   `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`

544. `syntax` — `reference-semantics/semantics/float.k:232` — attributes: none

   `syntax KItem ::= "#mathSqrt"`

545. `rule` — `reference-semantics/semantics/float.k:233` — attributes: priority

   `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`

546. `rule` — `reference-semantics/semantics/float.k:234` — attributes: none

   `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`

547. `rule` — `reference-semantics/semantics/float.k:235` — attributes: none

   `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>`

548. `syntax` — `reference-semantics/semantics/float.k:243` — attributes: none

   `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`

549. `rule` — `reference-semantics/semantics/float.k:244` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`

550. `rule` — `reference-semantics/semantics/float.k:245` — attributes: none

   `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`

551. `rule` — `reference-semantics/semantics/float.k:246` — attributes: none

   `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`

552. `rule` — `reference-semantics/semantics/float.k:247` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>`

553. `syntax` — `reference-semantics/semantics/float.k:250` — attributes: none

   `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`

554. `rule` — `reference-semantics/semantics/float.k:251` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`

555. `rule` — `reference-semantics/semantics/float.k:252` — attributes: none

   `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`

556. `rule` — `reference-semantics/semantics/float.k:253` — attributes: none

   `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`

557. `rule` — `reference-semantics/semantics/float.k:254` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>`

558. `syntax` — `reference-semantics/semantics/float.k:261` — attributes: none

   `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`

559. `rule` — `reference-semantics/semantics/float.k:262-263` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>`

560. `rule` — `reference-semantics/semantics/float.k:265` — attributes: none

   `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`

561. `rule` — `reference-semantics/semantics/float.k:266` — attributes: none

   `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`

562. `rule` — `reference-semantics/semantics/float.k:267-268` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>`

563. `rule` — `reference-semantics/semantics/float.k:270-271` — attributes: none

   `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>`

564. `syntax` — `reference-semantics/semantics/functions.k:8-11` — attributes: none

   `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall"`

565. `rule` — `reference-semantics/semantics/functions.k:14-16` — attributes: none

   `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`

566. `syntax` — `reference-semantics/semantics/functions.k:18` — attributes: none

   `syntax Expr ::= closureExpr(ParamNames, Stmts)`

567. `rule` — `reference-semantics/semantics/functions.k:19-20` — attributes: none

   `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>`

568. `syntax` — `reference-semantics/semantics/functions.k:27` — attributes: none

   `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)`

569. `syntax` — `reference-semantics/semantics/functions.k:31-32` — attributes: none

   `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`

570. `rule` — `reference-semantics/semantics/functions.k:33-35` — attributes: none

   `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`

571. `rule` — `reference-semantics/semantics/functions.k:36-40` — attributes: none

   `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`

572. `rule` — `reference-semantics/semantics/functions.k:42-45` — attributes: none

   `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`

573. `rule` — `reference-semantics/semantics/functions.k:47-49` — attributes: none

   `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`

574. `rule` — `reference-semantics/semantics/functions.k:50-52` — attributes: none

   `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`

575. `rule` — `reference-semantics/semantics/functions.k:53-57` — attributes: none

   `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`

576. `rule` — `reference-semantics/semantics/functions.k:59-60` — attributes: none

   `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>`

577. `rule` — `reference-semantics/semantics/functions.k:63` — attributes: none

   `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`

578. `rule` — `reference-semantics/semantics/functions.k:64-66` — attributes: none

   `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>`

579. `rule` — `reference-semantics/semantics/functions.k:68-71` — attributes: none

   `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`

580. `rule` — `reference-semantics/semantics/functions.k:78-79` — attributes: none

   `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`

581. `rule` — `reference-semantics/semantics/functions.k:80-81` — attributes: none

   `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>`

582. `rule` — `reference-semantics/semantics/functions.k:85-90` — attributes: none

   `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`

583. `rule` — `reference-semantics/semantics/int.k:7` — attributes: none

   `rule applyUn("-", I:Int) => 0 -Int I`

584. `rule` — `reference-semantics/semantics/int.k:9` — attributes: none

   `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2`

585. `rule` — `reference-semantics/semantics/int.k:11` — attributes: none

   `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`

586. `rule` — `reference-semantics/semantics/int.k:12` — attributes: none

   `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`

587. `rule` — `reference-semantics/semantics/int.k:13` — attributes: none

   `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2`

588. `rule` — `reference-semantics/semantics/int.k:14` — attributes: none

   `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2`

589. `rule` — `reference-semantics/semantics/int.k:15` — attributes: none

   `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)`

590. `rule` — `reference-semantics/semantics/int.k:16` — attributes: none

   `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2`

591. `rule` — `reference-semantics/semantics/int.k:17` — attributes: none

   `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`

592. `syntax` — `reference-semantics/semantics/int.k:19` — attributes: function

   `syntax Int ::= pyMod(Int, Int) [function]`

593. `rule` — `reference-semantics/semantics/int.k:20` — attributes: none

   `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`

594. `rule` — `reference-semantics/semantics/int.k:22` — attributes: none

   `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2`

595. `rule` — `reference-semantics/semantics/int.k:23` — attributes: none

   `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2`

596. `rule` — `reference-semantics/semantics/int.k:24` — attributes: none

   `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2`

597. `rule` — `reference-semantics/semantics/int.k:25` — attributes: none

   `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2`

598. `rule` — `reference-semantics/semantics/int.k:26` — attributes: none

   `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2`

599. `rule` — `reference-semantics/semantics/int.k:27` — attributes: none

   `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2`

600. `syntax` — `reference-semantics/semantics/iter.k:8` — attributes: none

   `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`

601. `rule` — `reference-semantics/semantics/list.k:9` — attributes: none

   `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>`

602. `rule` — `reference-semantics/semantics/list.k:10` — attributes: none

   `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>`

603. `syntax` — `reference-semantics/semantics/list.k:13` — attributes: none

   `syntax ApplyK ::= "toList"`

604. `rule` — `reference-semantics/semantics/list.k:14` — attributes: none

   `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`

605. `rule` — `reference-semantics/semantics/list.k:15` — attributes: none

   `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>`

606. `syntax` — `reference-semantics/semantics/list.k:18` — attributes: function, total

   `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`

607. `rule` — `reference-semantics/semantics/list.k:19` — attributes: none

   `rule valSeqConcat(.ValSeq, T:ValSeq)                => T`

608. `rule` — `reference-semantics/semantics/list.k:20` — attributes: none

   `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))`

609. `rule` — `reference-semantics/semantics/list.k:24-25` — attributes: priority

   `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`

610. `rule` — `reference-semantics/semantics/list.k:27` — attributes: none

   `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`

611. `rule` — `reference-semantics/semantics/list.k:28` — attributes: none

   `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)`

612. `syntax` — `reference-semantics/semantics/list.k:33` — attributes: function, total

   `syntax Bool ::= hasRefVS(ValSeq) [function, total]`

613. `rule` — `reference-semantics/semantics/list.k:34` — attributes: none

   `rule hasRefVS(.ValSeq)                => false`

614. `rule` — `reference-semantics/semantics/list.k:35` — attributes: none

   `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`

615. `syntax` — `reference-semantics/semantics/list.k:37-38` — attributes: function

   `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map)        [function]`

616. `rule` — `reference-semantics/semantics/list.k:39` — attributes: none

   `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true`

617. `rule` — `reference-semantics/semantics/list.k:40` — attributes: none

   `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false`

618. `rule` — `reference-semantics/semantics/list.k:41` — attributes: none

   `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false`

619. `rule` — `reference-semantics/semantics/list.k:42-43` — attributes: none

   `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`

620. `rule` — `reference-semantics/semantics/list.k:45` — attributes: none

   `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)`

621. `rule` — `reference-semantics/semantics/list.k:47` — attributes: none

   `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)`

622. `rule` — `reference-semantics/semantics/list.k:49` — attributes: none

   `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`

623. `rule` — `reference-semantics/semantics/list.k:50` — attributes: owise

   `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]`

624. `rule` — `reference-semantics/semantics/list.k:53-55` — attributes: priority

   `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]`

625. `syntax` — `reference-semantics/semantics/list.k:58` — attributes: none

   `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`

626. `rule` — `reference-semantics/semantics/list.k:59` — attributes: none

   `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`

627. `rule` — `reference-semantics/semantics/list.k:60` — attributes: none

   `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`

628. `rule` — `reference-semantics/semantics/list.k:61` — attributes: none

   `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`

629. `rule` — `reference-semantics/semantics/list.k:62` — attributes: none

   `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`

630. `rule` — `reference-semantics/semantics/list.k:63` — attributes: none

   `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>`

631. `rule` — `reference-semantics/semantics/list.k:65` — attributes: none

   `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>`

632. `rule` — `reference-semantics/semantics/list.k:67` — attributes: none

   `rule <k> B:Bool ~> #notB => notBool B ... </k>`

633. `syntax` — `reference-semantics/semantics/methods.k:10` — attributes: function

   `syntax Val ::= applyMethod(Val, String, Vals) [function]`

634. `rule` — `reference-semantics/semantics/methods.k:13` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`

635. `rule` — `reference-semantics/semantics/methods.k:14` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`

636. `rule` — `reference-semantics/semantics/methods.k:15` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`

637. `rule` — `reference-semantics/semantics/methods.k:16` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)`

638. `rule` — `reference-semantics/semantics/methods.k:19` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))`

639. `rule` — `reference-semantics/semantics/methods.k:20` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))`

640. `rule` — `reference-semantics/semantics/methods.k:21` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))`

641. `rule` — `reference-semantics/semantics/methods.k:26` — attributes: none

   `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`

642. `syntax` — `reference-semantics/semantics/methods.k:27` — attributes: function, total

   `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`

643. `rule` — `reference-semantics/semantics/methods.k:28` — attributes: none

   `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`

644. `rule` — `reference-semantics/semantics/methods.k:29` — attributes: none

   `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`

645. `rule` — `reference-semantics/semantics/methods.k:30-31` — attributes: none

   `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))`

646. `rule` — `reference-semantics/semantics/methods.k:34` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`

647. `syntax` — `reference-semantics/semantics/methods.k:35` — attributes: function

   `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`

648. `rule` — `reference-semantics/semantics/methods.k:36` — attributes: none

   `rule cntSub(.IntSeq, _:IntSeq) => 0`

649. `rule` — `reference-semantics/semantics/methods.k:37` — attributes: none

   `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)`

650. `rule` — `reference-semantics/semantics/methods.k:39` — attributes: none

   `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)`

651. `syntax` — `reference-semantics/semantics/methods.k:41` — attributes: function, total

   `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`

652. `rule` — `reference-semantics/semantics/methods.k:42` — attributes: none

   `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`

653. `rule` — `reference-semantics/semantics/methods.k:43` — attributes: owise

   `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`

654. `rule` — `reference-semantics/semantics/methods.k:44` — attributes: none

   `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0`

655. `rule` — `reference-semantics/semantics/methods.k:47` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`

656. `syntax` — `reference-semantics/semantics/methods.k:48` — attributes: function, total

   `syntax IntSeq ::= trimWS(IntSeq) [function, total]`

657. `rule` — `reference-semantics/semantics/methods.k:49` — attributes: none

   `rule trimWS(.IntSeq) => .IntSeq`

658. `rule` — `reference-semantics/semantics/methods.k:50` — attributes: none

   `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`

659. `rule` — `reference-semantics/semantics/methods.k:51` — attributes: none

   `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`

660. `syntax` — `reference-semantics/semantics/methods.k:52` — attributes: function, total

   `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`

661. `rule` — `reference-semantics/semantics/methods.k:53` — attributes: none

   `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`

662. `rule` — `reference-semantics/semantics/methods.k:54` — attributes: none

   `rule revISAcc(.IntSeq, A:IntSeq) => A`

663. `rule` — `reference-semantics/semantics/methods.k:55` — attributes: none

   `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))`

664. `rule` — `reference-semantics/semantics/methods.k:58` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)`

665. `rule` — `reference-semantics/semantics/methods.k:61` — attributes: none

   `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)`

666. `rule` — `reference-semantics/semantics/methods.k:64` — attributes: none

   `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`

667. `syntax` — `reference-semantics/semantics/methods.k:65` — attributes: function, total

   `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`

668. `rule` — `reference-semantics/semantics/methods.k:66` — attributes: none

   `rule cntOccVS(.ValSeq, _:Val)                => 0`

669. `rule` — `reference-semantics/semantics/methods.k:67` — attributes: none

   `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`

670. `rule` — `reference-semantics/semantics/methods.k:68` — attributes: none

   `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)`

671. `rule` — `reference-semantics/semantics/methods.k:72-74` — attributes: priority

   `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`

672. `syntax` — `reference-semantics/semantics/methods.k:75` — attributes: function

   `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result`

673. `rule` — `reference-semantics/semantics/methods.k:76` — attributes: none

   `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`

674. `rule` — `reference-semantics/semantics/methods.k:77` — attributes: none

   `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))`

675. `rule` — `reference-semantics/semantics/methods.k:79` — attributes: none

   `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)`

676. `syntax` — `reference-semantics/semantics/methods.k:82` — attributes: function

   `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`

677. `rule` — `reference-semantics/semantics/methods.k:83` — attributes: none

   `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC`

678. `rule` — `reference-semantics/semantics/methods.k:84` — attributes: none

   `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`

679. `syntax` — `reference-semantics/semantics/methods.k:85` — attributes: function, total

   `syntax Bool ::= isWSC(Int) [function, total]`

680. `rule` — `reference-semantics/semantics/methods.k:86` — attributes: none

   `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13`

681. `rule` — `reference-semantics/semantics/methods.k:89-91` — attributes: priority

   `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]`

682. `rule` — `reference-semantics/semantics/methods.k:94-96` — attributes: priority

   `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`

683. `syntax` — `reference-semantics/semantics/methods.k:97` — attributes: function

   `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token`

684. `rule` — `reference-semantics/semantics/methods.k:98` — attributes: none

   `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)`

685. `rule` — `reference-semantics/semantics/methods.k:99` — attributes: none

   `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))`

686. `rule` — `reference-semantics/semantics/methods.k:101` — attributes: none

   `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))`

687. `rule` — `reference-semantics/semantics/methods.k:104-105` — attributes: none

   `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`

688. `syntax` — `reference-semantics/semantics/methods.k:106` — attributes: function, total

   `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`

689. `rule` — `reference-semantics/semantics/methods.k:107` — attributes: none

   `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq`

690. `rule` — `reference-semantics/semantics/methods.k:108` — attributes: none

   `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`

691. `rule` — `reference-semantics/semantics/methods.k:109` — attributes: none

   `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)`

692. `syntax` — `reference-semantics/semantics/methods.k:112` — attributes: function, total

   `syntax Bool ::= isUpperC(Int) [function, total]`

693. `rule` — `reference-semantics/semantics/methods.k:113` — attributes: none

   `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`

694. `syntax` — `reference-semantics/semantics/methods.k:115` — attributes: function, total

   `syntax Bool ::= isLowerC(Int) [function, total]`

695. `rule` — `reference-semantics/semantics/methods.k:116` — attributes: none

   `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`

696. `syntax` — `reference-semantics/semantics/methods.k:118` — attributes: function, total

   `syntax Bool ::= isAlphaC(Int) [function, total]`

697. `rule` — `reference-semantics/semantics/methods.k:119` — attributes: none

   `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`

698. `syntax` — `reference-semantics/semantics/methods.k:121` — attributes: function, total

   `syntax Bool ::= isDigitC(Int) [function, total]`

699. `rule` — `reference-semantics/semantics/methods.k:122` — attributes: none

   `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`

700. `syntax` — `reference-semantics/semantics/methods.k:124` — attributes: function, total

   `syntax Bool ::= hasUpper(IntSeq) [function, total]`

701. `rule` — `reference-semantics/semantics/methods.k:125` — attributes: none

   `rule hasUpper(.IntSeq) => false`

702. `rule` — `reference-semantics/semantics/methods.k:126` — attributes: none

   `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`

703. `syntax` — `reference-semantics/semantics/methods.k:128` — attributes: function, total

   `syntax Bool ::= hasLower(IntSeq) [function, total]`

704. `rule` — `reference-semantics/semantics/methods.k:129` — attributes: none

   `rule hasLower(.IntSeq) => false`

705. `rule` — `reference-semantics/semantics/methods.k:130` — attributes: none

   `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`

706. `syntax` — `reference-semantics/semantics/methods.k:132` — attributes: function, total

   `syntax Bool ::= allAlpha(IntSeq) [function, total]`

707. `rule` — `reference-semantics/semantics/methods.k:133` — attributes: none

   `rule allAlpha(.IntSeq) => true`

708. `rule` — `reference-semantics/semantics/methods.k:134` — attributes: none

   `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`

709. `syntax` — `reference-semantics/semantics/methods.k:136` — attributes: function, total

   `syntax Bool ::= allDigit(IntSeq) [function, total]`

710. `rule` — `reference-semantics/semantics/methods.k:137` — attributes: none

   `rule allDigit(.IntSeq) => true`

711. `rule` — `reference-semantics/semantics/methods.k:138` — attributes: none

   `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`

712. `syntax` — `reference-semantics/semantics/methods.k:140` — attributes: function, total

   `syntax Int ::= lowerC(Int) [function, total]`

713. `rule` — `reference-semantics/semantics/methods.k:142` — attributes: none

   `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`

714. `rule` — `reference-semantics/semantics/methods.k:143` — attributes: owise

   `rule lowerC(C:Int) => C         [owise]`

715. `syntax` — `reference-semantics/semantics/methods.k:145` — attributes: function, total

   `syntax Int ::= upperC(Int) [function, total]`

716. `rule` — `reference-semantics/semantics/methods.k:146` — attributes: none

   `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`

717. `rule` — `reference-semantics/semantics/methods.k:147` — attributes: owise

   `rule upperC(C:Int) => C         [owise]`

718. `syntax` — `reference-semantics/semantics/methods.k:149` — attributes: function, total

   `syntax Int ::= swapC(Int) [function, total]`

719. `rule` — `reference-semantics/semantics/methods.k:150` — attributes: none

   `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`

720. `rule` — `reference-semantics/semantics/methods.k:151` — attributes: none

   `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`

721. `rule` — `reference-semantics/semantics/methods.k:152` — attributes: owise

   `rule swapC(C:Int) => C         [owise]`

722. `syntax` — `reference-semantics/semantics/methods.k:154` — attributes: function, total

   `syntax IntSeq ::= mapLower(IntSeq) [function, total]`

723. `rule` — `reference-semantics/semantics/methods.k:155` — attributes: none

   `rule mapLower(.IntSeq) => .IntSeq`

724. `rule` — `reference-semantics/semantics/methods.k:156` — attributes: none

   `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`

725. `syntax` — `reference-semantics/semantics/methods.k:158` — attributes: function, total

   `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`

726. `rule` — `reference-semantics/semantics/methods.k:159` — attributes: none

   `rule mapUpper(.IntSeq) => .IntSeq`

727. `rule` — `reference-semantics/semantics/methods.k:160` — attributes: none

   `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`

728. `syntax` — `reference-semantics/semantics/methods.k:162` — attributes: function, total

   `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`

729. `rule` — `reference-semantics/semantics/methods.k:163` — attributes: none

   `rule mapSwap(.IntSeq) => .IntSeq`

730. `rule` — `reference-semantics/semantics/methods.k:164` — attributes: none

   `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`

731. `syntax` — `reference-semantics/semantics/methods.k:166` — attributes: function, total

   `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`

732. `rule` — `reference-semantics/semantics/methods.k:167` — attributes: none

   `rule startsWith(.IntSeq, _:IntSeq)               => true`

733. `rule` — `reference-semantics/semantics/methods.k:168` — attributes: none

   `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`

734. `rule` — `reference-semantics/semantics/methods.k:169` — attributes: none

   `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`

735. `rule` — `reference-semantics/semantics/operators.k:10` — attributes: none

   `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`

736. `rule` — `reference-semantics/semantics/operators.k:12` — attributes: none

   `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>`

737. `context` — `reference-semantics/semantics/operators.k:15` — attributes: none

   `context Compare(HOLE, _)`

738. `context` — `reference-semantics/semantics/operators.k:16` — attributes: none

   `context Compare(_:Val, CmpOp(_, HOLE))`

739. `rule` — `reference-semantics/semantics/operators.k:17` — attributes: owise

   `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`

740. `rule` — `reference-semantics/semantics/operators.k:19` — attributes: none

   `rule applyCmp("is",     V:Val, noneV) => V ==K noneV`

741. `rule` — `reference-semantics/semantics/operators.k:20` — attributes: none

   `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)`

742. `rule` — `reference-semantics/semantics/operators.k:25-27` — attributes: priority

   `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

743. `rule` — `reference-semantics/semantics/operators.k:28-29` — attributes: none

   `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap>`

744. `rule` — `reference-semantics/semantics/operators.k:34-35` — attributes: none

   `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap>`

745. `rule` — `reference-semantics/semantics/operators.k:38-39` — attributes: none

   `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap>`

746. `rule` — `reference-semantics/semantics/operators.k:44-46` — attributes: priority

   `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

747. `syntax` — `reference-semantics/semantics/range.k:9` — attributes: function, total

   `syntax Bool ::= inRange(Int, Int, Int) [function, total]`

748. `rule` — `reference-semantics/semantics/range.k:10` — attributes: none

   `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`

749. `syntax` — `reference-semantics/semantics/range.k:12` — attributes: function

   `syntax Int ::= rangeLen(Int, Int, Int) [function]`

750. `rule` — `reference-semantics/semantics/range.k:13` — attributes: none

   `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST`

751. `rule` — `reference-semantics/semantics/range.k:15` — attributes: none

   `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)`

752. `rule` — `reference-semantics/semantics/range.k:17` — attributes: none

   `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0`

753. `rule` — `reference-semantics/semantics/range.k:20-21` — attributes: none

   `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>`

754. `rule` — `reference-semantics/semantics/range.k:23` — attributes: none

   `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>`

755. `syntax` — `reference-semantics/semantics/set.k:8` — attributes: none

   `syntax Val ::= setV(IntSeq)`

756. `syntax` — `reference-semantics/semantics/set.k:11` — attributes: function, total

   `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`

757. `rule` — `reference-semantics/semantics/set.k:12` — attributes: none

   `rule codeIn(_:Int, .IntSeq)                => false`

758. `rule` — `reference-semantics/semantics/set.k:13` — attributes: none

   `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)`

759. `syntax` — `reference-semantics/semantics/set.k:16-17` — attributes: function, total

   `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] | dedupFrom(IntSeq, IntSeq)  [function, total]`

760. `rule` — `reference-semantics/semantics/set.k:18` — attributes: none

   `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`

761. `rule` — `reference-semantics/semantics/set.k:19` — attributes: none

   `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`

762. `rule` — `reference-semantics/semantics/set.k:20` — attributes: none

   `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)`

763. `rule` — `reference-semantics/semantics/set.k:22` — attributes: none

   `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))`

764. `syntax` — `reference-semantics/semantics/set.k:25` — attributes: function, total

   `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`

765. `rule` — `reference-semantics/semantics/set.k:26` — attributes: none

   `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)`

766. `rule` — `reference-semantics/semantics/set.k:27` — attributes: none

   `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))`

767. `syntax` — `reference-semantics/semantics/set.k:31` — attributes: function, total

   `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`

768. `rule` — `reference-semantics/semantics/set.k:32` — attributes: none

   `rule subsetCodes(.IntSeq, _:IntSeq)                => true`

769. `rule` — `reference-semantics/semantics/set.k:33` — attributes: none

   `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`

770. `syntax` — `reference-semantics/semantics/set.k:35` — attributes: function, total

   `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`

771. `rule` — `reference-semantics/semantics/set.k:36` — attributes: none

   `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)`

772. `rule` — `reference-semantics/semantics/set.k:39` — attributes: none

   `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`

773. `syntax` — `reference-semantics/semantics/sort.k:18` — attributes: function, no-evaluators, symbol, total

   `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`

774. `syntax` — `reference-semantics/semantics/sort.k:19` — attributes: function

   `syntax ValSeq ::= insVS(Int, ValSeq) [function]`

775. `rule` — `reference-semantics/semantics/sort.k:20` — attributes: concrete

   `rule sortVS(.ValSeq)                => .ValSeq          [concrete]`

776. `rule` — `reference-semantics/semantics/sort.k:21` — attributes: concrete

   `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`

777. `rule` — `reference-semantics/semantics/sort.k:22` — attributes: concrete

   `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]`

778. `rule` — `reference-semantics/semantics/sort.k:23` — attributes: concrete

   `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`

779. `rule` — `reference-semantics/semantics/sort.k:24` — attributes: concrete

   `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]`

780. `syntax` — `reference-semantics/semantics/sort.k:26` — attributes: function

   `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`

781. `rule` — `reference-semantics/semantics/sort.k:27` — attributes: concrete

   `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`

782. `rule` — `reference-semantics/semantics/sort.k:28` — attributes: concrete

   `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`

783. `rule` — `reference-semantics/semantics/sort.k:29` — attributes: none

   `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))`

784. `rule` — `reference-semantics/semantics/sort.k:31` — attributes: none

   `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))`

785. `rule` — `reference-semantics/semantics/sort.k:36-37` — attributes: none

   `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>`

786. `rule` — `reference-semantics/semantics/sort.k:40-42` — attributes: priority

   `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]`

787. `syntax` — `reference-semantics/semantics/sort.k:49` — attributes: function, no-evaluators, symbol, total

   `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`

788. `syntax` — `reference-semantics/semantics/sort.k:51-52` — attributes: function, total

   `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`

789. `rule` — `reference-semantics/semantics/sort.k:53` — attributes: none

   `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`

790. `rule` — `reference-semantics/semantics/sort.k:54` — attributes: none

   `rule revVSAcc(.ValSeq, A:ValSeq) => A`

791. `rule` — `reference-semantics/semantics/sort.k:55` — attributes: none

   `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`

792. `syntax` — `reference-semantics/semantics/sort.k:57` — attributes: function, total

   `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`

793. `rule` — `reference-semantics/semantics/sort.k:58` — attributes: none

   `rule condRev(S:ValSeq, false) => S`

794. `rule` — `reference-semantics/semantics/sort.k:59` — attributes: none

   `rule condRev(S:ValSeq, true)  => revVS(S)`

795. `rule` — `reference-semantics/semantics/sort.k:61-62` — attributes: none

   `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`

796. `rule` — `reference-semantics/semantics/sort.k:63-64` — attributes: none

   `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`

797. `rule` — `reference-semantics/semantics/sort.k:65-66` — attributes: none

   `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>`

798. `rule` — `reference-semantics/semantics/str.k:8` — attributes: none

   `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>`

799. `rule` — `reference-semantics/semantics/str.k:9-10` — attributes: none

   `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>`

800. `syntax` — `reference-semantics/semantics/str.k:13` — attributes: function

   `syntax IntSeq ::= strToCodes(String) [function]`

801. `rule` — `reference-semantics/semantics/str.k:14` — attributes: none

   `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`

802. `rule` — `reference-semantics/semantics/str.k:15` — attributes: none

   `rule strToCodes("") => .IntSeq`

803. `rule` — `reference-semantics/semantics/str.k:16` — attributes: none

   `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))`

804. `syntax` — `reference-semantics/semantics/str.k:20` — attributes: function, total

   `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`

805. `rule` — `reference-semantics/semantics/str.k:21` — attributes: none

   `rule seqConcat(.IntSeq, T:IntSeq)                => T`

806. `rule` — `reference-semantics/semantics/str.k:22` — attributes: none

   `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`

807. `rule` — `reference-semantics/semantics/str.k:24` — attributes: none

   `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`

808. `rule` — `reference-semantics/semantics/str.k:25` — attributes: none

   `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`

809. `rule` — `reference-semantics/semantics/str.k:26` — attributes: none

   `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)`

810. `rule` — `reference-semantics/semantics/str.k:29` — attributes: none

   `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`

811. `rule` — `reference-semantics/semantics/str.k:30` — attributes: none

   `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`

812. `syntax` — `reference-semantics/semantics/str.k:32` — attributes: function, total

   `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`

813. `rule` — `reference-semantics/semantics/str.k:33` — attributes: none

   `rule strPrefix(.IntSeq, _:IntSeq)               => true`

814. `rule` — `reference-semantics/semantics/str.k:34` — attributes: none

   `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`

815. `rule` — `reference-semantics/semantics/str.k:35` — attributes: none

   `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`

816. `syntax` — `reference-semantics/semantics/str.k:37` — attributes: function, total

   `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`

817. `rule` — `reference-semantics/semantics/str.k:38` — attributes: none

   `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)`

818. `rule` — `reference-semantics/semantics/str.k:39` — attributes: none

   `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)`

819. `rule` — `reference-semantics/semantics/str.k:40` — attributes: none

   `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)`

820. `syntax` — `reference-semantics/semantics/str.k:48` — attributes: function, total

   `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`

821. `rule` — `reference-semantics/semantics/str.k:49` — attributes: none

   `rule strLt(.IntSeq, .IntSeq)                => false`

822. `rule` — `reference-semantics/semantics/str.k:50` — attributes: none

   `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`

823. `rule` — `reference-semantics/semantics/str.k:51` — attributes: none

   `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`

824. `rule` — `reference-semantics/semantics/str.k:52` — attributes: none

   `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B`

825. `rule` — `reference-semantics/semantics/str.k:53` — attributes: none

   `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B`

826. `rule` — `reference-semantics/semantics/str.k:54` — attributes: none

   `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`

827. `rule` — `reference-semantics/semantics/str.k:56` — attributes: none

   `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`

828. `rule` — `reference-semantics/semantics/str.k:57` — attributes: none

   `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`

829. `rule` — `reference-semantics/semantics/str.k:58` — attributes: none

   `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`

830. `rule` — `reference-semantics/semantics/str.k:59` — attributes: none

   `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`

831. `syntax` — `reference-semantics/semantics/subscript.k:11` — attributes: function, total

   `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`

832. `rule` — `reference-semantics/semantics/subscript.k:12` — attributes: none

   `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V`

833. `rule` — `reference-semantics/semantics/subscript.k:13` — attributes: none

   `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)`

834. `syntax` — `reference-semantics/semantics/subscript.k:16` — attributes: function

   `syntax Int ::= intSeqAt(IntSeq, Int) [function]`

835. `rule` — `reference-semantics/semantics/subscript.k:17` — attributes: none

   `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C`

836. `rule` — `reference-semantics/semantics/subscript.k:18` — attributes: none

   `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)`

837. `syntax` — `reference-semantics/semantics/subscript.k:21` — attributes: function, total

   `syntax Int ::= normIdx(Int, Int) [function, total]`

838. `rule` — `reference-semantics/semantics/subscript.k:22` — attributes: none

   `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`

839. `rule` — `reference-semantics/semantics/subscript.k:23` — attributes: none

   `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0`

840. `context` — `reference-semantics/semantics/subscript.k:27` — attributes: none

   `context Subscript(HOLE, _)`

841. `context` — `reference-semantics/semantics/subscript.k:28` — attributes: none

   `context Subscript(_:Val, HOLE:Expr)`

842. `rule` — `reference-semantics/semantics/subscript.k:31-33` — attributes: priority

   `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

843. `rule` — `reference-semantics/semantics/subscript.k:35` — attributes: none

   `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`

844. `syntax` — `reference-semantics/semantics/subscript.k:37` — attributes: function

   `syntax Val ::= applyIndex(Val, Int) [function]`

845. `rule` — `reference-semantics/semantics/subscript.k:38` — attributes: none

   `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`

846. `rule` — `reference-semantics/semantics/subscript.k:39` — attributes: none

   `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`

847. `rule` — `reference-semantics/semantics/subscript.k:40-41` — attributes: none

   `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))`

848. `syntax` — `reference-semantics/semantics/subscript.k:44-47` — attributes: none

   `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`

849. `syntax` — `reference-semantics/semantics/subscript.k:49` — attributes: none

   `syntax OptInt ::= "noB" | someB(Int)`

850. `rule` — `reference-semantics/semantics/subscript.k:50` — attributes: none

   `rule <k> #evalB(NoBound)  => noB ... </k>`

851. `rule` — `reference-semantics/semantics/subscript.k:51` — attributes: none

   `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>`

852. `rule` — `reference-semantics/semantics/subscript.k:52` — attributes: none

   `rule <k> I:Int ~> #toSome => someB(I) ... </k>`

853. `rule` — `reference-semantics/semantics/subscript.k:54` — attributes: none

   `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`

854. `rule` — `reference-semantics/semantics/subscript.k:55` — attributes: none

   `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`

855. `rule` — `reference-semantics/semantics/subscript.k:56` — attributes: none

   `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>`

856. `rule` — `reference-semantics/semantics/subscript.k:58-60` — attributes: priority

   `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`

857. `rule` — `reference-semantics/semantics/subscript.k:61` — attributes: none

   `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`

858. `syntax` — `reference-semantics/semantics/subscript.k:63` — attributes: function

   `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`

859. `rule` — `reference-semantics/semantics/subscript.k:64-65` — attributes: none

   `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`

860. `rule` — `reference-semantics/semantics/subscript.k:66-67` — attributes: none

   `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`

861. `rule` — `reference-semantics/semantics/subscript.k:68-69` — attributes: none

   `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))`

862. `syntax` — `reference-semantics/semantics/subscript.k:72` — attributes: function, total

   `syntax Int ::= slStep(OptInt) [function, total]`

863. `rule` — `reference-semantics/semantics/subscript.k:73` — attributes: none

   `rule slStep(noB)          => 1`

864. `rule` — `reference-semantics/semantics/subscript.k:74` — attributes: none

   `rule slStep(someB(S:Int)) => S`

865. `syntax` — `reference-semantics/semantics/subscript.k:76` — attributes: function

   `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`

866. `rule` — `reference-semantics/semantics/subscript.k:77` — attributes: none

   `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0`

867. `rule` — `reference-semantics/semantics/subscript.k:79` — attributes: none

   `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1`

868. `rule` — `reference-semantics/semantics/subscript.k:81` — attributes: none

   `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`

869. `syntax` — `reference-semantics/semantics/subscript.k:83` — attributes: function

   `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`

870. `rule` — `reference-semantics/semantics/subscript.k:84` — attributes: none

   `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN`

871. `rule` — `reference-semantics/semantics/subscript.k:86` — attributes: none

   `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1`

872. `rule` — `reference-semantics/semantics/subscript.k:88` — attributes: none

   `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`

873. `syntax` — `reference-semantics/semantics/subscript.k:90` — attributes: function, total

   `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`

874. `rule` — `reference-semantics/semantics/subscript.k:91` — attributes: none

   `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)`

875. `rule` — `reference-semantics/semantics/subscript.k:93` — attributes: none

   `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)`

876. `syntax` — `reference-semantics/semantics/subscript.k:96` — attributes: function, total

   `syntax Int ::= clampLo(Int, Int) [function, total]`

877. `rule` — `reference-semantics/semantics/subscript.k:97` — attributes: none

   `rule clampLo(J:Int, _STEP:Int) => J`

878. `rule` — `reference-semantics/semantics/subscript.k:99` — attributes: none

   `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi`

879. `syntax` — `reference-semantics/semantics/subscript.k:102` — attributes: function, total

   `syntax Int ::= clampHi(Int, Int, Int) [function, total]`

880. `rule` — `reference-semantics/semantics/subscript.k:103` — attributes: none

   `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I`

881. `rule` — `reference-semantics/semantics/subscript.k:105` — attributes: none

   `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi`

882. `syntax` — `reference-semantics/semantics/subscript.k:109` — attributes: function

   `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`

883. `rule` — `reference-semantics/semantics/subscript.k:110-111` — attributes: none

   `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))`

884. `rule` — `reference-semantics/semantics/subscript.k:113` — attributes: none

   `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq`

885. `syntax` — `reference-semantics/semantics/subscript.k:116` — attributes: function

   `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`

886. `rule` — `reference-semantics/semantics/subscript.k:117-118` — attributes: none

   `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))`

887. `rule` — `reference-semantics/semantics/subscript.k:120` — attributes: none

   `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq`

888. `syntax` — `reference-semantics/semantics/syntax.k:9-30` — attributes: macro, seqstrict, strict

   `syntax Expr ::= "Int"      "(" Int ")" | "Float"    "(" Float ")" | "Bool"     "(" Bool ")" | "Name"     "(" String ")" | "Str"      "(" String ")" | "UnaryOp"  "(" String "," Expr ")" [strict(2)] | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp"    "(" String "," Exprs ")" | "ListExpr"  "(" Exprs ")" | "DictExpr"  "(" Entries ")" | "ListComp"  "(" Expr "," CompFors ")" [macro] | "GenExp"    "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda"    "(" Params "," Expr ")" | "KwArg"     "(" String "," Expr ")" | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call"      "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare"   "(" Expr "," CmpOp ")"`

889. `syntax` — `reference-semantics/semantics/syntax.k:32` — attributes: none

   `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"`

890. `syntax` — `reference-semantics/semantics/syntax.k:33` — attributes: none

   `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"`

891. `syntax` — `reference-semantics/semantics/syntax.k:34` — attributes: none

   `syntax Entries  ::= List{Entry, ","}`

892. `syntax` — `reference-semantics/semantics/syntax.k:35` — attributes: none

   `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`

893. `syntax` — `reference-semantics/semantics/syntax.k:36` — attributes: none

   `syntax CompFors ::= List{CompFor, ""}`

894. `syntax` — `reference-semantics/semantics/syntax.k:37` — attributes: none

   `syntax Exprs    ::= List{Expr, ","}`

895. `syntax` — `reference-semantics/semantics/syntax.k:38` — attributes: none

   `syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`

896. `syntax` — `reference-semantics/semantics/syntax.k:39` — attributes: none

   `syntax Bound    ::= Expr | "NoBound"`

897. `syntax` — `reference-semantics/semantics/syntax.k:41-54` — attributes: strict

   `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] | "Import"    "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While"     "(" Expr "," Stmts ")" | "Break" | "Continue" | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return"    "(" Expr ")" [strict] | "Assert"    "(" Expr ")" [strict] | "Expr"      "(" Expr ")" [strict] | "FuncDef"   "(" String "," Params "," Stmts ")" | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`

898. `syntax` — `reference-semantics/semantics/syntax.k:56` — attributes: none

   `syntax Stmts      ::= List{Stmt, ""}`

899. `syntax` — `reference-semantics/semantics/syntax.k:57` — attributes: none

   `syntax Params     ::= "Params" "(" ParamNames ")"`

900. `syntax` — `reference-semantics/semantics/syntax.k:58` — attributes: none

   `syntax CellVars   ::= "CellVars" "(" ParamNames ")"`

901. `syntax` — `reference-semantics/semantics/syntax.k:59` — attributes: none

   `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"`

902. `syntax` — `reference-semantics/semantics/syntax.k:60` — attributes: none

   `syntax ParamNames ::= List{String, ","}`

903. `syntax` — `reference-semantics/semantics/syntax.k:61` — attributes: none

   `syntax Module     ::= "Module" "(" Stmts ")"`

904. `rule` — `reference-semantics/semantics/tuple.k:10` — attributes: none

   `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>`

905. `rule` — `reference-semantics/semantics/tuple.k:11` — attributes: none

   `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>`

906. `syntax` — `reference-semantics/semantics/tuple.k:14` — attributes: none

   `syntax ApplyK ::= "toTuple"`

907. `rule` — `reference-semantics/semantics/tuple.k:15` — attributes: none

   `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`

908. `rule` — `reference-semantics/semantics/tuple.k:16` — attributes: none

   `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`

909. `rule` — `reference-semantics/semantics/tuple.k:18` — attributes: none

   `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B`

910. `rule` — `reference-semantics/semantics/tuple.k:20` — attributes: none

   `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`

911. `rule` — `reference-semantics/semantics/tuple.k:21` — attributes: none

   `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>`

912. `rule` — `reference-semantics/semantics/tuple.k:23` — attributes: none

   `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`

913. `syntax` — `reference-semantics/semantics/tuple.k:24` — attributes: function

   `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`

914. `rule` — `reference-semantics/semantics/tuple.k:25` — attributes: none

   `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`

915. `rule` — `reference-semantics/semantics/tuple.k:26` — attributes: none

   `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)`

916. `rule` — `reference-semantics/semantics/tuple.k:28` — attributes: none

   `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)`

917. `syntax` — `reference-semantics/semantics/tuple.k:31` — attributes: none

   `syntax KItem ::= #bindTgt(Expr, Val)`

918. `rule` — `reference-semantics/semantics/tuple.k:32-34` — attributes: none

   `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`

919. `rule` — `reference-semantics/semantics/tuple.k:35-37` — attributes: none

   `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`

920. `rule` — `reference-semantics/semantics/tuple.k:42` — attributes: none

   `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`

921. `rule` — `reference-semantics/semantics/tuple.k:43` — attributes: none

   `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`

922. `rule` — `reference-semantics/semantics/tuple.k:44-46` — attributes: priority

   `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

923. `syntax` — `reference-semantics/semantics/tuple.k:49` — attributes: none

   `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`

924. `rule` — `reference-semantics/semantics/tuple.k:50` — attributes: none

   `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`

925. `rule` — `reference-semantics/semantics/tuple.k:51` — attributes: none

   `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`

926. `rule` — `reference-semantics/semantics/tuple.k:52-54` — attributes: priority

   `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

927. `rule` — `reference-semantics/semantics/tuple.k:55-56` — attributes: none

   `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`

928. `rule` — `reference-semantics/semantics/tuple.k:57` — attributes: none

   `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`

929. `syntax` — `verification.k:8-9` — attributes: none

   `syntax GridRows ::= ".GridRows" | gCons(IntSeq, GridRows)`

930. `syntax` — `verification.k:11-12` — attributes: function, total

   `syntax ValSeq ::= rowVals(IntSeq) [function, total] | gridVals(GridRows) [function, total]`

931. `rule` — `verification.k:14` — attributes: none

   `rule rowVals(.IntSeq)                 => .ValSeq`

932. `rule` — `verification.k:15` — attributes: none

   `rule rowVals(iCons(I:Int, IS:IntSeq)) => vCons(I, rowVals(IS))`

933. `rule` — `verification.k:17` — attributes: none

   `rule gridVals(.GridRows) => .ValSeq`

934. `rule` — `verification.k:18-19` — attributes: none

   `rule gridVals(gCons(IS:IntSeq, GS:GridRows)) => vCons(list(rowVals(IS)), gridVals(GS))`

935. `syntax` — `verification.k:24-28` — attributes: function, total

   `syntax Int ::= rowSum(IntSeq) [function, total] | rowTotal(Int, IntSeq) [function, total] | ceilDiv(Int, Int) [function, total] | fillTotal(Int, GridRows, Int) [function, total] | maxFillSpec(GridRows, Int) [function, total]`

936. `rule` — `verification.k:30` — attributes: none

   `rule rowSum(IS:IntSeq) => rowTotal(0, IS)`

937. `rule` — `verification.k:31` — attributes: none

   `rule rowTotal(A:Int, .IntSeq) => A`

938. `rule` — `verification.k:32-33` — attributes: none

   `rule rowTotal(A:Int, iCons(I:Int, IS:IntSeq)) => rowTotal(A +Int I, IS)`

939. `rule` — `verification.k:35-36` — attributes: none

   `rule ceilDiv(N:Int, C:Int) => ((N +Int C -Int 1) -Int pyMod(N +Int C -Int 1, C)) /Int C`

940. `rule` — `verification.k:38` — attributes: none

   `rule fillTotal(A:Int, .GridRows, _C:Int) => A`

941. `rule` — `verification.k:39-40` — attributes: none

   `rule fillTotal(A:Int, gCons(IS:IntSeq, GS:GridRows), C:Int) => fillTotal(A +Int ceilDiv(rowSum(IS), C), GS, C)`

942. `rule` — `verification.k:41` — attributes: none

   `rule maxFillSpec(GS:GridRows, C:Int) => fillTotal(0, GS, C)`

943. `syntax` — `verification.k:44` — attributes: macro

   `syntax Stmts ::= "MAX_FILL_LOOP_BODY" [macro]`

944. `rule` — `verification.k:45-57` — attributes: none

   `rule MAX_FILL_LOOP_BODY => Assign(Name("water"), Call(Name("sum"), Name("row"))) AugAssign( Name("result"), "+", BinOp( "//", BinOp( "-", BinOp("+", Name("water"), Name("capacity")), Int(1)), Name("capacity"))) .Stmts`

945. `syntax` — `verification.k:70-71` — attributes: none

   `syntax ValSeq ::= symRow(IntSeq) | symGrid(GridRows)`

946. `syntax` — `verification.k:73-74` — attributes: none

   `syntax KItem ::= #typedSum(IntSeq, Int) | #typedLoop(GridRows, Expr, Stmts)`

947. `rule` — `verification.k:79-83` — attributes: priority

   `rule <k> #sumAcc(list(symRow(IS:IntSeq)), A:Int) => #typedSum(IS, A) ... </k> [priority(40)]`

948. `rule` — `verification.k:85-88` — attributes: none

   `rule <k> #typedSum(.IntSeq, A:Int) => #iterNext(list(.ValSeq)) ~> #sumCont(A) ... </k>`

949. `rule` — `verification.k:90-93` — attributes: none

   `rule <k> #typedSum(iCons(I:Int, IS:IntSeq), A:Int) => #iterNext(list(vCons(I, symRow(IS)))) ~> #sumCont(A) ... </k>`

950. `rule` — `verification.k:95-102` — attributes: priority

   `rule <k> #loop( list(symGrid(GS:GridRows)), T:Expr, B:Stmts) => #typedLoop(GS, T, B) ... </k> [priority(40)]`

951. `rule` — `verification.k:104-107` — attributes: none

   `rule <k> #typedLoop(.GridRows, T:Expr, B:Stmts) => #iterNext(list(.ValSeq)) ~> #loopStep(T, B) ... </k>`

952. `rule` — `verification.k:109-117` — attributes: none

   `rule <k> #typedLoop( gCons(IS:IntSeq, GS:GridRows), T:Expr, B:Stmts) => #iterNext( list(vCons(list(symRow(IS)), symGrid(GS)))) ~> #loopStep(T, B) ... </k>`

953. `syntax` — `verification.k:119` — attributes: function, total

   `syntax Val ::= finalRow(GridRows, Val) [function, total]`

954. `syntax` — `verification.k:120` — attributes: function, total

   `syntax Int ::= finalWater(GridRows, Int) [function, total]`

955. `rule` — `verification.k:122` — attributes: none

   `rule finalRow(.GridRows, V:Val) => V`

956. `rule` — `verification.k:123-124` — attributes: none

   `rule finalRow(gCons(IS:IntSeq, GS:GridRows), _V:Val) => finalRow(GS, list(symRow(IS)))`

957. `rule` — `verification.k:126` — attributes: none

   `rule finalWater(.GridRows, W:Int) => W`

958. `rule` — `verification.k:127-128` — attributes: none

   `rule finalWater(gCons(IS:IntSeq, GS:GridRows), _W:Int) => finalWater(GS, rowSum(IS))`

959. `syntax` — `verification.k:137` — attributes: none

   `syntax KItem ::= #runMaxFill(GridRows, Int)`

960. `rule` — `verification.k:138-154` — attributes: none

   `rule <k> #runMaxFill(GS:GridRows, C:Int) => #loadAll( Module( FuncDef( "max_fill", Params("grid", "capacity"), Assign(Name("result"), Int(0)) Assign(Name("row"), Int(0)) Assign(Name("water"), Int(0)) For( Name("row"), Name("grid"), MAX_FILL_LOOP_BODY) Return(Name("result"))))) ~> Call(Name("max_fill"), list(symGrid(GS)), C) ... </k>`

961. `claim` — `spec.k:8-11` — attributes: none

   `claim [bridge-sum-empty]: <k> #sumAcc(list(rowVals(.IntSeq)), A:Int) ~> K:K => #iterNext(list(.ValSeq)) ~> #sumCont(A) ~> K </k>`

962. `claim` — `spec.k:13-21` — attributes: none

   `claim [bridge-sum-step]: <k> #sumAcc( list(rowVals(iCons(I:Int, IS:IntSeq))), A:Int) ~> K:K => #iterNext(list(vCons(I, rowVals(IS)))) ~> #sumCont(A) ~> K </k>`

963. `claim` — `spec.k:23-32` — attributes: none

   `claim [bridge-loop-empty]: <k> #loop( list(gridVals(.GridRows)), T:Expr, B:Stmts) ~> K:K => #iterNext(list(.ValSeq)) ~> #loopStep(T, B) ~> K </k>`

964. `claim` — `spec.k:34-44` — attributes: none

   `claim [bridge-loop-step]: <k> #loop( list(gridVals(gCons(IS:IntSeq, GS:GridRows))), T:Expr, B:Stmts) ~> K:K => #iterNext( list(vCons(list(rowVals(IS)), gridVals(GS)))) ~> #loopStep(T, B) ~> K </k>`

965. `claim` — `spec.k:51-54` — attributes: none

   `claim [sum-fold]: <k> #sumAcc(list(symRow(IS:IntSeq)), A:Int) ~> K:K => rowTotal(A, IS) ~> K </k>`

966. `claim` — `spec.k:58-87` — attributes: none

   `claim [fill-loop]: <k> #loop( list(symGrid(GS:GridRows)), Name("row"), MAX_FILL_LOOP_BODY) ~> K:K => K </k> <env> 1 </env> <scopes> -1 |-> builtinsScope 0 |-> scope("max_fill" |-> F:Val, parent(-1)) 1 |-> scope( "grid" |-> list(symGrid(INPUT:GridRows)) "capacity" |-> C:Int "result" |-> A:Int "row" |-> RV:Val "water" |-> W:Int, parent(0)) => -1 |-> builtinsScope 0 |-> scope("max_fill" |-> F, parent(-1)) 1 |-> scope( "grid" |-> list(symGrid(INPUT)) "capacity" |-> C "result" |-> fillTotal(A, GS, C) "row" |-> finalRow(GS, RV) "water" |-> finalWater(GS, W), parent(0)) </scopes>`

967. `claim` — `spec.k:91-108` — attributes: none

   `claim [max-fill-correct]: <k> #runMaxFill(GS:GridRows, C:Int) => maxFillSpec(GS, C) </k> <env> 0 </env> <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope => ?FINALSCOPES:Map </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code>`


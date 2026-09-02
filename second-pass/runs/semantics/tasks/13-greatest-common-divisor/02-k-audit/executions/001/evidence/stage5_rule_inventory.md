# Exhaustive K declaration and rule inventory

Generated independently from the fresh scratch source. Each item begins at the cited source line; multi-line bodies, guards, and attributes are normalized onto one line.

## Summary

- Source files: 26
- Inventoried items: 946
- claim: 4
- concrete rule: 37
- configuration: 1
- context: 5
- function syntax: 123
- macro syntax: 9
- opaque-symbol syntax: 23
- ordinary rule: 594
- owise rule: 26
- priority rule: 46
- syntax: 78
- Declarations carrying `total`: 107
- Declarations carrying `functional`: 0
- Rules carrying `simplification`: 0
- Rules carrying a priority: 46
- Declarations carrying `no-evaluators`: 23

## `reference-semantics/semantics/assert.k`

1. `reference-semantics/semantics/assert.k:6` — **ordinary rule**; attributes: `none` — `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)`

2. `reference-semantics/semantics/assert.k:8` — **ordinary rule**; attributes: `none` — `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)`

3. `reference-semantics/semantics/assert.k:13` — **priority rule**; attributes: `priority(40)` — `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## `reference-semantics/semantics/bool.k`

4. `reference-semantics/semantics/bool.k:8` — **ordinary rule**; attributes: `none` — `rule applyUn("not", V:Val) => notBool truthy(V)`

5. `reference-semantics/semantics/bool.k:10` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`

6. `reference-semantics/semantics/bool.k:11` — **ordinary rule**; attributes: `none` — `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2`

7. `reference-semantics/semantics/bool.k:16` — **context**; attributes: `none` — `context BoolOp(_, (HOLE:Expr, _:Exprs))`

8. `reference-semantics/semantics/bool.k:17` — **ordinary rule**; attributes: `none` — `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`

9. `reference-semantics/semantics/bool.k:18` — **ordinary rule**; attributes: `none` — `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)`

10. `reference-semantics/semantics/bool.k:20` — **ordinary rule**; attributes: `none` — `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)`

11. `reference-semantics/semantics/bool.k:22` — **ordinary rule**; attributes: `none` — `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)`

12. `reference-semantics/semantics/bool.k:24` — **ordinary rule**; attributes: `none` — `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)`

13. `reference-semantics/semantics/bool.k:29` — **priority rule**; attributes: `priority(40)` — `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`

14. `reference-semantics/semantics/bool.k:31` — **priority rule**; attributes: `priority(40)` — `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`

15. `reference-semantics/semantics/bool.k:35` — **priority rule**; attributes: `priority(40)` — `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`

16. `reference-semantics/semantics/bool.k:39` — **priority rule**; attributes: `priority(40)` — `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`

17. `reference-semantics/semantics/bool.k:43` — **priority rule**; attributes: `priority(40)` — `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`

## `reference-semantics/semantics/builtins.k`

18. `reference-semantics/semantics/builtins.k:17` — **function syntax**; attributes: `function` — `syntax Val ::= applyBuiltin(String, Vals) [function]`

19. `reference-semantics/semantics/builtins.k:20` — **function syntax**; attributes: `function` — `syntax Int ::= seqLen(Val) [function]`

20. `reference-semantics/semantics/builtins.k:21` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`

21. `reference-semantics/semantics/builtins.k:22` — **ordinary rule**; attributes: `none` — `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)`

22. `reference-semantics/semantics/builtins.k:23` — **ordinary rule**; attributes: `none` — `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)`

23. `reference-semantics/semantics/builtins.k:24` — **ordinary rule**; attributes: `none` — `rule seqLen(str(IS:IntSeq))                   => isLen(IS)`

24. `reference-semantics/semantics/builtins.k:25` — **ordinary rule**; attributes: `none` — `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)`

25. `reference-semantics/semantics/builtins.k:26` — **ordinary rule**; attributes: `none` — `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)`

26. `reference-semantics/semantics/builtins.k:32` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>`

27. `reference-semantics/semantics/builtins.k:33` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`

28. `reference-semantics/semantics/builtins.k:34` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>`

29. `reference-semantics/semantics/builtins.k:35` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>`

30. `reference-semantics/semantics/builtins.k:36` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= charsOf(IntSeq) [function, total]`

31. `reference-semantics/semantics/builtins.k:37` — **ordinary rule**; attributes: `none` — `rule charsOf(.IntSeq)                => .ValSeq`

32. `reference-semantics/semantics/builtins.k:38` — **ordinary rule**; attributes: `none` — `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))`

33. `reference-semantics/semantics/builtins.k:41` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))`

34. `reference-semantics/semantics/builtins.k:44` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)`

35. `reference-semantics/semantics/builtins.k:47` — **syntax**; attributes: `none` — `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`

36. `reference-semantics/semantics/builtins.k:48` — **ordinary rule**; attributes: `none` — `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`

37. `reference-semantics/semantics/builtins.k:49` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`

38. `reference-semantics/semantics/builtins.k:50` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)`

39. `reference-semantics/semantics/builtins.k:54` — **function syntax**; attributes: `function` — `syntax Int ::= intOf(Val) [function]`

40. `reference-semantics/semantics/builtins.k:55` — **ordinary rule**; attributes: `none` — `rule intOf(I:Int)  => I`

41. `reference-semantics/semantics/builtins.k:56` — **ordinary rule**; attributes: `none` — `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi`

42. `reference-semantics/semantics/builtins.k:59` — **syntax**; attributes: `none` — `syntax KItem ::= #allAcc(Iterable) | "#allCont"`

43. `reference-semantics/semantics/builtins.k:60` — **ordinary rule**; attributes: `none` — `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`

44. `reference-semantics/semantics/builtins.k:61` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #allCont => true ... </k>`

45. `reference-semantics/semantics/builtins.k:62` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)`

46. `reference-semantics/semantics/builtins.k:64` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)`

47. `reference-semantics/semantics/builtins.k:67` — **syntax**; attributes: `none` — `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`

48. `reference-semantics/semantics/builtins.k:68` — **ordinary rule**; attributes: `none` — `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`

49. `reference-semantics/semantics/builtins.k:69` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #anyCont => false ... </k>`

50. `reference-semantics/semantics/builtins.k:70` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)`

51. `reference-semantics/semantics/builtins.k:72` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)`

52. `reference-semantics/semantics/builtins.k:76` — **syntax**; attributes: `none` — `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`

53. `reference-semantics/semantics/builtins.k:77` — **ordinary rule**; attributes: `none` — `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`

54. `reference-semantics/semantics/builtins.k:78` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)`

55. `reference-semantics/semantics/builtins.k:80` — **ordinary rule**; attributes: `none` — `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`

56. `reference-semantics/semantics/builtins.k:81` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`

57. `reference-semantics/semantics/builtins.k:82` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)`

58. `reference-semantics/semantics/builtins.k:86` — **syntax**; attributes: `none` — `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`

59. `reference-semantics/semantics/builtins.k:87` — **ordinary rule**; attributes: `none` — `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`

60. `reference-semantics/semantics/builtins.k:88` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)`

61. `reference-semantics/semantics/builtins.k:90` — **ordinary rule**; attributes: `none` — `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`

62. `reference-semantics/semantics/builtins.k:91` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`

63. `reference-semantics/semantics/builtins.k:92` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)`

64. `reference-semantics/semantics/builtins.k:97` — **function syntax**; attributes: `function` — `syntax Int ::= maxVals(Int, Vals) [function]`

65. `reference-semantics/semantics/builtins.k:98` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`

66. `reference-semantics/semantics/builtins.k:99` — **ordinary rule**; attributes: `none` — `rule maxVals(M:Int, .Vals)           => M`

67. `reference-semantics/semantics/builtins.k:100` — **ordinary rule**; attributes: `none` — `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`

68. `reference-semantics/semantics/builtins.k:102` — **function syntax**; attributes: `function` — `syntax Int ::= minVals(Int, Vals) [function]`

69. `reference-semantics/semantics/builtins.k:103` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`

70. `reference-semantics/semantics/builtins.k:104` — **ordinary rule**; attributes: `none` — `rule minVals(M:Int, .Vals)           => M`

71. `reference-semantics/semantics/builtins.k:105` — **ordinary rule**; attributes: `none` — `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)`

72. `reference-semantics/semantics/builtins.k:108` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0`

73. `reference-semantics/semantics/builtins.k:111` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0`

74. `reference-semantics/semantics/builtins.k:114` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= binCodes(Int) [function, total]`

75. `reference-semantics/semantics/builtins.k:115` — **ordinary rule**; attributes: `none` — `rule binCodes(0) => iCons(48, .IntSeq)`

76. `reference-semantics/semantics/builtins.k:116` — **ordinary rule**; attributes: `none` — `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`

77. `reference-semantics/semantics/builtins.k:117` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`

78. `reference-semantics/semantics/builtins.k:118` — **ordinary rule**; attributes: `none` — `rule binAcc(0, ACC:IntSeq) => ACC`

79. `reference-semantics/semantics/builtins.k:119` — **ordinary rule**; attributes: `none` — `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0`

80. `reference-semantics/semantics/builtins.k:124` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`

81. `reference-semantics/semantics/builtins.k:126` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`

82. `reference-semantics/semantics/builtins.k:127` — **ordinary rule**; attributes: `none` — `rule enumVS(.ValSeq, _:Int) => .ValSeq`

83. `reference-semantics/semantics/builtins.k:128` — **ordinary rule**; attributes: `none` — `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))`

84. `reference-semantics/semantics/builtins.k:132` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`

85. `reference-semantics/semantics/builtins.k:134` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`

86. `reference-semantics/semantics/builtins.k:135` — **ordinary rule**; attributes: `none` — `rule mapStrVS(.ValSeq) => .ValSeq`

87. `reference-semantics/semantics/builtins.k:136` — **ordinary rule**; attributes: `none` — `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`

88. `reference-semantics/semantics/builtins.k:137` — **ordinary rule**; attributes: `none` — `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))`

89. `reference-semantics/semantics/builtins.k:140` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("int", I:Int, .Vals) => I`

90. `reference-semantics/semantics/builtins.k:143` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`

91. `reference-semantics/semantics/builtins.k:144` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128`

92. `reference-semantics/semantics/builtins.k:148` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))`

93. `reference-semantics/semantics/builtins.k:149` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)`

94. `reference-semantics/semantics/builtins.k:152` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57`

95. `reference-semantics/semantics/builtins.k:156` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2`

96. `reference-semantics/semantics/builtins.k:158` — **function syntax**; attributes: `function, total` — `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`

97. `reference-semantics/semantics/builtins.k:159` — **ordinary rule**; attributes: `none` — `rule intDigAcc(.IntSeq, ACC:Int)             => ACC`

98. `reference-semantics/semantics/builtins.k:160` — **ordinary rule**; attributes: `none` — `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))`

99. `reference-semantics/semantics/builtins.k:163` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`

100. `reference-semantics/semantics/builtins.k:164` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)`

101. `reference-semantics/semantics/builtins.k:167` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`

102. `reference-semantics/semantics/builtins.k:169` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>`

103. `reference-semantics/semantics/builtins.k:170` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`

104. `reference-semantics/semantics/builtins.k:171` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`

105. `reference-semantics/semantics/builtins.k:173` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>`

106. `reference-semantics/semantics/builtins.k:174` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>`

107. `reference-semantics/semantics/builtins.k:177` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)`

108. `reference-semantics/semantics/builtins.k:178` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)`

109. `reference-semantics/semantics/builtins.k:179` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0`

110. `reference-semantics/semantics/builtins.k:187` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`

111. `reference-semantics/semantics/builtins.k:188` — **function syntax**; attributes: `function` — `syntax Int ::= evalArith(IntSeq) [function]`

112. `reference-semantics/semantics/builtins.k:189` — **ordinary rule**; attributes: `none` — `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`

113. `reference-semantics/semantics/builtins.k:192` — **syntax**; attributes: `none` — `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`

114. `reference-semantics/semantics/builtins.k:194` — **function syntax**; attributes: `function, total` — `syntax Bool ::= evDigit(Int) [function, total]`

115. `reference-semantics/semantics/builtins.k:195` — **ordinary rule**; attributes: `none` — `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`

116. `reference-semantics/semantics/builtins.k:196` — **function syntax**; attributes: `function, total` — `syntax Bool ::= evHead42(IntSeq) [function, total]`

117. `reference-semantics/semantics/builtins.k:197` — **ordinary rule**; attributes: `none` — `rule evHead42(iCons(42, _:IntSeq)) => true`

118. `reference-semantics/semantics/builtins.k:198` — **owise rule**; attributes: `owise` — `rule evHead42(_:IntSeq)            => false [owise]`

119. `reference-semantics/semantics/builtins.k:199` — **function syntax**; attributes: `function, total` — `syntax Bool ::= evHead47(IntSeq) [function, total]`

120. `reference-semantics/semantics/builtins.k:200` — **ordinary rule**; attributes: `none` — `rule evHead47(iCons(47, _:IntSeq)) => true`

121. `reference-semantics/semantics/builtins.k:201` — **owise rule**; attributes: `owise` — `rule evHead47(_:IntSeq)            => false [owise]`

122. `reference-semantics/semantics/builtins.k:203` — **function syntax**; attributes: `function, total` — `syntax OpSeq ::= tokOps(IntSeq) [function, total]`

123. `reference-semantics/semantics/builtins.k:204` — **ordinary rule**; attributes: `none` — `rule tokOps(.IntSeq)                 => .OpSeq`

124. `reference-semantics/semantics/builtins.k:205` — **ordinary rule**; attributes: `none` — `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)`

125. `reference-semantics/semantics/builtins.k:206` — **ordinary rule**; attributes: `none` — `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)`

126. `reference-semantics/semantics/builtins.k:207` — **ordinary rule**; attributes: `none` — `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`

127. `reference-semantics/semantics/builtins.k:208` — **ordinary rule**; attributes: `none` — `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)`

128. `reference-semantics/semantics/builtins.k:209` — **ordinary rule**; attributes: `none` — `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))`

129. `reference-semantics/semantics/builtins.k:210` — **ordinary rule**; attributes: `none` — `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)`

130. `reference-semantics/semantics/builtins.k:211` — **ordinary rule**; attributes: `none` — `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))`

131. `reference-semantics/semantics/builtins.k:212` — **ordinary rule**; attributes: `none` — `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))`

132. `reference-semantics/semantics/builtins.k:214` — **function syntax**; attributes: `function, total, function, total` — `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`

133. `reference-semantics/semantics/builtins.k:216` — **ordinary rule**; attributes: `none` — `rule tokNds(.IntSeq)                => .IntSeq`

134. `reference-semantics/semantics/builtins.k:217` — **ordinary rule**; attributes: `none` — `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)`

135. `reference-semantics/semantics/builtins.k:218` — **ordinary rule**; attributes: `none` — `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`

136. `reference-semantics/semantics/builtins.k:219` — **ordinary rule**; attributes: `none` — `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32`

137. `reference-semantics/semantics/builtins.k:221` — **ordinary rule**; attributes: `none` — `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)`

138. `reference-semantics/semantics/builtins.k:223` — **owise rule**; attributes: `owise` — `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`

139. `reference-semantics/semantics/builtins.k:225` — **syntax**; attributes: `none` — `syntax EvPair ::= evp(OpSeq, IntSeq)`

140. `reference-semantics/semantics/builtins.k:226` — **function syntax**; attributes: `function, total` — `syntax Int ::= firstNdE(EvPair) [function, total]`

141. `reference-semantics/semantics/builtins.k:227` — **ordinary rule**; attributes: `none` — `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`

142. `reference-semantics/semantics/builtins.k:228` — **owise rule**; attributes: `owise` — `rule firstNdE(_:EvPair) => 0 [owise]`

143. `reference-semantics/semantics/builtins.k:230` — **function syntax**; attributes: `function, total` — `syntax Int ::= applyOpE(String, Int, Int) [function, total]`

144. `reference-semantics/semantics/builtins.k:231` — **ordinary rule**; attributes: `none` — `rule applyOpE("+",  A:Int, B:Int) => A +Int B`

145. `reference-semantics/semantics/builtins.k:232` — **ordinary rule**; attributes: `none` — `rule applyOpE("-",  A:Int, B:Int) => A -Int B`

146. `reference-semantics/semantics/builtins.k:233` — **ordinary rule**; attributes: `none` — `rule applyOpE("*",  A:Int, B:Int) => A *Int B`

147. `reference-semantics/semantics/builtins.k:234` — **ordinary rule**; attributes: `none` — `rule applyOpE("//", A:Int, B:Int) => A divInt B`

148. `reference-semantics/semantics/builtins.k:235` — **ordinary rule**; attributes: `none` — `rule applyOpE("**", A:Int, B:Int) => A ^Int B`

149. `reference-semantics/semantics/builtins.k:236` — **owise rule**; attributes: `owise` — `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`

150. `reference-semantics/semantics/builtins.k:238` — **function syntax**; attributes: `function, total` — `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`

151. `reference-semantics/semantics/builtins.k:239` — **ordinary rule**; attributes: `none` — `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`

152. `reference-semantics/semantics/builtins.k:240` — **ordinary rule**; attributes: `none` — `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`

153. `reference-semantics/semantics/builtins.k:241` — **ordinary rule**; attributes: `none` — `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"`

154. `reference-semantics/semantics/builtins.k:243` — **owise rule**; attributes: `owise` — `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`

155. `reference-semantics/semantics/builtins.k:244` — **function syntax**; attributes: `function, total` — `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`

156. `reference-semantics/semantics/builtins.k:245` — **ordinary rule**; attributes: `none` — `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`

157. `reference-semantics/semantics/builtins.k:246` — **ordinary rule**; attributes: `none` — `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`

158. `reference-semantics/semantics/builtins.k:247` — **function syntax**; attributes: `function, total` — `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`

159. `reference-semantics/semantics/builtins.k:248` — **ordinary rule**; attributes: `none` — `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`

160. `reference-semantics/semantics/builtins.k:250` — **function syntax**; attributes: `function, total, function, total` — `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`

161. `reference-semantics/semantics/builtins.k:251` — **ordinary rule**; attributes: `none` — `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`

162. `reference-semantics/semantics/builtins.k:252` — **ordinary rule**; attributes: `none` — `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`

163. `reference-semantics/semantics/builtins.k:253` — **ordinary rule**; attributes: `none` — `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`

164. `reference-semantics/semantics/builtins.k:254` — **ordinary rule**; attributes: `none` — `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`

165. `reference-semantics/semantics/builtins.k:255` — **function syntax**; attributes: `function, total` — `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`

166. `reference-semantics/semantics/builtins.k:256` — **ordinary rule**; attributes: `none` — `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`

167. `reference-semantics/semantics/builtins.k:257` — **ordinary rule**; attributes: `none` — `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)`

168. `reference-semantics/semantics/builtins.k:260` — **ordinary rule**; attributes: `none` — `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)`

169. `reference-semantics/semantics/builtins.k:263` — **owise rule**; attributes: `owise` — `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`

170. `reference-semantics/semantics/builtins.k:265` — **function syntax**; attributes: `function, total` — `syntax Bool ::= inLevelE(String, String) [function, total]`

171. `reference-semantics/semantics/builtins.k:266` — **ordinary rule**; attributes: `none` — `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"`

172. `reference-semantics/semantics/builtins.k:267` — **ordinary rule**; attributes: `none` — `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`

173. `reference-semantics/semantics/builtins.k:268` — **owise rule**; attributes: `owise` — `rule inLevelE(_:String, _:String) => false [owise]`

174. `reference-semantics/semantics/builtins.k:269` — **function syntax**; attributes: `function, total` — `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`

175. `reference-semantics/semantics/builtins.k:270` — **ordinary rule**; attributes: `none` — `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`

176. `reference-semantics/semantics/builtins.k:271` — **ordinary rule**; attributes: `none` — `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`

177. `reference-semantics/semantics/builtins.k:272` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`

178. `reference-semantics/semantics/builtins.k:273` — **ordinary rule**; attributes: `none` — `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`

179. `reference-semantics/semantics/builtins.k:274` — **ordinary rule**; attributes: `none` — `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))`

180. `reference-semantics/semantics/builtins.k:279` — **syntax**; attributes: `none` — `syntax KItem ::= "#md5"`

181. `reference-semantics/semantics/builtins.k:280` — **priority rule**; attributes: `priority(40)` — `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`

182. `reference-semantics/semantics/builtins.k:282` — **ordinary rule**; attributes: `none` — `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`

183. `reference-semantics/semantics/builtins.k:283` — **syntax**; attributes: `none` — `syntax Val ::= md5Obj(IntSeq)`

184. `reference-semantics/semantics/builtins.k:284` — **ordinary rule**; attributes: `none` — `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`

185. `reference-semantics/semantics/builtins.k:285` — **opaque-symbol syntax**; attributes: `function, total, symbol(md5hexCodes), no-evaluators` — `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`

186. `reference-semantics/semantics/builtins.k:291` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`

187. `reference-semantics/semantics/builtins.k:292` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`

188. `reference-semantics/semantics/builtins.k:293` — **function syntax**; attributes: `function, function` — `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`

189. `reference-semantics/semantics/builtins.k:294` — **ordinary rule**; attributes: `none` — `rule isIntV(_:Int)         => true`

190. `reference-semantics/semantics/builtins.k:295` — **owise rule**; attributes: `owise` — `rule isIntV(_:Val)         => false [owise]`

191. `reference-semantics/semantics/builtins.k:296` — **ordinary rule**; attributes: `none` — `rule isStrV(str(_:IntSeq)) => true`

192. `reference-semantics/semantics/builtins.k:297` — **owise rule**; attributes: `owise` — `rule isStrV(_:Val)         => false [owise]`

## `reference-semantics/semantics/call.k`

193. `reference-semantics/semantics/call.k:16` — **ordinary rule**; attributes: `none` — `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>`

194. `reference-semantics/semantics/call.k:19` — **syntax**; attributes: `none` — `syntax KItem ::= #callee(Exprs)`

195. `reference-semantics/semantics/call.k:20` — **owise rule**; attributes: `owise` — `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`

196. `reference-semantics/semantics/call.k:21` — **ordinary rule**; attributes: `none` — `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>`

197. `reference-semantics/semantics/call.k:24` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`

198. `reference-semantics/semantics/call.k:26` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`

199. `reference-semantics/semantics/call.k:27` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>`

200. `reference-semantics/semantics/call.k:28` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>`

201. `reference-semantics/semantics/call.k:29` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>`

202. `reference-semantics/semantics/call.k:30` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>`

203. `reference-semantics/semantics/call.k:31` — **owise rule**; attributes: `owise` — `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`

204. `reference-semantics/semantics/call.k:32` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>`

205. `reference-semantics/semantics/call.k:38` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

206. `reference-semantics/semantics/call.k:42` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]`

207. `reference-semantics/semantics/call.k:47` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

208. `reference-semantics/semantics/call.k:52` — **function syntax**; attributes: `function, total` — `syntax Bool ::= isMutMethod(String) [function, total]`

209. `reference-semantics/semantics/call.k:53` — **ordinary rule**; attributes: `none` — `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`

210. `reference-semantics/semantics/call.k:56` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]`

211. `reference-semantics/semantics/call.k:63` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]`

212. `reference-semantics/semantics/call.k:69` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`

213. `reference-semantics/semantics/call.k:80` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env>     CALLERL:Int => NEWL </env> <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`

214. `reference-semantics/semantics/call.k:87` — **syntax**; attributes: `none` — `syntax KItem ::= #allocCells(ParamNames)`

215. `reference-semantics/semantics/call.k:88` — **ordinary rule**; attributes: `none` — `rule <k> #allocCells(.ParamNames) => .K ... </k>`

216. `reference-semantics/semantics/call.k:89` — **ordinary rule**; attributes: `none` — `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap>    H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`

## `reference-semantics/semantics/comprehension.k`

217. `reference-semantics/semantics/comprehension.k:11` — **ordinary rule**; attributes: `none` — `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`

218. `reference-semantics/semantics/comprehension.k:12` — **ordinary rule**; attributes: `none` — `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`

219. `reference-semantics/semantics/comprehension.k:14` — **macro syntax**; attributes: `macro` — `syntax Stmts ::= compBody(CompFors, Expr) [macro]`

220. `reference-semantics/semantics/comprehension.k:15` — **ordinary rule**; attributes: `none` — `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`

221. `reference-semantics/semantics/comprehension.k:18` — **macro syntax**; attributes: `macro-rec` — `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`

222. `reference-semantics/semantics/comprehension.k:19` — **ordinary rule**; attributes: `none` — `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`

223. `reference-semantics/semantics/comprehension.k:21` — **ordinary rule**; attributes: `none` — `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`

224. `reference-semantics/semantics/comprehension.k:24` — **macro syntax**; attributes: `macro` — `syntax Expr ::= compGuard(Exprs) [macro]`

225. `reference-semantics/semantics/comprehension.k:25` — **ordinary rule**; attributes: `none` — `rule compGuard(.Exprs)             => Bool(true)`

226. `reference-semantics/semantics/comprehension.k:26` — **ordinary rule**; attributes: `none` — `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`

## `reference-semantics/semantics/concrete.k`

227. `reference-semantics/semantics/concrete.k:13` — **ordinary rule**; attributes: `none` — `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`

228. `reference-semantics/semantics/concrete.k:16` — **ordinary rule**; attributes: `none` — `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`

229. `reference-semantics/semantics/concrete.k:25` — **syntax**; attributes: `none` — `syntax Val ::= kvP(Val, Val)`

230. `reference-semantics/semantics/concrete.k:26` — **syntax**; attributes: `none` — `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`

231. `reference-semantics/semantics/concrete.k:28` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`

232. `reference-semantics/semantics/concrete.k:31` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`

233. `reference-semantics/semantics/concrete.k:34` — **ordinary rule**; attributes: `none` — `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`

234. `reference-semantics/semantics/concrete.k:36` — **ordinary rule**; attributes: `none` — `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`

235. `reference-semantics/semantics/concrete.k:38` — **ordinary rule**; attributes: `none` — `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)`

236. `reference-semantics/semantics/concrete.k:42` — **function syntax**; attributes: `function` — `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`

237. `reference-semantics/semantics/concrete.k:43` — **ordinary rule**; attributes: `none` — `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`

238. `reference-semantics/semantics/concrete.k:44` — **ordinary rule**; attributes: `none` — `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)`

239. `reference-semantics/semantics/concrete.k:47` — **ordinary rule**; attributes: `none` — `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)`

240. `reference-semantics/semantics/concrete.k:51` — **function syntax**; attributes: `function` — `syntax Bool ::= kLt(Val, Val) [function]`

241. `reference-semantics/semantics/concrete.k:52` — **ordinary rule**; attributes: `none` — `rule kLt(I1:Int, I2:Int)             => I1 <Int I2`

242. `reference-semantics/semantics/concrete.k:53` — **ordinary rule**; attributes: `none` — `rule kLt(F1:Float, F2:Float)         => F1 <Float F2`

243. `reference-semantics/semantics/concrete.k:54` — **ordinary rule**; attributes: `none` — `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`

244. `reference-semantics/semantics/concrete.k:56` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`

245. `reference-semantics/semantics/concrete.k:57` — **ordinary rule**; attributes: `none` — `rule unpairVS(.ValSeq) => .ValSeq`

246. `reference-semantics/semantics/concrete.k:58` — **ordinary rule**; attributes: `none` — `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`

247. `reference-semantics/semantics/concrete.k:59` — **owise rule**; attributes: `owise` — `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`

## `reference-semantics/semantics/controls.k`

248. `reference-semantics/semantics/controls.k:9` — **ordinary rule**; attributes: `none` — `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`

249. `reference-semantics/semantics/controls.k:12` — **priority rule**; attributes: `priority(40)` — `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`

250. `reference-semantics/semantics/controls.k:20` — **ordinary rule**; attributes: `none` — `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)`

251. `reference-semantics/semantics/controls.k:27` — **priority rule**; attributes: `priority(40)` — `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]`

252. `reference-semantics/semantics/controls.k:35` — **ordinary rule**; attributes: `none` — `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`

253. `reference-semantics/semantics/controls.k:36` — **owise rule**; attributes: `owise` — `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`

254. `reference-semantics/semantics/controls.k:37` — **syntax**; attributes: `none` — `syntax KItem ::= #bindImports(ParamNames)`

255. `reference-semantics/semantics/controls.k:38` — **ordinary rule**; attributes: `none` — `rule <k> #bindImports(.ParamNames) => .K ... </k>`

256. `reference-semantics/semantics/controls.k:39` — **ordinary rule**; attributes: `none` — `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"`

257. `reference-semantics/semantics/controls.k:43` — **ordinary rule**; attributes: `none` — `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")`

258. `reference-semantics/semantics/controls.k:48` — **ordinary rule**; attributes: `none` — `rule <k> Expr(_:Val) => .K ... </k>`

259. `reference-semantics/semantics/controls.k:51` — **syntax**; attributes: `none` — `syntax KItem ::= #branch(Bool, Stmts, Stmts)`

260. `reference-semantics/semantics/controls.k:52` — **ordinary rule**; attributes: `none` — `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`

261. `reference-semantics/semantics/controls.k:53` — **ordinary rule**; attributes: `none` — `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>`

262. `reference-semantics/semantics/controls.k:54` — **ordinary rule**; attributes: `none` — `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>`

263. `reference-semantics/semantics/controls.k:57` — **ordinary rule**; attributes: `none` — `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)`

264. `reference-semantics/semantics/controls.k:59` — **ordinary rule**; attributes: `none` — `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)`

265. `reference-semantics/semantics/controls.k:65` — **syntax**; attributes: `none` — `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`

266. `reference-semantics/semantics/controls.k:69` — **ordinary rule**; attributes: `none` — `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`

267. `reference-semantics/semantics/controls.k:71` — **ordinary rule**; attributes: `none` — `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`

268. `reference-semantics/semantics/controls.k:72` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`

269. `reference-semantics/semantics/controls.k:73` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>`

270. `reference-semantics/semantics/controls.k:77` — **ordinary rule**; attributes: `none` — `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`

271. `reference-semantics/semantics/controls.k:78` — **ordinary rule**; attributes: `none` — `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`

272. `reference-semantics/semantics/controls.k:79` — **ordinary rule**; attributes: `none` — `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)`

273. `reference-semantics/semantics/controls.k:81` — **ordinary rule**; attributes: `none` — `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)`

274. `reference-semantics/semantics/controls.k:85` — **ordinary rule**; attributes: `none` — `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`

275. `reference-semantics/semantics/controls.k:86` — **ordinary rule**; attributes: `none` — `rule <k> Continue => #cont ... </k>`

276. `reference-semantics/semantics/controls.k:87` — **ordinary rule**; attributes: `none` — `rule <k> Break => #brk ... </k>`

277. `reference-semantics/semantics/controls.k:88` — **ordinary rule**; attributes: `none` — `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`

278. `reference-semantics/semantics/controls.k:89` — **owise rule**; attributes: `owise` — `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`

279. `reference-semantics/semantics/controls.k:90` — **ordinary rule**; attributes: `none` — `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`

280. `reference-semantics/semantics/controls.k:91` — **owise rule**; attributes: `owise` — `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]`

281. `reference-semantics/semantics/controls.k:95` — **priority rule**; attributes: `priority(40)` — `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

282. `reference-semantics/semantics/controls.k:98` — **priority rule**; attributes: `priority(40)` — `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

283. `reference-semantics/semantics/controls.k:101` — **priority rule**; attributes: `priority(40)` — `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

284. `reference-semantics/semantics/controls.k:106` — **priority rule**; attributes: `priority(40)` — `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## `reference-semantics/semantics/core.k`

285. `reference-semantics/semantics/core.k:13` — **syntax**; attributes: `none` — `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`

286. `reference-semantics/semantics/core.k:14` — **syntax**; attributes: `none` — `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`

287. `reference-semantics/semantics/core.k:15` — **syntax**; attributes: `none` — `syntax Str    ::= str(IntSeq)`

288. `reference-semantics/semantics/core.k:18` — **syntax**; attributes: `none` — `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`

289. `reference-semantics/semantics/core.k:25` — **syntax**; attributes: `none` — `syntax Val      ::= Int | Bool | "noneV" | Iterable | ref(Int)          // a heap object: <heap> holds its list(VS) | cellRef(Int)      // a closure cell: <heap> holds cellV(V) | closureVal(ParamNames, Stmts, Int) | typeV(String)     // a type object (int/str), resolved from the builtins frame | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough) | boundMethodV(Val, String)   // a cooled Attribute: obj.method`

290. `reference-semantics/semantics/core.k:36` — **syntax**; attributes: `none` — `syntax Parent   ::= "root" | parent(Int)`

291. `reference-semantics/semantics/core.k:37` — **syntax**; attributes: `none` — `syntax Scope    ::= scope(Map, Parent)`

292. `reference-semantics/semantics/core.k:38` — **syntax**; attributes: `none` — `syntax KResult  ::= Val`

293. `reference-semantics/semantics/core.k:39` — **syntax**; attributes: `none` — `syntax Expr     ::= Val   // cooling puts results back into expression holes`

294. `reference-semantics/semantics/core.k:40` — **syntax**; attributes: `none` — `syntax Vals     ::= List{Val, ","}`

295. `reference-semantics/semantics/core.k:41` — **syntax**; attributes: `none` — `syntax Exc      ::= "NoExc" | "AssertionError"`

296. `reference-semantics/semantics/core.k:42` — **syntax**; attributes: `none` — `syntax RetState ::= "noRet" | retV(Val)`

297. `reference-semantics/semantics/core.k:49` — **configuration**; attributes: `none` — `configuration <k>       #loadAll($PGM:Module) </k> <env>     0 </env> <scopes>   0     |-> scope(.Map, parent(-1)) -1    |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap>    .Map </heap> <heapLoc> 0 </heapLoc> <stack>   .List </stack> <ret>     noRet </ret> <exc>     NoExc </exc> <exit-code exit=""> 0 </exit-code>`

298. `reference-semantics/semantics/core.k:68` — **function syntax**; attributes: `function, total` — `syntax Bool ::= isRefV(Val) [function, total]`

299. `reference-semantics/semantics/core.k:69` — **ordinary rule**; attributes: `none` — `rule isRefV(ref(_:Int)) => true`

300. `reference-semantics/semantics/core.k:70` — **owise rule**; attributes: `owise` — `rule isRefV(_:Val)      => false [owise]`

301. `reference-semantics/semantics/core.k:75` — **syntax**; attributes: `none` — `syntax HeapVal ::= cellV(Val)`

302. `reference-semantics/semantics/core.k:76` — **function syntax**; attributes: `function, total` — `syntax Bool ::= isCellRef(Val) [function, total]`

303. `reference-semantics/semantics/core.k:77` — **ordinary rule**; attributes: `none` — `rule isCellRef(cellRef(_:Int)) => true`

304. `reference-semantics/semantics/core.k:78` — **owise rule**; attributes: `owise` — `rule isCellRef(_:Val)          => false [owise]`

305. `reference-semantics/semantics/core.k:85` — **priority rule**; attributes: `priority(40)` — `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]`

306. `reference-semantics/semantics/core.k:95` — **syntax**; attributes: `none` — `syntax Val ::= kwV(String, Val)`

307. `reference-semantics/semantics/core.k:96` — **syntax**; attributes: `none` — `syntax KItem ::= #kwTag(String)`

308. `reference-semantics/semantics/core.k:97` — **ordinary rule**; attributes: `none` — `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`

309. `reference-semantics/semantics/core.k:98` — **ordinary rule**; attributes: `none` — `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)`

310. `reference-semantics/semantics/core.k:100` — **function syntax**; attributes: `function, total` — `syntax Bool ::= isKwV(Val) [function, total]`

311. `reference-semantics/semantics/core.k:101` — **ordinary rule**; attributes: `none` — `rule isKwV(kwV(_:String, _:Val)) => true`

312. `reference-semantics/semantics/core.k:102` — **owise rule**; attributes: `owise` — `rule isKwV(_:Val)                => false [owise]`

313. `reference-semantics/semantics/core.k:106` — **syntax**; attributes: `none` — `syntax Val ::= cellsMark(ParamNames)`

314. `reference-semantics/semantics/core.k:107` — **function syntax**; attributes: `function` — `syntax ParamNames ::= cellsOf(Val) [function]`

315. `reference-semantics/semantics/core.k:108` — **ordinary rule**; attributes: `none` — `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`

316. `reference-semantics/semantics/core.k:109` — **function syntax**; attributes: `function, total` — `syntax Bool ::= pnMember(String, ParamNames) [function, total]`

317. `reference-semantics/semantics/core.k:110` — **ordinary rule**; attributes: `none` — `rule pnMember(_:String, .ParamNames) => false`

318. `reference-semantics/semantics/core.k:111` — **ordinary rule**; attributes: `none` — `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`

319. `reference-semantics/semantics/core.k:113` — **syntax**; attributes: `none` — `syntax KItem ::= #cellW(Val, Val)`

320. `reference-semantics/semantics/core.k:114` — **ordinary rule**; attributes: `none` — `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`

321. `reference-semantics/semantics/core.k:117` — **syntax**; attributes: `none` — `syntax KItem ::= #alloc(Val)`

322. `reference-semantics/semantics/core.k:118` — **ordinary rule**; attributes: `none` — `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap>    H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`

323. `reference-semantics/semantics/core.k:124` — **syntax**; attributes: `none` — `syntax KItem ::= #loadAll(Module)`

324. `reference-semantics/semantics/core.k:125` — **ordinary rule**; attributes: `none` — `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`

325. `reference-semantics/semantics/core.k:126` — **ordinary rule**; attributes: `none` — `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`

326. `reference-semantics/semantics/core.k:127` — **ordinary rule**; attributes: `none` — `rule <k> .Stmts => .K ... </k>`

327. `reference-semantics/semantics/core.k:130` — **syntax**; attributes: `none` — `syntax KItem ::= #look(String, Int)`

328. `reference-semantics/semantics/core.k:131` — **ordinary rule**; attributes: `none` — `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`

329. `reference-semantics/semantics/core.k:132` — **ordinary rule**; attributes: `none` — `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)`

330. `reference-semantics/semantics/core.k:145` — **priority rule**; attributes: `priority(40)` — `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]`

331. `reference-semantics/semantics/core.k:152` — **ordinary rule**; attributes: `none` — `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))`

332. `reference-semantics/semantics/core.k:157` — **function syntax**; attributes: `function, total` — `syntax Scope ::= "builtinsScope" [function, total]`

333. `reference-semantics/semantics/core.k:158` — **ordinary rule**; attributes: `none` — `rule builtinsScope => scope(.Map [ "len"    <- builtinV("len")    ] [ "set"    <- builtinV("set")    ] [ "sum"    <- builtinV("sum")    ] [ "abs"    <- builtinV("abs")    ] [ "min"    <- builtinV("min")    ] [ "max"    <- builtinV("max")    ] [ "ord"    <- builtinV("ord")    ] [ "chr"    <- builtinV("chr")    ] [ "range"  <- builtinV("range")  ] [ "all"    <- builtinV("all")    ] [ "any"    <- builtinV("any")    ] [ "zip"    <- builtinV("zip")    ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list"   <- builtinV("list")   ] [ "round"  <- builtinV("round")  ] [ "bin"    <- builtinV("bin")    ] [ "enumerate" <- builtinV("enumerate") ] [ "map"    <- builtinV("map")    ] [ "eval"   <- builtinV("eval")   ] [ "int"    <- typeV("int")       ] [ "str"    <- typeV("str")       ] [ "float"  <- typeV("float")     ], root)`

334. `reference-semantics/semantics/core.k:185` — **syntax**; attributes: `none` — `syntax ApplyK ::= toCall(Val)`

335. `reference-semantics/semantics/core.k:186` — **syntax**; attributes: `none` — `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`

336. `reference-semantics/semantics/core.k:189` — **ordinary rule**; attributes: `none` — `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`

337. `reference-semantics/semantics/core.k:190` — **ordinary rule**; attributes: `none` — `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`

338. `reference-semantics/semantics/core.k:191` — **ordinary rule**; attributes: `none` — `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>`

339. `reference-semantics/semantics/core.k:194` — **ordinary rule**; attributes: `none` — `rule <k> Int(I:Int)   => I ... </k>`

340. `reference-semantics/semantics/core.k:195` — **ordinary rule**; attributes: `none` — `rule <k> Bool(B:Bool) => B ... </k>`

341. `reference-semantics/semantics/core.k:196` — **ordinary rule**; attributes: `none` — `rule <k> NoneVal      => noneV ... </k>`

342. `reference-semantics/semantics/core.k:199` — **function syntax**; attributes: `function` — `syntax Bool ::= truthy(Val) [function]`

343. `reference-semantics/semantics/core.k:200` — **ordinary rule**; attributes: `none` — `rule truthy(B:Bool)          => B`

344. `reference-semantics/semantics/core.k:201` — **ordinary rule**; attributes: `none` — `rule truthy(noneV)           => false`

345. `reference-semantics/semantics/core.k:202` — **ordinary rule**; attributes: `none` — `rule truthy(I:Int)           => I =/=Int 0`

346. `reference-semantics/semantics/core.k:203` — **ordinary rule**; attributes: `none` — `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)`

347. `reference-semantics/semantics/core.k:204` — **ordinary rule**; attributes: `none` — `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)`

348. `reference-semantics/semantics/core.k:205` — **ordinary rule**; attributes: `none` — `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)`

349. `reference-semantics/semantics/core.k:208` — **function syntax**; attributes: `function` — `syntax Val  ::= applyUn(String, Val) [function]`

350. `reference-semantics/semantics/core.k:209` — **function syntax**; attributes: `function` — `syntax Val  ::= applyBin(String, Val, Val) [function]`

351. `reference-semantics/semantics/core.k:210` — **function syntax**; attributes: `function` — `syntax Bool ::= applyCmp(String, Val, Val) [function]`

352. `reference-semantics/semantics/core.k:213` — **function syntax**; attributes: `function, total` — `syntax Vals ::= appendVal(Vals, Val) [function, total]`

353. `reference-semantics/semantics/core.k:214` — **ordinary rule**; attributes: `none` — `rule appendVal(.Vals, V:Val)              => V , .Vals`

354. `reference-semantics/semantics/core.k:215` — **ordinary rule**; attributes: `none` — `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)`

355. `reference-semantics/semantics/core.k:217` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`

356. `reference-semantics/semantics/core.k:218` — **ordinary rule**; attributes: `none` — `rule vals2valSeq(.Vals)            => .ValSeq`

357. `reference-semantics/semantics/core.k:219` — **ordinary rule**; attributes: `none` — `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))`

358. `reference-semantics/semantics/core.k:223` — **function syntax**; attributes: `function, total` — `syntax Int ::= vsLen(ValSeq) [function, total]`

359. `reference-semantics/semantics/core.k:224` — **ordinary rule**; attributes: `none` — `rule vsLen(.ValSeq)                => 0`

360. `reference-semantics/semantics/core.k:225` — **ordinary rule**; attributes: `none` — `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`

361. `reference-semantics/semantics/core.k:227` — **function syntax**; attributes: `function, total` — `syntax Int ::= isLen(IntSeq) [function, total]`

362. `reference-semantics/semantics/core.k:228` — **ordinary rule**; attributes: `none` — `rule isLen(.IntSeq)                => 0`

363. `reference-semantics/semantics/core.k:229` — **ordinary rule**; attributes: `none` — `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)`

364. `reference-semantics/semantics/core.k:233` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`

365. `reference-semantics/semantics/core.k:234` — **ordinary rule**; attributes: `none` — `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq`

366. `reference-semantics/semantics/core.k:235` — **ordinary rule**; attributes: `none` — `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)`

367. `reference-semantics/semantics/core.k:236` — **ordinary rule**; attributes: `none` — `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0`

368. `reference-semantics/semantics/core.k:238` — **ordinary rule**; attributes: `none` — `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS requires I <Int 0`

## `reference-semantics/semantics/dict.k`

369. `reference-semantics/semantics/dict.k:20` — **syntax**; attributes: `none` — `syntax Val ::= dictV(ValSeq, ValSeq)`

370. `reference-semantics/semantics/dict.k:23` — **syntax**; attributes: `none` — `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`

371. `reference-semantics/semantics/dict.k:26` — **ordinary rule**; attributes: `none` — `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`

372. `reference-semantics/semantics/dict.k:27` — **ordinary rule**; attributes: `none` — `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`

373. `reference-semantics/semantics/dict.k:28` — **ordinary rule**; attributes: `none` — `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`

374. `reference-semantics/semantics/dict.k:30` — **ordinary rule**; attributes: `none` — `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`

375. `reference-semantics/semantics/dict.k:32` — **ordinary rule**; attributes: `none` — `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>`

376. `reference-semantics/semantics/dict.k:37` — **function syntax**; attributes: `function, total` — `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`

377. `reference-semantics/semantics/dict.k:38` — **ordinary rule**; attributes: `none` — `rule dHasKey(.ValSeq, _:Val)                => false`

378. `reference-semantics/semantics/dict.k:39` — **ordinary rule**; attributes: `none` — `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K`

379. `reference-semantics/semantics/dict.k:40` — **ordinary rule**; attributes: `none` — `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)`

380. `reference-semantics/semantics/dict.k:43` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`

381. `reference-semantics/semantics/dict.k:44` — **ordinary rule**; attributes: `none` — `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)`

382. `reference-semantics/semantics/dict.k:45` — **ordinary rule**; attributes: `none` — `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)`

383. `reference-semantics/semantics/dict.k:49` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`

384. `reference-semantics/semantics/dict.k:50` — **ordinary rule**; attributes: `none` — `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR) requires A ==K K`

385. `reference-semantics/semantics/dict.k:52` — **ordinary rule**; attributes: `none` — `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)`

386. `reference-semantics/semantics/dict.k:54` — **owise rule**; attributes: `owise` — `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]`

387. `reference-semantics/semantics/dict.k:58` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]`

388. `reference-semantics/semantics/dict.k:63` — **ordinary rule**; attributes: `none` — `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`

389. `reference-semantics/semantics/dict.k:64` — **function syntax**; attributes: `function` — `syntax Val ::= applyIndexD(Val, Val) [function]`

390. `reference-semantics/semantics/dict.k:65` — **priority rule**; attributes: `priority(45)` — `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]`

391. `reference-semantics/semantics/dict.k:70` — **function syntax**; attributes: `function` — `syntax Val ::= dictSet(Val, Val, Val) [function]`

392. `reference-semantics/semantics/dict.k:71` — **ordinary rule**; attributes: `none` — `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))`

393. `reference-semantics/semantics/dict.k:76` — **syntax**; attributes: `none` — `syntax KItem ::= #dsetK(String, Val)`

394. `reference-semantics/semantics/dict.k:77` — **ordinary rule**; attributes: `none` — `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`

395. `reference-semantics/semantics/dict.k:78` — **ordinary rule**; attributes: `none` — `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)`

396. `reference-semantics/semantics/dict.k:82` — **ordinary rule**; attributes: `none` — `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)`

397. `reference-semantics/semantics/dict.k:86` — **syntax**; attributes: `none` — `syntax KItem ::= #dsetV(Val, Val, Val)`

398. `reference-semantics/semantics/dict.k:87` — **ordinary rule**; attributes: `none` — `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>`

399. `reference-semantics/semantics/dict.k:90` — **function syntax**; attributes: `function, total` — `syntax Int ::= normIdxD(Int, Int) [function, total]`

400. `reference-semantics/semantics/dict.k:91` — **ordinary rule**; attributes: `none` — `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`

401. `reference-semantics/semantics/dict.k:92` — **ordinary rule**; attributes: `none` — `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0`

402. `reference-semantics/semantics/dict.k:95` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`

403. `reference-semantics/semantics/dict.k:97` — **function syntax**; attributes: `function` — `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`

404. `reference-semantics/semantics/dict.k:98` — **ordinary rule**; attributes: `none` — `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`

405. `reference-semantics/semantics/dict.k:99` — **ordinary rule**; attributes: `none` — `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`

406. `reference-semantics/semantics/dict.k:101` — **function syntax**; attributes: `function` — `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`

407. `reference-semantics/semantics/dict.k:102` — **ordinary rule**; attributes: `none` — `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K`

408. `reference-semantics/semantics/dict.k:103` — **ordinary rule**; attributes: `none` — `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`

## `reference-semantics/semantics/float.k`

409. `reference-semantics/semantics/float.k:20` — **syntax**; attributes: `none` — `syntax Val ::= Float`

410. `reference-semantics/semantics/float.k:21` — **ordinary rule**; attributes: `none` — `rule <k> Float(F:Float) => F ... </k>`

411. `reference-semantics/semantics/float.k:24` — **opaque-symbol syntax**; attributes: `function, total, symbol(intFloatDiv), no-evaluators` — `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`

412. `reference-semantics/semantics/float.k:25` — **concrete rule**; attributes: `concrete` — `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`

413. `reference-semantics/semantics/float.k:27` — **ordinary rule**; attributes: `none` — `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)`

414. `reference-semantics/semantics/float.k:30` — **opaque-symbol syntax**; attributes: `function, total, symbol(divII), no-evaluators` — `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`

415. `reference-semantics/semantics/float.k:31` — **concrete rule**; attributes: `concrete` — `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`

416. `reference-semantics/semantics/float.k:32` — **ordinary rule**; attributes: `none` — `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)`

417. `reference-semantics/semantics/float.k:37` — **opaque-symbol syntax**; attributes: `function, total, symbol(floatMod), no-evaluators` — `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`

418. `reference-semantics/semantics/float.k:38` — **concrete rule**; attributes: `concrete` — `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`

419. `reference-semantics/semantics/float.k:39` — **ordinary rule**; attributes: `none` — `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)`

420. `reference-semantics/semantics/float.k:43` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`

421. `reference-semantics/semantics/float.k:44` — **ordinary rule**; attributes: `none` — `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)`

422. `reference-semantics/semantics/float.k:50` — **opaque-symbol syntax**; attributes: `function, total, symbol(floatLt), no-evaluators` — `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`

423. `reference-semantics/semantics/float.k:51` — **concrete rule**; attributes: `concrete` — `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`

424. `reference-semantics/semantics/float.k:52` — **ordinary rule**; attributes: `none` — `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`

425. `reference-semantics/semantics/float.k:54` — **opaque-symbol syntax**; attributes: `function, total, symbol(absF), no-evaluators` — `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`

426. `reference-semantics/semantics/float.k:55` — **concrete rule**; attributes: `concrete` — `rule absF(F:Float) => absFloat(F) [concrete]`

427. `reference-semantics/semantics/float.k:56` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)`

428. `reference-semantics/semantics/float.k:61` — **ordinary rule**; attributes: `none` — `rule <k> Import(_:String) => .K ... </k>`

429. `reference-semantics/semantics/float.k:65` — **syntax**; attributes: `none` — `syntax KItem ::= "#mathCeil"`

430. `reference-semantics/semantics/float.k:66` — **priority rule**; attributes: `priority(40)` — `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`

431. `reference-semantics/semantics/float.k:67` — **ordinary rule**; attributes: `none` — `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>`

432. `reference-semantics/semantics/float.k:70` — **syntax**; attributes: `none` — `syntax KItem ::= "#mathFloor"`

433. `reference-semantics/semantics/float.k:71` — **priority rule**; attributes: `priority(40)` — `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`

434. `reference-semantics/semantics/float.k:72` — **ordinary rule**; attributes: `none` — `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`

435. `reference-semantics/semantics/float.k:73` — **function syntax**; attributes: `function, total, symbol(floorFI)` — `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`

436. `reference-semantics/semantics/float.k:74` — **concrete rule**; attributes: `concrete` — `rule floorFI(I:Int)   => I                        [concrete]`

437. `reference-semantics/semantics/float.k:75` — **concrete rule**; attributes: `concrete` — `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]`

438. `reference-semantics/semantics/float.k:78` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`

439. `reference-semantics/semantics/float.k:79` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)`

440. `reference-semantics/semantics/float.k:82` — **syntax**; attributes: `none` — `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`

441. `reference-semantics/semantics/float.k:83` — **priority rule**; attributes: `priority(40)` — `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`

442. `reference-semantics/semantics/float.k:84` — **ordinary rule**; attributes: `none` — `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`

443. `reference-semantics/semantics/float.k:85` — **ordinary rule**; attributes: `none` — `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`

444. `reference-semantics/semantics/float.k:86` — **function syntax**; attributes: `function, total, symbol(toF)` — `syntax Float ::= toF(Val) [function, total, symbol(toF)]`

445. `reference-semantics/semantics/float.k:87` — **concrete rule**; attributes: `concrete` — `rule toF(F:Float) => F        [concrete]`

446. `reference-semantics/semantics/float.k:88` — **concrete rule**; attributes: `concrete` — `rule toF(I:Int)   => intToF(I) [concrete]`

447. `reference-semantics/semantics/float.k:93` — **function syntax**; attributes: `function, total, symbol(ceilF)` — `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`

448. `reference-semantics/semantics/float.k:94` — **concrete rule**; attributes: `concrete` — `rule ceilF(I:Int)   => I                       [concrete]`

449. `reference-semantics/semantics/float.k:95` — **concrete rule**; attributes: `concrete` — `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]`

450. `reference-semantics/semantics/float.k:99` — **ordinary rule**; attributes: `none` — `rule applyUn("-", F:Float) => 0.0 -Float F`

451. `reference-semantics/semantics/float.k:103` — **opaque-symbol syntax**; attributes: `function, total, symbol(subF), no-evaluators` — `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`

452. `reference-semantics/semantics/float.k:104` — **concrete rule**; attributes: `concrete` — `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`

453. `reference-semantics/semantics/float.k:105` — **ordinary rule**; attributes: `none` — `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`

454. `reference-semantics/semantics/float.k:107` — **opaque-symbol syntax**; attributes: `function, total, symbol(divF), no-evaluators` — `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`

455. `reference-semantics/semantics/float.k:108` — **concrete rule**; attributes: `concrete` — `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`

456. `reference-semantics/semantics/float.k:109` — **ordinary rule**; attributes: `none` — `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`

457. `reference-semantics/semantics/float.k:111` — **opaque-symbol syntax**; attributes: `function, total, symbol(addF), no-evaluators` — `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`

458. `reference-semantics/semantics/float.k:112` — **concrete rule**; attributes: `concrete` — `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`

459. `reference-semantics/semantics/float.k:113` — **ordinary rule**; attributes: `none` — `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`

460. `reference-semantics/semantics/float.k:115` — **opaque-symbol syntax**; attributes: `function, total, symbol(mulF), no-evaluators` — `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`

461. `reference-semantics/semantics/float.k:116` — **concrete rule**; attributes: `concrete` — `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`

462. `reference-semantics/semantics/float.k:117` — **ordinary rule**; attributes: `none` — `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`

463. `reference-semantics/semantics/float.k:119` — **opaque-symbol syntax**; attributes: `function, total, symbol(powF), no-evaluators` — `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`

464. `reference-semantics/semantics/float.k:120` — **concrete rule**; attributes: `concrete` — `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`

465. `reference-semantics/semantics/float.k:121` — **ordinary rule**; attributes: `none` — `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)`

466. `reference-semantics/semantics/float.k:125` — **opaque-symbol syntax**; attributes: `function, total, symbol(gtF), no-evaluators` — `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`

467. `reference-semantics/semantics/float.k:126` — **concrete rule**; attributes: `concrete` — `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`

468. `reference-semantics/semantics/float.k:127` — **ordinary rule**; attributes: `none` — `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)`

469. `reference-semantics/semantics/float.k:128` — **ordinary rule**; attributes: `none` — `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`

470. `reference-semantics/semantics/float.k:129` — **ordinary rule**; attributes: `none` — `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)`

471. `reference-semantics/semantics/float.k:132` — **ordinary rule**; attributes: `none` — `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`

472. `reference-semantics/semantics/float.k:133` — **ordinary rule**; attributes: `none` — `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`

473. `reference-semantics/semantics/float.k:134` — **ordinary rule**; attributes: `none` — `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)`

474. `reference-semantics/semantics/float.k:135` — **ordinary rule**; attributes: `none` — `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))`

475. `reference-semantics/semantics/float.k:136` — **ordinary rule**; attributes: `none` — `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)`

476. `reference-semantics/semantics/float.k:137` — **ordinary rule**; attributes: `none` — `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))`

477. `reference-semantics/semantics/float.k:138` — **ordinary rule**; attributes: `none` — `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)`

478. `reference-semantics/semantics/float.k:139` — **ordinary rule**; attributes: `none` — `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))`

479. `reference-semantics/semantics/float.k:142` — **opaque-symbol syntax**; attributes: `function, total, symbol(eqF), no-evaluators` — `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`

480. `reference-semantics/semantics/float.k:143` — **concrete rule**; attributes: `concrete` — `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`

481. `reference-semantics/semantics/float.k:144` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`

482. `reference-semantics/semantics/float.k:145` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`

483. `reference-semantics/semantics/float.k:146` — **ordinary rule**; attributes: `none` — `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`

484. `reference-semantics/semantics/float.k:147` — **ordinary rule**; attributes: `none` — `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`

485. `reference-semantics/semantics/float.k:148` — **ordinary rule**; attributes: `none` — `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)`

486. `reference-semantics/semantics/float.k:149` — **ordinary rule**; attributes: `none` — `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))`

487. `reference-semantics/semantics/float.k:150` — **ordinary rule**; attributes: `none` — `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)`

488. `reference-semantics/semantics/float.k:151` — **ordinary rule**; attributes: `none` — `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))`

489. `reference-semantics/semantics/float.k:154` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", V:Val, noneV) => V ==K noneV`

490. `reference-semantics/semantics/float.k:155` — **ordinary rule**; attributes: `none` — `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)`

491. `reference-semantics/semantics/float.k:160` — **opaque-symbol syntax**; attributes: `function, total, symbol(decStrToF), no-evaluators` — `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`

492. `reference-semantics/semantics/float.k:161` — **concrete rule**; attributes: `concrete` — `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`

493. `reference-semantics/semantics/float.k:162` — **concrete rule**; attributes: `concrete` — `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]`

494. `reference-semantics/semantics/float.k:165` — **function syntax**; attributes: `function` — `syntax Int ::= headIS(IntSeq) [function]`

495. `reference-semantics/semantics/float.k:166` — **ordinary rule**; attributes: `none` — `rule headIS(iCons(C:Int, _:IntSeq)) => C`

496. `reference-semantics/semantics/float.k:167` — **function syntax**; attributes: `function, total, function, total` — `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`

497. `reference-semantics/semantics/float.k:168` — **ordinary rule**; attributes: `none` — `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`

498. `reference-semantics/semantics/float.k:169` — **ordinary rule**; attributes: `none` — `rule intPartAcc(.IntSeq, A:Int) => A`

499. `reference-semantics/semantics/float.k:170` — **ordinary rule**; attributes: `none` — `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`

500. `reference-semantics/semantics/float.k:171` — **ordinary rule**; attributes: `none` — `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46`

501. `reference-semantics/semantics/float.k:173` — **function syntax**; attributes: `function, total, function, total` — `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`

502. `reference-semantics/semantics/float.k:174` — **ordinary rule**; attributes: `none` — `rule fracPart(.IntSeq) => 0`

503. `reference-semantics/semantics/float.k:175` — **ordinary rule**; attributes: `none` — `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`

504. `reference-semantics/semantics/float.k:176` — **ordinary rule**; attributes: `none` — `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`

505. `reference-semantics/semantics/float.k:177` — **ordinary rule**; attributes: `none` — `rule fracAcc(.IntSeq, A:Int) => A`

506. `reference-semantics/semantics/float.k:178` — **ordinary rule**; attributes: `none` — `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`

507. `reference-semantics/semantics/float.k:179` — **function syntax**; attributes: `function, total, function, total` — `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`

508. `reference-semantics/semantics/float.k:180` — **ordinary rule**; attributes: `none` — `rule fracScale(.IntSeq) => 1`

509. `reference-semantics/semantics/float.k:181` — **ordinary rule**; attributes: `none` — `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`

510. `reference-semantics/semantics/float.k:182` — **ordinary rule**; attributes: `none` — `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`

511. `reference-semantics/semantics/float.k:183` — **ordinary rule**; attributes: `none` — `rule fscAcc(.IntSeq, A:Int) => A`

512. `reference-semantics/semantics/float.k:184` — **ordinary rule**; attributes: `none` — `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`

513. `reference-semantics/semantics/float.k:185` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`

514. `reference-semantics/semantics/float.k:186` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)`

515. `reference-semantics/semantics/float.k:187` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("float", F:Float, .Vals)        => F`

516. `reference-semantics/semantics/float.k:190` — **opaque-symbol syntax**; attributes: `function, total, symbol(divFloatIntV), no-evaluators` — `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`

517. `reference-semantics/semantics/float.k:191` — **concrete rule**; attributes: `concrete` — `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`

518. `reference-semantics/semantics/float.k:192` — **ordinary rule**; attributes: `none` — `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)`

519. `reference-semantics/semantics/float.k:195` — **opaque-symbol syntax**; attributes: `function, total, symbol(intToF), no-evaluators` — `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`

520. `reference-semantics/semantics/float.k:196` — **concrete rule**; attributes: `concrete` — `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`

521. `reference-semantics/semantics/float.k:197` — **ordinary rule**; attributes: `none` — `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`

522. `reference-semantics/semantics/float.k:198` — **ordinary rule**; attributes: `none` — `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`

523. `reference-semantics/semantics/float.k:199` — **ordinary rule**; attributes: `none` — `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`

524. `reference-semantics/semantics/float.k:200` — **ordinary rule**; attributes: `none` — `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`

525. `reference-semantics/semantics/float.k:201` — **ordinary rule**; attributes: `none` — `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`

526. `reference-semantics/semantics/float.k:202` — **ordinary rule**; attributes: `none` — `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`

527. `reference-semantics/semantics/float.k:203` — **ordinary rule**; attributes: `none` — `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`

528. `reference-semantics/semantics/float.k:204` — **ordinary rule**; attributes: `none` — `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`

529. `reference-semantics/semantics/float.k:205` — **ordinary rule**; attributes: `none` — `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`

530. `reference-semantics/semantics/float.k:206` — **ordinary rule**; attributes: `none` — `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`

531. `reference-semantics/semantics/float.k:209` — **opaque-symbol syntax**; attributes: `function, total, symbol(truncF), no-evaluators` — `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`

532. `reference-semantics/semantics/float.k:210` — **concrete rule**; attributes: `concrete` — `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`

533. `reference-semantics/semantics/float.k:211` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`

534. `reference-semantics/semantics/float.k:213` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)`

535. `reference-semantics/semantics/float.k:214` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("float", F:Float, .Vals) => F`

536. `reference-semantics/semantics/float.k:217` — **opaque-symbol syntax**; attributes: `function, total, symbol(roundF), no-evaluators` — `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`

537. `reference-semantics/semantics/float.k:218` — **concrete rule**; attributes: `concrete` — `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`

538. `reference-semantics/semantics/float.k:223` — **opaque-symbol syntax**; attributes: `function, total, symbol(roundFN), no-evaluators` — `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`

539. `reference-semantics/semantics/float.k:224` — **concrete rule**; attributes: `concrete` — `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`

540. `reference-semantics/semantics/float.k:227` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)`

541. `reference-semantics/semantics/float.k:228` — **ordinary rule**; attributes: `none` — `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`

542. `reference-semantics/semantics/float.k:230` — **opaque-symbol syntax**; attributes: `function, total, symbol(sqrtF), no-evaluators` — `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`

543. `reference-semantics/semantics/float.k:231` — **concrete rule**; attributes: `concrete` — `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`

544. `reference-semantics/semantics/float.k:232` — **syntax**; attributes: `none` — `syntax KItem ::= "#mathSqrt"`

545. `reference-semantics/semantics/float.k:233` — **priority rule**; attributes: `priority(40)` — `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`

546. `reference-semantics/semantics/float.k:234` — **ordinary rule**; attributes: `none` — `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`

547. `reference-semantics/semantics/float.k:235` — **ordinary rule**; attributes: `none` — `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>`

548. `reference-semantics/semantics/float.k:243` — **syntax**; attributes: `none` — `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`

549. `reference-semantics/semantics/float.k:244` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`

550. `reference-semantics/semantics/float.k:245` — **ordinary rule**; attributes: `none` — `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`

551. `reference-semantics/semantics/float.k:246` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`

552. `reference-semantics/semantics/float.k:247` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`

553. `reference-semantics/semantics/float.k:250` — **syntax**; attributes: `none` — `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`

554. `reference-semantics/semantics/float.k:251` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`

555. `reference-semantics/semantics/float.k:252` — **ordinary rule**; attributes: `none` — `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`

556. `reference-semantics/semantics/float.k:253` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`

557. `reference-semantics/semantics/float.k:254` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`

558. `reference-semantics/semantics/float.k:261` — **syntax**; attributes: `none` — `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`

559. `reference-semantics/semantics/float.k:262` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))`

560. `reference-semantics/semantics/float.k:265` — **ordinary rule**; attributes: `none` — `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`

561. `reference-semantics/semantics/float.k:266` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`

562. `reference-semantics/semantics/float.k:267` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)`

563. `reference-semantics/semantics/float.k:270` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)`

## `reference-semantics/semantics/functions.k`

564. `reference-semantics/semantics/functions.k:8` — **syntax**; attributes: `none` — `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall"`

565. `reference-semantics/semantics/functions.k:14` — **ordinary rule**; attributes: `none` — `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`

566. `reference-semantics/semantics/functions.k:18` — **syntax**; attributes: `none` — `syntax Expr ::= closureExpr(ParamNames, Stmts)`

567. `reference-semantics/semantics/functions.k:19` — **ordinary rule**; attributes: `none` — `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>`

568. `reference-semantics/semantics/functions.k:27` — **syntax**; attributes: `none` — `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)`

569. `reference-semantics/semantics/functions.k:31` — **syntax**; attributes: `none` — `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`

570. `reference-semantics/semantics/functions.k:33` — **ordinary rule**; attributes: `none` — `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`

571. `reference-semantics/semantics/functions.k:36` — **ordinary rule**; attributes: `none` — `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`

572. `reference-semantics/semantics/functions.k:42` — **ordinary rule**; attributes: `none` — `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`

573. `reference-semantics/semantics/functions.k:47` — **ordinary rule**; attributes: `none` — `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`

574. `reference-semantics/semantics/functions.k:50` — **ordinary rule**; attributes: `none` — `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`

575. `reference-semantics/semantics/functions.k:53` — **ordinary rule**; attributes: `none` — `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`

576. `reference-semantics/semantics/functions.k:59` — **ordinary rule**; attributes: `none` — `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>`

577. `reference-semantics/semantics/functions.k:63` — **ordinary rule**; attributes: `none` — `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`

578. `reference-semantics/semantics/functions.k:64` — **ordinary rule**; attributes: `none` — `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>`

579. `reference-semantics/semantics/functions.k:68` — **priority rule**; attributes: `priority(40)` — `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]`

580. `reference-semantics/semantics/functions.k:78` — **ordinary rule**; attributes: `none` — `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`

581. `reference-semantics/semantics/functions.k:80` — **ordinary rule**; attributes: `none` — `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>`

582. `reference-semantics/semantics/functions.k:85` — **ordinary rule**; attributes: `none` — `rule <k> #pop => V ~> CONT </k> <ret>   retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env>   L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`

## `reference-semantics/semantics/int.k`

583. `reference-semantics/semantics/int.k:7` — **ordinary rule**; attributes: `none` — `rule applyUn("-", I:Int) => 0 -Int I`

584. `reference-semantics/semantics/int.k:9` — **ordinary rule**; attributes: `none` — `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2`

585. `reference-semantics/semantics/int.k:11` — **ordinary rule**; attributes: `none` — `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`

586. `reference-semantics/semantics/int.k:12` — **ordinary rule**; attributes: `none` — `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`

587. `reference-semantics/semantics/int.k:13` — **ordinary rule**; attributes: `none` — `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2`

588. `reference-semantics/semantics/int.k:14` — **ordinary rule**; attributes: `none` — `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2`

589. `reference-semantics/semantics/int.k:15` — **ordinary rule**; attributes: `none` — `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)`

590. `reference-semantics/semantics/int.k:16` — **ordinary rule**; attributes: `none` — `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2`

591. `reference-semantics/semantics/int.k:17` — **ordinary rule**; attributes: `none` — `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`

592. `reference-semantics/semantics/int.k:19` — **function syntax**; attributes: `function` — `syntax Int ::= pyMod(Int, Int) [function]`

593. `reference-semantics/semantics/int.k:20` — **ordinary rule**; attributes: `none` — `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`

594. `reference-semantics/semantics/int.k:22` — **ordinary rule**; attributes: `none` — `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2`

595. `reference-semantics/semantics/int.k:23` — **ordinary rule**; attributes: `none` — `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2`

596. `reference-semantics/semantics/int.k:24` — **ordinary rule**; attributes: `none` — `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2`

597. `reference-semantics/semantics/int.k:25` — **ordinary rule**; attributes: `none` — `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2`

598. `reference-semantics/semantics/int.k:26` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2`

599. `reference-semantics/semantics/int.k:27` — **ordinary rule**; attributes: `none` — `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2`

## `reference-semantics/semantics/iter.k`

600. `reference-semantics/semantics/iter.k:8` — **syntax**; attributes: `none` — `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`

## `reference-semantics/semantics/list.k`

601. `reference-semantics/semantics/list.k:9` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>`

602. `reference-semantics/semantics/list.k:10` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>`

603. `reference-semantics/semantics/list.k:13` — **syntax**; attributes: `none` — `syntax ApplyK ::= "toList"`

604. `reference-semantics/semantics/list.k:14` — **ordinary rule**; attributes: `none` — `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`

605. `reference-semantics/semantics/list.k:15` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>`

606. `reference-semantics/semantics/list.k:18` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`

607. `reference-semantics/semantics/list.k:19` — **ordinary rule**; attributes: `none` — `rule valSeqConcat(.ValSeq, T:ValSeq)                => T`

608. `reference-semantics/semantics/list.k:20` — **ordinary rule**; attributes: `none` — `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))`

609. `reference-semantics/semantics/list.k:24` — **priority rule**; attributes: `priority(45)` — `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`

610. `reference-semantics/semantics/list.k:27` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`

611. `reference-semantics/semantics/list.k:28` — **ordinary rule**; attributes: `none` — `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)`

612. `reference-semantics/semantics/list.k:33` — **function syntax**; attributes: `function, total` — `syntax Bool ::= hasRefVS(ValSeq) [function, total]`

613. `reference-semantics/semantics/list.k:34` — **ordinary rule**; attributes: `none` — `rule hasRefVS(.ValSeq)                => false`

614. `reference-semantics/semantics/list.k:35` — **ordinary rule**; attributes: `none` — `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`

615. `reference-semantics/semantics/list.k:37` — **function syntax**; attributes: `function, function` — `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map)        [function]`

616. `reference-semantics/semantics/list.k:39` — **ordinary rule**; attributes: `none` — `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true`

617. `reference-semantics/semantics/list.k:40` — **ordinary rule**; attributes: `none` — `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false`

618. `reference-semantics/semantics/list.k:41` — **ordinary rule**; attributes: `none` — `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false`

619. `reference-semantics/semantics/list.k:42` — **ordinary rule**; attributes: `none` — `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`

620. `reference-semantics/semantics/list.k:45` — **ordinary rule**; attributes: `none` — `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)`

621. `reference-semantics/semantics/list.k:47` — **ordinary rule**; attributes: `none` — `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)`

622. `reference-semantics/semantics/list.k:49` — **ordinary rule**; attributes: `none` — `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`

623. `reference-semantics/semantics/list.k:50` — **owise rule**; attributes: `owise` — `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]`

624. `reference-semantics/semantics/list.k:53` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]`

625. `reference-semantics/semantics/list.k:58` — **syntax**; attributes: `none` — `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`

626. `reference-semantics/semantics/list.k:59` — **ordinary rule**; attributes: `none` — `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`

627. `reference-semantics/semantics/list.k:60` — **ordinary rule**; attributes: `none` — `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`

628. `reference-semantics/semantics/list.k:61` — **ordinary rule**; attributes: `none` — `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`

629. `reference-semantics/semantics/list.k:62` — **ordinary rule**; attributes: `none` — `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`

630. `reference-semantics/semantics/list.k:63` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V`

631. `reference-semantics/semantics/list.k:65` — **ordinary rule**; attributes: `none` — `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)`

632. `reference-semantics/semantics/list.k:67` — **ordinary rule**; attributes: `none` — `rule <k> B:Bool ~> #notB => notBool B ... </k>`

## `reference-semantics/semantics/methods.k`

633. `reference-semantics/semantics/methods.k:10` — **function syntax**; attributes: `function` — `syntax Val ::= applyMethod(Val, String, Vals) [function]`

634. `reference-semantics/semantics/methods.k:13` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`

635. `reference-semantics/semantics/methods.k:14` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`

636. `reference-semantics/semantics/methods.k:15` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`

637. `reference-semantics/semantics/methods.k:16` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)`

638. `reference-semantics/semantics/methods.k:19` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))`

639. `reference-semantics/semantics/methods.k:20` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))`

640. `reference-semantics/semantics/methods.k:21` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))`

641. `reference-semantics/semantics/methods.k:26` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`

642. `reference-semantics/semantics/methods.k:27` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`

643. `reference-semantics/semantics/methods.k:28` — **ordinary rule**; attributes: `none` — `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`

644. `reference-semantics/semantics/methods.k:29` — **ordinary rule**; attributes: `none` — `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`

645. `reference-semantics/semantics/methods.k:30` — **ordinary rule**; attributes: `none` — `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))`

646. `reference-semantics/semantics/methods.k:34` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`

647. `reference-semantics/semantics/methods.k:35` — **function syntax**; attributes: `function` — `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`

648. `reference-semantics/semantics/methods.k:36` — **ordinary rule**; attributes: `none` — `rule cntSub(.IntSeq, _:IntSeq) => 0`

649. `reference-semantics/semantics/methods.k:37` — **ordinary rule**; attributes: `none` — `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0`

650. `reference-semantics/semantics/methods.k:39` — **ordinary rule**; attributes: `none` — `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0`

651. `reference-semantics/semantics/methods.k:41` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`

652. `reference-semantics/semantics/methods.k:42` — **ordinary rule**; attributes: `none` — `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`

653. `reference-semantics/semantics/methods.k:43` — **owise rule**; attributes: `owise` — `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`

654. `reference-semantics/semantics/methods.k:44` — **ordinary rule**; attributes: `none` — `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0`

655. `reference-semantics/semantics/methods.k:47` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`

656. `reference-semantics/semantics/methods.k:48` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= trimWS(IntSeq) [function, total]`

657. `reference-semantics/semantics/methods.k:49` — **ordinary rule**; attributes: `none` — `rule trimWS(.IntSeq) => .IntSeq`

658. `reference-semantics/semantics/methods.k:50` — **ordinary rule**; attributes: `none` — `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`

659. `reference-semantics/semantics/methods.k:51` — **ordinary rule**; attributes: `none` — `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`

660. `reference-semantics/semantics/methods.k:52` — **function syntax**; attributes: `function, total, function, total` — `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`

661. `reference-semantics/semantics/methods.k:53` — **ordinary rule**; attributes: `none` — `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`

662. `reference-semantics/semantics/methods.k:54` — **ordinary rule**; attributes: `none` — `rule revISAcc(.IntSeq, A:IntSeq) => A`

663. `reference-semantics/semantics/methods.k:55` — **ordinary rule**; attributes: `none` — `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))`

664. `reference-semantics/semantics/methods.k:58` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)`

665. `reference-semantics/semantics/methods.k:61` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)`

666. `reference-semantics/semantics/methods.k:64` — **ordinary rule**; attributes: `none` — `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`

667. `reference-semantics/semantics/methods.k:65` — **function syntax**; attributes: `function, total` — `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`

668. `reference-semantics/semantics/methods.k:66` — **ordinary rule**; attributes: `none` — `rule cntOccVS(.ValSeq, _:Val)                => 0`

669. `reference-semantics/semantics/methods.k:67` — **ordinary rule**; attributes: `none` — `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`

670. `reference-semantics/semantics/methods.k:68` — **ordinary rule**; attributes: `none` — `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)`

671. `reference-semantics/semantics/methods.k:72` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`

672. `reference-semantics/semantics/methods.k:75` — **function syntax**; attributes: `function` — `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result`

673. `reference-semantics/semantics/methods.k:76` — **ordinary rule**; attributes: `none` — `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`

674. `reference-semantics/semantics/methods.k:77` — **ordinary rule**; attributes: `none` — `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)`

675. `reference-semantics/semantics/methods.k:79` — **ordinary rule**; attributes: `none` — `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)`

676. `reference-semantics/semantics/methods.k:82` — **function syntax**; attributes: `function` — `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`

677. `reference-semantics/semantics/methods.k:83` — **ordinary rule**; attributes: `none` — `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC`

678. `reference-semantics/semantics/methods.k:84` — **ordinary rule**; attributes: `none` — `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`

679. `reference-semantics/semantics/methods.k:85` — **function syntax**; attributes: `function, total` — `syntax Bool ::= isWSC(Int) [function, total]`

680. `reference-semantics/semantics/methods.k:86` — **ordinary rule**; attributes: `none` — `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13`

681. `reference-semantics/semantics/methods.k:89` — **priority rule**; attributes: `priority(39)` — `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]`

682. `reference-semantics/semantics/methods.k:94` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`

683. `reference-semantics/semantics/methods.k:97` — **function syntax**; attributes: `function` — `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token`

684. `reference-semantics/semantics/methods.k:98` — **ordinary rule**; attributes: `none` — `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)`

685. `reference-semantics/semantics/methods.k:99` — **ordinary rule**; attributes: `none` — `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP`

686. `reference-semantics/semantics/methods.k:101` — **ordinary rule**; attributes: `none` — `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)`

687. `reference-semantics/semantics/methods.k:104` — **ordinary rule**; attributes: `none` — `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`

688. `reference-semantics/semantics/methods.k:106` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`

689. `reference-semantics/semantics/methods.k:107` — **ordinary rule**; attributes: `none` — `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq`

690. `reference-semantics/semantics/methods.k:108` — **ordinary rule**; attributes: `none` — `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`

691. `reference-semantics/semantics/methods.k:109` — **ordinary rule**; attributes: `none` — `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)`

692. `reference-semantics/semantics/methods.k:112` — **function syntax**; attributes: `function, total` — `syntax Bool ::= isUpperC(Int) [function, total]`

693. `reference-semantics/semantics/methods.k:113` — **ordinary rule**; attributes: `none` — `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`

694. `reference-semantics/semantics/methods.k:115` — **function syntax**; attributes: `function, total` — `syntax Bool ::= isLowerC(Int) [function, total]`

695. `reference-semantics/semantics/methods.k:116` — **ordinary rule**; attributes: `none` — `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`

696. `reference-semantics/semantics/methods.k:118` — **function syntax**; attributes: `function, total` — `syntax Bool ::= isAlphaC(Int) [function, total]`

697. `reference-semantics/semantics/methods.k:119` — **ordinary rule**; attributes: `none` — `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`

698. `reference-semantics/semantics/methods.k:121` — **function syntax**; attributes: `function, total` — `syntax Bool ::= isDigitC(Int) [function, total]`

699. `reference-semantics/semantics/methods.k:122` — **ordinary rule**; attributes: `none` — `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`

700. `reference-semantics/semantics/methods.k:124` — **function syntax**; attributes: `function, total` — `syntax Bool ::= hasUpper(IntSeq) [function, total]`

701. `reference-semantics/semantics/methods.k:125` — **ordinary rule**; attributes: `none` — `rule hasUpper(.IntSeq) => false`

702. `reference-semantics/semantics/methods.k:126` — **ordinary rule**; attributes: `none` — `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`

703. `reference-semantics/semantics/methods.k:128` — **function syntax**; attributes: `function, total` — `syntax Bool ::= hasLower(IntSeq) [function, total]`

704. `reference-semantics/semantics/methods.k:129` — **ordinary rule**; attributes: `none` — `rule hasLower(.IntSeq) => false`

705. `reference-semantics/semantics/methods.k:130` — **ordinary rule**; attributes: `none` — `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`

706. `reference-semantics/semantics/methods.k:132` — **function syntax**; attributes: `function, total` — `syntax Bool ::= allAlpha(IntSeq) [function, total]`

707. `reference-semantics/semantics/methods.k:133` — **ordinary rule**; attributes: `none` — `rule allAlpha(.IntSeq) => true`

708. `reference-semantics/semantics/methods.k:134` — **ordinary rule**; attributes: `none` — `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`

709. `reference-semantics/semantics/methods.k:136` — **function syntax**; attributes: `function, total` — `syntax Bool ::= allDigit(IntSeq) [function, total]`

710. `reference-semantics/semantics/methods.k:137` — **ordinary rule**; attributes: `none` — `rule allDigit(.IntSeq) => true`

711. `reference-semantics/semantics/methods.k:138` — **ordinary rule**; attributes: `none` — `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`

712. `reference-semantics/semantics/methods.k:140` — **function syntax**; attributes: `function, total` — `syntax Int ::= lowerC(Int) [function, total]`

713. `reference-semantics/semantics/methods.k:142` — **ordinary rule**; attributes: `none` — `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`

714. `reference-semantics/semantics/methods.k:143` — **owise rule**; attributes: `owise` — `rule lowerC(C:Int) => C         [owise]`

715. `reference-semantics/semantics/methods.k:145` — **function syntax**; attributes: `function, total` — `syntax Int ::= upperC(Int) [function, total]`

716. `reference-semantics/semantics/methods.k:146` — **ordinary rule**; attributes: `none` — `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`

717. `reference-semantics/semantics/methods.k:147` — **owise rule**; attributes: `owise` — `rule upperC(C:Int) => C         [owise]`

718. `reference-semantics/semantics/methods.k:149` — **function syntax**; attributes: `function, total` — `syntax Int ::= swapC(Int) [function, total]`

719. `reference-semantics/semantics/methods.k:150` — **ordinary rule**; attributes: `none` — `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`

720. `reference-semantics/semantics/methods.k:151` — **ordinary rule**; attributes: `none` — `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`

721. `reference-semantics/semantics/methods.k:152` — **owise rule**; attributes: `owise` — `rule swapC(C:Int) => C         [owise]`

722. `reference-semantics/semantics/methods.k:154` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= mapLower(IntSeq) [function, total]`

723. `reference-semantics/semantics/methods.k:155` — **ordinary rule**; attributes: `none` — `rule mapLower(.IntSeq) => .IntSeq`

724. `reference-semantics/semantics/methods.k:156` — **ordinary rule**; attributes: `none` — `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`

725. `reference-semantics/semantics/methods.k:158` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`

726. `reference-semantics/semantics/methods.k:159` — **ordinary rule**; attributes: `none` — `rule mapUpper(.IntSeq) => .IntSeq`

727. `reference-semantics/semantics/methods.k:160` — **ordinary rule**; attributes: `none` — `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`

728. `reference-semantics/semantics/methods.k:162` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`

729. `reference-semantics/semantics/methods.k:163` — **ordinary rule**; attributes: `none` — `rule mapSwap(.IntSeq) => .IntSeq`

730. `reference-semantics/semantics/methods.k:164` — **ordinary rule**; attributes: `none` — `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`

731. `reference-semantics/semantics/methods.k:166` — **function syntax**; attributes: `function, total` — `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`

732. `reference-semantics/semantics/methods.k:167` — **ordinary rule**; attributes: `none` — `rule startsWith(.IntSeq, _:IntSeq)               => true`

733. `reference-semantics/semantics/methods.k:168` — **ordinary rule**; attributes: `none` — `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`

734. `reference-semantics/semantics/methods.k:169` — **ordinary rule**; attributes: `none` — `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`

## `reference-semantics/semantics/operators.k`

735. `reference-semantics/semantics/operators.k:10` — **ordinary rule**; attributes: `none` — `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`

736. `reference-semantics/semantics/operators.k:12` — **ordinary rule**; attributes: `none` — `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>`

737. `reference-semantics/semantics/operators.k:15` — **context**; attributes: `none` — `context Compare(HOLE, _)`

738. `reference-semantics/semantics/operators.k:16` — **context**; attributes: `none` — `context Compare(_:Val, CmpOp(_, HOLE))`

739. `reference-semantics/semantics/operators.k:17` — **owise rule**; attributes: `owise` — `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`

740. `reference-semantics/semantics/operators.k:19` — **ordinary rule**; attributes: `none` — `rule applyCmp("is",     V:Val, noneV) => V ==K noneV`

741. `reference-semantics/semantics/operators.k:20` — **ordinary rule**; attributes: `none` — `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)`

742. `reference-semantics/semantics/operators.k:25` — **priority rule**; attributes: `priority(40)` — `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

743. `reference-semantics/semantics/operators.k:28` — **priority rule**; attributes: `priority(40)` — `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]`

744. `reference-semantics/semantics/operators.k:34` — **priority rule**; attributes: `priority(40)` — `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]`

745. `reference-semantics/semantics/operators.k:38` — **priority rule**; attributes: `priority(40)` — `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]`

746. `reference-semantics/semantics/operators.k:44` — **priority rule**; attributes: `priority(40)` — `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## `reference-semantics/semantics/range.k`

747. `reference-semantics/semantics/range.k:9` — **function syntax**; attributes: `function, total` — `syntax Bool ::= inRange(Int, Int, Int) [function, total]`

748. `reference-semantics/semantics/range.k:10` — **ordinary rule**; attributes: `none` — `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`

749. `reference-semantics/semantics/range.k:12` — **function syntax**; attributes: `function` — `syntax Int ::= rangeLen(Int, Int, Int) [function]`

750. `reference-semantics/semantics/range.k:13` — **ordinary rule**; attributes: `none` — `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO`

751. `reference-semantics/semantics/range.k:15` — **ordinary rule**; attributes: `none` — `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO`

752. `reference-semantics/semantics/range.k:17` — **ordinary rule**; attributes: `none` — `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)`

753. `reference-semantics/semantics/range.k:20` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)`

754. `reference-semantics/semantics/range.k:23` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)`

## `reference-semantics/semantics/set.k`

755. `reference-semantics/semantics/set.k:8` — **syntax**; attributes: `none` — `syntax Val ::= setV(IntSeq)`

756. `reference-semantics/semantics/set.k:11` — **function syntax**; attributes: `function, total` — `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`

757. `reference-semantics/semantics/set.k:12` — **ordinary rule**; attributes: `none` — `rule codeIn(_:Int, .IntSeq)                => false`

758. `reference-semantics/semantics/set.k:13` — **ordinary rule**; attributes: `none` — `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)`

759. `reference-semantics/semantics/set.k:16` — **function syntax**; attributes: `function, total, function, total` — `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total] | dedupFrom(IntSeq, IntSeq)  [function, total]`

760. `reference-semantics/semantics/set.k:18` — **ordinary rule**; attributes: `none` — `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`

761. `reference-semantics/semantics/set.k:19` — **ordinary rule**; attributes: `none` — `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`

762. `reference-semantics/semantics/set.k:20` — **ordinary rule**; attributes: `none` — `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)`

763. `reference-semantics/semantics/set.k:22` — **ordinary rule**; attributes: `none` — `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)`

764. `reference-semantics/semantics/set.k:25` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`

765. `reference-semantics/semantics/set.k:26` — **ordinary rule**; attributes: `none` — `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)`

766. `reference-semantics/semantics/set.k:27` — **ordinary rule**; attributes: `none` — `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))`

767. `reference-semantics/semantics/set.k:31` — **function syntax**; attributes: `function, total` — `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`

768. `reference-semantics/semantics/set.k:32` — **ordinary rule**; attributes: `none` — `rule subsetCodes(.IntSeq, _:IntSeq)                => true`

769. `reference-semantics/semantics/set.k:33` — **ordinary rule**; attributes: `none` — `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`

770. `reference-semantics/semantics/set.k:35` — **function syntax**; attributes: `function, total` — `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`

771. `reference-semantics/semantics/set.k:36` — **ordinary rule**; attributes: `none` — `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)`

772. `reference-semantics/semantics/set.k:39` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`

## `reference-semantics/semantics/sort.k`

773. `reference-semantics/semantics/sort.k:18` — **opaque-symbol syntax**; attributes: `function, total, symbol(sortVS), no-evaluators` — `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`

774. `reference-semantics/semantics/sort.k:19` — **function syntax**; attributes: `function` — `syntax ValSeq ::= insVS(Int, ValSeq) [function]`

775. `reference-semantics/semantics/sort.k:20` — **concrete rule**; attributes: `concrete` — `rule sortVS(.ValSeq)                => .ValSeq          [concrete]`

776. `reference-semantics/semantics/sort.k:21` — **concrete rule**; attributes: `concrete` — `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`

777. `reference-semantics/semantics/sort.k:22` — **concrete rule**; attributes: `concrete` — `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]`

778. `reference-semantics/semantics/sort.k:23` — **concrete rule**; attributes: `concrete` — `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`

779. `reference-semantics/semantics/sort.k:24` — **concrete rule**; attributes: `concrete` — `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]`

780. `reference-semantics/semantics/sort.k:26` — **function syntax**; attributes: `function` — `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`

781. `reference-semantics/semantics/sort.k:27` — **concrete rule**; attributes: `concrete` — `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`

782. `reference-semantics/semantics/sort.k:28` — **concrete rule**; attributes: `concrete` — `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`

783. `reference-semantics/semantics/sort.k:29` — **concrete rule**; attributes: `concrete` — `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]`

784. `reference-semantics/semantics/sort.k:31` — **concrete rule**; attributes: `concrete` — `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]`

785. `reference-semantics/semantics/sort.k:36` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>`

786. `reference-semantics/semantics/sort.k:40` — **priority rule**; attributes: `priority(40)` — `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]`

787. `reference-semantics/semantics/sort.k:49` — **opaque-symbol syntax**; attributes: `function, total, symbol(sortKeyVS), no-evaluators` — `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`

788. `reference-semantics/semantics/sort.k:51` — **function syntax**; attributes: `function, total, function, total` — `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`

789. `reference-semantics/semantics/sort.k:53` — **ordinary rule**; attributes: `none` — `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`

790. `reference-semantics/semantics/sort.k:54` — **ordinary rule**; attributes: `none` — `rule revVSAcc(.ValSeq, A:ValSeq) => A`

791. `reference-semantics/semantics/sort.k:55` — **ordinary rule**; attributes: `none` — `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`

792. `reference-semantics/semantics/sort.k:57` — **function syntax**; attributes: `function, total` — `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`

793. `reference-semantics/semantics/sort.k:58` — **ordinary rule**; attributes: `none` — `rule condRev(S:ValSeq, false) => S`

794. `reference-semantics/semantics/sort.k:59` — **ordinary rule**; attributes: `none` — `rule condRev(S:ValSeq, true)  => revVS(S)`

795. `reference-semantics/semantics/sort.k:61` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`

796. `reference-semantics/semantics/sort.k:63` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`

797. `reference-semantics/semantics/sort.k:65` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>`

## `reference-semantics/semantics/str.k`

798. `reference-semantics/semantics/str.k:8` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>`

799. `reference-semantics/semantics/str.k:9` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>`

800. `reference-semantics/semantics/str.k:13` — **function syntax**; attributes: `function` — `syntax IntSeq ::= strToCodes(String) [function]`

801. `reference-semantics/semantics/str.k:14` — **ordinary rule**; attributes: `none` — `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`

802. `reference-semantics/semantics/str.k:15` — **ordinary rule**; attributes: `none` — `rule strToCodes("") => .IntSeq`

803. `reference-semantics/semantics/str.k:16` — **ordinary rule**; attributes: `none` — `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128`

804. `reference-semantics/semantics/str.k:20` — **function syntax**; attributes: `function, total` — `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`

805. `reference-semantics/semantics/str.k:21` — **ordinary rule**; attributes: `none` — `rule seqConcat(.IntSeq, T:IntSeq)                => T`

806. `reference-semantics/semantics/str.k:22` — **ordinary rule**; attributes: `none` — `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`

807. `reference-semantics/semantics/str.k:24` — **ordinary rule**; attributes: `none` — `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`

808. `reference-semantics/semantics/str.k:25` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`

809. `reference-semantics/semantics/str.k:26` — **ordinary rule**; attributes: `none` — `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)`

810. `reference-semantics/semantics/str.k:29` — **ordinary rule**; attributes: `none` — `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`

811. `reference-semantics/semantics/str.k:30` — **ordinary rule**; attributes: `none` — `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`

812. `reference-semantics/semantics/str.k:32` — **function syntax**; attributes: `function, total` — `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`

813. `reference-semantics/semantics/str.k:33` — **ordinary rule**; attributes: `none` — `rule strPrefix(.IntSeq, _:IntSeq)               => true`

814. `reference-semantics/semantics/str.k:34` — **ordinary rule**; attributes: `none` — `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`

815. `reference-semantics/semantics/str.k:35` — **ordinary rule**; attributes: `none` — `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`

816. `reference-semantics/semantics/str.k:37` — **function syntax**; attributes: `function, total` — `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`

817. `reference-semantics/semantics/str.k:38` — **ordinary rule**; attributes: `none` — `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)`

818. `reference-semantics/semantics/str.k:39` — **ordinary rule**; attributes: `none` — `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)`

819. `reference-semantics/semantics/str.k:40` — **ordinary rule**; attributes: `none` — `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))`

820. `reference-semantics/semantics/str.k:48` — **function syntax**; attributes: `function, total` — `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`

821. `reference-semantics/semantics/str.k:49` — **ordinary rule**; attributes: `none` — `rule strLt(.IntSeq, .IntSeq)                => false`

822. `reference-semantics/semantics/str.k:50` — **ordinary rule**; attributes: `none` — `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`

823. `reference-semantics/semantics/str.k:51` — **ordinary rule**; attributes: `none` — `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`

824. `reference-semantics/semantics/str.k:52` — **ordinary rule**; attributes: `none` — `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B`

825. `reference-semantics/semantics/str.k:53` — **ordinary rule**; attributes: `none` — `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B`

826. `reference-semantics/semantics/str.k:54` — **ordinary rule**; attributes: `none` — `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`

827. `reference-semantics/semantics/str.k:56` — **ordinary rule**; attributes: `none` — `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`

828. `reference-semantics/semantics/str.k:57` — **ordinary rule**; attributes: `none` — `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`

829. `reference-semantics/semantics/str.k:58` — **ordinary rule**; attributes: `none` — `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`

830. `reference-semantics/semantics/str.k:59` — **ordinary rule**; attributes: `none` — `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`

## `reference-semantics/semantics/subscript.k`

831. `reference-semantics/semantics/subscript.k:11` — **function syntax**; attributes: `function, total` — `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`

832. `reference-semantics/semantics/subscript.k:12` — **ordinary rule**; attributes: `none` — `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V`

833. `reference-semantics/semantics/subscript.k:13` — **ordinary rule**; attributes: `none` — `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0`

834. `reference-semantics/semantics/subscript.k:16` — **function syntax**; attributes: `function` — `syntax Int ::= intSeqAt(IntSeq, Int) [function]`

835. `reference-semantics/semantics/subscript.k:17` — **ordinary rule**; attributes: `none` — `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C`

836. `reference-semantics/semantics/subscript.k:18` — **ordinary rule**; attributes: `none` — `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0`

837. `reference-semantics/semantics/subscript.k:21` — **function syntax**; attributes: `function, total` — `syntax Int ::= normIdx(Int, Int) [function, total]`

838. `reference-semantics/semantics/subscript.k:22` — **ordinary rule**; attributes: `none` — `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0`

839. `reference-semantics/semantics/subscript.k:23` — **ordinary rule**; attributes: `none` — `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0`

840. `reference-semantics/semantics/subscript.k:27` — **context**; attributes: `none` — `context Subscript(HOLE, _)`

841. `reference-semantics/semantics/subscript.k:28` — **context**; attributes: `none` — `context Subscript(_:Val, HOLE:Expr)`

842. `reference-semantics/semantics/subscript.k:31` — **priority rule**; attributes: `priority(40)` — `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

843. `reference-semantics/semantics/subscript.k:35` — **ordinary rule**; attributes: `none` — `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`

844. `reference-semantics/semantics/subscript.k:37` — **function syntax**; attributes: `function` — `syntax Val ::= applyIndex(Val, Int) [function]`

845. `reference-semantics/semantics/subscript.k:38` — **ordinary rule**; attributes: `none` — `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`

846. `reference-semantics/semantics/subscript.k:39` — **ordinary rule**; attributes: `none` — `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`

847. `reference-semantics/semantics/subscript.k:40` — **ordinary rule**; attributes: `none` — `rule applyIndex(str(IS:IntSeq),   I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))`

848. `reference-semantics/semantics/subscript.k:44` — **syntax**; attributes: `none` — `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`

849. `reference-semantics/semantics/subscript.k:49` — **syntax**; attributes: `none` — `syntax OptInt ::= "noB" | someB(Int)`

850. `reference-semantics/semantics/subscript.k:50` — **ordinary rule**; attributes: `none` — `rule <k> #evalB(NoBound)  => noB ... </k>`

851. `reference-semantics/semantics/subscript.k:51` — **ordinary rule**; attributes: `none` — `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>`

852. `reference-semantics/semantics/subscript.k:52` — **ordinary rule**; attributes: `none` — `rule <k> I:Int ~> #toSome => someB(I) ... </k>`

853. `reference-semantics/semantics/subscript.k:54` — **ordinary rule**; attributes: `none` — `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`

854. `reference-semantics/semantics/subscript.k:55` — **ordinary rule**; attributes: `none` — `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`

855. `reference-semantics/semantics/subscript.k:56` — **ordinary rule**; attributes: `none` — `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>`

856. `reference-semantics/semantics/subscript.k:58` — **priority rule**; attributes: `priority(45)` — `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`

857. `reference-semantics/semantics/subscript.k:61` — **ordinary rule**; attributes: `none` — `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`

858. `reference-semantics/semantics/subscript.k:63` — **function syntax**; attributes: `function` — `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`

859. `reference-semantics/semantics/subscript.k:64` — **ordinary rule**; attributes: `none` — `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`

860. `reference-semantics/semantics/subscript.k:66` — **ordinary rule**; attributes: `none` — `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`

861. `reference-semantics/semantics/subscript.k:68` — **ordinary rule**; attributes: `none` — `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))`

862. `reference-semantics/semantics/subscript.k:72` — **function syntax**; attributes: `function, total` — `syntax Int ::= slStep(OptInt) [function, total]`

863. `reference-semantics/semantics/subscript.k:73` — **ordinary rule**; attributes: `none` — `rule slStep(noB)          => 1`

864. `reference-semantics/semantics/subscript.k:74` — **ordinary rule**; attributes: `none` — `rule slStep(someB(S:Int)) => S`

865. `reference-semantics/semantics/subscript.k:76` — **function syntax**; attributes: `function` — `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`

866. `reference-semantics/semantics/subscript.k:77` — **ordinary rule**; attributes: `none` — `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0`

867. `reference-semantics/semantics/subscript.k:79` — **ordinary rule**; attributes: `none` — `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1 requires slStep(ST) <Int 0`

868. `reference-semantics/semantics/subscript.k:81` — **ordinary rule**; attributes: `none` — `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`

869. `reference-semantics/semantics/subscript.k:83` — **function syntax**; attributes: `function` — `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`

870. `reference-semantics/semantics/subscript.k:84` — **ordinary rule**; attributes: `none` — `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN requires slStep(ST) >Int 0`

871. `reference-semantics/semantics/subscript.k:86` — **ordinary rule**; attributes: `none` — `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0`

872. `reference-semantics/semantics/subscript.k:88` — **ordinary rule**; attributes: `none` — `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))`

873. `reference-semantics/semantics/subscript.k:90` — **function syntax**; attributes: `function, total` — `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`

874. `reference-semantics/semantics/subscript.k:91` — **ordinary rule**; attributes: `none` — `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I  <Int 0`

875. `reference-semantics/semantics/subscript.k:93` — **ordinary rule**; attributes: `none` — `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0`

876. `reference-semantics/semantics/subscript.k:96` — **function syntax**; attributes: `function, total` — `syntax Int ::= clampLo(Int, Int) [function, total]`

877. `reference-semantics/semantics/subscript.k:97` — **ordinary rule**; attributes: `none` — `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0`

878. `reference-semantics/semantics/subscript.k:99` — **ordinary rule**; attributes: `none` — `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0`

879. `reference-semantics/semantics/subscript.k:102` — **function syntax**; attributes: `function, total` — `syntax Int ::= clampHi(Int, Int, Int) [function, total]`

880. `reference-semantics/semantics/subscript.k:103` — **ordinary rule**; attributes: `none` — `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I  <Int LEN`

881. `reference-semantics/semantics/subscript.k:105` — **ordinary rule**; attributes: `none` — `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN`

882. `reference-semantics/semantics/subscript.k:109` — **function syntax**; attributes: `function` — `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`

883. `reference-semantics/semantics/subscript.k:110` — **ordinary rule**; attributes: `none` — `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`

884. `reference-semantics/semantics/subscript.k:113` — **ordinary rule**; attributes: `none` — `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`

885. `reference-semantics/semantics/subscript.k:116` — **function syntax**; attributes: `function` — `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`

886. `reference-semantics/semantics/subscript.k:117` — **ordinary rule**; attributes: `none` — `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`

887. `reference-semantics/semantics/subscript.k:120` — **ordinary rule**; attributes: `none` — `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`

## `reference-semantics/semantics/syntax.k`

888. `reference-semantics/semantics/syntax.k:9` — **macro syntax**; attributes: `seqstrict(2, 3), macro, macro` — `syntax Expr ::= "Int"      "(" Int ")" | "Float"    "(" Float ")" | "Bool"     "(" Bool ")" | "Name"     "(" String ")" | "Str"      "(" String ")" | "UnaryOp"  "(" String "," Expr ")" [strict(2)] | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp"    "(" String "," Exprs ")" | "ListExpr"  "(" Exprs ")" | "DictExpr"  "(" Entries ")" | "ListComp"  "(" Expr "," CompFors ")" [macro] | "GenExp"    "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda"    "(" Params "," Expr ")" | "KwArg"     "(" String "," Expr ")" | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call"      "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare"   "(" Expr "," CmpOp ")"`

889. `reference-semantics/semantics/syntax.k:32` — **syntax**; attributes: `none` — `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"`

890. `reference-semantics/semantics/syntax.k:33` — **syntax**; attributes: `none` — `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"`

891. `reference-semantics/semantics/syntax.k:34` — **syntax**; attributes: `none` — `syntax Entries  ::= List{Entry, ","}`

892. `reference-semantics/semantics/syntax.k:35` — **syntax**; attributes: `none` — `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`

893. `reference-semantics/semantics/syntax.k:36` — **syntax**; attributes: `none` — `syntax CompFors ::= List{CompFor, ""}`

894. `reference-semantics/semantics/syntax.k:37` — **syntax**; attributes: `none` — `syntax Exprs    ::= List{Expr, ","}`

895. `reference-semantics/semantics/syntax.k:38` — **syntax**; attributes: `none` — `syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`

896. `reference-semantics/semantics/syntax.k:39` — **syntax**; attributes: `none` — `syntax Bound    ::= Expr | "NoBound"`

897. `reference-semantics/semantics/syntax.k:41` — **syntax**; attributes: `strict, strict, strict` — `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)] | "Import"    "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While"     "(" Expr "," Stmts ")" | "Break" | "Continue" | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return"    "(" Expr ")" [strict] | "Assert"    "(" Expr ")" [strict] | "Expr"      "(" Expr ")" [strict] | "FuncDef"   "(" String "," Params "," Stmts ")" | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`

898. `reference-semantics/semantics/syntax.k:56` — **syntax**; attributes: `none` — `syntax Stmts      ::= List{Stmt, ""}`

899. `reference-semantics/semantics/syntax.k:57` — **syntax**; attributes: `none` — `syntax Params     ::= "Params" "(" ParamNames ")"`

900. `reference-semantics/semantics/syntax.k:58` — **syntax**; attributes: `none` — `syntax CellVars   ::= "CellVars" "(" ParamNames ")"`

901. `reference-semantics/semantics/syntax.k:59` — **syntax**; attributes: `none` — `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"`

902. `reference-semantics/semantics/syntax.k:60` — **syntax**; attributes: `none` — `syntax ParamNames ::= List{String, ","}`

903. `reference-semantics/semantics/syntax.k:61` — **syntax**; attributes: `none` — `syntax Module     ::= "Module" "(" Stmts ")"`

## `reference-semantics/semantics/tuple.k`

904. `reference-semantics/semantics/tuple.k:10` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>`

905. `reference-semantics/semantics/tuple.k:11` — **ordinary rule**; attributes: `none` — `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>`

906. `reference-semantics/semantics/tuple.k:14` — **syntax**; attributes: `none` — `syntax ApplyK ::= "toTuple"`

907. `reference-semantics/semantics/tuple.k:15` — **ordinary rule**; attributes: `none` — `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`

908. `reference-semantics/semantics/tuple.k:16` — **ordinary rule**; attributes: `none` — `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`

909. `reference-semantics/semantics/tuple.k:18` — **ordinary rule**; attributes: `none` — `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B`

910. `reference-semantics/semantics/tuple.k:20` — **ordinary rule**; attributes: `none` — `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`

911. `reference-semantics/semantics/tuple.k:21` — **ordinary rule**; attributes: `none` — `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>`

912. `reference-semantics/semantics/tuple.k:23` — **ordinary rule**; attributes: `none` — `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`

913. `reference-semantics/semantics/tuple.k:24` — **function syntax**; attributes: `function` — `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`

914. `reference-semantics/semantics/tuple.k:25` — **ordinary rule**; attributes: `none` — `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`

915. `reference-semantics/semantics/tuple.k:26` — **ordinary rule**; attributes: `none` — `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)`

916. `reference-semantics/semantics/tuple.k:28` — **ordinary rule**; attributes: `none` — `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)`

917. `reference-semantics/semantics/tuple.k:31` — **syntax**; attributes: `none` — `syntax KItem ::= #bindTgt(Expr, Val)`

918. `reference-semantics/semantics/tuple.k:32` — **ordinary rule**; attributes: `none` — `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`

919. `reference-semantics/semantics/tuple.k:35` — **priority rule**; attributes: `priority(40)` — `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`

920. `reference-semantics/semantics/tuple.k:42` — **ordinary rule**; attributes: `none` — `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`

921. `reference-semantics/semantics/tuple.k:43` — **ordinary rule**; attributes: `none` — `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`

922. `reference-semantics/semantics/tuple.k:44` — **priority rule**; attributes: `priority(40)` — `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

923. `reference-semantics/semantics/tuple.k:49` — **syntax**; attributes: `none` — `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`

924. `reference-semantics/semantics/tuple.k:50` — **ordinary rule**; attributes: `none` — `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`

925. `reference-semantics/semantics/tuple.k:51` — **ordinary rule**; attributes: `none` — `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>`

926. `reference-semantics/semantics/tuple.k:52` — **priority rule**; attributes: `priority(40)` — `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

927. `reference-semantics/semantics/tuple.k:55` — **ordinary rule**; attributes: `none` — `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`

928. `reference-semantics/semantics/tuple.k:57` — **ordinary rule**; attributes: `none` — `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`

## `verification.k`

929. `verification.k:9` — **macro syntax**; attributes: `macro` — `syntax Stmt ::= "GcdDef" [macro]`

930. `verification.k:10` — **macro syntax**; attributes: `macro` — `syntax Stmts ::= "GcdBody" [macro]`

931. `verification.k:11` — **macro syntax**; attributes: `macro` — `syntax Expr ::= "GcdCondition" [macro]`

932. `verification.k:12` — **macro syntax**; attributes: `macro` — `syntax Stmts ::= "GcdLoopBody" [macro]`

933. `verification.k:14` — **ordinary rule**; attributes: `none` — `rule GcdDef => FuncDef("greatest_common_divisor", Params("a", "b"), GcdBody)`

934. `verification.k:17` — **ordinary rule**; attributes: `none` — `rule GcdCondition => Compare(Name("b"), CmpOp("!=", Int(0)))`

935. `verification.k:20` — **ordinary rule**; attributes: `none` — `rule GcdLoopBody => Assign(TupleExpr((Name("a"), Name("b"), .Exprs)), TupleExpr((Name("b"), BinOp("%", Name("a"), Name("b")), .Exprs))) .Stmts`

936. `verification.k:26` — **ordinary rule**; attributes: `none` — `rule GcdBody => Assign(Name("a"), Call(Name("abs"), (Name("a"), .Exprs))) Assign(Name("b"), Call(Name("abs"), (Name("b"), .Exprs))) While(GcdCondition, GcdLoopBody) Return(Name("a")) .Stmts`

937. `verification.k:33` — **macro syntax**; attributes: `macro` — `syntax Val ::= "GcdClosure" [macro]`

938. `verification.k:34` — **ordinary rule**; attributes: `none` — `rule GcdClosure => closureVal(("a", "b", .ParamNames), GcdBody, 0)`

939. `verification.k:39` — **opaque-symbol syntax**; attributes: `function, symbol(gcdSpec), no-evaluators` — `syntax Int ::= gcdSpec(Int, Int) [function, symbol(gcdSpec), no-evaluators]`

940. `verification.k:41` — **concrete rule**; attributes: `concrete` — `rule gcdSpec(A:Int, 0) => A requires A >=Int 0 [concrete]`

941. `verification.k:44` — **concrete rule**; attributes: `concrete` — `rule gcdSpec(A:Int, B:Int) => gcdSpec(B, pyMod(A, B)) requires A >=Int 0 andBool B >Int 0 [concrete]`

942. `verification.k:51` — **priority rule**; attributes: `priority(40), symbolic(A, B)` — `rule <k> #while(GcdCondition, GcdLoopBody) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(("a" |-> (A:Int => gcdSpec(A, B)) "b" |-> (B:Int => 0)), P:Parent) ... </scopes> requires A >=Int 0 andBool B >=Int 0 [priority(40), symbolic(A, B)]`

## `spec.k`

943. `spec.k:9` — **claim**; attributes: `label(euclid-step)` — `claim <k> GcdLoopBody => .K </k> <env> L:Int </env> <scopes> SC:Map L |-> scope(("a" |-> A:Int "b" |-> B:Int), P:Parent) => SC L |-> scope(("a" |-> B "b" |-> pyMod(A, B)), P) </scopes> <heap> .Map </heap> requires A >=Int 0 andBool B >Int 0 [label(euclid-step)]`

944. `spec.k:28` — **claim**; attributes: `label(program-correct)` — `claim <k> #loadAll(Module(GcdDef .Stmts)) ~> Call(Name("greatest_common_divisor"), (A0:Int, B0:Int, .Exprs)) => gcdSpec(absInt(A0), absInt(B0)) </k> <env> 0 </env> <scopes> (0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope) => (0 |-> scope("greatest_common_divisor" |-> GcdClosure, parent(-1)) -1 |-> builtinsScope) </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <stack> .List </stack> <ret> noRet </ret> [label(program-correct)]`

945. `spec.k:53` — **claim**; attributes: `label(example-3-5)` — `claim <k> #loadAll(Module(GcdDef .Stmts)) ~> Call(Name("greatest_common_divisor"), (3, 5, .Exprs)) => 1 </k> <env> 0 </env> <scopes> (0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope) => (0 |-> scope("greatest_common_divisor" |-> GcdClosure, parent(-1)) -1 |-> builtinsScope) </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <stack> .List </stack> <ret> noRet </ret> [label(example-3-5)]`

946. `spec.k:74` — **claim**; attributes: `label(example-25-15)` — `claim <k> #loadAll(Module(GcdDef .Stmts)) ~> Call(Name("greatest_common_divisor"), (25, 15, .Exprs)) => 5 </k> <env> 0 </env> <scopes> (0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope) => (0 |-> scope("greatest_common_divisor" |-> GcdClosure, parent(-1)) -1 |-> builtinsScope) </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <stack> .List </stack> <ret> noRet </ret> [label(example-25-15)]`


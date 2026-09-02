# Exhaustive K declaration and rule inventory

Generated mechanically from the fresh scratch source copy. Each entry records the full declaration/rule text compacted to one line; source files and line numbers are authoritative.

- Files inventoried: 25
- Total entries: 962
- Kinds: {'configuration': 1, 'context': 5, 'rule': 715, 'syntax': 241}
- Class tags: {'configuration': 1, 'context': 5, 'function': 155, 'macro': 7, 'no-evaluators': 25, 'opaque-symbol': 25, 'ordinary-rule': 712, 'owise': 26, 'priority': 29, 'simplification-rule': 3, 'symbol': 28, 'syntax-declaration': 241, 'total': 117}

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/assert.k

1. L6 · `MPY-ASSERT` · **ordinary-rule** — `rule <k> Assert(V:Val) => .K ... </k>`
2. L8 · `MPY-ASSERT` · **ordinary-rule** — `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code>`
3. L13 · `MPY-ASSERT` · **ordinary-rule, priority** — `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/bool.k

1. L8 · `MPY-BOOL` · **ordinary-rule** — `rule applyUn("not", V:Val) => notBool truthy(V)`
2. L10 · `MPY-BOOL` · **ordinary-rule** — `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`
3. L11 · `MPY-BOOL` · **ordinary-rule** — `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2`
4. L16 · `MPY-BOOL` · **context** — `context BoolOp(_, (HOLE:Expr, _:Exprs))`
5. L17 · `MPY-BOOL` · **ordinary-rule** — `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`
6. L18 · `MPY-BOOL` · **ordinary-rule** — `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>`
7. L20 · `MPY-BOOL` · **ordinary-rule** — `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>`
8. L22 · `MPY-BOOL` · **ordinary-rule** — `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k>`
9. L24 · `MPY-BOOL` · **ordinary-rule** — `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>`
10. L29 · `MPY-BOOL` · **ordinary-rule, priority** — `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`
11. L31 · `MPY-BOOL` · **ordinary-rule** — `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`
12. L35 · `MPY-BOOL` · **ordinary-rule** — `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap>`
13. L39 · `MPY-BOOL` · **ordinary-rule** — `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap>`
14. L43 · `MPY-BOOL` · **ordinary-rule** — `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/builtins.k

1. L17 · `MPY-BUILTINS` · **syntax-declaration, function** — `syntax Val ::= applyBuiltin(String, Vals) [function]`
2. L20 · `MPY-BUILTINS` · **syntax-declaration, function** — `syntax Int ::= seqLen(Val) [function]`
3. L21 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`
4. L22 · `MPY-BUILTINS` · **ordinary-rule** — `rule seqLen(list(VS:ValSeq)) => vsLen(VS)`
5. L23 · `MPY-BUILTINS` · **ordinary-rule** — `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)`
6. L24 · `MPY-BUILTINS` · **ordinary-rule** — `rule seqLen(str(IS:IntSeq)) => isLen(IS)`
7. L25 · `MPY-BUILTINS` · **ordinary-rule** — `rule seqLen(setV(DS:IntSeq)) => isLen(DS)`
8. L26 · `MPY-BUILTINS` · **ordinary-rule** — `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)`
9. L32 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`
10. L33 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`
11. L34 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>`
12. L35 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>`
13. L36 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax ValSeq ::= charsOf(IntSeq) [function, total]`
14. L37 · `MPY-BUILTINS` · **ordinary-rule** — `rule charsOf(.IntSeq) => .ValSeq`
15. L38 · `MPY-BUILTINS` · **ordinary-rule** — `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))`
16. L41 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))`
17. L44 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)`
18. L47 · `MPY-BUILTINS` · **syntax-declaration** — `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`
19. L48 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`
20. L49 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`
21. L50 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k>`
22. L54 · `MPY-BUILTINS` · **syntax-declaration, function** — `syntax Int ::= intOf(Val) [function]`
23. L55 · `MPY-BUILTINS` · **ordinary-rule** — `rule intOf(I:Int) => I`
24. L56 · `MPY-BUILTINS` · **ordinary-rule** — `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi`
25. L59 · `MPY-BUILTINS` · **syntax-declaration** — `syntax KItem ::= #allAcc(Iterable) | "#allCont"`
26. L60 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`
27. L61 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterDone ~> #allCont => true ... </k>`
28. L62 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>`
29. L64 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>`
30. L67 · `MPY-BUILTINS` · **syntax-declaration** — `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`
31. L68 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`
32. L69 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterDone ~> #anyCont => false ... </k>`
33. L70 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>`
34. L72 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>`
35. L76 · `MPY-BUILTINS` · **syntax-declaration** — `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`
36. L77 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`
37. L78 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>`
38. L80 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`
39. L81 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`
40. L82 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>`
41. L86 · `MPY-BUILTINS` · **syntax-declaration** — `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`
42. L87 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`
43. L88 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>`
44. L90 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`
45. L91 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`
46. L92 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k>`
47. L97 · `MPY-BUILTINS` · **syntax-declaration, function** — `syntax Int ::= maxVals(Int, Vals) [function]`
48. L98 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`
49. L99 · `MPY-BUILTINS` · **ordinary-rule** — `rule maxVals(M:Int, .Vals) => M`
50. L100 · `MPY-BUILTINS` · **ordinary-rule** — `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`
51. L102 · `MPY-BUILTINS` · **syntax-declaration, function** — `syntax Int ::= minVals(Int, Vals) [function]`
52. L103 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`
53. L104 · `MPY-BUILTINS` · **ordinary-rule** — `rule minVals(M:Int, .Vals) => M`
54. L105 · `MPY-BUILTINS` · **ordinary-rule** — `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)`
55. L108 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))`
56. L111 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))`
57. L114 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax IntSeq ::= binCodes(Int) [function, total]`
58. L115 · `MPY-BUILTINS` · **ordinary-rule** — `rule binCodes(0) => iCons(48, .IntSeq)`
59. L116 · `MPY-BUILTINS` · **ordinary-rule** — `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`
60. L117 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`
61. L118 · `MPY-BUILTINS` · **ordinary-rule** — `rule binAcc(0, ACC:IntSeq) => ACC`
62. L119 · `MPY-BUILTINS` · **ordinary-rule** — `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))`
63. L124 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`
64. L126 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`
65. L127 · `MPY-BUILTINS` · **ordinary-rule** — `rule enumVS(.ValSeq, _:Int) => .ValSeq`
66. L128 · `MPY-BUILTINS` · **ordinary-rule** — `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))`
67. L132 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`
68. L134 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`
69. L135 · `MPY-BUILTINS` · **ordinary-rule** — `rule mapStrVS(.ValSeq) => .ValSeq`
70. L136 · `MPY-BUILTINS` · **ordinary-rule** — `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`
71. L137 · `MPY-BUILTINS` · **ordinary-rule** — `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))`
72. L140 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("int", I:Int, .Vals) => I`
73. L143 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`
74. L144 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))`
75. L148 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))`
76. L149 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)`
77. L152 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48`
78. L156 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)`
79. L158 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`
80. L159 · `MPY-BUILTINS` · **ordinary-rule** — `rule intDigAcc(.IntSeq, ACC:Int) => ACC`
81. L160 · `MPY-BUILTINS` · **ordinary-rule** — `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))`
82. L163 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`
83. L164 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B)`
84. L167 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`
85. L169 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>`
86. L170 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`
87. L171 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`
88. L173 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>`
89. L174 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>`
90. L177 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)`
91. L178 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)`
92. L179 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)`
93. L187 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`
94. L188 · `MPY-BUILTINS` · **syntax-declaration, function** — `syntax Int ::= evalArith(IntSeq) [function]`
95. L189 · `MPY-BUILTINS` · **ordinary-rule** — `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`
96. L192 · `MPY-BUILTINS` · **syntax-declaration** — `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`
97. L194 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax Bool ::= evDigit(Int) [function, total]`
98. L195 · `MPY-BUILTINS` · **ordinary-rule** — `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`
99. L196 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax Bool ::= evHead42(IntSeq) [function, total]`
100. L197 · `MPY-BUILTINS` · **ordinary-rule** — `rule evHead42(iCons(42, _:IntSeq)) => true`
101. L198 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule evHead42(_:IntSeq) => false [owise]`
102. L199 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax Bool ::= evHead47(IntSeq) [function, total]`
103. L200 · `MPY-BUILTINS` · **ordinary-rule** — `rule evHead47(iCons(47, _:IntSeq)) => true`
104. L201 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule evHead47(_:IntSeq) => false [owise]`
105. L203 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax OpSeq ::= tokOps(IntSeq) [function, total]`
106. L204 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokOps(.IntSeq) => .OpSeq`
107. L205 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)`
108. L206 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)`
109. L207 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`
110. L208 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)`
111. L209 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("`
112. L210 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)`
113. L211 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))`
114. L212 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))`
115. L214 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`
116. L216 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokNds(.IntSeq) => .IntSeq`
117. L217 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)`
118. L218 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`
119. L219 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)`
120. L221 · `MPY-BUILTINS` · **ordinary-rule** — `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)`
121. L223 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`
122. L225 · `MPY-BUILTINS` · **syntax-declaration** — `syntax EvPair ::= evp(OpSeq, IntSeq)`
123. L226 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax Int ::= firstNdE(EvPair) [function, total]`
124. L227 · `MPY-BUILTINS` · **ordinary-rule** — `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`
125. L228 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule firstNdE(_:EvPair) => 0 [owise]`
126. L230 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax Int ::= applyOpE(String, Int, Int) [function, total]`
127. L231 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyOpE("+", A:Int, B:Int) => A +Int B`
128. L232 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyOpE("-", A:Int, B:Int) => A -Int B`
129. L233 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyOpE("*", A:Int, B:Int) => A *Int B`
130. L234 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyOpE("`
131. L235 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyOpE("**", A:Int, B:Int) => A ^Int B`
132. L236 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`
133. L238 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`
134. L239 · `MPY-BUILTINS` · **ordinary-rule** — `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`
135. L240 · `MPY-BUILTINS` · **ordinary-rule** — `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`
136. L241 · `MPY-BUILTINS` · **ordinary-rule** — `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))`
137. L243 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`
138. L244 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`
139. L245 · `MPY-BUILTINS` · **ordinary-rule** — `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`
140. L246 · `MPY-BUILTINS` · **ordinary-rule** — `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`
141. L247 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`
142. L248 · `MPY-BUILTINS` · **ordinary-rule** — `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`
143. L250 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`
144. L251 · `MPY-BUILTINS` · **ordinary-rule** — `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`
145. L252 · `MPY-BUILTINS` · **ordinary-rule** — `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
146. L253 · `MPY-BUILTINS` · **ordinary-rule** — `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`
147. L254 · `MPY-BUILTINS` · **ordinary-rule** — `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
148. L255 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`
149. L256 · `MPY-BUILTINS` · **ordinary-rule** — `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`
150. L257 · `MPY-BUILTINS` · **ordinary-rule** — `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)`
151. L260 · `MPY-BUILTINS` · **ordinary-rule** — `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))`
152. L263 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`
153. L265 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax Bool ::= inLevelE(String, String) [function, total]`
154. L266 · `MPY-BUILTINS` · **ordinary-rule** — `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "`
155. L267 · `MPY-BUILTINS` · **ordinary-rule** — `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`
156. L268 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule inLevelE(_:String, _:String) => false [owise]`
157. L269 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`
158. L270 · `MPY-BUILTINS` · **ordinary-rule** — `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`
159. L271 · `MPY-BUILTINS` · **ordinary-rule** — `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`
160. L272 · `MPY-BUILTINS` · **syntax-declaration, function, total** — `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`
161. L273 · `MPY-BUILTINS` · **ordinary-rule** — `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`
162. L274 · `MPY-BUILTINS` · **ordinary-rule** — `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))`
163. L279 · `MPY-BUILTINS` · **syntax-declaration** — `syntax KItem ::= "#md5"`
164. L280 · `MPY-BUILTINS` · **ordinary-rule, priority** — `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`
165. L282 · `MPY-BUILTINS` · **ordinary-rule** — `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`
166. L283 · `MPY-BUILTINS` · **syntax-declaration** — `syntax Val ::= md5Obj(IntSeq)`
167. L284 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`
168. L285 · `MPY-BUILTINS` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`
169. L291 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`
170. L292 · `MPY-BUILTINS` · **ordinary-rule** — `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`
171. L293 · `MPY-BUILTINS` · **syntax-declaration, function** — `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`
172. L294 · `MPY-BUILTINS` · **ordinary-rule** — `rule isIntV(_:Int) => true`
173. L295 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule isIntV(_:Val) => false [owise]`
174. L296 · `MPY-BUILTINS` · **ordinary-rule** — `rule isStrV(str(_:IntSeq)) => true`
175. L297 · `MPY-BUILTINS` · **ordinary-rule, owise** — `rule isStrV(_:Val) => false [owise]`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/call.k

1. L16 · `MPY-CALL` · **ordinary-rule** — `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>`
2. L19 · `MPY-CALL` · **syntax-declaration** — `syntax KItem ::= #callee(Exprs)`
3. L20 · `MPY-CALL` · **ordinary-rule, owise** — `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`
4. L21 · `MPY-CALL` · **ordinary-rule** — `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>`
5. L24 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`
6. L26 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`
7. L27 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>`
8. L28 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>`
9. L29 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>`
10. L30 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>`
11. L31 · `MPY-CALL` · **ordinary-rule, owise** — `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`
12. L32 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k>`
13. L38 · `MPY-CALL` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
14. L42 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`
15. L47 · `MPY-CALL` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
16. L52 · `MPY-CALL` · **syntax-declaration, function, total** — `syntax Bool ::= isMutMethod(String) [function, total]`
17. L53 · `MPY-CALL` · **ordinary-rule** — `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`
18. L56 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap>`
19. L63 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap>`
20. L69 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
21. L80 · `MPY-CALL` · **ordinary-rule** — `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
22. L87 · `MPY-CALL` · **syntax-declaration** — `syntax KItem ::= #allocCells(ParamNames)`
23. L88 · `MPY-CALL` · **ordinary-rule** — `rule <k> #allocCells(.ParamNames) => .K ... </k>`
24. L89 · `MPY-CALL` · **ordinary-rule** — `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc>`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/comprehension.k

1. L11 · `MPY-COMPREHENSION` · **ordinary-rule** — `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
2. L12 · `MPY-COMPREHENSION` · **ordinary-rule** — `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
3. L14 · `MPY-COMPREHENSION` · **syntax-declaration, macro** — `syntax Stmts ::= compBody(CompFors, Expr) [macro]`
4. L15 · `MPY-COMPREHENSION` · **ordinary-rule** — `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`
5. L18 · `MPY-COMPREHENSION` · **syntax-declaration, macro** — `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`
6. L19 · `MPY-COMPREHENSION` · **ordinary-rule** — `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`
7. L21 · `MPY-COMPREHENSION` · **ordinary-rule** — `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`
8. L24 · `MPY-COMPREHENSION` · **syntax-declaration, macro** — `syntax Expr ::= compGuard(Exprs) [macro]`
9. L25 · `MPY-COMPREHENSION` · **ordinary-rule** — `rule compGuard(.Exprs) => Bool(true)`
10. L26 · `MPY-COMPREHENSION` · **ordinary-rule** — `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/concrete.k

1. L13 · `MPY-CONCRETE` · **ordinary-rule** — `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap>`
2. L16 · `MPY-CONCRETE` · **ordinary-rule** — `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap>`
3. L25 · `MPY-CONCRETE` · **syntax-declaration** — `syntax Val ::= kvP(Val, Val)`
4. L26 · `MPY-CONCRETE` · **syntax-declaration** — `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`
5. L28 · `MPY-CONCRETE` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`
6. L31 · `MPY-CONCRETE` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`
7. L34 · `MPY-CONCRETE` · **ordinary-rule** — `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`
8. L36 · `MPY-CONCRETE` · **ordinary-rule** — `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`
9. L38 · `MPY-CONCRETE` · **ordinary-rule** — `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>`
10. L42 · `MPY-CONCRETE` · **syntax-declaration, function** — `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`
11. L43 · `MPY-CONCRETE` · **ordinary-rule** — `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`
12. L44 · `MPY-CONCRETE` · **ordinary-rule** — `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R))`
13. L47 · `MPY-CONCRETE` · **ordinary-rule** — `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V))`
14. L51 · `MPY-CONCRETE` · **syntax-declaration, function** — `syntax Bool ::= kLt(Val, Val) [function]`
15. L52 · `MPY-CONCRETE` · **ordinary-rule** — `rule kLt(I1:Int, I2:Int) => I1 <Int I2`
16. L53 · `MPY-CONCRETE` · **ordinary-rule** — `rule kLt(F1:Float, F2:Float) => F1 <Float F2`
17. L54 · `MPY-CONCRETE` · **ordinary-rule** — `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
18. L56 · `MPY-CONCRETE` · **syntax-declaration, function, total** — `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`
19. L57 · `MPY-CONCRETE` · **ordinary-rule** — `rule unpairVS(.ValSeq) => .ValSeq`
20. L58 · `MPY-CONCRETE` · **ordinary-rule** — `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`
21. L59 · `MPY-CONCRETE` · **ordinary-rule, owise** — `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/controls.k

1. L9 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
2. L12 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
3. L20 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>`
4. L27 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
5. L35 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`
6. L36 · `MPY-CONTROLS` · **ordinary-rule, owise** — `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`
7. L37 · `MPY-CONTROLS` · **syntax-declaration** — `syntax KItem ::= #bindImports(ParamNames)`
8. L38 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #bindImports(.ParamNames) => .K ... </k>`
9. L39 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>`
10. L43 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>`
11. L48 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> Expr(_:Val) => .K ... </k>`
12. L51 · `MPY-CONTROLS` · **syntax-declaration** — `syntax KItem ::= #branch(Bool, Stmts, Stmts)`
13. L52 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`
14. L53 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>`
15. L54 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>`
16. L57 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>`
17. L59 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>`
18. L65 · `MPY-CONTROLS` · **syntax-declaration** — `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`
19. L69 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`
20. L71 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`
21. L72 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`
22. L73 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>`
23. L77 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`
24. L78 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`
25. L79 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>`
26. L81 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>`
27. L85 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`
28. L86 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> Continue => #cont ... </k>`
29. L87 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> Break => #brk ... </k>`
30. L88 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`
31. L89 · `MPY-CONTROLS` · **ordinary-rule, owise** — `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`
32. L90 · `MPY-CONTROLS` · **ordinary-rule** — `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`
33. L91 · `MPY-CONTROLS` · **ordinary-rule, owise** — `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]`
34. L95 · `MPY-CONTROLS` · **ordinary-rule, priority** — `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
35. L98 · `MPY-CONTROLS` · **ordinary-rule, priority** — `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
36. L101 · `MPY-CONTROLS` · **ordinary-rule, priority** — `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
37. L106 · `MPY-CONTROLS` · **ordinary-rule, priority** — `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/core.k

1. L13 · `MPY-CORE` · **syntax-declaration** — `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`
2. L14 · `MPY-CORE` · **syntax-declaration** — `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`
3. L15 · `MPY-CORE` · **syntax-declaration** — `syntax Str ::= str(IntSeq)`
4. L18 · `MPY-CORE` · **syntax-declaration** — `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`
5. L25 · `MPY-CORE` · **syntax-declaration** — `syntax Val ::= Int | Bool | "noneV" | Iterable | ref(Int) | cellRef(Int) | closureVal(ParamNames, Stmts, Int) | typeV(String) | builtinV(String) | boundMethodV(Val, String)`
6. L36 · `MPY-CORE` · **syntax-declaration** — `syntax Parent ::= "root" | parent(Int)`
7. L37 · `MPY-CORE` · **syntax-declaration** — `syntax Scope ::= scope(Map, Parent)`
8. L38 · `MPY-CORE` · **syntax-declaration** — `syntax KResult ::= Val`
9. L39 · `MPY-CORE` · **syntax-declaration** — `syntax Expr ::= Val`
10. L40 · `MPY-CORE` · **syntax-declaration** — `syntax Vals ::= List{Val, ","}`
11. L41 · `MPY-CORE` · **syntax-declaration** — `syntax Exc ::= "NoExc" | "AssertionError"`
12. L42 · `MPY-CORE` · **syntax-declaration** — `syntax RetState ::= "noRet" | retV(Val)`
13. L49 · `MPY-CORE` · **configuration** — `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code>`
14. L68 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax Bool ::= isRefV(Val) [function, total]`
15. L69 · `MPY-CORE` · **ordinary-rule** — `rule isRefV(ref(_:Int)) => true`
16. L70 · `MPY-CORE` · **ordinary-rule, owise** — `rule isRefV(_:Val) => false [owise]`
17. L75 · `MPY-CORE` · **syntax-declaration** — `syntax HeapVal ::= cellV(Val)`
18. L76 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax Bool ::= isCellRef(Val) [function, total]`
19. L77 · `MPY-CORE` · **ordinary-rule** — `rule isCellRef(cellRef(_:Int)) => true`
20. L78 · `MPY-CORE` · **ordinary-rule, owise** — `rule isCellRef(_:Val) => false [owise]`
21. L85 · `MPY-CORE` · **ordinary-rule** — `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap>`
22. L95 · `MPY-CORE` · **syntax-declaration** — `syntax Val ::= kwV(String, Val)`
23. L96 · `MPY-CORE` · **syntax-declaration** — `syntax KItem ::= #kwTag(String)`
24. L97 · `MPY-CORE` · **ordinary-rule** — `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`
25. L98 · `MPY-CORE` · **ordinary-rule** — `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>`
26. L100 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax Bool ::= isKwV(Val) [function, total]`
27. L101 · `MPY-CORE` · **ordinary-rule** — `rule isKwV(kwV(_:String, _:Val)) => true`
28. L102 · `MPY-CORE` · **ordinary-rule, owise** — `rule isKwV(_:Val) => false [owise]`
29. L106 · `MPY-CORE` · **syntax-declaration** — `syntax Val ::= cellsMark(ParamNames)`
30. L107 · `MPY-CORE` · **syntax-declaration, function** — `syntax ParamNames ::= cellsOf(Val) [function]`
31. L108 · `MPY-CORE` · **ordinary-rule** — `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`
32. L109 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax Bool ::= pnMember(String, ParamNames) [function, total]`
33. L110 · `MPY-CORE` · **ordinary-rule** — `rule pnMember(_:String, .ParamNames) => false`
34. L111 · `MPY-CORE` · **ordinary-rule** — `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`
35. L113 · `MPY-CORE` · **syntax-declaration** — `syntax KItem ::= #cellW(Val, Val)`
36. L114 · `MPY-CORE` · **ordinary-rule** — `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`
37. L117 · `MPY-CORE` · **syntax-declaration** — `syntax KItem ::= #alloc(Val)`
38. L118 · `MPY-CORE` · **ordinary-rule** — `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc>`
39. L124 · `MPY-CORE` · **syntax-declaration** — `syntax KItem ::= #loadAll(Module)`
40. L125 · `MPY-CORE` · **ordinary-rule** — `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`
41. L126 · `MPY-CORE` · **ordinary-rule** — `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`
42. L127 · `MPY-CORE` · **ordinary-rule** — `rule <k> .Stmts => .K ... </k>`
43. L130 · `MPY-CORE` · **syntax-declaration** — `syntax KItem ::= #look(String, Int)`
44. L131 · `MPY-CORE` · **ordinary-rule** — `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`
45. L132 · `MPY-CORE` · **ordinary-rule** — `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>`
46. L145 · `MPY-CORE` · **ordinary-rule** — `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap>`
47. L152 · `MPY-CORE` · **ordinary-rule** — `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>`
48. L157 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax Scope ::= "builtinsScope" [function, total]`
49. L158 · `MPY-CORE` · **ordinary-rule** — `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root)`
50. L185 · `MPY-CORE` · **syntax-declaration** — `syntax ApplyK ::= toCall(Val)`
51. L186 · `MPY-CORE` · **syntax-declaration** — `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`
52. L189 · `MPY-CORE` · **ordinary-rule** — `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`
53. L190 · `MPY-CORE` · **ordinary-rule** — `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`
54. L191 · `MPY-CORE` · **ordinary-rule** — `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>`
55. L194 · `MPY-CORE` · **ordinary-rule** — `rule <k> Int(I:Int) => I ... </k>`
56. L195 · `MPY-CORE` · **ordinary-rule** — `rule <k> Bool(B:Bool) => B ... </k>`
57. L196 · `MPY-CORE` · **ordinary-rule** — `rule <k> NoneVal => noneV ... </k>`
58. L199 · `MPY-CORE` · **syntax-declaration, function** — `syntax Bool ::= truthy(Val) [function]`
59. L200 · `MPY-CORE` · **ordinary-rule** — `rule truthy(B:Bool) => B`
60. L201 · `MPY-CORE` · **ordinary-rule** — `rule truthy(noneV) => false`
61. L202 · `MPY-CORE` · **ordinary-rule** — `rule truthy(I:Int) => I =/=Int 0`
62. L203 · `MPY-CORE` · **ordinary-rule** — `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)`
63. L204 · `MPY-CORE` · **ordinary-rule** — `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)`
64. L205 · `MPY-CORE` · **ordinary-rule** — `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)`
65. L208 · `MPY-CORE` · **syntax-declaration, function** — `syntax Val ::= applyUn(String, Val) [function]`
66. L209 · `MPY-CORE` · **syntax-declaration, function** — `syntax Val ::= applyBin(String, Val, Val) [function]`
67. L210 · `MPY-CORE` · **syntax-declaration, function** — `syntax Bool ::= applyCmp(String, Val, Val) [function]`
68. L213 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax Vals ::= appendVal(Vals, Val) [function, total]`
69. L214 · `MPY-CORE` · **ordinary-rule** — `rule appendVal(.Vals, V:Val) => V , .Vals`
70. L215 · `MPY-CORE` · **ordinary-rule** — `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)`
71. L217 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`
72. L218 · `MPY-CORE` · **ordinary-rule** — `rule vals2valSeq(.Vals) => .ValSeq`
73. L219 · `MPY-CORE` · **ordinary-rule** — `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))`
74. L223 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax Int ::= vsLen(ValSeq) [function, total]`
75. L224 · `MPY-CORE` · **ordinary-rule** — `rule vsLen(.ValSeq) => 0`
76. L225 · `MPY-CORE` · **ordinary-rule** — `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`
77. L227 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax Int ::= isLen(IntSeq) [function, total]`
78. L228 · `MPY-CORE` · **ordinary-rule** — `rule isLen(.IntSeq) => 0`
79. L229 · `MPY-CORE` · **ordinary-rule** — `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)`
80. L233 · `MPY-CORE` · **syntax-declaration, function, total** — `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`
81. L234 · `MPY-CORE` · **ordinary-rule** — `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq`
82. L235 · `MPY-CORE` · **ordinary-rule** — `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)`
83. L236 · `MPY-CORE` · **ordinary-rule** — `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))`
84. L238 · `MPY-CORE` · **ordinary-rule** — `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/dict.k

1. L20 · `MPY-DICT` · **syntax-declaration** — `syntax Val ::= dictV(ValSeq, ValSeq)`
2. L23 · `MPY-DICT` · **syntax-declaration** — `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`
3. L26 · `MPY-DICT` · **ordinary-rule** — `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`
4. L27 · `MPY-DICT` · **ordinary-rule** — `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`
5. L28 · `MPY-DICT` · **ordinary-rule** — `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`
6. L30 · `MPY-DICT` · **ordinary-rule** — `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`
7. L32 · `MPY-DICT` · **ordinary-rule** — `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>`
8. L37 · `MPY-DICT` · **syntax-declaration, function, total** — `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`
9. L38 · `MPY-DICT` · **ordinary-rule** — `rule dHasKey(.ValSeq, _:Val) => false`
10. L39 · `MPY-DICT` · **ordinary-rule** — `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K`
11. L40 · `MPY-DICT` · **ordinary-rule** — `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)`
12. L43 · `MPY-DICT` · **syntax-declaration, function, total** — `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`
13. L44 · `MPY-DICT` · **ordinary-rule** — `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)`
14. L45 · `MPY-DICT` · **ordinary-rule** — `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)`
15. L49 · `MPY-DICT` · **syntax-declaration, function, total** — `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`
16. L50 · `MPY-DICT` · **ordinary-rule** — `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR)`
17. L52 · `MPY-DICT` · **ordinary-rule** — `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))`
18. L54 · `MPY-DICT` · **ordinary-rule, owise** — `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]`
19. L58 · `MPY-DICT` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]`
20. L63 · `MPY-DICT` · **ordinary-rule** — `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`
21. L64 · `MPY-DICT` · **syntax-declaration, function** — `syntax Val ::= applyIndexD(Val, Val) [function]`
22. L65 · `MPY-DICT` · **ordinary-rule, priority** — `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]`
23. L70 · `MPY-DICT` · **syntax-declaration, function** — `syntax Val ::= dictSet(Val, Val, Val) [function]`
24. L71 · `MPY-DICT` · **ordinary-rule** — `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))`
25. L76 · `MPY-DICT` · **syntax-declaration** — `syntax KItem ::= #dsetK(String, Val)`
26. L77 · `MPY-DICT` · **ordinary-rule** — `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`
27. L78 · `MPY-DICT` · **ordinary-rule** — `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>`
28. L82 · `MPY-DICT` · **ordinary-rule** — `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
29. L86 · `MPY-DICT` · **syntax-declaration** — `syntax KItem ::= #dsetV(Val, Val, Val)`
30. L87 · `MPY-DICT` · **ordinary-rule** — `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>`
31. L90 · `MPY-DICT` · **syntax-declaration, function, total** — `syntax Int ::= normIdxD(Int, Int) [function, total]`
32. L91 · `MPY-DICT` · **ordinary-rule** — `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`
33. L92 · `MPY-DICT` · **ordinary-rule** — `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0`
34. L95 · `MPY-DICT` · **ordinary-rule** — `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`
35. L97 · `MPY-DICT` · **syntax-declaration, function** — `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`
36. L98 · `MPY-DICT` · **ordinary-rule** — `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`
37. L99 · `MPY-DICT` · **ordinary-rule** — `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`
38. L101 · `MPY-DICT` · **syntax-declaration, function** — `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`
39. L102 · `MPY-DICT` · **ordinary-rule** — `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K`
40. L103 · `MPY-DICT` · **ordinary-rule** — `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/float.k

1. L20 · `MPY-FLOAT` · **syntax-declaration** — `syntax Val ::= Float`
2. L21 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> Float(F:Float) => F ... </k>`
3. L24 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`
4. L25 · `MPY-FLOAT` · **ordinary-rule** — `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`
5. L27 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)`
6. L30 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`
7. L31 · `MPY-FLOAT` · **ordinary-rule** — `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`
8. L32 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)`
9. L37 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`
10. L38 · `MPY-FLOAT` · **ordinary-rule** — `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`
11. L39 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)`
12. L43 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`
13. L44 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)`
14. L50 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`
15. L51 · `MPY-FLOAT` · **ordinary-rule** — `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`
16. L52 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`
17. L54 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`
18. L55 · `MPY-FLOAT` · **ordinary-rule** — `rule absF(F:Float) => absFloat(F) [concrete]`
19. L56 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)`
20. L61 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> Import(_:String) => .K ... </k>`
21. L65 · `MPY-FLOAT` · **syntax-declaration** — `syntax KItem ::= "#mathCeil"`
22. L66 · `MPY-FLOAT` · **ordinary-rule, priority** — `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`
23. L67 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>`
24. L70 · `MPY-FLOAT` · **syntax-declaration** — `syntax KItem ::= "#mathFloor"`
25. L71 · `MPY-FLOAT` · **ordinary-rule, priority** — `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`
26. L72 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`
27. L73 · `MPY-FLOAT` · **syntax-declaration, function, total, symbol** — `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`
28. L74 · `MPY-FLOAT` · **ordinary-rule** — `rule floorFI(I:Int) => I [concrete]`
29. L75 · `MPY-FLOAT` · **ordinary-rule** — `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]`
30. L78 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`
31. L79 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V)`
32. L82 · `MPY-FLOAT` · **syntax-declaration** — `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`
33. L83 · `MPY-FLOAT` · **ordinary-rule, priority** — `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`
34. L84 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`
35. L85 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`
36. L86 · `MPY-FLOAT` · **syntax-declaration, function, total, symbol** — `syntax Float ::= toF(Val) [function, total, symbol(toF)]`
37. L87 · `MPY-FLOAT` · **ordinary-rule** — `rule toF(F:Float) => F [concrete]`
38. L88 · `MPY-FLOAT` · **ordinary-rule** — `rule toF(I:Int) => intToF(I) [concrete]`
39. L93 · `MPY-FLOAT` · **syntax-declaration, function, total, symbol** — `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`
40. L94 · `MPY-FLOAT` · **ordinary-rule** — `rule ceilF(I:Int) => I [concrete]`
41. L95 · `MPY-FLOAT` · **ordinary-rule** — `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]`
42. L99 · `MPY-FLOAT` · **ordinary-rule** — `rule applyUn("-", F:Float) => 0.0 -Float F`
43. L103 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`
44. L104 · `MPY-FLOAT` · **ordinary-rule** — `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`
45. L105 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`
46. L107 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`
47. L108 · `MPY-FLOAT` · **ordinary-rule** — `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`
48. L109 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`
49. L111 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`
50. L112 · `MPY-FLOAT` · **ordinary-rule** — `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`
51. L113 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`
52. L115 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`
53. L116 · `MPY-FLOAT` · **ordinary-rule** — `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`
54. L117 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`
55. L119 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`
56. L120 · `MPY-FLOAT` · **ordinary-rule** — `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`
57. L121 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)`
58. L125 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`
59. L126 · `MPY-FLOAT` · **ordinary-rule** — `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`
60. L127 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)`
61. L128 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`
62. L129 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)`
63. L132 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`
64. L133 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`
65. L134 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`
66. L135 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`
67. L136 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`
68. L137 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`
69. L138 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`
70. L139 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`
71. L142 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`
72. L143 · `MPY-FLOAT` · **ordinary-rule** — `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`
73. L144 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`
74. L145 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`
75. L146 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`
76. L147 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`
77. L148 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`
78. L149 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`
79. L150 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`
80. L151 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`
81. L154 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("==", V:Val, noneV) => V ==K noneV`
82. L155 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)`
83. L160 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`
84. L161 · `MPY-FLOAT` · **ordinary-rule** — `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`
85. L162 · `MPY-FLOAT` · **ordinary-rule** — `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))`
86. L165 · `MPY-FLOAT` · **syntax-declaration, function** — `syntax Int ::= headIS(IntSeq) [function]`
87. L166 · `MPY-FLOAT` · **ordinary-rule** — `rule headIS(iCons(C:Int, _:IntSeq)) => C`
88. L167 · `MPY-FLOAT` · **syntax-declaration, function, total** — `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`
89. L168 · `MPY-FLOAT` · **ordinary-rule** — `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`
90. L169 · `MPY-FLOAT` · **ordinary-rule** — `rule intPartAcc(.IntSeq, A:Int) => A`
91. L170 · `MPY-FLOAT` · **ordinary-rule** — `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`
92. L171 · `MPY-FLOAT` · **ordinary-rule** — `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))`
93. L173 · `MPY-FLOAT` · **syntax-declaration, function, total** — `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`
94. L174 · `MPY-FLOAT` · **ordinary-rule** — `rule fracPart(.IntSeq) => 0`
95. L175 · `MPY-FLOAT` · **ordinary-rule** — `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`
96. L176 · `MPY-FLOAT` · **ordinary-rule** — `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`
97. L177 · `MPY-FLOAT` · **ordinary-rule** — `rule fracAcc(.IntSeq, A:Int) => A`
98. L178 · `MPY-FLOAT` · **ordinary-rule** — `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`
99. L179 · `MPY-FLOAT` · **syntax-declaration, function, total** — `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`
100. L180 · `MPY-FLOAT` · **ordinary-rule** — `rule fracScale(.IntSeq) => 1`
101. L181 · `MPY-FLOAT` · **ordinary-rule** — `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`
102. L182 · `MPY-FLOAT` · **ordinary-rule** — `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`
103. L183 · `MPY-FLOAT` · **ordinary-rule** — `rule fscAcc(.IntSeq, A:Int) => A`
104. L184 · `MPY-FLOAT` · **ordinary-rule** — `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`
105. L185 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`
106. L186 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`
107. L187 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("float", F:Float, .Vals) => F`
108. L190 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`
109. L191 · `MPY-FLOAT` · **ordinary-rule** — `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`
110. L192 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)`
111. L195 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`
112. L196 · `MPY-FLOAT` · **ordinary-rule** — `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`
113. L197 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`
114. L198 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`
115. L199 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`
116. L200 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`
117. L201 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`
118. L202 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`
119. L203 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`
120. L204 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`
121. L205 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`
122. L206 · `MPY-FLOAT` · **ordinary-rule** — `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`
123. L209 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`
124. L210 · `MPY-FLOAT` · **ordinary-rule** — `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`
125. L211 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`
126. L213 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`
127. L214 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("float", F:Float, .Vals) => F`
128. L217 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`
129. L218 · `MPY-FLOAT` · **ordinary-rule** — `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`
130. L223 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`
131. L224 · `MPY-FLOAT` · **ordinary-rule** — `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`
132. L227 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)`
133. L228 · `MPY-FLOAT` · **ordinary-rule** — `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`
134. L230 · `MPY-FLOAT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`
135. L231 · `MPY-FLOAT` · **ordinary-rule** — `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`
136. L232 · `MPY-FLOAT` · **syntax-declaration** — `syntax KItem ::= "#mathSqrt"`
137. L233 · `MPY-FLOAT` · **ordinary-rule, priority** — `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`
138. L234 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`
139. L235 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>`
140. L243 · `MPY-FLOAT` · **syntax-declaration** — `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`
141. L244 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
142. L245 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`
143. L246 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`
144. L247 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>`
145. L250 · `MPY-FLOAT` · **syntax-declaration** — `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`
146. L251 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
147. L252 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`
148. L253 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`
149. L254 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>`
150. L261 · `MPY-FLOAT` · **syntax-declaration** — `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`
151. L262 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>`
152. L265 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`
153. L266 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`
154. L267 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>`
155. L270 · `MPY-FLOAT` · **ordinary-rule** — `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/functions.k

1. L8 · `MPY-FUNCTIONS` · **syntax-declaration** — `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall"`
2. L14 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`
3. L18 · `MPY-FUNCTIONS` · **syntax-declaration** — `syntax Expr ::= closureExpr(ParamNames, Stmts)`
4. L19 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>`
5. L27 · `MPY-FUNCTIONS` · **syntax-declaration** — `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)`
6. L31 · `MPY-FUNCTIONS` · **syntax-declaration** — `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`
7. L33 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`
8. L36 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
9. L42 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`
10. L47 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`
11. L50 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`
12. L53 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
13. L59 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>`
14. L63 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`
15. L64 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>`
16. L68 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
17. L78 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`
18. L80 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>`
19. L85 · `MPY-FUNCTIONS` · **ordinary-rule** — `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/int.k

1. L7 · `MPY-INT` · **ordinary-rule** — `rule applyUn("-", I:Int) => 0 -Int I`
2. L9 · `MPY-INT` · **ordinary-rule** — `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2`
3. L11 · `MPY-INT` · **ordinary-rule** — `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`
4. L12 · `MPY-INT` · **ordinary-rule** — `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`
5. L13 · `MPY-INT` · **ordinary-rule** — `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2`
6. L14 · `MPY-INT` · **ordinary-rule** — `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2`
7. L15 · `MPY-INT` · **ordinary-rule** — `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)`
8. L16 · `MPY-INT` · **ordinary-rule** — `rule applyBin("`
9. L17 · `MPY-INT` · **ordinary-rule** — `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`
10. L19 · `MPY-INT` · **syntax-declaration, function** — `syntax Int ::= pyMod(Int, Int) [function]`
11. L20 · `MPY-INT` · **ordinary-rule** — `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`
12. L22 · `MPY-INT` · **ordinary-rule** — `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2`
13. L23 · `MPY-INT` · **ordinary-rule** — `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2`
14. L24 · `MPY-INT` · **ordinary-rule** — `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2`
15. L25 · `MPY-INT` · **ordinary-rule** — `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2`
16. L26 · `MPY-INT` · **ordinary-rule** — `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2`
17. L27 · `MPY-INT` · **ordinary-rule** — `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/iter.k

1. L8 · `MPY-ITER` · **syntax-declaration** — `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/list.k

1. L9 · `MPY-LIST` · **ordinary-rule** — `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>`
2. L10 · `MPY-LIST` · **ordinary-rule** — `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>`
3. L13 · `MPY-LIST` · **syntax-declaration** — `syntax ApplyK ::= "toList"`
4. L14 · `MPY-LIST` · **ordinary-rule** — `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`
5. L15 · `MPY-LIST` · **ordinary-rule** — `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>`
6. L18 · `MPY-LIST` · **syntax-declaration, function, total** — `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`
7. L19 · `MPY-LIST` · **ordinary-rule** — `rule valSeqConcat(.ValSeq, T:ValSeq) => T`
8. L20 · `MPY-LIST` · **ordinary-rule** — `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))`
9. L24 · `MPY-LIST` · **ordinary-rule, priority** — `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`
10. L27 · `MPY-LIST` · **ordinary-rule** — `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`
11. L28 · `MPY-LIST` · **ordinary-rule** — `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)`
12. L33 · `MPY-LIST` · **syntax-declaration, function, total** — `syntax Bool ::= hasRefVS(ValSeq) [function, total]`
13. L34 · `MPY-LIST` · **ordinary-rule** — `rule hasRefVS(.ValSeq) => false`
14. L35 · `MPY-LIST` · **ordinary-rule** — `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`
15. L37 · `MPY-LIST` · **syntax-declaration, function** — `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map) [function]`
16. L39 · `MPY-LIST` · **ordinary-rule** — `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true`
17. L40 · `MPY-LIST` · **ordinary-rule** — `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false`
18. L41 · `MPY-LIST` · **ordinary-rule** — `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false`
19. L42 · `MPY-LIST` · **ordinary-rule** — `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`
20. L45 · `MPY-LIST` · **ordinary-rule** — `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)`
21. L47 · `MPY-LIST` · **ordinary-rule** — `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)`
22. L49 · `MPY-LIST` · **ordinary-rule** — `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`
23. L50 · `MPY-LIST` · **ordinary-rule, owise** — `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]`
24. L53 · `MPY-LIST` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]`
25. L58 · `MPY-LIST` · **syntax-declaration** — `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`
26. L59 · `MPY-LIST` · **ordinary-rule** — `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`
27. L60 · `MPY-LIST` · **ordinary-rule** — `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`
28. L61 · `MPY-LIST` · **ordinary-rule** — `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`
29. L62 · `MPY-LIST` · **ordinary-rule** — `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`
30. L63 · `MPY-LIST` · **ordinary-rule** — `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>`
31. L65 · `MPY-LIST` · **ordinary-rule** — `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>`
32. L67 · `MPY-LIST` · **ordinary-rule** — `rule <k> B:Bool ~> #notB => notBool B ... </k>`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/methods.k

1. L10 · `MPY-METHODS` · **syntax-declaration, function** — `syntax Val ::= applyMethod(Val, String, Vals) [function]`
2. L13 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`
3. L14 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`
4. L15 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`
5. L16 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)`
6. L19 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))`
7. L20 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))`
8. L21 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))`
9. L26 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`
10. L27 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`
11. L28 · `MPY-METHODS` · **ordinary-rule** — `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`
12. L29 · `MPY-METHODS` · **ordinary-rule** — `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`
13. L30 · `MPY-METHODS` · **ordinary-rule** — `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))`
14. L34 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`
15. L35 · `MPY-METHODS` · **syntax-declaration, function** — `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`
16. L36 · `MPY-METHODS` · **ordinary-rule** — `rule cntSub(.IntSeq, _:IntSeq) => 0`
17. L37 · `MPY-METHODS` · **ordinary-rule** — `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)`
18. L39 · `MPY-METHODS` · **ordinary-rule** — `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)`
19. L41 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`
20. L42 · `MPY-METHODS` · **ordinary-rule** — `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`
21. L43 · `MPY-METHODS` · **ordinary-rule, owise** — `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`
22. L44 · `MPY-METHODS` · **ordinary-rule** — `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0`
23. L47 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`
24. L48 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax IntSeq ::= trimWS(IntSeq) [function, total]`
25. L49 · `MPY-METHODS` · **ordinary-rule** — `rule trimWS(.IntSeq) => .IntSeq`
26. L50 · `MPY-METHODS` · **ordinary-rule** — `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`
27. L51 · `MPY-METHODS` · **ordinary-rule** — `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`
28. L52 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`
29. L53 · `MPY-METHODS` · **ordinary-rule** — `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`
30. L54 · `MPY-METHODS` · **ordinary-rule** — `rule revISAcc(.IntSeq, A:IntSeq) => A`
31. L55 · `MPY-METHODS` · **ordinary-rule** — `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))`
32. L58 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)`
33. L61 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)`
34. L64 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`
35. L65 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`
36. L66 · `MPY-METHODS` · **ordinary-rule** — `rule cntOccVS(.ValSeq, _:Val) => 0`
37. L67 · `MPY-METHODS` · **ordinary-rule** — `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`
38. L68 · `MPY-METHODS` · **ordinary-rule** — `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V)`
39. L72 · `MPY-METHODS` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`
40. L75 · `MPY-METHODS` · **syntax-declaration, function** — `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]`
41. L76 · `MPY-METHODS` · **ordinary-rule** — `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`
42. L77 · `MPY-METHODS` · **ordinary-rule** — `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))`
43. L79 · `MPY-METHODS` · **ordinary-rule** — `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)`
44. L82 · `MPY-METHODS` · **syntax-declaration, function** — `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`
45. L83 · `MPY-METHODS` · **ordinary-rule** — `rule flushTok(ACC:ValSeq, .IntSeq) => ACC`
46. L84 · `MPY-METHODS` · **ordinary-rule** — `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`
47. L85 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= isWSC(Int) [function, total]`
48. L86 · `MPY-METHODS` · **ordinary-rule** — `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13`
49. L89 · `MPY-METHODS` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]`
50. L94 · `MPY-METHODS` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`
51. L97 · `MPY-METHODS` · **syntax-declaration, function** — `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]`
52. L98 · `MPY-METHODS` · **ordinary-rule** — `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)`
53. L99 · `MPY-METHODS` · **ordinary-rule** — `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))`
54. L101 · `MPY-METHODS` · **ordinary-rule** — `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))`
55. L104 · `MPY-METHODS` · **ordinary-rule** — `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`
56. L106 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`
57. L107 · `MPY-METHODS` · **ordinary-rule** — `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq`
58. L108 · `MPY-METHODS` · **ordinary-rule** — `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`
59. L109 · `MPY-METHODS` · **ordinary-rule** — `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)`
60. L112 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= isUpperC(Int) [function, total]`
61. L113 · `MPY-METHODS` · **ordinary-rule** — `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`
62. L115 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= isLowerC(Int) [function, total]`
63. L116 · `MPY-METHODS` · **ordinary-rule** — `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`
64. L118 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= isAlphaC(Int) [function, total]`
65. L119 · `MPY-METHODS` · **ordinary-rule** — `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`
66. L121 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= isDigitC(Int) [function, total]`
67. L122 · `MPY-METHODS` · **ordinary-rule** — `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`
68. L124 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= hasUpper(IntSeq) [function, total]`
69. L125 · `MPY-METHODS` · **ordinary-rule** — `rule hasUpper(.IntSeq) => false`
70. L126 · `MPY-METHODS` · **ordinary-rule** — `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`
71. L128 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= hasLower(IntSeq) [function, total]`
72. L129 · `MPY-METHODS` · **ordinary-rule** — `rule hasLower(.IntSeq) => false`
73. L130 · `MPY-METHODS` · **ordinary-rule** — `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`
74. L132 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= allAlpha(IntSeq) [function, total]`
75. L133 · `MPY-METHODS` · **ordinary-rule** — `rule allAlpha(.IntSeq) => true`
76. L134 · `MPY-METHODS` · **ordinary-rule** — `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`
77. L136 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= allDigit(IntSeq) [function, total]`
78. L137 · `MPY-METHODS` · **ordinary-rule** — `rule allDigit(.IntSeq) => true`
79. L138 · `MPY-METHODS` · **ordinary-rule** — `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`
80. L140 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Int ::= lowerC(Int) [function, total]`
81. L142 · `MPY-METHODS` · **ordinary-rule** — `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`
82. L143 · `MPY-METHODS` · **ordinary-rule, owise** — `rule lowerC(C:Int) => C [owise]`
83. L145 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Int ::= upperC(Int) [function, total]`
84. L146 · `MPY-METHODS` · **ordinary-rule** — `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`
85. L147 · `MPY-METHODS` · **ordinary-rule, owise** — `rule upperC(C:Int) => C [owise]`
86. L149 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Int ::= swapC(Int) [function, total]`
87. L150 · `MPY-METHODS` · **ordinary-rule** — `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`
88. L151 · `MPY-METHODS` · **ordinary-rule** — `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`
89. L152 · `MPY-METHODS` · **ordinary-rule, owise** — `rule swapC(C:Int) => C [owise]`
90. L154 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax IntSeq ::= mapLower(IntSeq) [function, total]`
91. L155 · `MPY-METHODS` · **ordinary-rule** — `rule mapLower(.IntSeq) => .IntSeq`
92. L156 · `MPY-METHODS` · **ordinary-rule** — `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`
93. L158 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`
94. L159 · `MPY-METHODS` · **ordinary-rule** — `rule mapUpper(.IntSeq) => .IntSeq`
95. L160 · `MPY-METHODS` · **ordinary-rule** — `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`
96. L162 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`
97. L163 · `MPY-METHODS` · **ordinary-rule** — `rule mapSwap(.IntSeq) => .IntSeq`
98. L164 · `MPY-METHODS` · **ordinary-rule** — `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`
99. L166 · `MPY-METHODS` · **syntax-declaration, function, total** — `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`
100. L167 · `MPY-METHODS` · **ordinary-rule** — `rule startsWith(.IntSeq, _:IntSeq) => true`
101. L168 · `MPY-METHODS` · **ordinary-rule** — `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`
102. L169 · `MPY-METHODS` · **ordinary-rule** — `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/operators.k

1. L10 · `MPY-OPERATORS` · **ordinary-rule** — `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`
2. L12 · `MPY-OPERATORS` · **ordinary-rule** — `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>`
3. L15 · `MPY-OPERATORS` · **context** — `context Compare(HOLE, _)`
4. L16 · `MPY-OPERATORS` · **context** — `context Compare(_:Val, CmpOp(_, HOLE))`
5. L17 · `MPY-OPERATORS` · **ordinary-rule, owise** — `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`
6. L19 · `MPY-OPERATORS` · **ordinary-rule** — `rule applyCmp("is", V:Val, noneV) => V ==K noneV`
7. L20 · `MPY-OPERATORS` · **ordinary-rule** — `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)`
8. L25 · `MPY-OPERATORS` · **ordinary-rule, priority** — `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
9. L28 · `MPY-OPERATORS` · **ordinary-rule** — `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap>`
10. L34 · `MPY-OPERATORS` · **ordinary-rule** — `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap>`
11. L38 · `MPY-OPERATORS` · **ordinary-rule** — `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap>`
12. L44 · `MPY-OPERATORS` · **ordinary-rule, priority** — `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/range.k

1. L9 · `MPY-RANGE` · **syntax-declaration, function, total** — `syntax Bool ::= inRange(Int, Int, Int) [function, total]`
2. L10 · `MPY-RANGE` · **ordinary-rule** — `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`
3. L12 · `MPY-RANGE` · **syntax-declaration, function** — `syntax Int ::= rangeLen(Int, Int, Int) [function]`
4. L13 · `MPY-RANGE` · **ordinary-rule** — `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST`
5. L15 · `MPY-RANGE` · **ordinary-rule** — `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)`
6. L17 · `MPY-RANGE` · **ordinary-rule** — `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0`
7. L20 · `MPY-RANGE` · **ordinary-rule** — `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>`
8. L23 · `MPY-RANGE` · **ordinary-rule** — `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/set.k

1. L8 · `MPY-SET` · **syntax-declaration** — `syntax Val ::= setV(IntSeq)`
2. L11 · `MPY-SET` · **syntax-declaration, function, total** — `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`
3. L12 · `MPY-SET` · **ordinary-rule** — `rule codeIn(_:Int, .IntSeq) => false`
4. L13 · `MPY-SET` · **ordinary-rule** — `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)`
5. L16 · `MPY-SET` · **syntax-declaration, function, total** — `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] | dedupFrom(IntSeq, IntSeq) [function, total]`
6. L18 · `MPY-SET` · **ordinary-rule** — `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`
7. L19 · `MPY-SET` · **ordinary-rule** — `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`
8. L20 · `MPY-SET` · **ordinary-rule** — `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)`
9. L22 · `MPY-SET` · **ordinary-rule** — `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))`
10. L25 · `MPY-SET` · **syntax-declaration, function, total** — `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`
11. L26 · `MPY-SET` · **ordinary-rule** — `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)`
12. L27 · `MPY-SET` · **ordinary-rule** — `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))`
13. L31 · `MPY-SET` · **syntax-declaration, function, total** — `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`
14. L32 · `MPY-SET` · **ordinary-rule** — `rule subsetCodes(.IntSeq, _:IntSeq) => true`
15. L33 · `MPY-SET` · **ordinary-rule** — `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`
16. L35 · `MPY-SET` · **syntax-declaration, function, total** — `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`
17. L36 · `MPY-SET` · **ordinary-rule** — `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)`
18. L39 · `MPY-SET` · **ordinary-rule** — `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/sort.k

1. L18 · `MPY-SORT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`
2. L19 · `MPY-SORT` · **syntax-declaration, function** — `syntax ValSeq ::= insVS(Int, ValSeq) [function]`
3. L20 · `MPY-SORT` · **ordinary-rule** — `rule sortVS(.ValSeq) => .ValSeq [concrete]`
4. L21 · `MPY-SORT` · **ordinary-rule** — `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`
5. L22 · `MPY-SORT` · **ordinary-rule** — `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]`
6. L23 · `MPY-SORT` · **ordinary-rule** — `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`
7. L24 · `MPY-SORT` · **ordinary-rule** — `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete]`
8. L26 · `MPY-SORT` · **syntax-declaration, function** — `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`
9. L27 · `MPY-SORT` · **ordinary-rule** — `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`
10. L28 · `MPY-SORT` · **ordinary-rule** — `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`
11. L29 · `MPY-SORT` · **ordinary-rule** — `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))`
12. L31 · `MPY-SORT` · **ordinary-rule** — `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))`
13. L36 · `MPY-SORT` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>`
14. L40 · `MPY-SORT` · **ordinary-rule, priority** — `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]`
15. L49 · `MPY-SORT` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`
16. L51 · `MPY-SORT` · **syntax-declaration, function, total** — `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`
17. L53 · `MPY-SORT` · **ordinary-rule** — `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`
18. L54 · `MPY-SORT` · **ordinary-rule** — `rule revVSAcc(.ValSeq, A:ValSeq) => A`
19. L55 · `MPY-SORT` · **ordinary-rule** — `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`
20. L57 · `MPY-SORT` · **syntax-declaration, function, total** — `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`
21. L58 · `MPY-SORT` · **ordinary-rule** — `rule condRev(S:ValSeq, false) => S`
22. L59 · `MPY-SORT` · **ordinary-rule** — `rule condRev(S:ValSeq, true) => revVS(S)`
23. L61 · `MPY-SORT` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`
24. L63 · `MPY-SORT` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`
25. L65 · `MPY-SORT` · **ordinary-rule** — `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/str.k

1. L8 · `MPY-STR` · **ordinary-rule** — `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>`
2. L9 · `MPY-STR` · **ordinary-rule** — `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>`
3. L13 · `MPY-STR` · **syntax-declaration, function** — `syntax IntSeq ::= strToCodes(String) [function]`
4. L14 · `MPY-STR` · **ordinary-rule** — `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`
5. L15 · `MPY-STR` · **ordinary-rule** — `rule strToCodes("") => .IntSeq`
6. L16 · `MPY-STR` · **ordinary-rule** — `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))`
7. L20 · `MPY-STR` · **syntax-declaration, function, total** — `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`
8. L21 · `MPY-STR` · **ordinary-rule** — `rule seqConcat(.IntSeq, T:IntSeq) => T`
9. L22 · `MPY-STR` · **ordinary-rule** — `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`
10. L24 · `MPY-STR` · **ordinary-rule** — `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`
11. L25 · `MPY-STR` · **ordinary-rule** — `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`
12. L26 · `MPY-STR` · **ordinary-rule** — `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)`
13. L29 · `MPY-STR` · **ordinary-rule** — `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`
14. L30 · `MPY-STR` · **ordinary-rule** — `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`
15. L32 · `MPY-STR` · **syntax-declaration, function, total** — `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`
16. L33 · `MPY-STR` · **ordinary-rule** — `rule strPrefix(.IntSeq, _:IntSeq) => true`
17. L34 · `MPY-STR` · **ordinary-rule** — `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`
18. L35 · `MPY-STR` · **ordinary-rule** — `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`
19. L37 · `MPY-STR` · **syntax-declaration, function, total** — `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`
20. L38 · `MPY-STR` · **ordinary-rule** — `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)`
21. L39 · `MPY-STR` · **ordinary-rule** — `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)`
22. L40 · `MPY-STR` · **ordinary-rule** — `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)`
23. L48 · `MPY-STR` · **syntax-declaration, function, total** — `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`
24. L49 · `MPY-STR` · **ordinary-rule** — `rule strLt(.IntSeq, .IntSeq) => false`
25. L50 · `MPY-STR` · **ordinary-rule** — `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`
26. L51 · `MPY-STR` · **ordinary-rule** — `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`
27. L52 · `MPY-STR` · **ordinary-rule** — `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B`
28. L53 · `MPY-STR` · **ordinary-rule** — `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B`
29. L54 · `MPY-STR` · **ordinary-rule** — `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`
30. L56 · `MPY-STR` · **ordinary-rule** — `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
31. L57 · `MPY-STR` · **ordinary-rule** — `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`
32. L58 · `MPY-STR` · **ordinary-rule** — `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`
33. L59 · `MPY-STR` · **ordinary-rule** — `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/subscript.k

1. L11 · `MPY-SUBSCRIPT` · **syntax-declaration, function, total** — `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`
2. L12 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V`
3. L13 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)`
4. L16 · `MPY-SUBSCRIPT` · **syntax-declaration, function** — `syntax Int ::= intSeqAt(IntSeq, Int) [function]`
5. L17 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C`
6. L18 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)`
7. L21 · `MPY-SUBSCRIPT` · **syntax-declaration, function, total** — `syntax Int ::= normIdx(Int, Int) [function, total]`
8. L22 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`
9. L23 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule normIdx(I:Int, _:Int) => I requires I >=Int 0`
10. L27 · `MPY-SUBSCRIPT` · **context** — `context Subscript(HOLE, _)`
11. L28 · `MPY-SUBSCRIPT` · **context** — `context Subscript(_:Val, HOLE:Expr)`
12. L31 · `MPY-SUBSCRIPT` · **ordinary-rule, priority** — `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
13. L35 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`
14. L37 · `MPY-SUBSCRIPT` · **syntax-declaration, function** — `syntax Val ::= applyIndex(Val, Int) [function]`
15. L38 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
16. L39 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
17. L40 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))`
18. L44 · `MPY-SUBSCRIPT` · **syntax-declaration** — `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`
19. L49 · `MPY-SUBSCRIPT` · **syntax-declaration** — `syntax OptInt ::= "noB" | someB(Int)`
20. L50 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule <k> #evalB(NoBound) => noB ... </k>`
21. L51 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>`
22. L52 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule <k> I:Int ~> #toSome => someB(I) ... </k>`
23. L54 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`
24. L55 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`
25. L56 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>`
26. L58 · `MPY-SUBSCRIPT` · **ordinary-rule, priority** — `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`
27. L61 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`
28. L63 · `MPY-SUBSCRIPT` · **syntax-declaration, function** — `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`
29. L64 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
30. L66 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
31. L68 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))`
32. L72 · `MPY-SUBSCRIPT` · **syntax-declaration, function, total** — `syntax Int ::= slStep(OptInt) [function, total]`
33. L73 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slStep(noB) => 1`
34. L74 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slStep(someB(S:Int)) => S`
35. L76 · `MPY-SUBSCRIPT` · **syntax-declaration, function** — `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`
36. L77 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slStart(noB, ST:OptInt, _LEN:Int) => 0`
37. L79 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1`
38. L81 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`
39. L83 · `MPY-SUBSCRIPT` · **syntax-declaration, function** — `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`
40. L84 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slStop(noB, ST:OptInt, LEN:Int) => LEN`
41. L86 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slStop(noB, ST:OptInt, _LEN:Int) => -1`
42. L88 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`
43. L90 · `MPY-SUBSCRIPT` · **syntax-declaration, function, total** — `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`
44. L91 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)`
45. L93 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)`
46. L96 · `MPY-SUBSCRIPT` · **syntax-declaration, function, total** — `syntax Int ::= clampLo(Int, Int) [function, total]`
47. L97 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule clampLo(J:Int, _STEP:Int) => J`
48. L99 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi`
49. L102 · `MPY-SUBSCRIPT` · **syntax-declaration, function, total** — `syntax Int ::= clampHi(Int, Int, Int) [function, total]`
50. L103 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I`
51. L105 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi`
52. L109 · `MPY-SUBSCRIPT` · **syntax-declaration, function** — `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`
53. L110 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))`
54. L113 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq`
55. L116 · `MPY-SUBSCRIPT` · **syntax-declaration, function** — `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`
56. L117 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))`
57. L120 · `MPY-SUBSCRIPT` · **ordinary-rule** — `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/syntax.k

1. L9 · `MPY-SYNTAX` · **syntax-declaration, macro** — `syntax Expr ::= "Int" "(" Int ")" | "Float" "(" Float ")" | "Bool" "(" Bool ")" | "Name" "(" String ")" | "Str" "(" String ")" | "UnaryOp" "(" String "," Expr ")" [strict(2)] | "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp" "(" String "," Exprs ")" | "ListExpr" "(" Exprs ")" | "DictExpr" "(" Entries ")" | "ListComp" "(" Expr "," CompFors ")" [macro] | "GenExp" "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda" "(" Params "," Expr ")" | "KwArg" "(" String "," Expr ")" | "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call" "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare" "(" Expr "," CmpOp ")"`
2. L32 · `MPY-SYNTAX` · **syntax-declaration** — `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"`
3. L33 · `MPY-SYNTAX` · **syntax-declaration** — `syntax Entry ::= "Entry" "(" Expr "," Expr ")"`
4. L34 · `MPY-SYNTAX` · **syntax-declaration** — `syntax Entries ::= List{Entry, ","}`
5. L35 · `MPY-SYNTAX` · **syntax-declaration** — `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`
6. L36 · `MPY-SYNTAX` · **syntax-declaration** — `syntax CompFors ::= List{CompFor, ""}`
7. L37 · `MPY-SYNTAX` · **syntax-declaration** — `syntax Exprs ::= List{Expr, ","}`
8. L38 · `MPY-SYNTAX` · **syntax-declaration** — `syntax Index ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`
9. L39 · `MPY-SYNTAX` · **syntax-declaration** — `syntax Bound ::= Expr | "NoBound"`
10. L41 · `MPY-SYNTAX` · **syntax-declaration** — `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] | "Import" "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While" "(" Expr "," Stmts ")" | "Break" | "Continue" | "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return" "(" Expr ")" [strict] | "Assert" "(" Expr ")" [strict] | "Expr" "(" Expr ")" [strict] | "FuncDef" "(" String "," Params "," Stmts ")" | "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`
11. L56 · `MPY-SYNTAX` · **syntax-declaration** — `syntax Stmts ::= List{Stmt, ""}`
12. L57 · `MPY-SYNTAX` · **syntax-declaration** — `syntax Params ::= "Params" "(" ParamNames ")"`
13. L58 · `MPY-SYNTAX` · **syntax-declaration** — `syntax CellVars ::= "CellVars" "(" ParamNames ")"`
14. L59 · `MPY-SYNTAX` · **syntax-declaration** — `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"`
15. L60 · `MPY-SYNTAX` · **syntax-declaration** — `syntax ParamNames ::= List{String, ","}`
16. L61 · `MPY-SYNTAX` · **syntax-declaration** — `syntax Module ::= "Module" "(" Stmts ")"`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics/tuple.k

1. L10 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>`
2. L11 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>`
3. L14 · `MPY-TUPLE` · **syntax-declaration** — `syntax ApplyK ::= "toTuple"`
4. L15 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`
5. L16 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`
6. L18 · `MPY-TUPLE` · **ordinary-rule** — `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B`
7. L20 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`
8. L21 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>`
9. L23 · `MPY-TUPLE` · **ordinary-rule** — `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`
10. L24 · `MPY-TUPLE` · **syntax-declaration, function** — `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`
11. L25 · `MPY-TUPLE` · **ordinary-rule** — `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`
12. L26 · `MPY-TUPLE` · **ordinary-rule** — `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)`
13. L28 · `MPY-TUPLE` · **ordinary-rule** — `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)`
14. L31 · `MPY-TUPLE` · **syntax-declaration** — `syntax KItem ::= #bindTgt(Expr, Val)`
15. L32 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
16. L35 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes>`
17. L42 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
18. L43 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
19. L44 · `MPY-TUPLE` · **ordinary-rule, priority** — `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
20. L49 · `MPY-TUPLE` · **syntax-declaration** — `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`
21. L50 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
22. L51 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
23. L52 · `MPY-TUPLE` · **ordinary-rule, priority** — `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
24. L55 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`
25. L57 · `MPY-TUPLE` · **ordinary-rule** — `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`

## /tmp/audit-work/candidate-clean/reference-semantics/semantics.k


## /tmp/audit-work/candidate-clean/verification.k

1. L7 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, macro** — `syntax Stmts ::= "#specialElementBody" [macro]`
2. L8 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule #specialElementBody => If(Compare(Name("num"), CmpOp(">", Int(10))), Assign(Name("digits"), Call(Name("str"), Name("num"))) If(BoolOp("and", Compare(Subscript(Name("digits"), Int(0)), CmpOp("in", Str("13579"))), Compare(Subscript(Name("digits"), UnaryOp("-", Int(1))), CmpOp("in", Str("13579")))), AugAssign(Name("count"), "+", Int(1)), .Stmts), .Stmts)`
3. L20 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, macro** — `syntax Stmts ::= "#specialFunctionBody" [macro]`
4. L21 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule #specialFunctionBody => Assign(Name("count"), Int(0)) Assign(Name("num"), Int(0)) Assign(Name("digits"), Str("")) For(Name("num"), Name("nums"), #specialElementBody) Return(Name("count"))`
5. L28 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, macro** — `syntax Module ::= "#specialModule" [macro]`
6. L29 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule #specialModule => Module(FuncDef("specialFilter", Params("nums"), #specialFunctionBody))`
7. L36 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax IntSeq ::= decimalCodes(Int) [function, total, symbol(decimalCodes), no-evaluators]`
8. L38 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Int ::= decimalLength(Int) [function, total, symbol(decimalLength), no-evaluators]`
9. L40 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total, no-evaluators, symbol, opaque-symbol** — `syntax Int ::= decimalCodeAt(Int, Int) [function, total, symbol(decimalCodeAt), no-evaluators]`
10. L43 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **simplification-rule** — `rule strToCodes(Int2String(N:Int)) => decimalCodes(N) [simplification]`
11. L45 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **simplification-rule** — `rule isLen(decimalCodes(N:Int)) => decimalLength(N) [simplification]`
12. L47 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **simplification-rule** — `rule intSeqAt(decimalCodes(N:Int), I:Int) => decimalCodeAt(N, I) [simplification]`
13. L51 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total** — `syntax Str ::= decimalString(Int) [function, total]`
14. L52 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule decimalString(N:Int) => str(strToCodes(Int2String(N)))`
15. L56 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total** — `syntax Bool ::= hasOddEndDigits(Int) [function, total]`
16. L57 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule hasOddEndDigits(N:Int) => strContains( iCons(intSeqAt(strToCodes(Int2String(N)), 0), .IntSeq), strToCodes("13579")) andBool strContains( iCons(intSeqAt(strToCodes(Int2String(N)), -1 +Int isLen(strToCodes(Int2String(N)))), .IntSeq), strToCodes("13579"))`
17. L68 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total** — `syntax Int ::= boolAsInt(Bool) [function, total]`
18. L69 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule boolAsInt(true) => 1`
19. L70 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule boolAsInt(false) => 0`
20. L73 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total** — `syntax Int ::= specialBit(Int) [function, total]`
21. L74 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule specialBit(N:Int) => #if N >Int 10 #then boolAsInt(hasOddEndDigits(N)) #else 0 #fi`
22. L83 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration** — `syntax ValSeq ::= intVals(IntSeq)`
23. L84 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule <k> #iterNext(list(intVals(.IntSeq))) => #iterDone ... </k>`
24. L86 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule <k> #iterNext(list(intVals(iCons(N:Int, REST:IntSeq)))) => #iterYield(N, list(intVals(REST))) ... </k>`
25. L90 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total** — `syntax Int ::= specialCount(IntSeq) [function, total]`
26. L91 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule specialCount(.IntSeq) => 0`
27. L92 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule specialCount(iCons(N:Int, REST:IntSeq)) => specialBit(N) +Int specialCount(REST)`
28. L95 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total** — `syntax Int ::= finalNum(Int, IntSeq) [function, total]`
29. L96 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule finalNum(OLD:Int, .IntSeq) => OLD`
30. L97 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule finalNum(_:Int, iCons(N:Int, REST:IntSeq)) => finalNum(N, REST)`
31. L100 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **syntax-declaration, function, total** — `syntax Str ::= finalDigits(Str, IntSeq) [function, total]`
32. L101 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule finalDigits(OLD:Str, .IntSeq) => OLD`
33. L102 · `SPECIALFILTER-VERIFICATION-SYNTAX` · **ordinary-rule** — `rule finalDigits(OLD:Str, iCons(N:Int, REST:IntSeq)) => finalDigits( #if N >Int 10 #then decimalString(N) #else OLD #fi, REST)`
34. L119 · `SPECIALFILTER-VERIFICATION` · **ordinary-rule** — `rule <k> #loop(list(intVals(NS:IntSeq)), Name("num"), #specialElementBody) => .K </k> <env> 1 </env> <scopes> 1 |-> scope( "nums" |-> list(intVals(ALL:IntSeq)) "count" |-> C:Int "num" |-> OLDNUM:Int "digits" |-> OLDDIGITS:Str, parent(0)) 0 |-> scope(GLOBAL:Map, parent(-1)) -1 |-> scope(BUILTINMAP:Map, root) => 1 |-> scope( "nums" |-> list(intVals(ALL)) "count" |-> C +Int specialCount(NS) "num" |-> finalNum(OLDNUM, NS) "digits" |-> finalDigits(OLDDIGITS, NS), parent(0)) 0 |-> scope(GLOBAL, parent(-1)) -1 |-> scope(BUILTINMAP, root) </scopes>`
